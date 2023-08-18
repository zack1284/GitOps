'''gitops
執行git各項操作
'''
import os
from gitops_definition import Gitops




if __name__ == "__main__":
    REMOTE_REPO_URL = "https://gitea.com/zack1284/giteapy_testing.git"
    LOCAL_REPO_URL = r"C:\Users\user\Desktop\giteapy_testing"
    CLONE_BRANCH = None #if branch is main/master = None  else "branchname"

    # Check if local repository exists
    if os.path.exists(LOCAL_REPO_URL):
        print("Local Git repository already exists.")  
        git_operations = Gitops(REMOTE_REPO_URL,LOCAL_REPO_URL,branch = None, clone_or_not = False)   
    else:
        # Clone the remote repository to the local directory
        os.makedirs(LOCAL_REPO_URL, exist_ok=True)
        git_operations = Gitops(REMOTE_REPO_URL,LOCAL_REPO_URL,branch = CLONE_BRANCH, clone_or_not = True)
    git_operations.add_files(untracked=True, modified= True)
    git_operations.commit_upload(branch = CLONE_BRANCH, commit_messages= "upload")