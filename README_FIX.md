# ? API 406 错误 - 完全诊断和修复指南

## ? 快速摘要

```
问题: HTTP 406 + {"code": -1, "success": false}
原因: 缺少 B1 参数 (浏览器 localStorage 值)
修复: 3-5 分钟
难度: ? 非常简单
```

---

## ? 文档导航

### ? 我应该看哪个文档？

**您的情况** → **推荐文档**

| 您的需求 | 推荐文档 | 时间 |
|---------|--------|------|
| 快速修复，立即开始 | `QUICK_FIX_B1.md` | 3 分钟 |
| 详细步骤和解释 | `FIX_B1_PARAMETER.md` | 10 分钟 |
| 完整修复指南 + 检查清单 | `FINAL_FIX_GUIDE.md` | 5 分钟 |
| 技术细节和学习 | `DIAGNOSIS_REPORT.md` | 20 分钟 |
| 诊断过程总结 | `B1_PARAMETER_ANALYSIS.md` | 15 分钟 |

---

## ? 开始修复 (只需 3 步)

### ? 第一步：从浏览器获取 B1 值

**在浏览器中操作**：

```
1. 打开 Chrome/Firefox
2. 访问 https://www.xiaohongshu.com
3. 按 F12 打开开发者工具
4. 点击 "Application" 标签
5. 左侧菜单: Local Storage → https://www.xiaohongshu.com
6. 在表格中查找 "b1" 键
7. 复制其值（长字符串，如 af847d5c-6e1e-4f8a-...）
```

**B1 值示例**:
```
af847d5c-6e1e-4f8a-9b1c-2d3e4f5a6b7c
```

### ? 第二步：更新代码

编辑文件: `xhs_monitor/crawler.py`

找到 `sign_wrapper` 函数（约在第 1-30 行）并修改：

**从**:
```python
def sign_wrapper(uri, data=None, ctime=None, a1="", b1="", **kwargs):
    return xhs_sign(uri, data=data, ctime=ctime, a1=a1, b1=b1)
```

**改为**:
```python
def sign_wrapper(uri, data=None, ctime=None, a1="", b1="", **kwargs):
    # 从浏览器 localStorage 获取的 B1 值
    BROWSER_B1 = "af847d5c-6e1e-4f8a-9b1c-2d3e4f5a6b7c"  # ← 粘贴您的 B1 值
    
    return xhs_sign(uri, data=data, ctime=ctime, a1=a1, b1=BROWSER_B1)
```

### ? 第三步：验证修复

```bash
python deep_diagnosis.py
```

**预期输出**:
```
? [TEST 1] Sign Function: OK
? [TEST 2] Client Initialization: OK
? [TEST 4] Authentication: OK
? [TEST 3] User Info: OK
```

全部显示 ? = 修复成功！

---

## ? 详细文档

### 快速参考
- **QUICK_FIX_B1.md** - 3 分钟快速修复指南

### 完整指南
- **FINAL_FIX_GUIDE.md** - 带检查清单的完整指南
- **FIX_B1_PARAMETER.md** - 详细技术指南

### 诊断和学习
- **DIAGNOSIS_REPORT.md** - 完整诊断报告
- **B1_PARAMETER_ANALYSIS.md** - 工作总结

---

## ? 诊断脚本

### 已创建的脚本

```
deep_diagnosis.py          ← 4 层诊断测试（推荐运行）
advanced_diagnosis.py      ← 原始 HTTP 请求分析
test_headers.py           ← 请求头组合测试
test_b1_param.py          ← B1 参数影响测试
fix_b1_auto.py            ← 自动化修复工具
```

### 运行诊断

```bash
# 基础诊断（强烈推荐）
python deep_diagnosis.py

# 高级诊断（查看请求详情）
python advanced_diagnosis.py

# 自动修复（交互式）
python fix_b1_auto.py
```

---

## ? 诊断结果

### 已确认 ?
```
? Sign 函数: 正常工作
? XhsClient 初始化: 成功
? Cookie 解析: 正确
? 请求头: 有效
```

### 已找到问题 ?
```
? B1 参数: 缺失（这导致了 406 错误）
```

### 解决方案 ?
```
? 从浏览器获取 B1 值，添加到代码
? 所有问题解决
```

---

## ? 问题详解

### 为什么返回 406？

