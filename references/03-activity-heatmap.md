# 聊天活跃度热力图 Skill

## 触发关键词
- "活跃度热力图"
- "聊天时间分布"
- "activity heatmap"
- "时间热力图"
- "活跃时段分析"

## 功能描述
生成 24×7 聊天活跃度热力图，直观展示一周内每个小时的聊天活跃度，帮助用户了解最佳沟通时间。

## API 依赖
- `GET /analysis/hourly` - 每小时活跃度分析
- `GET /analysis/weekday` - 星期活跃度分析

## 工作流程

### 1. 参数收集
- **会话 ID** (talker_id): 可选，不填则分析全局数据
- **时间范围** (time_range): 可选，默认最近 30 天

### 2. 数据获取
```javascript
// 1. 获取每小时活跃度
GET /analysis/hourly?talker_id={talker_id}&time_range={time_range}
// 返回：[{hour: 0, count: 10}, {hour: 1, count: 5}, ...]

// 2. 获取星期活跃度
GET /analysis/weekday?talker_id={talker_id}&time_range={time_range}
// 返回：[{weekday: 0, count: 100}, {weekday: 1, count: 120}, ...]
```

### 3. 数据处理
```javascript
// 构建 24×7 矩阵
const heatmapData = [];
for (let day = 0; day < 7; day++) {
  for (let hour = 0; hour < 24; hour++) {
    heatmapData.push({
      day: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][day],
      hour: hour,
      value: getMessageCount(day, hour), // 从 API 数据计算
      intensity: normalizeValue(getMessageCount(day, hour)) // 0-1 归一化
    });
  }
}
```

### 4. HTML 页面生成

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>聊天活跃度热力图 - {{contact_name}}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-chart-matrix@2.0.1"></script>
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

    .heatmap-cell {
      aspect-ratio: 1;
      border-radius: 0.25rem;
      transition: all 0.2s;
      cursor: pointer;
    }

    .heatmap-cell:hover {
      transform: scale(1.1);
      box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }

    .legend-item {
      display: inline-block;
      width: 40px;
      height: 20px;
      border-radius: 0.25rem;
    }
  </style>
</head>
<body class="bg-background text-foreground antialiased">
  <div class="container mx-auto py-8 px-4 max-w-6xl">
    <!-- 页面头部 -->
    <div class="flex flex-col gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">🔥 聊天活跃度热力图</h1>
        <p class="text-muted-foreground mt-2">{{description}}</p>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <span class="badge">📅 {{date_range}}</span>
        <span class="badge">💬 {{total_messages}} 条消息</span>
        <span class="badge">⏰ 最活跃时段：{{peak_time}}</span>
      </div>
    </div>

    <div class="separator mb-8"></div>

    <!-- 热力图卡片 -->
    <div class="card p-6 mb-6">
      <div class="mb-6">
        <h2 class="text-xl font-semibold mb-2">24×7 活跃度分布</h2>
        <p class="text-sm text-muted-foreground">颜色越深表示该时段消息越多</p>
      </div>

      <!-- 热力图容器 -->
      <div class="overflow-x-auto">
        <div style="min-width: 800px;">
          <canvas id="heatmapChart" height="400"></canvas>
        </div>
      </div>

      <!-- 图例 -->
      <div class="mt-6 flex items-center justify-center gap-2">
        <span class="text-sm text-muted-foreground">少</span>
        <div class="legend-item" style="background: #ebedf0;"></div>
        <div class="legend-item" style="background: #9be9a8;"></div>
        <div class="legend-item" style="background: #40c463;"></div>
        <div class="legend-item" style="background: #30a14e;"></div>
        <div class="legend-item" style="background: #216e39;"></div>
        <span class="text-sm text-muted-foreground">多</span>
      </div>
    </div>

    <!-- 洞察卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <!-- 最活跃时段 -->
      <div class="card p-6">
        <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <span>🌟</span>
          <span>最活跃时段</span>
        </h3>
        <div class="space-y-3">
          {{#each peak_hours}}
          <div class="flex items-center justify-between">
            <span class="text-foreground">{{day}} {{hour}}:00</span>
            <span class="font-semibold text-primary">{{count}} 条</span>
          </div>
          {{/each}}
        </div>
      </div>

      <!-- 活跃度统计 -->
      <div class="card p-6">
        <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <span>📊</span>
          <span>活跃度统计</span>
        </h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-muted-foreground">最活跃的一天</span>
            <span class="font-semibold">{{most_active_day}}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-muted-foreground">最活跃的时段</span>
            <span class="font-semibold">{{most_active_hour}}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-muted-foreground">平均每小时</span>
            <span class="font-semibold">{{avg_per_hour}} 条</span>
          </div>
        </div>
      </div>
    </div>

    <!-- AI 洞察 -->
    <div class="card p-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
        <span>💡</span>
        <span>AI 洞察</span>
      </h3>
      <div class="prose prose-sm max-w-none">
        <p class="text-foreground">{{ai_insights}}</p>
      </div>
    </div>

    <!-- 页脚 -->
    <div class="mt-12 text-center text-sm text-muted-foreground">
      <p>由 Wetrace 生成 • {{generation_time}}</p>
    </div>
  </div>

  <script>
    // 热力图数据
    const heatmapData = {{heatmap_data_json}};

    // 配置 Chart.js
    const ctx = document.getElementById('heatmapChart').getContext('2d');

    // 准备数据
    const data = {
      datasets: [{
        label: '消息数量',
        data: heatmapData.map(d => ({
          x: d.hour,
          y: d.day,
          v: d.value
        })),
        backgroundColor(context) {
          const value = context.dataset.data[context.dataIndex].v;
          const max = Math.max(...heatmapData.map(d => d.value));
          const intensity = value / max;

          // GitHub 风格颜色
          if (intensity === 0) return '#ebedf0';
          if (intensity < 0.25) return '#9be9a8';
          if (intensity < 0.5) return '#40c463';
          if (intensity < 0.75) return '#30a14e';
          return '#216e39';
        },
        borderWidth: 2,
        borderColor: '#fff',
        width: ({chart}) => (chart.chartArea || {}).width / 24 - 2,
        height: ({chart}) => (chart.chartArea || {}).height / 7 - 2
      }]
    };

    // 创建图表
    new Chart(ctx, {
      type: 'matrix',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              title() {
                return '';
              },
              label(context) {
                const d = heatmapData[context.dataIndex];
                return `${d.day} ${d.hour}:00 - ${d.value} 条消息`;
              }
            }
          }
        },
        scales: {
          x: {
            type: 'linear',
            min: 0,
                max: 23,
            ticks: {
              stepSize: 1,
              callback: (value) => value + ':00'
            },
            grid: {
              display: false
            }
          },
          y: {
            type: 'category',
            labels: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
            offset: true,
            grid: {
              display: false
            }
          }
        }
      }
    });
  </script>
