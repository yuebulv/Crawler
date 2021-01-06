import requests
import json
def get_corp_id(page):
    # 获取公司ID
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    url='https://glxy.mot.gov.cn/company/getCompanyAptitude.do'
    kw='b'#input('enter a word:')
    param={
        'page': page,
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
    filename=kw+'.txt'
    with open(filename,'w',encoding='utf-8') as fp:
        fp.write(id_list)
def get_prj_id():
    # 获取项目ID
    pass
if __name__=="__main__":
    #1.获得公司名称及ID
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    url='https://glxy.mot.gov.cn/company/getCompanyAptitude.do'
    kw='b'#input('enter a word:')
    param={
        'page': '1',
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
        url = 'https://glxy.mot.gov.cn/company/getCompanyAchieveList.do?companyId='+id+'&type=1a'
        # url='https://glxy.mot.gov.cn/company/getCompanyAchieveList.do?companyId=596b4e9580f94532ad6c066f3701aa07&type=1a'
        data={
            'page': '1',
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
            for prjdic in prjcont['data']:
                companyid_list.append(prjdic['companyId'])
                companyname_list.append(prjdic['corpName'])
                company_prjid_list.append(prjdic['id'])
                company_prjname_list.append(prjdic['projectName'])
                remark_list.append(prjdic['remark'])
    # 'page_text=response.text'
                filename=kw+'.txt'
                with open(filename,'w',encoding='utf-8') as fp:
                    fp.write(str(companyid_list))
    # filename=kw+'.json'
    # fp=open(filename,'w',encoding='utf-8')
    # json.dump(page_text,fp=fp,ensure_ascii=False)
    print(filename,'保存成功')