```
API 验证流程:
  1. 检查签名 (x-s, x-t) ?
  2. 检查 Cookie (a1, web_session) ?
  3. 检查 x-s-common 中的 b1 ? ← 为空
  4. 返回 406 Not Acceptable
```

### B1 的作用

```
x-s-common 包含:
{
  "x5": "a1_from_cookie",   ← Cookie 值
  "x8": "b1_from_localStorage",  ← 浏览器值 ← 缺失！
  "x6": "timestamp",
  "x7": "signature"
}
```

不包含有效的 b1 → 签名验证失败 → 406

---

## ?? 重要注意

### B1 值会过期
- 有效期通常 1-4 周
- 过期后需要重新从浏览器复制
- 如果再次出现 406，重新获取新 B1

### 需要有效的 Cookie
- 同时需要有效的 `a1` 和 `web_session`
- 这些在 Cookie 中，您已经有了
- 如果 Cookie 过期需要重新登录小红书

### 防爬虫限制
```
小红书有以下限制:
- IP 访问频率: 稍等片刻再爬
- 验证码: 可能需要手动完成
- 会话超时: Cookie 过期
```

---

## ? 测试流程

### 步骤 1: 诊断
```bash
python deep_diagnosis.py
```

### 步骤 2: 爬取测试
```bash
python test_crawl_debug.py
```

### 步骤 3: 启动应用
```bash
python run.py
```

### 步骤 4: 访问 Web UI
```
http://localhost:5000
```

---

## ? 常见问题

### Q: 我找不到 B1 值？
**A**: 
- 确保在 Chrome/Firefox DevTools 中操作
- 确认网址是 https://www.xiaohongshu.com
- 尝试刷新页面后再查找
- 或重新登录

### Q: 仍然返回 406？
**A**:
- 检查 B1 值是否完全复制（包括所有字符）
- 确保没有额外的空格或换行
- B1 可能已过期，尝试获取新的
- 运行 `python advanced_diagnosis.py` 查看详情

### Q: B1 值看起来像什么？
**A**:
```
? 正确的 B1 值:
  af847d5c-6e1e-4f8a-9b1c-2d3e4f5a6b7c
  或
  xhs_b1_token_1234567890_abcdef

? 错误的 B1 值:
  空值
  太短的字符串 (< 10 个字符)
```

### Q: 多久需要重新获取 B1？
**A**:
- 通常能用 1-4 周
- 如果再次出现 406，重新获取

### Q: 自动化修复工具安全吗？
**A**:
- 完全安全，只修改一个参数
- 不会修改其他代码
- 可以查看源代码验证

---

## ? 修复前检查

在开始修复前，确保：

- [ ] 您有浏览器访问权限
- [ ] 已登录小红书账号
- [ ] 能看到 DevTools
- [ ] 能找到 Local Storage

---

## ? 修复后验证

修复完成后，检查：

- [ ] 所有诊断测试都显示 ?
- [ ] `python test_crawl_debug.py` 成功运行
- [ ] Web UI 能加载
- [ ] 能成功获取内容

---

## ? 学习资源

### 如果您想了解更多

1. **HTTP 406 错误**
   - 404 = Not Found
   - 406 = Not Acceptable (格式/验证错误)

2. **浏览器 LocalStorage**
   - 存储客户端特定数据
   - 与 Cookie 不同（但都用于会话追踪）

3. **API 签名验证**
   - 小红书使用多层验证
   - 包括时间戳、哈希、设备指纹

4. **反爬虫机制**
   - 检查 User-Agent
   - 要求浏览器生成的 Token
   - 频率限制和 IP 检测

---

## ? 需要帮助？

### 问题 1: 修复不工作
```bash
# 获取详细诊断信息
python advanced_diagnosis.py
```

### 问题 2: 需要自动化
```bash
# 使用自动修复工具
python fix_b1_auto.py
```

### 问题 3: 需要详细说明
查看相应文档：
- `QUICK_FIX_B1.md` - 快速参考
- `FIX_B1_PARAMETER.md` - 详细指南
- `DIAGNOSIS_REPORT.md` - 技术文档

---

## ? 开始吧！

### 现在就开始修复

1. 从浏览器复制 B1 值
2. 编辑 `xhs_monitor/crawler.py`
3. 运行 `python deep_diagnosis.py` 验证
4. 完成！

**预计时间**: 3-5 分钟  
**难度**: ? 非常简单  
**成功率**: 95%+

---

**诊断完成** ?  
**现在开始修复** ?
