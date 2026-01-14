# -*- coding: utf-8 -*-
import datetime
import json
import sqlite3
import os
from time import sleep

from xhs import DataFetchError, XhsClient


def get_chrome_cookies():
    """从本地 Chrome 浏览器数据库中获取小红书 Cookie"""
    
    print("[Cookie 获取] 正在从 Chrome 浏览器中获取 Cookie...\n")
    
    # Chrome 数据库路径 (Windows)
    chrome_path = os.path.expanduser(
        "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies"
    )
    
    if not os.path.exists(chrome_path):
        print(f"? 未找到 Chrome Cookie 数据库: {chrome_path}")
        print("? 请确保已安装 Chrome 浏览器，并至少访问过一次小红书")
        return None
    
    print(f"[Cookie 获取] Chrome Cookie 数据库路径: {chrome_path}")
    
    try:
        # 连接到 Chrome 的 Cookie 数据库
        conn = sqlite3.connect(chrome_path)
        cursor = conn.cursor()
        
        # 查询小红书相关的 Cookie
        cursor.execute("""
            SELECT name, value, host_key 
            FROM cookies 
            WHERE host_key LIKE '%xiaohongshu%'
            ORDER BY host_key
        """)
        
        cookies_data = cursor.fetchall()
        conn.close()
        
        if not cookies_data:
            print("? 在 Chrome 中未找到小红书 Cookie")
            print("? 请先在 Chrome 中访问 https://www.xiaohongshu.com 并登录")
            return None
        
        # 转换为字典
        cookies_dict = {}
        for name, value, host in cookies_data:
            cookies_dict[name] = value
            if name in ["a1", "webId", "gid", "web_session"]:
                print(f"[Cookie 获取] ? {name}: {value[:50]}...")
        
        print(f"\n[Cookie 获取] ? 从 Chrome 获取到 {len(cookies_dict)} 个 Cookie\n")
        return cookies_dict
        
    except sqlite3.OperationalError as e:
        print(f"? 无法读取 Chrome Cookie 数据库: {str(e)}")
        print("? 请确保 Chrome 浏览器已关闭，然后重试")
        return None


def sign_with_external_service(uri, data=None, a1="", web_session=""):
    """
    使用外部签名服务或直接调用小红书的签名接口
    这里使用库自带的签名函数（需要正确的 a1）
    """
    from xhs.help import sign as xhs_sign
    
    try:
        signs = xhs_sign(uri, data, a1=a1)
        return {
            "x-s": signs["x-s"],
            "x-t": signs["x-t"],
            "x-s-common": signs.get("x-s-common", ""),
        }
    except Exception as e:
        print(f"[签名] 错误: {str(e)}")
        raise


if __name__ == '__main__':
    print("=" * 60)
    print("小红书爬虫 - 使用真实浏览器 Cookie")
    print("=" * 60)
    print(f"当前时间: {datetime.datetime.now()}\n")
    
    # 第一步：从 Chrome 获取 Cookie
    cookies_dict = get_chrome_cookies()
    
    if not cookies_dict:
        print("? 无法获取 Cookie，程序退出")
        exit(1)
    
    # 第二步：将 Cookie 转换为字符串
    cookie_string = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
    
    # 第三步：初始化 XhsClient
    print("[主程序] 初始化 XhsClient...")
    xhs_client = XhsClient(cookie=cookie_string, sign=sign_with_external_service)
    
    # 添加额外的请求头，伪装成真实浏览器
    xhs_client.session.headers.update({
        "referer": "https://www.xiaohongshu.com/",
        "origin": "https://www.xiaohongshu.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-language": "zh-CN,zh;q=0.9",
    })
    
    # 第四步：带重试的 API 调用
    max_api_retries = 3
    api_success = False
    
    for retry_count in range(max_api_retries):
        try:
            print(f"\n[主程序] 第 {retry_count + 1}/{max_api_retries} 次尝试获取用户信息...")
            sef_info = xhs_client.get_user_info("360485984")
            
            print("\n" + "=" * 60)
            print("? 获取成功！用户信息如下：")
            print("=" * 60)
            print(json.dumps(sef_info, indent=4, ensure_ascii=False))
            
            api_success = True
            break
            
        except Exception as e:
            error_name = type(e).__name__
            error_msg = str(e)
            
            if "NeedVerifyError" in error_name or "验证码" in error_msg:
                print(f"\n??  需要验证码")
                print(f"错误信息: {error_msg}")
                print(f"? 请在 Chrome 浏览器中访问小红书并完成验证")
                print(f"验证完成后，按 Enter 继续...\n")
                input(">>> ")
                sleep(3)
                
            elif "IPBlockError" in error_name or "IP" in error_msg:
                print(f"\n? IP 被限制: {error_msg}")
                break
                
            elif retry_count < max_api_retries - 1:
                print(f"\n? 错误: {error_name}")
                print(f"错误信息: {error_msg}")
                print(f"等待 3 秒后重试...")
                sleep(3)
                
            else:
                print(f"\n? 最终失败: {error_name}: {error_msg}")
                import traceback
                traceback.print_exc()
    
    if not api_success:
        print("\n? 无法获取用户信息")
        print("? 可能的原因：")
        print("  1. Cookie 已过期 - 请在 Chrome 中重新登录小红书")
        print("  2. IP 被限制 - 请更换网络或等待")
        print("  3. 账号被限制 - 请检查小红书账号状态")
