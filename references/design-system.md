# Wetrace 页面设计系统

本文档定义了 Wetrace 生成的所有 HTML 页面的统一设计系统，基于 Tailwind CSS 和现代化的设计原则。

## 🎨 设计理念

### 核心原则
1. **简洁优雅**：干净的视觉层次，大量留白
2. **响应式优先**：移动端到桌面端的完美适配
3. **一致性**：统一的间距、颜色和组件样式
4. **可访问性**：符合 WCAG 标准的对比度和交互
5. **性能优化**：轻量级、快速加载

### 技术栈
- **Tailwind CSS v3**：通过 CDN 引入，无需构建
- **Chart.js v4**：数据可视化
- **原生 JavaScript**：交互功能
- **系统字体栈**：无需加载外部字体

---

## 🎨 颜色系统

### CSS 变量定义

```css
:root {
  /* 基础颜色 */
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;

  /* 卡片和容器 */
  --card: 0 0% 100%;
  --card-foreground: 222.2 84% 4.9%;

  /* 主色调 */
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;

  /* 次要色 */
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;

  /* 边框 */
  --border: 214.3 31.8% 91.4%;

  /* 状态颜色 */
  --success: 142 76% 36%;
  --warning: 38 92% 50%;
  --destructive: 0 84.2% 60.2%;
}

/* 暗色模式（可选） */
@media (prefers-color-scheme: dark) {
  :root {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --border: 217.2 32.6% 17.5%;
  }
}
```

### 语义化颜色使用

```css
/* 文本颜色 */
.text-foreground { color: hsl(var(--foreground)); }
.text-muted-foreground { color: hsl(var(--muted-foreground)); }

/* 背景颜色 */
.bg-background { background-color: hsl(var(--background)); }
.bg-card { background-color: hsl(var(--card)); }
.bg-muted { background-color: hsl(var(--muted)); }
.bg-primary { background-color: hsl(var(--primary)); }

/* 边框颜色 */
.border { border-color: hsl(var(--border)); }
```

---

## 📦 组件库

### 1. Card 组件

```css
.card {
  background-color: hsl(var(--card));
  color: hsl(var(--card-foreground));
  border-radius: 0.5rem;
  border: 1px solid hsl(var(--border));
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  transition: all 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

.card-header {
  padding: 1.5rem;
  padding-bottom: 1rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.75rem;
}

.card-description {
  font-size: 0.875rem;
  color: hsl(var(--muted-foreground));
  margin-top: 0.25rem;
}

.card-content {
  padding: 1.5rem;
  padding-top: 0;
}

.card-footer {
  padding: 1.5rem;
  padding-top: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
```

**使用示例**：
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">卡片标题</h3>
    <p class="card-description">卡片描述文本</p>
  </div>
  <div class="card-content">
    <!-- 卡片内容 -->
  </div>
  <div class="card-footer">
    <!-- 卡片底部 -->
  </div>
</div>
```

---

### 2. Badge 组件

```css
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

.badge-success {
  background-color: hsl(var(--success));
  color: white;
}

.badge-warning {
  background-color: hsl(var(--warning));
  color: white;
}

.badge-destructive {
  background-color: hsl(var(--destructive));
  color: white;
}
```

**使用示例**：
```html
<span class="badge badge-primary">主要</span>
<span class="badge badge-muted">次要</span>
<span class="badge badge-success">成功</span>
<span class="badge badge-warning">警告</span>
<span class="badge badge-destructive">危险</span>
```

---

### 3. Button 组件

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  transition: all 0.2s;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background-color: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
}

.btn-primary:hover {
  opacity: 0.9;
}

.btn-outline {
  background-color: transparent;
  border: 1px solid hsl(var(--border));
  color: hsl(var(--foreground));
}

.btn-outline:hover {
  background-color: hsl(var(--muted));
}

.btn-ghost {
  background-color: transparent;
  color: hsl(var(--foreground));
}

.btn-ghost:hover {
  background-color: hsl(var(--muted));
}
```

**使用示例**：
```html
<button class="btn btn-primary">主要按钮</button>
<button class="btn btn-outline">次要按钮</button>
<button class="btn btn-ghost">幽灵按钮</button>
```

---

### 4. Separator 组件

```css
.separator {
  height: 1px;
  background-color: hsl(var(--border));
  margin: 1.5rem 0;
}

.separator-vertical {
  width: 1px;
  height: 100%;
  background-color: hsl(var(--border));
  margin: 0 1.5rem;
}
```

**使用示例**：
```html
<div class="separator"></div>
<div class="separator-vertical"></div>
```

---

### 5. Input 组件

```css
.input {
  display: flex;
  width: 100%;
  border-radius: 0.375rem;
  border: 1px solid hsl(var(--border));
  background-color: transparent;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.input:focus {
  outline: none;
  border-color: hsl(var(--primary));
  box-shadow: 0 0 0 3px hsl(var(--primary) / 0.1);
}

.input::placeholder {
  color: hsl(var(--muted-foreground));
}
```

**使用示例**：
```html
<input type="text" class="input" placeholder="请输入内容">
```

---

## 📐 布局系统

### Container

```css
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

@media (min-width: 640px) {
  .container { max-width: 640px; }
}

@media (min-width: 768px) {
  .container { max-width: 768px; }
}

@media (min-width: 1024px) {
  .container { max-width: 1024px; }
}

@media (min-width: 1280px) {
  .container { max-width: 1280px; }
}

@media (min-width: 1536px) {
  .container { max-width: 1536px; }
}
```

### 间距系统

使用 Tailwind 的间距类：
- `p-{n}`: padding
- `m-{n}`: margin
- `gap-{n}`: gap
- `space-y-{n}`: 垂直间距
- `space-x-{n}`: 水平间距

