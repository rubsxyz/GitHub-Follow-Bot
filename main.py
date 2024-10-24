import os
from scripts.unfollower_manager import unfollow_script
from scripts.follower_manager import follow_specific_user, follow_random_user

def clear_screen():
    """
    Clears the terminal screen for a cleaner interface.
    Works for both Windows (cls) and Unix-based systems (clear).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_main_menu():
    """
    Prints the main menu with better formatting and appeal.
    """
    print("\n" + "=" * 50)
    print(" " * 15 + "GITHUB BOT MENU")
    print("=" * 50)
    print("Welcome to your GitHub automation tool!")
    print("Please select one of the options below:")
    print("=" * 50)
    print("1. 🧹 Run Unfollow Script (Unfollow users who don't follow you back)")
    print("2. 👥 Run Follow Script")
    print("3. ❌ Exit")
    print("=" * 50)

def print_follow_menu():
    """
    Prints the follow sub-menu with better formatting and appeal.
    """
    print("\n" + "=" * 50)
    print(" " * 18 + "FOLLOW MENU")
    print("=" * 50)
    print("1. 👤 Follow users from a specific GitHub account")
    print("2. 🌍 Randomly follow trending GitHub users")
    print("3. 🔙 Return to the main menu")
    print("=" * 50)

def main_menu():
    """
    Main menu to select between unfollowing or following scripts with a cleaner layout.
    """
    while True:
        clear_screen()  # Clear the screen before displaying the main menu
        print_main_menu()
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            clear_screen()  # Clear screen before starting the unfollow script
            unfollow_script()
        elif choice == '2':
            follow_menu()
        elif choice == '3':
            clear_screen()  # Clear screen before exiting
            print("Exiting the program. Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please select a valid option (1/2/3).")
            input("Press Enter to continue...")  # Wait for user input before refreshing the screen

def follow_menu():
    """
    Sub-menu for the follow script with a cleaner layout.
    """
    while True:
        clear_screen()  # Clear the screen before displaying the follow menu
        print_follow_menu()
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            clear_screen()  # Clear screen before starting specific user follow
            follow_specific_user()
        elif choice == '2':
            clear_screen()  # Clear screen before starting random follow
            follow_random_user()
        elif choice == '3':
            break
        else:
            print("❌ Invalid choice. Please select a valid option (1/2/3).")
            input("Press Enter to continue...")  # Wait for user input before refreshing the screen

if __name__ == "__main__":
    main_menu()
