import requests
if __name__=="__main__":
    url='https://wwww.qiushibike.com/pic/page/%d/?s='
    for pagenum in range(1,10):
        new_url=format(url%pagenum)
        print(new_url)