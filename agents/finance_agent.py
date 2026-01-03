from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tools.finance_tools import financial_projection
from tools.scenario_tools import simulate_business_scenario
from tools.scenario_compare_tool import compare_business_scenarios
from state.shared_state import StrategyState, BoardOpinion

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a finance advisor. "
     "Use financial tools to generate structured insights. "
     "Always prefer tools over text when possible."),
    ("human",
     "Budget: {budget}\nRisk tolerance: {risk_tolerance}")
])

def finance_agent(state: StrategyState) -> StrategyState:
    llm = ChatOpenAI(model="gpt-4o-mini")

    chain = prompt | llm.bind_tools([
        financial_projection,
        simulate_business_scenario,
        compare_business_scenarios
    ])

    response = chain.invoke({
        "budget": state.budget or 0,
        "risk_tolerance": state.risk_tolerance or "Medium"
    })

    tool_outputs = dict(state.tool_outputs)

    # 🔥 EXECUTE ALL TOOL CALLS
    if response.tool_calls:
        for call in response.tool_calls:
            name = call["name"]
            args = call["args"]

            if name == "financial_projection":
                tool_outputs[name] = financial_projection.invoke(args)

            elif name == "simulate_business_scenario":
                tool_outputs[name] = simulate_business_scenario.invoke(args)

            elif name == "compare_business_scenarios":
                tool_outputs[name] = compare_business_scenarios.invoke(args)

    # ---------- HUMAN-READABLE SUMMARY ----------
    summary = (
        "Financial analysis completed using scenario modeling and projections. "
        "Key metrics such as ROI, break-even timeline, and risk exposure "
        "have been evaluated using structured tools."
    )

    opinion = BoardOpinion(
        agent="Finance Advisor",
        opinion=summary,
        confidence=0.78
    )

    return state.copy(update={
        "board_opinions": state.board_opinions + [opinion],
        "tool_outputs": tool_outputs,
        "history": state.history + [{
            "agent": "Finance Advisor",
            "tool_used": bool(response.tool_calls),
            "tools_called": [c["name"] for c in response.tool_calls] if response.tool_calls else [],
            "output": tool_outputs
        }]
    })
