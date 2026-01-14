#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Automated B1 Fix Script
This script allows you to quickly update the b1 parameter without manual editing
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("\n" + "=" * 80)
    print("? 小红书爬虫 - B1 参数修复工具")
    print("=" * 80)
    
    print("""
本工具将帮助您修复 API 406 错误。

根本原因分析:
? Sign 函数: 正常工作
? Client 初始化: 正常工作  
? Cookies: 有效
? B1 参数: 缺失 ← 这导致了 406 错误

解决方案: 从浏览器获取 B1 值
    """)
    
    print("\n获取 B1 值的步骤:")
    print("  1. 打开浏览器，按 F12 打开开发者工具")
    print("  2. 进入 Application > Local Storage > https://www.xiaohongshu.com")
    print("  3. 找到 'b1' 键，复制其值（长字符串）")
    print("\n示例:")
    print("  ? b1 值看起来像: af847d5c-6e1e-4f8a-9b1c-2d3e4f5a6b7c")
    
    # Get b1 from user
    while True:
        print("\n" + "-" * 80)
        b1_value = input("请输入您从浏览器复制的 B1 值 (或 'skip' 跳过): ").strip()
        
        if b1_value.lower() == 'skip':
            print("??  跳过修复")
            return False
        
        if not b1_value:
            print("? B1 值不能为空，请重试")
            continue
        
        if len(b1_value) < 10:
            print("? B1 值太短（应至少 10 个字符），请检查是否完全复制")
            continue
        
        # Confirm
        print(f"\n您输入的 B1 值: {b1_value[:50]}...")
        confirm = input("确认无误? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            break
        else:
            print("? 取消，请重新输入")
            continue
    
    # Update crawler.py
    print("\n" + "-" * 80)
    print("? 正在更新 xhs_monitor/crawler.py...")
    
    crawler_path = os.path.join(os.path.dirname(__file__), 'xhs_monitor', 'crawler.py')
    
    if not os.path.exists(crawler_path):
        print(f"? 错误: 找不到 {crawler_path}")
        return False
    
    # Read current file
    with open(crawler_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has b1
    if 'BROWSER_B1 =' in content or 'B1_VALUE =' in content or 'b1 =' in content and '"从浏览器' not in content:
        print("??  文件已包含 B1 定义")
        overwrite = input("要覆盖现有的 B1 值吗? (yes/no): ").strip().lower()
        if overwrite not in ['yes', 'y']:
            print("??  保持原值")
            return False
    
    # Find and replace in sign_wrapper function
    import re
    
    # Pattern to find the sign_wrapper function
    pattern = r'(def sign_wrapper\([^)]*\):\s*"""[^"]*"""\s+)'
    
    # Check if pattern exists
    if not re.search(pattern, content):
        print("??  找不到 sign_wrapper 函数定义")
        # Try simpler pattern
        if 'def sign_wrapper' in content:
            print("   找到了函数，尝试手动插入...")
            lines = content.split('\n')
            new_lines = []
            inserted = False
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                
                if not inserted and 'def sign_wrapper' in line:
                    # Find the docstring end
                    j = i + 1
                    while j < len(lines) and '"""' in lines[j]:
                        new_lines.append(lines[j])
                        j += 1
                        if j - i > 1 and '"""' in lines[j-1]:
                            # Found closing docstring
                            break
                    
                    # Insert b1 definition
                    indent = '    '
                    new_lines.append(f"{indent}BROWSER_B1 = {repr(b1_value)}")
                    inserted = True
                    
                    # Skip original b1 definitions if any
                    while j < len(lines) and (
                        lines[j].strip().startswith('B1_VALUE') or 
                        lines[j].strip().startswith('BROWSER_B1') or
                        lines[j].strip().startswith('b1 =')
                    ):
                        j += 1
                    i = j - 1
            
            content = '\n'.join(new_lines)
        else:
            print("? 无法找到 sign_wrapper 函数")
            return False
    
    # Replace any existing b1_VALUE or BROWSER_B1
    content = re.sub(
        r'(BROWSER_B1|B1_VALUE)\s*=\s*["\'][^"\']*["\']',
        f'BROWSER_B1 = {repr(b1_value)}',
        content
    )
    
    # Write back
    with open(crawler_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"? 已更新 B1 值: {b1_value[:50]}...")
    
    # Test the fix
    print("\n" + "-" * 80)
    print("? 测试修复...")
    
    test_result = test_b1_fix(b1_value)
    
    if test_result:
        print("\n? 修复成功!")
        print("\n下一步:")
        print("  1. 运行: python deep_diagnosis.py")
        print("  2. 如果所有测试都通过，运行: python test_crawl_debug.py")
        print("  3. 启动 Web 应用: python run.py")
        return True
    else:
        print("\n??  测试失败，可能 B1 值已过期")
        print("   请重新从浏览器获取新的 B1 值")
        return False


def test_b1_fix(b1_value):
    """Test if B1 value works"""
    try:
        from xhs import XhsClient
        from xhs.help import sign as xhs_sign
        
        # Test sign function
        uri = "/api/sns/web/v1/user/selfinfo"
        a1 = "test_a1"
        
        signs = xhs_sign(uri, data=None, a1=a1, b1=b1_value)
        
        # Check if signature generated
        if 'x-s' in signs and 'x-t' in signs and 'x-s-common' in signs:
            print("? 签名生成成功")
            return True
        else:
            print("? 签名生成失败")
            return False
    except Exception as e:
        print(f"? 测试异常: {str(e)}")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
