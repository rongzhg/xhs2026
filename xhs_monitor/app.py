"""Flask应用程序主文件"""
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from .models import Database, Account, Content
from .crawler import ContentCrawler, sign_wrapper
from .converter import DummyConverter, ContentConverter


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_AS_ASCII'] = False

# 初始化数据库
db = Database(data_dir='data')

# 初始化爬取器和转换器
# 使用包装的 sign 函数来处理 XhsClient 传递的额外参数
crawler = ContentCrawler(sign_func=sign_wrapper)  # 使用包装的 sign 函数
converter = DummyConverter()  # 使用虚拟转换器演示


# ============ 账号管理接口 ============

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    """获取所有账号"""
    accounts = db.get_all_accounts()
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': [acc.to_dict() for acc in accounts]
    })


@app.route('/api/accounts', methods=['POST'])
def add_account():
    """添加新账号"""
    try:
        data = request.json
        
        # 验证必需字段
        required_fields = ['username', 'user_id', 'cookie']
        if not all(field in data for field in required_fields):
            return jsonify({
                'code': -1,
                'message': '缺少必需字段'
            }), 400
        
        account_id = str(uuid.uuid4())
        account = Account(
            account_id=account_id,
            username=data['username'],
            user_id=data['user_id'],
            cookie=data['cookie'],
            a1=data.get('a1', '')
        )
        
        if db.add_account(account):
            return jsonify({
                'code': 0,
                'message': '账号添加成功',
                'data': account.to_dict()
            })
        else:
            return jsonify({
                'code': -1,
                'message': '账号已存在'
            }), 400
            
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': str(e)
        }), 500


@app.route('/api/accounts/<account_id>', methods=['DELETE'])
def delete_account(account_id):
    """删除账号"""
    try:
        if db.delete_account(account_id):
            return jsonify({
                'code': 0,
                'message': '账号删除成功'
            })
        else:
            return jsonify({
                'code': -1,
                'message': '账号不存在'
            }), 404
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': str(e)
        }), 500


# ============ 内容爬取和转换接口 ============

@app.route('/api/fetch-content', methods=['POST'])
def fetch_content():
    """爬取指定用户的内容"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'code': -1,
                'message': '请求体为空'
            }), 400
        
        account_id = data.get('account_id')
        user_id = data.get('user_id')
        
        if not account_id or not user_id:
            return jsonify({
                'code': -1,
                'message': '缺少必需参数: account_id 和 user_id 都是必需的'
            }), 400
        
        # 验证user_id格式
        if not isinstance(user_id, str) or len(user_id.strip()) == 0:
            return jsonify({
                'code': -1,
                'message': '用户ID格式不正确'
            }), 400
        
        account = db.get_account(account_id)
        if not account:
            return jsonify({
                'code': -1,
                'message': '账号不存在或已被删除'
            }), 404
        
        # 验证账号Cookie
        if not account.cookie or account.cookie.strip() == "":
            return jsonify({
                'code': -1,
                'message': '账号Cookie为空，请检查账号配置'
            }), 400
        
        # 爬取内容
        print(f"开始爬取用户 {user_id} 的内容...")
        contents = crawler.fetch_user_content(account, user_id.strip())
        
        if not contents:
            return jsonify({
                'code': 0,
                'message': '该用户暂无可爬取的内容（可能用户ID错误或用户无发布内容）',
                'data': {
                    'total': 0,
                    'saved': 0
                }
            })
        
        # 保存到数据库并进行转换
        saved_count = 0
        failed_count = 0
        
        for content in contents:
            try:
                if db.add_content(content):
                    saved_count += 1
                    # 自动转换内容
                    try:
                        converter.convert_content(content)
                        db.update_content(content)
                    except Exception as e:
                        print(f"转换失败: {str(e)}")
            except Exception as e:
                failed_count += 1
                print(f"保存内容失败: {str(e)}")
        
        message = f'成功爬取 {saved_count} 条新内容'
        if failed_count > 0:
            message += f'，失败 {failed_count} 条'
        
        return jsonify({
            'code': 0,
            'message': message,
            'data': {
                'total': len(contents),
                'saved': saved_count,
                'failed': failed_count
            }
        })
        
    except ValueError as e:
        return jsonify({
            'code': -1,
            'message': f'参数错误: {str(e)}'
        }), 400
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({
            'code': -1,
            'message': f'爬取失败: {str(e)}'
        }), 500


@app.route('/api/convert-content/<note_id>', methods=['POST'])
def convert_single_content(note_id):
    """转换单条内容"""
    try:
        content = db.get_content(note_id)
        if not content:
            return jsonify({
                'code': -1,
                'message': '内容不存在'
            }), 404
        
        # 执行转换
        success = converter.convert_content(content)
        db.update_content(content)
        
        return jsonify({
            'code': 0,
            'message': '转换成功' if success else '转换失败',
            'data': content.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': str(e)
        }), 500


# ============ 内容查询接口 ============

@app.route('/api/contents/user/<user_id>', methods=['GET'])
def get_user_contents(user_id):
    """获取指定用户的所有内容"""
    try:
        contents = db.get_user_contents(user_id)
        
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': [content.to_dict() for content in contents]
        })
        
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': str(e)
        }), 500


@app.route('/api/contents/type', methods=['GET'])
def get_contents_by_type():
    """根据类型获取内容"""
    try:
        user_id = request.args.get('user_id')
        content_type = request.args.get('type')  # video, image, text
        
        if not user_id or not content_type:
            return jsonify({
                'code': -1,
                'message': '缺少必需参数'
            }), 400
        
        contents = db.get_contents_by_type(user_id, content_type)
        
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': [content.to_dict() for content in contents]
        })
        
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': str(e)
        }), 500


@app.route('/api/contents/<note_id>', methods=['GET'])
def get_content_detail(note_id):
    """获取单条内容详情"""
    try:
        content = db.get_content(note_id)
        if not content:
            return jsonify({
                'code': -1,
                'message': '内容不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': content.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': str(e)
        }), 500


# ============ 统计接口 ============

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """获取统计数据"""
    try:
        all_contents = db.get_all_contents()
        all_accounts = db.get_all_accounts()
        
        # 统计各类型内容
        video_count = sum(1 for c in all_contents if c.content_type == 'video')
        image_count = sum(1 for c in all_contents if c.content_type == 'image')
        text_count = sum(1 for c in all_contents if c.content_type == 'text')
        
        # 统计转换状态
        completed_count = sum(1 for c in all_contents if c.conversion_status == 'completed')
        pending_count = sum(1 for c in all_contents if c.conversion_status == 'pending')
        failed_count = sum(1 for c in all_contents if c.conversion_status == 'failed')
        
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': {
                'total_accounts': len(all_accounts),
                'total_contents': len(all_contents),
                'content_types': {
                    'video': video_count,
                    'image': image_count,
                    'text': text_count
                },
                'conversion_status': {
                    'completed': completed_count,
                    'pending': pending_count,
                    'failed': failed_count
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': str(e)
        }), 500


# ============ 错误处理 ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'code': -1,
        'message': '资源不存在'
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'code': -1,
        'message': '服务器内部错误'
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
