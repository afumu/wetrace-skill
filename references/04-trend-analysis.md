# 互动趋势分析 Skill

## 触发关键词
- "趋势分析"
- "互动趋势"
- "trend analysis"
- "消息趋势"
- "活跃度趋势"

## 功能描述
生成可钻取的多层级时间趋势图（年→月→周→日→小时），直观展示聊天活跃度的变化趋势。

## API 依赖
- `GET /analysis/monthly` - 月度趋势
- `GET /analysis/daily/:id` - 每日趋势
- `GET /analysis/hourly` - 每小时趋势

## 工作流程

### 1. 参数收集
- **会话 ID** (talker_id): 可选
- **时间范围** (time_range): 可选，默认最近一年
- **粒度** (granularity): 可选，默认 "monthly"

### 2. 数据获取
```javascript
// 1. 月度数据
GET /analysis/monthly?talker_id={talker_id}&time_range={time_range}

// 2. 每日数据（用于钻取）
GET /analysis/daily/{talker_id}?time_range={time_range}

// 3. 每小时数据（用于钻取）
GET /analysis/hourly?talker_id={talker_id}&time_range={time_range}
```

### 3. HTML 页面生成

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>互动趋势分析 - {{contact_name}}</title>
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

    .trend-indicator {
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      padding: 0.25rem 0.5rem;
      border-radius: 0.25rem;
      font-size: 0.875rem;
      font-weight: 600;
    }

    .trend-up {
      background: #dcfce7;
      color: #166534;
    }

    .trend-down {
      background: #fee2e2;
      color: #991b1b;
    }

    .trend-stable {
      background: hsl(var(--muted));
      color: hsl(var(--muted-foreground));
    }
  </style>
</head>
<body class="bg-background text-foreground antialiased">
  <div class="container mx-auto py-8 px-4 max-w-6xl">
    <!-- 页面头部 -->
    <div class="flex flex-col gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">📈 互动趋势分析</h1>
        <p class="text-muted-foreground mt-2">{{description}}</p>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <span class="badge">📅 {{date_range}}</span>
        <span class="badge">💬 {{total_messages}} 条消息</span>
        <span class="trend-indicator {{trend_class}}">
          {{trend_icon}} {{trend_text}}
        </span>
      </div>
    </div>

    <div class="separator mb-8"></div>

    <!-- 趋势图卡片 -->
    <div class="card p-6 mb-6">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-xl font-semibold">消息趋势图</h2>
          <p class="text-sm text-muted-foreground mt-1">点击数据点查看详细信息</p>
        </div>
        <div class="flex gap-2">
          <button class="btn-outline" onclick="changeGranularity('monthly')">月度</button>
          <button class="btn-outline" onclick="changeGranularity('daily')">每日</button>
          <button class="btn-outline" onclick="changeGranularity('hourly')">每小时</button>
        </div>
      </div>

      <div style="height: 400px;">
        <canvas id="trendChart"></canvas>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-primary">{{peak_value}}</div>
        <div class="text-sm text-muted-foreground mt-1">峰值消息数</div>
        <div class="text-xs text-muted-foreground mt-1">{{peak_date}}</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-primary">{{avg_value}}</div>
        <div class="text-sm text-muted-foreground mt-1">平均消息数</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-primary">{{growth_rate}}</div>
        <div class="text-sm text-muted-foreground mt-1">增长率</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-primary">{{active_days}}</div>
        <div class="text-sm text-muted-foreground mt-1">活跃天数</div>
      </div>
    </div>

    <!-- 趋势洞察 -->
    <div class="card p-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
        <span>💡</span>
        <span>趋势洞察</span>
      </h3>
      <div class="space-y-4">
        {{#each insights}}
        <div class="flex items-start gap-3">
          <span class="text-2xl">{{icon}}</span>
          <div>
            <div class="font-medium text-foreground">{{title}}</div>
            <div class="text-sm text-muted-foreground mt-1">{{description}}</div>
          </div>
        </div>
        {{/each}}
      </div>
    </div>

    <!-- 页脚 -->
    <div class="mt-12 text-center text-sm text-muted-foreground">
      <p>由 Wetrace 生成 • {{generation_time}}</p>
    </div>
  </div>

  <script>
    // 趋势数据
    const monthlyData = {{monthly_data_json}};
    const dailyData = {{daily_data_json}};
    const hourlyData = {{hourly_data_json}};

    let currentChart = null;
    let currentGranularity = 'monthly';

    // 创建图表
    function createChart(granularity) {
      const ctx = document.getElementById('trendChart').getContext('2d');

      let data, labels;
      if (granularity === 'monthly') {
        data = monthlyData;
        labels = data.map(d => d.month);
      } else if (granularity === 'daily') {
        data = dailyData;
        labels = data.map(d => d.date);
      } else {
        data = hourlyData;
        labels = data.map(d => d.hour + ':00');
      }

      if (currentChart) {
        currentChart.destroy();
      }

      currentChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: '消息数量',
            data: data.map(d => d.count),
            borderColor: 'hsl(222.2, 47.4%, 11.2%)',
            backgroundColor: 'hsla(222.2, 47.4%, 11.2%, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  return `消息数：${context.parsed.y} 条`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                precision: 0
              }
            }
          },
          onClick: (event, elements) => {
            if (elements.length > 0) {
              const index = elements[0].index;
              const dataPoint = data[index];
              alert(`${labels[index]}\n消息数：${dataPoint.count} 条`);
            }
          }
        }
      });
    }

    // 切换粒度
    function changeGranularity(granularity) {
      currentGranularity = granularity;
      createChart(granularity);
    }

    // 初始化
    createChart('monthly');
  </script>
</body>
</html>
```

## 输出格式

```
✅ 互动趋势分析已生成！

📊 统计信息：
- 分析对象：张三
- 时间范围：2023-01-01 至 2024-01-31
- 消息总数：5,678 条

📈 趋势概览：
- 整体趋势：📈 上升 (+23%)
- 峰值月份：2024-01 (789 条)
- 平均每月：473 条
- 活跃天数：298 天

💡 关键洞察：
• 2024年1月达到峰值，可能与项目冲刺有关
• 周末消息量明显减少，工作日为主
• 下午3-5点是最活跃时段

📄 完整报告已保存至：
~/wetrace-exports/trend_zhangsan_20240131.html
```

## 技术要点

### 1. 多层级钻取
- 月度 → 每日 → 每小时
- 点击数据点查看详情
- 平滑的动画过渡

### 2. 趋势识别
- 自动识别上升/下降/稳定趋势
- 计算增长率和变化率
- 标注峰值和低谷

### 3. 数据可视化
- Chart.js 折线图
- 填充区域增强视觉效果
- 响应式设计

## 扩展功能（未来）

- [ ] 预测未来趋势
- [ ] 多人趋势对比
- [ ] 导出为图片/PDF
- [ ] 异常检测和提醒
