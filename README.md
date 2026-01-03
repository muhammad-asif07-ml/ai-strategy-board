# 🧠 AI Strategy Board

An **agentic AI decision-making system** that simulates a real-world executive board using multiple AI agents, structured tools, and **human-in-the-loop approval**.

Built with **Streamlit**, **LangChain**, and **LangGraph**, this project demonstrates advanced agent orchestration, tool usage, and AI governance patterns used in production systems.

---

## 🚀 What This Project Does

The AI Strategy Board helps founders, product managers, and executives make **data-informed strategic decisions** by:

- Running **multiple specialized AI agents**
- Using **structured tools** for analysis (finance, risk, scenarios)
- Enforcing **human approval** for sensitive decisions
- Producing a **transparent decision report** with full execution history

This is **not a chatbot** — it is a true **agentic AI system**.

---

## 🧩 Agents Involved

Each agent has a clear role and tool access:

### 🧠 Market Advisor
- Analyzes market context and competition
- Uses structured market analysis tools

### ⚠️ Risk Advisor
- Evaluates budget vs risk tolerance
- Triggers human approval for low-risk tolerance

### 💰 Finance Advisor
- Performs financial projections
- Simulates business scenarios
- Compares low-risk vs high-risk strategies

### 👨‍💼 CEO (Strategy Agent)
- Synthesizes all board opinions
- Produces the final strategic recommendation

---

## 🛠️ Tools Used

This project uses **real tools**, not just text outputs:

- `analyze_market` → Market insights
- `assess_risk` → Risk evaluation
- `financial_projection` → ROI & budget analysis
- `simulate_business_scenario` → ROI, loss, break-even simulation
- `compare_business_scenarios` → Low-risk vs high-risk comparison

All tool outputs are:
- Stored in shared state
- Displayed clearly in the UI
- Logged in full execution history

---

## 🧑‍⚖️ Human-in-the-Loop Approval

When **risk tolerance is LOW**, the system:

1. Pauses execution
2. Requests human approval
3. Accepts:
   - Approve
   - Reject
   - Request changes
4. Resumes execution from the same state

This demonstrates **enterprise-grade AI governance**.

---

## 🖥️ User Interface (Streamlit)

The UI provides:

- Business input form
- Expandable board opinions
- Visual scenario comparison tables
- KPI metrics (ROI, loss, break-even)
- Tool transparency
- Full execution history
- JSON decision report export

---

## 🏗️ Architecture Overview


