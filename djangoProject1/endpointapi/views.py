import json
import urllib
import datetime

import requests
from django.http import HttpResponse
from django.shortcuts import render
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



# Create your views here.

def index(request):
    return render(request, 'index.html')


def add_event(request):
    app_key = "OTNhODQ2ODlhNDdmMTE3YTM3NDQwZjcw"
    app_secret = "Mzg4YmY1YTExMGZkNjgxZTFlMGIyMGFm"
    app_id = "2qp3z9r1or"
    portal = "A9OzNNOV"
    postbody = request.GET.get("postbody")
    postbody = urllib.parse.unquote(postbody)  # urldecode解码
    if postbody.find("WindowsLogonLog") >= 0: #只处理包含“WindowsLogonLog”的入参
        postbody_json = json.loads(postbody)
        username = postbody_json["TargetUserName"]
        logonguid = postbody_json["LogonGuid"]
        TimeGenerated = postbody_json["TimeGenerated"]
        timeindex = TimeGenerated.index('.')
        TimeGenerated = TimeGenerated[0:timeindex]
        date = datetime.datetime.strptime(TimeGenerated, '%Y-%m-%dT%H:%M:%S')
        date = date + datetime.timedelta(hours=8)  # 时区+8

        computer = postbody_json["Computer"]
        computerindex = computer.index('.hillhouse')
        computername = computer[0:computerindex]  # 获取机器名

        print("postbody:" + postbody)
        # if username == "bzhang" or "hongtaoliu" or "xbai" or "mingzhang":
        if logonguid != "00000000-0000-0000-0000-000000000000":
            useremail = username + "@hillhousecap.com"
            token = get_accesstoken(app_key, app_secret)
            openid = get_user(token, portal, useremail)
            openidarray = [openid]
            msg_str = {"zh": {"message": "电脑登录提示", "content": "您好！我们注意到您的帐户在北京时间 " + str(
                date) + " 登录了机器" + computername + "。如果不是您本人操作，请及时联系 security@hillhousecap.com"},
                       "en": {"message": "Computer logon notice",
                              "content": "There was a logon attempt on computer " + computername + " at " + str(
                                  date) + " (Beijing time). Please report to security@hillhousecap.com promptly if this is a suspicous activity."}}

            send_msg(token, portal, app_id, "card", openidarray, msg_str)
            # print("response:" + json.dumps(s))
            # print(postbody)

    return HttpResponse(postbody)


def get_accesstoken(app_key, app_secret):
    url = "https://open-ushu.hillinsight.tech/cgi/token/get"
    fields = {
        'app_key': app_key,
        'app_secret': app_secret,
    }

    response = requests.get(url, data=fields, verify=False)
    data = response.json()
    accesstoken = ""
    if data["error_code"] == 0:
        accesstoken = data["result"]["access_token"]
    return accesstoken


def get_user(accesstoken, portal, query):
    openid = ""
    if accesstoken != "":
        url = "https://open-ushu.hillinsight.tech/cgi/user/search"
        fields = {
            'access_token': accesstoken,
            'portal': portal,
            'query': query,
        }
        fields = urllib.parse.urlencode(fields)
        # print(fields)
        req = url + '?' + fields
        response = requests.get(req, verify=False)
        data = response.json()
        if data["error_code"] == 0:
            openid = data["result"][0]["open_id"]
    return openid


def send_msg(accesstoken, portal, appid, msgtype, touser, msg):
    fields_get = {
        'access_token': accesstoken,
    }
    fields_get = urllib.parse.urlencode(fields_get)

    url = "https://open-ushu.hillinsight.tech/cgi/message/send_lang" + "?" + fields_get
    # print(url)
    headers = {
        "content-type": "application/json"
    }
    fields = {
        "portal": portal,
        "app_id": appid,
        "msgtype": msgtype,
        "touser": touser,
        "msg": msg,
    }
    # fields = urllib.parse.urlencode(fields)
    # print(fields)
    data = json.dumps(fields).encode("utf-8")
    response = requests.post(url, headers=headers, data=data, verify=False)
    return response.json()

def getCity(ip):
    city_en = ""
    city_zh = ""
    if ip != "":
        url_en = "http://www.ip-api.com/json/"+ip
        response_en = requests.get(url_en, verify=False)
        resp_en = response_en.json()
        city_en = resp_en["city"]

        url_zh = "https://ip.taobao.com/outGetIpInfo?ip=" + ip
        response_zh = requests.get(url_zh, verify=False)
        resp_zh = response_zh.json()
        city_zh = resp_zh["data"]["city"]
    return [city_en, city_zh]


