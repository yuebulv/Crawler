import requests
import json
if __name__=="__main__":
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
    for dic in page_text['rows']:
        id_list.append(dic['id'])
    for id in id_list:
        url = 'https://glxy.mot.gov.cn/company/getCompanyAchieveList.do?company&idtype=1a'
        # url='https://glxy.mot.gov.cn/company/getCompanyAchieveList.do?companyId=596b4e9580f94532ad6c066f3701aa07&type=1a'
        data={
            'page': '1',
            'rows':'15',
            'sourceInfo':'1',
        }
        page_text = requests.post(url=url, headers=headers, data=data, verify=False).json()
        id_list = []
        for dic in page_text['rows']:
            id_list.append(dic['projectName'])
    'page_text=response.text'
    # filename=kw+'.html'
    # with open(filename,'w',encoding='utf-8') as fp:
    #     fp.write(page_text)
    filename=kw+'.json'
    fp=open(filename,'w',encoding='utf-8')
    json.dump(page_text,fp=fp,ensure_ascii=False)
    print(filename,'保存成功')
