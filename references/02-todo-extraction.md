# 待办事项提取 Skill

## 触发关键词
- "提取待办"
- "找出任务"
- "待办事项"
- "extract todos"
- "任务清单"
- "todo list"

## 功能描述
从聊天记录中自动提取待办事项和任务，生成结构化的任务清单 HTML 页面。

## API 依赖
- `GET /messages` - 获取消息数据
- `POST /ai/extract-todos` - AI 提取待办事项

## 工作流程

### 1. 参数收集
- **会话 ID** (talker_id): 必填
- **时间范围** (time_range): 可选，默认最近 30 天
- **消息数量** (limit): 可选，默认 1000 条

### 2. 数据获取与分析
```javascript
// 1. 获取消息
GET /messages?talker_id={talker_id}&time_range={time_range}&limit={limit}

// 2. 提取待办事项
POST /ai/extract-todos
{
  "messages": [...],
  "extract_deadline": true,
  "extract_assignee": true
}

// 返回数据结构
{
  "todos": [
    {
      "content": "完成项目文档",
      "deadline": "2024-01-31",
      "assignee": "张三",
      "priority": "high",
      "status": "pending",
      "source_message": "记得在月底前完成项目文档"
    }
  ]
}
```

### 3. HTML 页面生成

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>待办事项清单 - {{contact_name}}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {
      --background: 0 0% 100%;
      --foreground: 222.2 84% 4.9%;
      --card: 0 0% 100%;
      --primary: 222.2 47.4% 11.2%;
      --muted: 210 40% 96.1%;
      --muted-foreground: 215.4 16.3% 46.9%;
      --border: 214.3 31.8% 91.4%;
      --destructive: 0 84.2% 60.2%;
      --warning: 38 92% 50%;
      --success: 142 76% 36%;
    }

    .card {
      background-color: hsl(var(--card));
      border-radius: 0.5rem;
      border: 1px solid hsl(var(--border));
      box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }

    .todo-item {
      padding: 1rem;
      border-bottom: 1px solid hsl(var(--border));
      transition: background-color 0.2s;
    }

    .todo-item:hover {
      background-color: hsl(var(--muted));
    }

    .todo-item:last-child {
      border-bottom: none;
    }

    .priority-high {
      border-left: 4px solid hsl(var(--destructive));
    }

    .priority-medium {
      border-left: 4px solid hsl(var(--warning));
    }

    .priority-low {
      border-left: 4px solid hsl(var(--success));
    }

    .checkbox {
      width: 1.25rem;
      height: 1.25rem;
      border: 2px solid hsl(var(--border));
      border-radius: 0.25rem;
      cursor: pointer;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      border-radius: 9999px;
      padding: 0.25rem 0.625rem;
      font-size: 0.75rem;
      font-weight: 600;
    }
  </style>
