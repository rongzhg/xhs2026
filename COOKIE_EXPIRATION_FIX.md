## API Code: -1 Error Diagnosis and Solution

### Problem Analysis

**Current Status:**
- All API calls return: `{'code': -1, 'success': False}`
- Affects: get_self_info(), get_user_info(), get_user_notes()
- Root Cause: **Cookie is expired or invalid**

### Why This Happens

The Xiaohongshu API returned code `-1` typically means:
1. ? Cookie has expired (most common)
2. ? Cookie format is incorrect
3. ? API version mismatch
4. ? Server-side authentication failure

### Solution: Refresh Cookie

**Step 1: Open Xiaohongshu in Your Browser**
1. Go to: https://www.xiaohongshu.com
2. Make sure you're logged in

**Step 2: Extract Fresh Cookie**
1. Open Developer Tools (Press F12)
2. Go to Application tab ¡ú Cookies
3. Select domain: xiaohongshu.com
4. Look for these key cookies:
   - `a1` - User session token
   - `web_session` - Session ID
   - `webId` - Web session identifier

**Step 3: Build Cookie String**
Copy ALL cookies and format as:
```
key1=value1; key2=value2; key3=value3; ...
```

**Step 4: Replace in Your Account**
1. Go to web interface: http://localhost:5000
2. Go to "Account Management" tab
3. Delete old account (if exists)
4. Add new account with fresh cookie

### Detailed Cookie Extraction Guide

**Using Firefox:**
1. Open DevTools (F12)
2. Storage ¡ú Cookies ¡ú xiaohongshu.com
3. Select all, right-click, copy
4. Paste into text editor

**Using Chrome:**
1. Open DevTools (F12)
2. Application ¡ú Cookies ¡ú xiaohongshu.com
3. Right-click any cookie ¡ú Edit
4. Copy all cookies manually

### Complete Cookie List

These are the essential cookies you need:
```
- gid           (Device ID)
- xsecappid     (App ID)
- abRequestId   (Request ID)
- a1            (User token - CRITICAL)
- webId         (Web ID)
- web_session   (Session - CRITICAL)
- webBuild      (Build version)
- acw_tc        (Challenge token)
- loadts        (Load timestamp)
- websectiga    (Security signature)
- sec_poison_id (Poison ID)
- unread        (Unread messages)
```

### Testing New Cookie

After adding new cookie, run test:

```bash
python test_direct_api.py
```

**Expected Output:**
```
[2] Testing get_self_info()...
  SUCCESS: {'user_info': {'user_id': '227837619', 'nick_name': 'YourName', ...}}

[3] Testing get_user_info('360485984')...
  SUCCESS: {'user_info': {'user_id': '360485984', 'nick_name': 'TargetUser', ...}}

[4] Testing get_user_notes('360485984')...
  SUCCESS: Got 30 notes
```

### If Still Failing

**Check these:**
1. Ensure you're logged into Xiaohongshu website
2. Verify cookie contains semicolon separators
3. Check no special characters are missing
4. Try again after a few minutes (server timeout)
5. Check if account has any restrictions

### Cookie Expiration

Xiaohongshu cookies typically expire after:
- 7-14 days of inactivity
- 30 days from creation
- When logging out
- When accessing from new IP

### Automatic Testing

Run this to validate cookie status:

```bash
python test_direct_api.py
```

This will test all three critical API endpoints.

### Next Steps

1. ? Extract fresh cookie from browser
2. ? Update account in web interface
3. ? Run test_direct_api.py to verify
4. ? Run test_crawl_debug.py to test full crawling
5. ? Use web interface to crawl content

---

**Key Points:**
- Cookie must be fresh (extracted while logged in)
- Code -1 always means authentication failed
- Other errors (471, 461) mean different issues
- Once cookie works, crawling should succeed immediately

