"""
Flask应用初始化和路由配置示例
"""

# 注意：此文件展示了如何在existing Flask应用中集成xhs_monitor

from flask import Flask, render_template, request, jsonify
from xhs_monitor.app import app as xhs_monitor_app

# 如果要在其他Flask应用中集成xhs_monitor
def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 配置
    app.config['JSON_AS_ASCII'] = False
    
    # 注册xhs_monitor的蓝图（如果需要）
    # app.register_blueprint(xhs_monitor_app)
    
    # 或者挂载为子应用
    # app.add_url_rule('/xhs', 'xhs_monitor', xhs_monitor_app)
    
    return app


if __name__ == '__main__':
    # 直接运行xhs_monitor_app
    xhs_monitor_app.run(debug=True, host='0.0.0.0', port=5000)
