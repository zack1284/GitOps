import os
from gitops_definition import gitops
from datetime import datetime




if __name__ == "__main__":
    remote_repo_url = "https://gitea.com/zack1284/giteapy_testing.git"
    local_repo_path = r"C:\Users\user\Desktop\giteapy_testing"
    clone_branch = None #if branch is main/master = None  else "branchname"

    # Check if local repository exists
    if os.path.exists(local_repo_path):
        print("Local Git repository already exists.")  
        git_operations = gitops(remote_repo_url,local_repo_path,branch = None, clone_or_not = False)
    
    else:
        # Clone the remote repository to the local directory
        os.makedirs(local_repo_path, exist_ok=True)
        git_operations = gitops(remote_repo_url,local_repo_path,branch = clone_branch, clone_or_not = True)


    git_operations.add_files(untracked=True, modified= True)
    git_operations.commit_upload(branch = clone_branch, commit_messages=f"upload on ")