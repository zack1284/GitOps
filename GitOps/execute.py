import os
from gitops_definition import gitops





if __name__ == "__main__":
    remote_repo_url = "https://gitea.com/zack1284/giteapy_testing.git"
    local_repo_path = r"C:\Users\user\Desktop\giteapy_testing"
    branch = "testing"

    git_operations = gitops(remote_repo_url,local_repo_path)
    # Check if local repository exists
    if os.path.exists(local_repo_path):
        print("Local Git repository already exists.")  
        remote_connection = git_operations.initialization(branch = None, clone_bool = False)
    
    else:
        # Clone the remote repository to the local directory
        os.makedirs(local_repo_path, exist_ok=True)
        remote_connection = git_operations.initialization(branch = branch, clone_bool = True)

    all_files = git_operations.add_files(repo= remote_connection, untracked=True, modified= True, deleted=False, branch=branch)
    git_operations.commit_upload(repo= remote_connection, branch = branch, all_files = all_files)