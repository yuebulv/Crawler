# 1 从dat文件中获取逐桩横断面三维数据get3DdataFromDatfile(path)
    # 1.1 用正则将每个横断面dat数据放入list res中
# 2 将逐桩横断面三维数据转为纬地3dr格式数据trans3DdataTo3drFile(get3DdataFromDatfile)
    # 2.1 用正刚将每个横断面的dat数据中桩号、三维坐标放入list 中（key，HdmPoints_xyz）
    # 2.2 将list中的横断面三维数据转为3dr格式数据
    # 2.3 将list中的横断面三维数据转为tf格式数据
        #2.3-pro 暂时不考虑TF中正负号的问题
        #2.3.1 先转非填、挖面积、中桩填挖类数据
            #2.3.1.1 先将路基左侧数据存入list中
            #2.3.1.2 先将路基右侧数据存入list中
        #2.3.2 再将Ei are 中填挖面积、中桩填挖导入hint tf文件中
            # 2.3.2.1 先将Ei are 中填挖面积、中桩填挖数据存入list中
            # 2.3.2.2 将list数据存入tf文件
import re
def get3DdataFromDatfile(path): # 1 从dat文件中获取逐桩横断面三维数据
    DatFile=''
    with open(path, "r") as FData:
        DatFile = FData.read()
    regx = r'^\d+\.\d+[\r\n]+(?:(?:(?:\d+\.\d+ ?\d*){3}|\d+)[\r\n]+)+'
    res = re.findall(regx, DatFile, re.MULTILINE)   #1 用正则将每个横断面dat数据放入list res中
    FData.close()
    return res
def trans3DdataTo3drFile(get3DdataFromDatfile,path_3drsaved):   # 2 将逐桩横断面三维数据转为纬地3dr格式数据
    # 2.1 用正刚将每个横断面的dat数据中桩号、三维坐标放入list 中（key，HdmPoints_xyz）
    for res in get3DdataFromDatfile:
        regx=r'^(\d+\.\d+)[\n\r]'
        key = re.findall(regx,res,re.MULTILINE) #桩号
        file_3dr = open(path_3drsaved, 'a')
        file_3dr.write(key[0] + '\n')
        regx=r'((?:\d+\.\d+ ?){3})[\n\r]'
        key_design_xyz = re.findall(regx,res,re.MULTILINE)  #中桩三维坐标
        key_design_xyz=key_design_xyz[0].split( )
        key_design_xyz=list(map(float,key_design_xyz))
        regx = r'^(\d+)[\n\r]'
        TollNum_HdmPoints=re.findall(regx, res, re.MULTILINE)
        regx = r'(?:(?:\d+\.\d+ ){3}\d[\n\r]?)+'
        HdmPoints_xyz=re.findall(regx, res, re.MULTILINE)   #左右侧横断面三维坐标
        # 2.2 将list中的横断面三维数据转为3dr格式数据
            #1 左右侧
            #2 切成每个点
            #3 切成每个点的坐标
        for j in range(0,2):
            file_3dr.write(TollNum_HdmPoints[j]+' ')
            regx = r'((?:\d+\.\d+ ){3}\d)[\n\r]?'
            HdmPoint_xyz = re.findall(regx, HdmPoints_xyz[j], re.MULTILINE)  # 左右侧横断面三维坐标
            for Hdmlist in HdmPoint_xyz:
                Hdmlist=Hdmlist.split( )
                Hdmlist=list(map(float,Hdmlist))
                dist_3dr=((Hdmlist[0]-key_design_xyz[0])**2+(Hdmlist[1]-key_design_xyz[1])**2)**0.5
                dist_3dr = round(dist_3dr, 3)
                if j ==0:
                    dist_3dr=-dist_3dr
                file_3dr.write(str(dist_3dr) + ' '+str(Hdmlist[2])+' ')
            file_3dr.write('\n')
    file_3dr.close()
