# Mining Seminar Supporting Material

This repository contains Python scripts that serve as supporting material for the mining seminar. Each script is designed to demonstrate various concepts and techniques discussed during the seminar.

## Usage

To run the scripts in a reproducible environment we recommend creating a Conda environment and installing dependencies there. Example steps to create the environment, install `PyGithub`, and run the `github-rest.py` script:

```bash
# Create the Conda environment from `environment.yml`
conda env create -f environment.yml

# Activate the environment (interactive session) and run the script
conda activate mininglecture
python /Users/juridirocco/development/MiningLecture/github-rest.py

# Alternative: run without activating (uses `conda run`)
conda run -n mininglecture python /Users/juridirocco/development/MiningLecture/github-rest.py
```

Security note: `github-rest.py` currently includes a GitHub token hard-coded in the source. Do not commit tokens to version control. Instead set the token in your shell before running:

```bash
export GITHUB_TOKEN="ghp_your_personal_token_here"
# then modify the script to read `os.environ['GITHUB_TOKEN']` (recommended)
```

If you want, I can update `github-rest.py` to read the token from the `GITHUB_TOKEN` environment variable and use the modern PyGithub authentication API.

Using the `environment.yml` file keeps environment creation reproducible and is recommended for sharing with collaborators.

**Run other scripts**

- `github-graphql.py`: This script uses the GitHub GraphQL API via `requests`. It currently contains a hard-coded token—do not keep tokens in source control. Recommended workflow:

```bash
# Ensure the environment is active
conda activate mininglecture

# Set your token in the environment (example)
export GITHUB_TOKEN="ghp_your_personal_token_here"

# Edit `github-graphql.py` to read `GITHUB_TOKEN` from the environment, or replace the hard-coded token temporarily.
python /Users/juridirocco/development/MiningLecture/github-graphql.py
```

- `maven-repo.py`: Downloads a JAR from Maven Central (uses `requests`). Run it like this:

```bash
conda activate mininglecture
python /Users/juridirocco/development/MiningLecture/maven-repo.py
```

Both scripts require the `requests` package (included in `environment.yml`).


## License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

