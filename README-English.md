# LoginCAU

# Introduction
A *Python* script for login **Campus Gateway** of China Agricultural University in Linux.

Some highlight features:
- Convenience: Login information is stored locally. You don't need to type it every time.
- Secure: Password is not cleartext.
- Automated: The login address is automatically obtained for WLAN or LAN.

# Prerequisites
Python2 : this script supports ***Python2*** only.
```bash
# install pip for python2 if needed
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
python2 get-pip.py
# install requests module
python2 -m pip install requests
```
# Usage
## Download and Run
```bash
git clone https://github.com/Sherry520/LoginCAU.git
cd LoginCAU
python2 ./LoginCAU.py
```
## Input your account ID and Password
```bash
> input your ID:<Your Account ID>
> input your password:<password>
```
## Log in/out
```bash
> You have already logged in, do you want to log out? (y[es]/n[o], default no):
```
## **Data**
In LoginCAU.py's directory, user information is stored in the ***data.pkl*** file, which contains the login ID and encrypted password.

To further enhance security, you can modify the file permissions so that only you have read and write permissions:
```bash
chmod 600 data.pkl
```
# Question
1. Logout failed! You have to logout using your browser.

    Answer: This only happens the first time you use this script on a networked device. You have to log out once.
# License
The program package is released under the GNU GENERAL PUBLIC LICENSE version 3.0
(GPLv3). See the `LICENSE` file for the complete GPL license text.
