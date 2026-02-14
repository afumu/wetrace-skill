# 智能对话摘要生成器 Skill

## 触发关键词
- "对话摘要"
- "智能总结"
- "conversation summary"
- "分类摘要"
- "对话分析"

## 功能描述
使用 AI 对聊天记录进行智能分类和总结，自动提取待办事项、重要决策和关键信息。

## API 依赖
- `GET /messages` - 获取消息数据
- `GET /search/context` - 获取上下文消息
- `POST /ai/summarize` - AI 总结
- `POST /ai/extract-todos` - 待办提取
- `POST /ai/extract-info` - 信息提取

## 工作流程

### 1. 参数收集
- **会话 ID** (talker_id): 必填
- **时间范围** (time_range): 可选，默认最近 7 天
- **分类模式** (mode): "auto" 或 "custom"

### 2. 数据获取与分析
```javascript
// 1. 获取消息
GET /messages?talker_id={talker_id}&time_range={time_range}

// 2. AI 分类总结
POST /ai/summarize
{
  "messages": [...],
  "categorize": true,
  "extract_key_points": true
}

// 3. 提取待办事项
POST /ai/extract-todos

// 4. 提取关键信息
POST /ai/extract-info
{
  "extract_types": ["address", "time", "amount", "contact"]
}
```

### 3. HTML 页面生成

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>智能对话摘要 - {{contact_name}}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {
      --background: 0 0% 100%;
      --foreground: 222.2 84% 4.9%;
      --card: 0 0% 100%;
      --primary: 222.2 47.4% 11.2%;
      --muted: 210 40% 96.1%;
      --border: 214.3 31.8% 91.4%;
    }

    .card {
      background-color: hsl(var(--card));
      border-radius: 0.5rem;
      border: 1px solid hsl(var(--border));
      box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }

    .category-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.5rem 1rem;
      border-radius: 0.5rem;
      font-weight: 600;
      font-size: 0.875rem;
    }

    .category-work {
      background: #dbeafe;
      color: #1e40af;
    }

    .category-life {
      background: #fef3c7;
      color: #92400e;
    }

    .category-decision {
      background: #fce7f3;
      color: #9f1239;
    }

    .category-todo {
      background: #dcfce7;
      color: #166534;
    }

    .info-item {
      display: flex;
      align-items: start;
      gap: 0.75rem;
      padding: 0.75rem;
      border-radius: 0.375rem;
      background: hsl(var(--muted));
    }
  </style>
