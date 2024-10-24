import time
import random
import requests  # type: ignore
from scripts.github_utils import follow_user, star_user_random_repo, headers
import logging
import os

# Setup logging
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    filename=os.path.join(log_directory, 'follower_manager.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_rate_limit():
    """Fetch the current rate limit status from GitHub API with logging."""
    try:
        response = requests.get("https://api.github.com/rate_limit", headers=headers)
        response.raise_for_status()  # Raise exception for non-200 responses
        data = response.json()
        remaining = data['rate']['remaining']
        reset_time = data['rate']['reset']
        logging.info(f"Rate limit remaining: {remaining}, reset at {reset_time}")
        return remaining, reset_time
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching rate limit: {str(e)}")
        return None, None

def get_followers_of_user(username):
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
                logging.info(f"No more followers found for {username}")
                break
            followers.extend(data)
            logging.info(f"Fetched {len(data)} followers on page {page} for {username}")
            page += 1
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching followers of {username}: {str(e)}")
            break
    return followers

def follow_specific_user():
    """
    Follow users from a specific GitHub account by their username.
    """
    target_username = input("Enter the username whose followers you want to follow: ").strip()
    followers = get_followers_of_user(target_username)
    
    if not followers:
        logging.info(f"No followers found for {target_username}")
        return

    for user in followers:
        username = user['login']
        logging.info(f"Attempting to follow {username}...")
        if follow_user(username):
            logging.info(f"Successfully followed {username}")
            star_user_random_repo(username)
        else:
            logging.error(f"Failed to follow {username}")
        time.sleep(1)  # Delay to avoid rate limits

def follow_random_user():
    """
    Follows a random user from a random trending repository with logging.
    """
    trending_url = 'https://api.github.com/search/repositories?q=stars:>500&sort=stars'
    try:
        response = requests.get(trending_url, headers=headers)
        response.raise_for_status()
        repos = response.json().get('items', [])
        if repos:
            random_repo = random.choice(repos)
            owner = random_repo['owner']['login']
            logging.info(f"Following the owner of the trending repository: {owner}")
            if follow_user(owner):
                logging.info(f"Successfully followed {owner}")
                star_user_random_repo(owner)
            else:
                logging.error(f"Failed to follow {owner}")
        else:
            logging.info("No trending repositories found.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching trending repositories: {str(e)}")
