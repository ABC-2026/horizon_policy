'''from coppelia_env import CoppeliaYuMiEnv

env = CoppeliaYuMiEnv()

env.start()

obs = env.get_observation()

print("\n")
print("=" * 10)
print("OBSERVATION INFO")
print("=" * 10)

print()

print(
    "state shape:",
    obs["state"].shape
)

print(
    "state dtype:",
    obs["state"].dtype
)

print()

for name, img in obs["images"].items():

    print(
        name,
        img.shape,
        img.dtype
    )

env.stop()'''
from coppelia_env import CoppeliaYuMiEnv

env = CoppeliaYuMiEnv()

env.start()

obs = env.get_observation()

print("\nOBS KEYS")
print(obs.keys())

print("\nSTATE")
print(obs["state"])

print("\nSTATE SHAPE")
print(obs["state"].shape)

print("\nIMAGES")

for name, img in obs["images"].items():

    print(
        f"{name}: "
        f"shape={img.shape}, "
        f"dtype={img.dtype}, "
        f"min={img.min()}, "
        f"max={img.max()}"
    )

env.stop()