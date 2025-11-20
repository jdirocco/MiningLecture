from github import Github
import os
# Replace with your personal access token
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
if not GITHUB_TOKEN:
  raise EnvironmentError('Please set the GITHUB_TOKEN (or GH_TOKEN) environment variable')

# Create a Github instance
g = Github(GITHUB_TOKEN)

# Replace with the username you want to fetch repositories for
username = "jdirocco"

# Get the user
user = g.get_user(username)

# List all repositories for the user
# for repo in user.get_repos():
#     print(repo.name)
#     print(repo.description)
    # for commit in repo.get_commits():
    #     print(commit.commit.author.date)
    #     print(commit.commit.author.name)
    #     print(commit.commit.message)
    #     print("============================================")
    # print("============================================")
    # print("============================================")


# Get the repository from spring-projects/spring-framework
repo = g.get_repo("spring-projects/spring-framework")
# Print repository details
print("Repository Name:", repo.name)
print("Repository Description:", repo.description)
print("Repository Owner:", repo.owner.login)
print("Repository Stars:", repo.stargazers_count)
print("Repository Forks:", repo.forks_count)
print("Repository Open Issues:", repo.open_issues_count)

# Search for Java projects with more than 30 stars
query = "language:Java stars:>30"
result = g.search_repositories(query)

# Print the details of the repositories found

for repo in result:
    print("Repository Name:", repo.name)
    print("Repository Description:", repo.description)
    print("Repository Owner:", repo.owner.login)
    print("Repository Stars:", repo.stargazers_count)
    print("Repository Forks:", repo.forks_count)
    print("Repository Open Issues:", repo.open_issues_count)
    print("============================================")