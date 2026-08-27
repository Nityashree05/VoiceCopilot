# 🎙️ VoiceCopilot

### AI-Powered Customer Feedback Analysis & Product Decision Support

VoiceCopilot transforms raw customer feedback into **actionable product insights** using sentiment analysis, theme discovery, customer evidence, and AI-generated solution recommendations.

Instead of manually reading hundreds of customer reviews, VoiceCopilot helps product teams quickly understand **what customers like, what frustrates them, and what should be improved**.

---

## 🚀 Overview

Customer feedback often contains valuable information, but manually analyzing large amounts of feedback is time-consuming.

VoiceCopilot provides an end-to-end feedback analysis pipeline:

**Customer Feedback → Sentiment Analysis → Theme Discovery → Customer Evidence → Insights → AI Solutions**

The application combines traditional NLP techniques with generative AI to turn unstructured feedback into structured product intelligence.

---

## ✨ Key Features

### 📂 1. Customer Feedback Upload

Upload customer feedback directly through the Streamlit interface.

Supported formats:

- CSV
- Excel (`.xlsx`)
- Text (`.txt`)

The uploaded data is automatically processed and prepared for analysis.

---

### 😊 2. Sentiment Analysis

Each customer review is analyzed and classified as:

- 🟢 Positive
- ⚪ Neutral
- 🔴 Negative

The dashboard displays the overall sentiment distribution using easy-to-understand percentage cards and visualizations.

Each review also receives a sentiment score.

---

### 🔍 3. Automatic Theme Discovery

VoiceCopilot automatically identifies the most important recurring topics in customer feedback.

For example:

- Payment & Checkout
- App Performance
- Customer Support
- Delivery & Tracking
- Pricing

Each theme displays:

- Theme name
- Important keywords
- Number of related reviews
- Percentage of total feedback

Themes are presented using expandable sections to keep the dashboard clean and easy to navigate.

---

### 💬 4. Customer Evidence

VoiceCopilot doesn't just tell you **what the theme is**.

It also provides representative customer reviews as evidence.

This allows product teams to understand the actual customer experience behind each identified theme.

Example:

> "Payment failed three times when I tried to checkout."

This makes the insights **evidence-backed rather than purely statistical**.

---

### 💡 5. Key Insights

The application evaluates discovered themes and highlights areas that deserve product attention.

Insights can help identify:

- High-impact customer problems
- Areas causing customer frustration
- Frequently mentioned issues
- Opportunities for product improvement

---

### 🤖 6. AI-Generated Solutions

VoiceCopilot uses Google's Gemini API to generate potential solutions based on customer evidence.

For each important theme, the AI can propose:

- Possible solutions
- Solution descriptions
- Advantages
- Potential drawbacks

The generated solutions are intended to **support product decision-making**, not replace human judgment.

---

### 🧠 7. Human-in-the-Loop Decision Support

VoiceCopilot follows a human-in-the-loop approach.

The AI analyzes feedback and proposes alternatives, while the **final product decision remains with the human decision-maker**.

This helps combine:

**AI speed + Customer evidence + Human judgment**

---

## 🏗️ Project Architecture

```text
                    ┌──────────────────────┐
                    │  Customer Feedback   │
                    │   CSV / XLSX / TXT   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Data Processing    │
                    │  data_processor.py   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Sentiment Analysis  │
                    │    sentiment.py      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Theme Discovery    │
                    │      themes.py       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Customer Evidence    │
                    │     evidence.py      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Insight Analysis   │
                    │      insights.py     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ AI Recommendations   │
                    │ recommendations.py   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Streamlit UI       │
                    │       app.py         │
                    └──────────────────────┘
