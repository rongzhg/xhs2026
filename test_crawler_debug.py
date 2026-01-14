#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
小红书内容爬取测试脚本
用于诊断和测试爬取功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试必要的导入"""
    print("=" * 60)
    print("1. 测试导入...")
    print("=" * 60)
    
    try:
        from xhs_monitor.models import Database, Account, Content
        print("? models 导入成功")
    except Exception as e:
        print(f"? models 导入失败: {e}")
        return False
    
    try:
        from xhs_monitor.crawler import ContentCrawler
        print("? crawler 导入成功")
    except Exception as e:
        print(f"? crawler 导入失败: {e}")
        return False
    
    try:
        from xhs import XhsClient
        print("? xhs 导入成功")
    except Exception as e:
        print(f"? xhs 导入失败: {e}")
        return False
    
    return True


def test_database():
    """测试数据库"""
    print("\n" + "=" * 60)
    print("2. 测试数据库...")
    print("=" * 60)
    
    try:
        from xhs_monitor.models import Database, Account
        
        db = Database(data_dir='data')
        print("? 数据库初始化成功")
        
        # 创建测试账号
        test_account = Account(
            account_id="test_001",
            username="测试账号",
            user_id="user_test",
            cookie="test_cookie"
        )
        
        print(f"? 账号模型创建成功: {test_account.username}")
        return True
    except Exception as e:
        print(f"? 数据库测试失败: {e}")
        return False


def test_sign_function():
    """测试真实签名函数"""
    print("\n" + "=" * 60)
    print("6. 测试XHS签名函数...")
    print("=" * 60)
    
    try:
        from xhs.help import sign as xhs_sign
        
        # 测试签名函数
        result = xhs_sign(
            uri="/test",
            data={"test": "data"},
            a1="test_a1"
        )
        
        if result and "x-s" in result and "x-t" in result:
            print("? XHS签名函数工作正常")
            print(f"  - x-s: {result['x-s'][:20]}...")
            print(f"  - x-t: {result['x-t']}")
            if "x-s-common" in result:
                print(f"  - x-s-common: {result['x-s-common'][:20]}...")
            return True
        else:
            print(f"? 签名函数返回异常: {result}")
            return False
    except Exception as e:
        print(f"? 签名函数测试失败: {e}")
        return False


def test_app():
    """测试Flask应用"""
    print("\n" + "=" * 60)
    print("4. 测试Flask应用...")
    print("=" * 60)
    
    try:
        from xhs_monitor.app import app
        print("? Flask应用导入成功")
        
        # 测试应用配置
        if app.config.get('JSON_AS_ASCII') == False:
            print("? Flask应用配置正确")
        else:
            print("? Flask应用配置可能有问题")
        
        return True
    except Exception as e:
        print(f"? Flask应用测试失败: {e}")
        return False


def test_routes():
    """测试API路由"""
    print("\n" + "=" * 60)
    print("5. 测试API路由...")
    print("=" * 60)
    
    try:
        from xhs_monitor.app import app
        
        # 获取所有路由
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append(str(rule))
        
        print(f"? 发现 {len(routes)} 个路由:")
        for route in sorted(routes):
            print(f"  - {route}")
        
        return True
    except Exception as e:
        print(f"? 路由测试失败: {e}")
        return False


def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  ? 小红书内容监控系统 - 爬取功能诊断工具       ║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = []
    
    # 运行测试
    results.append(("导入测试", test_imports()))
    if results[-1][1]:
        results.append(("数据库测试", test_database()))
        results.append(("爬取器测试", test_crawler()))
        results.append(("XHS签名测试", test_sign_function()))
        results.append(("应用测试", test_app()))
        results.append(("路由测试", test_routes()))
    
    # 输出总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "? 通过" if result else "? 失败"
        print(f"{status}: {name}")
    
    print(f"\n总体: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n? 所有测试通过！系统已准备好爬取内容。")
        print("\n后续步骤:")
        print("1. 启动应用: python run.py")
        print("2. 打开浏览器: http://localhost:5000")
        print("3. 添加小红书账号")
        print("4. 输入目标用户ID并爬取内容")
        return 0
    else:
        print("\n? 部分测试失败，请查看上方错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
