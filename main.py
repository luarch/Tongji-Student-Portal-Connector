#!/usr/bin/env python3
import urllib.request as ur
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, quote
import requests
import os

LOGIN_SERVLET = "https://wlan.ct10000.com/authServlet"
LOGOUT_SERVLET = "https://wlan.ct10000.com/logoutServlet"

USERNAME = os.getenv('TJSP_USER', '102471252826')
PASSWORD = os.getenv('TJSP_PASSWD', '028723')


def getUrl():
    testUrl = "http://baidu.com"
    opener = ur.FancyURLopener()
    r = opener.open(testUrl)
    if r.url == testUrl:
        return 0
    else:
        return r

def parseParamStr(url):
    paramStr = urlparse(url).query
    paramStr = parse_qs(paramStr)
    paramStr = paramStr['paramStr'][0]
    paramStrEnc = quote(paramStr)
    return (paramStr, paramStrEnc)

def parseLoginPage(portPage):
    html_content = chinaNetPort.file.read().decode()
    bs4 = BeautifulSoup(html_content, "html.parser")
    loginUrl = bs4.frame.findChild()['src']
    loginUrl = "http://wlan.ct10000.com" + loginUrl

    paramStr, paramStrEnc = parseParamStr(loginUrl)

    payload = {
        'paramStr': paramStr,
        'paramStrEnc': paramStrEnc,
        'UserName': USERNAME,
        'PassWord': PASSWORD,
        'verifycode': '',
        'UserType': 1,
        'isChCardUser': False,
        'isWCardUser': False,
        'province': 'student',
        'isRegisterRealm': False,
        'defaultProv': 'sh',
        'isCookie': 0,
    }
    r = requests.post(LOGIN_SERVLET, data=payload)

    logoutUrl = r.url

    if 'fail' in r.url:
        print('Your username & password does not match')
        exit()

    print(logoutUrl)
    print('\nUse the URL above \nor press any key to log out.')
    input()

    paramStr, paramStrEnc = parseParamStr(logoutUrl)
    payload2 = {
        'paramStr': paramStr,
        'paramStrEnc': paramStrEnc,
        'pagetype': 5,
        'ip': '127.0.0.1',
        'realIp': '127.0.0.1',
        'bOffline': ''
    }
    r = requests.post(LOGOUT_SERVLET, data=payload2)

    print('Logged out.')

if __name__ == "__main__":
    print('''
======================
TONGJI.STUDENT.PORTAL
Connector
======================

        ''')

    chinaNetPort = getUrl()
    if not chinaNetPort:
        print("You are connected to the Internet.")
        exit()

    parseLoginPage(chinaNetPort)

