'''gitops
執行git各項操作
'''
from gitops import GitOps


if __name__ == "__main__":
    REMOTE_REPO_URL = "https://gitea.com/zack1284/giteapy_testing.git"
    LOCAL_REPO_URL = r"C:\Users\user\Desktop\giteapy_testing"
    git_operations = GitOps(REMOTE_REPO_URL,LOCAL_REPO_URL, branch= "main")   
    git_operations.add_files(modified=True, untracked=True, delete=True)    
    git_operations.commit(commit_messages= "upload")
    #git_operations.create_new_branch(new_branch="new2")
    #git_operations.checkout(checkout_branch="new2")
    git_operations.push(branch = "main", origin="origin")