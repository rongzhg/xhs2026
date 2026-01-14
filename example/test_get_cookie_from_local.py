import datetime
import json
import requests
from time import sleep
from playwright.sync_api import sync_playwright


def main():
    stealth_js_path = r"C:\Users\Administrator\Documents\xhs2026\stealth.min.js"
    
    with sync_playwright() as playwright:
        chromium = playwright.chromium
        
        print("[Browser] Starting browser...")
        browser = chromium.launch(headless=False)
        sleep(40)
        
        browser_context = browser.new_context()
        browser_context.add_init_script(path=stealth_js_path)
        context_page = browser_context.new_page()
        
        print("[Browser] Visiting Xiaohongshu...")
        context_page.goto("https://www.xiaohongshu.com")
        sleep(8)
        
        cookies = browser_context.cookies()
        cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        
        print(f"[Browser] Got {len(cookies)} cookies")
        
        uri = "/api/sns/web/v1/user/otherinfo?target_user_id=360485984"
        encrypt_params = context_page.evaluate(
            "([url, data]) => window._webmsxyw(url, data)", 
            [uri, None]
        )
        
        print("[Browser] Signature success")
        
        browser_context.close()
        browser.close()
        
        headers = {
            "user-agent": "Mozilla/5.0",
            "cookie": cookie_string,
            "x-s": encrypt_params["X-s"],
            "x-t": str(encrypt_params["X-t"]),
        }
        
        url = f"https://edith.xiaohongshu.com{uri}"
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        print("\n" + "=" * 60)
        print(json.dumps(data, indent=4, ensure_ascii=False))
        print("=" * 60)


if __name__ == '__main__':
    print(datetime.datetime.now())
    main()
