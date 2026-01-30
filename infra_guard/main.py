def terraform_entry():
    # from terraform_guard.app.main import main as terraform_main
    from infra_guard.terraform_guard.app.main import main as terraform_main
    terraform_main()


def ansible_entry():
    # from ansible_guard.app.main import main as ansible_main
    from infra_guard.ansible_guard.app.main import main as ansible_main
    ansible_main()


def main():
    while True:
        print("\n=========== Infra Guard ===========")
        print("1. Terraform Guard")
        print("2. Ansible Guard")
        print("3. Exit")
        print("==================================")

        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            terraform_entry()

        elif choice == "2":
            ansible_entry()

        elif choice == "3":
            print("👋 Exiting Infra Guard")
            break

        else:
            print("❌ Invalid option")


if __name__ == "__main__":
    main()
