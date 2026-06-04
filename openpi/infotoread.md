# OpenPI Repository Learning Guide

Welcome to the `openpi` repository! This guide is designed to help you navigate, learn, and eventually rebuild or modify the Vision-Language-Action (VLA) models (like $\pi_0$, $\pi_0$-FAST, and $\pi_{0.5}$) provided by the Physical Intelligence team.

## High-Level Overview: What is this repository?
This repository contains the training, inference, and model definitions for **Vision-Language-Action (VLA)** models. These are AI models that take in:
1. **Vision**: Images from robot cameras (e.g., wrist cameras, external cameras)
2. **Language**: A text prompt of what to do (e.g., "pick up the fork")
3. **Action**: The model outputs a sequence of motor commands (action chunks) to physically move the robot.

## Core Technical Stack & Frameworks

### 1. The JAX Deep Learning Ecosystem (Primary Training & Inference)
The repository leverages **JAX** as its core computation engine, taking advantage of its high performance, composability, and TPU/GPU optimization capabilities:
*   **JAX (`jax`)**: Used for functional programming, automatic differentiation, and compilation via XLA. Key primitives like `jax.jit` (Just-In-Time compilation), `jax.vmap` (vectorized mapping), and `jax.lax.while_loop` are central to high-speed action sampling.
*   **Equinox (`equinox`)**: Used as the primary neural network framework on top of JAX. It represents neural network parameters and states as PyTrees, ensuring pure functional model transformations.
*   **Flax & NNX (`flax`)**: Integrates model structures and parameter groups using Flax's new NNX module APIs and `flax.nnx.bridge.ToNNX` to support stateful neural network designs.
*   **Optax (`optax`)**: Powers optimization pipelines with robust gradient clipping, AdamW optimizers, and Cosine Decay learning rate schedulers with warmup steps.
*   **Orbax-Checkpoint (`orbax-checkpoint`)**: Manages model checkpointing, saving, and asynchronous restoration of dense PyTree weights and optimizer states.
*   **Chex & Jaxtyping (`chex`, `jaxtyping`)**: Enforces runtime type-checking, array shape assertions, and debugging utilities across functional parameters.

### 2. The PyTorch & Hugging Face Ecosystem (Alternative Backend)
For users integrated into the PyTorch infrastructure, the codebase offers a complete mirroring of the core architecture:
*   **PyTorch (`torch`)**: Powers the alternative training loops (`train_pytorch.py`) and supports Distributed Data Parallel (DDP) scaling across multi-GPU setups via `torchrun`.
*   **Hugging Face Transformers (`transformers`)**: Used to import and fine-tune Gemma LLM layers, incorporating custom patches (overriding standard attention/precision layers) to fix inference caching and numerical precision bottlenecks.

### 3. Robotic Datasets & Environments
Data loading, preparation, and formatting rely on modern standardizations:
*   **LeRobot (`lerobot`)**: Hugging Face's open-source framework for robot learning. It provides a standardized data format, data-saving schemas, and unified PyTorch dataset utilities.
*   **dlimp**: A specialized library built on top of `tf.data` for ultra-fast, multi-threaded RLDS (Robot Learning Dataset) loading and pre-processing (used heavily in `scripts/compute_norm_stats.py` and RLDS dataset pipelines).
*   **Gym-Aloha (`gym-aloha`)**: Reinforcement learning environment integrations for simulating ALOHA robot arms.

### 4. Supporting Libraries & Utilities
*   **Einops (`einops`)**: Simplifies multidimensional tensor manipulation (rearranging, repeating, and contracting shapes) for stitching image embeddings and action history tokens.
*   **Augmax (`augmax`)**: Provides JAX-compatible, differentiable image augmentations (cropping, color-jittering, normalization) within the functional JAX data pipeline.
*   **FastAPI & Uvicorn**: Serves real-time inference endpoints via high-throughput ASGI servers.
*   **Msgpack**: Handles low-latency, lightweight binary serialization/deserialization of high-frequency camera frames and joint vectors sent between the robot client and the GPU server.
*   **Tyro & Numpydantic**: Simplifies CLI argument configuration parsing and enforces pydantic-style data validation on numpy matrices.

---

## Core Techniques & Architectures

### 1. Continuous Action Generation via Flow Matching
Instead of casting robot action prediction as simple regression (which suffers under multimodal distributions) or discrete autoregression, models like $\pi_0$ and $\pi_{0.5}$ employ **Flow Matching**:
*   **Probability Path Matching**: The model defines a probability vector field $v_t$ that transports a simple source distribution (standard Gaussian noise at $t=1$) to the target action distribution (real robot trajectories at $t=0$).
*   **Objective Function**: During training, a random timestep $t \sim \text{Beta}(1.5, 1)$ is sampled. Noisy action trajectories $x_t = t \cdot \epsilon + (1 - t) \cdot x_{\text{target}}$ (where $\epsilon \sim \mathcal{N}(0, I)$) are computed. The model is trained to minimize the mean squared error between its predicted velocity $v_t$ and the target velocity vector $u_t = \epsilon - x_{\text{target}}$.
*   **Action Sampling Loop**: At inference time, the model draws a pure Gaussian noise tensor and runs a numerical integration loop (e.g., Euler integration over $10$ or $15$ steps) using `jax.lax.while_loop` to iteratively denoise the action candidate down to the target action.

