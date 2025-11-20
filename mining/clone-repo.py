import os
import subprocess

def clone_repo(repo_url, clone_dir):
    try:
        if not os.path.exists(clone_dir):
            os.makedirs(clone_dir)
        subprocess.run(['git', 'clone', repo_url, clone_dir], check=True)
        print(f"Repository cloned to {clone_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_class_names(clone_dir):
    class_names = []
    for root, dirs, files in os.walk(clone_dir):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        if line.strip().startswith("public class"):
                            class_name = line.strip().split()[2]
                            class_names.append(class_name)
    return class_names



def list_first_10_comments(clone_dir):
    comments = []
    for root, dirs, files in os.walk(clone_dir):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        stripped_line = line.strip()
                        if stripped_line.startswith("//") or stripped_line.startswith("/*") or stripped_line.startswith("*"):
                            comments.append(stripped_line)
                            if len(comments) == 10:
                                return comments
    return comments


def list_last_10_commits(clone_dir):
    try:
        result = subprocess.run(
            ['git', '-C', clone_dir, 'log', '--pretty=format:%H - %s', '-n', '10'],
            check=True, capture_output=True, text=True
        )
        commits = result.stdout.split('\n')
        return commits
    except subprocess.CalledProcessError as e:
        print(f"Error listing commits: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    repo_url = "https://github.com/google/guava.git"  # Replace with your repository URL
    clone_dir = "clone-folder"  # Replace with your desired clone directory
    #clone_repo(repo_url, clone_dir)
    class_names = extract_class_names(clone_dir)
    comments = list_first_10_comments(clone_dir)
    for class_name in class_names:
        print(class_name)
    comments = list_first_10_comments(clone_dir)  
    for comment in comments:
        print(comment)
    commits = list_last_10_commits(clone_dir)
    for commit in commits:
        print(commit)