</head>
<body class="bg-background text-foreground antialiased">
  <div class="container mx-auto py-8 px-4 max-w-4xl">
    <!-- 页面头部 -->
    <div class="flex flex-col gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">📋 待办事项清单</h1>
        <p class="text-muted-foreground mt-2">从与 {{contact_name}} 的对话中提取</p>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <span class="badge" style="background: hsl(var(--muted)); color: hsl(var(--muted-foreground));">
          📅 {{date_range}}
        </span>
        <span class="badge" style="background: hsl(var(--muted)); color: hsl(var(--muted-foreground));">
          ✅ {{total_todos}} 个任务
        </span>
        <span class="badge" style="background: hsl(var(--destructive)); color: white;">
          🔥 {{high_priority}} 个高优先级
        </span>
      </div>
    </div>

    <div style="height: 1px; background: hsl(var(--border)); margin-bottom: 2rem;"></div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-primary">{{total_todos}}</div>
        <div class="text-sm text-muted-foreground mt-1">总任务数</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold" style="color: hsl(var(--destructive));">{{high_priority}}</div>
        <div class="text-sm text-muted-foreground mt-1">高优先级</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold" style="color: hsl(var(--warning));">{{with_deadline}}</div>
        <div class="text-sm text-muted-foreground mt-1">有截止日期</div>
      </div>
    </div>

    <!-- 待办事项列表 -->
    <div class="space-y-6">
      <!-- 高优先级任务 -->
      {{#if high_priority_todos}}
      <div class="card">
        <div class="p-6 pb-4">
          <h2 class="text-xl font-semibold flex items-center gap-2">
            <span>🔥</span>
            <span>高优先级任务</span>
          </h2>
        </div>
        <div>
          {{#each high_priority_todos}}
          <div class="todo-item priority-high">
            <div class="flex items-start gap-3">
              <input type="checkbox" class="checkbox mt-1">
              <div class="flex-1">
                <div class="font-medium text-foreground">{{content}}</div>
                <div class="flex items-center gap-3 mt-2 text-sm text-muted-foreground">
                  {{#if deadline}}
                  <span>⏰ {{deadline}}</span>
                  {{/if}}
                  {{#if assignee}}
                  <span>👤 {{assignee}}</span>
                  {{/if}}
                </div>
                {{#if source_message}}
                <div class="mt-2 text-xs text-muted-foreground italic">
                  "{{source_message}}"
                </div>
                {{/if}}
              </div>
            </div>
          </div>
          {{/each}}
        </div>
      </div>
      {{/if}}

      <!-- 中优先级任务 -->
      {{#if medium_priority_todos}}
      <div class="card">
        <div class="p-6 pb-4">
          <h2 class="text-xl font-semibold flex items-center gap-2">
            <span>⚡</span>
            <span>中优先级任务</span>
          </h2>
        </div>
        <div>
          {{#each medium_priority_todos}}
          <div class="todo-item priority-medium">
            <div class="flex items-start gap-3">
              <input type="checkbox" class="checkbox mt-1">
              <div class="flex-1">
                <div class="font-medium text-foreground">{{content}}</div>
                <div class="flex items-center gap-3 mt-2 text-sm text-muted-foreground">
                  {{#if deadline}}
                  <span>⏰ {{deadline}}</span>
                  {{/if}}
                  {{#if assignee}}
                  <span>👤 {{assignee}}</span>
                  {{/if}}
                </div>
              </div>
            </div>
          </div>
          {{/each}}
        </div>
      </div>
      {{/if}}

      <!-- 低优先级任务 -->
      {{#if low_priority_todos}}
      <div class="card">
        <div class="p-6 pb-4">
          <h2 class="text-xl font-semibold flex items-center gap-2">
            <span>📌</span>
            <span>低优先级任务</span>
          </h2>
        </div>
        <div>
          {{#each low_priority_todos}}
          <div class="todo-item priority-low">
            <div class="flex items-start gap-3">
              <input type="checkbox" class="checkbox mt-1">
              <div class="flex-1">
                <div class="font-medium text-foreground">{{content}}</div>
                <div class="flex items-center gap-3 mt-2 text-sm text-muted-foreground">
                  {{#if deadline}}
                  <span>⏰ {{deadline}}</span>
                  {{/if}}
                  {{#if assignee}}
                  <span>👤 {{assignee}}</span>
                  {{/if}}
                </div>
              </div>
            </div>
          </div>
          {{/each}}
        </div>
      </div>
      {{/if}}
    </div>

    <!-- 页脚 -->
    <div class="mt-12 text-center text-sm text-muted-foreground">
      <p>由 Wetrace AI 提取 • {{generation_time}}</p>
      <p class="mt-1">💡 提示：点击复选框标记任务完成</p>
    </div>
  </div>

  <script>
    // 添加交互功能
    document.querySelectorAll('.checkbox').forEach(checkbox => {
      checkbox.addEventListener('change', function() {
        const todoItem = this.closest('.todo-item');
        if (this.checked) {
          todoItem.style.opacity = '0.5';
          todoItem.querySelector('.font-medium').style.textDecoration = 'line-through';
        } else {
          todoItem.style.opacity = '1';
          todoItem.querySelector('.font-medium').style.textDecoration = 'none';
        }
      });
    });
  </script>
</body>
</html>
```

### 4. 数据处理逻辑
```javascript
// 按优先级分组
const groupedTodos = {
  high_priority_todos: todos.filter(t => t.priority === 'high'),
  medium_priority_todos: todos.filter(t => t.priority === 'medium'),
  low_priority_todos: todos.filter(t => t.priority === 'low')
};

// 统计数据
const stats = {
  total_todos: todos.length,
  high_priority: groupedTodos.high_priority_todos.length,
  with_deadline: todos.filter(t => t.deadline).length
};

// 模板数据
const templateData = {
  contact_name: "张三",
  date_range: "2024-01-01 至 2024-01-31",
  ...stats,
  ...groupedTodos,
  generation_time: new Date().toLocaleString('zh-CN')
};
```

## 输出格式

```
✅ 待办事项提取完成！

📊 统计信息：
- 会话对象：张三
- 时间范围：2024-01-01 至 2024-01-31
- 总任务数：12 个
- 高优先级：3 个
- 有截止日期：8 个

🔥 高优先级任务：
1. 完成项目文档 - 截止：2024-01-31 - 负责人：张三
2. 提交季度报告 - 截止：2024-01-25
3. 修复线上 Bug - 紧急

📄 完整任务清单已保存至：
~/wetrace-exports/todos_zhangsan_20240131.html

🔗 在浏览器中打开查看完整清单
```

## 示例对话

**用户输入**：
```
提取我和张三最近的待办事项
```

**Skill 响应**：
```
好的，我来提取与张三对话中的待办事项。

正在分析聊天记录...
✓ 已分析 156 条消息
✓ 提取到 12 个待办事项

正在生成任务清单...
✓ 页面生成完成

---

✅ 待办事项提取完成！

📊 统计：12 个任务（3 个高优先级，8 个有截止日期）

🔥 高优先级任务预览：
1. 完成项目文档 - ⏰ 2024-01-31
2. 提交季度报告 - ⏰ 2024-01-25
3. 修复线上 Bug - 🚨 紧急

📄 完整清单：~/wetrace-exports/todos_zhangsan_20240131.html
```

## 错误处理

### 1. 未提取到待办事项
```
⚠️ 在指定时间范围内未找到待办事项
建议：
- 尝试扩大时间范围
- 检查是否有明确的任务描述
- 使用关键词搜索特定任务
```

### 2. AI 提取失败
```
❌ 待办事项提取失败：AI 服务暂时不可用
建议：稍后重试，或使用关键词搜索功能
```

## 技术要点

### 1. 智能识别
- 识别任务关键词（"需要"、"记得"、"完成"等）
- 提取截止日期（"明天"、"下周五"、"月底前"）
- 识别负责人（"你"、"我"、人名）
- 判断优先级（"紧急"、"重要"、"尽快"）

### 2. 交互功能
- 点击复选框标记完成
- 完成的任务显示删除线
- 悬停高亮效果

### 3. 视觉设计
- 优先级颜色编码（红/黄/绿）
- 清晰的任务分组
- 响应式布局

## 扩展功能（未来）

- [ ] 导出为 Markdown/CSV 格式
- [ ] 同步到日历应用
- [ ] 设置任务提醒
- [ ] 任务进度跟踪
- [ ] 多人协作任务分配
