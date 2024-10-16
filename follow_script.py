import time
import random
import requests
from github_utils import follow_user, star_user_random_repo, headers

def get_followers_of_user(username):
    """
    Retrieves followers of the specified user.
    """
    followers = []
    page = 1
    while True:
        followers_url = f'https://api.github.com/users/{username}/followers?page={page}'
        response = requests.get(followers_url, headers=headers)
        if response.status_code != 200:
            print(f'Error fetching followers of {username}: {response.status_code}')
            break
        data = response.json()
        if not data:
            break
        followers.extend(data)
        page += 1
    return followers

def follow_specific_user():
    """
    Follow users from a specific GitHub account by their username.
    """
    target_username = input("Enter the username whose followers you want to follow: ").strip()
    followers = get_followers_of_user(target_username)
    
    if not followers:
        print(f"No followers found for {target_username}")
        return

    for user in followers:
        username = user['login']
        print(f"Following {username}...")
        if follow_user(username):
            print(f"Successfully followed {username}")
            star_user_random_repo(username)
        else:
            print(f"Failed to follow {username}")
        time.sleep(1)  # Delay to avoid rate limits

def follow_random_user():
    """
    Follows a random user from a random trending repository.
    """
    trending_url = 'https://api.github.com/search/repositories?q=stars:>500&sort=stars'
    response = requests.get(trending_url, headers=headers)
    if response.status_code == 200:
        repos = response.json().get('items', [])
        if repos:
            random_repo = random.choice(repos)
            owner = random_repo['owner']['login']
            print(f"Following the owner of the trending repository: {owner}")
            if follow_user(owner):
                print(f"Successfully followed {owner}")
                star_user_random_repo(owner)
            else:
                print(f"Failed to follow {owner}")
        else:
            print("No trending repositories found.")
    else:
        print(f"Error fetching trending repositories: {response.status_code}")
