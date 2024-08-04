# LoginCAU

# 介绍 
这是一个用于在Linux系统登录“中国农业大学”校园网网关的*Python*脚本；  
通俗的讲就是提供联网认证的*Python*脚本。

特点：
- 方便：通过将登录信息存储在本地，这样你就不用每次都输入账号，密码。
- 安全：用户密码是加密存储的。**【但我还是建议你往下看，让它更[安全](#安全)】**
- 智能：校园网的wifi和有线的登录网关是不一样，这个脚本可以自动识别。

# 使用前提：
Python2：这个脚本是基于***Python2***写的，并且它只支持***Python2***。

唯一需要安装的模块：
```bash
# 安装python2对应的pip【如果需要】
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
python2 get-pip.py
# 安装 requests 模块
python2 -m pip install requests
```
# 使用方法
## 下载和使用
```bash
git clone https://github.com/Sherry520/LoginCAU.git
cd LoginCAU
python2 ./LoginCAU.py
```
## 第一次使用时，会提示你输入登录网关的账户名和密码
```bash
> input your ID:<Your Account ID>
> input your password:<password>
```
## 关闭联网
```bash
> You have already logged in, do you want to log out? (y[es]/n[o], default no):
```
## **安全**
在**LoginCAU.py**脚本所在的位置，用户信息存储在一个名为***data.pkl***的文件中，其中保存有账户名和加密后的密码。

**为了更加确保安全，你应该修改这个文件的权限，使得只有你本人可以对这个文件进行“读/写”操作：**
```bash
chmod 600 data.pkl
```
# 问题解答：
1. Logout failed! You have to logout using your browser.

   回答：当在一个已经联网的设备上，你第一次使用这个脚本去退出登录（即，关闭联网），才会显示这个信息。  
   你需要使用浏览器退出联网，仅此一次。
# 许可
本项目基于GNU GENERAL PUBLIC LICENSE version 3.0(GPLv3)发行。查看`LICENSE`文件阅读完整许可内容。
