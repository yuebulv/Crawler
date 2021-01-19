import requests
import json
import time
if __name__=="__main__":
    start_time = time.time()
    #1.获得公司名称及ID
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    url='https://glxy.mot.gov.cn/company/getCompanyAptitude.do'
    kw='b'#input('enter a word:')
    for corp_page in range(1, 4):
        param={
            'page': corp_page,
            'rows': '15',
            'type': '2',
            'text':'',
        }
        page_text=requests.post(url=url,headers=headers,data=param,verify=False).json()
        id_list=[]
        corpName_list = []
        for dic in page_text['rows']:
            id_list.append(dic['id'])
            corpName_list.append(dic['corpName'])
        #2.获得公司设计项目
        for id in id_list:
            for prj_page in range(1,2):
                url = 'https://glxy.mot.gov.cn/company/getCompanyAchieveList.do?companyId='+id+'&type=1a'
                # url='https://glxy.mot.gov.cn/company/getCompanyAchieveList.do?companyId=596b4e9580f94532ad6c066f3701aa07&type=1a'
                data={
                    'page': prj_page,
                    'rows':'15',
                    'sourceInfo':'1',
                }
                page_text = requests.post(url=url, headers=headers, data=data, verify=False).json()
                prj_list = []
                prjid_list = []
                companyid_list = []
                companyname_list = []
                company_prjid_list = []
                company_prjname_list = []
                remark_list = []
                for dic in page_text['rows']:
                    prj_list.append(dic['projectName'])
                    prjid_list.append(dic['id'])
                # 3.获得公司设计项目ramark内容
                for prjid in prjid_list:
                    prj_url='https://glxy.mot.gov.cn/company/getCompanyAchieveInfo.do'
                    prjdata={
                        'id': prjid,
                        'companyid': id,
                    }
                    prjcont= requests.post(url=prj_url, headers=headers, data=prjdata, verify=False).json()
                    res=prjcont['data']
                    res['remark']=res['remark'].replace('\n','')
                    res['remark']=res['remark'].replace('\r', '')
                    temp = '\n'+res['companyId']+" "+res['corpName']+" 初步设计批复时间："+res['designAllowDate']+" 施工图批复时间："+res['drawingAllowDate']+" "+res['id']+" "+res['projectType']+" "+res['projectName']+" "+res['remark']
                    filename=kw+'.txt'
                    with open(filename,'a',encoding='utf-8') as fp:
                        fp.write(str(temp))
        print("公司第"+str(corp_page)+"页完成")
        print("用时：%f" % (time.time() - start_time))
    print("用时：%f" % (time.time()-start_time))
