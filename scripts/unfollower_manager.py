import time
import requests  # type: ignore
from scripts.github_utils import unfollow_user, YOUR_USERNAME, headers
import logging
import os

# Setup logging
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    filename=os.path.join(log_directory, 'unfollower_manager.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_all_following():
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
                logging.info(f"No more users found in following list on page {page}")
                break
            following_users.extend(data)
            logging.info(f"Fetched {len(data)} users from following list on page {page}")
            page += 1
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching following list: {str(e)}")
            break
    return following_users

def get_all_followers():
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
                logging.info(f"No more followers found on page {page}")
                break
            followers.extend(data)
            logging.info(f"Fetched {len(data)} followers on page {page}")
            page += 1
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching followers: {str(e)}")
            break
    return followers

def unfollow_script():
    """
    Script for unfollowing users who don't follow back, with logging.
    """
    logging.info('Fetching the list of users you are following...')
    following_users = get_all_following()
    logging.info(f'Fetched {len(following_users)} users from the following list.')

    logging.info('Fetching the list of your followers...')
    followers = get_all_followers()
    logging.info(f'Fetched {len(followers)} followers.')

    followers_set = {follower['login'] for follower in followers}

    for user in following_users:
        username = user['login']
        if username not in followers_set:
            logging.info(f'{username} does not follow you back. Attempting to unfollow...')
            if unfollow_user(username):
                logging.info(f'Successfully unfollowed {username}')
            else:
                logging.error(f'Failed to unfollow {username}')
        else:
            logging.info(f'{username} follows you back. No action taken.')
        # Add delay to avoid hitting rate limits
        time.sleep(1)
