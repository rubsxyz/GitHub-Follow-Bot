# unfollower_manager.py

import time
import requests  # type: ignore
from scripts.github_utils import unfollow_user, headers, YOUR_USERNAME
import logging
import os

def setup_logging():
    """
    Sets up logging for unfollower_manager.py.
    Logs are stored in the 'logs' directory with the filename 'unfollower_manager.log'.
    """
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logger = logging.getLogger('unfollower_manager')
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if already set
    if not logger.handlers:
        fh = logging.FileHandler(os.path.join(log_directory, 'unfollower_manager.log'), mode='w')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.propagate = False

    return logger

def get_all_following(logger):
    """
    Retrieves all users that you are currently following with logging.
    Handles pagination to ensure all users are fetched.
    """
    following_users = []
    page = 1
    while True:
        following_url = f'https://api.github.com/user/following?page={page}'
        try:
            response = requests.get(following_url, headers=headers)
            response.raise_for_status()  # Raise exception for non-200 responses
            data = response.json()
            if not data:
                logger.info(f"No more users found in following list on page {page}")
                break
            following_users.extend(data)
            logger.info(f"Fetched {len(data)} users from following list on page {page}")
            page += 1
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching following list: {str(e)}")
            break
    return following_users

def get_all_followers(logger):
    """
    Retrieves all users that are following you with logging.
    Handles pagination to ensure all followers are fetched.
    """
    followers = []
    page = 1
    while True:
        followers_url = f'https://api.github.com/users/{YOUR_USERNAME}/followers?page={page}'
        try:
            response = requests.get(followers_url, headers=headers)
            response.raise_for_status()  # Raise exception for non-200 responses
            data = response.json()
            if not data:
                logger.info(f"No more followers found on page {page}")
                break
            followers.extend(data)
            logger.info(f"Fetched {len(data)} followers on page {page}")
            page += 1
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching followers: {str(e)}")
            break
    return followers

def unfollow_script():
    """
    Script for unfollowing users who don't follow back, with logging.
    """
    logger = logging.getLogger('unfollower_manager')
    logger.info('Starting Unfollow Script...')
    print("Running Unfollow Script...")

    logger.info('Fetching the list of users you are following...')
    following_users = get_all_following(logger)
    logger.info(f'Fetched {len(following_users)} users from the following list.')

    logger.info('Fetching the list of your followers...')
    followers = get_all_followers(logger)
    logger.info(f'Fetched {len(followers)} followers.')

    followers_set = {follower['login'] for follower in followers}

    unfollowed_count = 0

    for user in following_users:
        username = user['login']
        if username not in followers_set:
            logger.info(f'{username} does not follow you back. Attempting to unfollow...')
            print(f"Unfollowing {username}...")
            if unfollow_user(username):
                unfollowed_count += 1
                logger.info(f'Successfully unfollowed {username}')
                print(f"Successfully unfollowed {username}")
            else:
                logger.error(f'Failed to unfollow {username}')
                print(f"Failed to unfollow {username}")
        else:
            logger.info(f'{username} follows you back. No action taken.')
            print(f"{username} follows you back. No action taken.")
        # Add delay to avoid hitting rate limits
        time.sleep(1)

    logger.info(f"Total users unfollowed: {unfollowed_count}")
    print(f"Total users unfollowed: {unfollowed_count}")
    logger.info('Unfollow Script completed.')
