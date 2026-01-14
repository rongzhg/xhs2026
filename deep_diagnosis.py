#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deep Diagnosis Script
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xhs import XhsClient
from xhs.help import sign as xhs_sign
import json

COOKIE = "gid=yj8D4i2WfD9Syj8D4i2WY67FYdi0xJhS28M8S6Ddkj068Eq8DfYKhI888qyJ2yW8fiiKWWfy; xsecappid=xhs-pc-web; abRequestId=205c5fd149e894cf15b1440c6806b7fd; a1=1984ec28a9c2vt2dib5h8w7b1su8edwmx8rhe85ld30000426322; webId=7a5902b8d6e0b9f5c816ccdc5bd3587e; web_session=0400698d38cac5108a94b991b33a4b86e67f3e; webBuild=5.6.1; acw_tc=0a4ad8b317675906702185103ed48ac45705e5e306ce9ffd905b41518dfdd2; loadts=1767590816080; websectiga=16f444b9ff5e3d7e258b5f7674489196303a0b160e16647c6c2b4dcb609f4134; sec_poison_id=61e4a4be-75ef-4cb8-8a9b-af7e67f04924; unread={%22ub%22:%226936400b000000001e02908d%22%2C%22ue%22:%22695081f200000000210310f8%22%2C%22uc%22:33}"

def test_sign():
    """Test sign function"""
    print("=" * 80)
    print("[TEST 1] Test Sign Function")
    print("=" * 80)
    
    uri = "/api/sns/web/v1/user/otherinfo?target_user_id=360485984"
    result = xhs_sign(uri, data=None, a1="1984ec28a9c2vt2dib5h8w7b1su8edwmx8rhe85ld30000426322")
    
    print(f"URI: {uri}")
    print(f"Sign result type: {type(result)}")
    print(f"Sign result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
    print(f"Sign result: {json.dumps(result, indent=2)}")
    print("OK - Sign function works\n")
    
    return result

def test_client_init():
    """Test XhsClient initialization"""
    print("=" * 80)
    print("[TEST 2] Initialize XhsClient")
    print("=" * 80)
    
    def sign_wrapper(uri, data=None, ctime=None, a1="", b1="", **kwargs):
        return xhs_sign(uri, data=data, ctime=ctime, a1=a1, b1=b1)
    
    client = XhsClient(cookie=COOKIE, sign=sign_wrapper)
    print(f"Cookie length: {len(COOKIE)}")
    print(f"Cookie dict keys: {list(client.cookie_dict.keys())}")
    print(f"a1: {client.cookie_dict.get('a1', 'MISSING')}")
    print(f"web_session: {client.cookie_dict.get('web_session', 'MISSING')}")
    print(f"webId: {client.cookie_dict.get('webId', 'MISSING')}")
    print("OK - Client initialized\n")
    
    return client

def test_api_call(client):
    """Test API call"""
    print("=" * 80)
    print("[TEST 3] Test get_user_info API")
    print("=" * 80)
    
    try:
        result = client.get_user_info("360485984")
        print(f"SUCCESS - API call succeeded")
        print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else type(result)}")
        print(f"Result sample: {json.dumps(result, indent=2, ensure_ascii=False)[:300]}...\n")
        return True
    except Exception as e:
        print(f"FAILED - API call failed")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}\n")
        return False

def test_self_info(client):
    """Test self info"""
    print("=" * 80)
    print("[TEST 4] Test get_self_info API")
    print("=" * 80)
    
    try:
        result = client.get_self_info()
        print(f"SUCCESS - Self info retrieved")
        print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else type(result)}")
        print(f"Result sample: {json.dumps(result, indent=2, ensure_ascii=False)[:300]}...\n")
        return True
    except Exception as e:
        print(f"FAILED - Self info failed")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}\n")
        return False

if __name__ == "__main__":
    try:
        print("\n" + "=" * 80)
        print("XHS DEEP DIAGNOSIS")
        print("=" * 80 + "\n")
        
        test_sign()
        client = test_client_init()
        test_self = test_self_info(client)
        test_user = test_api_call(client)
        
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Self info: {'PASS' if test_self else 'FAIL'}")
        print(f"User info: {'PASS' if test_user else 'FAIL'}")
        print()
        
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
