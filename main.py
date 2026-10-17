"""Launch the chess platform: python3 main.py [user|admin]."""
import argparse


def run_admin():
    from admin import generate_competition, update_results, next_round

    actions = {
        "1": generate_competition,
        "2": update_results,
        "3": next_round,
    }
    while True:
        print("\n1. Generate competition\n2. Update results\n3. Next round\n4. Exit")
        choice = input("Choose an action: ").strip()
        if choice == "4":
            return
        action = actions.get(choice)
        if action is None:
            print("Please choose 1, 2, 3, or 4.")
        else:
            action()


def main():
    parser = argparse.ArgumentParser(description="Chess competition platform")
    parser.add_argument("mode", nargs="?", choices=("user", "admin"), default="user")
    args = parser.parse_args()
    if args.mode == "admin":
        run_admin()
    else:
        from gui import run
        run()


if __name__ == "__main__":
    main()
