# 智能摘要生成 Skill

## 触发关键词
- "总结聊天记录"
- "生成摘要"
- "智能总结"
- "summarize chat"
- "聊天总结"

## 功能描述
将指定会话的聊天记录转换为简洁的智能摘要，并生成精美的 HTML 页面供用户查看。

## API 依赖
- `GET /messages` - 获取消息数据
- `POST /ai/summarize` - AI 总结

## 工作流程

### 1. 参数收集
询问用户以下信息：
- **会话 ID** (talker_id): 必填，要总结的会话对象
- **时间范围** (time_range): 可选，格式如 "2024-01-01~2024-01-31"，默认为最近 30 天
- **消息数量限制** (limit): 可选，默认 1000 条

### 2. 数据获取
```javascript
// 调用 API 获取消息数据
GET /messages?talker_id={talker_id}&time_range={time_range}&limit={limit}

// 返回数据结构
{
  "data": [
    {
      "seq": 123456,
      "type": 1,
      "content": "消息内容",
      "sender": "wxid_xxx",
      "create_time": 1704067200,
      ...
    }
  ]
}
```

### 3. AI 总结
```javascript
// 调用 AI 总结 API
POST /ai/summarize
{
  "messages": [...], // 从步骤2获取的消息数据
  "max_length": 500  // 总结最大长度
}

// 返回数据结构
{
  "summary": "AI 生成的总结文本",
  "key_points": ["要点1", "要点2", "要点3"],
  "sentiment": "positive/neutral/negative"
}
```

### 4. HTML 页面生成

使用 page-best-practice 风格生成精美的 HTML 页面：

#### 4.1 页面结构
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>聊天记录智能摘要 - {{contact_name}}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    /* 基于 page-best-practice 的样式系统 */
    :root {
      --background: 0 0% 100%;
      --foreground: 222.2 84% 4.9%;
      --card: 0 0% 100%;
      --card-foreground: 222.2 84% 4.9%;
      --primary: 222.2 47.4% 11.2%;
      --primary-foreground: 210 40% 98%;
      --muted: 210 40% 96.1%;
      --muted-foreground: 215.4 16.3% 46.9%;
      --border: 214.3 31.8% 91.4%;
    }

    .card {
      background-color: hsl(var(--card));
      color: hsl(var(--card-foreground));
      border-radius: 0.5rem;
      border: 1px solid hsl(var(--border));
      box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }

    .badge {
      display: inline-flex;
      align-items: center;
      border-radius: 9999px;
      padding: 0.25rem 0.625rem;
      font-size: 0.75rem;
      font-weight: 600;
      transition: all 0.2s;
    }

    .badge-primary {
      background-color: hsl(var(--primary));
      color: hsl(var(--primary-foreground));
    }

    .badge-muted {
      background-color: hsl(var(--muted));
      color: hsl(var(--muted-foreground));
    }
  </style>
