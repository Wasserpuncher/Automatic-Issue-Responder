import os
import re
import requests
from github import Github, GithubException
from collections import defaultdict
from datetime import datetime, timedelta

# Ensure you have these packages installed:
# pip install requests PyGithub

# GitHub access token
GITHUB_ACCESS_TOKEN = 'your_github_access_token'
REPO_NAME = 'your_username/your_repository'
g = Github(GITHUB_ACCESS_TOKEN)
repo = g.get_repo(REPO_NAME)

# Predefined responses based on keywords
KEYWORDS_RESPONSES = {
    'bug': 'Thank you for reporting this bug! Our team will look into it as soon as possible.',
    'feature': 'Thank you for the feature suggestion! We will consider it for future releases.',
    'error': 'It looks like you encountered an error. Please provide more details so we can assist you better.',
    'help': 'It seems like you need help. Please provide more details so we can assist you.'
}

# Function to analyze and respond to issues
def analyze_and_respond_to_issues():
    issues = repo.get_issues(state='open')
    for issue in issues:
        if not issue.comments:  # Check if the issue has no comments yet
            response = generate_response(issue.title + " " + issue.body)
            if response:
                issue.create_comment(response)
                print(f'Responded to issue #{issue.number}')

# Function to generate a response based on issue content
def generate_response(issue_content):
    for keyword, response in KEYWORDS_RESPONSES.items():
        if re.search(r'\b' + re.escape(keyword) + r'\b', issue_content, re.IGNORECASE):
            return response
    return None

if __name__ == "__main__":
    analyze_and_respond_to_issues()
