from requests_html import HTMLSession
import json
import requests
class UsernameError(Exception):
    pass
class PlatformError(Exception):
    pass

class User:
    def __init__(self,username=None,platform=None):
        self.__username = username
        self.__platform = platform
    def codechef(self):
        url = "https://codechef.com/users/{}".format(self.__username)
        session = HTMLSession()
        r = session.get(url,timeout=10)
        if r.status_code!=200:
            raise UsernameError("User not found")
        try:
            rating_header = r.html.find(".rating-header",first=True)
        except:
            raise UsernameError('User not found')

        try:
            rating = rating_header.find(".rating-number",first=True).text
        except:
            raise UsernameError('User not found')
        Name = r.html.find('.h2-style', first=True).text
        max_rating = rating_header.find('small')[0].text[1:-1].split()[2]
        rating_star = len(r.html.find(".rating-star",first=True).find('span'))
        ranks = r.html.find('.rating-ranks',first=True).find('strong')
        global_rank = ranks[0].text
        country_rank = ranks[1].text
        return {'name': Name, 'rating':rating,'max_rating':max_rating,
                'global_rank':global_rank,'country_rank':country_rank,
                }
    def codeforces(self):
        url = 'https://codeforces.com/api/user.info?handles={}'.format(self.__username)
        r = requests.get(url,timeout=10)
        if r.status_code !=200:
            raise UsernameError('User not found')
        r_data = r.json()
        if r_data['status']!='OK':
            raise UsernameError('User not found')
        data  = dict()
        data['status'] = 'OK'
        data.update(r_data['result'][0])
        return data
        url = "https://atcoder.jp/users/{}".format(self.__username)
        session = HTMLSession()
        r = session.get(url,timeout=10)
        if r.status_code != 200:
            raise UsernameError('User not found')
        data_tables = r.html.find('.dl-table')
        if not len(data_tables):
            raise UsernameError('User not found')
        data = dict()
        data['status']='OK'
        for table in data_tables:
            data_rows = table.find('tr')
            for row in data_rows:
                attr = row.find('th',first=True).text
                val = row.find('td',first=True).text
                data[attr]=val
                if attr == 'Highest Rating':
                    val = val.split()[0]
                    data[attr]=val
        return data
        session = HTMLSession()
        url = "https://leetcode.com/{}/".format(self.__username)
        r = session.get(url,timeout=400)
        if r.status_code!=200:
            raise UsernameError('User not found')
        check = r.html.find('.username')
        if not len(check):
            raise UsernameError('User not found')
        target = r.html.find('.list-group-item')
        basic_profile = dict()
        contest = dict()
        progress = dict()
        contribution = dict()
        for li in target:
            text = li.text.split()
            if len(text)<6:
                    if len(text)>=2 and text[0]=='Location':
                        basic_profile['location'] = li.text.replace("Location ","")
                    elif len(text)>=1 and text[0]=='School':
                        basic_profile['school'] = li.text.replace("School ","")
                    elif len(text)>=2 and text[1]=='Rating':
                        contest['rating']=text[0]
                    elif len(text)>=3 and text[1]+text[2]=='FinishedContests':
                        contest['finished_contests']=text[0]
                    elif len(text)>=5 and text[len(text)-2]+text[len(text)-1]=='GlobalRanking':
                        contest['global_ranking'] = text[0]
                        contest['total_participants'] = text[2]
                    elif len(text)>=5 and text[len(text)-2]+text[len(text)-1]=='SolvedQuestion':
                        progress['solved_question'] = text[0]
                        progress['total_question'] = text[2]
                    elif len(text)>=5 and text[len(text)-2]+text[len(text)-1]=='AcceptedSubmission':
                        progress['accepted_submission'] = text[0]
                        progress['total_submission'] = text[2]
                    elif len(text)>=4 and text[len(text)-2]+text[len(text)-1]=='AcceptanceRate':
                        progress['acceptance_rate'] = text[0]+ " %"
                    elif len(text)>=2 and text[1]=="Problems":
                        contribution['problems'] = text[0]
                    elif len(text)>=2 and text[1]=="Points":
                        contribution['points']=text[0]
                    elif len(text)>=3 and text[len(text)-2]+text[len(text)-1]=='TestCases':
                        contribution['test_cases'] = text[0]
                    elif len(text)>=2 and text[0] == 'Website':
                        basic_profile['website'] = text[1]
                    elif len(text)>=2 and text[0]=='Company':
                        basic_profile['company'] = text[1]
        data = {'status':'OK','basic_profile':basic_profile,'contest':contest,'progress':progress,'contribution':contribution,}
        return data
    def get_info(self):
        desc = ''
        if self.__platform=='codechef':
            user = self.codechef()
            name = user['name']
            rating = user['rating']
            max_rating = user['max_rating']
            country_rank = user['country_rank']
            global_rank = user['global_rank']
            desc = (f'**NAME** - {name} \n'
            f'**RATING** - {rating}\n'
             f'**MAX RATING** - {max_rating}\n'
             f'**COUNTRY RANK** - {country_rank}\n'
             f'**GLOBAL RANK** - {global_rank}\n'
           )
        if self.__platform=='codeforces':
            user = self.codeforces()
            name = user['firstName'] + ' ' + user['lastName']
            rating = user['rating']
            max_rating = user['maxRating']
            rank = user['rank']
            city = user['city']
            country = user['country']
            desc = (f'**NAME** - {name} \n'
            f'**RATING** - {rating}\n'
             f'**MAX RATING** - {max_rating}\n'
             f'**RANK** - {rank}\n'
             f'**CITY** - {city}\n'
             f'**COUNTRY** - {country}\n'
            )
        return desc
if __name__ == '__main__':
    platform = input("Enter platform: ")
    username = input("Enter username: ")
    obj = User(username,platform)
    print(obj.get_info())