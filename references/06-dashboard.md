# 数据仪表板 Skill

## 触发关键词
- "生成仪表板"
- "数据总览"
- "dashboard"
- "数据面板"
- "总览仪表板"

## 功能描述
生成交互式数据仪表板 HTML 页面，集成多个数据可视化组件，提供全方位的数据总览。

## API 依赖
- `GET /dashboard` - 总览数据
- `GET /analysis/hourly` - 每小时活跃度
- `GET /analysis/weekday` - 星期活跃度
- `GET /analysis/personal/top-contacts` - Top 联系人
- `GET /analysis/message-types/:id` - 消息类型分布

## 工作流程

### 1. 参数收集
- **时间范围** (time_range): 可选，默认最近 30 天
- **会话 ID** (talker_id): 可选，不填则显示全局数据

### 2. 数据获取
```javascript
// 1. 获取总览数据
GET /dashboard

// 2. 获取各类分析数据
GET /analysis/hourly
GET /analysis/weekday
GET /analysis/personal/top-contacts
GET /analysis/message-types/{talker_id}
```

### 3. HTML 页面生成

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>数据仪表板 - Wetrace</title>
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

    body {
      background: linear-gradient(to bottom, #f8fafc, #f1f5f9);
    }

    .card {
      background-color: hsl(var(--card));
      border-radius: 0.5rem;
      border: 1px solid hsl(var(--border));
      box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }

    .metric-card {
      padding: 1.5rem;
      text-align: center;
    }

    .metric-value {
      font-size: 2.5rem;
      font-weight: bold;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .metric-label {
      font-size: 0.875rem;
      color: hsl(var(--muted-foreground));
      margin-top: 0.5rem;
    }

    .chart-container {
      position: relative;
      height: 300px;
    }
  </style>
</head>
<body class="antialiased">
  <div class="container mx-auto py-8 px-4 max-w-7xl">
    <!-- 页面头部 -->
    <div class="mb-8">
      <h1 class="text-4xl font-bold tracking-tight mb-2">📊 数据仪表板</h1>
      <p class="text-muted-foreground">实时数据总览与分析</p>
      <div class="mt-4 flex items-center gap-2">
        <span class="badge">📅 {{date_range}}</span>
        <span class="badge">🔄 最后更新：{{last_update}}</span>
      </div>
    </div>

    <!-- 核心指标卡片 -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div class="card metric-card">
        <div class="metric-value">{{total_messages}}</div>
        <div class="metric-label">消息总数</div>
        <div class="text-xs text-muted-foreground mt-2">
          <span class="text-green-600">↑ {{message_growth}}%</span> vs 上期
        </div>
      </div>
      <div class="card metric-card">
        <div class="metric-value">{{total_contacts}}</div>
        <div class="metric-label">联系人数</div>
        <div class="text-xs text-muted-foreground mt-2">
          <span class="text-green-600">↑ {{contact_growth}}%</span> vs 上期
        </div>
      </div>
      <div class="card metric-card">
        <div class="metric-value">{{total_sessions}}</div>
        <div class="metric-label">会话数</div>
        <div class="text-xs text-muted-foreground mt-2">
          活跃会话 {{active_sessions}}
        </div>
      </div>
      <div class="card metric-card">
        <div class="metric-value">{{avg_per_day}}</div>
        <div class="metric-label">日均消息</div>
        <div class="text-xs text-muted-foreground mt-2">
          峰值 {{peak_day_count}}
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- 消息类型分布 -->
      <div class="card p-6">
        <h2 class="text-xl font-semibold mb-4">💬 消息类型分布</h2>
        <div class="chart-container">
          <canvas id="messageTypeChart"></canvas>
        </div>
      </div>

      <!-- 每小时活跃度 -->
      <div class="card p-6">
        <h2 class="text-xl font-semibold mb-4">⏰ 每小时活跃度</h2>
        <div class="chart-container">
          <canvas id="hourlyChart"></canvas>
        </div>
      </div>

      <!-- 星期活跃度 -->
      <div class="card p-6">
        <h2 class="text-xl font-semibold mb-4">📅 星期活跃度</h2>
        <div class="chart-container">
          <canvas id="weekdayChart"></canvas>
        </div>
      </div>

      <!-- Top 联系人 -->
      <div class="card p-6">
        <h2 class="text-xl font-semibold mb-4">👥 Top 10 联系人</h2>
        <div class="space-y-2 overflow-y-auto" style="max-height: 300px;">
          {{#each top_contacts}}
          <div class="flex items-center justify-between p-2 rounded hover:bg-muted transition">
            <div class="flex items-center gap-2">
              <span class="text-sm font-bold text-muted-foreground w-6">{{rank}}</span>
              <span class="font-medium">{{name}}</span>
            </div>
            <div class="flex items-center gap-2">
              <div class="w-24 bg-muted rounded-full h-2">
                <div class="bg-primary h-2 rounded-full" style="width: {{percentage}}%"></div>
              </div>
              <span class="text-sm font-semibold text-primary w-16 text-right">{{count}}</span>
            </div>
          </div>
          {{/each}}
        </div>
      </div>
    </div>

    <!-- 快速洞察 -->
    <div class="card p-6">
      <h2 class="text-xl font-semibold mb-4">💡 快速洞察</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        {{#each quick_insights}}
        <div class="p-4 rounded border border-border bg-muted/30">
          <div class="text-3xl mb-2">{{icon}}</div>
          <div class="font-semibold text-foreground mb-1">{{title}}</div>
          <div class="text-sm text-muted-foreground">{{description}}</div>
        </div>
        {{/each}}
      </div>
    </div>

    <!-- 页脚 -->
    <div class="mt-12 text-center text-sm text-muted-foreground">
      <p>由 Wetrace 生成 • {{generation_time}}</p>
      <p class="mt-1">💡 提示：刷新页面获取最新数据</p>
    </div>
  </div>

  <script>
    // 消息类型分布图
    const messageTypeCtx = document.getElementById('messageTypeChart').getContext('2d');
    new Chart(messageTypeCtx, {
      type: 'doughnut',
      data: {
        labels: {{message_type_labels}},
        datasets: [{
          data: {{message_type_data}},
          backgroundColor: [
            '#667eea',
            '#764ba2',
            '#f093fb',
            '#4facfe',
            '#43e97b'
          ]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    });

    // 每小时活跃度图
    const hourlyCtx = document.getElementById('hourlyChart').getContext('2d');
    new Chart(hourlyCtx, {
      type: 'bar',
      data: {
        labels: {{hourly_labels}},
        datasets: [{
          label: '消息数',
          data: {{hourly_data}},
          backgroundColor: 'hsla(222.2, 47.4%, 11.2%, 0.8)'
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

    // 星期活跃度图
    const weekdayCtx = document.getElementById('weekdayChart').getContext('2d');
    new Chart(weekdayCtx, {
      type: 'radar',
      data: {
        labels: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
        datasets: [{
          label: '消息数',
          data: {{weekday_data}},
          backgroundColor: 'hsla(222.2, 47.4%, 11.2%, 0.2)',
          borderColor: 'hsl(222.2, 47.4%, 11.2%)',
          pointBackgroundColor: 'hsl(222.2, 47.4%, 11.2%)'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
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
✅ 数据仪表板已生成！

📊 核心指标：
- 消息总数：12,345 条 (↑ 15%)
- 联系人数：89 人 (↑ 8%)
- 会话数：156 个
- 日均消息：412 条

💡 快速洞察：
• 最活跃时段：周三 14:00
• 最常用消息类型：文本 (78%)
• Top 联系人：张三 (1,234 条)

📄 完整仪表板已保存至：
~/wetrace-exports/dashboard_20240131.html

🔗 在浏览器中打开查看完整仪表板
```

## 示例对话

**用户输入**：
```
生成数据仪表板
```

**Skill 响应**：
```
好的，我来生成数据仪表板。

正在收集数据...
✓ 总览数据
✓ 活跃度分析
✓ 联系人统计
✓ 消息类型分布

正在生成仪表板...
✓ 4 个核心指标卡片
✓ 4 个可视化图表
✓ 快速洞察面板

---

✅ 数据仪表板已生成！

📊 核心指标：
- 消息总数：12,345 条 (↑ 15% vs 上期)
- 联系人数：89 人
- 日均消息：412 条

📄 查看完整仪表板：
~/wetrace-exports/dashboard_20240131.html
```

## 技术要点

### 1. 多图表集成
- 饼图（消息类型）
- 柱状图（每小时）
- 雷达图（星期）
- 进度条（Top 联系人）

### 2. 响应式布局
- Grid 布局系统
- 移动端适配
- 卡片悬停效果

### 3. 数据实时性
- 显示最后更新时间
- 支持手动刷新
- 增长率对比

## 扩展功能（未来）

- [ ] 自动刷新数据
- [ ] 自定义仪表板布局
- [ ] 导出为 PDF
- [ ] 数据钻取功能
- [ ] 多维度筛选
