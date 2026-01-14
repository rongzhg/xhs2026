#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Advanced Diagnosis Script - Check full request/response details
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

print("\n" + "=" * 100)
print("ADVANCED DIAGNOSIS - Checking Raw API Request/Response")
print("=" * 100)

# Initialize client
client = XhsClient(cookie=COOKIE, sign=sign_wrapper)
a1 = client.cookie_dict.get('a1', '')

uri = "/api/sns/web/v1/user/selfinfo"
print(f"\n[1] Testing URI: {uri}")
print(f"    A1 value: {a1[:20]}...")

# Get sign headers
signs = sign_wrapper(uri, data=None, a1=a1)
print(f"\n[2] Sign headers generated:")
print(f"    x-s: {signs.get('x-s', 'MISSING')[:50]}...")
print(f"    x-t: {signs.get('x-t', 'MISSING')}")
print(f"    x-s-common: {signs.get('x-s-common', 'MISSING')[:50]}...")

# Build full request
full_url = f"https://edith.xiaohongshu.com{uri}"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "x-s": signs.get('x-s', ''),
    "x-t": signs.get('x-t', ''),
    "x-s-common": signs.get('x-s-common', ''),
}

print(f"\n[3] Full request details:")
print(f"    URL: {full_url}")
print(f"    Method: GET")
print(f"    Headers: {json.dumps({k: v[:50] if len(str(v)) > 50 else v for k, v in headers.items()}, indent=8)}")
print(f"    Cookies (keys): {list(client.cookie_dict.keys())}")

# Make raw request
print(f"\n[4] Sending raw request...")
try:
    response = requests.get(
        full_url,
        headers=headers,
        cookies=client.cookie_dict,
        timeout=10
    )
    print(f"    Status code: {response.status_code}")
    print(f"    Response headers: {dict(response.headers)}")
    
    try:
        resp_json = response.json()
        print(f"    Response body: {json.dumps(resp_json, indent=4)}")
    except:
        print(f"    Response text: {response.text[:200]}")
        
except Exception as e:
    print(f"    Error: {type(e).__name__}: {str(e)}")

# Try using client method
print(f"\n[5] Using XhsClient method...")
try:
    result = client.get_self_info()
    print(f"    Result: {result}")
except Exception as e:
    print(f"    Error: {type(e).__name__}: {str(e)}")

# Check if cookie might be expired - try without sign verification
print(f"\n[6] Testing cookie validity in other ways...")
print(f"    Cookie contains web_session: {'web_session' in client.cookie_dict}")
print(f"    Cookie contains a1: {'a1' in client.cookie_dict}")
print(f"    Cookie contains webId: {'webId' in client.cookie_dict}")

print("\n" + "=" * 100)
print("DIAGNOSIS COMPLETE")
print("=" * 100 + "\n")
