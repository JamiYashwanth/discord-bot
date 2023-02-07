from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
import requests
import json
from pytz import timezone

def getCodechefContests():
    response = requests.get("https://www.codechef.com/contests/")
    codechefContests = []
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        contests = soup.select(".content-wrapper > div")[3].find_all("tr")
        contests.pop(0)
        for contest in contests:
            elements = contest.select("td")
            elements.pop(0)
            codechefContest = {}
            codechefContest["platform"] = "CodeChef"
            codechefContest["contestName"] = elements[0].text.strip()
            codechefContest["contestLink"] = "https://www.codechef.com"+elements[0].select("a")[0].get("href")
            codechefContest["startTime"] = elements[1].get(
                "data-starttime").replace('+05:30', '+0530')
            start = datetime.strptime(
                codechefContest["startTime"][0: codechefContest["startTime"].index('+')], '%Y-%m-%dT%H:%M:%S')
            end = datetime.strptime(elements[2].get(
                "data-endtime")[0:elements[2].get("data-endtime").index("+")], '%Y-%m-%dT%H:%M:%S')
            td = (end - start)
            totalSeconds = td.total_seconds()
            days = int(totalSeconds//86400)
            remainingSeconds = totalSeconds%86400
            hours = int(remainingSeconds//3600)
            remainingSeconds = remainingSeconds%3600
            minutes = int(remainingSeconds//60)
            dayPresent = False
            hourPresent = False
            contestDuration = ""
            if days:
                dayPresent = True
                contestDuration += str(days)+" Days"
            if hours:
                if dayPresent:
                    contestDuration+=", "
                contestDuration += str(hours)+" Hours"
                hourPresent = True
            if minutes:
                if hourPresent or dayPresent:
                    contestDuration += ", "
                contestDuration += str(minutes)+" Minutes"
            contestDuration+="."
            codechefContest["contestDuration"] = contestDuration

            codechefContests.append(codechefContest)
    return codechefContests

def getCodeforcesContests():
    response = requests.get("https://codeforces.com/api/contest.list")
    codeforcesContests = []
    if response.status_code == 200:
        jsonResponse = json.loads(response.text)
        contests = jsonResponse["result"]
        for contest in contests:
            if contest["phase"] == "BEFORE":
                codeforcesContest = {}
                codeforcesContest["platform"] = "CodeForces"
                codeforcesContest["contestName"] = contest["name"]
                codeforcesContest["contestLink"] = "https://codeforces.com/contests/" + str(contest["id"])
                codeforcesContest["startTime"] = datetime.strftime(datetime.fromtimestamp(
                    contest["startTimeSeconds"]), '%Y-%m-%dT%H:%M:%S') + '+0530'
                codeforcesContest["contestDuration"] = "0" + \
                    str(contest["durationSeconds"]//3600) + ":00 hours."
                codeforcesContests.append(codeforcesContest)
    return codeforcesContests


def getHackerearthContests():
    response = requests.get(
        "https://www.hackerearth.com/chrome-extension/events/")
    hackerearthContests = []
    if response.status_code == 200:
        jsonResponse = json.loads(response.text)
        contests = jsonResponse["response"]
        for contest in contests:
            hackerearthContest = {}
            hackerearthContest["platform"] = "HackerEarth"
            if contest["status"] == "UPCOMING":
                hackerearthContest["contestName"] = contest["title"]
                hackerearthContest["contestLink"] = contest["url"]
                start = contest["start_tz"][0: contest["start_tz"].rindex(
                    ':')] + contest["start_tz"][contest["start_tz"].rindex(':')+1:]
                start = start.replace(" ", "T")
                end = contest["end_tz"].replace(" ", "T")
                try:
                    hackerearthContest["startTime"] = datetime.strptime(
                        start, '%Y-%m-%dT%H:%M:%S%z').astimezone(timezone('Asia/Kolkata')).strftime('%Y-%m-%dT%H:%M:%S%z')
                    td = datetime.strptime(
                        end, '%Y-%m-%dT%H:%M:%S%z') - datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
                    if td.days and td.seconds:
                        hackerearthContest["contestDuration"] = str(
                            td.days) + " Days & " + str((td.seconds)//3600) + " hours."
                    elif td.days:
                        hackerearthContest["contestDuration"] = str(
                            td.days) + " Days"
                    elif td.seconds and td.seconds > 3600:
                        hours = ""
                        mins = ""
                        if (td.seconds)//3600 < 10:
                            hours = "0" + str((td.seconds)//3600)
                        else:
                            hours = (td.seconds)//3600
                        if ((td.seconds)//60) % 60 < 10:
                            mins = "0" + str(((td.seconds)//60) % 60)
                        else:
                            mins = ((td.seconds)//60) % 60
                        hackerearthContest["contestDuration"] = hours + \
                            ":" + mins + " hours."
                    if hackerearthContest["contestDuration"]:
                        hackerearthContests.append(hackerearthContest)
                except:
                    continue
    return hackerearthContests

def getAtCoderContests():
    response = requests.get("https://atcoder.jp/contests/")
    atCoderContests = []
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        contests = soup.select("#contest-table-upcoming tbody tr")
        for contest in contests:
            elements = contest.find_all("td")
            atCoderContest = {}
            atCoderContest["platform"] = "AtCoder"
            atCoderContest["contestName"] = elements[1].text.strip()[elements[1].text.strip().index(
                "\n")+1:]
            atCoderContest["contestLink"] = "https://atcoder.jp" + elements[1].select("a")[0].get("href")
            atCoderContest["startTime"] = datetime.strptime(elements[0].text.replace(
                " ", "T"), '%Y-%m-%dT%H:%M:%S%z').astimezone(timezone('Asia/Kolkata')).strftime('%Y-%m-%dT%H:%M:%S%z')
            atCoderContest["contestDuration"] = elements[2].text + " hours."
            atCoderContests.append(atCoderContest)
    return atCoderContests