</head>
<body class="bg-background text-foreground antialiased">
  <div class="container mx-auto py-8 px-4 max-w-4xl">
    <!-- 页面头部 -->
    <div class="flex flex-col gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">聊天记录智能摘要</h1>
        <p class="text-muted-foreground mt-2">与 {{contact_name}} 的对话总结</p>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <span class="badge badge-muted">📅 {{date_range}}</span>
        <span class="badge badge-muted">💬 {{total_messages}} 条消息</span>
        <span class="badge badge-muted">⏱️ {{active_days}} 天活跃</span>
      </div>
    </div>

    <div class="separator mb-8"></div>

    <!-- 主要内容区域 -->
    <div class="space-y-6">
      <!-- AI 总结卡片 -->
      <div class="card p-6">
        <div class="mb-4">
          <h2 class="text-xl font-semibold flex items-center gap-2">
            <span>🤖</span>
            <span>AI 智能总结</span>
          </h2>
        </div>
        <div class="prose prose-sm max-w-none">
          <p class="text-foreground leading-relaxed">{{summary}}</p>
        </div>
      </div>

      <!-- 关键要点卡片 -->
      <div class="card p-6">
        <div class="mb-4">
          <h2 class="text-xl font-semibold flex items-center gap-2">
            <span>💡</span>
            <span>关键要点</span>
          </h2>
        </div>
        <ul class="space-y-2">
          {{#each key_points}}
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span class="text-foreground">{{this}}</span>
          </li>
          {{/each}}
        </ul>
      </div>

      <!-- 统计数据卡片 -->
      <div class="card p-6">
        <div class="mb-4">
          <h2 class="text-xl font-semibold flex items-center gap-2">
            <span>📊</span>
            <span>数据统计</span>
          </h2>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center">
            <div class="text-2xl font-bold text-primary">{{total_messages}}</div>
            <div class="text-sm text-muted-foreground">消息总数</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-primary">{{active_days}}</div>
            <div class="text-sm text-muted-foreground">活跃天数</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-primary">{{avg_per_day}}</div>
            <div class="text-sm text-muted-foreground">日均消息</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-primary">{{sentiment_emoji}}</div>
            <div class="text-sm text-muted-foreground">整体情感</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <div class="mt-12 text-center text-sm text-muted-foreground">
      <p>由 Wetrace AI 生成 • {{generation_time}}</p>
    </div>
  </div>
</body>
</html>
```

#### 4.2 数据填充逻辑
```javascript
// 填充模板变量
const templateData = {
  contact_name: "张三", // 从联系人信息获取
  date_range: "2024-01-01 至 2024-01-31",
  total_messages: 156,
  active_days: 28,
  avg_per_day: Math.round(156 / 28),
  summary: aiSummary.summary,
  key_points: aiSummary.key_points,
  sentiment_emoji: getSentimentEmoji(aiSummary.sentiment),
  generation_time: new Date().toLocaleString('zh-CN')
};

function getSentimentEmoji(sentiment) {
  const emojiMap = {
    'positive': '😊 积极',
    'neutral': '😐 中性',
    'negative': '😔 消极'
  };
  return emojiMap[sentiment] || '😐 中性';
}
```

### 5. 文件保存
```javascript
// 生成文件名
const fileName = `chat_summary_${talker_id}_${Date.now()}.html`;
const filePath = `~/wetrace-exports/${fileName}`;

// 保存 HTML 文件
fs.writeFileSync(filePath, htmlContent);

// 返回访问路径
return {
  success: true,
  file_path: filePath,
  preview_url: `file://${filePath}`
};
```

### 6. 输出格式

向用户展示：
```
✅ 聊天记录摘要已生成！

📊 统计信息：
- 会话对象：张三
- 时间范围：2024-01-01 至 2024-01-31
- 消息总数：156 条
- 活跃天数：28 天

🤖 AI 总结：
[显示总结的前 200 字...]

📄 HTML 页面已保存至：
~/wetrace-exports/chat_summary_wxid_xxx_1704067200.html

🔗 点击查看完整报告：
file:///Users/apple/wetrace-exports/chat_summary_wxid_xxx_1704067200.html
```

## 示例对话

**用户输入**：
```
总结我和张三最近一个月的聊天记录
```

**Skill 响应**：
```
好的，我来为您生成与张三的聊天记录摘要。

正在获取数据...
✓ 已获取 156 条消息
✓ 时间范围：2024-01-01 至 2024-01-31

正在使用 AI 分析...
✓ 总结生成完成

正在生成 HTML 页面...
✓ 页面生成完成

---

✅ 聊天记录摘要已生成！

📊 统计信息：
- 会话对象：张三
- 时间范围：2024-01-01 至 2024-01-31
- 消息总数：156 条
- 活跃天数：28 天
- 日均消息：5.6 条
- 整体情感：😊 积极

🤖 AI 总结：
本月与张三的沟通主要围绕项目进展和技术讨论。讨论了新功能的实现方案，
解决了几个技术难题。整体沟通顺畅，合作愉快。

💡 关键要点：
• 确定了新功能的技术方案
• 解决了数据库性能问题
• 约定了下周的项目评审时间

📄 完整报告已保存至：
~/wetrace-exports/chat_summary_zhangsan_20240131.html

🔗 在浏览器中打开查看完整报告
```

## 错误处理

### 1. API 调用失败
```
❌ 获取消息数据失败：网络连接超时
建议：请检查网络连接后重试
```

### 2. 会话不存在
```
❌ 未找到指定的会话
建议：请检查会话 ID 是否正确，或使用 /sessions 查看可用会话列表
```

### 3. 消息数据为空
```
⚠️ 指定时间范围内没有消息记录
建议：尝试扩大时间范围或选择其他会话
```

### 4. AI 总结失败
```
❌ AI 总结生成失败：服务暂时不可用
建议：稍后重试，或使用基础统计功能
```

## 技术要点

### 1. 响应式设计
- 使用 Tailwind CSS 的响应式类
- 移动端优先的设计理念
- 适配不同屏幕尺寸

### 2. 性能优化
- 限制消息数量避免过载
- 使用分页加载大量数据
- HTML 文件大小控制在 1MB 以内

### 3. 用户体验
- 清晰的进度提示
- 友好的错误信息
- 快速的页面加载

### 4. 数据安全
- 本地文件存储
- 不上传敏感信息
- 支持文件加密（可选）

## 扩展功能（未来）

- [ ] 支持多会话对比总结
- [ ] 导出为 PDF 格式
- [ ] 自定义总结长度和风格
- [ ] 支持语音播报总结内容
- [ ] 添加情感趋势图表
