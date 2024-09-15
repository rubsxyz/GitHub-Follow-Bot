import requests # type: ignore
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
YOUR_USERNAME = os.getenv('GITHUB_USERNAME')

# Check if TOKEN and YOUR_USERNAME are set
if not TOKEN or not YOUR_USERNAME:
    print('Error: GITHUB_TOKEN and GITHUB_USERNAME must be set in the .env file.')
    exit(1)

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

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

def is_following_back(username):
    """
    Checks if the specified user is following you back.
    """
    check_follow_url = f'https://api.github.com/users/{username}/following/{YOUR_USERNAME}'
    check_response = requests.get(check_follow_url, headers=headers)
    return check_response.status_code == 204

def unfollow_user(username):
    """
    Unfollows the specified user.
    """
    unfollow_url = f'https://api.github.com/user/following/{username}'
    unfollow_response = requests.delete(unfollow_url, headers=headers)
    return unfollow_response.status_code == 204

def log_unfollowed_user(username):
    with open('unfollowed_users.txt', 'a') as f:
        f.write(f'{username}\n')

def main():
    print('Fetching the list of users you are following...')
    following_users = get_all_following()
    print(f'Total users you are following: {len(following_users)}\n')

    for user in following_users:
        username = user['login']
        print(f'Checking if {username} follows you back...')
        if is_following_back(username):
            print(f'{username} follows you back. No action taken.\n')
        else:
            print(f'{username} does not follow you back. Unfollowing...')
            if unfollow_user(username):
                print(f'Successfully unfollowed {username}\n')
                log_unfollowed_user(username)
            else:
                print(f'Failed to unfollow {username}\n')
        # Add delay to avoid hitting rate limits
        time.sleep(1)

if __name__ == "__main__":
    main()