def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position


if __name__ == '__main__':
    # token = get_accesstoken("OTNhODQ2ODlhNDdmMTE3YTM3NDQwZjcw", "Mzg4YmY1YTExMGZkNjgxZTFlMGIyMGFm")
    # print(token)
    # openid = get_user(token, "A9OzNNOV", "bzhang@hillhousecap.com")
    # openidarray = [openid]
    # msg_str = {"zh": {"message": "这是一条严重警告", "content": "你已经被FBI盯上，赶紧去楼下眉州东坡自首！！！",
    #                   "url": "https://www.ushu.tech/?lang=en", "attachmentId": "7821688145847456921"}}
    # # msg = json.dumps(msg_str)
    # print(openidarray)
    # s = send_msg(token, "A9OzNNOV", "2qp3z9r1or", "card", openidarray, msg_str)
    # print(s)

    # postbody = "%7B%22Account%22:%22HILLHOUSE%5C%5Cxbai%22,%22AccountType%22:%22User%22,%22Activity%22:%224624%20-%20An%20account%20was%20successfully%20logged%20on.%22,%22Computer%22:%22HHBJL8881.hillhouse.com.cn%22,%22EventID%22:4624,%22IPAddress%22:%22127.0.0.1%22,%22Identity%22:%22WindowsLogonLog%22,%22LogonGuid%22:%2200000000-0000-0000-0000-000000000000%22,%22LogonType%22:11,%22TargetUserName%22:%22xbai%22,%22TimeCollected%22:%222021-04-08T06:19:18.604Z%22,%22TimeGenerated%22:%222021-04-08T06:19:15.937Z%22,%22Title%22:%2201611232-832b-4ff9-917d-c3d9d914b1ad%22%7D"
    # postbody = urllib.parse.unquote(postbody)
    # postbody_json = json.loads(postbody)
    # username = postbody_json["TargetUserName"]
    # useremail = username + "@hillhousecap.com"
    # token = get_accesstoken("OTNhODQ2ODlhNDdmMTE3YTM3NDQwZjcw", "Mzg4YmY1YTExMGZkNjgxZTFlMGIyMGFm")
    # openid = get_user(token, "A9OzNNOV", useremail)
    # openidarray = [openid]
    # msg_str = {"zh": {"message": "这是一条严重警告", "content": "你已经被FBI盯上，赶紧去楼下眉州东坡自首！！！",
    #                   "url": "https://www.ushu.tech/?lang=en", "attachmentId": "7821688145847456921"}}
    #
    # s = send_msg(token, "A9OzNNOV", "2qp3z9r1or", "card", openidarray, msg_str)
    # print(s)
    # gentime = "2021-04-08T10:12:40.997Z"
    # index = gentime.index('.')
    # gentime = gentime[0:index]
    # print(gentime)
    # date = datetime.datetime.strptime(gentime, '%Y-%m-%dT%H:%M:%S')
    # date = date + datetime.timedelta(hours=8)
    # print(str(date))
    #
    # computer = "HHIT-X1CB-19.hillhouse.com.cn"
    # computerindex = computer.index('.hillhouse')
    # computername = computer[0:computerindex]
    # print(computername)

    # postbody = '{"Account":"HILLHOUSE\\bzhang","AccountType":"User","Activity":"4624 - An account was successfully logged on.","Computer":"HHIT-X1CB-19.hillhouse.com.cn","EventID":4624,"IPAddress":"127.0.0.1","Identity":"WindowsLogon1Log","LogonGuid":"60cf58b3-a532-5e0d-c87a-95031282b444","LogonType":2,"TargetUserName":"bzhang","TimeCollected":"2021-04-08T09:34:26.662Z","TimeGenerated":"2021-04-08T09:34:03.787Z","Title":"b3daac0a-8c3d-40b1-9c6e-5d7827619530"}'
    # s = postbody.find("WindowsLogon1Log")
    # print(s)

    # ip = "103.17.31.46"
    # city = getCity(ip)
    # print(city[0])
    # print(city[1])


    username = "@@@CN=S-1-5-21-1688374118-3456136249-3781258208-225624/f5e1b443-61b9-4d9f-bb3b-6d1b4a2d9988/login.windows.net/abe80f4e-79cc-4539-bbc9-cfda44c74773/llzheng@hillhousecap.com"
    if username.find("@hillhousecap.com") >= 0:
        s1 = find_last(username, "/")
        s2 = username.index("@hillhousecap.com")

        s = username[s1+1:s2]
        print(s)



