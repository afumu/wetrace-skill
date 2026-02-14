# Wetrace API 参考文档

基础 URL：`http://127.0.0.1:5200/api/v1`

## 目录

- [会话管理](#会话管理)
- [消息查询](#消息查询)
- [联系人管理](#联系人管理)
- [群聊管理](#群聊管理)
- [搜索功能](#搜索功能)
- [总览数据](#总览数据)
- [数据分析](#数据分析)
- [数据导出](#数据导出)
- [通用参数](#通用参数)

---

## 会话管理

### GET /sessions
获取聊天会话列表。

**查询参数：**
- `keyword`（字符串，可选）：会话名称搜索关键词
- `limit`（整数，可选）：返回结果数量（默认：50）
- `offset`（整数，可选）：分页偏移量（默认：0）

**响应示例：**
```json
[
  {
    "UserName": "wxid_abc123",
    "NickName": "张三",
    "Remark": "同事",
    "LastMessageTime": 1704067200,
    "MessageCount": 1234,
    "UnreadCount": 5
  }
]
```

### DELETE /sessions/:id
根据用户名删除会话。

**路径参数：**
- `id`（字符串，必需）：会话用户名（如："wxid_abc123"）

---

## 消息查询

### GET /messages
获取特定会话的消息或执行全局搜索。

**查询参数：**
- `talker_id`（字符串，可选）：会话用户名。如果为空且有 keyword，则执行全局搜索
- `sender_id`（字符串，可选）：按发送者用户名筛选
- `keyword`（字符串，可选）：在消息内容中搜索关键词
- `time_range`（字符串，可选）：格式 "2024-01-01~2024-01-31" 或 "last_week"、"last_month"
- `reverse`（布尔值，可选）：倒序排列（默认：false）
- `limit`（整数，可选）：返回结果数量（默认：50）
- `offset`（整数，可选）：分页偏移量（默认：0）

**响应示例：**
```json
[
  {
    "Seq": 123456789,
    "MsgSvrID": 987654321,
    "Type": 1,
    "SubType": 0,
    "IsSender": 1,
    "CreateTime": 1704067200,
    "Talker": "wxid_abc123",
    "Content": "你好世界",
    "CompressContent": "",
    "BytesExtra": ""
  }
]
```

**消息类型：**
- `1`：文本
- `3`：图片
- `34`：语音
- `43`：视频
- `47`：表情包/贴纸
- `49`：链接/文件
- `10000`：系统消息

---

## 联系人管理

### GET /contacts
获取联系人列表。

**查询参数：**
- `keyword`（字符串，可选）：搜索关键词
- `limit`（整数，可选）：返回结果数量（默认：50）
- `offset`（整数，可选）：分页偏移量（默认：0）

**响应示例：**
```json
[
  {
    "UserName": "wxid_abc123",
    "Alias": "zhangsan",
    "NickName": "张三",
    "Remark": "同事",
    "IsFriend": true,
    "Type": 3
  }
]
```

### GET /contacts/:id
根据用户名获取单个联系人。

### GET /contacts/need-contact
获取需要跟进的联系人。

**查询参数：**
- `days`（整数，可选）：自上次联系以来的天数（默认：7）

**响应示例：**
```json
[
  {
    "UserName": "wxid_abc123",
    "NickName": "张三",
    "Remark": "客户",
    "LastContactTime": 1704067200,
    "DaysSinceContact": 15,
    "MessageCount": 234
  }
]
```

### GET /contacts/export
导出联系人为 CSV 或 XLSX 格式。

**查询参数：**
- `format`（字符串，可选）："csv" 或 "xlsx"（默认："csv"）
- `keyword`（字符串，可选）：筛选关键词

---

## 群聊管理

### GET /chatrooms
获取群聊（群组聊天）列表。

**查询参数：**
- `keyword`（字符串，可选）：搜索关键词
- `limit`（整数，可选）：返回结果数量（默认：50）
- `offset`（整数，可选）：分页偏移量（默认：0）

**响应示例：**
```json
[
  {
    "ChatRoomName": "12345678@chatroom",
    "DisplayName": "项目讨论组",
    "MemberCount": 15,
    "Members": "wxid_1;wxid_2;wxid_3"
  }
]
```

### GET /chatrooms/:id
根据 ID 获取单个群聊。

---

## 搜索功能

### GET /search
跨所有消息进行全文搜索。

**查询参数：**
- `keyword`（字符串，必需）：搜索关键词
- `talker`（字符串，可选）：按会话用户名筛选
- `sender`（字符串，可选）：按发送者用户名筛选
- `type`（整数，可选）：按消息类型筛选
- `time_range`（字符串，可选）：时间范围筛选
- `limit`（整数，可选）：返回结果数量（默认：50）
- `offset`（整数，可选）：分页偏移量（默认：0）

**响应示例：**
```json
{
  "Items": [
    {
      "Seq": 123456789,
      "Talker": "wxid_abc123",
      "TalkerName": "张三",
      "Content": "项目进度如何？",
      "Highlight": "<em>项目</em>进度如何？",
      "CreateTime": 1704067200,
      "Type": 1
    }
  ],
  "Total": 156,
  "HasMore": true
}
```

### GET /search/context
获取搜索结果周围的上下文消息。

**查询参数：**
- `talker`（字符串，必需）：会话用户名
- `seq`（int64，必需）：消息序列号
- `before`（整数，可选）：之前的消息数量（默认：10）
- `after`（整数，可选）：之后的消息数量（默认：10）

**响应示例：**
```json
{
  "messages": [...],
  "anchor_index": 10
}
```

---

## 总览数据

### GET /dashboard
获取概览统计数据。

**响应示例：**
```json
{
  "TotalMessages": 123456,
  "TotalContacts": 234,
  "TotalSessions": 189,
  "TotalChatrooms": 45,
  "RecentActivity": [...]
}
```

---

## 数据分析

所有分析端点返回特定会话的统计数据。

### GET /analysis/hourly/:id
每小时活跃度分布（0-23 小时）。

**响应示例：**
```json
[
  {"Hour": 0, "Count": 12},
  {"Hour": 1, "Count": 5},
  ...
  {"Hour": 23, "Count": 18}
]
```

### GET /analysis/daily/:id
每日活跃度随时间变化。

**响应示例：**
```json
[
  {"Date": "2024-01-01", "Count": 45},
  {"Date": "2024-01-02", "Count": 67},
  ...
]
```

### GET /analysis/weekday/:id
星期活跃度分布（0=周日，6=周六）。

**响应示例：**
```json
[
  {"Weekday": 0, "Count": 123},
  {"Weekday": 1, "Count": 234},
  ...
]
```

### GET /analysis/monthly/:id
月度活跃度分布。

**响应示例：**
```json
[
  {"Month": "2024-01", "Count": 456},
  {"Month": "2024-02", "Count": 567},
  ...
]
```

### GET /analysis/type_distribution/:id
消息类型分布。

**响应示例：**
```json
[
  {"Type": 1, "TypeName": "文本", "Count": 1234, "Percentage": 78.5},
  {"Type": 3, "TypeName": "图片", "Count": 234, "Percentage": 14.9},
  {"Type": 34, "TypeName": "语音", "Count": 56, "Percentage": 3.6},
  ...
]
```

### GET /analysis/member_activity/:id
群聊中的成员活跃度。

**响应示例：**
```json
[
  {
    "UserName": "wxid_abc123",
    "NickName": "张三",
    "MessageCount": 456,
    "Percentage": 23.4
  },
  ...
]
```

### GET /analysis/repeat/:id
重复消息分析。

**响应示例：**
```json
[
  {
    "Content": "+1",
    "Count": 45,
    "Users": ["张三", "李四", "王五"]
  },
  ...
]
```

### GET /analysis/personal/top_contacts
个人社交排行榜（按消息数量排名的前几位联系人）。

**响应示例：**
```json
[
  {
    "UserName": "wxid_abc123",
    "NickName": "张三",
    "Remark": "同事",
    "MessageCount": 5678,
    "Rank": 1
  },
  ...
]
```

### GET /report/annual
年度报告，包含综合统计数据。

**查询参数：**
- `year`（整数，可选）：年份（默认：当前年份）

**响应示例：**
```json
{
  "Year": 2024,
  "TotalMessages": 123456,
  "TotalDays": 365,
  "TopContacts": [...],
  "MostActiveMonth": "2024-03",
  "MostActiveHour": 20,
  "MessageTypeStats": [...],
  "MonthlyTrend": [...]
}
```

### GET /analysis/wordcloud/global
全局词云数据。

**响应示例：**
```json
[
  {"Word": "项目", "Count": 234},
  {"Word": "会议", "Count": 189},
  ...
]
```

### GET /analysis/wordcloud/:id
特定会话的词云数据。

---

## 数据导出

### GET /export/chat
以多种格式导出聊天记录。

**查询参数：**
- `talker`（字符串，必需）：会话用户名
- `name`（字符串，可选）：导出时显示的名称
- `time_range`（字符串，可选）：时间范围筛选
- `format`（字符串，可选）：导出格式
  - `html`（默认）：带嵌入媒体的 HTML（ZIP）
  - `txt`：纯文本
  - `csv`：CSV 格式
  - `xlsx`：Excel 格式
  - `docx`：Word 文档
  - `pdf`：PDF 文档

**响应：** 文件下载（内容类型因格式而异）

### GET /export/forensic
导出用于法律/取证目的的记录，带水印和完整性验证。

**查询参数：**
- `talker`（字符串，必需）：会话用户名
- `name`（字符串，可选）：显示名称
- `time_range`（字符串，可选）：时间范围筛选

**响应：** 包含 HTML 报告和验证数据的 ZIP 文件

### GET /export/voices
导出语音消息。

**查询参数：**
- `talker`（字符串，必需）：会话用户名
- `time_range`（字符串，可选）：时间范围筛选

**响应：** 包含语音文件的 ZIP 文件

---

## 通用参数

### 时间范围格式

支持多种格式：
- **绝对时间**：`"2024-01-01~2024-01-31"`
- **相对时间**：`"last_week"`、`"last_month"`、`"last_year"`
- **天数**：`"last_7_days"`、`"last_30_days"`

### 分页

大多数列表端点支持：
- `limit`：每页结果数量（默认：50，最大：1000）
- `offset`：跳过 N 个结果（用于分页）

### 错误响应

所有端点可能返回：
- `400 Bad Request`：无效参数
- `404 Not Found`：资源未找到
- `500 Internal Server Error`：服务器错误

错误格式：
```json
{
  "error": "错误消息描述"
}
```
