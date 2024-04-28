import requests
import csv
import random
import time
from datetime import datetime, timedelta
import os

# Constants
GITHUB_TOKEN = 'PERSONAL_TOKEN'  # Replace with your GitHub personal access token
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}
LANGUAGES = ['Java', 'Python', 'C++']
REPOS_PER_LANGUAGE = 1000  # Fetch more repos to select randomly
RANDOM_SELECTION_COUNT = 50  # Number of repos to select randomly
CURRENT_DATE = datetime.now().isoformat()[:-7] + 'Z'  # Format to match GitHub API requirements
INTERVAL = 1    # inter 0 semi monthly, 1 monthly and 6 semi annually

def get_github_api(url, paginate):
    """Utility function to handle API requests with rate limiting and pagination."""
    results = []
    page = 1
    while url:
        response = requests.get(url, headers=HEADERS)
        params = {'per_page': 100, 'page': page}
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            if not data:
                break
            results.extend(data)
            if paginate == False:
                break
            page+=1
        elif response.status_code == 403 and 'X-RateLimit-Reset' in response.headers:
            # Extract rate limiting info
            reset_timestamp = int(response.headers['X-RateLimit-Reset'])
            sleep_duration = reset_timestamp - int(time.time()) + 10  # Sleep a bit longer than necessary
            print(f"Rate limit hit, sleeping for {sleep_duration} seconds.")
            time.sleep(sleep_duration)
        else:
            print(f"Failed to retrieve data: {response.status_code}, {response.text}")
            return None
    return results
        
def get_daily_intervals(start_date):
    """Generate daily intervals from start_date to end_date."""
    start = datetime.fromisoformat(start_date[:-1])
    end = datetime.fromisoformat(CURRENT_DATE[:-1])
    intervals = []
    
    while start < end:
        # Calculate the end of the current day
        next_day = start + timedelta(days=1)
        
        # Add the interval for the current day
        intervals.append((start.isoformat() + 'Z', next_day.isoformat() + 'Z'))
        
        # Move to the next day
        start = next_day
    
    return intervals


def get_semi_monthly_intervals(start_date):
    """Generate semi-monthly intervals from start_date to end_date."""
    start = datetime.fromisoformat(start_date[:-1])
    end = datetime.fromisoformat(CURRENT_DATE[:-1])
    intervals = []
    while start < end:
        middle = start + timedelta(days=15)
        if middle.month == start.month:
            intervals.append((start.isoformat() + 'Z', middle.isoformat() + 'Z'))
            start = middle
        else:
            if start.month == 12:
                month_end = datetime(start.year+1, 1, 1)  - timedelta(seconds=1)
                intervals.append((start.isoformat() + 'Z', month_end.isoformat() + 'Z'))
                start = datetime(start.year+1, 1, 1)
            else:
                month_end = datetime(start.year, start.month + 1, 1) - timedelta(seconds=1)
                intervals.append((start.isoformat() + 'Z', month_end.isoformat() + 'Z'))
                start = datetime(start.year, start.month + 1, 1)
        if start.day == 16:
            if start.month == 12:
                month_end = datetime(start.year+1, 1, 1)  - timedelta(seconds=1)
                intervals.append((start.isoformat() + 'Z', month_end.isoformat() + 'Z'))
                start = datetime(start.year+1, 1, 1)
            else:
                month_end = datetime(start.year, start.month + 1, 1) - timedelta(seconds=1)
                intervals.append((start.isoformat() + 'Z', month_end.isoformat() + 'Z'))
                start = datetime(start.year, start.month + 1, 1)
    return intervals

