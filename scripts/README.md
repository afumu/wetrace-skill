# Wetrace API 脚本使用指南

这是一个无依赖的 Python 脚本，用于调用 Wetrace API。使用 Python 标准库实现，无需安装任何第三方包。

## 快速开始

```bash
# 查看帮助
python3 scripts/wetrace_api.py --help

# 查看具体命令的帮助
python3 scripts/wetrace_api.py sessions --help
```

## 常用命令

### 1. 会话管理

```bash
# 获取所有会话
python3 scripts/wetrace_api.py sessions

# 搜索会话
python3 scripts/wetrace_api.py sessions --keyword "张三" --limit 20
```

### 2. 消息查询

```bash
# 获取某个会话的消息
python3 scripts/wetrace_api.py messages --talker wxid_abc123 --limit 100

# 按时间范围查询
python3 scripts/wetrace_api.py messages --talker wxid_abc123 --time-range "2024-01-01~2024-01-31"

# 搜索消息中的关键词
python3 scripts/wetrace_api.py messages --talker wxid_abc123 --keyword "项目"
```

### 3. 联系人管理

```bash
# 获取所有联系人
python3 scripts/wetrace_api.py contacts

# 搜索联系人
python3 scripts/wetrace_api.py contacts --keyword "张三"

# 获取单个联系人详情
python3 scripts/wetrace_api.py contact wxid_abc123

# 获取需要跟进的联系人（7天未联系）
python3 scripts/wetrace_api.py need-contact --days 7
```

### 4. 群聊管理

```bash
# 获取所有群聊
python3 scripts/wetrace_api.py chatrooms

# 搜索群聊
python3 scripts/wetrace_api.py chatrooms --keyword "项目组"

# 获取单个群聊详情
python3 scripts/wetrace_api.py chatroom 12345678@chatroom
```

### 5. 全文搜索

```bash
# 搜索关键词
python3 scripts/wetrace_api.py search --keyword "项目"

# 在特定会话中搜索
python3 scripts/wetrace_api.py search --keyword "项目" --talker wxid_abc123

# 按时间范围搜索
python3 scripts/wetrace_api.py search --keyword "项目" --time-range "last_week"

# 获取搜索结果的上下文
python3 scripts/wetrace_api.py search-context --talker wxid_abc123 --seq 123456789
```

### 6. 数据分析

```bash
# 获取概览数据
python3 scripts/wetrace_api.py dashboard

# 每小时活跃度分析
python3 scripts/wetrace_api.py analysis hourly wxid_abc123

# 每日活跃度分析
python3 scripts/wetrace_api.py analysis daily wxid_abc123

# 星期活跃度分析
python3 scripts/wetrace_api.py analysis weekday wxid_abc123

# 月度活跃度分析
python3 scripts/wetrace_api.py analysis monthly wxid_abc123

# 消息类型分布
python3 scripts/wetrace_api.py analysis type wxid_abc123

# 群成员活跃度
python3 scripts/wetrace_api.py analysis member 12345678@chatroom

# 重复消息分析
python3 scripts/wetrace_api.py analysis repeat wxid_abc123

# 词云数据
python3 scripts/wetrace_api.py analysis wordcloud wxid_abc123
python3 scripts/wetrace_api.py analysis wordcloud_global

# 社交排行榜
python3 scripts/wetrace_api.py analysis top_contacts

# 年度报告
python3 scripts/wetrace_api.py analysis annual --year 2024
```

### 7. 数据导出

```bash
# 导出聊天记录为 HTML
python3 scripts/wetrace_api.py export chat --talker wxid_abc123 --format html

# 导出为 PDF
python3 scripts/wetrace_api.py export chat --talker wxid_abc123 --format pdf

# 导出为 Word 文档
python3 scripts/wetrace_api.py export chat --talker wxid_abc123 --format docx

# 导出为 Excel
python3 scripts/wetrace_api.py export chat --talker wxid_abc123 --format xlsx

# 导出取证记录
python3 scripts/wetrace_api.py export forensic --talker wxid_abc123

# 导出语音消息
python3 scripts/wetrace_api.py export voices --talker wxid_abc123

# 导出联系人
python3 scripts/wetrace_api.py export contacts --format csv
```

## 在代码中使用

你也可以在 Python 代码中导入使用：

```python
import sys
sys.path.append('scripts')
from wetrace_api import WetraceClient

# 创建客户端
client = WetraceClient()

# 获取会话列表
sessions = client.get_sessions(keyword="张三", limit=10)
for session in sessions:
    print(f"{session['NickName']}: {session['MessageCount']} 条消息")

# 搜索消息
results = client.search(keyword="项目", limit=20)
print(f"找到 {results['Total']} 条消息")

# 获取分析数据
hourly = client.get_hourly_analysis("wxid_abc123")
for item in hourly:
    print(f"{item['Hour']}时: {item['Count']} 条消息")
```

## 时间范围格式

支持多种时间范围格式：

- **绝对时间**: `2024-01-01~2024-01-31`
- **相对时间**: `last_week`, `last_month`, `last_year`
- **天数**: `last_7_days`, `last_30_days`

## 输出格式

所有命令默认输出 JSON 格式，方便解析和处理。

## 自定义 API 地址

如果 Wetrace 服务运行在其他地址，可以使用 `--base-url` 参数：

```bash
python3 scripts/wetrace_api.py --base-url http://192.168.1.100:5200/api/v1 sessions
```

## 错误处理

脚本会自动处理常见错误：
- 连接失败：检查 Wetrace 服务是否运行
- HTTP 404：资源不存在
- HTTP 500：服务器错误

错误信息会以友好的格式输出。
