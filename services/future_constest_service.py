import requests 
import json 
from datetime import datetime


def getFutureContest(url):
    response_API = requests.get(url)
    data = response_API.text 
    parse_json = json.loads(data)
    return parse_json

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
            desc += (f'`{em}{contest_name}{em}|'
            f'{em}{contest_start_time}{em}|'
             f'{em}{contest_end_time}{em}|'
            f'{em}`[`link {sq}`]({contest_url} "Link to contest page")')
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
            desc += (f'`{em}{contest_name}{em} |'
            f'{em}{contest_start_time}{em}UTC |'
            f'{em}{contest_end_time}{em}UTC |'
            f'{em}`[`link {sq}`]({contest_url} "Link to contest page")')
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
            desc += (f'`{em}{contest_name}{em} |'
            f'{em}{contest_start_time}{em}UTC |'
            f'{em}{contest_end_time}{em}UTC |'
            f'{em}`[`link {sq}`]({contest_url} "Link to contest page")')
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
            desc += (f'`{em}{contest_name}{em} |'
            f'{em}{contest_start_time}{em}UTC |'
            f'{em}{contest_end_time}{em}UTC |'
            f'{em}`[`link {sq}`]({contest_url} "Link to contest page")')
            desc += newline
        return desc