#!/usr/bin/python
# coding=utf-8
import pickle
import base64
import hashlib
import httplib
from urlparse import urljoin
import requests
import re
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import os
import platform
import time
# from io import open

# Following codes are copied from network
class AuthCode(object):
 
    @classmethod
    def encode(cls, string, key, expiry=0):
        return cls._auth_code(string, 'ENCODE', key, expiry)
 
    @classmethod
    def decode(cls, string, key, expiry=0):
        return cls._auth_code(string, 'DECODE', key, expiry)
 
    @staticmethod
    def _md5(source_string):
        return hashlib.md5(source_string).hexdigest()
 
    @classmethod
    def _auth_code(cls, input_string, operation='DECODE', key='', expiry=3600):
        rand_key_length = 4
        key = cls._md5(key)
        key_a = cls._md5(key[:16])
        key_b = cls._md5(key[16:])
        if rand_key_length:
            if operation == 'DECODE':
                key_c = input_string[:rand_key_length]
            else:
                key_c = cls._md5(str(time.time()))[-rand_key_length:]
        else:
            key_c = ''
        crypt_key = key_a + cls._md5(key_a + key_c)
        if operation == 'DECODE':
            handled_string = base64.b64decode(input_string[rand_key_length:])
        else:
            expiration_time = expiry + int(time.time) if expiry else 0
            handled_string = '%010d' % expiration_time + \
                cls._md5(input_string + key_b)[:16] + input_string
        rand_key = list()
        for i in xrange(256):
            rand_key.append(ord(crypt_key[i % len(crypt_key)]))
        box = range(256)
        j = 0
        for i in xrange(256):
            j = (j + box[i] + rand_key[i]) % 256
            tmp = box[i]
            box[i] = box[j]
            box[j] = tmp
        result = ''
        a = 0
        j = 0
        for i in xrange(len(handled_string)):
            a = (a + 1) % 256
            j = (j + box[a]) % 256
            tmp = box[a]
            box[a] = box[j]
            box[j] = tmp
            result += chr(ord(handled_string[i]) ^ (box[(box[a]+box[j]) % 256]))
        if operation == 'DECODE':
            if (int(result[:10]) == 0 or (int(result[:10]) - time.time() > 0)) and \
                    (result[10:26] == cls._md5(result[26:] + key_b)[:16]):
                output_string = result[26:]
            else:
                output_string = ''
        else:
            output_string = key_c + base64.b64encode(result)
        return output_string


def getLoginUrl():
    # 地址跳转
    conn = httplib.HTTPConnection("www.msftconnecttest.com")
    conn.request('GET', '/redirect', headers={
                 "Host": "www.msftconnecttest.com", "User-Agent": "MMLE", "Accept": "text/plain"})
    res = conn.getresponse()
    # 获取跳转地址
    target = res.getheader("location")
    domain = re.findall(ur'^(?:https?:\/\/)?([^\/]+)', target)
    if res.status == 302:
        if domain[0] == 'go.microsoft.com':
            conn.close()
            return 'logged'
        else:
            conn.close()
            return target
    else:
        conn.close()
        return 'error'


def displayAuthor():
    print "*********************************************************************"
    print "*                Login CAU                                          *"
    print "*Note: This program is only available for Python2                   *"
    print "*Version:V0.1                                                       *"
    print "*Author:Bruce Guo                                                   *"
    print "*  IF you find any bugs or you have some suggestions, please write  *"
    print "*a ISSUE in https://github.com/Sherry520/LoginCAU                   *"
    print "*********************************************************************"


def fin():
    inp = raw_input("enter to exit\n")
    os._exit(0)


def getPWD():
    syst = platform.system()
    if syst == "Windows":
        return os.getcwdu()+'\\'
    else:
        return os.getcwdu()+'/'


