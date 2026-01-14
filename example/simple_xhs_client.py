# -*- coding: utf-8 -*-
"""
使用真实 Cookie 和 XhsClient 的最简单方案
"""
import datetime
import json
from time import sleep

from xhs import XhsClient
from xhs.help import sign as xhs_sign


def sign_wrapper(uri, data=None, a1="", web_session=""):
    """签名函数包装"""
    try:
        result = xhs_sign(uri, data, a1=a1)
        return {
            "x-s": result.get("x-s", ""),
            "x-t": result.get("x-t", ""),
            "x-s-common": result.get("x-s-common", ""),
        }
    except Exception as e:
        print(f"[签名错误] {str(e)}")
        raise


if __name__ == '__main__':
    print("=" * 60)
    print("小红书爬虫 - 使用真实浏览器 Cookie")
    print("=" * 60)
    print(f"当前时间: {datetime.datetime.now()}\n")
    
    # ===== 获取 Cookie =====
    print("[步骤 1] 获取 Cookie")
    print("-" * 60)
    print("请按以下步骤获取 Cookie：")
    print("  1. 打开 Chrome 浏览器")
    print("  2. 访问 https://www.xiaohongshu.com")
    print("  3. 登录你的账号")
    print("  4. 按 F12 打开开发者工具")
    print("  5. 切换到 Network 标签")
    print("  6. 刷新页面")
    print("  7. 点击任意请求")
    print("  8. 在 Request Headers 中找到 cookie: 字段")
    print("  9. 复制完整的 Cookie 值\n")
    
    print("请粘贴你的 Cookie：")
    cookie = input(">>> ").strip()
    
    if not cookie:
        print("? Cookie 不能为空")
        exit(1)
    
    if "a1=" not in cookie:
        print("? Cookie 中未找到 a1 字段")
        exit(1)
    
    print(f"\n? 已获取 Cookie，长度: {len(cookie)} 字符\n")
    
    # ===== 初始化 XhsClient =====
    print("[步骤 2] 初始化 XhsClient")
    print("-" * 60)
    
    xhs_client = XhsClient(cookie=cookie, sign=sign_wrapper)
    
    # 添加反爬虫对抗 Headers
    xhs_client.session.headers.update({
        "referer": "https://www.xiaohongshu.com/",
        "origin": "https://www.xiaohongshu.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    })
    
    print("? XhsClient 已初始化\n")
    
    # ===== 获取用户信息 =====
    print("[步骤 3] 获取用户信息")
    print("-" * 60)
    
    max_retries = 3
    success = False
    
    for attempt in range(max_retries):
        try:
            print(f"\n[尝试 {attempt + 1}/{max_retries}] 正在获取用户信息...")
            
            user_info = xhs_client.get_user_info("360485984")
            
            print("\n" + "=" * 60)
            print("? 获取成功！")
            print("=" * 60)
            print(json.dumps(user_info, indent=2, ensure_ascii=False))
            
            success = True
            break
            
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            
            print(f"\n? 错误: {error_type}")
            print(f"   信息: {error_msg}")
            
            if attempt < max_retries - 1:
                print(f"   等待 3 秒后重试...\n")
                sleep(3)
    
    if not success:
        print("\n? 无法获取用户信息")
        print("\n可能的原因：")
        print("  ? Cookie 已过期 - 需要重新获取")
        print("  ? 账号异常 - 请检查小红书账号状态")
        print("  ? IP 被限制 - 请稍后重试或更换网络")