### 2. Visual-Language Tokenization & Joint Attention
The architecture stitches vision encoders and Large Language Models together into a unified sequence:
*   **Image Tokenization**: Robotic camera inputs (wrist and external cameras) are processed through a vision encoder like **SigLIP** (specifically the `So400m/14` variant). Images are projected into spatial visual tokens.
*   **Prompt Tokenization**: Human instructions are tokenized via a `SentencePiece` tokenizer.
*   **Prefix-LM Causal Attention**: Bidirectional attention is used for the *Prefix* (images + text prompt) so all input tokens can attend to each other fully. A causal attention mask is dynamically constructed for the *Suffix* (proprioceptive state + actions), preventing the model from looking ahead in time while allowing actions to query all visual and text context.

### 3. Timestep Conditioning via AdaRMS & MLPs
To condition the action generation process on the diffusion/flow timestep $t$:
*   **Sine-Cosine Positional Encoding**: The scalar timestep $t \in [0, 1]$ is embedded using high-resolution sine and cosine positional encoding vectors.
*   **AdaRMS (Adaptive Root Mean Square Normalization)**: Used in $\pi_{0.5}$. The embedded timestep passes through a multi-layer perceptron (MLP) to compute scale parameters that modulate layer normalization statistics throughout the Gemma LLM layers.
*   **MLP Temporal Mixing**: In standard $\pi_0$, the timestep embeddings are mixed directly with the continuous action embeddings using linear projections and Swish activation MLPs before feeding them into the action expert layers.

### 4. Parameter-Efficient Fine-Tuning (LoRA)
Fine-tuning heavy vision-language-action models on individual robot workstations is made accessible through Low-Rank Adaptation (LoRA):
*   **Freeze Filters**: The `freeze_filter` system utilizes `nnx.All(nnx.Param, nnx.Not(self.freeze_filter))` to freeze the massive base weights of the PaliGemma and SigLIP encoders.
*   **LoRA Adapters**: Low-rank update matrices are inserted into the attention linear projections. Only these adapters are trained, reducing GPU memory requirements (VRAM) so that fine-tuning can run on consumer GPUs (e.g., RTX 4090 with 24GB VRAM) instead of multi-GPU servers (80GB A100s).

### 5. Action Chunking & Temporal Ensembling
To avoid jerky movements and account for execution latency, the models use **Action Chunking**:
*   Instead of predicting a single command for the next time-step, the model generates an entire sequence block (e.g., a horizon of $10$ or $15$ future actions).
*   During continuous control, the robot executes these overlapping chunks, smoothing out trajectories and reducing susceptibility to momentary network delays or sensor noise.

---

## Core Processes & Workflows

### 1. Data Repacking & Normalization
A robust pipeline converts raw, messy robot demonstrations into clean, standardized inputs:
*   **Repack Transforms**: Remaps dataset-specific key-value trees (e.g., differing joint naming schemas or camera channels) into unified keys like `observation/images` and `observation/state`.
*   **Normalization Statistics**: Calculated via `scripts/compute_norm_stats.py`. Joint values and gripper states are normalized using Z-score (mean/std) or Quantile Normalization to scale them within a safe $[-1, 1]$ bounding box, preventing model instability.
*   **Delta Action Conversions**: Actions are optionally transformed from absolute coordinates (e.g., joint positions in radians) to relative offsets (delta actions) relative to the robot's current pose at the beginning of each action chunk.

### 2. Prefix KV Caching for Fast Denoising
Because Flow Matching requires running $10+$ steps of inference for a single control command, re-processing the static image and language inputs on every step would be computationally prohibitive:
*   **Cache Initialization**: During step $1$ of sampling, the Prefix (images + prompt) is passed through the vision encoder and LLM to compute Key (K) and Value (V) tensors. These are stored in a **KV Cache**.
*   **Incremental Decoding**: For the remaining denoising steps, only the changing action expert tokens and timestep embeddings are sent through the model. The model retrieves the saved visual and text keys/values from the cache, dropping inference latency to a fraction of a full forward pass.

### 3. JAX-to-PyTorch Weight Translation
To allow users to switch seamlessly between frameworks:
*   `convert_jax_model_to_pytorch.py` maps the JAX PyTree parameter dictionaries directly to PyTorch state dicts.
*   The script re-orders multi-head attention weights, maps linear projections, and matches normalization parameters to ensure identical numeric outputs between JAX and PyTorch forward passes.

### 4. WebSocket Server-Client Communication
Due to weight sizes, inference is hosted on high-end local or remote servers:
*   **Serve Policy Server (`serve_policy.py`)**: Uses FastAPI/Uvicorn to spin up a WebSocket server, maintaining the model state, weights, and active KV caches in GPU memory.
*   **Robot Client (`openpi-client`)**: A lightweight client runs on the robot's companion computer. In the main control loop, it captures camera frames and joint states, encodes them using Msgpack, sends them over a local WebSocket, and immediately receives the predicted action sequence chunk to execute on the robot's motor controllers.

