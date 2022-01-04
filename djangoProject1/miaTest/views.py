import json

# Create your views here.
from django.shortcuts import render
from django.shortcuts import HttpResponse
import uuid, os
import requests
import datetime


# 将请求定位到index.html文件中
def index(request):
    return render(request, 'index.html')


def exploit(request):
    return render(request, 'chrome-0day/exploit.html')


def userfile(request):
    return render(request, 'uploadFile.html')


def downloadfile(request):
    return render(request, 'downloadFile.html')


def detailFile(request):
    if request.method == "POST":
        name = request.POST.get('name')
        file = request.FILES.get('file', None)
        if not file:
            return HttpResponse("<p>您还未上传文件！</p>")
        file.name = getUUID(file.name)
        # user = User.objects.create(name=name, file=file)
        # with open(os.path.join("C:\\upload", file.name), 'wb+') as relfile:
        with open(os.path.join("/data/djangoProject1/upload", file.name), 'wb+') as relfile:
            for crunk in file.chunks():
                relfile.write(crunk)
        # resp = appUpload("C:\\upload", file.name)
        resp = appUpload("/data/djangoProject1/upload", file.name)
        print(resp)
        sha256 = resp['data']['sha256']
        reportlink = resp['data']['permalink']
        return HttpResponse(sha256 + "<br>" + reportlink)
    else:
        pass


def getUUID(filename):
    id = str(uuid.uuid4())
    extend = os.path.splitext(filename)[1]
    return id + extend


def appUpload(filepath, filename):
    apikey = '7026f7de2ff04a0b9ff5e0d3ac234a1333488cb10b7442e2b1fe8161e3400450'
    sandbox_type = 'win7_sp1_enx86_office2013'
    url = 'https://api.threatbook.cn/v3/file/upload';
    fields = {
        'apikey': apikey,
        'sandbox_type': sandbox_type,
        'run_time': 600
    }
    file_dir = filepath
    file_name = filename
    files = {
        'file': (file_name, open(os.path.join(file_dir, file_name), 'rb'))
    }
    response = requests.post(url, data=fields, files=files, verify=False)
    # print(response.json())
    return response.json()


def meetings(request):
    return render(request, 'meetings.html')


# def meetinglist(request):
#
#     # datalist = {
#     #     "total": 3,
#     #     "rows": [{
#     #         "id": 1,
#     #         "name": "mdm",
#     #         "price": 200
#     #     }]
#     # }
#     # print("testok")
#     url = 'https://api.zoom.us/v2/metrics/meetings?page_size=100';
#     return HttpResponse(json.dumps(datalist))

def meetingdetailPage(request):
    return render(request, 'meetingdetail.html')


def meetingdetail(request):
    namelist = ""
    meetingid = request.POST.get('meetingid')
    meetingid = meetingid.strip()
    meetingid = meetingid.replace(" ", "")
    urlparticipants = "https://api.zoom.us/v2/metrics/meetings/" + meetingid + "/participants?page_size=300"
    urlmeetingdetail = "https://api.zoom.us/v2/meetings/" + meetingid
    jwt = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJXRDlFUGJ3OFFkeTVIOVZwQXBXc0FnIiwiZXhwIjoiNDEwMjM5MDY2NzAwMCJ9.CviDYEow941jj5I0ZQ0mm29Bu9Zf88AaYqCAQ9GLZ4U"
    headers = {"Authorization": jwt}
    result_urlparticipants = requests.get(urlparticipants, headers=headers, verify=False)
    result_meetingdetail = requests.get(urlmeetingdetail, headers=headers, verify=False)
    html_urlparticipants = result_urlparticipants.text
    html_meetingdetail = result_meetingdetail.text
    meetingdetailjson = json.loads(html_meetingdetail)

    try:
        meetingname = meetingdetailjson["topic"]
        status = meetingdetailjson["status"]
        namelist = namelist + "Meeting Topic：" + meetingname + "\n" + "<br><br>"
        if status != "waiting":
            ret_dic = json.loads(html_urlparticipants)
            participants = ret_dic["participants"]
            namelist = namelist + "Participants:" + "<br>"
            for participant in participants:
                name = participant["user_name"]
                try:
                    jointime = participant["join_time"]
                    dt_jointime = datetime.datetime.strptime(jointime, "%Y-%m-%dT%H:%M:%SZ")
                    tz1 = dt_jointime + datetime.timedelta(hours=8)
                    tz_jointime = tz1.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    tz_jointime = ""
                try:
                    leavetime = participant["leave_time"]
                    dt_leavetime = datetime.datetime.strptime(leavetime, "%Y-%m-%dT%H:%M:%SZ")
                    tz2 = dt_leavetime + datetime.timedelta(hours=8)
                    tz_leavetime = tz2.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    tz_leavetime = ""
                namelist = namelist + "&nbsp&nbsp&nbsp&nbsp" + name + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbspjointime:" + tz_jointime + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbspleavetime:" + tz_leavetime + "\n" + "<br>"
        else:
            namelist = namelist + "Meeting Ended or Not Started" + "<br>"
    except:
        namelist = "Meeting id error, please check and input again!" + "<br>"

    return HttpResponse(namelist)


