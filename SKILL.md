---
name: wetrace
description: "微信聊天记录分析助手，用于查询、分析和导出本地微信数据库中的聊天数据。适用场景：(1) 查看与特定联系人或群组的聊天消息，(2) 通过关键词搜索跨会话消息，(3) 分析聊天模式、活跃度趋势或关系动态，(4) 导出多种格式的聊天记录（HTML/PDF/DOCX/CSV/XLSX），(5) 获取社交互动和沟通习惯的洞察，(6) 管理客户关系和跟进提醒，(7) 生成年度报告或统计数据，(8) 生成精美的可视化 HTML 页面。触发词：wetrace、微信、聊天记录、wechat、分析聊天、导出聊天、生成报告、生成仪表板，或任何涉及微信聊天数据分析、消息搜索或关系洞察的请求。"
---

# 微信数据分析助手

查询、分析和导出微信聊天数据，提供 AI 驱动的智能洞察和精美的可视化页面。

## 前置条件

- Wetrace 服务运行在 `http://127.0.0.1:5200`
- 微信数据库已解密并加载
- 如果服务未运行，先提示用户启动服务

## 核心工作流程

### 1. 理解用户意图

将用户请求分类为以下类别：

- **查询（Query）**：查看消息、会话、联系人、群聊
- **搜索（Search）**：通过关键词查找消息
- **分析（Analysis）**：分析模式、生成统计数据
- **导出（Export）**：导出多种格式的数据
- **洞察（Insight）**：综合分析并提供建议
- **可视化（Visualization）**：生成精美的 HTML 页面

### 2. 提取参数

从用户请求中识别关键参数：
- **联系人名称**：提取人名或群名
- **时间范围**：提取时间段
- **关键词**：提取搜索词
- **格式**：提取导出格式

### 3. 调用 API

使用 WebFetch 工具调用 Wetrace API。基础 URL：`http://127.0.0.1:5200/api/v1`

**完整 API 文档**：参考 [references/api.md](references/api.md)

#### 常用 API 模式

```
GET /sessions?keyword={名称}&limit=50
GET /messages?talker_id={id}&time_range={范围}&limit=100
GET /search?keyword={关键词}&time_range={范围}&limit=50
GET /analysis/hourly/{session_id}
GET /analysis/daily/{session_id}
GET /export/chat?talker={id}&format={格式}&time_range={范围}
```

### 4. 处理和呈现数据

#### 简单查询/搜索

以清晰、结构化的格式呈现数据。

#### 分析任务

1. 从分析 API 获取原始数据
2. 使用 [references/analysis-prompts.md](references/analysis-prompts.md) 中的模板生成 AI 总结
3. 以清晰的结构呈现

#### 导出任务

调用导出 API，告知用户下载信息。

#### 洞察任务

1. 从多个 API 收集数据
2. 综合信息
3. 生成全面的洞察和建议
4. 使用 analysis-prompts.md 中的适当模板

### 5. 错误处理

- **API 返回 404**：数据库可能未加载，联系人/会话可能不存在
- **API 返回 500**：服务器错误，建议检查日志
- **无数据返回**：验证时间范围和联系人名称
- **服务器无响应**：提示用户启动 Wetrace 服务

## 🎨 智能网页生成功能

Wetrace 提供 8 个核心可视化功能，每个功能都会：
1. 调用 Wetrace API 获取数据
2. 使用 AI 分析生成总结
3. 使用统一的设计系统生成精美的 HTML 页面
4. 保存 HTML 文件到 `~/wetrace-exports/` 并提供访问链接

### 可用的可视化功能

当用户请求生成可视化页面时，根据触发关键词选择对应的功能：

1. **智能摘要生成** - 触发词：总结聊天记录、生成摘要、智能总结
   - 详见 [references/01-smart-summary.md](references/01-smart-summary.md)

2. **待办事项提取** - 触发词：提取待办、找出任务、待办事项
   - 详见 [references/02-todo-extraction.md](references/02-todo-extraction.md)

3. **聊天活跃度热力图** - 触发词：活跃度热力图、聊天时间分布
   - 详见 [references/03-activity-heatmap.md](references/03-activity-heatmap.md)

4. **互动趋势分析** - 触发词：趋势分析、互动趋势
   - 详见 [references/04-trend-analysis.md](references/04-trend-analysis.md)

5. **智能周报月报** - 触发词：生成周报、生成月报
   - 详见 [references/05-weekly-monthly-report.md](references/05-weekly-monthly-report.md)

6. **数据仪表板** - 触发词：生成仪表板、数据总览
   - 详见 [references/06-dashboard.md](references/06-dashboard.md)

7. **智能对话摘要** - 触发词：对话摘要、智能总结、分类摘要
   - 详见 [references/07-conversation-summary.md](references/07-conversation-summary.md)

8. **客户关系健康度** - 触发词：客户健康度、CRM 仪表板
   - 详见 [references/08-customer-health.md](references/08-customer-health.md)

### 设计系统

所有生成的 HTML 页面都遵循统一的设计系统，详见 [references/design-system.md](references/design-system.md)，包括：
- 颜色系统：基于 HSL 的 CSS 变量
- 组件库：Card、Badge、Button、Separator、Input 等
- 布局系统：响应式容器和统一间距
- 数据可视化：Chart.js 配置和颜色方案

### HTML 页面特点

所有生成的 HTML 页面：
- ✅ **独立运行**：无需服务器，双击即可在浏览器打开
- ✅ **响应式设计**：适配所有设备（桌面/平板/手机）
- ✅ **现代化样式**：使用 Tailwind CSS
- ✅ **交互式图表**：使用 Chart.js 实现数据可视化
- ✅ **清晰层次**：卡片布局、统一间距、语义化颜色
- ✅ **易于分享**：可直接发送给他人查看

### 使用流程

当用户请求生成网页时：

1. **识别功能**：根据触发关键词匹配对应的功能
2. **读取详细文档**：从 references 目录读取对应的 .md 文件
3. **收集参数**：询问用户必要的参数（会话 ID、时间范围等）
4. **调用 API**：获取所需数据
5. **AI 分析**：使用 analysis-prompts.md 中的模板生成总结
6. **生成 HTML**：使用 design-system.md 风格生成精美页面
7. **保存文件**：保存到 `~/wetrace-exports/` 目录
8. **提供链接**：返回文件路径和访问链接

## 高级功能

### 时间范围解析

支持多种格式：
- 中文：最近一周、上个月、今年
- 英文：last week、last month、this year
- 绝对时间：2024-01-01~2024-01-31
- 相对天数：last 7 days、last 30 days

转换为 API 格式：`YYYY-MM-DD~YYYY-MM-DD`

### 联系人名称匹配

1. 首先在会话中尝试精确匹配
2. 如未找到，在联系人中搜索
3. 如有多个匹配，请用户明确
4. 同时支持昵称（NickName）和备注（Remark）字段

### 分页策略

对于大数据集：
1. 从 `limit=50` 开始
2. 如用户需要更多，增加 limit 或使用 offset
3. 告知用户总数
4. 如数据集非常大，建议导出

## 使用提示

- 调用 API 前始终验证服务器是否运行
- 使用适当的分析模板以保持输出一致性
- 提供可操作的洞察，而不仅仅是原始统计数据
- 尊重用户隐私 - 不要对关系做出假设
- 提供后续步骤或跟进行动
- 同等处理中文和英文查询
- **生成 HTML 页面时**：始终参考 design-system.md 的设计系统
- **文件保存位置**：统一保存到 `~/wetrace-exports/` 目录
- **提供访问链接**：生成完成后提供 `file://` 协议的完整路径
