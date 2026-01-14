#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify sign function integration
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("\n" + "=" * 70)
    print("Verifying XHS Sign Function Integration")
    print("=" * 70 + "\n")
    
    # 1. Verify xhs.help.sign exists
    print("1. Checking xhs.help.sign function...")
    try:
        from xhs.help import sign
        print(f"   OK - Found xhs.help.sign function: {sign}")
    except ImportError as e:
        print(f"   ERROR - Cannot import xhs.help.sign: {e}")
        return False
    
    # 2. Verify crawler module uses real sign
    print("\n2. Checking sign wrapper in crawler.py...")
    try:
        from xhs_monitor.crawler import ContentCrawler, sign_wrapper
        crawler = ContentCrawler()
        if callable(crawler.sign_func):
            print(f"   OK - crawler.sign_func is callable: {crawler.sign_func.__name__}")
        else:
            print(f"   ERROR - crawler.sign_func is not callable: {crawler.sign_func}")
            return False
        
        # Test the wrapper function
        result = sign_wrapper(
            uri="/test",
            data={"test": "data"},
            a1="test_a1",
            web_session="test_web_session"  # This should be ignored
        )
        
        if result and "x-s" in result:
            print(f"   OK - sign_wrapper handles extra parameters correctly")
        else:
            print(f"   ERROR - sign_wrapper failed: {result}")
            return False
    except Exception as e:
        print(f"   ERROR - crawler initialization failed: {e}")
        return False
    
    # 3. Verify sign function works
    print("\n3. Testing sign function...")
    try:
        result = sign(
            uri="/homefeed.feed",
            data={"cursor": "", "num": 30},
            a1="test_a1_value"
        )
        
        if result and isinstance(result, dict):
            keys = list(result.keys())
            print(f"   OK - sign function returns result with keys: {keys}")
            for key, value in result.items():
                if isinstance(value, str):
                    display_value = (value[:40] + "...") if len(value) > 40 else value
                    print(f"      - {key}: {display_value}")
                else:
                    print(f"      - {key}: {value}")
        else:
            print(f"   ERROR - sign function returned invalid result: {result}")
            return False
    except Exception as e:
        print(f"   ERROR - sign function execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 4. Verify app module
    print("\n4. Checking crawler initialization in app.py...")
    try:
        from xhs_monitor.app import crawler as app_crawler, sign_wrapper
        print(f"   OK - app crawler initialized: {app_crawler}")
        if callable(app_crawler.sign_func):
            print(f"   OK - app crawler sign_func is callable: {app_crawler.sign_func.__name__}")
            
            # Test with XhsClient-style parameters
            result = app_crawler.sign_func(
                uri="/test",
                data={"test": "data"},
                a1="test_a1",
                web_session="extra_param"  # Extra param that XhsClient might pass
            )
            if result and "x-s" in result:
                print(f"   OK - sign_func handles XhsClient parameters correctly")
            else:
                print(f"   ERROR - sign_func failed: {result}")
                return False
        else:
            print(f"   ERROR - app crawler sign_func is not callable: {app_crawler.sign_func}")
            return False
    except Exception as e:
        print(f"   ERROR - app crawler initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 70)
    print("SUCCESS - All integration checks passed!")
    print("=" * 70 + "\n")
    print("Next steps:")
    print("1. Start the application: python run.py")
    print("2. Open browser and visit: http://localhost:5000")
    print("3. Add your Xiaohongshu account in 'Account Management'")
    print("4. Click 'Crawl Content' to test the functionality")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
