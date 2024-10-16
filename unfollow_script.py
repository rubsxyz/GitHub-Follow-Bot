import time
from github_utils import unfollow_user, YOUR_USERNAME, headers
import requests

def get_all_following():
    """
    Retrieves all users that you are currently following.
    Handles pagination to ensure all users are fetched.
    """
    following_users = []
    page = 1
    while True:
        following_url = f'https://api.github.com/user/following?page={page}'
        response = requests.get(following_url, headers=headers)
        if response.status_code != 200:
            print(f'Error fetching following list: {response.status_code}')
            break
        data = response.json()
        if not data:
            break
        following_users.extend(data)
        page += 1
    return following_users

def get_all_followers():
    """
    Retrieves all users that are following you.
    Handles pagination to ensure all followers are fetched.
    """
    followers = []
    page = 1
    while True:
        followers_url = f'https://api.github.com/users/{YOUR_USERNAME}/followers?page={page}'
        response = requests.get(followers_url, headers=headers)
        if response.status_code != 200:
            print(f'Error fetching followers: {response.status_code}')
            break
        data = response.json()
        if not data:
            break
        followers.extend(data)
        page += 1
    return followers

def unfollow_script():
    """
    Script for unfollowing users who don't follow back.
    """
    print('Fetching the list of users you are following...')
    following_users = get_all_following()
    followers = get_all_followers()
    followers_set = {follower['login'] for follower in followers}
    
    print(f'Total users you are following: {len(following_users)}')

    for user in following_users:
        username = user['login']
        if username not in followers_set:
            print(f'{username} does not follow you back. Unfollowing...')
            if unfollow_user(username):
                print(f'Successfully unfollowed {username}')
            else:
                print(f'Failed to unfollow {username}')
        else:
            print(f'{username} follows you back. No action taken.')
        # Add delay to avoid hitting rate limits
        time.sleep(1)
