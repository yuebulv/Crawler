import requests
import json
import time
import os
import re
import copy


def output_company_glxy_data(headers, company_id: list, company_name: list,  start_page: int = 1, end_page: int = 7, output_filename='company_glxy_data'):
    # start_time = time.time()
    #1.获得公司名称及ID
    # headers={
    #     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    # }
    # url='https://glxy.mot.gov.cn/company/getCompanyAptitude.do'

    # id_list=[]
    # corpName_list = []
    # dic = {'id':'8250ecff0c7a401d9301d0730726249f', 'corpName':'河北省交通规划设计院'}
    # # dic['id'] = '8250ecff0c7a401d9301d0730726249f'
    # # dic['corpName'] = '河北省交通规划设计院'
    # id_list.append(dic['id'])
    # corpName_list.append(dic['corpName'])

    id_list = company_id
    corpName_list = company_name
    kw = output_filename  # '#input('enter a word:')
    # 2.获得公司设计项目
    end_page += 1
    for companyId in id_list:
        for prj_page in range(start_page, end_page):
            url = 'https://glxy.mot.gov.cn/company/getCompanyAchieveList.do?companyId=' + companyId + '&type=1a'
            # url='https://glxy.mot.gov.cn/company/getCompanyAchieveList.do?companyId=596b4e9580f94532ad6c066f3701aa07&type=1a'
            data={
                'page': prj_page,
                'rows':'15',
                'sourceInfo':'1',
            }
            page_text = requests.post(url=url, headers=headers, data=data, verify=False).json()
            # print(f'page_text:{page_text}')
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
            try:
                if prjid_list == prjid_pre_list:  # 过虑重复项目
                    break
            except NameError:
                pass
            prjid_pre_list = copy.copy(prjid_list)
            # 3.获得公司设计项目ramark内容
            for prjid in prjid_list:
                prj_url='https://glxy.mot.gov.cn/company/getCompanyAchieveInfo.do'
                prjdata={
                    'id': prjid,
                    'companyid': companyId,
                }
                prjcont= requests.post(url=prj_url, headers=headers, data=prjdata, verify=False).json()
                res=prjcont['data']
                res['remark']=res['remark'].replace('\n','')
                res['remark']=res['remark'].replace('\r', '')
                temp = '\n'+res['companyId']+"\t"+res['corpName']+"\t初步设计批复时间："+res['designAllowDate']+"\t施工图批复时间："+res['drawingAllowDate']+"\t"+res['id']+"\t"+res['projectType']+"\t"+res['projectName']+"\t"+res['remark']
                filename = kw+'.txt'
                with open(filename, 'a', encoding='utf-8') as fp:
                    fp.write(str(temp))
    # print("用时：%f" % (time.time() - start_time))


def get_companyId(headers, url, start_page: int = 1, end_page: int = 3) -> dict:
    # 1.获得公司名称及ID
    # headers = {
    #     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    # }
    # url = 'https://glxy.mot.gov.cn/company/getCompanyAptitude.do'
    id_list = []
    corpName_list = []
    end_page += 1
    for corp_page in range(start_page, end_page):
        param = {
            'page': corp_page,
            'rows': '15',
            'type': '2',
            'text': '',
        }
        page_text = requests.post(url=url, headers=headers, data=param, verify=False).json()
        # print(f'page_text:{page_text}')
        # id_list = []
        # corpName_list = []
        for dic in page_text['rows']:
            id_list.append(dic['id'])
            corpName_list.append(dic['corpName'])
    companyId_dic = {'id': id_list, 'corpName': corpName_list}
    return companyId_dic


def get_pageRange(path):
    regx = r'查询企业页码范围：(\d*)\D(\d*)'
    # config_data = getData_list(config_path, regx)
    if not os.path.exists(path):
        print(f"{path}文件不存在")
        quit()
    with open(path, 'r', encoding="UTF-8") as file:
        fileData = file.read()
    fileData_list = re.findall(regx, fileData, re.MULTILINE)
    regx = r'查询企业设计项目页码范围：(\d*)\D(\d*)'
    fileData_list.append(re.findall(regx, fileData, re.MULTILINE)[0])
    # page1 = fileData_list[0][0]
    # page2 = fileData_list[0][1]
    # print(fileData_list)
    # print(page1, page2)
    return fileData_list


def main():
    # 功能：获得https://glxy.mot.gov.cn/->从业企业->设计企业->业绩信息->总承包业绩（已建、在建）信息
    # 默认输出到当前路径company_glxy_data.txt中
    # 开始前需要配置当前路径中glxy_config.txt
    #   查询企业页码范围：6-7
    #   查询企业设计项目页码范围：1-40
    start_time = time.time()
    path = os.path.abspath('glxy_config.txt')
    page_range_list = get_pageRange(path)
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    url = 'https://glxy.mot.gov.cn/company/getCompanyAptitude.do'
    # 1.获得公司名称及ID
    company_start_page = int(page_range_list[0][0])
    company_end_page = int(page_range_list[0][1])
    companyId_dic = get_companyId(headers, url, company_start_page, company_end_page)

    # 2.获得公司设计项目
    # headers = {
    #     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    # }
    company_prj_start_page = int(page_range_list[1][0])
    company_prj_end_page = int(page_range_list[1][1])
    output_company_glxy_data(headers, companyId_dic['id'], companyId_dic['corpName'], start_page=company_prj_start_page,
                             end_page=company_prj_end_page)
    print("用时：%f" % (time.time() - start_time))


if __name__ == "__main__":
    main()
