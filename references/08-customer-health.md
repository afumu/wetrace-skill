# 客户关系健康度仪表板 Skill

## 触发关键词
- "客户健康度"
- "CRM 仪表板"
- "customer health"
- "客户关系分析"
- "客户跟进"

## 功能描述
生成客户关系健康度仪表板，帮助销售人员和客户经理了解客户状态，优先跟进重要客户。

## API 依赖
- `GET /contacts/need-contact` - 需要跟进的客户列表
- `GET /analysis/daily/:id` - 客户活跃度
- `POST /ai/sentiment` - 情感分析
- `GET /messages` - 消息数据

## 工作流程

### 1. 参数收集
- **跟进天数阈值** (days): 可选，默认 7 天
- **客户列表** (contacts): 可选，不填则分析所有需跟进客户

### 2. 数据获取与分析
```javascript
// 1. 获取需要跟进的客户
GET /contacts/need-contact?days={days}

// 2. 对每个客户进行分析
for (const contact of contacts) {
  // 获取活跃度数据
  const activity = await GET(`/analysis/daily/${contact.id}`);

  // 获取最近消息
  const messages = await GET(`/messages?talker_id=${contact.id}&limit=50`);

  // 情感分析
  const sentiment = await POST('/ai/sentiment', { messages });

  // 计算健康度评分
  const healthScore = calculateHealthScore({
    activity,
    sentiment,
    lastContactDays: contact.days_since_last_contact
  });
}
```

### 3. 健康度评分算法
```javascript
function calculateHealthScore(data) {
  let score = 100;

  // 1. 联系频率 (40%)
  const daysSinceLastContact = data.lastContactDays;
  if (daysSinceLastContact > 30) score -= 40;
  else if (daysSinceLastContact > 14) score -= 20;
  else if (daysSinceLastContact > 7) score -= 10;

  // 2. 情感倾向 (30%)
  if (data.sentiment === 'negative') score -= 30;
  else if (data.sentiment === 'neutral') score -= 10;

  // 3. 互动趋势 (30%)
  const trend = calculateTrend(data.activity);
  if (trend === 'declining') score -= 30;
  else if (trend === 'stable') score -= 10;

  return Math.max(0, Math.min(100, score));
}

function getHealthLevel(score) {
  if (score >= 80) return { level: 'healthy', color: 'green', icon: '💚' };
  if (score >= 60) return { level: 'warning', color: 'yellow', icon: '💛' };
  return { level: 'critical', color: 'red', icon: '❤️' };
}
```