</body>
</html>
```

### 5. AI 洞察生成
```javascript
// 使用 analysis-prompts.md 中的模板生成洞察
const insights = generateInsights({
  peak_hours: topHours,
  most_active_day: mostActiveDay,
  pattern: detectPattern(heatmapData)
});

// 示例洞察
// "您与张三的沟通主要集中在工作日的上午 10-12 点和下午 3-5 点，
//  这表明你们的沟通以工作讨论为主。周末的沟通较少，建议在工作日
//  的活跃时段进行重要事项的沟通。"
```

## 输出格式

```
✅ 聊天活跃度热力图已生成！

📊 统计信息：
- 分析对象：张三
- 时间范围：2024-01-01 至 2024-01-31
- 消息总数：1,234 条

🌟 最活跃时段：
1. 周三 14:00 - 89 条
2. 周二 10:00 - 76 条
3. 周四 15:00 - 72 条

💡 AI 洞察：
您与张三的沟通主要集中在工作日的上午和下午，周末较少。
建议在工作日的 10-12 点和 14-16 点进行重要沟通。

📄 完整热力图已保存至：
~/wetrace-exports/heatmap_zhangsan_20240131.html
```

## 示例对话

**用户输入**：
```
生成我和张三的聊天活跃度热力图
```

**Skill 响应**：
```
好的，我来生成与张三的聊天活跃度热力图。

正在分析数据...
✓ 已分析 1,234 条消息
✓ 覆盖 31 天

正在生成热力图...
✓ 24×7 热力图生成完成

---

✅ 热力图已生成！

🌟 最活跃时段：周三 14:00（89 条消息）

💡 洞察：工作日上午和下午是最佳沟通时间

📄 查看完整热力图：
~/wetrace-exports/heatmap_zhangsan_20240131.html
```

## 技术要点

### 1. 数据可视化
- 使用 Chart.js Matrix 插件
- GitHub 风格的颜色方案
- 响应式设计

### 2. 交互功能
- 悬停显示详细数据
- 点击单元格高亮
- 缩放和平移支持

### 3. 性能优化
- 数据归一化处理
- Canvas 渲染优化
- 懒加载图表库

## 扩展功能（未来）

- [ ] 支持多人对比热力图
- [ ] 导出为图片格式
- [ ] 自定义颜色主题
- [ ] 按月份查看历史热力图
- [ ] 活跃度趋势预测
