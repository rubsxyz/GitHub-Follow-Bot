# follower_manager.py

import time
import requests  # type: ignore
from scripts.github_utils import follow_user, star_user_random_repo, headers
import logging
import os

def setup_logging():
    """
    Sets up logging for follower_manager.py.
    Logs are stored in the 'logs' directory with the filename 'follower_manager.log'.
    """
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logger = logging.getLogger('follower_manager')
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if already set
    if not logger.handlers:
        fh = logging.FileHandler(os.path.join(log_directory, 'follower_manager.log'), mode='w')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.propagate = False

    return logger

def get_rate_limit(logger):
    """Fetch the current rate limit status from GitHub API with logging."""
    try:
        response = requests.get("https://api.github.com/rate_limit", headers=headers)
        response.raise_for_status()  # Raise exception for non-200 responses
        data = response.json()
        remaining = data['rate']['remaining']
        reset_time = data['rate']['reset']
        logger.info(f"Rate limit remaining: {remaining}, reset at {reset_time}")
        return remaining, reset_time
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching rate limit: {str(e)}")
        return None, None

def get_followers_of_user(username, logger):
    """
    Retrieves followers of the specified user, with logging.
    """
    followers = []
    page = 1
    while True:
        followers_url = f'https://api.github.com/users/{username}/followers?page={page}'
        try:
            response = requests.get(followers_url, headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            data = response.json()
            if not data:
                logger.info(f"No more followers found for {username}")
                break
            followers.extend(data)
            logger.info(f"Fetched {len(data)} followers on page {page} for {username}")
            page += 1
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching followers of {username}: {str(e)}")
            break
    return followers

def follow_specific_user(should_star=True):
    """
    Follow users from a specific GitHub account by their username.
    Optionally star their repositories.
    """
    logger = logging.getLogger('follower_manager')
    target_username = input("Enter the username whose followers you want to follow: ").strip()
    logger.info(f"User initiated following followers of: {target_username}")
    followers = get_followers_of_user(target_username, logger)

    if not followers:
        logger.info(f"No followers found for {target_username}")
        return

    followed_count = 0
    starred_count = 0

    for user in followers:
        username = user['login']
        logger.info(f"Attempting to follow {username}...")
        if follow_user(username):
            followed_count += 1
            logger.info(f"Successfully followed {username}")
            if should_star:
                if star_user_random_repo(username):
                    starred_count += 1
                    logger.info(f"Successfully starred a repository for {username}")
                else:
                    logger.error(f"Failed to star a repository for {username}")
        else:
            logger.error(f"Failed to follow {username}")
        time.sleep(1)  # Delay to avoid rate limits

    logger.info(f"Total users followed: {followed_count}")
    if should_star:
        logger.info(f"Total repositories starred: {starred_count}")
    print(f"Total users followed: {followed_count}")
    if should_star:
        print(f"Total repositories starred: {starred_count}")

def search_most_followed_in_following():
    """
    Searches for users in your following list with the most followers.
    Displays the top 10 users sorted by their follower count with a progress bar.
    """
    logger = logging.getLogger('follower_manager')
    try:
        # Fetch the list of users you are following
        following = []
        page = 1
        per_page = 100  # Max per page for GitHub API
        github_username = os.getenv("GITHUB_USERNAME")
        if not github_username:
            logger.error("GITHUB_USERNAME is not set in the environment variables.")
            print("Error: GITHUB_USERNAME is not set in the environment variables.")
            return

        while True:
            following_url = f'https://api.github.com/users/{github_username}/following?page={page}&per_page={per_page}'
            response = requests.get(following_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            following.extend(data)
            logger.info(f"Fetched {len(data)} users from following list on page {page}")
            page += 1
        if not following:
            print("You are not following anyone.")
            logger.info("No users found in your following list.")
            return

        total_users = len(following)
        user_followers = []
        fetched_followers = 0

        print(f"Fetching follower counts for {total_users} users you are following...")

        # Initialize tqdm progress bar
        try:
            from tqdm import tqdm
        except ImportError:
            print("tqdm module not found. Installing it now...")
            import subprocess
            subprocess.check_call(["pip", "install", "tqdm"])
            from tqdm import tqdm

        with tqdm(total=total_users, desc="Processing Users", unit="user") as pbar:
            for user in following:
                username = user['login']
                user_url = f'https://api.github.com/users/{username}'
                try:
                    user_response = requests.get(user_url, headers=headers)
                    user_response.raise_for_status()
                    user_data = user_response.json()
                    follower_count = user_data.get('followers', 0)
                    user_followers.append((username, follower_count))
                    fetched_followers += follower_count
                    logger.info(f"Fetched {username} with {follower_count} followers.")
                except requests.exceptions.RequestException as e:
                    logger.error(f"Failed to fetch data for {username}. Error: {str(e)}")
                pbar.update(1)  # Update the progress bar
                time.sleep(0.5)  # Delay to avoid rate limits

        # Sort users by follower count in descending order
        user_followers.sort(key=lambda x: x[1], reverse=True)
        # Display top 10 users
        top_n = 10
        print(f"\nTop {top_n} users you are following by follower count:")
        print("=" * 50)
        for i, (username, followers) in enumerate(user_followers[:top_n], start=1):
            print(f"{i}. {username} - {followers} followers")
        logger.info(f"Displayed top {top_n} users you are following by follower count.")
        print(f"\nTotal followers fetched: {fetched_followers}")
        logger.info(f"Total followers fetched: {fetched_followers}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching following list or user data: {str(e)}")
        print(f"An error occurred: {str(e)}")
