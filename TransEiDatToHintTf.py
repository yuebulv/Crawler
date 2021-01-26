#function 将EI dat文件转为hint tf文件
    #1 先转非填、挖面积、中桩填挖类数据
        #1 暂时不考虑TF中正负号的问题

    #2 再将Ei are 中填挖面积、中桩填挖导入hint tf文件中
        #1 考虑字典存取
import re
import os
import tkinter as tk
from tkinter import filedialog

from tkinter import *

def getHdmAreFromEIarefile(key, EiarefilePath):
    # 功能通过已知桩号key，查找EiarefilePath中桩号key对应行的数据
    try:
        key = '{:.1f}'.format(int(float(key) * 10) / 10)
    except:
        print(key)
        print(type(key))
    else:
        pass
    pathregx = r'(.+\\?\/?\S+\.)\w+$'
    path_errfile = re.findall(pathregx, EiarefilePath, re.MULTILINE)
    path_errfile = path_errfile[0] + 'err.txt'
    file_are = open(EiarefilePath, 'r')
    DataOfEiare = file_are.read()
    regx = f'^{key}\d*\t.+(?=\n)'
    res = re.findall(regx, DataOfEiare, re.MULTILINE)  # 1 用正则将每个横断面dat数据放入list res中
    if len(res) == 0:
        errfile = open(path_errfile, 'a')
        errfile.write(f'{EiarefilePath}中未找到桩号：{key}\n')
        errfile.close()
    else:
        return res
    file_are.close()

if __name__:
    sy=getHdmAreFromEIarefile(55,r'C:\Users\Administrator.DESKTOP-95R7ULF\Desktop\E.are')