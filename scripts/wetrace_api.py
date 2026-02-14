#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wetrace API Python Client
微信聊天记录分析工具的 Python 客户端
使用标准库，无需安装任何第三方依赖
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import sys
import io
from typing import Optional, List, Dict, Any, Union

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class WetraceClient:
    """Wetrace API 客户端"""

    def __init__(self, base_url: str = "http://127.0.0.1:5200/api/v1"):
        """
        初始化客户端

        Args:
            base_url: API 基础 URL
        """
        self.base_url = base_url.rstrip('/')

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Union[Dict, List, bytes]:
        """
        发送 HTTP 请求

        Args:
            method: HTTP 方法
            endpoint: API 端点
            params: 查询参数

        Returns:
            响应数据
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # 添加查询参数
        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"

        # 创建请求
        req = urllib.request.Request(url, method=method)

        try:
            with urllib.request.urlopen(req) as response:
                content_type = response.headers.get('Content-Type', '')

                # 如果是文件下载，返回字节
                if 'application/octet-stream' in content_type or \
                   'application/zip' in content_type or \
                   'application/pdf' in content_type:
                    return response.read()

                # 否则解析 JSON
                data = response.read()
                return json.loads(data.decode('utf-8'))

        except urllib.error.HTTPError as e:
            error_msg = e.read().decode('utf-8')
            try:
                error_data = json.loads(error_msg)
                raise Exception(f"HTTP {e.code}: {error_data.get('error', error_msg)}")
            except json.JSONDecodeError:
                raise Exception(f"HTTP {e.code}: {error_msg}")
        except urllib.error.URLError as e:
            raise Exception(f"连接失败: {e.reason}")

    # ==================== 会话管理 ====================

    def get_sessions(self, keyword: Optional[str] = None,
                    limit: int = 50, offset: int = 0) -> List[Dict]:
        """
        获取聊天会话列表

        Args:
            keyword: 会话名称搜索关键词
            limit: 返回结果数量
            offset: 分页偏移量

        Returns:
            会话列表
        """
        params = {'limit': limit, 'offset': offset}
        if keyword:
            params['keyword'] = keyword

        return self._request('GET', '/sessions', params=params)

    def delete_session(self, session_id: str) -> Dict:
        """
        删除会话

        Args:
            session_id: 会话用户名

        Returns:
            删除结果
        """
        return self._request('DELETE', f'/sessions/{session_id}')

    # ==================== 消息查询 ====================

    def get_messages(self, talker_id: Optional[str] = None,
                    sender_id: Optional[str] = None,
                    keyword: Optional[str] = None,
                    time_range: Optional[str] = None,
                    reverse: bool = False,
                    limit: int = 50, offset: int = 0) -> List[Dict]:
        """
        获取消息列表

        Args:
            talker_id: 会话用户名
            sender_id: 发送者用户名
            keyword: 搜索关键词
            time_range: 时间范围 (如 "2024-01-01~2024-01-31" 或 "last_week")
            reverse: 是否倒序
            limit: 返回结果数量
            offset: 分页偏移量

        Returns:
            消息列表
        """
        params = {'limit': limit, 'offset': offset, 'reverse': reverse}
        if talker_id:
            params['talker_id'] = talker_id
        if sender_id:
            params['sender_id'] = sender_id
        if keyword:
            params['keyword'] = keyword
        if time_range:
            params['time_range'] = time_range

        return self._request('GET', '/messages', params=params)

    # ==================== 联系人管理 ====================

    def get_contacts(self, keyword: Optional[str] = None,
                    limit: int = 50, offset: int = 0) -> List[Dict]:
        """
        获取联系人列表

        Args:
            keyword: 搜索关键词
            limit: 返回结果数量
            offset: 分页偏移量

        Returns:
            联系人列表
        """
        params = {'limit': limit, 'offset': offset}
        if keyword:
            params['keyword'] = keyword

        return self._request('GET', '/contacts', params=params)

    def get_contact(self, contact_id: str) -> Dict:
        """
        获取单个联系人

        Args:
            contact_id: 联系人用户名

        Returns:
            联系人信息
        """
        return self._request('GET', f'/contacts/{contact_id}')

    def get_need_contact(self, days: int = 7) -> List[Dict]:
        """
        获取需要跟进的联系人

        Args:
            days: 自上次联系以来的天数

        Returns:
            需要跟进的联系人列表
        """
        return self._request('GET', '/contacts/need-contact', params={'days': days})

    def export_contacts(self, format: str = 'csv',
                       keyword: Optional[str] = None) -> bytes:
        """
        导出联系人

        Args:
            format: 导出格式 ("csv" 或 "xlsx")
            keyword: 筛选关键词

        Returns:
            文件内容
        """
        params = {'format': format}
        if keyword:
            params['keyword'] = keyword

        return self._request('GET', '/contacts/export', params=params)

    # ==================== 群聊管理 ====================

    def get_chatrooms(self, keyword: Optional[str] = None,
                     limit: int = 50, offset: int = 0) -> List[Dict]:
        """
        获取群聊列表

        Args:
            keyword: 搜索关键词
            limit: 返回结果数量
            offset: 分页偏移量

        Returns:
            群聊列表
        """
        params = {'limit': limit, 'offset': offset}
        if keyword:
            params['keyword'] = keyword

        return self._request('GET', '/chatrooms', params=params)

    def get_chatroom(self, chatroom_id: str) -> Dict:
        """
        获取单个群聊

        Args:
            chatroom_id: 群聊 ID

        Returns:
            群聊信息
        """
        return self._request('GET', f'/chatrooms/{chatroom_id}')

    # ==================== 搜索功能 ====================

    def search(self, keyword: str,
              talker: Optional[str] = None,
              sender: Optional[str] = None,
              msg_type: Optional[int] = None,
              time_range: Optional[str] = None,
              limit: int = 50, offset: int = 0) -> Dict:
        """
        全文搜索

        Args:
            keyword: 搜索关键词
            talker: 会话用户名
            sender: 发送者用户名
            msg_type: 消息类型
            time_range: 时间范围
            limit: 返回结果数量
            offset: 分页偏移量

        Returns:
            搜索结果
        """
        params = {'keyword': keyword, 'limit': limit, 'offset': offset}
        if talker:
            params['talker'] = talker
        if sender:
            params['sender'] = sender
        if msg_type is not None:
            params['type'] = msg_type
        if time_range:
            params['time_range'] = time_range

        return self._request('GET', '/search', params=params)

    def get_search_context(self, talker: str, seq: int,
                          before: int = 10, after: int = 10) -> Dict:
        """
        获取搜索结果的上下文消息

        Args:
            talker: 会话用户名
            seq: 消息序列号
            before: 之前的消息数量
            after: 之后的消息数量

        Returns:
            上下文消息
        """
        params = {'talker': talker, 'seq': seq, 'before': before, 'after': after}
        return self._request('GET', '/search/context', params=params)

    # ==================== 总览数据 ====================

    def get_dashboard(self) -> Dict:
        """
        获取概览统计数据

        Returns:
            统计数据
        """
        return self._request('GET', '/dashboard')

    # ==================== 数据分析 ====================

    def get_hourly_analysis(self, session_id: str) -> List[Dict]:
        """
        获取每小时活跃度分布

        Args:
            session_id: 会话 ID

        Returns:
            每小时统计数据
        """
        return self._request('GET', f'/analysis/hourly/{session_id}')

    def get_daily_analysis(self, session_id: str) -> List[Dict]:
        """
        获取每日活跃度

        Args:
            session_id: 会话 ID

        Returns:
            每日统计数据
        """
        return self._request('GET', f'/analysis/daily/{session_id}')

    def get_weekday_analysis(self, session_id: str) -> List[Dict]:
        """
        获取星期活跃度分布

        Args:
            session_id: 会话 ID

        Returns:
            星期统计数据
        """
        return self._request('GET', f'/analysis/weekday/{session_id}')

    def get_monthly_analysis(self, session_id: str) -> List[Dict]:
        """
        获取月度活跃度

        Args:
            session_id: 会话 ID

        Returns:
            月度统计数据
        """
        return self._request('GET', f'/analysis/monthly/{session_id}')

    def get_type_distribution(self, session_id: str) -> List[Dict]:
        """
        获取消息类型分布

        Args:
            session_id: 会话 ID

        Returns:
            类型分布数据
        """
        return self._request('GET', f'/analysis/type_distribution/{session_id}')

    def get_member_activity(self, session_id: str) -> List[Dict]:
        """
        获取群聊成员活跃度

        Args:
            session_id: 会话 ID

        Returns:
            成员活跃度数据
        """
        return self._request('GET', f'/analysis/member_activity/{session_id}')

    def get_repeat_analysis(self, session_id: str) -> List[Dict]:
        """
        获取重复消息分析

        Args:
            session_id: 会话 ID

        Returns:
            重复消息数据
        """
        return self._request('GET', f'/analysis/repeat/{session_id}')

    def get_top_contacts(self) -> List[Dict]:
        """
        获取个人社交排行榜

        Returns:
            排行榜数据
        """
        return self._request('GET', '/analysis/personal/top_contacts')

    def get_annual_report(self, year: Optional[int] = None) -> Dict:
        """
        获取年度报告

        Args:
            year: 年份（默认当前年份）

        Returns:
            年度报告数据
        """
        params = {}
        if year:
            params['year'] = year

        return self._request('GET', '/report/annual', params=params)

    def get_global_wordcloud(self) -> List[Dict]:
        """
        获取全局词云数据

        Returns:
            词云数据
        """
        return self._request('GET', '/analysis/wordcloud/global')

    def get_wordcloud(self, session_id: str) -> List[Dict]:
        """
        获取特定会话的词云数据

        Args:
            session_id: 会话 ID

        Returns:
            词云数据
        """
        return self._request('GET', f'/analysis/wordcloud/{session_id}')

    # ==================== 数据导出 ====================

    def export_chat(self, talker: str,
                   name: Optional[str] = None,
                   time_range: Optional[str] = None,
                   format: str = 'html') -> bytes:
        """
        导出聊天记录

        Args:
            talker: 会话用户名
            name: 显示名称
            time_range: 时间范围
            format: 导出格式 ("html", "txt", "csv", "xlsx", "docx", "pdf")

        Returns:
            文件内容
        """
        params = {'talker': talker, 'format': format}
        if name:
            params['name'] = name
        if time_range:
            params['time_range'] = time_range

        return self._request('GET', '/export/chat', params=params)

    def export_forensic(self, talker: str,
                       name: Optional[str] = None,
                       time_range: Optional[str] = None) -> bytes:
        """
        导出取证记录

        Args:
            talker: 会话用户名
            name: 显示名称
            time_range: 时间范围

        Returns:
            ZIP 文件内容
        """
        params = {'talker': talker}
        if name:
            params['name'] = name
        if time_range:
            params['time_range'] = time_range

        return self._request('GET', '/export/forensic', params=params)

    def export_voices(self, talker: str,
                     time_range: Optional[str] = None) -> bytes:
        """
        导出语音消息

        Args:
            talker: 会话用户名
            time_range: 时间范围

        Returns:
            ZIP 文件内容
        """
        params = {'talker': talker}
        if time_range:
            params['time_range'] = time_range

        return self._request('GET', '/export/voices', params=params)


# ==================== 命令行接口 ====================

def print_json(data):
    """格式化输出 JSON"""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_sessions(args):
    """获取会话列表"""
    client = WetraceClient(args.base_url)
    sessions = client.get_sessions(
        keyword=args.keyword,
        limit=args.limit,
        offset=args.offset
    )
    print_json(sessions)


def cmd_messages(args):
    """获取消息列表"""
    client = WetraceClient(args.base_url)
    messages = client.get_messages(
        talker_id=args.talker,
        sender_id=args.sender,
        keyword=args.keyword,
        time_range=args.time_range,
        reverse=args.reverse,
        limit=args.limit,
        offset=args.offset
    )
    print_json(messages)


def cmd_contacts(args):
    """获取联系人列表"""
    client = WetraceClient(args.base_url)
    contacts = client.get_contacts(
        keyword=args.keyword,
        limit=args.limit,
        offset=args.offset
    )
    print_json(contacts)


def cmd_contact(args):
    """获取单个联系人"""
    client = WetraceClient(args.base_url)
    contact = client.get_contact(args.id)
    print_json(contact)


def cmd_need_contact(args):
    """获取需要跟进的联系人"""
    client = WetraceClient(args.base_url)
    contacts = client.get_need_contact(days=args.days)
    print_json(contacts)


def cmd_chatrooms(args):
    """获取群聊列表"""
    client = WetraceClient(args.base_url)
    chatrooms = client.get_chatrooms(
        keyword=args.keyword,
        limit=args.limit,
        offset=args.offset
    )
    print_json(chatrooms)


def cmd_chatroom(args):
    """获取单个群聊"""
    client = WetraceClient(args.base_url)
    chatroom = client.get_chatroom(args.id)
    print_json(chatroom)


def cmd_search(args):
    """全文搜索"""
    client = WetraceClient(args.base_url)
    results = client.search(
        keyword=args.keyword,
        talker=args.talker,
        sender=args.sender,
        msg_type=args.type,
        time_range=args.time_range,
        limit=args.limit,
        offset=args.offset
    )
    print_json(results)


def cmd_search_context(args):
    """获取搜索上下文"""
    client = WetraceClient(args.base_url)
    context = client.get_search_context(
        talker=args.talker,
        seq=args.seq,
        before=args.before,
        after=args.after
    )
    print_json(context)


def cmd_dashboard(args):
    """获取概览数据"""
    client = WetraceClient(args.base_url)
    dashboard = client.get_dashboard()
    print_json(dashboard)


def cmd_analysis(args):
    """数据分析"""
    client = WetraceClient(args.base_url)

    analysis_map = {
        'hourly': client.get_hourly_analysis,
        'daily': client.get_daily_analysis,
        'weekday': client.get_weekday_analysis,
        'monthly': client.get_monthly_analysis,
        'type': client.get_type_distribution,
        'member': client.get_member_activity,
        'repeat': client.get_repeat_analysis,
        'wordcloud': client.get_wordcloud,
    }

    if args.analysis_type == 'top_contacts':
        result = client.get_top_contacts()
    elif args.analysis_type == 'wordcloud_global':
        result = client.get_global_wordcloud()
    elif args.analysis_type == 'annual':
        result = client.get_annual_report(year=args.year)
    else:
        func = analysis_map.get(args.analysis_type)
        if not func:
            print(f"错误: 未知的分析类型 '{args.analysis_type}'")
            return
        result = func(args.session_id)

    print_json(result)


def cmd_export(args):
    """数据导出"""
    client = WetraceClient(args.base_url)

    if args.export_type == 'chat':
        data = client.export_chat(
            talker=args.talker,
            name=args.name,
            time_range=args.time_range,
            format=args.format
        )
    elif args.export_type == 'forensic':
        data = client.export_forensic(
            talker=args.talker,
            name=args.name,
            time_range=args.time_range
        )
    elif args.export_type == 'voices':
        data = client.export_voices(
            talker=args.talker,
            time_range=args.time_range
        )
    elif args.export_type == 'contacts':
        data = client.export_contacts(
            format=args.format,
            keyword=args.keyword
        )
    else:
        print(f"错误: 未知的导出类型 '{args.export_type}'")
        return

    # 保存文件
    import os
    output_dir = os.path.expanduser('~/wetrace-exports')
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{args.export_type}_{args.talker or 'export'}.{args.format}"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'wb') as f:
        f.write(data)

    print(f"文件已保存到: {filepath}")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Wetrace API 命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--base-url', default='http://127.0.0.1:5200/api/v1',
                       help='API 基础 URL')

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # sessions 命令
    p_sessions = subparsers.add_parser('sessions', help='获取会话列表')
    p_sessions.add_argument('--keyword', help='搜索关键词')
    p_sessions.add_argument('--limit', type=int, default=50, help='返回数量')
    p_sessions.add_argument('--offset', type=int, default=0, help='偏移量')
    p_sessions.set_defaults(func=cmd_sessions)

    # messages 命令
    p_messages = subparsers.add_parser('messages', help='获取消息列表')
    p_messages.add_argument('--talker', help='会话用户名')
    p_messages.add_argument('--sender', help='发送者用户名')
    p_messages.add_argument('--keyword', help='搜索关键词')
    p_messages.add_argument('--time-range', help='时间范围')
    p_messages.add_argument('--reverse', action='store_true', help='倒序')
    p_messages.add_argument('--limit', type=int, default=50, help='返回数量')
    p_messages.add_argument('--offset', type=int, default=0, help='偏移量')
    p_messages.set_defaults(func=cmd_messages)

    # contacts 命令
    p_contacts = subparsers.add_parser('contacts', help='获取联系人列表')
    p_contacts.add_argument('--keyword', help='搜索关键词')
    p_contacts.add_argument('--limit', type=int, default=50, help='返回数量')
    p_contacts.add_argument('--offset', type=int, default=0, help='偏移量')
    p_contacts.set_defaults(func=cmd_contacts)

    # contact 命令
    p_contact = subparsers.add_parser('contact', help='获取单个联系人')
    p_contact.add_argument('id', help='联系人用户名')
    p_contact.set_defaults(func=cmd_contact)

    # need-contact 命令
    p_need = subparsers.add_parser('need-contact', help='获取需要跟进的联系人')
    p_need.add_argument('--days', type=int, default=7, help='天数')
    p_need.set_defaults(func=cmd_need_contact)

    # chatrooms 命令
    p_chatrooms = subparsers.add_parser('chatrooms', help='获取群聊列表')
    p_chatrooms.add_argument('--keyword', help='搜索关键词')
    p_chatrooms.add_argument('--limit', type=int, default=50, help='返回数量')
    p_chatrooms.add_argument('--offset', type=int, default=0, help='偏移量')
    p_chatrooms.set_defaults(func=cmd_chatrooms)

    # chatroom 命令
    p_chatroom = subparsers.add_parser('chatroom', help='获取单个群聊')
    p_chatroom.add_argument('id', help='群聊 ID')
    p_chatroom.set_defaults(func=cmd_chatroom)

    # search 命令
    p_search = subparsers.add_parser('search', help='全文搜索')
    p_search.add_argument('--keyword', required=True, help='搜索关键词')
    p_search.add_argument('--talker', help='会话用户名')
    p_search.add_argument('--sender', help='发送者用户名')
    p_search.add_argument('--type', type=int, help='消息类型')
    p_search.add_argument('--time-range', help='时间范围')
    p_search.add_argument('--limit', type=int, default=50, help='返回数量')
    p_search.add_argument('--offset', type=int, default=0, help='偏移量')
    p_search.set_defaults(func=cmd_search)

    # search-context 命令
    p_context = subparsers.add_parser('search-context', help='获取搜索上下文')
    p_context.add_argument('--talker', required=True, help='会话用户名')
    p_context.add_argument('--seq', type=int, required=True, help='消息序列号')
    p_context.add_argument('--before', type=int, default=10, help='之前消息数')
    p_context.add_argument('--after', type=int, default=10, help='之后消息数')
    p_context.set_defaults(func=cmd_search_context)

    # dashboard 命令
    p_dashboard = subparsers.add_parser('dashboard', help='获取概览数据')
    p_dashboard.set_defaults(func=cmd_dashboard)

    # analysis 命令
    p_analysis = subparsers.add_parser('analysis', help='数据分析')
    p_analysis.add_argument('analysis_type',
                           choices=['hourly', 'daily', 'weekday', 'monthly',
                                   'type', 'member', 'repeat', 'wordcloud',
                                   'wordcloud_global', 'top_contacts', 'annual'],
                           help='分析类型')
    p_analysis.add_argument('session_id', nargs='?', help='会话 ID')
    p_analysis.add_argument('--year', type=int, help='年份（用于 annual）')
    p_analysis.set_defaults(func=cmd_analysis)

    # export 命令
    p_export = subparsers.add_parser('export', help='数据导出')
    p_export.add_argument('export_type',
                         choices=['chat', 'forensic', 'voices', 'contacts'],
                         help='导出类型')
    p_export.add_argument('--talker', help='会话用户名')
    p_export.add_argument('--name', help='显示名称')
    p_export.add_argument('--time-range', help='时间范围')
    p_export.add_argument('--format', default='html',
                         choices=['html', 'txt', 'csv', 'xlsx', 'docx', 'pdf'],
                         help='导出格式')
    p_export.add_argument('--keyword', help='搜索关键词（用于 contacts）')
    p_export.set_defaults(func=cmd_export)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        args.func(args)
    except Exception as e:
        print(f"错误: {e}")
        import sys
        sys.exit(1)


if __name__ == '__main__':
    main()