</head>
<body class="bg-background text-foreground antialiased">
  <div class="container mx-auto py-8 px-4 max-w-5xl">
    <!-- 页面头部 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold tracking-tight mb-2">🤖 智能对话摘要</h1>
      <p class="text-muted-foreground">与 {{contact_name}} 的对话分析</p>
      <div class="mt-4 flex items-center gap-2 flex-wrap">
        <span class="badge">📅 {{date_range}}</span>
        <span class="badge">💬 {{total_messages}} 条消息</span>
        <span class="badge">📋 {{total_categories}} 个分类</span>
      </div>
    </div>

    <!-- 分类导航 -->
    <div class="flex gap-3 mb-8 overflow-x-auto pb-2">
      <button class="category-badge category-work" onclick="scrollToCategory('work')">
        💼 工作讨论 ({{work_count}})
      </button>
      <button class="category-badge category-life" onclick="scrollToCategory('life')">
        🏠 日常闲聊 ({{life_count}})
      </button>
      <button class="category-badge category-decision" onclick="scrollToCategory('decision')">
        ⚡ 重要决策 ({{decision_count}})
      </button>
      <button class="category-badge category-todo" onclick="scrollToCategory('todo')">
        ✅ 待办事项 ({{todo_count}})
      </button>
    </div>

    <!-- 工作讨论 -->
    <div id="work" class="card p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4 flex items-center gap-2">
        <span>💼</span>
        <span>工作讨论</span>
      </h2>
      <div class="prose prose-sm max-w-none mb-4">
        <p class="text-foreground leading-relaxed">{{work_summary}}</p>
      </div>
      <div class="space-y-2">
        <h3 class="font-semibold text-sm text-muted-foreground">关键要点：</h3>
        <ul class="space-y-1">
          {{#each work_key_points}}
          <li class="flex items-start gap-2">
            <span class="text-primary mt-1">•</span>
            <span>{{this}}</span>
          </li>
          {{/each}}
        </ul>
      </div>
    </div>

    <!-- 日常闲聊 -->
    <div id="life" class="card p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4 flex items-center gap-2">
        <span>🏠</span>
        <span>日常闲聊</span>
      </h2>
      <div class="prose prose-sm max-w-none">
        <p class="text-foreground leading-relaxed">{{life_summary}}</p>
      </div>
    </div>

    <!-- 重要决策 -->
    <div id="decision" class="card p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4 flex items-center gap-2">
        <span>⚡</span>
        <span>重要决策</span>
      </h2>
      <div class="space-y-4">
        {{#each decisions}}
        <div class="p-4 border border-border rounded">
          <div class="font-semibold text-foreground mb-2">{{title}}</div>
          <div class="text-sm text-muted-foreground mb-2">{{description}}</div>
          <div class="text-xs text-muted-foreground">📅 {{date}}</div>
        </div>
        {{/each}}
      </div>
    </div>

    <!-- 待办事项 -->
    <div id="todo" class="card p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4 flex items-center gap-2">
        <span>✅</span>
        <span>待办事项清单</span>
      </h2>
      <div class="space-y-3">
        {{#each todos}}
        <div class="flex items-start gap-3 p-3 border border-border rounded">
          <input type="checkbox" class="mt-1 w-5 h-5">
          <div class="flex-1">
            <div class="font-medium">{{content}}</div>
            {{#if deadline}}
            <div class="text-sm text-muted-foreground mt-1">⏰ {{deadline}}</div>
            {{/if}}
          </div>
        </div>
        {{/each}}
      </div>
    </div>

    <!-- 关键信息提取 -->
    <div class="card p-6">
      <h2 class="text-2xl font-semibold mb-4 flex items-center gap-2">
        <span>📌</span>
        <span>关键信息</span>
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- 时间信息 -->
        {{#if time_info}}
        <div>
          <h3 class="font-semibold mb-2 text-sm text-muted-foreground">⏰ 时间信息</h3>
          <div class="space-y-2">
            {{#each time_info}}
            <div class="info-item">
              <span>{{this}}</span>
            </div>
            {{/each}}
          </div>
        </div>
        {{/if}}

        <!-- 地址信息 -->
        {{#if address_info}}
        <div>
          <h3 class="font-semibold mb-2 text-sm text-muted-foreground">📍 地址信息</h3>
          <div class="space-y-2">
            {{#each address_info}}
            <div class="info-item">
              <span>{{this}}</span>
            </div>
            {{/each}}
          </div>
        </div>
        {{/if}}

        <!-- 金额信息 -->
        {{#if amount_info}}
        <div>
          <h3 class="font-semibold mb-2 text-sm text-muted-foreground">💰 金额信息</h3>
          <div class="space-y-2">
            {{#each amount_info}}
            <div class="info-item">
              <span>{{this}}</span>
            </div>
            {{/each}}
          </div>
        </div>
        {{/if}}

        <!-- 联系方式 -->
        {{#if contact_info}}
        <div>
          <h3 class="font-semibold mb-2 text-sm text-muted-foreground">📞 联系方式</h3>
          <div class="space-y-2">
            {{#each contact_info}}
            <div class="info-item">
              <span>{{this}}</span>
            </div>
            {{/each}}
          </div>
        </div>
        {{/if}}
      </div>
    </div>

    <!-- 页脚 -->
    <div class="mt-12 text-center text-sm text-muted-foreground">
      <p>由 Wetrace AI 生成 • {{generation_time}}</p>
    </div>
  </div>

  <script>
    function scrollToCategory(id) {
      document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
    }
  </script>
</body>
</html>
```

## 输出格式

```
✅ 智能对话摘要已生成！

📊 分类统计：
- 工作讨论：45 条
- 日常闲聊：23 条
- 重要决策：8 条
- 待办事项：12 条

💼 工作讨论摘要：
主要讨论了项目进展和技术方案，确定了下一步的开发计划...

⚡ 重要决策：
1. 采用新的技术架构
2. 调整项目时间表
3. 增加团队成员

✅ 待办事项：12 个任务待完成

📄 完整摘要已保存至：
~/wetrace-exports/conversation_summary_zhangsan_20240131.html
```

## 技术要点

### 1. 智能分类
- AI 自动识别对话类型
- 多维度分类标签
- 关键信息提取

### 2. 结构化输出
- 分类导航
- 可折叠内容
- 交互式待办清单

### 3. 信息提取
- 时间、地址、金额
- 联系方式
- 关键决策点

## 扩展功能（未来）

- [ ] 自定义分类规则
- [ ] 导出为 Markdown
- [ ] 关键词高亮
- [ ] 对话时间线视图
