"""内容爬取模块"""
import uuid
import logging
from typing import List, Optional
try:
    from xhs import XhsClient, DataFetchError
except ImportError:
    from xhs import XhsClient
    DataFetchError = Exception

from xhs.help import sign as xhs_sign
from .models import Content, Account

logger = logging.getLogger(__name__)


def sign_wrapper(uri, data=None, ctime=None, a1="", b1="", **kwargs):
    """
    Wrapper for xhs.help.sign to handle extra parameters from XhsClient.
    XhsClient may pass additional parameters like web_session, which we ignore.
    """
    BROWSER_B1 = "I38rHdgsjopgIvesdVwgIC+oIELmBZ5e3VwXLgFTIxS3bqwErFeexd0ekncAzMFYnqthIhJeSBMDKutRI3KsYorWHPtGrbV0P9WfIi/eWc6eYqtyQApPI37ekmR6QL+5Ii6sdneeSfqYHqwl2qt5B0DBIx++GDi/sVtkIxdsxuwr4qtiIhuaIE3e3LV0I3VTIC7e0utl2ADmsLveDSKsSPw5IEvsiVtJOqw8BuwfPpdeTFWOIx4TIiu6ZPwbPutXIvlaLbgs3qtxIxes1VwHIkumIkIyejgsY/WTge7eSqte/D7sDcpipedeYrDtIC6eDVw2IENsSqtlnlSuNjVtIvoekqt3cZ7sVo4gIESyIhEgQ9quIxhnqz8gIkIfoqwkICZWG73sdlOeVPw3IvAe0fged0iNIi5s3Ibf2utAIiKsidvekZNeTPt4nAOeWPwEIvSgz0eefqwhpnOsfPwrI3lrIxE5Luwwaqw+rekhZANe1MNe0Pw9ICNsVLoeSbIFIkosSr7sVnFiIkgsVVtMIiudqqw+tqtWI30e3PwIIhoe3ut1IiOsjut3wutnsPwXICclI3Ir27lk2I5e1utCIES/IEJs0PtnpYIAO0JeYfD1IErPOPtKoqw3I3OexqtWQL5eizdsVMmmIhgsVdJs3PtPLVwaIvgefVwfIkgs60WoICKedo/efqt9I3OsVqw62dMBIhIGIveskLoeVdveDS6edVtBIkF1I3Q6rVtQIvchIE5s3FqAwLgeDuwzIkL8Lqw+tLNeYY/sTutsnPtrI3qFIhkdOqtvZqwMIiNsVmJeTqwtzPtZIh8OeVtPICc4pnTrIivsDFee0BdsVutqqPwmIkrxIvvsiVw5IiesjchlIvRNHsYAIvmTIv/eVqw2GqtC+qtXI3WnIENsYedekVwE/nZTICDn4ut1mut8IxhlIibxI3pbIv/edBNsdnkGBVwFIEFJ2Pwjeuw2Ii6eTASRIiZucFgs0utdzVtnal+brc=="  # ← 粘贴这里

    return xhs_sign(uri, data=data, ctime=ctime, a1=a1, b1=BROWSER_B1)


