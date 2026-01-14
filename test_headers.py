#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Browser Request Analysis - Compare with XHS requirements
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import json
from xhs import XhsClient
from xhs.help import sign as xhs_sign

COOKIE = "gid=yj8D4i2WfD9Syj8D4i2WY67FYdi0xJhS28M8S6Ddkj068Eq8DfYKhI888qyJ2yW8fiiKWWfy; xsecappid=xhs-pc-web; abRequestId=205c5fd149e894cf15b1440c6806b7fd; a1=1984ec28a9c2vt2dib5h8w7b1su8edwmx8rhe85ld30000426322; webId=7a5902b8d6e0b9f5c816ccdc5bd3587e; web_session=0400698d38cac5108a94b991b33a4b86e67f3e; webBuild=5.6.1; acw_tc=0a4ad8b317675906702185103ed48ac45705e5e306ce9ffd905b41518dfdd2; loadts=1767590816080; websectiga=16f444b9ff5e3d7e258b5f7674489196303a0b160e16647c6c2b4dcb609f4134; sec_poison_id=61e4a4be-75ef-4cb8-8a9b-af7e67f04924; unread={%22ub%22:%226936400b000000001e02908d%22%2C%22ue%22:%22695081f200000000210310f8%22%2C%22uc%22:33}"

def sign_wrapper(uri, data=None, ctime=None, a1="", b1="", **kwargs):
    """Wrapper ignores extra web_session param"""
    return xhs_sign(uri, data=data, ctime=ctime, a1=a1, b1=b1)

client = XhsClient(cookie=COOKIE, sign=sign_wrapper)
a1 = client.cookie_dict.get('a1', '')

uri = "/api/sns/web/v1/user/selfinfo"
signs = sign_wrapper(uri, data=None, a1=a1)

# Test 1: Minimal headers (current approach)
print("\n" + "=" * 100)
print("TEST 1 - Minimal Headers (Current)")
print("=" * 100)

minimal_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "x-s": signs.get('x-s', ''),
    "x-t": signs.get('x-t', ''),
    "x-s-common": signs.get('x-s-common', ''),
}

response = requests.get(
    f"https://edith.xiaohongshu.com{uri}",
    headers=minimal_headers,
    cookies=client.cookie_dict,
    timeout=10
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 2: Add common browser headers
print("\n" + "=" * 100)
print("TEST 2 - With Common Browser Headers")
print("=" * 100)

browser_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "x-s": signs.get('x-s', ''),
    "x-t": signs.get('x-t', ''),
    "x-s-common": signs.get('x-s-common', ''),
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "referer": "https://www.xiaohongshu.com/",
    "origin": "https://www.xiaohongshu.com",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
}

response = requests.get(
    f"https://edith.xiaohongshu.com{uri}",
    headers=browser_headers,
    cookies=client.cookie_dict,
    timeout=10
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 3: With x-sign header
print("\n" + "=" * 100)
print("TEST 3 - With x-sign Header")
print("=" * 100)

sign_headers = browser_headers.copy()
sign_headers["x-sign"] = signs.get('x-s', '')  # Try x-sign as alternative

response = requests.get(
    f"https://edith.xiaohongshu.com{uri}",
    headers=sign_headers,
    cookies=client.cookie_dict,
    timeout=10
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 4: Check what server expects - make request from browser directly
print("\n" + "=" * 100)
print("TEST 4 - Request WITHOUT signature headers (to see if auth works)")
print("=" * 100)

no_sig_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
}

response = requests.get(
    f"https://www.xiaohongshu.com/api/sns/web/v1/user/selfinfo",  # Try main domain
    headers=no_sig_headers,
    cookies=client.cookie_dict,
    timeout=10
)
print(f"Status: {response.status_code}")
try:
    print(f"Response: {response.json()}")
except:
    print(f"Response text: {response.text[:200]}")

print("\n" + "=" * 100)
