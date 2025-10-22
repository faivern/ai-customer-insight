# 🧠 AI Customer Insight

**AI Customer Insight** is a command-line tool that turns raw customer feedback into structured business insights using the OpenAI API.

It reads a CSV file with customer reviews or survey feedback, analyzes the data, and generates a **Markdown report** summarizing:
- Overall sentiment and key themes  
- Suggested improvements and quick wins  
- Long-term strategic actions  

This helps businesses quickly understand what customers value and where improvements are needed — **without manually reading every comment**.

---

## 🚀 Problem it solves

Organizations collect large amounts of customer feedback, but manual analysis is time-consuming and inconsistent.  
This tool automates that process by combining simple data handling (via CSV) with AI-driven summarization — producing **consistent, actionable insights** in seconds.

---

## ⚙️ Setup

Follow these steps to get started locally.

### 1️⃣ Clone and enter the project
```bash
git clone https://github.com/yourusername/ai-customer-insight.git
cd ai-customer-insight
```

### 2️⃣ Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
python -m pip install -U pip
python -m pip install -r requirements.txt
```

### 4️⃣ Add your OpenAI API key

Create a `.env` file in the project root and add your key:

```
OPENAI_API_KEY=sk-your-secret-key
```

Recommended scopes for a restricted key:

- Models → Read
- Responses API → Write

(If using an older SDK with Chat Completions, also enable Chat Completions → Write.)

---

▶️ Usage

Run the CLI with a path to your feedback CSV:

```bash
python main.py examples/customerFeedback.csv --out-path report.md
```

Options
| Flag | Description | Default |
|---|---:|---|
| --out-path | Path to save Markdown report | report.md |
| --text-col | Column name for feedback text | feedback |
| --rating-col | Column name for rating | rating |
| --date-col | Column name for date | date |
| --sample-size | Limit number of samples sent to AI | 200 |

### 🧩 Example
Input CSV
```
id,date,rating,feedback
1,2025-10-20,5,"Love the app, super easy to use!"
2,2025-10-19,2,"Checkout fails on mobile sometimes."
3,2025-10-18,4,"Support is great, but shipping was slow."
4,2025-10-18,1,"Couldn't log in after the update."
5,2025-10-17,5,"Fast delivery and friendly customer service!"
```

Run
```bash
python main.py examples/customerFeedback.csv --out-path report.md
```

Output (report.md)
```
# Customer Insight Report
Generated: 2025-10-21

## Overview
- **Total responses:** 5
- **Average rating:** 3.4 / 5

---

## TL;DR
Customers love the simplicity, but reliability issues in checkout and login frustrate users. Shipping delays reduce satisfaction. Prioritize stability and transparency in order processing.

## Top Themes
- Easy-to-use interface
- Checkout and login issues
- Shipping delays
- Great customer support

## Recommended Improvements
- Fix checkout flow and login errors
- Communicate shipping timelines
- Keep improving customer support quality

## Quick Wins
- Add retry button for failed checkouts
- Improve login error feedback

## Long-Term Actions
- Strengthen backend reliability
- Optimize logistics chain

🧠 Summary

AI Customer Insight automatically transforms feedback data into actionable intelligence —
giving teams a fast, objective overview of customer experience trends without manual review.

