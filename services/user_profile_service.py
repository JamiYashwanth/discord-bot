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
        self._image = ''
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
        image_tag = r.html.find("img.profileImage")[0]
        self._image = image_tag.attrs["src"]
        max_rating = rating_header.find('small')[0].text[1:-1].split()[2]
        rating_star = len(r.html.find(".rating-star",first=True).find('span'))
        ranks = r.html.find('.rating-ranks',first=True).find('strong')
        global_rank = ranks[0].text
        country_rank = ranks[1].text
        print(rating_header, rating)
        return {'name': Name, 'rating':rating,'max_rating':max_rating,
                'global_rank':global_rank,'country_rank':country_rank
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
            print(user)
            self._image = user['titlePhoto']
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