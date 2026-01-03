import os
import uuid
import json
import streamlit as st

from graphs.ops_workflow import build_workflow
from state.shared_state import StrategyState

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Strategy Board",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Strategy Board")
st.caption(
    "Agentic AI • Human-in-the-loop • Tool Transparency • Scenario Intelligence"
)

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔐 OpenAI Configuration")

api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-xxxxxxxxxxxx"
)

if not api_key:
    st.sidebar.warning("Enter API key to continue")
    st.stop()

os.environ["OPENAI_API_KEY"] = api_key

# ---------------- THREAD ID ----------------
st.sidebar.header("🧵 Session / Time Travel")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

thread_id = st.sidebar.text_input(
    "Thread ID",
    value=st.session_state.thread_id,
    help="Same ID = same execution timeline"
)

st.session_state.thread_id = thread_id

# ---------------- INPUT FORM ----------------
st.subheader("📌 Business Inputs")

with st.form("inputs_form"):
    business_goal = st.text_input(
        "Business Goal",
        placeholder="Launch low-cost B2B SaaS analytics tool"
    )

    market_context = st.text_area(
        "Market Context",
        placeholder="UK & Netherlands, strong SaaS adoption, high competition"
    )

    budget = st.number_input(
        "Budget (USD)",
        min_value=0.0,
        step=1000.0
    )

    risk_tolerance = st.selectbox(
        "Risk Tolerance",
        ["Low", "Medium", "High"],
        help="Low risk requires human approval"
    )

    submit = st.form_submit_button("🚀 Run Strategy Analysis")

# ---------------- RUN GRAPH ----------------
if submit:
    graph = build_workflow()

    initial_state = StrategyState(
        business_goal=business_goal,
        market_context=market_context,
        budget=budget,
        risk_tolerance=risk_tolerance
    )

    result = graph.invoke(
        initial_state,
        config={"configurable": {"thread_id": thread_id}}
    )

    if isinstance(result, list):
        result = result[-1]

    # ---- HUMAN APPROVAL ----
    if "__interrupt__" in result:
        interrupt = result["__interrupt__"][0].value
        st.warning(interrupt.get("message", "Human approval required"))

        decision = st.radio(
            "Approve Strategy?",
            ["Approve", "Reject", "Request Changes"]
        )

        notes = st.text_area(
            "Human Notes (optional)"
        )

        if st.button("Submit Decision"):
            resumed_state = StrategyState(**interrupt["state"])
            resumed_state.human_decision = decision
            resumed_state.human_notes = notes

            final = graph.invoke(
                resumed_state,
                config={"configurable": {"thread_id": thread_id}}
            )

            if isinstance(final, list):
                final = final[-1]

            st.session_state.final_state = StrategyState(**final)
    else:
        st.session_state.final_state = StrategyState(**result)

# ---------------- OUTPUT ----------------
if "final_state" in st.session_state:
    state = st.session_state.final_state

    st.success("✅ Analysis Complete")

    # -------- BOARD OPINIONS --------
    st.subheader("🧠 Board Opinions")

    board_opinions = state.board_opinions or []

    if not board_opinions:
        st.info("No board opinions generated.")
    else:
        for op in board_opinions:
            with st.expander(f"{op.agent} ({int(op.confidence * 100)}%)"):
                st.write(op.opinion)

    # -------- FINAL DECISION --------
    st.subheader("🏁 Final Recommendation")
    st.info(state.final_recommendation or "No recommendation generated.")

    # -------- TOOL OUTPUTS --------
    st.subheader("📊 Decision Insights (Tools)")

    tools = state.tool_outputs or {}

    if not tools:
        st.info("No tools were triggered in this run.")

    # ---- Scenario Comparison ----
    if "compare_business_scenarios" in tools:
        st.markdown("### 🧮 Scenario Comparison")

        comparison = tools["compare_business_scenarios"]

        st.table({
            "Low Risk Strategy": comparison.get("low_risk_strategy", {}),
            "High Risk Strategy": comparison.get("high_risk_strategy", {})
        })

        if comparison.get("final_hint"):
            st.info(comparison["final_hint"])

    # ---- Scenario Simulation ----
    if "simulate_business_scenario" in tools:
        st.markdown("### 📈 Scenario Simulation")

        sim = tools["simulate_business_scenario"]
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Best Case ROI", sim.get("best_case_roi", "N/A"))
        c2.metric("Worst Case Loss", sim.get("worst_case_loss", "N/A"))
        c3.metric("Break-even (Months)", sim.get("break_even_month", "N/A"))
        c4.metric("Risk Level", sim.get("risk_level", "N/A"))

    # ---- Other Tools (SAFE RENDERING) ----
    for tool, output in tools.items():
        if tool not in ["compare_business_scenarios", "simulate_business_scenario"]:
            st.markdown(f"### 🔧 {tool.replace('_', ' ').title()}")

            if isinstance(output, dict):
                st.json(output)
            else:
                st.success(output)

    # -------- DOWNLOAD SECTION --------
    st.subheader("📥 Export Decision Report")

    report = {
        "inputs": {
            "business_goal": state.business_goal,
            "market_context": state.market_context,
            "budget": state.budget,
            "risk_tolerance": state.risk_tolerance,
        },
        "board_opinions": [op.dict() for op in board_opinions],
        "tool_outputs": tools,
        "final_recommendation": state.final_recommendation,
        "history": state.history,
    }

    st.download_button(
        "⬇️ Download JSON Report",
        data=json.dumps(report, indent=2),
        file_name="ai_strategy_report.json",
        mime="application/json"
    )

    with st.expander("🧾 Full Execution History"):
        st.json(state.history)
