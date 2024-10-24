import requests # type: ignore
import random
import os
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

def follow_user(username):
    """
    Follows the specified user.
    """
    follow_url = f'https://api.github.com/user/following/{username}'
    follow_response = requests.put(follow_url, headers=headers)
    return follow_response.status_code == 204

def unfollow_user(username):
    """
    Unfollows the specified user.
    """
    unfollow_url = f'https://api.github.com/user/following/{username}'
    unfollow_response = requests.delete(unfollow_url, headers=headers)
    return unfollow_response.status_code == 204

def star_repository(owner, repo_name):
    """
    Stars the specified repository. Logs error details if the request fails.
    """
    star_url = f'https://api.github.com/user/starred/{owner}/{repo_name}'
    star_response = requests.put(star_url, headers=headers)

    if star_response.status_code == 204:
        print(f"Successfully starred {owner}/{repo_name}")
        return True
    else:
        print(f"Failed to star {owner}/{repo_name}. Status code: {star_response.status_code}")
        try:
            print(f"Error message: {star_response.json()}")
        except Exception as e:
            print(f"Error parsing the response: {e}")
        return False

def star_user_readme_repo(username):
    """
    Tries to star the user's README repository (which displays their GitHub bio).
    The repository is typically named after their username (username/username).
    """
    repo_name = username  # GitHub README repo is usually username/username
    print(f"Attempting to star {username}'s README repository: {repo_name}...")

    # Check if the username/username repo exists
    repos_url = f'https://api.github.com/repos/{username}/{repo_name}'
    response = requests.get(repos_url, headers=headers)

    if response.status_code == 200:
        # Try to star the README repository
        if star_repository(username, repo_name):
            print(f"Successfully starred {username}/{repo_name}")
        else:
            print(f"Failed to star {username}/{repo_name}")
    elif response.status_code == 404:
        print(f"{username} does not have a README repository.")
    else:
        print(f"Failed to check repository {repo_name}. Status code: {response.status_code}")

def star_user_random_repo(username):
    """
    Attempts to find and star the user's GitHub README repository or a random repository.
    """
    # First try to star the README repository
    star_user_readme_repo(username)

    # If the README repo doesn't exist or fails, star a random repo
    repos_url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(repos_url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        if repos:
            random_repo = random.choice(repos)
            print(f"Starring random repository: {random_repo['name']} from {username}...")
            if star_repository(username, random_repo['name']):
                print(f"Successfully starred {username}/{random_repo['name']}")
            else:
                print(f"Failed to star {username}/{random_repo['name']}")
        else:
            print(f"{username} has no repositories to star.")
    else:
        print(f"Failed to fetch repositories for {username}")
