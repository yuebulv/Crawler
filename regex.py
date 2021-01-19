import re
def get3DdataFromDatfile(path):
    # 从dat文件中获取逐桩横断面三维数据get3DdataFromDatfile(path)
    # 将逐桩横断面三维数据转为纬地3dr格式数据trans3DdataTo3drFile(get3DdataFromDatfile)
    DatFile=''
    with open(path, "r") as FData:
        DatFile = FData.read()
    regx = r'^\d+\.\d+[\r\n]+(?:(?:(?:\d+\.\d+ ?\d*){3}|\d+)[\r\n]+)+'
    res = re.findall(regx, DatFile, re.MULTILINE)
    FData.close()
    return res
def trans3DdataTo3drFile(get3DdataFromDatfile,path_3drsaved):
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






if __name__=="__main__":
    path="C:\\Users\\Administrator.DESKTOP-95R7ULF\\Desktop\\B5.dat"
    data_dat=get3DdataFromDatfile(path)
    path_3drsaved = 'C:\\Users\\Administrator.DESKTOP-95R7ULF\\Desktop\\B5.3dr'
    try:
        tempfile=open(path_3drsaved,'a')
        tempfile.truncate(0)
        tempfile.write('HINTCAD5.83_HDM_SHUJU'+'\n')
        tempfile.close()
    except FileNotFoundError:
        print("打开文件错误")
    else:
        pass
    result=trans3DdataTo3drFile(data_dat,path_3drsaved)




