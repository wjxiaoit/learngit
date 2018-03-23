#!/usr/bin/python
#-*-coding: UTF-8 -*-

import os
import fnmatch

def is_file_match(filename,patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(filename,pattern):
            return True
    return False

def find_specific_files(root,patterns=['*'],exclude_dirs=[]):
    for root,dirnames,filenames in os.walk(root):
        for filename in filenames:
            if is_file_match(filename,patterns):
                yield os.path.join(root,filename)
        for d in exclude_dirs:
            if d in dirnames:
                dirnames.remove(d)

#列出指定目录的文件
#for item in find_specific_files("."):
#    print(item)



#找出指定类型的文件
#patterns=['*.jpg']
#for item in find_specific_files("/root/xm/test",patterns):
#    print(item)


#查看目录树中，除 test 目录以外其他目录下的所有图片：
patterns = ['*.jpg']
exclude_dirs = ['test']

for item in find_specific_files('/root/xm',patterns,exclude_dirs):
    print(item)
