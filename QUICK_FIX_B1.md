# ? 快速修复指南 - 只需 3 分钟

## 根本原因已确定

您的 API 请求失败是因为**缺少 `b1` 参数**。

```
Sign Function:      ? 工作正常  
Client Init:        ? 工作正常  
Cookies:            ? 有效  
Authentication:     ? 失败 (缺少 b1)
        ↓
HTTP 406 + code: -1
```

---

## 修复步骤

### 步骤 1??  - 获取 b1 值（1 分钟）

```
1. 在浏览器按 F12 打开开发者工具
2. 点击 "Application" 标签
3. 左侧菜单 → Local Storage → https://www.xiaohongshu.com
4. 找到 "b1" 键，复制其值
5. 例如: "xxxx_yyyy_zzzz_abcd_1234"
```

? **截图参考**:
```
Application tab
├── Local Storage
    └── https://www.xiaohongshu.com
        ├── ...
        ├── b1 ← 复制这个值
        └── ...
```

### 步骤 2?? - 更新代码（1 分钟）

编辑文件：`xhs_monitor/crawler.py`

找到这段代码（大约第 1-30 行）：

```python
def sign_wrapper(uri, data=None, ctime=None, a1="", b1="", **kwargs):
    """
    包装 sign 函数以处理 XhsClient 传递的额外参数
    """
    return xhs_sign(uri, data=data, ctime=ctime, a1=a1, b1=b1)
```

**替换为**：

```python
def sign_wrapper(uri, data=None, ctime=None, a1="", b1="", **kwargs):
    """
    包装 sign 函数以处理 XhsClient 传递的额外参数
    
    重要: 需要从浏览器 LocalStorage 获取 b1 值
    """
    # TODO: 将下面的值替换为从浏览器获取的实际 b1 值
    BROWSER_B1 = "从浏览器复制的_b1_值"  # ← 替换这行
    
    return xhs_sign(uri, data=data, ctime=ctime, a1=a1, b1=BROWSER_B1)
```

### 步骤 3?? - 验证修复（1 分钟）

运行诊断脚本：

```bash
python deep_diagnosis.py
```

预期看到：

```
? [TEST 1] Sign Function: OK
? [TEST 2] Client Initialization: OK  
? [TEST 4] Authentication: OK ← 从 ? 变成 ?
? [TEST 3] User Info: OK ← 从 ? 变成 ?
```

---

## 我已经做完了，现在怎么办？

测试爬取功能：

```bash
python test_crawl_debug.py
```

或启动 Web 界面：

```bash
python run.py
```

然后在浏览器访问 http://localhost:5000

---

## ?? 重要提醒

1. **b1 值会过期** - 如果不再工作，重新从浏览器获取新值
2. **不要公开 b1** - 它类似于 Cookie，应该保密
3. **每个浏览器/设备不同** - 从您实际使用的浏览器获取

---

## 常见问题

### Q: 我找不到 b1 值？
A: 
- 确保在 Chrome/Firefox 的 DevTools 中，不是 Safari 或 IE
- 确保网站是 https://www.xiaohongshu.com
- 登出并重新登录，然后再查找
- 刷新页面

### Q: 仍然显示 406 错误？
A: 
- 检查 b1 值是否完全复制（包括所有字符）
- 没有多余的空格或换行符
- b1 可能已过期，尝试新的

### Q: b1 值应该看起来像什么？
A: 通常类似这样：
```
abcd_1234_xyzw_5678_mnop
或者
af847d5c-6e1e-4f8a-9b1c-2d3e4f5a6b7c
```
（长字符串）

---

## 下一步

? 从浏览器复制 b1
? 更新 `sign_wrapper()` 函数  
? 运行 `python deep_diagnosis.py` 验证
? 启动应用测试

---

## 需要帮助？

如果修复后仍有问题，运行：

```bash
python advanced_diagnosis.py
```

查看详细的请求/响应信息。

---

**预计修复时间**: 3-5 分钟  
**难度等级**: ? 简单
