#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
XHS Crawl Diagnostic Tool
Track each step's calls and errors
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xhs_monitor.models import Account, Database
from xhs_monitor.crawler import ContentCrawler, sign_wrapper

def test_crawl():
    print("\n" + "="*80)
    print("Xiaohongshu Content Crawl Diagnostic Tool")
    print("="*80 + "\n")
    
    # Your account info
    my_cookie = "gid=yj8D4i2WfD9Syj8D4i2WY67FYdi0xJhS28M8S6Ddkj068Eq8DfYKhI888qyJ2yW8fiiKWWfy; xsecappid=xhs-pc-web; abRequestId=205c5fd149e894cf15b1440c6806b7fd; a1=1984ec28a9c2vt2dib5h8w7b1su8edwmx8rhe85ld30000426322; webId=7a5902b8d6e0b9f5c816ccdc5bd3587e; web_session=0400698d38cac5108a94b991b33a4b86e67f3e; webBuild=5.6.1; acw_tc=0a4ad8b317675906702185103ed48ac45705e5e306ce9ffd905b41518dfdd2; loadts=1767590816080; websectiga=16f444b9ff5e3d7e258b5f7674489196303a0b160e16647c6c2b4dcb609f4134; sec_poison_id=61e4a4be-75ef-4cb8-8a9b-af7e67f04924; unread={%22ub%22:%226936400b000000001e02908d%22%2C%22ue%22:%22695081f200000000210310f8%22%2C%22uc%22:33}"
    target_user_id = "360485984"
    
    # Create account object
    account = Account(
        account_id="test_account",
        username="227837619",
        user_id="227837619",
        cookie=my_cookie
    )
    
    print(f"[Test Info]")
    print(f"  - Crawler Account: {account.username} ({account.user_id})")
    print(f"  - Target User: {target_user_id}")
    print(f"  - Cookie Length: {len(account.cookie)}")
    print(f"  - Sign Function: {sign_wrapper.__name__}")
    print()
    
    # Create crawler
    print(f"[Initialize Crawler]")
    crawler = ContentCrawler(sign_func=sign_wrapper)
    print(f"  OK - Crawler initialized")
    print()
    
    # Start crawling
    print(f"[Start Crawl Process]")
    print()
    
    contents = crawler.fetch_user_content(account, target_user_id)
    
    print()
    print("="*80)
    print(f"[Crawl Result]")
    print(f"  - Successfully fetched: {len(contents)} notes")
    
    if contents:
        print(f"\n[First 5 Notes]")
        for idx, content in enumerate(contents[:5], 1):
            print(f"  {idx}. {content.title[:50]}...")
            print(f"     Type: {content.content_type}")
            print(f"     Link: {content.link}")
            print()
    
    print("="*80 + "\n")
    
    return len(contents) > 0

if __name__ == "__main__":
    success = test_crawl()
    sys.exit(0 if success else 1)