# Monthly
def add_one_month(dt):
    """ Helper function to add one month to a date, accounting for year boundaries and month lengths. """
    month = dt.month - 1 + 1  # Add one month
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, [31, 29 if year % 4 == 0 and not year % 100 == 0 or year % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return datetime(year, month, day)

def get_monthly_intervals(start_date):
    """Generate monthly intervals from start_date to the current date."""
    start = datetime.fromisoformat(start_date[:-1])
    end = datetime.now()
    intervals = []
    while start < end:
        # Calculate end of the monthly period
        one_month_later = add_one_month(start)
        if one_month_later > end:
            one_month_later = end
        intervals.append((start.isoformat() + 'Z', one_month_later.isoformat() + 'Z'))
        start = one_month_later
    return intervals


def add_six_months(dt):
    """ Helper function to add six months to a date, accounting for year boundaries. """
    month = dt.month - 1 + 6
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, [31, 29 if year % 4 == 0 and not year % 100 == 0 or year % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return datetime(year, month, day)

def get_semi_annual_intervals(start_date):
    """Generate semi-annual intervals from start_date to the current date."""
    start = datetime.fromisoformat(start_date[:-1])
    end = datetime.now()
    intervals = []
    while start < end:
        # Calculate end of the semi-annual period
        six_months_later = add_six_months(start)
        if six_months_later > end:
            six_months_later = end
        intervals.append((start.isoformat() + 'Z', six_months_later.isoformat() + 'Z'))
        start = six_months_later
    return intervals

def get_intervals(start_date):
    if INTERVAL == 0:
        return get_semi_monthly_intervals(start_date)
    elif INTERVAL == 1:
        return get_monthly_intervals(start_date)
    elif INTERVAL == 6:
        return get_semi_annual_intervals(start_date)
    elif INTERVAL == -1:
        return get_daily_intervals(start_date)

def get_github_api_(url):
    """Utility function to handle API requests with rate limiting and pagination."""
    while True:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403 and 'X-RateLimit-Reset' in response.headers:
            # Extract rate limiting info
            reset_timestamp = int(response.headers['X-RateLimit-Reset'])
            sleep_duration = reset_timestamp - int(time.time()) + 10  # Sleep a bit longer than necessary
            print(f"Rate limit hit, sleeping for {sleep_duration} seconds.")
            time.sleep(sleep_duration)
        else:
            print(f"Failed to retrieve data: {response.status_code}, {response.text}")
            return None
        
def get_random_repos():
    """Fetch a random selection of repositories for the specified languages created after January 2020."""
    all_repos = []
    for language in LANGUAGES:
        url = f'https://api.github.com/search/repositories?q=language:{language}+created:2020-01-01..2020-02-28&+stars:1001..1500&per_page={REPOS_PER_LANGUAGE}'
        print("URL", url)
        response = get_github_api_(url)
        if response and 'items' in response:  # Check if response is not None and contains 'items'
            repos = response['items']
            if len(repos) >= RANDOM_SELECTION_COUNT:
                selected_repos = random.sample(repos, RANDOM_SELECTION_COUNT)
            else:
                selected_repos = repos
            all_repos.extend(selected_repos)
        else:
            print(f"No valid data received for {language}. Continuing with other languages.")
    return all_repos


def fetch_repo_data(repo):
    """Fetch all relevant metrics for the repository on a semi-monthly basis."""
    repo_data = []
    
    pulls_url = f"{repo['pulls_url'].split('{')[0]}"
    contributors_url = f"{repo['contributors_url'].split('{')[0]}"
    releases_url = f"{repo['releases_url'].split('{')[0]}"

    pulls = get_github_api(pulls_url, True)
    contributors = get_github_api(contributors_url, True)
    releases = get_github_api(releases_url, True)
    
    # Calculate total download count (example, may need adjustments based on GitHub API responses)
    total_downloads = sum([rel['assets'][0]['download_count'] for rel in releases if 'assets' in rel and rel['assets']])
  
    # Check if responses are valid before counting them
    repo_data.append({
        'repo_name': repo['name'],
        'language': repo['language'],
        'watchers': repo['watchers_count'],
        'stars': repo['stargazers_count'],
        'size': repo['size'],  # Size of the repo in kilobytes as returned by GitHub
        'downloads': total_downloads,
        'contributors': len(contributors) if contributors else 0,
        'pull_requests': len(pulls) if pulls else 0,
        'releases': len(releases) if releases else 0,
    })

    time_series_data = fetch_repo_time_series_data(repo)
    save_time_series_data_to_csv(time_series_data)

    return repo_data

def fetch_repo_time_series_data(repo):
    """Fetch all relevant metrics for the repository on a semi-monthly basis."""
    repo_data = []
    
    intervals = get_intervals(repo['created_at'])
    for start, end in intervals:
        commits_url = f"{repo['commits_url'].split('{')[0]}?since={start}&until={end}"
        issues_url = f"{repo['issues_url'].split('{')[0]}?state=all&since={start}&until={end}"

        commits = get_github_api(commits_url, True)
        issues = get_github_api(issues_url, True)
        

        # Check if responses are valid before counting them
        repo_data.append({
            'repo_name': repo['name'],
            'language': repo['language'],
            'period_start': start,
            'period_end': end,
            'issues': len(issues) if issues else 0,
            'commits': len(commits) if commits else 0,
        })
    return repo_data

def save_time_series_data_to_csv(data, repo_name):
    """Save collected data to a CSV file."""
    filename = f"DATA/2_{INTERVAL}_months_interval_data_new.csv"  # Ensure filename is valid

     # Check if the file exists and if it is empty
    file_exists = os.path.exists(filename)
    file_empty = True if not file_exists or os.stat(filename).st_size == 0 else False
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = [
        'repo_name', 'language','period_start', 'period_end', 'issues', 'commits'
        ]       
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file_empty:
            writer.writeheader()
        for entry in data:
            writer.writerow(entry)
        print(f"Data for {repo_name} has been saved to {filename}")

def save_data_to_csv(data, repo_name):
    """Save collected data to a CSV file."""
    filename = f"DATA/2_data_new.csv"  # Ensure filename is valid

     # Check if the file exists and if it is empty
    file_exists = os.path.exists(filename)
    file_empty = True if not file_exists or os.stat(filename).st_size == 0 else False
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = [
        'repo_name', 'language','watchers', 'forks', 'stars', 'size', 'period_start', 'period_end', 'contributors', 'pull_requests', 
        'issues', 'downloads', 'releases', 'commits'
        ]       
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file_empty:
            writer.writeheader()
        for entry in data:
            writer.writerow(entry)
        print(f"Data for {repo_name} has been saved to {filename}")


def main():
    random_repos = get_random_repos()
    for repo in random_repos:
        repo_data = fetch_repo_data(repo)
        save_data_to_csv(repo_data, repo['name'])

if __name__ == "__main__":
    main()
