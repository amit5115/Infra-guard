# import sys
# from plan_utils import load_plan, plan_counts
# from plan_analyzer import get_destructive_resources
# from ai_advisor import explain_risk
# from ui import header, success, warning, error, show_plan_summary, show_ai_output
# from plan_utils import plan_exists
# from plan_analyzer import get_all_resource_changes
# from ai_advisor import explain_all_changes
# from plan_utils import tf_files_changed, save_tf_hash
# from cost_engine import calculate_cost_impact
# from ai_advisor import explain_cost_impact
# from ui import show_cost_impact
# from cost_guard import is_cost_allowed
# from cost_trend import save_trend, get_latest_trend
# from ui import show_cost_trend
# import subprocess
# import os



import sys
import subprocess
import os
from rich.console import Console
from .env_loader import set_env, generate_tfvars
from .audit_logger import log_event

from .plan_utils import (
    load_plan,
    plan_counts,
    plan_exists,
    tf_files_changed,
    save_tf_hash
)

from .plan_analyzer import (
    get_destructive_resources,
    get_all_resource_changes
)

from .ai_advisor import (
    explain_all_changes,
    explain_cost_impact
)

from .cost_engine import calculate_cost_impact
from .cost_guard import is_cost_allowed
from .cost_trend import load_last_cost, save_current_cost

from .ui import (
    header,
    success,
    warning,
    error,
    show_plan_summary,
    show_ai_output,
    show_cost_impact
)

console = Console()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TERRAFORM_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "../terraform")
)

PLANS_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "../plans")
)

# STATE_DIR = os.path.join(TERRAFORM_DIR, "state")
# os.makedirs(STATE_DIR, exist_ok=True)


# ---------------------------------------------------
# COST UI
# ---------------------------------------------------
def cost_ui():
    header("Cost Impact Analyzer")

    ensure_latest_plan(force=False)

    costs, total = calculate_cost_impact()

    if not costs:
        success("No cost-impacting changes detected")
        return

    show_cost_impact(costs, total)

    last_total = load_last_cost()

    if last_total is not None:
        diff = total - last_total

        if diff > 0:
            msg = f"📈 Cost increased by ${diff} (previous ${last_total})"
            style = "bold red"
        elif diff < 0:
            msg = f"📉 Cost decreased by ${abs(diff)} (previous ${last_total})"
            style = "bold green"
        else:
            msg = f"➖ Cost unchanged (${total})"
            style = "bold cyan"

        console.print(msg, style=style)

    save_current_cost(total)

    log_event("COST_ANALYSIS_RUN", f"Total change: ${total}")

    ai_text = explain_cost_impact(costs)
    show_ai_output(ai_text)

# # ---------------------------------------------------
# # TERRAFORM PLAN
# # ---------------------------------------------------
# def run_terraform_plan():
#     header("Terraform Plan Generator")

#     os.makedirs(PLANS_DIR, exist_ok=True)

#     success("Running terraform init")
#     subprocess.run(
#         ["terraform", "init", "-input=false"],
#         cwd=TERRAFORM_DIR,
#         stdout=subprocess.DEVNULL,
#         stderr=subprocess.DEVNULL,
#         check=True
#     )

#     success("Running terraform plan")
#     subprocess.run(
#         ["terraform", "plan", "-out",
#          os.path.join(PLANS_DIR, "plan.out")],
#         cwd=TERRAFORM_DIR,
#         stdout=subprocess.DEVNULL,
#         stderr=subprocess.DEVNULL,
#         check=True
#     )

#     success("Converting plan to JSON")
#     with open(os.path.join(PLANS_DIR, "plan.json"), "w") as f:
#         subprocess.run(
#             ["terraform", "show", "-json",
#              os.path.join(PLANS_DIR, "plan.out")],
#             cwd=TERRAFORM_DIR,
#             stdout=f,
#             stderr=subprocess.DEVNULL,
#             check=True
#         )

#     success("Terraform plan.json generated successfully")
#     log_event("PLAN_GENERATED")

# # ---------------------------------------------------
# # PLAN CHECK
# # ---------------------------------------------------
# def ensure_latest_plan(force=False):
#     if plan_exists() and not force and not tf_files_changed():
#         warning("Using existing Terraform plan for analysis")
#         return

