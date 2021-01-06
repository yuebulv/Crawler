import requests
if __name__=="__main__":
    #1.获得公司名称及ID
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    url='https://glxy.mot.gov.cn/company/getCompanyAchieveInfo.do'
    kw='b'#input('enter a word:')
    param={
        'id': 'f51cb26b665b428d8f807745793b955b',
        'companyid': '596b4e9580f94532ad6c066f3701aa07',
    }
    page_text=requests.post(url=url,headers=headers,data=param,verify=False).json()
    # page_text = requests.post(url=url, headers=headers, verify=False).json()
    print(page_text)
    # id_list=[]
    # corpName_list = []
    # for dic in page_text['data']:
    #     id_list.append(dic['id'])
    #     corpName_list.append(dic['remark'])
