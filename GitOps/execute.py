'''gitops
執行git各項操作
'''
import os
from gitops_definition import GitOps


def delete_files_in_directory(directory_path):
    '''
    刪除資料夾內的檔案
    '''
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
        print("All files have been deleted.")
    except Exception as error_execption:
        print(f"An error occurred: {error_execption}")

if __name__ == "__main__":
    REMOTE_REPO_URL = "https://gitea.com/zack1284/giteapy_testing.git"
    LOCAL_REPO_URL = r"C:\Users\user\Desktop\giteapy_testing"
    CLONE_BRANCH = None #if branch is main/master = None  else "branchname"
    git_operations = GitOps(REMOTE_REPO_URL,LOCAL_REPO_URL,branch = None)   
    git_operations.add_files(modified=True, untracked=True)
    git_operations.commit_upload(branch = CLONE_BRANCH, commit_messages= "upload")
    #delete_files_in_directory(LOCAL_REPO_URL)