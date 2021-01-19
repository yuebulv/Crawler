import requests


def str_connect():
    url='https://wwww.qiushibike.com/pic/page/%d/?s='
    for pagenum in range(1,10):
        new_url=format(url%pagenum)
        print(new_url)

def str_connect():
    page=1
    print("第"+str(page)+"页")

def text1():
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    url='https://glxy.mot.gov.cn/company/getCompanyAptitude.do'
    kw='b'#input('enter a word:')
    for corp_page in range(1, 8):
        param={
            # 'page': corp_page,
            # 'rows': 15,
            # 'type': 2,
            # 'regProvinceCode':"",
            # 'catype':"",
            # 'grade':"",
            # 'text':"",
            'page': corp_page,
            'rows': '15',
            'type': '2',
            'text': '',

        }
        page_text=requests.post(url=url,headers=headers,data=param,verify=False).json()
        print(page_text)
if __name__=="__main__":
    temp=text1()