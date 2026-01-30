import os
import yaml
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_DIR = os.path.abspath(os.path.join(BASE_DIR, "../terraform/env"))
TF_DIR = os.path.abspath(os.path.join(BASE_DIR, "../terraform"))

# default env
CURRENT_ENV = "dev"


def set_env(env):
    global CURRENT_ENV

    env = env.lower()

    if env not in ["dev", "prod"]:
        raise ValueError("Environment must be dev or prod")

    CURRENT_ENV = env
    print(f"✅ Environment set to: {CURRENT_ENV}")


def generate_tfvars():
    env_file = os.path.join(ENV_DIR, f"{CURRENT_ENV}.yaml")

    print(f"📄 Using env file: {env_file}")

    with open(env_file) as f:
        data = yaml.safe_load(f)

    tfvars_path = os.path.join(TF_DIR, "terraform.auto.tfvars.json")

    with open(tfvars_path, "w") as f:
        json.dump(data, f, indent=2)

    print("✅ terraform.auto.tfvars.json generated")
