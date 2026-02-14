# 智能周报月报生成器 Skill

## 触发关键词
- "生成周报"
- "生成月报"
- "weekly report"
- "monthly report"
- "周报"
- "月报"

## 功能描述
自动生成精美的周报或月报 HTML 页面，包含数据统计、AI 总结、趋势分析和可视化图表。

## API 依赖
- `GET /report/annual` - 年度报告（可用于月报）
- `GET /analysis/daily/:id` - 每日数据
- `GET /analysis/personal/top-contacts` - Top 联系人
- `POST /ai/summarize` - AI 总结

## 工作流程

### 1. 参数收集
- **报告类型** (type): "weekly" 或 "monthly"
- **时间范围** (time_range): 自动计算（上周/上月）
- **会话 ID** (talker_id): 可选，不填则生成全局报告

### 2. 数据获取
```javascript
// 1. 获取时间范围内的每日数据
GET /analysis/daily/{talker_id}?time_range={time_range}

// 2. 获取 Top 联系人
GET /analysis/personal/top-contacts?time_range={time_range}&limit=10

// 3. 获取消息数据用于 AI 总结
GET /messages?time_range={time_range}&limit=500

// 4. 生成 AI 总结
POST /ai/summarize
```

### 3. HTML 页面生成

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{report_type}} - {{date_range}}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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

    .stat-card {
      text-align: center;
      padding: 1.5rem;
    }

    .stat-value {
      font-size: 2.5rem;
      font-weight: bold;
      color: hsl(var(--primary));
    }

    .stat-label {
      font-size: 0.875rem;
      color: hsl(var(--muted-foreground));
      margin-top: 0.5rem;
    }

    .highlight-box {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 2rem;
      border-radius: 0.5rem;
      margin-bottom: 2rem;
    }
  </style>
</head>
<body class="bg-background text-foreground antialiased">
  <div class="container mx-auto py-8 px-4 max-w-6xl">
    <!-- 封面 -->
    <div class="highlight-box text-center">
      <h1 class="text-4xl font-bold mb-2">{{report_title}}</h1>
      <p class="text-xl opacity-90">{{date_range}}</p>
      <div class="mt-6 flex items-center justify-center gap-8">
        <div>
          <div class="text-3xl font-bold">{{total_messages}}</div>
          <div class="text-sm opacity-80">消息总数</div>
        </div>
        <div>
          <div class="text-3xl font-bold">{{active_contacts}}</div>
          <div class="text-sm opacity-80">活跃联系人</div>
        </div>
        <div>
          <div class="text-3xl font-bold">{{active_days}}</div>
          <div class="text-sm opacity-80">活跃天数</div>
        </div>
      </div>
    </div>

    <!-- AI 总结 -->
    <div class="card p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4 flex items-center gap-2">
        <span>🤖</span>
        <span>AI 智能总结</span>
      </h2>
      <div class="prose prose-sm max-w-none">
        <p class="text-foreground leading-relaxed text-lg">{{ai_summary}}</p>
      </div>
    </div>

    <!-- 数据统计 -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="card stat-card">
        <div class="stat-value">{{total_messages}}</div>
        <div class="stat-label">消息总数</div>
      </div>
      <div class="card stat-card">
        <div class="stat-value">{{avg_per_day}}</div>
        <div class="stat-label">日均消息</div>
      </div>
      <div class="card stat-card">
        <div class="stat-value">{{peak_day_count}}</div>
        <div class="stat-label">峰值消息</div>
      </div>
      <div class="card stat-card">
        <div class="stat-value">{{growth_rate}}</div>
        <div class="stat-label">增长率</div>
      </div>
    </div>

    <!-- 趋势图 -->
    <div class="card p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">📈 消息趋势</h2>
      <div style="height: 300px;">
        <canvas id="trendChart"></canvas>
      </div>
    </div>

    <!-- Top 联系人 -->
    <div class="card p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">👥 Top 10 联系人</h2>
      <div class="space-y-3">
        {{#each top_contacts}}
        <div class="flex items-center justify-between p-3 rounded hover:bg-muted transition">
          <div class="flex items-center gap-3">
            <div class="text-2xl font-bold text-muted-foreground">{{rank}}</div>
            <div>
              <div class="font-medium">{{name}}</div>
              <div class="text-sm text-muted-foreground">{{count}} 条消息</div>
            </div>
          </div>
          <div class="text-right">
            <div class="text-sm font-semibold text-primary">{{percentage}}%</div>
          </div>
        </div>
        {{/each}}
      </div>
    </div>

    <!-- 关键洞察 -->
    <div class="card p-6">
      <h2 class="text-xl font-semibold mb-4">💡 关键洞察</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {{#each insights}}
        <div class="p-4 rounded border border-border">
          <div class="flex items-start gap-3">
            <span class="text-2xl">{{icon}}</span>
            <div>
              <div class="font-semibold text-foreground">{{title}}</div>
              <div class="text-sm text-muted-foreground mt-1">{{description}}</div>
            </div>
          </div>
        </div>
        {{/each}}
      </div>
    </div>

    <!-- 页脚 -->
    <div class="mt-12 text-center text-sm text-muted-foreground">
      <p>由 Wetrace AI 生成 • {{generation_time}}</p>
    </div>
  </div>

  <script>
    // 趋势图数据
    const trendData = {{trend_data_json}};

    const ctx = document.getElementById('trendChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: trendData.map(d => d.date),
        datasets: [{
          label: '消息数量',
          data: trendData.map(d => d.count),
          borderColor: 'hsl(222.2, 47.4%, 11.2%)',
          backgroundColor: 'hsla(222.2, 47.4%, 11.2%, 0.1)',
          fill: true,
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  </script>
</body>
</html>
```

## 输出格式

```
✅ {{report_type}}已生成！

📊 本{{period}}概览：
- 时间范围：{{date_range}}
- 消息总数：{{total_messages}} 条
- 活跃联系人：{{active_contacts}} 人
- 日均消息：{{avg_per_day}} 条

🤖 AI 总结：
{{summary_preview}}

👥 Top 3 联系人：
1. 张三 - 234 条 (18.9%)
2. 李四 - 189 条 (15.3%)
3. 王五 - 156 条 (12.6%)

📄 完整报告已保存至：
~/wetrace-exports/{{report_type}}_{{date}}.html
```

## 示例对话

**用户输入**：
```
生成上周的周报
```

**Skill 响应**：
```
好的，我来生成上周（2024-01-22 至 2024-01-28）的周报。

正在收集数据...
✓ 已分析 456 条消息
✓ 统计 23 位联系人

正在生成 AI 总结...
✓ 总结完成

正在生成报告...
✓ 报告生成完成

---

✅ 周报已生成！

📊 上周概览：
- 消息总数：456 条
- 活跃联系人：23 人
- 日均消息：65 条
- 增长率：+12%

🤖 AI 总结：
上周沟通活跃度较高，主要围绕项目进展和技术讨论。
与张三的沟通最为频繁，主要讨论了新功能的实现方案。

📄 完整报告：~/wetrace-exports/weekly_20240128.html
```

## 技术要点

### 1. 自动时间计算
- 周报：上周一到周日
- 月报：上个自然月

### 2. 数据聚合
- 多个 API 数据整合
- 统计指标计算
- 趋势分析

### 3. 视觉设计
- 渐变色封面
- 数据卡片布局
- 图表可视化

## 扩展功能（未来）

- [ ] 定时自动生成
- [ ] 邮件推送
- [ ] 多人协作报告
- [ ] 自定义报告模板
