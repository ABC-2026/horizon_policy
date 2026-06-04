# Project File Structure (excluding .git and .vscode)

```
openpi/
├─ .dockerignore
├─ .github/
│  ├─ CODEOWNERS
│  └─ workflows/
│     ├─ pre-commit.yml
│     └─ test.yml
├─ .gitignore
├─ .gitmodules
├─ .pre-commit-config.yaml
├─ .python-version
├─ CONTRIBUTING.md
├─ LICENSE
├─ LICENSE_GEMMA.txt
├─ README.md
├─ docs/
├─ examples/
│  ├─ aloha_real/
│  │  ├─ Dockerfile
│  │  ├─ README.md
│  │  ├─ compose.yml
│  │  ├─ constants.py
│  │  ├─ convert_aloha_data_to_lerobot.py
│  │  ├─ env.py
│  │  ├─ main.py
│  │  ├─ real_env.py
│  │  ├─ requirements.in
│  │  ├─ requirements.txt
│  │  ├─ robot_utils.py
│  │  └─ video_display.py
│  ├─ aloha_sim/
│  │  ├─ Dockerfile
│  │  ├─ README.md
│  │  ├─ compose.yml
│  │  ├─ env.py
│  │  ├─ main.py
│  │  ├─ requirements.in
│  │  ├─ requirements.txt
│  │  ├─ saver.py
│  │  └─ (other files…) 
│  ├─ droid/ (contents omitted)
│  ├─ libero/ (contents omitted)
│  ├─ simple_client/ (contents omitted)
│  ├─ ur5/ (contents omitted)
│  └─ convert_jax_model_to_pytorch.py
├─ infotoread.md
├─ packages/
│  └─ openpi-client/
├─ pyproject.toml
├─ scripts/
│  ├─ __init__.py
│  ├─ compute_norm_stats.py
│  ├─ docker/ (contents omitted)
│  ├─ serve_policy.py
│  ├─ train.py
│  ├─ train_pytorch.py
│  └─ train_test.py
├─ src/
│  ├─ __init__.py
│  ├─ conftest.py
│  ├─ models/ (contents omitted)
│  ├─ models_pytorch/ (contents omitted)
│  ├─ policies/ (contents omitted)
│  ├─ py.typed
│  ├─ serving/ (contents omitted)
│  ├─ shared/ (contents omitted)
│  ├─ training/ (contents omitted)
│  ├─ transforms.py
│  └─ transforms_test.py
├─ third_party/ (contents omitted)
├─ to_use.md
└─ uv.lock
```
