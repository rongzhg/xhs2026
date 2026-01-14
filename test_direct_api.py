#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Direct API test without crawler
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xhs import XhsClient
from xhs.help import sign as xhs_sign

def sign_wrapper(uri, data=None, ctime=None, a1="", b1="", **kwargs):
    """Wrapper to ignore extra parameters"""
    return xhs_sign(uri, data=data, ctime=ctime, a1=a1, b1=b1)

def main():
    print("\n" + "="*80)
    print("Direct XhsClient API Test")
    print("="*80 + "\n")
    
    my_cookie = "gid=yj8D4i2WfD9Syj8D4i2WY67FYdi0xJhS28M8S6Ddkj068Eq8DfYKhI888qyJ2yW8fiiKWWfy; xsecappid=xhs-pc-web; abRequestId=205c5fd149e894cf15b1440c6806b7fd; a1=1984ec28a9c2vt2dib5h8w7b1su8edwmx8rhe85ld30000426322; webId=7a5902b8d6e0b9f5c816ccdc5bd3587e; web_session=0400698d38cac5108a94b991b33a4b86e67f3e; webBuild=5.6.1; acw_tc=0a4ad8b317675906702185103ed48ac45705e5e306ce9ffd905b41518dfdd2; loadts=1767590816080; websectiga=16f444b9ff5e3d7e258b5f7674489196303a0b160e16647c6c2b4dcb609f4134; sec_poison_id=61e4a4be-75ef-4cb8-8a9b-af7e67f04924; unread={%22ub%22:%226936400b000000001e02908d%22%2C%22ue%22:%22695081f200000000210310f8%22%2C%22uc%22:33}"
    target_user_id = "360485984"
    
    print("[1] Creating XhsClient with sign_wrapper...")
    client = XhsClient(cookie=my_cookie, sign=sign_wrapper)
    print("OK - XhsClient created\n")
    
    # Test 1: get_self_info
    print("[2] Testing get_self_info()...")
    print(f"  - URI: /api/sns/web/v1/user/selfinfo")
    try:
        result = client.get_self_info()
        print(f"  SUCCESS: {result}")
    except Exception as e:
        print(f"  FAILED: {e}\n")
    
    # Test 2: get_user_info
    print(f"\n[3] Testing get_user_info('{target_user_id}')...")
    print(f"  - URI: /api/sns/web/v1/user/otherinfo")
    print(f"  - Params: target_user_id={target_user_id}")
    try:
        result = client.get_user_info(target_user_id)
        print(f"  SUCCESS: {result}")
    except Exception as e:
        print(f"  FAILED: {e}\n")
    
    # Test 3: get_user_notes
    print(f"\n[4] Testing get_user_notes('{target_user_id}')...")
    print(f"  - URI: /api/sns/web/v1/user_posted")
    print(f"  - Params: num=30, cursor='', user_id={target_user_id}, image_scenes=FD_WM_WEBP")
    try:
        result = client.get_user_notes(target_user_id, cursor="")
        print(f"  SUCCESS: Got {len(result.get('notes', []))} notes")
        print(f"  - Full response keys: {list(result.keys())}")
    except Exception as e:
        print(f"  FAILED: {e}\n")
    
    print("\n" + "="*80)
    print("Diagnosis Summary:")
    print("  If all tests fail with code:-1, cookie might be expired")
    print("  Try refreshing the cookie from your browser")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
