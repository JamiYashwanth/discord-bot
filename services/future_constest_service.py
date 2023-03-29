import requests 
import json 
from datetime import datetime


def getFutureContest(url):
    response_API = requests.get(url)
    data = response_API.text 
    parse_json = json.loads(data)
    return parse_json

def convertToGoogleCalendarTime(t):
    dt = datetime.strptime(t, "%Y-%m-%d %H:%M:%S %Z")
    time_string_converted = dt.strftime("%Y%m%dT%H%M%SZ")
    return time_string_converted

def contestHost(host):
    em = '\N{EN SPACE}'
    sq = '\N{WHITE SQUARE WITH UPPER RIGHT QUADRANT}'
    newline = '\n\n'

    if host == 'codechef':
        contests = getFutureContest('https://kontests.net/api/v1/code_chef') 
        contests.reverse()
        desc = ''
        for contest in contests: 
            contest_name = contest['name']
            contest_start_time = contest['start_time']
            contest_end_time = contest['end_time']
            contest_url = contest['url']
            url_contest_name = contest_name.replace(" ", "+")
            convertedStartTime = convertToGoogleCalendarTime(contest_start_time)
            convertedEndTime = convertToGoogleCalendarTime(contest_end_time)
            remind_me = "https://calendar.google.com/calendar/u/0/r/eventedit?text=" + url_contest_name + "&dates=" + convertedStartTime + "/" +  convertedEndTime
            desc += (f'`{em}{contest_name}{em}|'
            f'{em}{contest_start_time}{em}|'
             f'{em}{contest_end_time}{em}|'
            f'{em}`[`link {sq} `]({contest_url} "Link to contest page"){em}|')
            desc += (f'{em}[`remind {sq}`]({remind_me})')
            desc += newline
        return desc

    if host == 'codeforces':
        contests = getFutureContest('https://kontests.net/api/v1/codeforces') 
        desc = ''
        for contest in contests: 
            contest_name = contest['name']
            contest_start_time = datetime.strptime(contest['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            contest_end_time = datetime.strptime(contest['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            contest_url = contest['url']
            url_contest_name = contest_name.replace(" ", "+")
            new_contest_start_time = str(contest_start_time) +  " UTC"
            new_contest_end_time = str(contest_end_time) + " UTC"
            convertedStartTime = convertToGoogleCalendarTime(new_contest_start_time) 
            convertedEndTime = convertToGoogleCalendarTime(new_contest_end_time)
            remind_me = "https://calendar.google.com/calendar/u/0/r/eventedit?text=" + url_contest_name + "&dates=" + convertedStartTime + "/" + convertedEndTime
            desc += (f'`{em}{contest_name}{em} |'
            f'{em}{contest_start_time}{em}UTC |'
            f'{em}{contest_end_time}{em}UTC |'
            f'{em}`[`link {sq}`]({contest_url} "Link to contest page")|')
            desc += (f'{em}[`remind {sq}`]({remind_me})')
            desc += newline
        return desc

    if host == 'leetcode':
        contests = getFutureContest('https://kontests.net/api/v1/leet_code') 
        contests.reverse()
        desc = ''
        for contest in contests: 
            contest_name = contest['name']
            contest_start_time = datetime.strptime(contest['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            contest_end_time = datetime.strptime(contest['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            contest_url = contest['url']
            url_contest_name = contest_name.replace(" ", "+")
            new_contest_start_time = str(contest_start_time) +  " UTC"
            new_contest_end_time = str(contest_end_time) + " UTC"
            convertedStartTime = convertToGoogleCalendarTime(new_contest_start_time) 
            convertedEndTime = convertToGoogleCalendarTime(new_contest_end_time)
            remind_me = "https://calendar.google.com/calendar/u/0/r/eventedit?text=" + url_contest_name + "&dates=" + convertedStartTime + "/" + convertedEndTime
            desc += (f'`{em}{contest_name}{em} |'
            f'{em}{contest_start_time}{em}UTC |'
            f'{em}{contest_end_time}{em}UTC |'
            f'{em}`[`link {sq}`]({contest_url} "Link to contest page")|')
            desc += (f'{em}[`remind {sq}`]({remind_me})')
            desc += newline
        return desc

    if host == 'hackerearth':
        contests = getFutureContest('https://kontests.net/api/v1/hacker_earth')
        desc = ''
        for contest in contests: 
            contest_name = contest['name']
            contest_start_time = datetime.strptime(contest['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            contest_end_time = datetime.strptime(contest['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            contest_url = contest['url']
            url_contest_name = contest_name.replace(" ", "+")
            new_contest_start_time = str(contest_start_time) +  " UTC"
            new_contest_end_time = str(contest_end_time) + " UTC"
            convertedStartTime = convertToGoogleCalendarTime(new_contest_start_time) 
            convertedEndTime = convertToGoogleCalendarTime(new_contest_end_time)
            remind_me = "https://calendar.google.com/calendar/u/0/r/eventedit?text=" + url_contest_name + "&dates=" + convertedStartTime + "/" + convertedEndTime
            desc += (f'`{em}{contest_name}{em} |'
            f'{em}{contest_start_time}{em}UTC |'
            f'{em}{contest_end_time}{em}UTC |'
            f'{em}`[`link {sq}`]({contest_url} "Link to contest page")|')
            desc += (f'{em}[`remind {sq}`]({remind_me})')
            desc += newline
        return desc