#     warning("Terraform files changed or plan missing")
#     warning("Generating fresh Terraform plan...")
#     run_terraform_plan()
#     save_tf_hash()

# # ---------------------------------------------------
# # APPLY PHASE
# # ---------------------------------------------------
# def apply_phase():
#     header("Terraform Apply")

#     log_event("APPLY_ATTEMPT")

#     ensure_latest_plan(force=True)

#     costs, total = calculate_cost_impact()
#     allowed, total = is_cost_allowed(costs)

#     if not allowed:
#         error(f"Cost limit exceeded: ${total}/month")
#         error("Apply is BLOCKED by cost guardrail")
#         log_event("APPLY_BLOCKED_COST", f"${total}")
#         return

#     destructive = get_destructive_resources()

#     if destructive:
#         error("Destructive changes detected")

#         confirm = input(
#             "⚠️ Destructive changes found. Continue anyway? (yes/no): "
#         ).strip().lower()

#         if confirm != "yes":
#             warning("Apply aborted by user.")
#             log_event("APPLY_ABORTED_DESTRUCTIVE")
#             return

#     success("Applying Terraform...")

#     subprocess.run(
#         ["terraform", "apply", "-auto-approve"],
#         cwd=TERRAFORM_DIR,
#         check=True
#     )

#     success("Terraform apply completed successfully")
#     log_event("APPLY_SUCCESS")


# def destroy_phase():
#     header("Terraform Destroy")

#     log_event("DESTROY_ATTEMPT")

#     confirm = input(
#         "⚠️ This will DESTROY infrastructure. Continue? (yes/no): "
#     ).strip().lower()

#     if confirm != "yes":
#         warning("Destroy aborted by user.")
#         log_event("DESTROY_ABORTED")
#         return

#     success("Destroying infrastructure...")

#     subprocess.run(
#         ["terraform", "destroy", "-auto-approve"],
#         cwd=TERRAFORM_DIR,
#         check=True
#     )

#     success("Terraform destroy completed")
#     log_event("DESTROY_SUCCESS")



