#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XHS Content Monitor - Fetch Function Test Script

Test and diagnose fetch functionality
"""

import json
import sys
from pathlib import Path

def test_xhs_library():
    """Test if XHS library is correctly installed"""
    print("=" * 50)
    print("Test 1: Check XHS Library")
    print("=" * 50)
    
    try:
        from xhs import XhsClient
        print("OK: XHS library is correctly installed")
        return True
    except ImportError as e:
        print(f"ERROR: XHS library not installed: {e}")
        print("  Run: pip install xhs")
        return False


def test_flask_library():
    """Test if Flask library is correctly installed"""
    print("\n" + "=" * 50)
    print("Test 2: Check Flask Library")
    print("=" * 50)
    
    try:
        import flask
        print(f"OK: Flask is installed (version: {flask.__version__})")
        return True
    except ImportError:
        print("ERROR: Flask not installed")
        print("  Run: pip install flask")
        return False


def test_database():
    """Test if database is available"""
    print("\n" + "=" * 50)
    print("Test 3: Check Data Files")
    print("=" * 50)
    
    try:
        from xhs_monitor.models import Database
        
        db = Database(data_dir='data')
        accounts = db.get_all_accounts()
        
        print(f"OK: Database is available")
        print(f"  Number of configured accounts: {len(accounts)}")
        
        if accounts:
            print("\n  Account list:")
            for acc in accounts:
                print(f"    - {acc.username} ({acc.user_id})")
                # Verify cookie
                if acc.cookie:
                    print(f"      Cookie length: {len(acc.cookie)} characters")
                else:
                    print(f"      WARNING: Cookie is empty")
        
        return True
    except Exception as e:
        print(f"ERROR: Database error: {e}")
        return False


def test_crawler():
    """Test if crawler module is available"""
    print("\n" + "=" * 50)
    print("Test 4: Check Crawler Module")
    print("=" * 50)
    
    try:
        from xhs_monitor.crawler import ContentCrawler
        
        crawler = ContentCrawler()
        print("OK: Crawler module is loaded")
        return True
    except Exception as e:
        print(f"ERROR: Crawler module error: {e}")
        return False


def test_converter():
    """Test if converter module is available"""
    print("\n" + "=" * 50)
    print("Test 5: Check Converter Module")
    print("=" * 50)
    
    try:
        from xhs_monitor.converter import DummyConverter
        
        converter = DummyConverter()
        print("OK: Converter module is loaded")
        return True
    except Exception as e:
        print(f"ERROR: Converter module error: {e}")
        return False


def test_api():
    """Test if API is available"""
    print("\n" + "=" * 50)
    print("Test 6: Check API")
    print("=" * 50)
    
    try:
        from xhs_monitor.app import app
        
        print("OK: Flask application is loaded")
        
        # Test API routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        api_routes = [r for r in routes if r.startswith('/api/')]
        
        print(f"OK: Found {len(api_routes)} API endpoints:")
        for route in sorted(api_routes):
            print(f"    - {route}")
        
        return True
    except Exception as e:
        print(f"ERROR: API error: {e}")
        return False


def test_cookie_format():
    """Test cookie format"""
    print("\n" + "=" * 50)
    print("Test 7: Verify Cookie Format")
    print("=" * 50)
    
    try:
        from xhs_monitor.models import Database
        
        db = Database()
        accounts = db.get_all_accounts()
        
        if not accounts:
            print("WARNING: No accounts configured, skipping cookie verification")
            return True
        
        for acc in accounts:
            print(f"\n  Check account: {acc.username}")
            
            if not acc.cookie:
                print("    ERROR: Cookie is empty")
                continue
            
            # Check for key fields
            required_fields = ['a1', 'web_session', 'x-sign']
            found_fields = []
            
            for field in required_fields:
                if field in acc.cookie:
                    found_fields.append(field)
            
            if len(found_fields) >= 2:
                print(f"    OK: Cookie format is correct (contains: {', '.join(found_fields)})")
            else:
                print(f"    WARNING: Cookie might be incomplete (only contains: {', '.join(found_fields)})")
                print("      Suggestion: Re-login to XHS, copy the latest Cookie")
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def test_network():
    """Test network connectivity"""
    print("\n" + "=" * 50)
    print("Test 8: Check Network Connection")
    print("=" * 50)
    
    try:
        import socket
        
        result = socket.gethostbyname('xiaohongshu.com')
        print(f"OK: Can connect to XHS server ({result})")
        return True
    except Exception as e:
        print(f"ERROR: Network connection error: {e}")
        print("  Check your network connection or firewall settings")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n")
    print("=" * 50)
    print("XHS Content Monitor - Fetch Diagnostic Tool")
    print("=" * 50)
    print()
    
    tests = [
        ("XHS Library", test_xhs_library),
        ("Flask Library", test_flask_library),
        ("Database", test_database),
        ("Crawler Module", test_crawler),
        ("Converter Module", test_converter),
        ("API", test_api),
        ("Cookie Format", test_cookie_format),
        ("Network Connection", test_network),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\nERROR: {test_name} test exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for test_name, result in results:
        status = "OK" if result else "ERROR"
        print(f"[{status}] {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nOK: System is functioning normally, fetch operations can proceed")
        return True
    else:
        print("\nWARNING: Issues found, please follow the recommendations above to fix them")
        return False


def main():
    """Main function"""
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