标准间距值：`0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24`

---

## 📱 响应式设计

### 断点系统

```css
/* 移动端优先 */
/* sm: 640px */
@media (min-width: 640px) { }

/* md: 768px */
@media (min-width: 768px) { }

/* lg: 1024px */
@media (min-width: 1024px) { }

/* xl: 1280px */
@media (min-width: 1280px) { }

/* 2xl: 1536px */
@media (min-width: 1536px) { }
```

### 响应式类使用

```html
<!-- 移动端垂直，桌面端水平 -->
<div class="flex flex-col md:flex-row gap-4">
  ...
</div>

<!-- 移动端全宽，桌面端固定宽度 -->
<div class="w-full md:w-64">
  ...
</div>

<!-- 移动端隐藏，桌面端显示 -->
<div class="hidden md:block">
  ...
</div>
```

---

## 🎭 页面模板

### 基础页面结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{页面标题}}</title>

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- Chart.js (如需图表) -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <!-- 自定义样式 -->
  <style>
    /* 引入上述 CSS 变量和组件样式 */
  </style>
</head>
<body class="bg-background text-foreground antialiased">
  <div class="container mx-auto py-8 px-4 max-w-6xl">
    <!-- 页面头部 -->
    <div class="flex flex-col gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">{{页面标题}}</h1>
        <p class="text-muted-foreground mt-2">{{页面描述}}</p>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <!-- 徽章和元信息 -->
      </div>
    </div>

    <div class="separator mb-8"></div>

    <!-- 主要内容区域 -->
    <div class="space-y-6">
      <!-- 内容卡片 -->
    </div>

    <!-- 页脚 -->
    <div class="mt-12 text-center text-sm text-muted-foreground">
      <p>由 Wetrace 生成 • {{生成时间}}</p>
    </div>
  </div>

  <script>
    // 交互逻辑
  </script>
</body>
</html>
```

---

## 📊 数据可视化

### Chart.js 配置

```javascript
// 通用图表配置
const chartConfig = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        font: {
          family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 12,
      titleFont: {
        size: 14
      },
      bodyFont: {
        size: 13
      }
    }
  }
};

// 颜色方案
const colors = {
  primary: 'hsl(222.2, 47.4%, 11.2%)',
  success: 'hsl(142, 76%, 36%)',
  warning: 'hsl(38, 92%, 50%)',
  destructive: 'hsl(0, 84.2%, 60.2%)',
  muted: 'hsl(210, 40%, 96.1%)'
};
```

---

## 🎨 特殊组件

### 1. 统计卡片

```css
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

.stat-change {
  font-size: 0.75rem;
  margin-top: 0.5rem;
}

.stat-change.positive {
  color: hsl(var(--success));
}

.stat-change.negative {
  color: hsl(var(--destructive));
}
```

### 2. 进度条

```css
.progress {
  width: 100%;
  height: 0.5rem;
  background-color: hsl(var(--muted));
  border-radius: 9999px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: hsl(var(--primary));
  border-radius: 9999px;
  transition: width 0.3s ease;
}
```

### 3. 加载动画

```css
.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid hsl(var(--muted));
  border-top-color: hsl(var(--primary));
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

---

## 💡 最佳实践

### 1. 颜色使用
- ✅ 使用语义化的 CSS 变量
- ✅ 保持足够的对比度（WCAG AA 标准）
- ❌ 避免硬编码颜色值

### 2. 间距
- ✅ 使用统一的间距系统（4px 基数）
- ✅ 保持视觉层次清晰
- ❌ 避免不规则的间距值

### 3. 响应式
- ✅ 移动端优先设计
- ✅ 使用 Tailwind 的响应式类
- ❌ 避免固定宽度和高度

### 4. 性能
- ✅ 使用 CDN 加载外部资源
- ✅ 最小化 JavaScript 代码
- ✅ 懒加载图表和图片
- ❌ 避免过多的 DOM 操作

### 5. 可访问性
- ✅ 使用语义化的 HTML 标签
- ✅ 提供 alt 文本和 aria 标签
- ✅ 支持键盘导航
- ❌ 避免仅依赖颜色传达信息

---

## 📝 代码示例

### 完整的卡片示例

```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title flex items-center gap-2">
      <span>📊</span>
      <span>数据统计</span>
    </h3>
    <p class="card-description">最近 30 天的数据概览</p>
  </div>
  <div class="card-content">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="stat-card">
        <div class="stat-value">1,234</div>
        <div class="stat-label">消息总数</div>
        <div class="stat-change positive">↑ 12%</div>
      </div>
      <!-- 更多统计卡片 -->
    </div>
  </div>
</div>
```

### 响应式布局示例

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div class="card">
    <!-- 卡片 1 -->
  </div>
  <div class="card">
    <!-- 卡片 2 -->
  </div>
  <div class="card">
    <!-- 卡片 3 -->
  </div>
</div>
```

---

## 🔧 工具函数

### 日期格式化

```javascript
function formatDate(date) {
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}
```

### 数字格式化

```javascript
function formatNumber(num) {
  return num.toLocaleString('zh-CN');
}

function formatPercentage(num) {
  return (num * 100).toFixed(1) + '%';
}
```

### 颜色工具

```javascript
function getColorByValue(value, max) {
  const intensity = value / max;
  if (intensity < 0.25) return '#ebedf0';
  if (intensity < 0.5) return '#9be9a8';
  if (intensity < 0.75) return '#40c463';
  return '#30a14e';
}
```

---

## 📚 参考资源

- [Tailwind CSS 文档](https://tailwindcss.com/docs)
- [Chart.js 文档](https://www.chartjs.org/docs/)
- [WCAG 可访问性指南](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Web 文档](https://developer.mozilla.org/)