# ---------------------------------------------------
# env_centric op
# ---------------------------------------------------
# ---------------------------------------------------
# TERRAFORM PLAN
# ---------------------------------------------------
def run_terraform_plan():
    header("Terraform Plan Generator")
    generate_tfvars()

    # plan file paths
    plan_file = os.path.join(PLANS_DIR, "plan.out")
    plan_json = os.path.join(PLANS_DIR, "plan.json")

    # remove old plan files
    if os.path.exists(plan_file):
        os.remove(plan_file)

    if os.path.exists(plan_json):
        os.remove(plan_json)

    success("Running terraform init")
    subprocess.run(
        ["terraform", "init", "-input=false"],
        cwd=TERRAFORM_DIR,
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL,
        check=True
    )

    success("Running terraform plan")
    subprocess.run(
        [
            "terraform",
            "plan",
            "-out",
            os.path.join(PLANS_DIR, "plan.out")
        ],
        cwd=TERRAFORM_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

    success("Converting plan to JSON")
    with open(os.path.join(PLANS_DIR, "plan.json"), "w") as f:
        subprocess.run(
            [
                "terraform",
                "show",
                "-json",
                os.path.join(PLANS_DIR, "plan.out")
            ],
            cwd=TERRAFORM_DIR,
            stdout=f,
            stderr=subprocess.DEVNULL,
            check=True
        )

    success("Terraform plan.json generated successfully")
    log_event("PLAN_GENERATED")

# ---------------------------------------------------
# PLAN CHECK
# ---------------------------------------------------
def ensure_latest_plan(force=False):
    # Always regenerate tfvars from YAML
    try:
        generate_tfvars()
        success("Environment config loaded")
    except Exception as e:
        warning(f"Could not regenerate tfvars: {e}")

    if plan_exists() and not force and not tf_files_changed():
        warning("Using existing Terraform plan for analysis")
        return

    warning("Terraform files changed or plan missing")
    warning("Generating fresh Terraform plan...")
    run_terraform_plan()
    save_tf_hash()


# ---------------------------------------------------
# APPLY PHASE
# ---------------------------------------------------
def apply_phase():
    header("Terraform Apply")

    log_event("APPLY_ATTEMPT")

    ensure_latest_plan(force=True)

    costs, total = calculate_cost_impact()
    allowed, total = is_cost_allowed(costs)

    if not allowed:
        error(f"Cost limit exceeded: ${total}/month")
        error("Apply is BLOCKED by cost guardrail")
        log_event("APPLY_BLOCKED_COST", f"${total}")
        return

    destructive = get_destructive_resources()

    if destructive:
        error("Destructive changes detected")

        confirm = input(
            "⚠️ Destructive changes found. Continue anyway? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            warning("Apply aborted by user.")
            log_event("APPLY_ABORTED_DESTRUCTIVE")
            return

    success("Applying Terraform...")

    subprocess.run(
        ["terraform", "apply", "-auto-approve"],
        cwd=TERRAFORM_DIR,
        check=True
    )

    success("Terraform apply completed successfully")
    log_event("APPLY_SUCCESS")

# ---------------------------------------------------
# DESTROY PHASE
# ---------------------------------------------------
def destroy_phase():
    header("Terraform Destroy")

    log_event("DESTROY_ATTEMPT")

    confirm = input(
        "⚠️ This will DESTROY infrastructure. Continue? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        warning("Destroy aborted by user.")
        log_event("DESTROY_ABORTED")
        return

    success("Destroying infrastructure...")

    subprocess.run(
        ["terraform", "destroy", "-auto-approve"],
        cwd=TERRAFORM_DIR,
        check=True
    )

    success("Terraform destroy completed")
    log_event("DESTROY_SUCCESS")


# ---------------------------------------------------
# MENU
# ---------------------------------------------------
def interactive_menu():
    while True:
        print("\n================ Terraform Guard Menu ================")
        print("1. Load & Show Terraform Plan Summary")
        print("2. AI Risk Analysis")
        print("3. Cost Impact Analysis")
        print("4. Apply Terraform (only if safe)")
        print("5. Destroy Infrastructure")
        print("6. Exit")
        print("=====================================================")

        choice = input("Select an option (1-6): ").strip()

        if choice in ["6", "exit", "quit", "q"]:
            print("👋 Exiting Terraform Guard")
            break

        elif choice == "1":
            header("Terraform Plan Inspector")
            ensure_latest_plan(force=True)
            terraform_ui()

        elif choice == "2":
            ai_ui()

        elif choice == "3":
            cost_ui()

        elif choice == "4":
            apply_phase()

        elif choice == "5":
            destroy_phase()

        else:
            print("❌ Invalid option")


# ---------------------------------------------------
# PLAN SUMMARY
# ---------------------------------------------------
def terraform_ui():
    header("Terraform Plan Inspector")

    ensure_latest_plan()

    plan = load_plan()
    add, change, destroy = plan_counts(plan)

    success("Terraform plan loaded successfully")
    show_plan_summary(add, change, destroy)

# ---------------------------------------------------
# AI ANALYSIS
# ---------------------------------------------------
def ai_ui():
    log_event("AI_ANALYSIS_RUN")

    header("AI Risk Analyzer")

    ensure_latest_plan()

    changes = get_all_resource_changes()

    if not changes:
        success("No infrastructure changes detected")
        return

    ai_text = explain_all_changes(changes)
    show_ai_output(ai_text)

# ---------------------------------------------------
# ENTRY
# ---------------------------------------------------
def main():
    # ✅ Environment selection
    env = input("Select environment (dev/prod): ").strip().lower()
    set_env(env)
    generate_tfvars()

    # Existing logic
    if len(sys.argv) == 1:
        interactive_menu()
        return

    mode = sys.argv[1].lower()

    if mode == "plan":
        run_terraform_plan()

    elif mode in ["terraform", "summary"]:
        terraform_ui()

    elif mode == "ai":
        ai_ui()

    elif mode == "apply":
        apply_phase()

    else:
        print("Usage:")
        print("  python3 main.py")


if __name__ == "__main__":
    main()