class ContentCrawler:
    """内容爬取器"""
    
    def __init__(self, sign_func=None):
        """
        初始化爬取器
        
        Args:
            sign_func: 签名函数，用于获取签名参数
        """
        # 如果没有提供签名函数，使用包装的 sign 函数
        self.sign_func = sign_func if sign_func is not None else sign_wrapper
        self.max_retries = 3
    
    def fetch_user_content(self, account: Account, user_id: str) -> List[Content]:
        """
        获取指定用户的所有内容
        
        Args:
            account: 用于爬取的账号信息
            user_id: 目标用户ID
            
        Returns:
            内容列表
        """
        print("\n" + "="*80)
        print(f"开始爬取用户 {user_id} 的内容...")
        print("="*80)
        
        try:
            if not account.cookie or account.cookie.strip() == "":
                print("❌ 账号Cookie为空")
                logger.error("账号Cookie为空")
                return []
            
            # 创建XhsClient，使用签名函数
            print(f"\n[1/5] 初始化 XhsClient...")
            print(f"  - 账号ID: {account.account_id}")
            print(f"  - 账号用户名: {account.username}")
            print(f"  - Cookie长度: {len(account.cookie)}")
            print(f"  - Sign函数: {self.sign_func.__name__ if self.sign_func else 'None'}")
            
            client = XhsClient(
                cookie=account.cookie,
                sign=self.sign_func if callable(self.sign_func) else None
            )
            print("✓ XhsClient 初始化成功")
            
            # 验证Cookie是否有效
            print(f"\n[2/5] 验证Cookie有效性...")
            try:
                self_info = client.get_self_info()
                if self_info and "user_info" in self_info:
                    my_user_id = self_info["user_info"].get("user_id", "Unknown")
                    my_username = self_info["user_info"].get("nick_name", "Unknown")
                    print(f"✓ Cookie验证成功")
                    print(f"  - 当前登录用户ID: {my_user_id}")
                    print(f"  - 当前登录用户名: {my_username}")
                else:
                    print(f"⚠ Cookie验证失败，返回数据异常: {self_info}")
                    print(f"  继续尝试爬取目标用户...")
            except Exception as e:
                error_msg = str(e)
                print(f"⚠ Cookie验证异常: {error_msg}")
                print(f"  - 错误类型: {type(e).__name__}")
                print(f"  - 这可能表示 Cookie 已过期或无效")
                print(f"  继续尝试爬取目标用户...")

            
            # 获取用户信息
            print(f"\n[3/5] 获取用户 {user_id} 的信息...")
            try:
                print(f"  - 调用 client.get_user_info('{user_id}')")
                user_info = client.get_user_info(user_id)
                print(f"  - API返回数据: {str(user_info)[:200]}...")
                
                if not user_info or "user_info" not in user_info:
                    print(f"⚠ 无法获取用户 {user_id} 的信息")
                    username = "Unknown"
                else:
                    username = user_info.get("user_info", {}).get("nick_name", "Unknown")
                    user_signature = user_info.get("user_info", {}).get("signature", "")
                    print(f"✓ 成功获取用户信息")
                    print(f"  - 用户名: {username}")
                    print(f"  - 个签: {user_signature}")
            except Exception as e:
                print(f"❌ 获取用户信息失败: {str(e)}")
                import traceback
                traceback.print_exc()
                logger.warning(f"获取用户信息失败: {str(e)}, 使用默认用户名")
                username = "Unknown"
            
            # 获取用户笔记列表
            print(f"\n[4/5] 获取用户 {user_id} 的笔记列表...")
            try:
                print(f"  - 调用 client.get_user_all_notes('{user_id}', crawl_interval=1)")
                notes = client.get_user_all_notes(user_id, crawl_interval=1)
                print(f"✓ 成功获取笔记列表")
                print(f"  - 笔记总数: {len(notes)}")
                
                if not notes:
                    print(f"⚠ 用户 {user_id} 暂无笔记")
                    return []
                
                # 打印前3条笔记的信息
                for idx, note in enumerate(notes[:3]):
                    print(f"  - 笔记 {idx+1}: {note.title[:50]}... (ID: {note.note_id})")
                if len(notes) > 3:
                    print(f"  - ... 还有 {len(notes)-3} 条笔记")
                    
            except Exception as e:
                print(f"❌ 爬取笔记失败: {str(e)}")
                import traceback
                traceback.print_exc()
                logger.error(f"爬取笔记失败: {str(e)}")
                return []
            
            # 解析笔记
            print(f"\n[5/5] 解析笔记并转换为Content对象...")
            contents = []
            for idx, note_data in enumerate(notes):
                try:
                    content = self._parse_note_to_content(note_data, user_id, username)
                    if content:
                        contents.append(content)
                        print(f"  ✓ 笔记 {idx+1}: {content.title[:50]}...")
                except Exception as e:
                    print(f"  ❌ 笔记 {idx+1} 解析失败: {str(e)}")
                    logger.warning(f"解析笔记失败: {str(e)}")
                    continue
            
            print("\n" + "="*80)
            print(f"✓ 成功爬取用户 {user_id} 的 {len(contents)} 条笔记")
            print("="*80 + "\n")
            return contents
            
        except Exception as e:
            print("\n" + "="*80)
            print(f"❌ 爬取用户 {user_id} 的内容时发生错误")
            print("="*80)
            print(f"错误信息: {str(e)}")
            import traceback
            traceback.print_exc()
            logger.error(f"爬取用户 {user_id} 的内容时发生错误: {str(e)}")
            return []
    
    def _parse_note_to_content(self, note_data: dict, user_id: str, username: str) -> Optional[Content]:
        """
        将笔记数据转换为Content对象
        
        Args:
            note_data: 笔记数据
            user_id: 用户ID
            username: 用户名
            
        Returns:
            Content对象或None
        """
        try:
            note_id = note_data.get("note_id", "")
            title = note_data.get("title", "")
            desc = note_data.get("desc", "")
            content_type = note_data.get("type", "normal")
            publish_time = note_data.get("time", 0)
            
            # 构造链接
            link = f"https://www.xiaohongshu.com/explore/{note_id}"
            
            # 获取媒体信息
            img_urls = note_data.get("img_urls", [])
            video_url = note_data.get("video_url", "")
            
            # 确定内容类型
            if video_url:
                inferred_type = "video"
            elif img_urls:
                inferred_type = "image"
            else:
                inferred_type = "text"
            
            content = Content(
                note_id=note_id,
                title=title,
                desc=desc,
                content_type=inferred_type,
                publish_time=publish_time,
                link=link,
                user_id=user_id,
                username=username,
                img_urls=img_urls,
                video_url=video_url
            )
            
            return content
        except Exception as e:
            print(f"Error parsing note: {str(e)}")
            return None
