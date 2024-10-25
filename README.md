# GitHub Automation Bot

![Maintained](https://img.shields.io/badge/Maintained-yes-green.svg)

This project is a GitHub automation tool written in Python, designed to help users automate common GitHub actions such as following, unfollowing, starring repositories, and managing starred repositories. This bot is **actively maintained**.

## Features

- 🧹 **Unfollow users** who do not follow you back.
- 👥 **Follow users** from a specific GitHub account.
- ⭐ **Automatically star** repositories of followed users.
- 🗑️ **Delete all starred repositories**.
- 🔍 **Search and display** the most followed users from your following list.

## Prerequisites

Ensure you have the following software installed:

1. **Python 3.x**: Check Python installation:

   ```bash
   python --version
   ```

   #### If Python is not installed, download and install it from the official [Python website](https://www.python.org/downloads/).

2. **pip**: Python’s package manager to install dependencies:

   ```bash
   pip --version
   ```

3. **Generate a GitHub Personal Access Token (PAT)**

   1. Go to [GitHub Developer Settings](https://github.com/settings/tokens) and click **Generate new token**.
   2. Under **Select Scopes**, choose the following permissions:
      - **`public_repo`**: Allows the bot to access and interact with public repositories (e.g., starring repositories).
      - **`read:user`**: Grants read access to your GitHub profile information.
      - **`user:follow`**: Enables the bot to follow and unfollow other GitHub users on your behalf.
   3. Click **Generate token** and copy the token immediately.
   4. Save this token to the `.env` file (see the next step).

---

## Project Setup

Follow these steps to get the project up and running:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/rubsxyz/GitHubScript.git
   ```

2. **Navigate into the project folder:**

   ```bash
   cd GitHubScript
   ```

3. **Install Dependencies**

   Install the required Python libraries using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   1. In the root directory of the project, locate the `.env-example` file.
   2. Open the file and replace the placeholder values with your GitHub Personal Access Token and username:

      ```bash
      GITHUB_TOKEN=your_github_token_here
      GITHUB_USERNAME=your_github_username_here
      ```

   3. After updating the values, **rename** the file from `.env-example` to `.env`:

      ```bash
      mv .env-example .env
      ```

   4. Ensure that `your_github_token_here` and `your_github_username_here` are correctly replaced with your actual GitHub token and username.

5. **Run the Script**

   Run the main menu by executing the `main.py` script:

   ```bash
   python main.py
   ```

6. **Choose an Option from the Menu**

   Once the script is running, you'll see the following menu options:

   ```markdown
   ==================================================
   GITHUB BOT MENU
   ==================================================
   Welcome to your GitHub automation tool!
   Please select one of the options below:
   ==================================================

   1. 🧹 Run Unfollow Script (Unfollow users who don't follow you back)
   2. 👥 Run Follow Script
   3. ⭐ Delete All Starred Repositories
   4. 🔍 Search Most Followed Users in Your Following
   5. ❌ Exit
      Enter your choice (1/2/3/4/5):
   ```

   Select an option, and follow the prompts to perform actions such as unfollowing, following, deleting starred repositories, searching for the most followed users, or exiting the program.

## How It Works

- **Unfollow Script**: Automatically unfollows users who are not following you back.
- **Follow Script**: Allows you to follow users from a specific GitHub account's followers. You can choose to star their repositories as well.
- **Delete All Starred Repositories**: Removes (unstars) all repositories you have previously starred.
- **Search Most Followed Users in Your Following**: Displays the top 10 users you are following based on their follower counts.

## Logging

Each script maintains its own log file stored in the `logs/` directory:

- **`main.log`**: Logs user interactions and overall script executions.
- **`follower_manager.log`**: Logs actions related to following users and starring repositories.
- **`unfollower_manager.log`**: Logs actions related to unfollowing users.

**Note**: Log files are overwritten each time you run the scripts to ensure logs are clear and up-to-date.

## License

This project is licensed under the `MIT License` - see the [LICENSE](LICENSE) file for details.

---
