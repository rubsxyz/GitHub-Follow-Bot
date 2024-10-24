# GitHub Automation Bot

![Maintained](https://img.shields.io/badge/Maintained-yes-green.svg)

This project is a GitHub automation tool written in Python, designed to help users automate common GitHub actions such as following, unfollowing, and starring repositories. This bot is **actively maintained**.

## Features

-   🧹 **Unfollow users** who do not follow you back.
-   👥 **Follow users** from a specific GitHub account or follow random trending users.
-   ⭐ **Automatically star** repositories of followed users.

## Prerequisites

Ensure you have the following software installed:

1. **Python 3.x**: Check Python installation:

    ```bash
    python --version
    ```

#### If Python is not installed, download and install it from the official Python website.

2. **pip**: Python’s package manager to install dependencies:

    ```bash
    pip --version
    ```

### 3. **Generate a GitHub Personal Access Token (PAT)**

1. Go to [GitHub Developer Settings](https://github.com/settings/tokens) and click **Generate new token**.
2. Under **Select Scopes**, choose the following permissions:
    - **`public_repo`**: Allows the bot to access and interact with public repositories (e.g., starring repositories).
    - **`read:user`**: Grants read access to your GitHub profile information.
    - **`user:follow`**: Enables the bot to follow and unfollow other GitHub users on your behalf.
3. Click **Generate token** and copy the token immediately.
4. Save this token to the `.env` file (see the next step).

---

### 4. **Set Up Environment Variables**

1. In the root directory of the project, locate the `.env-example` file.
2. Open the file and replace the placeholder values with your GitHub Personal Access Token and username:

    ```bash
    GITHUB_TOKEN=your_github_token_here
    GITHUB_USERNAME=your_github_username_here
    ```

3. After updating the values, **rename** the file from `.env-example` to `.env`:
4. Ensure that `your_github_token_here` and `your_github_username_here` are correctly replaced with your actual GitHub token and username.

## Project Setup

#### Follow these steps to get the project up and running:

1. **Clone the Repository**

```bash
git clone https://github.com/rubsxyz/GitHubScript.git
```

2. **Navigate into the project folder:**

```bash
cd GitHubScript
```

3. **Install Dependencies**

Install the required Python libraries using the requirements.txt file:

```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**

Create a `.env` file in the root directory of the project to store your GitHub API token and username. The file should look like this:

```bash
GITHUB_TOKEN="your_github_token_here"
GITHUB_USERNAME="your_github_username_here"
```

Make sure to replace `your_github_token_here` and `your_github_username_here` with your actual GitHub Personal Access Token and username.

5. **Run the Script**
   Run the main menu by executing the main.py script:

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
3. ❌ Exit
   Enter your choice (1/2/3):
   Select an option, and follow the prompts to either unfollow, follow, or exit the program.
```

## How It Works

-   Unfollow Script: Automatically unfollows users who are not following you back.
-   Follow Script: Allows you to either follow users from a specific account's followers or randomly follow trending GitHub users. It will also star the repositories of the users you follow.

## License

This project is licensed under the `MIT License` - see the LICENSE file for details.
