from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tools.risk_tools import assess_risk
from state.shared_state import StrategyState, BoardOpinion

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a risk advisor. "
     "Use the risk assessment tool when evaluating budget and risk tolerance."),
    ("human",
     "Budget: {budget}\nRisk tolerance: {risk_tolerance}")
])

def risk_agent(state: StrategyState) -> StrategyState:
    llm = ChatOpenAI(model="gpt-4o-mini")
    chain = prompt | llm.bind_tools([assess_risk])

    response = chain.invoke({
        "budget": state.budget or 0,
        "risk_tolerance": state.risk_tolerance or "Medium"
    })

    tool_output = None

    if response.tool_calls:
        for call in response.tool_calls:
            if call["name"] == "assess_risk":
                tool_output = assess_risk.invoke(call["args"])

    final_opinion = tool_output or response.content

    opinion = BoardOpinion(
        agent="Risk Advisor",
        opinion=str(final_opinion),
        confidence=0.75
    )

    return state.copy(update={
        "board_opinions": state.board_opinions + [opinion],

        # 🔥 MISSING LINK ADDED
        "tool_outputs": {
            **state.tool_outputs,
            "risk_assessment": tool_output
        } if tool_output else state.tool_outputs,

        "history": state.history + [{
            "agent": "Risk Advisor",
            "tool_used": bool(tool_output),
            "output": final_opinion
        }]
    })
