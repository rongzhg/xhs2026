import datetime
import json
from time import sleep

from playwright.sync_api import sync_playwright

from xhs import DataFetchError, XhsClient, help


# 全局变量：存储浏览器实例和 Cookie
BROWSER_SESSION = {
    "browser": None,
    "context": None,
    "page": None,
    "cookies": {},
    "playwright": None  # 保存 playwright 实例
}


def get_browser_cookies_and_session():
    """启动浏览器，获取所有 Cookie 并缓存浏览器会话"""
    global BROWSER_SESSION
    
    if BROWSER_SESSION["browser"]:
        print("[浏览器] 使用已有的浏览器会话")
        return BROWSER_SESSION["cookies"]
    
    stealth_js_path = r"C:\Users\Administrator\Documents\xhs2026\stealth.min.js"
    
    print("[浏览器] 正在启动浏览器...")
    
    # 不使用 with 语句，手动管理生命周期
    playwright = sync_playwright().start()
    BROWSER_SESSION["playwright"] = playwright
    
    chromium = playwright.chromium
    
    print("[浏览器] ✓ Playwright 初始化完成")
    print("[浏览器] 正在启动 Chromium 浏览器...")
    browser = chromium.launch(headless=False)
    print("[浏览器] ✓ Chromium 已启动，等待 4 秒...")
    sleep(4)
    
    print("[浏览器] ✓ 创建浏览器上下文...")
    browser_context = browser.new_context()
    browser_context.add_init_script(path=stealth_js_path)
    context_page = browser_context.new_page()
    
    print("[浏览器] 正在访问小红书主页...")
    context_page.goto("https://www.xiaohongshu.com")
    print("[浏览器] ✓ 页面加载完成，等待 40 秒...")
    sleep(40)
    
    # 获取浏览器自动生成的所有 Cookie
    cookies = browser_context.cookies()
    print(f"[浏览器] ✓ 获取到 {len(cookies)} 个 Cookie")
    
    for cookie in cookies:
        BROWSER_SESSION["cookies"][cookie["name"]] = cookie["value"]
        if cookie["name"] in ["a1", "webId", "gid", "web_session"]:
            print(f"[浏览器] • {cookie['name']}: {cookie['value'][:50]}...")
    
    print("[浏览器] 等待 2 秒...")
    sleep(2)
    
    # 保存浏览器会话，供后续使用
    BROWSER_SESSION["browser"] = browser
    BROWSER_SESSION["context"] = browser_context
    BROWSER_SESSION["page"] = context_page
    
    print("[浏览器] ✓ 浏览器会话保存成功")
    
    return BROWSER_SESSION["cookies"]


def sign(uri, data=None, a1="", web_session=""):
    """签名函数 - 使用持久化的浏览器会话"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"\n[签名] 第 {attempt + 1}/{max_retries} 次尝试...")
            
            # 获取或创建浏览器会话
            if not BROWSER_SESSION["page"]:
                get_browser_cookies_and_session()
            
            context_page = BROWSER_SESSION["page"]
            
            print(f"[签名] 执行签名: uri={uri}")
            encrypt_params = context_page.evaluate(
                "([url, data]) => window._webmsxyw(url, data)", 
                [uri, data]
            )
            
            print(f"[签名] ✓ 签名成功!")
            
            return {
                "x-s": encrypt_params["X-s"],
                "x-t": str(encrypt_params["X-t"])
            }
                
        except Exception as e:
            print(f"[签名] ✗ 异常: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            sleep(5)

    raise Exception("重试了这么多次还是无法签名成功")


if __name__ == '__main__':
    print("=" * 60)
    print("小红书爬虫 - 使用 XhsClient + 持久化浏览器")
    print("=" * 60)
    print(f"当前时间: {datetime.datetime.now()}\n")
    
    # 第一步：启动浏览器获取 Cookie
    print("[主程序] 启动浏览器获取 Cookie...\n")
    browser_cookies = get_browser_cookies_and_session()
    
    # 第二步：将 Cookie 转换为字符串
    cookie_string = "; ".join([f"{k}={v}" for k, v in browser_cookies.items()])
    print(f"\n[主程序] ✓ 获取到 {len(browser_cookies)} 个 Cookie")
    print("[主程序] ⚠️  浏览器已启动，如果出现验证码，请在浏览器中手动完成验证")
    print("[主程序] 💡 验证完成后，请按 Enter 键继续...\n")
    
    input(">>> ")
    
    # 第三步：初始化 XhsClient
    cookie_string = "; ".join([f"{k}={v}" for k, v in browser_cookies.items()])
    xhs_client = XhsClient(cookie=cookie_string, sign=sign)
    
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
    max_api_retries = 5
    api_success = False
    
    for retry_count in range(max_api_retries):
        try:
            print(f"\n[主程序] 第 {retry_count + 1}/{max_api_retries} 次尝试获取用户信息...")
            sef_info = xhs_client.get_user_info("360485984")
            
            print("\n" + "=" * 60)
            print("✓ 获取成功！用户信息如下：")
            print("=" * 60)
            print(json.dumps(sef_info, indent=4, ensure_ascii=False))
            
            api_success = True
            break
            
        except Exception as e:
            error_name = type(e).__name__
            error_msg = str(e)
            
            if "NeedVerifyError" in error_name or "验证码" in error_msg:
                print(f"\n⚠️  需要验证码")
                print(f"错误信息: {error_msg}")
                print(f"💡 请在浏览器中完成验证，完成后按 Enter 继续...\n")
                input(">>> ")
                sleep(3)  # 等待验证完成
                
            elif "IPBlockError" in error_name or "IP" in error_msg:
                print(f"\n❌ IP 被限制")
                print(f"错误信息: {error_msg}")
                break
                
            elif retry_count < max_api_retries - 1:
                print(f"\n❌ 错误: {error_name}: {error_msg}")
                print(f"等待 3 秒后重试...")
                sleep(3)
                
            else:
                print(f"\n❌ 最终失败: {error_name}: {error_msg}")
                import traceback
                traceback.print_exc()
    
    # 清理资源
    print("\n[清理] 正在关闭资源...")
    try:
        if BROWSER_SESSION["context"]:
            BROWSER_SESSION["context"].close()
            print("[清理] ✓ 浏览器上下文已关闭")
    except:
        pass
    
    try:
        if BROWSER_SESSION["browser"]:
            BROWSER_SESSION["browser"].close()
            print("[清理] ✓ 浏览器已关闭")
    except:
        pass
    
    try:
        if BROWSER_SESSION["playwright"]:
            BROWSER_SESSION["playwright"].stop()
            print("[清理] ✓ Playwright 已停止")
    except:
        pass
    
    print("[清理] 完成")
