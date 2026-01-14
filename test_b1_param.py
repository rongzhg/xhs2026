#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnose - Testing with b1 parameter
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import json
from xhs import XhsClient
from xhs.help import sign as xhs_sign

COOKIE = "gid=yj8D4i2WfD9Syj8D4i2WY67FYdi0xJhS28M8S6Ddkj068Eq8DfYKhI888qyJ2yW8fiiKWWfy; xsecappid=xhs-pc-web; abRequestId=205c5fd149e894cf15b1440c6806b7fd; a1=1984ec28a9c2vt2dib5h8w7b1su8edwmx8rhe85ld30000426322; webId=7a5902b8d6e0b9f5c816ccdc5bd3587e; web_session=0400698d38cac5108a94b991b33a4b86e67f3e; webBuild=5.6.1; acw_tc=0a4ad8b317675906702185103ed48ac45705e5e306ce9ffd905b41518dfdd2; loadts=1767590816080; websectiga=16f444b9ff5e3d7e258b5f7674489196303a0b160e16647c6c2b4dcb609f4134; sec_poison_id=61e4a4be-75ef-4cb8-8a9b-af7e67f04924; unread={%22ub%22:%226936400b000000001e02908d%22%2C%22ue%22:%22695081f200000000210310f8%22%2C%22uc%22:33}"

print("\n" + "=" * 100)
print("TESTING - With vs Without b1 Parameter")
print("=" * 100)

a1 = "1984ec28a9c2vt2dib5h8w7b1su8edwmx8rhe85ld30000426322"
b1 = ""  # Empty b1 - what we're currently using

uri = "/api/sns/web/v1/user/selfinfo"

# Parse cookies
cookie_dict = {}
for item in COOKIE.split('; '):
    key, value = item.split('=', 1)
    cookie_dict[key] = value

print(f"\n[1] Current approach (b1 empty):")
print(f"    a1: {a1[:20]}...")
print(f"    b1: '{b1}'")

signs_without_b1 = xhs_sign(uri, data=None, a1=a1, b1=b1)
print(f"    x-s-common (no b1): {signs_without_b1['x-s-common'][:50]}...")

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "x-s": signs_without_b1.get('x-s', ''),
    "x-t": signs_without_b1.get('x-t', ''),
    "x-s-common": signs_without_b1.get('x-s-common', ''),
}

response = requests.get(
    f"https://edith.xiaohongshu.com{uri}",
    headers=headers,
    cookies=cookie_dict,
    timeout=10
)
print(f"    Result: {response.status_code} - {response.json()}")

# Now try with a sample b1
print(f"\n[2] With sample b1 value:")
b1_test = "test123"
print(f"    b1: '{b1_test}'")

signs_with_b1 = xhs_sign(uri, data=None, a1=a1, b1=b1_test)
print(f"    x-s-common (with b1): {signs_with_b1['x-s-common'][:50]}...")

headers["x-s"] = signs_with_b1.get('x-s', '')
headers["x-t"] = signs_with_b1.get('x-t', '')
headers["x-s-common"] = signs_with_b1.get('x-s-common', '')

response = requests.get(
    f"https://edith.xiaohongshu.com{uri}",
    headers=headers,
    cookies=cookie_dict,
    timeout=10
)
print(f"    Result: {response.status_code} - {response.json()}")

print(f"\n[3] Checking what headers browser sends:")
print(f"    The issue might be that we don't have the browser's b1 value")
print(f"    b1 should come from: localStorage.getItem('b1')")
print(f"    Current b1: EMPTY (this might be the issue)")

print("\n" + "=" * 100)
print("POSSIBLE SOLUTION:")
print("=" * 100)
print("""
The problem is likely that:
1. You need the 'b1' value from your browser's localStorage
2. The sign function creates 'x-s-common' header which includes the b1
3. Without the correct b1, the API rejects the request with 406

To fix this:
1. Open browser DevTools (F12)
2. Go to Application > Local Storage > https://www.xiaohongshu.com
3. Find the key 'b1' and copy its value
4. Add it to the wrapper function: sign_wrapper(..., b1="YOUR_B1_VALUE")
""")
print("=" * 100 + "\n")
