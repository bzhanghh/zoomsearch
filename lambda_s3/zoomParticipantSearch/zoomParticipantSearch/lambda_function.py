import json
import requests
import datetime


def lambda_handler(event, context):
    search_kw = event['queryStringParameters']['meetingid']
    namelist = ""
    items = []
    meetingid = search_kw.strip()
    jwt = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJXRDlFUGJ3OFFkeTVIOVZwQXBXc0FnIiwiZXhwIjoiNDEwMjM5MDY2NzAwMCJ9.CviDYEow941jj5I0ZQ0mm29Bu9Zf88AaYqCAQ9GLZ4U"
    headers = {"Authorization": jwt}
    meetingid = str(meetingid).lower()
    if meetingid.startswith("web"):
        meetingid = meetingid.replace(" ", "")
        meetingid = str(meetingid)[3:]
        urlparticipants = "https://api.zoom.us/v2/metrics/webinars/" + meetingid + "/participants?page_size=1000"
        result_urlparticipants = requests.get(urlparticipants, headers=headers, verify=False)
        html_urlparticipants = result_urlparticipants.text
        testline = {}
        try:
            ret_dic = json.loads(html_urlparticipants)
            participants = ret_dic["participants"]
            namelist = namelist + "Participants:" + "<br>"
            for participant in participants:
                name = participant["user_name"]
                testline['name'] = name
                try:
                    email = participant["email"]
                    testline['email'] = email
                except:
                    email = ""
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
    else:
        allidlist = []
        if meetingid != "":

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
                                email = participant["email"]
                                testline['email'] = email
                            except:
                                email = ""
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

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(items)
    }