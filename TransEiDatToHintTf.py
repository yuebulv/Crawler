#function 将EI dat文件转为hint tf文件
    #1 先转非填、挖面积、中桩填挖类数据
        #1 暂时不考虑TF中正负号的问题

    #2 再将Ei are 中填挖面积、中桩填挖导入hint tf文件中
        #1 考虑字典存取
import re

key=1087.660
EiarefilePath=r'C:\Users\Administrator.DESKTOP-95R7ULF\Desktop\E.are'
file_are = open(EiarefilePath, 'r')
DataOfEiare = file_are.read()
regx =f'^{key}0*\\t.+(?=\\n)'
# regx = r'^\d+\.\d+[\r\n]+(?:(?:(?:\d+\.\d+ ?\d*){3}|\d+)[\r\n]+)+'
res = re.findall(regx, DataOfEiare, re.MULTILINE)  # 1 用正则将每个横断面dat数据放入list res中
if len(res) ==0:
    pass

print(res)
print(len(res))
file_are.close()
