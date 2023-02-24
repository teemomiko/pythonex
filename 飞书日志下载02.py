#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import urllib.parse
from requests.exceptions import RequestException
from urllib.parse import urljoin
from lxml import etree
import re
import json
from django.core.management.base import BaseCommand
import datetime
import time
import xlwt
import traceback
import openpyxl
import pandas as pd
import xlsxwriter
dataList = []
NameDict = {}
import csv

# 搜索时间范围
begin = '2021-10-27 00:00:00'
end = '2021-10-27 23:59:59'
# end = '2021-10-20 18:00:00'
class GetAuditFeishu():

    def handle(self, *args, **options):
        token = self.GetToken()
        # print('token', token)

        print("开始获取用户列表。。。。。。。。。。")
        # 获取部门列表
        delist = self.getAllDepartments(token)

        # 获取部门下的所有用户
        for de in delist:
            self.getAllUserListNextPage(token,de,'')


        print("开始获取飞书文档操作日志。。。。。。")
        # 获取飞书文档操作日志
        event_list = {"export_doc": "导出云文档", "share_to_3rdApp": "分享到第三方应用",
                      "front_export_csv": "电子表格导出CSV", "print_doc": "打印云文档", "download_file": "下载文件",
                      "copy_content": "复制内容"}
        for e in event_list:
            print("当前文档类型:{}".format(e))
            self.GetOperateDocEvent(token, e, event_list[e], '')
        self.WriteDataToExcel(dataList)

        # delist = self.getAllDepartments(token)
        # for de in delist:
        #     self.getAllUserListNextPage(token, de, '')
        #
        # with open('6月飞书文档操作数据.csv', 'r') as f:
        #     reader = csv.reader(f)
        #
        #     for row in reader:
        #         if row[2] in NameList:
        #             usename = NameList[row[2]]
        #             row[1] = usename
        #
        #         if row[-1] in NameList:
        #             owner = NameList[row[-1]]
        #             row.append(owner)
        #         dataList.append(row)
        # self.WriteDataToExcel(dataList)
        # self.getAllUserList(token)
        # self.getAllDepartments(token)
        # with open("./1.txt", "r") as f:
        #     for line in f.readlines():
        #         line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        #         userid = line.split(',')[0]
        #         count = line.split(',')[1]
        #         username = self.GetUserInfo(token,userid)
        #
        #         print(userid,count,username)
        # event_list = {"export_doc": "导出云文档", "share_to_3rdApp": "分享到第三方应用",
        #               "front_export_csv": "电子表格导出CSV", "print_doc": "打印云文档", "download_file": "下载文件","copy_content": "复制内容"}
        # for e in event_list:
        #     token = self.GetToken()
        #     print('begin------------',e)
        #     self.GetOperateDocEvent(token,e,event_list[e],'')
        # self.WriteDataToExcel(dataList)
        # self.GetUserInfo(token,"47474bdd")
        # self.getAllUserList(token)
    def GetToken(self):
        app_id = "cli_a03eff189afxxxx"
        app_secret = "wrDaJyDAqkYbLYvrhxXTOcL4R0xxxxxx"
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
        headers = {'content-type': "application/json; charset=utf-8"}
        body = {"app_id":app_id,"app_secret":app_secret}
        response = requests.post(url, data=json.dumps(body), headers=headers)
        data = response.json()
        tenant_access_token = data["tenant_access_token"]
        return tenant_access_token



    def GetOperateDocEvent(self,token,eventname,eventEname,page_token):



        oldest = int(time.mktime(time.strptime(begin, "%Y-%m-%d %H:%M:%S")))
        latest = int(time.mktime(time.strptime(end, "%Y-%m-%d %H:%M:%S")))

        if page_token != "":
            url = "https://open.feishu.cn/open-apis/admin/v1/audit_infos?latest={}&oldest={}&page_size=200&event_name={}&user_id_type=user_id&page_token={}".format(latest, oldest,eventname,page_token)
        else:
            url = "https://open.feishu.cn/open-apis/admin/v1/audit_infos?latest={}&oldest={}&page_size=200&event_name={}&user_id_type=user_id".format(latest, oldest, eventname)
        headers = {'Authorization': "Bearer" + ' ' + token}
        response = requests.get(url, headers=headers)
        data = response.json()
        try:
            for i in data['data']['items']:
                # try:
                #     username = self.GetUserInfo(token,i['operator_value'])
                # except:
                #     username = "Null"
                username = "Null"
                ownername = "Null"
                # ownername = self.GetUserInfo(token,i['objects'][0]['object_owner'])
                if i['operator_value'] in NameDict:
                    username = NameDict[i['operator_value']]
                if i['objects'][0]['object_owner'] in NameDict:
                    ownername = NameDict[i['objects'][0]['object_owner']]

                timeArray = time.localtime(i['event_time'])
                otherStyleTime = time.strftime("%Y/%-m/%-d %H:%M:%S", timeArray)
                value = [username, i['operator_value'], eventname, eventEname, i['ip'], otherStyleTime, i['objects'][0]['object_name'], i['objects'][0]['object_owner'],ownername]
                dataList.append(value)

            if "has_more" in data['data']:
                if data['data']['has_more'] == True:
                    print(data['data']['page_token'])
                    self.GetOperateDocEvent(token,eventname,eventEname,data['data']['page_token'])
        except:
            pass
            #traceback.print_exc()
            # dataList.append(i['event_name'])

    def WriteDataToExcel(self, data):
        name = ['operator', 'user_id', 'event_name', 'event_description', 'ip', 'time', 'document_name', 'owner_id','owner_name']
        test = pd.DataFrame(columns=name,data=data)
        # test.to_csv('/Users/username/Documents/py/feishu/10月/1014飞书文档操作日志.csv',encoding='utf_8_sig')
        test.to_csv('/Users/username/Documents/py/feishu/10月/1028飞书文档操作日志.csv',encoding='utf_8_sig')

    def WriteDataToExcel1(self, data):
        name = ['operator', 'user_id']
        test = pd.DataFrame(columns=name, data=data)
        test.to_csv('人员名单对照表.csv', encoding='utf_8_sig')
            # print(response.text)
    # 递归调用分页数据
    def GetOperateDocEventNextPageInfo(self,token,pageToken,eventname,latest,oldest):
        url = "https://open.feishu.cn/open-apis/admin/v1/audit_infos?latest={}&oldest={}&page_size=200&event_name={}&user_id_type=user_id&page_token={}".format(
            latest, oldest, eventname, pageToken)
        headers = {'Authorization': "Bearer" + ' ' + token}
        response = requests.get(url, headers=headers)
        datas = response.json()
        if datas['data']['has_more'] == True:
            self.GetOperateDocEventNextPageInfo(token,pageToken,eventname,latest,oldest)


    def GetUserInfo(self,token,userId):

        try:
            url = "https://open.feishu.cn/open-apis/contact/v3/users/{}".format(userId)
            body = {"user_id_type":"user_id"}
            headers = {'Authorization':"Bearer" + ' ' + token}
            response = requests.get(url, headers=headers,params=body)
            UserInfo = response.json()
            # print(UserInfo)
            # print(UserInfo)
            username = UserInfo['data']['user']['name']
        except:
            # traceback.print_exc()
            username = "Null"
        return username

    def getAllUserListNextPage(self,token,depat,pagetoken):

        # for de in delist:
        # url = "https://open.feishu.cn/open-apis/contact/v3/users?page_size=50&department_id={}&page_token={}".format(depat,pagetoken)
        url = "https://open.feishu.cn/open-apis/contact/v3/users?page_size=50&department_id={}&page_token={}&user_id_type=open_id&department_id_type=department_id".format(depat,pagetoken)
        headers = {'Authorization': "Bearer" + ' ' + token}
        response = requests.get(url, headers=headers)
        data = response.json()
        try:
            for i in data['data']['items']:
                NameDict[i['user_id']] = i['name']

            if data['data']['has_more'] == True:
                self.getAllUserListNextPage(token,depat,data['data']['page_token'])
        except:
            # pass
            traceback.print_exc()
        # for i in data['data']['items']:
        #     print(i)
        # print(response.text)


    def getAllDepartments(self,token):
        url = "https://open.feishu.cn/open-apis/contact/v3/departments"

        headers = {'Authorization': "Bearer" + ' ' + token}

        response = requests.get(url, headers=headers)
        data = response.json()
        delist = []
        for i in data['data']['items']:
            delist.append(i['department_id'])


        return delist


sav = GetAuditFeishu()
sav.handle()