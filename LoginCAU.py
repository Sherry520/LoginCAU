#!/usr/bin/env python3
import sys
import getpass
import keyring
import urllib.parse
import requests

# 服务名称（用于 keyring 存储）
SERVICE_NAME = "CAU_Campus_Network"

def get_login_url():
    """通过访问 http://www.msftconnecttest.com/redirect 获取认证网关地址"""
    try:
        response = requests.get("http://www.msftconnecttest.com/redirect", allow_redirects=False)
        if response.status_code == 302:  # 重定向状态码
            location = response.headers.get("Location", "")
            if location:
                print(f"检测到认证网关地址: {location}")
                return location
        print("错误: 无法获取认证网关地址，请检查网络连接")
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {str(e)}")
    return None

def display_author():
    """显示作者信息"""
    print("*********************************************************************")
    print("*                Secure CAU Campus Network Login                   *")
    print("* Version: v2.0                                                    *")
    print("* Author: Bruce Guo                                                *")
    print("* GitHub: https://github.com/Sherry520/LoginCAU                    *")
    print("*                                                                  *")
    print("* 安全特性:                                               *")
    print("*  - Python 3 兼容版本                                             *")
    print("*  - 使用系统密钥库存储凭据                                        *")
    print("*  - 密码输入无回显                                                *")
    print("*********************************************************************")

def get_credentials():
    """从系统密钥库获取或输入账号密码"""
    user_id = keyring.get_password(SERVICE_NAME, "last_user_id")
    
    if user_id:
        password = keyring.get_password(SERVICE_NAME, user_id)
        if password:
            return user_id, password
    
    # 交互式输入
    print("\n首次使用或需要更新凭据：")
    user_id = input("校园网账号: ").strip()
    while not user_id:
        print("账号不能为空！")
        user_id = input("校园网账号: ").strip()
    
    password = getpass.getpass("登录密码: ")
    while not password:
        print("密码不能为空！")
        password = getpass.getpass("登录密码: ")
    
    # 存储凭据
    keyring.set_password(SERVICE_NAME, "last_user_id", user_id)
    keyring.set_password(SERVICE_NAME, user_id, password)
    return user_id, password

def secure_request(url, params):
    """发送 HTTP 请求"""
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{url}?{encoded_params}"
    
    try:
        response = requests.get(full_url)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {str(e)}")
        return False

def network_login(login_url, user_id, password):
    """执行登录操作"""
    # 构造完整的登录URL
    login_path = "/drcom/login"
    full_login_url = urllib.parse.urljoin(login_url, login_path)
    
    login_params = {
        "callback": "dr1003",
        "DDDDD": f"{user_id}@cau",  # 账号需要附加 @cau
        "upass": password,          # 密码直接使用，URL 编码会自动处理特殊字符
        "0MKKey": "123456",
        "R1": "0",
        "R3": "0",
        "R6": "0",
        "para": "00",
        "v6ip": "",
        "v": "3124"  # 添加 v 参数
    }
    
    if secure_request(full_login_url, login_params):
        print("登录请求已发送，验证状态...")
        if check_login_status():
            print("登录成功")
            return True
        else:
            print("登录失败，请检查凭据")
            return False
    else:
        print("登录请求失败")
        return False

def check_login_status():
    """验证登录状态"""
    try:
        response = requests.get("http://www.msftconnecttest.com/redirect", allow_redirects=False)
        if response.status_code == 302:
            location = response.headers.get("Location", "")
            if "go.microsoft.com" in location:
                return True  # 已经登录
        return False
    except requests.exceptions.RequestException:
        return False

def network_logout(login_url):
    """执行注销"""
    # 解析登录URL的协议和主机部分
    parsed_url = urllib.parse.urlparse(login_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # 构造注销URL
    logout_url = f"{base_url}/drcom/logout"
    logout_params = {
        "callback": "dr1004",  # 注销回调函数
        "v": "3690"           # 注销版本号
    }
    print(f"正在注销，使用注销地址: {logout_url}?{urllib.parse.urlencode(logout_params)}")
    if secure_request(logout_url, logout_params):
        print("注销成功")
    else:
        print("注销失败")

if __name__ == '__main__':
    display_author()
    
    try:
        # 检查是否已经登录
        if check_login_status():
            print("提示: 您已经登录了！")
            while True:
                choice = input("是否要注销？(Y/N, 默认 N): ").strip().lower()
                if choice in ('y', 'yes'):  # 支持 y 和 yes
                    # 获取上次使用的网关地址
                    user_id = keyring.get_password(SERVICE_NAME, "last_user_id")
                    if user_id:
                        login_url = keyring.get_password(SERVICE_NAME, f"{user_id}_url")
                        if login_url:
                            network_logout(login_url)
                        else:
                            print("错误: 找不到存储的网关地址")
                    else:
                        print("错误: 找不到存储的用户ID")
                    break
                elif choice in ('n', 'no', ''):  # 支持 n、no 和直接回车
                    print("未注销，退出程序。")
                    break
                else:
                    print("无效输入，请输入 Y/N 或 Yes/No。")
            sys.exit(0)
        
        # 获取认证网关地址
        login_url = get_login_url()
        if not login_url:
            sys.exit(1)
        
        # 获取账号密码
        user_id, password = get_credentials()
        
        # 尝试登录
        if not network_login(login_url, user_id, password):
            # 如果登录失败，清除存储的凭据并提示重新输入
            print("登录失败，清除存储的凭据...")
            keyring.delete_password(SERVICE_NAME, "last_user_id")
            keyring.delete_password(SERVICE_NAME, user_id)
            user_id, password = get_credentials()
            network_login(login_url, user_id, password)
        
        # 存储网关URL
        keyring.set_password(SERVICE_NAME, f"{user_id}_url", login_url)
    except KeyboardInterrupt:
        print("\n操作已终止")
    finally:
        # 内存安全清理
        if 'password' in locals():
            del password
        sys.exit(0)
        