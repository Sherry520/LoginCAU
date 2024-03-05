# LoginCAU

# Introduction
A *Python* script for login **Campus Gateway** of China Agricultural University in Linux.
Some highlight features:
- Convenience: Login information is stored locally. You don't need to type it every time.
- Secure: Password is not cleartext.
- Automated: The login address is automatically obtained.

# Prerequisites
Python2 : this script supports ***Python2*** only.
```Pyhton
python2 -m pip install requests
```
# Usage
```Pyhton
python .\LoginCAU.py
```
## Input your account ID and Password
```bash
> input your ID:<Your Account ID>
> input your password:<password>
```
## Log in/out
```bash
> you have already logged in, do you want to log out?(y[es]/n[o], default no):
```
# Question
1. Logout failed! You have to logout by your browser.

    Answer: This happened only when you use the script first time in a net logged machine. You have to log out by handled only once.
# License
The program package is released under the GNU Lesser General Public License version 3.0
(LGPLv3). See the `LICENSE` file for the complete LGPL license text.
