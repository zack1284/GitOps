import git
import os.path

repopath = 'https://gitea.com/zack1284/giteapy_testing.git'
repo = git.Repo(repopath)
repo.git.archive('<tag>', '-o', '<tag>.zip')
if os.path.exists('<tag>.zip'):
    pass