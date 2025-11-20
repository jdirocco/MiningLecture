import requests
import os

# Replace 'your_token_here' with your GitHub personal access token
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
if not GITHUB_TOKEN:
  raise EnvironmentError('Please set the GITHUB_TOKEN (or GH_TOKEN) environment variable')
GITHUB_API_URL = 'https://api.github.com/graphql'

def run_query(query):
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.post(GITHUB_API_URL, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

# Example query to get the name and description of a repository
query = """
{
  repository(owner: "octocat", name: "Hello-World") {
    name
    description
  }
}
"""

result = run_query(query)
print(result)
query = """
{
repository(owner:"spring-projects", name:"spring-framework") {
    issues(last:20, states:CLOSED) {
      edges {
        node {
          title
          url
          labels(first:5) {
            edges {
              node {
                name
              }
            }
          }
        }
      }
    }
  }
}
"""
print("============================================")
result = run_query(query)
print(result)
