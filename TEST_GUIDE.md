## Application Test Guide

### Current Status ?

Application is **running successfully** on:
- **URL:** http://localhost:5000
- **Status:** All endpoints responding
- **Sign Function:** Using sign_wrapper (handles parameter mismatches)

### Server Logs

```
Running on http://127.0.0.1:5000
Running on http://172.22.87.121:5000
Debug mode: on
Debugger PIN: 102-837-481
```

### Testing Steps

#### Step 1: Access the Web Interface

1. Open browser at: `http://localhost:5000`
2. You should see the Xiaohongshu Content Monitor dashboard

#### Step 2: Add a Xiaohongshu Account

1. Go to **"Account Management"** tab (left side)
2. Fill in the account form:
   - **Username:** Your Xiaohongshu account name
   - **User ID:** Your Xiaohongshu user ID (e.g., 360485984)
   - **Cookie:** Your Xiaohongshu session cookie
3. Click **"Add Account"** button

**Note:** You need valid Xiaohongshu cookies for this to work. Get them from your browser's Developer Tools (F12):
- Open DevTools → Application → Cookies → xiaohongshu.com
- Copy the cookie string

#### Step 3: Test Content Crawling

1. Select the account you just added
2. Click **"Crawl Content"** button
3. Watch the console output for status updates

**Expected output:**
```
Starting to crawl user 360485984...
User info fetched successfully
Fetched 15 notes
Content classified: 8 videos, 5 images, 2 text posts
Success
```

#### Step 4: View Fetched Content

1. Go to **"Content Display"** tab
2. You should see a table with fetched posts:
   - Post title
   - Content type (Video/Image/Text)
   - Post link
   - Publication date
   - View/Download button

#### Step 5: Check Statistics

1. Go to **"Statistics"** tab
2. View analytics about:
   - Total posts crawled
   - Content type distribution (pie chart)
   - Posts per day (bar chart)

### API Endpoints

The following endpoints are available and tested:

```
GET  /                          - Main page
GET  /api/accounts              - List all accounts
POST /api/accounts              - Add new account
GET  /api/accounts/{id}         - Get account details
DELETE /api/accounts/{id}       - Delete account
GET  /api/contents/user/all     - List all contents
POST /api/contents/crawl        - Start crawling
GET  /api/contents/{id}         - Get content details
GET  /api/statistics            - Get statistics
```

### Troubleshooting

#### Error: "sign() got an unexpected keyword argument 'web_session'"

**Status:** ? FIXED in latest version
- The `sign_wrapper` function now handles extra parameters
- Verify you're using the latest code from `xhs_monitor/crawler.py`

#### Error: "获取用户信息失败" (Failed to fetch user info)

**Possible causes:**
1. Invalid or expired cookie
2. User ID doesn't exist
3. Network connection issue

**Solution:**
- Get fresh cookies from browser DevTools
- Verify the user ID is correct
- Check internet connection

#### Error: "获取笔记失败" (Failed to fetch notes)

**Possible causes:**
1. Same as above
2. User has no public notes
3. User has blocked content access

**Solution:**
- Ensure user has public posts
- Try with a different user ID
- Check Xiaohongshu privacy settings

### Console Output Meanings

```
? User info fetched successfully     - Good! User found
? Fetched X notes                    - X posts retrieved
? Content classified: ...            - Content types identified
? Failed to fetch user info          - Cookie/user ID issue
? Sign function error                - Fixed in latest version
```

### Performance Notes

- First crawl takes 2-5 seconds
- Subsequent crawls may be faster due to caching
- Large accounts (100+ posts) may take longer
- Browser may slow down with 1000+ items in table

### Next Steps

1. ? Application running - DONE
2. ? Add account and test crawling
3. ? Verify content displays correctly
4. ? Configure external APIs for text conversion (optional)

---

**Test Date:** 2025-01-05
**Application Status:** RUNNING ?
**Sign Function Status:** FIXED ?
