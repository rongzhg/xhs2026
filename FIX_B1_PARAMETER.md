# ? 完整修复指南 - 解决 API code: -1 和 406 错误

## 问题诊断

### 错误现象
- **HTTP 状态码**: 406
- **API 响应**: `{"code": -1, "success": False}`
- **原因**: 缺少浏览器 `localStorage` 中的 `b1` 参数

### 为什么会这样
小红书 API 要求客户端发送完整的身份认证签名，包括：
1. `a1` - Cookie 中的身份令牌 ? **已有**
2. `b1` - 浏览器 LocalStorage 中的值 ? **缺失**
3. 签名生成需要这两个值来创建有效的 `x-s-common` 请求头

## 解决方案 - 5 个步骤

### 第 1 步：从浏览器获取 b1 值

**在浏览器中执行**：

1. 打开浏览器的开发者工具 (按 **F12**)
2. 点击 **Application** 标签
3. 在左侧菜单选择 **Local Storage**
4. 从列表中选择 **https://www.xiaohongshu.com**
5. 在列表中查找 **b1** 键
6. 复制其值（长字符串，例如 `xxxx_yyyy_zzzz` 的格式）

### 第 2 步：更新爬虫代码

编辑文件: `xhs_monitor/crawler.py`

在 `sign_wrapper` 函数中添加 `b1` 参数：

```python
def sign_wrapper(uri, data=None, ctime=None, a1="", b1="", web_session="", **kwargs):
    """
    包装 sign 函数以处理 XhsClient 传递的额外参数
    """
    # 在这里添加从浏览器复制的 b1 值
    B1_VALUE = "YOUR_B1_VALUE_HERE"  # ← 替换为实际的 b1 值
    
    return xhs_sign(
        uri, 
        data=data, 
        ctime=ctime, 
        a1=a1, 
        b1=B1_VALUE  # ← 传入 b1
    )
```

### 第 3 步：更新应用启动代码

编辑文件: `xhs_monitor/app.py`

在初始化爬虫时确保传入正确的 sign 函数：

```python
from xhs_monitor.crawler import sign_wrapper

# 创建爬虫实例
crawler = Crawler(sign=sign_wrapper)
```

### 第 4 步：验证修复

运行诊断脚本来测试：

```bash
python deep_diagnosis.py
```

预期输出：
```
[TEST 1] Sign Function: OK ?
[TEST 2] Client Initialization: OK ?
[TEST 4] Authentication (get_self_info): OK ? (应该显示用户信息)
[TEST 3] User Info Fetch: OK ? (应该显示目标用户信息)
```

### 第 5 步：测试完整爬取流程

```bash
python test_crawl_debug.py
```

应该能够成功获取内容。

## 重要注意事项

### ?? b1 值的有效期
- `b1` 值是浏览器生成的，可能会过期
- 如果不再工作，需要重新从浏览器复制新值
- 建议每次运行前都验证 b1 是否仍然有效

### ? 动态更新 b1（可选）
如果您想自动处理 b1 过期问题，可以定期从浏览器获取：

```python
# 方案 1：使用 Selenium 自动获取
from selenium import webdriver

def get_b1_from_browser():
    """使用 Selenium 从浏览器获取 b1"""
    driver = webdriver.Chrome()
    driver.get("https://www.xiaohongshu.com")
    # 等待 JS 执行
    time.sleep(5)
    b1 = driver.execute_script("return localStorage.getItem('b1')")
    driver.quit()
    return b1
```

### ? Cookie 完整性检查表
确保您的 Cookie 包含以下必要值：
- [ ] `a1` - 用户身份令牌
- [ ] `web_session` - 会话 ID
- [ ] `webId` - Web ID
- [ ] `gid` - 跟踪 ID
- [ ] 其他必要 cookies

## 文件位置参考

| 文件 | 用途 |
|------|------|
| `xhs_monitor/crawler.py` | 需要更新 `sign_wrapper` 函数 |
| `xhs_monitor/app.py` | Flask 应用，使用爬虫 |
| `deep_diagnosis.py` | 诊断脚本 |
| `test_crawl_debug.py` | 测试爬取功能 |

## 故障排除

### 问题：仍然收到 406 错误

**解决方案**：
1. 验证 b1 值是否正确复制（不要包含空格）
2. 检查 b1 是否过期，重新从浏览器获取
3. 确保 Cookie（a1, web_session 等）未过期

### 问题：认证失败 (code: -1)

**解决方案**：
1. 重新登录小红书网站
2. 重新从浏览器复制所有 cookies
3. 重新获取 b1 值

### 问题：API 返回 "出现验证码"

**解决方案**：
1. 减慢爬取速度（增加 `crawl_interval` 参数）
2. 在浏览器中手动完成验证
3. 等待 1-2 小时后重试

## 验证和测试

完成修复后，运行以下测试序列：

```bash
# 1. 测试诊断
python deep_diagnosis.py

# 2. 测试爬取（单个用户）
python test_crawl_debug.py

# 3. 启动 Web 界面并手动测试
python run.py

# 然后访问 http://localhost:5000 进行 UI 测试
```

## 技术细节

### Sign 函数如何工作

```
输入: URI, 数据, a1, b1
      ↓
生成签名: x-s, x-t
      ↓
构建 x-s-common:
  - 包含 b1 值
  - 包含 a1 值
  - 包含时间戳
  - Base64 编码
      ↓
发送请求头:
  x-s, x-t, x-s-common
  + 其他浏览器头部
  + Cookies
      ↓
服务器验证签名和 b1
      ↓
成功或失败
```

### 为什么 406 无法解决
- 406 表示服务器拒绝处理请求
- 这发生在签名验证失败时
- 缺少 b1 会导致签名验证失败
- 即使其他一切都正确也会返回 406

## 常见问题

**Q: 为什么之前的代码不工作？**
A: 因为没有提供 b1 值。XhsClient 库需要它来创建有效的签名。

**Q: 我可以生成 b1 值吗？**
A: 不行。b1 必须从浏览器获取。它是浏览器在访问小红书时生成的唯一值。

**Q: b1 会暴露我的隐私吗？**
A: 不会。b1 类似于浏览器 cookie，不包含个人信息。

**Q: 多久需要重新获取一次 b1？**
A: 通常能用几天到几周。如果出现 406 错误，重新获取新的 b1。

## 下一步

1. ? 从浏览器复制 b1 值
2. ? 更新 `sign_wrapper` 函数
3. ? 运行诊断脚本验证
4. ? 测试爬取功能
5. ? 在 Web UI 中进行最终测试

---

需要帮助? 运行诊断脚本查看详细错误信息:
```bash
python deep_diagnosis.py
```
