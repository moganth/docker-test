import subprocess
import os

# Run any docker command via subprocess
def run_command(command: list):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return {"output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr.strip()}

# Clone the GitHub repository to the home directory
def clone_github_repo(github_url: str, destination_dir: str = "/home/ubuntu"):
    try:
        # Ensure the destination directory exists
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Get the repo name (last part of the URL) to name the folder
        repo_name = github_url.split("/")[-1].replace(".git", "")
        destination_path = os.path.join(destination_dir, repo_name)

        # Clone the GitHub repository to the specified path
        clone_command = ["git", "clone", github_url, destination_path]
        result = subprocess.run(clone_command, capture_output=True, text=True, check=True)
        return {"message": f"Repository cloned to {destination_path}", "output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"error": f"Failed to clone repository: {e.stderr.strip()}"}

# Build a Docker image from the cloned repository
def build_image_from_repo(github_url: str, image_name: str):
    try:
        # Clone the repository first
        clone_response = clone_github_repo(github_url)
        if "error" in clone_response:
            return clone_response  # Return error if cloning fails

        # Assuming the repository contains a Dockerfile at the root level
        destination_dir = "/home/ubuntu/docker-app"  # Default destination for cloned repo
        build_command = ["docker", "build", "-t", image_name, destination_dir]

        # Run the build command
        build_response = run_command(build_command)
        return build_response
    except Exception as e:
        return {"error": str(e)}

# Run a Docker container (after build)
def run_container(image_name: str, container_name: str = None):
    command = ["docker", "run", "-d"]
    if container_name:
        command += ["--name", container_name]
    command.append(image_name)
    return run_command(command)

# List Docker containers
def list_containers(all_containers: bool = False):
    command = ["docker", "ps"]
    if all_containers:
        command.append("-a")
    return run_command(command)

# Get logs of a Docker container
def get_logs(container_name: str):
    return run_command(["docker", "logs", container_name])

# Delete a Docker container
def delete_container(container_name: str):
    return run_command(["docker", "rm", "-f", container_name])

# Create a Docker volume
def create_volume(volume_name: str):
    return run_command(["docker", "volume", "create", volume_name])

# List all Docker volumes
def list_volumes():
    return run_command(["docker", "volume", "ls"])

# Remove a Docker volume
def remove_volume(volume_name: str):
    return run_command(["docker", "volume", "rm", volume_name])