def TransEiDatToHintTf(get3DdataFromDatfile,path_tfsaved):
    # 2.1 用正刚将每个横断面的dat数据中桩号、三维坐标放入list 中（key，HdmPoints_xyz）
    for res in get3DdataFromDatfile:
        regx=r'^(\d+\.\d+)[\n\r]'
        key = re.findall(regx,res,re.MULTILINE) #桩号
        file_3dr = open(path_tfsaved, 'a')
        # file_3dr.write(key[0] + ' ')
        regx=r'((?:\d+\.\d+ ?){3})[\n\r]'
        key_design_xyz = re.findall(regx,res,re.MULTILINE)  #中桩三维坐标
        key_design_xyz=key_design_xyz[0].split( )
        key_design_xyz=list(map(float,key_design_xyz))
        regx = r'^(\d+)[\n\r]'
        TollNum_HdmPoints=re.findall(regx, res, re.MULTILINE)
        regx = r'(?:(?:\d+\.\d+ ){3}\d[\n\r]?)+'
        HdmPoints_xyz=re.findall(regx, res, re.MULTILINE)   #左右侧横断面三维坐标
        # 2.3 将list中的横断面三维数据转为tf格式数据
            #2.3-pro 暂时不考虑TF中正负号的问题
            #2.3.1 先转非填、挖面积、中桩填挖类数据
                #2.3.1.1 先将路基左侧数据存入list中
                #2.3.1.2 先将路基右侧数据存入list中
            #2.3.2 再将Ei are 中填挖面积、中桩填挖导入hint tf文件中
                # 2.3.2.1 先将Ei are 中填挖面积、中桩填挖数据存入list中
                # 2.3.2.2 将list数据存入tf文件
        Tflist=[]
        for temp in range(1,63):
            Tflist.append(0)
        # 2.3.1 先转非填、挖面积、中桩填挖类数据
        Tflist[0]=key[0]
        for j in range(0,2):
            regx = r'((?:\d+\.\d+ ){3}\d)[\n\r]?'
            HdmPoint_xyz = re.findall(regx, HdmPoints_xyz[j], re.MULTILINE)  # 左右侧横断面三维坐标
            UpSlopeStatus = 0
            list_dist_3dr=[]
            list_high=[]
            Hdmlist_last=[]
            for Hdmlist in HdmPoint_xyz:
                Hdmlist=Hdmlist.split( )
                Hdmlist=list(map(float,Hdmlist))
                dist_3dr=((Hdmlist[0]-key_design_xyz[0])**2+(Hdmlist[1]-key_design_xyz[1])**2)**0.5 #平距
                dist_3dr = round(dist_3dr, 3)
                # 判断当前Hdmlist在横断面中处于哪个部位#2.3.1.1 先将路基左/右侧数据存入list中
                if Hdmlist[-1]==1:  #中央分隔带
                    pass
                elif Hdmlist[-1]==2:    #行车道
                    pass
                elif Hdmlist[-1]==3:    #
                    pass
                elif Hdmlist[-1]==4:    #
                    pass
                elif Hdmlist[-1]==5:    #土路肩
                    Tflist[4+j] =round(dist_3dr,3)   #路基宽度
                    Tflist[6+j] = round(Hdmlist[2],3)    #路基高程
                    Tflist[8 + j] = round(dist_3dr,3)  # 坡脚距
                    Tflist[10 + j] = round(Hdmlist[2],3)
                elif Hdmlist[-1]==6:    #填方边坡
                    Tflist[8+j] =round(dist_3dr,3)   #坡脚距
                    Tflist[10+j] = round(Hdmlist[2],3)
                elif Hdmlist[-1]==7:    #边沟\排水沟
                    try:    #识别填方护坡道
                        dist_AdjacentPoints=((Hdmlist_last[0]-Hdmlist_last_last[0])**2+(Hdmlist_last[1]-Hdmlist_last_last[1])**2)**0.5 #相邻两点间距离
                        high_AdjacentPoints=abs(Hdmlist_last[2]-Hdmlist_last_last[2]) #相邻两点间高差
                        slope_AdjacentPoints=dist_AdjacentPoints/high_AdjacentPoints
                    except ZeroDivisionError:
                        if Hdmlist_last[3]==6:
                            Tflist[14+j]=round(dist_AdjacentPoints,3)
                            Tflist[8 + j] = round(Tflist[8 + j]-dist_AdjacentPoints,3) # 坡脚距
                    else:
                        if slope_AdjacentPoints>=24 and Hdmlist_last[3]==6: #最后一级边坡坡度缓于1:24判断为填方护坡道
                            Tflist[14+j]=round(dist_AdjacentPoints,3)
                            Tflist[8 + j] = round(Tflist[8 + j] - dist_AdjacentPoints,3)  # 坡脚距
                            Tflist[10 + j] = round(Hdmlist_last_last[2],3)
                    Tflist[12+j] =round(dist_3dr,3)  #沟缘距
                    list_dist_3dr.append(dist_3dr)
                    list_dist_3dr.sort()
                    min_dist_3dr=list_dist_3dr[0]
                    max_dist_3dr=list_dist_3dr[-1]
                    Tflist[18+j]=round((min_dist_3dr+max_dist_3dr)/2,3) #沟心距
                    list_high.append(Hdmlist[2])
                    list_high.sort()
                    min_high=list_high[0]
                    max_high=list_high[-1]
                    Tflist[16 + j] =round(min_high,3)
                    Tflist[20+j]=round(max_high-min_high,3)  #沟深
                elif Hdmlist[-1]==8:    #挖方边坡
                    try:    #识别挖方碎落台
                        dist_AdjacentPoints=round(((Hdmlist[0]-Hdmlist_last[0])**2+(Hdmlist[1]-Hdmlist_last[1])**2)**0.5,3) #相邻两点间距离
                        high_AdjacentPoints=abs(Hdmlist[2]-Hdmlist_last[2]) #相邻两点间高差
                        slope_AdjacentPoints=dist_AdjacentPoints/high_AdjacentPoints
                    except ZeroDivisionError:
                        Tflist[14+j]=dist_AdjacentPoints
                    else:
                        if slope_AdjacentPoints>=24 and UpSlopeStatus==0: #第一级边坡坡度缓于1:24判断为碎落台
                            Tflist[14+j]=dist_AdjacentPoints
                    UpSlopeStatus=UpSlopeStatus+1
                    Tflist[8+j] =-round(dist_3dr,3) #坡脚距
                    Tflist[10+j] = round(Hdmlist[2],3)
                elif Hdmlist[-1]==9:    #
                    pass
                Hdmlist_last_last=Hdmlist_last[:]
                Hdmlist_last=Hdmlist[:]
                # dist_3dr = round(dist_3dr, 3)
                # if j ==0:
                #     dist_3dr=-dist_3dr
        file_3dr.write(str(Tflist).replace(',',' ').replace('[','').replace(']','').replace('\'',''))
        file_3dr.write('\n')
    file_3dr.close()