def meetingdetailtest(request):
    # 接收url传递来的search_kw参数值
    search_kw = request.GET.get('search_kw')
    namelist = ""
    items = []
    meetingid = search_kw.strip()
    allidlist = []
    if meetingid != "":
        jwt = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJXRDlFUGJ3OFFkeTVIOVZwQXBXc0FnIiwiZXhwIjoiNDEwMjM5MDY2NzAwMCJ9.CviDYEow941jj5I0ZQ0mm29Bu9Zf88AaYqCAQ9GLZ4U"
        headers = {"Authorization": jwt}
        urlallmeetings = "https://api.zoom.us/v2/metrics/meetings?page_size=100"
        result_allmeetings = requests.get(urlallmeetings, headers=headers, verify=False)
        html_allmeetings = result_allmeetings.text
        allmeetingsjson = json.loads(html_allmeetings)
        for meeting in allmeetingsjson.get("meetings"):
            id = str(meeting.get("id"))
            if id.find(meetingid) >= 0:
                allidlist.append(id)
        print(allidlist)
        if len(allidlist) == 1:
            meetingid = allidlist[0]

            meetingid = meetingid.replace(" ", "")

            urlparticipants = "https://api.zoom.us/v2/metrics/meetings/" + meetingid + "/participants?page_size=300"
            urlmeetingdetail = "https://api.zoom.us/v2/meetings/" + meetingid

            result_urlparticipants = requests.get(urlparticipants, headers=headers, verify=False)
            result_meetingdetail = requests.get(urlmeetingdetail, headers=headers, verify=False)

            html_urlparticipants = result_urlparticipants.text
            html_meetingdetail = result_meetingdetail.text

            meetingdetailjson = json.loads(html_meetingdetail)

            testline = {}
            try:
                meetingname = meetingdetailjson["topic"]
                status = meetingdetailjson["status"]
                namelist = namelist + "Meeting Topic：" + meetingname + "\n" + "<br><br>"
                if status != "waiting":
                    ret_dic = json.loads(html_urlparticipants)
                    participants = ret_dic["participants"]
                    namelist = namelist + "Participants:" + "<br>"
                    for participant in participants:
                        name = participant["user_name"]
                        testline['name'] = name
                        try:
                            jointime = participant["join_time"]
                            dt_jointime = datetime.datetime.strptime(jointime, "%Y-%m-%dT%H:%M:%SZ")
                            tz1 = dt_jointime + datetime.timedelta(hours=8)
                            tz_jointime = tz1.strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            tz_jointime = ""
                        try:
                            leavetime = participant["leave_time"]
                            dt_leavetime = datetime.datetime.strptime(leavetime, "%Y-%m-%dT%H:%M:%SZ")
                            tz2 = dt_leavetime + datetime.timedelta(hours=8)
                            tz_leavetime = tz2.strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            tz_leavetime = ""
                        testline['jointime'] = tz_jointime
                        testline['leavetime'] = tz_leavetime
                        items.append(testline.copy())
                        namelist = namelist + "&nbsp&nbsp&nbsp&nbsp" + name + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbspjointime:" + tz_jointime + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbspleavetime:" + tz_leavetime + "\n" + "<br>"
                else:
                    namelist = namelist + "Meeting Ended or Not Started" + "<br>"
            except:
                namelist = "Meeting id error, please check and input again!" + "<br>"
    print(str(items))
    return HttpResponse(json.dumps(items))


if __name__ == '__main__':
    tt = "2021-12-30T07:36:41Z"
    dt = datetime.datetime.strptime(tt, "%Y-%m-%dT%H:%M:%SZ")
    tz = dt + datetime.timedelta(hours=8)
    print(tz.strftime("%Y-%m-%d %H:%M:%S"))