---

## Repository Structure: What is used for what?

### 1. `src/openpi/` (The Core Library)
This is the heart of the repository. If you want to understand how the models are built, start here.
- **`models/`**: Contains the raw JAX/Equinox neural network architectures.
  - `gemma.py` & `gemma_fast.py`: The core Large Language Model (LLM) backbone based on Google's Gemma.
  - `siglip.py` & `vit.py`: Vision Encoders used to process the camera images.
  - `pi0.py` & `pi0_fast.py`: The overall VLA models that stitch the Vision and Language parts together to predict actions (using flow-matching or autoregressive decoding).
  - `tokenizer.py`: Tokenizes the continuous robot actions into discrete tokens (for the FAST model).
  - `lora.py`: Implementation of Low-Rank Adaptation (LoRA) for efficient fine-tuning.
- **`models_pytorch/`**: The exact same architectures as above, but implemented in PyTorch.
- **`policies/`**: Bridges the gap between the raw neural networks and specific robots.
  - `aloha_policy.py`, `droid_policy.py`, `libero_policy.py`: Mappings that define how the raw model inputs/outputs translate into specific formats for ALOHA, DROID, or Libero robots.
  - `policy.py`: The abstract base class for a policy.
- **`training/`**: Contains the code for training the models.
  - `config.py`: The centralized configuration file where hyperparameters, data paths, and model sizes are defined.
- **`serving/`**: Code for hosting the model as an API/WebSocket server so a robot can query it remotely.

### 2. `scripts/` (The Entry Points)
These are the executable scripts you will run from your terminal.
- `train.py` & `train_pytorch.py`: The main training loops for fine-tuning the models in JAX or PyTorch.
- `serve_policy.py`: Starts a local server that loads a model checkpoint and waits for a robot to send images over the network to get actions back.
- `compute_norm_stats.py`: Calculates normalization statistics (mean/std) for robot state and action data before training.

### 3. `examples/` (The Tutorials)
This is the best place to learn how to *use* the codebase.
- `inference.ipynb`: A Jupyter Notebook showing a basic forward pass of the model. **(Start here!)**
- `aloha_real/`, `aloha_sim/`, `droid/`, `ur5/`, `libero/`: Specific guides and scripts for integrating the models with these respective robots/simulators.
- `simple_client/`: Shows how to write a Python script that acts like a robot and talks to the `serve_policy.py` server.
- `convert_jax_model_to_pytorch.py`: A utility to convert JAX weights to PyTorch weights.

### 4. `packages/`
- Contains `openpi-client`, which is the client-side library you install on your physical robot's computer to talk to the heavy GPU server running `serve_policy.py`.

---

## Recommended Learning Path

If you want to be able to rebuild this or build something similar, follow these steps:

### Step 1: See it in action (Inference)
1. Setup the environment using `uv sync` as described in the README.
2. Open `examples/inference.ipynb` and step through the cells. This will teach you how a model is loaded, how an observation (images + text) is formatted, and how actions are generated.

### Step 2: Understand the Architecture
1. Read `src/openpi/models/pi0.py`. This is the flow-matching VLA. Look at how it initializes the `gemma` language model and the `siglip` vision encoder. 
2. Understand the forward pass: Notice how images are embedded into tokens, concatenated with text tokens, and then processed to predict the robot's action distribution.

### Step 3: Understand the Data & Policies
1. Read `src/openpi/policies/policy.py` to see the standard interface.
2. Then look at `src/openpi/policies/aloha_policy.py` to see how real-world camera names and joint angles are normalized and reshaped into the generic tensors the model expects.

### Step 4: Follow the Training Loop
1. Look at `src/openpi/training/config.py` to see what a training configuration looks like (e.g., `pi05_libero`). Notice how it specifies the model, the data loaders, and hyperparameters.
2. Read `scripts/train.py`. Trace how it loads the dataset using LeRobot, initializes the model state, and runs the training steps. 

### Step 5: System Deployment (Robot to GPU Communication)
1. Read `scripts/serve_policy.py` to see how the model is wrapped in a WebSocket server.
2. Read the code in `examples/simple_client/` to see how a robot packs its camera images, sends them over the network, and unpacks the returned actions to execute physically.

## Key Concepts to Research Separately
To fully grasp this repository, you may need to research these underlying concepts:
- **Vision-Language Models (VLMs)**: How LLMs (like Gemma) are modified to accept image tokens.
- **Flow Matching / Diffusion Models**: The mathematical process used in $\pi_0$ and $\pi_{0.5}$ to generate continuous action sequences.
- **JAX and Equinox**: If you plan to stick with the JAX implementation, learning the basics of JAX (functional programming, `jax.jit`, `jax.vmap`) and Equinox (neural networks in JAX) is highly recommended.
