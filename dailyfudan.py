import time
from json import loads as json_loads
from lxml import etree
from requests import session
import ddddocr
import re


class Fudan:
    __doc__ = '\n    建立与复旦服务器的会话，执行登录/登出操作\n    '
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'

    def __init__(self, uid, psw, url_login='https://uis.fudan.edu.cn/authserver/login'):
        """
        初始化一个session，及登录信息
        :param uid: 学号
        :param psw: 密码
        :param url_login: 登录页，默认服务为空
        """
        self.session = session()
        self.session.headers['User-Agent'] = self.UA
        self.url_login = url_login
        self.uid = uid
        self.psw = psw

    def _page_init(self):
        """
        检查是否能打开登录页面
        :return: 登录页page source
        """
        print('◉Initiating——', end='')
        page_login = self.session.get(self.url_login)
        print('return status code', page_login.status_code)
        if page_login.status_code == 200:
            print('◉Initiated——', end='')
            return page_login.text
        print('◉Fail to open Login Page, Check your Internet connection\n')
        self.close()

    def login(self):
        """
        执行登录
        """
        page_login = self._page_init()
        print('parsing Login page——', end='')
        html = etree.HTML(page_login, etree.HTMLParser())
        print('getting tokens')
        data = {'username':self.uid, 
         'password':self.psw, 
         'service':'https://zlapp.fudan.edu.cn/site/ncov/fudanDaily'}
        data.update(zip(html.xpath('/html/body/form/input/@name'), html.xpath('/html/body/form/input/@value')))
        headers = {'Host':'uis.fudan.edu.cn', 
         'Origin':'https://uis.fudan.edu.cn', 
         'Referer':self.url_login, 
         'User-Agent':self.UA}
        print('◉Login ing——', end='')
        post = self.session.post((self.url_login),
          data=data,
          headers=headers,
          allow_redirects=False)
        print('return status code', post.status_code)
        if post.status_code == 302:
            print('\n***********************\n◉登录成功\n***********************\n')
        else:
            print('◉登录失败，请检查账号信息')
            self.close()

    def logout(self):
        """
        执行登出
        """
        exit_url = 'https://uis.fudan.edu.cn/authserver/logout?service=/authserver/login'
        expire = self.session.get(exit_url).headers.get('Set-Cookie')
        if '01-Jan-1970' in expire:
            print('◉登出完毕')
        else:
            print('◉登出异常')

    def close(self):
        """
        执行登出并关闭会话
        """
        self.logout()
        self.session.close()
        print('◉关闭会话')
        print('************************')

class Zlapp(Fudan):
    last_info = ''

    def check(self):
        """
        检查
        """
        print('◉检测是否已提交')
        get_info = self.session.get('https://zlapp.fudan.edu.cn/ncov/wap/fudan/get-info', verify=False)
        last_info = get_info.json()
        print('◉上一次提交日期为:', last_info['d']['info']['date'])
        position = last_info['d']['info']['geo_api_info']
        position = json_loads(position)
        print('◉上一次提交地址为:', position['formattedAddress'])
        today = time.strftime('%Y%m%d', time.localtime())
        if last_info['d']['info']['date'] == today:
            print('\n*******今日已提交*******')

            return True
        else:
            print('\n\n*******未提交*******')
            self.last_info = last_info['d']['info']
            return False

    def checkin(self):
        """
        提交
        """
        headers = {'Host':'zlapp.fudan.edu.cn', 
         'Referer':'https://zlapp.fudan.edu.cn/site/ncov/fudanDaily?from=history', 
         'DNT':'1', 
         'TE':'Trailers', 
         'User-Agent':self.UA}
        print('\n\n◉◉提交中')
        geo_api_info = json_loads(self.last_info['geo_api_info'])
        province = geo_api_info['addressComponent'].get('province', '')
        city = geo_api_info['addressComponent'].get('city', '')
        district = geo_api_info['addressComponent'].get('district', '')
        self.last_info['code'] = self.get_ver()
        self.last_info['sfzx'] = self.sfzx
        #self.last_info['xwszxqsffbhjf'] = 3
        if not city: 
            city = province
            self.last_info.update({'tw':'13', 'province':province, 'city':city, 'area':' '.join((city, district))})
        else:
            self.last_info.update({'tw':'13', 'province':province, 'city':city, 'area':' '.join((province, city, district))})

        save = self.session.post('https://zlapp.fudan.edu.cn/ncov/wap/fudan/save',
          data=(self.last_info),
          headers=headers,
          allow_redirects=False)
        save_msg = json_loads(save.text)['m']
        print(save_msg, '\n\n')

    def get_ver(self):
        time.sleep(1)
        ocr = ddddocr.DdddOcr()
        img = self.session.get('https://zlapp.fudan.edu.cn/backend/default/code').content
        res = ocr.classification(img)
        time.sleep(2)
        return res

    def check_change(self):
        html = self.session.get('https://zlapp.fudan.edu.cn/site/static/js/142.85116606364fc44c0516.js?v=1657286258363')
        html = html.text
        chinese = ''.join(re.findall(r'[\u4e00-\u9fa5]', html))
        
        with open('yesterday.txt', 'r', encoding='utf-8') as f:
            yesterday = f.read()

        if chinese == yesterday:
            return True
        else:
            with open('today.txt', 'w', encoding='utf-8') as f:
                f.write(chinese)
            return False