def getHdmAreFromEIarefile(key,EiarefilePath):
    #功能通过已知桩号，查找EiarefilePath中挖方面积、填方面积、中桩填挖
# 2.3.2 再将Ei are 中填挖面积、中桩填挖导入hint tf文件中
# 2.3.2.1 先将Ei are 中填挖面积、中桩填挖数据存入list中
# 2.3.2.2 将list数据存入tf文件
    file_are=open(EiarefilePath,'r')
    DataOfEiare=file_are.read()
    regx = r'^\d+\.\d+[\r\n]+(?:(?:(?:\d+\.\d+ ?\d*){3}|\d+)[\r\n]+)+'
    res = re.findall(regx, DataOfEiare, re.MULTILINE)   #1 用正则将每个横断面dat数据放入list res中
    file_are.close()
    pass


if __name__=="__main__":
    path="C:\\Users\\Administrator.DESKTOP-95R7ULF\\Desktop\\E.dat"
    data_dat=get3DdataFromDatfile(path)
    path_3drsaved = 'C:\\Users\\Administrator.DESKTOP-95R7ULF\\Desktop\\E.3dr'
    path_tfsaved = r'C:\Users\Administrator.DESKTOP-95R7ULF\Desktop\E.tf'
    try:
        tempfile=open(path_3drsaved,'a')
        tempfile.truncate(0)
        tempfile.write('HINTCAD5.83_HDM_SHUJU'+'\n')
        tempfile.close()
    except FileNotFoundError:
        print("打开文件错误")
    else:
        pass
    # result1=trans3DdataTo3drFile(data_dat,path_3drsaved)
    result2 = TransEiDatToHintTf(data_dat, path_tfsaved)




