# OpenPI: Practical "How-To" Guide

This guide is your actionable cheat sheet for using the `openpi` repository. If you want to know "how do I do X?", you are in the right place.

## 1. How to Set Up Your Environment
Before you do anything, you need to install the dependencies. The repository uses `uv` for lightning-fast Python package management.

**Do this:**
```bash
# 1. Clone the repo with all submodules (like LeRobot)
git clone --recurse-submodules git@github.com:Physical-Intelligence/openpi.git
cd openpi

# 2. Sync dependencies using uv (GIT_LFS_SKIP_SMUDGE prevents downloading massive LeRobot datasets during setup)
GIT_LFS_SKIP_SMUDGE=1 uv sync
GIT_LFS_SKIP_SMUDGE=1 uv pip install -e .
```
*Note: Make sure you have at least an RTX 4090 (24GB VRAM) for fine-tuning LoRA, or an A100/H100 (80GB VRAM) for full fine-tuning.*

---

## 2. How to Run a Pre-Trained Model (Inference)
If you want to see the model predict an action from an image and a text prompt without running a physical robot.

**Do this:**
1. Open the `examples/inference.ipynb` notebook.
2. Run the cells. Under the hood, it does this:
```python
from openpi.training import config as _config
from openpi.policies import policy_config
from openpi.shared import download

# 1. Load the configuration for a specific model (e.g., pi05_droid)
config = _config.get_config("pi05_droid")

# 2. Download the pre-trained weights from Google Cloud
checkpoint_dir = download.maybe_download("gs://openpi-assets/checkpoints/pi05_droid")

# 3. Create the policy
policy = policy_config.create_trained_policy(config, checkpoint_dir)

# 4. Pass in dummy (or real) data to get an action
example = {
    "observation/exterior_image_1_left": ..., # Your camera image
    "observation/wrist_image_left": ...,      # Your wrist camera image
    "prompt": "pick up the fork"              # What you want it to do
}
action_chunk = policy.infer(example)["actions"]
print(action_chunk)
```

---

## 3. How to Deploy the Model for a Physical Robot (Remote Inference)
Usually, the robot's onboard computer isn't powerful enough to run a massive VLA model. You run the model on a heavy GPU server, and the robot talks to it over the network.

**Do this on your GPU Server:**
```bash
# This starts a WebSocket server on port 8000 hosting the model
uv run scripts/serve_policy.py policy:checkpoint --policy.config=pi05_droid --policy.dir=gs://openpi-assets/checkpoints/pi05_droid
```

**Do this on your Physical Robot:**
1. Install the client package on your robot: `pip install packages/openpi-client`
2. Write a script that connects to your server:
```python
from openpi_client import websocket_client

# Connect to the GPU server
client = websocket_client.WebsocketClient("ws://<YOUR_GPU_SERVER_IP>:8000")

# Inside your robot control loop:
observation = {"image": current_camera_frame, "prompt": "fold the towel"}
action = client.infer(observation)
# Execute 'action' on your robot's motors
```

---

## 4. How to Fine-Tune the Model on Your Own Data
If the base model doesn't know how to use your specific robot or do your specific task, you need to fine-tune it.

**Step 1: Convert your data to LeRobot format.**
You must format your recorded robot demonstrations into a HuggingFace `lerobot` dataset.
*Example script:* Look at `examples/libero/convert_libero_data_to_lerobot.py` and adapt it for your own data.

**Step 2: Create a Configuration**
Open `src/openpi/training/config.py` and create a new configuration (copy an existing one like `pi05_libero`) that points to your new dataset.

**Step 3: Compute Normalization Stats**
The model needs to know the mean/std bounds of your robot's joints.
```bash
uv run scripts/compute_norm_stats.py --config-name <YOUR_CONFIG_NAME>
```

**Step 4: Start Training**
```bash
# XLA_PYTHON_CLIENT_MEM_FRACTION=0.9 tells JAX it's allowed to use 90% of your GPU memory
XLA_PYTHON_CLIENT_MEM_FRACTION=0.9 uv run scripts/train.py <YOUR_CONFIG_NAME> --exp-name=my_first_finetune
```

---

## 5. How to use PyTorch instead of JAX
If you prefer PyTorch (e.g., you want to use standard HuggingFace/PyTorch tooling), the repository fully supports it!

**Do this to fix PyTorch Transformers dependency:**
```bash
# Apply a required patch to the transformers library to fix caching and precision bugs
cp -r ./src/openpi/models_pytorch/transformers_replace/* .venv/lib/python3.11/site-packages/transformers/
```

**Do this to train in PyTorch:**
Use `train_pytorch.py` instead of `train.py`.
```bash
# Single GPU training
uv run scripts/train_pytorch.py <YOUR_CONFIG_NAME> --exp_name pytorch_test

# Multi-GPU training
uv run torchrun --standalone --nnodes=1 --nproc_per_node=2 scripts/train_pytorch.py <YOUR_CONFIG_NAME> --exp_name pytorch_ddp_test
```

**Do this to convert existing JAX weights to PyTorch:**
```bash
uv run examples/convert_jax_model_to_pytorch.py \
    --config_name <CONFIG_NAME> \
    --checkpoint_dir /path/to/jax/base/model \
    --output_path /path/to/pytorch/base/model
```

---

## Summary Checklist for a New Project:
1. [ ] Collect data on your robot.
2. [ ] Write a script to convert your data into a `lerobot` dataset.
3. [ ] Define a `Policy` mapping in `src/openpi/policies/` so the model knows what your state/actions mean.
4. [ ] Create a training config in `src/openpi/training/config.py`.
5. [ ] Run `compute_norm_stats.py`.
6. [ ] Run `train.py` to fine-tune.
7. [ ] Start `serve_policy.py` on your GPU.
8. [ ] Point your robot's control script to the WebSocket server using `openpi-client`.