### 4. HTML 页面生成

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>客户关系健康度仪表板</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {
      --background: 0 0% 100%;
      --foreground: 222.2 84% 4.9%;
      --card: 0 0% 100%;
      --primary: 222.2 47.4% 11.2%;
      --muted: 210 40% 96.1%;
      --border: 214.3 31.8% 91.4%;
      --success: 142 76% 36%;
      --warning: 38 92% 50%;
      --destructive: 0 84.2% 60.2%;
    }

    .card {
      background-color: hsl(var(--card));
      border-radius: 0.5rem;
      border: 1px solid hsl(var(--border));
      box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }

    .health-indicator {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      font-weight: bold;
      color: white;
    }

    .health-healthy {
      background: linear-gradient(135deg, #10b981, #059669);
    }

    .health-warning {
      background: linear-gradient(135deg, #f59e0b, #d97706);
    }

    .health-critical {
      background: linear-gradient(135deg, #ef4444, #dc2626);
    }

    .priority-badge {
      display: inline-flex;
      align-items: center;
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
    }

    .priority-high {
      background: #fee2e2;
      color: #991b1b;
    }

    .priority-medium {
      background: #fef3c7;
      color: #92400e;
    }

    .priority-low {
      background: #dbeafe;
      color: #1e40af;
    }
  </style>
</head>
<body class="bg-background text-foreground antialiased">
  <div class="container mx-auto py-8 px-4 max-w-7xl">
    <!-- 页面头部 -->
    <div class="mb-8">
      <h1 class="text-4xl font-bold tracking-tight mb-2">💼 客户关系健康度仪表板</h1>
      <p class="text-muted-foreground">实时监控客户状态，优先跟进重要客户</p>
      <div class="mt-4 flex items-center gap-2 flex-wrap">
        <span class="badge">📅 {{date}}</span>
        <span class="badge">👥 {{total_customers}} 位客户</span>
        <span class="badge">⚠️ {{need_attention}} 位需要关注</span>
      </div>
    </div>

    <!-- 健康度概览 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="card p-6 text-center">
        <div class="text-5xl font-bold text-green-600 mb-2">{{healthy_count}}</div>
        <div class="text-sm text-muted-foreground">健康客户</div>
        <div class="mt-4 w-full bg-muted rounded-full h-2">
          <div class="bg-green-600 h-2 rounded-full" style="width: {{healthy_percentage}}%"></div>
        </div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-5xl font-bold text-yellow-600 mb-2">{{warning_count}}</div>
        <div class="text-sm text-muted-foreground">需要关注</div>
        <div class="mt-4 w-full bg-muted rounded-full h-2">
          <div class="bg-yellow-600 h-2 rounded-full" style="width: {{warning_percentage}}%"></div>
        </div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-5xl font-bold text-red-600 mb-2">{{critical_count}}</div>
        <div class="text-sm text-muted-foreground">紧急跟进</div>
        <div class="mt-4 w-full bg-muted rounded-full h-2">
          <div class="bg-red-600 h-2 rounded-full" style="width: {{critical_percentage}}%"></div>
        </div>
      </div>
    </div>

    <!-- 紧急跟进列表 -->
    {{#if critical_customers}}
    <div class="card p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4 flex items-center gap-2">
        <span>🚨</span>
        <span>紧急跟进客户</span>
      </h2>
      <div class="space-y-4">
        {{#each critical_customers}}
        <div class="flex items-center gap-4 p-4 border border-red-200 rounded-lg bg-red-50">
          <div class="health-indicator health-critical">
            {{health_score}}
          </div>
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <span class="font-semibold text-lg">{{name}}</span>
              <span class="priority-badge priority-high">高优先级</span>
            </div>
            <div class="text-sm text-muted-foreground space-y-1">
              <div>⏰ 已 {{days_since_last_contact}} 天未联系</div>
              <div>💬 最近消息：{{last_message_preview}}</div>
              <div>😔 情感倾向：{{sentiment_text}}</div>
            </div>
          </div>
          <div class="text-right">
            <button class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition">
              立即跟进
            </button>
            <div class="text-xs text-muted-foreground mt-2">
              建议话术：{{suggested_opener}}
            </div>
          </div>
        </div>
        {{/each}}
      </div>
    </div>
    {{/if}}

    <!-- 需要关注列表 -->
    {{#if warning_customers}}
    <div class="card p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4 flex items-center gap-2">
        <span>⚠️</span>
        <span>需要关注客户</span>
      </h2>
      <div class="space-y-4">
        {{#each warning_customers}}
        <div class="flex items-center gap-4 p-4 border border-yellow-200 rounded-lg bg-yellow-50">
          <div class="health-indicator health-warning">
            {{health_score}}
          </div>
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <span class="font-semibold text-lg">{{name}}</span>
              <span class="priority-badge priority-medium">中优先级</span>
            </div>
            <div class="text-sm text-muted-foreground space-y-1">
              <div>⏰ 已 {{days_since_last_contact}} 天未联系</div>
              <div>📊 互动趋势：{{trend_text}}</div>
            </div>
          </div>
          <div class="text-right">
            <button class="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700 transition">
              计划跟进
            </button>
          </div>
        </div>
        {{/each}}
      </div>
    </div>
    {{/if}}

    <!-- 健康客户列表 -->
    {{#if healthy_customers}}
    <div class="card p-6">
      <h2 class="text-2xl font-semibold mb-4 flex items-center gap-2">
        <span>💚</span>
        <span>健康客户</span>
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {{#each healthy_customers}}
        <div class="flex items-center gap-4 p-4 border border-green-200 rounded-lg bg-green-50">
          <div class="health-indicator health-healthy">
            {{health_score}}
          </div>
          <div class="flex-1">
            <div class="font-semibold">{{name}}</div>
            <div class="text-sm text-muted-foreground">
              ✅ 关系良好，保持联系
            </div>
          </div>
        </div>
        {{/each}}
      </div>
    </div>
    {{/if}}

    <!-- 页脚 -->
    <div class="mt-12 text-center text-sm text-muted-foreground">
      <p>由 Wetrace AI 生成 • {{generation_time}}</p>
      <p class="mt-1">💡 提示：健康度评分基于联系频率、情感倾向和互动趋势综合计算</p>
    </div>
  </div>

  <script>
    // 添加交互功能
    document.querySelectorAll('button').forEach(button => {
      button.addEventListener('click', function() {
        const customerName = this.closest('.flex').querySelector('.font-semibold').textContent;
        alert(`准备跟进客户：${customerName}`);
      });
    });
  </script>
</body>
</html>
```

## 输出格式

```
✅ 客户关系健康度仪表板已生成！

📊 客户健康度概览：
- 健康客户：15 位 (60%)
- 需要关注：7 位 (28%)
- 紧急跟进：3 位 (12%)

🚨 紧急跟进客户：
1. 张三 - 健康度：45 - 已 15 天未联系
   💬 建议话术：您好张三，最近项目进展如何？

2. 李四 - 健康度：38 - 已 21 天未联系
   💬 建议话术：李总，好久不见，有空聊聊新的合作机会吗？

3. 王五 - 健康度：42 - 已 18 天未联系
   💬 建议话术：王经理，上次讨论的方案有进展吗？

📄 完整仪表板已保存至：
~/wetrace-exports/customer_health_20240131.html

🔗 在浏览器中打开查看完整仪表板
```

## 示例对话

**用户输入**：
```
生成客户关系健康度仪表板
```

**Skill 响应**：
```
好的，我来生成客户关系健康度仪表板。

正在分析客户数据...
✓ 已分析 25 位客户
✓ 计算健康度评分
✓ 生成跟进建议

---

✅ 客户健康度仪表板已生成！

📊 健康度分布：
- 💚 健康：15 位 (60%)
- 💛 关注：7 位 (28%)
- ❤️ 紧急：3 位 (12%)

🚨 需要立即跟进：
1. 张三 (健康度 45) - 已 15 天未联系
2. 李四 (健康度 38) - 已 21 天未联系
3. 王五 (健康度 42) - 已 18 天未联系

💡 建议：优先跟进健康度低于 50 的客户

📄 查看完整仪表板：
~/wetrace-exports/customer_health_20240131.html
```

## 技术要点

### 1. 健康度评分算法
- 联系频率（40%）
- 情感倾向（30%）
- 互动趋势（30%）

### 2. 优先级分级
- 健康（80-100）：绿色
- 关注（60-79）：黄色
- 紧急（0-59）：红色

### 3. 智能建议
- 基于历史对话生成话术
- 考虑客户特点和偏好
- 提供最佳联系时间

### 4. 视觉设计
- 红黄绿灯状态指示
- 健康度圆形指示器
- 优先级徽章

## 扩展功能（未来）

- [ ] 自动发送跟进提醒
- [ ] 集成日历安排跟进
- [ ] 客户分组管理
- [ ] 跟进记录追踪
- [ ] 预测客户流失风险
- [ ] 导出为 CRM 系统
