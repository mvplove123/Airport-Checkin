import re

import requests
import json
import os

requests.packages.urllib3.disable_warnings()
SCKEY = os.environ.get('SCKEY')
TG_BOT_TOKEN = os.environ.get('TGBOT')
TG_USER_ID = os.environ.get('TGUSERID')
EMAIL = os.environ.get('EMAIL')
BASE_URL = os.environ.get('BASE_URL')
PASSWORD = os.environ.get('PASSWORD')

def checkin(email, password, real_domain=BASE_URL, ):
    print(email)
    email = email.split('@')
    email = email[0] + '%40' + email[1]

    html = requests.get(real_domain).text

    domain_pattern = r'<a href="(https://[^"]+)/" target="_blank">'
    domains = re.findall(domain_pattern, html)

    if domains:
        base_url = domains[0]
    else:
        base_url = 'https://ikuuu.boo/'

    session = requests.session()
    session.get(base_url, verify=False)
    login_url = base_url + '/auth/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    post_data = 'email=' + email + '&passwd=' + password + '&code='
    post_data = post_data.encode()
    response = session.post(login_url, post_data, headers=headers, verify=False)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Referer': base_url + '/user'
    }
    response = session.post(base_url + '/user/checkin', headers=headers,
                            verify=False)
    response = json.loads(response.text)
    print(response['msg'])
    return email + response['msg']


def output(username, password):
    result = checkin(email=username, password=password)
    if SCKEY != '':
        sendurl = 'https://sctapi.ftqq.com/' + SCKEY + '.send?title=机场签到&desp=' + result
        r = requests.get(url=sendurl)
    if TG_USER_ID != '':
        sendurl = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={TG_USER_ID}&text={result}&disable_web_page_preview=True'
        r = requests.get(url=sendurl)


def auto_check():
    emails = EMAIL.split(",")
    for email in emails:
        username = email.split("#")[0]
        password = email.split("#")[1]
        output(username, password)


auto_check()
