
import os
from shutil import move

# -----------------------------------------------------------
#     author：wangshinan
#     description：移动文件
#     param：path 原始路径
#           disdir 移动的目标目录
#     remarks：
# -----------------------------------------------------------

def moveFiles(path, disdir, name):
    dirlist = os.listdir(path)
    new_dirlist = disdir + '\\' + name
    if os.path.isdir(new_dirlist):
        pass
    else:
        os.makedirs(new_dirlist)
    if len(dirlist):
        for i in dirlist:
            child = os.path.join('%s\%s' % (path, i))
            if os.path.isfile(child):
                move(child, os.path.join(new_dirlist, i))
                continue
    else:
        pass

# -----------------------------------------------------------
#     author：wangshinan
#     description：刪除文件
#     param：path 文件
#     remarks：
# -----------------------------------------------------------

def deleteFiles(path):
    if os.path.exists(path):  # 如果文件存在
        # 删除文件，可使用以下两种方法
        os.remove(path)
        # os.unlink(path)
    else:
        pass


