import requests

def download_jar(group_id, artifact_id, version, output_dir):
    base_url = "https://repo1.maven.org/maven2"
    group_path = group_id.replace('.', '/')
    jar_url = f"{base_url}/{group_path}/{artifact_id}/{version}/{artifact_id}-{version}.jar"
    
    response = requests.get(jar_url)
    if response.status_code == 200:
        jar_path = f"{output_dir}/{artifact_id}-{version}.jar"
        with open(jar_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {artifact_id}-{version}.jar to {jar_path}")
    else:
        print(f"Failed to download {artifact_id}-{version}.jar. HTTP Status Code: {response.status_code}")

# Example usage


group_id = "com.google.guava"
artifact_id = "guava"
version = "33.3.1-jre"
output_dir = "/Users/juridirocco/Desktop/phuong lecture"

download_jar(group_id, artifact_id, version, output_dir)