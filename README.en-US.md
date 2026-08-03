

# Wetrace Skill - WeChat Chat Log Analysis Assistant

<div align="center">

![Wetrace](https://img.shields.io/badge/Wetrace-微信分析-brightgreen)
![Claude](https://img.shields.io/badge/Claude-AI%20Skill-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Powerful WeChat Chat Log Analysis Capabilities for Claude Code**

[Features](#-功能特性) • [Quick Start](#-快速开始) • [Usage Examples](#-使用示例) • [Visualization Features](#-可视化功能) • [Documentation](#-文档)

</div>

---

## 📖 Introduction

Wetrace Skill is a skill package designed specifically for Claude Code, enabling AI assistants to query, analyze, and visualize WeChat chat logs. Through natural language interaction, effortlessly complete complex data analysis tasks and generate beautifully designed visualization reports.

> **⚠️ Important Notice**
> - This Skill relies on the [Wetrace](https://github.com/afumu/wetrace) service
> - **Windows platform only** (WeChat database is located on Windows systems)
> - You must install and run the Wetrace service before using this Skill

### Core Capabilities

- 🔍 **Smart Query**: Query chat logs, contacts, and groups via natural language
- 📊 **Data Analysis**: Analyze chat patterns, activity trends, and relationship dynamics
- 🎨 **Visualization Reports**: Generate 8 types of beautifully designed HTML visualization pages
- 💾 **Multi-format Export**: Supports HTML, PDF, DOCX, CSV, XLSX, and more
- 🤖 **AI Insights**: Provides smart summaries, todo extraction, sentiment analysis, and more
- 📈 **Customer Management**: CRM health analysis, follow-up reminders

---

## ✨ Features

### Basic Features

| Feature | Description | Trigger Example |
|------|------|-----------|
| 📝 Query Messages | View chat logs with specific contacts | "View my chat with Zhang San" |
| 🔎 Search Messages | Search cross-session messages by keyword | "Search messages containing 'project'" |
| 📊 Data Statistics | Analyze chat frequency, active hours | "Statistics on the most active time period" |
| 💾 Export Data | Export chat logs in various formats | "Export chat logs as PDF" |
| 💡 Smart Insights | Comprehensive analysis and recommendations | "Summarize my social situation" |

### Visualization Features (8 Types)

| Feature | Description | Trigger |
|------|------|--------|
| 🤖 Smart Summary | AI summarizes chat logs | "Summarize chat logs" |
| ✅ Todo Extraction | Automatically extract task lists | "Extract todos" |
| 🔥 Activity Heatmap | 24×7 time distribution heatmap | "Generate activity heatmap" |
| 📈 Trend Analysis | Multi-level time trend chart | "Analyze interaction trends" |
| 📋 Weekly/Monthly Report | Automatically generate weekly/monthly reports | "Generate this week's report" |
| 📊 Data Dashboard | Comprehensive data visualization panel | "Generate data dashboard" |
| 💬 Conversation Summary | Intelligently categorize conversation content | "Generate conversation summary" |
| 💼 Customer Health | CRM relationship health analysis | "Analyze customer health" |

---

## 🚀 Quick Start

### System Requirements

- **Operating System**: Windows 10/11 (Required)
- **Reason**: WeChat database only exists on Windows systems

### Prerequisites

1. **Wetrace Service**: Must install and run [Wetrace](https://github.com/afumu/wetrace) first
   ```bash
   # Download and run Wetrace
   # Please refer to the Wetrace project documentation for detailed installation steps
   ```
2. **Claude Code CLI**: Claude Code installed (Windows version)
3. **WeChat Database**: Decrypted WeChat database
4. **Wetrace Service Running**: Ensure Wetrace service is running at `http://127.0.0.1:5200`

### Installation Steps
#### Install from Source

```bash
# Clone the repository
git clone https://github.com/afumu/wetrace-skill.git

# Copy wetrace-skill to the .claude/skills directory
```

### Verify Installation

Type in Claude Code:

```
View my WeChat contacts
```

If the skill is working properly, Claude will start querying your WeChat data.

---

## 💡 Usage Examples

### Example 1: Query Chat Logs

**User Input:**
```
View my chat with Zhang San from the last month
```

**Claude Response:**
```
Fetching data...
✓ Retrieved 156 messages
✓ Time range: 2024-01-01 to 2024-01-31

## Query Results: Chat Logs with Zhang San

**Total Messages:** 156
**Active Days:** 28
**Daily Average:** 5.6 messages

### Recent Messages
1. [2024-01-31 14:23] Zhang San: See you tomorrow
2. [2024-01-31 10:15] Me: Okay, tomorrow at 2 PM
...
```

### Example 2: Generate Visualization Report

**User Input:**
```
Generate an activity heatmap for my chat with Zhang San
```

**Claude Response:**
```
Analyzing data...
✓ Analyzed 1,234 messages
✓ Covers 31 days

Generating heatmap...
✓ 24×7 heatmap generation complete

---

✅ Heatmap generated!

🌟 Most active period: Wednesday 14:00 (89 messages)

💡 Insight: Workday mornings and afternoons are the best times for communication

📄 View full heatmap:
~/wetrace-exports/heatmap_zhangsan_20240131.html
```

### Example 3: Smart Todo Extraction

**User Input:**
```
Extract recent todos from my chat with the project team
```

**Claude Response:**
```
Analyzing chat logs...
✓ Analyzed 256 messages
✓ Extracted 12 todos

---

✅ Todo extraction complete!

📊 Statistics: 12 tasks (3 high priority, 8 with deadlines)

🔥 High Priority Tasks Preview:
1. Complete project documentation - ⏰ 2024-01-31
2. Submit quarterly report - ⏰ 2024-01-25
3. Fix online Bug - 🚨 Urgent

📄 Full list: ~/wetrace-exports/todos_project_20240131.html
```

---

## 🎨 Visualization Features

All generated HTML pages have the following characteristics:

- ✅ **Standalone**: No server required, double-click to open in a browser
- ✅ **Responsive Design**: Perfectly adapted for desktop, tablet, and mobile
- ✅ **Modern Styling**: Beautiful design based on Tailwind CSS
- ✅ **Interactive Charts**: Data visualization using Chart.js
- ✅ **Unified Design System**: Consistent colors, components, and layouts
- ✅ **Easy to Share**: Can be directly sent to others for viewing

### 1. Smart Summary Generation

Converts chat logs into concise smart summaries, including AI summaries, key points, and data statistics.

**Triggers:** Summarize chat logs, generate summary, smart summary

**Example Output:**
- 📊 Total messages, active days, daily average
- 🤖 AI smart summary
- 💡 Key points list
- 😊 Overall sentiment analysis

### 2. Todo Extraction

Automatically extracts todos from chat logs to generate structured task lists.

**Triggers:** Extract todos, find tasks, todos

**Example Output:**
- 🔥 High priority tasks
- ⚡ Medium priority tasks
- 📌 Low priority tasks
- ⏰ Deadlines and assignees
- ✅ Interactive checkboxes

### 3. Chat Activity Heatmap

Generates a GitHub-style 24×7 activity heatmap to intuitively display the best communication times.

**Triggers:** Activity heatmap, chat time distribution

**Example Output:**
- 🔥 24×7 heatmap matrix
- 🌟 Top active periods ranking
- 📊 Activity statistics
- 💡 AI communication suggestions

### 4. Interaction Trend Analysis

Generates a drill-down multi-level time trend chart (Month → Day → Hour).

**Triggers:** Trend analysis, interaction trends

**Example Output:**
- 📈 Switchable trend charts (Monthly/Daily/Hourly)
- 📊 Peaks, averages, growth rates
- 💡 Trend insights and recommendations

### 5. Smart Weekly/Monthly Reports

Automatically generates beautifully designed weekly or monthly reports, including data statistics, AI summaries, and visualization charts.

**Triggers:** Generate weekly report, generate monthly report

**Example Output:**
- 🎨 Gradient cover design
- 📊 Core data statistics
- 🤖 AI smart summary
- 📈 Message trend chart
- 👥 Top 10 contacts ranking
- 💡 Key insights

### 6. Data Dashboard

Generates an interactive data dashboard integrating multiple visualization components.

**Triggers:** Generate dashboard, data overview

**Example Output:**
- 📊 Core metric cards (total messages, number of contacts, daily average)
- 🍩 Message type distribution pie chart
- 📊 Hourly activity bar chart
- 🕸️ Day-of-week activity radar chart
- 👥 Top contacts ranking
- 💡 Quick insights panel

### 7. Smart Conversation Summary

Uses AI to intelligently categorize and summarize chat logs, automatically extracting key information.

**Triggers:** Conversation summary, smart summary, categorized summary

**Example Output:**
- 💼 Work discussion category
- 🏠 Daily chat category
- ⚡ Important decision records
- ✅ Todo list
- 📌 Key information extraction (time, address, amount, contact info)

### 8. Customer Relationship Health

Generates a customer relationship health dashboard to help manage customer relations.

**Triggers:** Customer health, CRM dashboard

**Example Output:**
- 💚 Healthy customer list
- 💛 Customers needing attention
- ❤️ Urgent follow-up customers
- 📊 Health score algorithm (0-100)
- 💬 Smart follow-up suggestions
- ⏰ Best contact time

---

## 📚 Documentation

### Core Documentation

- **[SKILL.md](SKILL.md)** - Main skill document, containing core workflows
- **[API Documentation](references/api.md)** - Complete Wetrace API reference
- **[Design System](references/design-system.md)** - HTML page design specifications
- **[Analysis Prompts](references/analysis-prompts.md)** - AI analysis templates

### Visualization Feature Documentation

- [Smart Summary Generation](references/01-smart-summary.md)
- [Todo Extraction](references/02-todo-extraction.md)
- [Activity Heatmap](references/03-activity-heatmap.md)
- [Interaction Trend Analysis](references/04-trend-analysis.md)
- [Smart Weekly/Monthly Report](references/05-weekly-monthly-report.md)
- [Data Dashboard](references/06-dashboard.md)
- [Smart Conversation Summary](references/07-conversation-summary.md)
- [Customer Relationship Health](references/08-customer-health.md)

---

## 🔧 Advanced Configuration

### Custom API Address

If your Wetrace service is running on a non-default address, you can specify it during use:

```
Use http://192.168.1.100:5200 as the Wetrace service address
```

### Custom Export Directory

The default export directory is `~/wetrace-exports/`, you can specify another directory during use:

```
Export reports to ~/Documents/wetrace-reports/
```

### Time Range Formats

Supports multiple time range formats:

- **Chinese**: Last week, last month, this year
- **English**: last week, last month, this year
- **Absolute Time**: 2024-01-01~2024-01-31
- **Relative Days**: last 7 days, last 30 days

---

## 🛠️ Troubleshooting

### Issue 1: Unable to connect to Wetrace service

**Symptom:** Claude prompts "Server not responding"

**Solution:**
1. Confirm Wetrace service is running: `ps aux | grep wetrace`
2. Check service address: `curl http://127.0.0.1:5200/api/v1/health`
3. If service is not running, start it: `./wetrace`

### Issue 2: Contact or session not found

**Symptom:** Claude prompts "Specified session not found"

**Solution:**
1. Confirm the contact name spelling is correct
2. Try using the remark name or nickname
3. First query all sessions: `Show all contacts`

### Issue 3: Generated HTML page cannot be opened

**Symptom:** Double-clicking the HTML file does nothing

**Solution:**
1. Right-click file → Open with → Choose browser
2. Check if the file path contains special characters
3. Confirm the file is fully generated (check file size)

### Issue 4: API returns 404 error

**Symptom:** Claude prompts "API returns 404"

**Solution:**
1. Confirm WeChat database is loaded
2. Check if Wetrace service version supports this API
3. View Wetrace service logs

---

## 🤝 Contributing Guide

Contributions of code, bug reports, or suggestions are welcome!

### Reporting Issues

If you find a bug or have a feature suggestion, please:

1. Create a new issue in [GitHub Issues](https://github.com/afumu/wetrace-skill/issues)
2. Provide a detailed issue description and reproduction steps
3. Attach relevant error messages or screenshots

### Contributing Code

1. Fork this repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Create a Pull Request

### Development Guide

- Follow existing code style and documentation format
- Ensure all documentation is in English
- Test your changes
- Update relevant documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- [Claude Code](https://claude.ai/code) - AI coding assistant
- [Wetrace](https://github.com/afumu/wetrace) - WeChat data analysis tool
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [Chart.js](https://www.chartjs.org/) - Chart library