def checkPassFile(LoginURL,flag=1):
    data = {}
    data1 = {}
    py_path = getPWD()
    try:
        if flag == 1:
            f = open(py_path+'data.pkl', 'r')
            data = pickle.load(f)
            f.close()
            if data['ID'] == '' or data['Pass'] == '':
                raise ValueError
            else:
                # 如果只缺少Url信息，则在登陆时添加
                if ('Url' not in data.keys()) or data['Url'] == "WrongURL" or data['Url'] == '' or data['Url'] == 'logged':
                    data['Url'] = LoginURL
                    f = open(py_path+'data.pkl', 'wb')
                    pickle.dump(data, f)
                    f.close()
                tmp = AuthCode.decode(data['Pass'], data['ID'])
                data['Pass'] = tmp
        if flag == 0:
            os.unlink(py_path+'data.pkl')
            raise ValueError
    # 抛出异常后，才会运行下面代码
    except Exception, e:
        if flag == 1:
            print "It seems that you havn't save your ID and Password or the File is destroyed, \n please input your ID and Password. And these will be encrypted."
        else:
            print "Please re-input your ID and Password"
            #data1['Url'] = LoginURL
        ID = raw_input('input your ID:')
        Pass = raw_input("input your password:")
        data = {'ID': ID, 'Pass': Pass, 'Url': LoginURL}
        EncodePass = AuthCode.encode(Pass, ID)
        data1['ID'] = data['ID']
        data1['Pass'] = EncodePass
        data1['Url'] = LoginURL
        f = open(py_path+'data.pkl', 'wb')
        pickle.dump(data1, f)
        f.close()
    return data

def netLogIn(LoginURL, logName, logPass):
    # 登录参数，除了用户名和密码之外的参数，不用全写上，不然可能有问题
    params = "/drcom/login?callback=dr1003&DDDDD="+logName + "&upass="+logPass+"&0MKKey=123456&R1=0&R3=0&R6=0&para=00&v6ip="
    # print LoginURL[7:]
    # return 0
    url = urljoin(LoginURL, params)
    res = requests.get(url)
    res.close()
 
    # 测试是否已经登陆
    conn = httplib.HTTPConnection("www.msftconnecttest.com")
    conn.request('GET', '/redirect', headers={"Host": "www.msftconnecttest.com", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", "Accept": "text/plain"})
    res = conn.getresponse()
    target = res.getheader("location")
    domain = re.findall(ur'^(?:https?:\/\/)?([^\/]+)', target)
    # 因为是用跳转链接测试，正常情况下，它永远返回302
    if res.status == 302:
        conn.close()
        # 跳到微软，已经在登录状态
        if domain[0] == 'go.microsoft.com':
            conn.close()
            print "login success"
        # 要跳到登录页
        elif domain[0] == LoginURL[7:]:
            # 保存的信息不对。因为在netLogIn()运行之前，已经强制获取了ID和Pass信息
            tmp = raw_input("ID or Password error or you don't have enough flow,do you want to correct your ID and Password?(y/n):")
            if tmp.lower() == 'yes' or tmp.lower() == 'y':
                data1 = checkPassFile(LoginURL,0)
                netLogIn(LoginURL, data1['ID'], data1['Pass'])
        else:
            print "sorry ,bye bye"
    else:
        print "unkonwn error"


def netLogOut(LoginURL):
    params = "/drcom/logout?callback=dr1002"
    url = urljoin(LoginURL, params)
    res = requests.get(url)
    print "Log Out"


if __name__ == '__main__':
    displayAuthor()
    LoginURL = getLoginUrl()
    data = checkPassFile(LoginURL,1)
    if LoginURL == 'logged':
        # 检测到已经登陆，是否要退出？
        tmp = raw_input(
                "you have already logged in, do you want to log out?(y[es]/n[o], default no):")
        if tmp.lower() == 'yes' or tmp.lower() == 'y':
            try:
                netLogOut(data['Url'])
            except Exception ,e:
                print "Logout failed! You have to logout by Chrome in Windows"
                py_path = getPWD()
                # 提取信息
                f = open(py_path+'data.pkl', 'r')
                data1 = pickle.load(f)
                f.close()
                # 重新写入信息
                f = open(py_path+'data.pkl', 'wb')
                data1['Url'] = "WrongURL"
                pickle.dump(data1, f)
                f.close()
                fin()
    elif data['ID'] != '' and data['Pass'] != '':
        netLogIn(LoginURL, data['ID'], data['Pass'])
    else:
        print "network error"
