from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tools.market_tools import analyze_market
from state.shared_state import StrategyState, BoardOpinion

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a market strategy advisor. "
     "You MUST analyze the market using the provided tool before giving advice."),
    ("human",
     "Business goal: {business_goal}\n"
     "Market context: {market_context}")
])

def market_agent(state: StrategyState) -> StrategyState:
    llm = ChatOpenAI(model="gpt-4o-mini")
    chain = prompt | llm.bind_tools([analyze_market])

    response = chain.invoke({
        "business_goal": state.business_goal,
        "market_context": state.market_context or "No context"
    })

    tool_output = None

    if response.tool_calls:
        for call in response.tool_calls:
            if call["name"] == "analyze_market":
                tool_output = analyze_market.invoke(call["args"])

    final_opinion = tool_output or response.content

    opinion = BoardOpinion(
        agent="Market Advisor",
        opinion=str(final_opinion),
        confidence=0.82
    )

    return state.copy(update={
        "board_opinions": state.board_opinions + [opinion],

        # 🔥 MISSING LINK ADDED
        "tool_outputs": {
            **state.tool_outputs,
            "market_analysis": tool_output
        } if tool_output else state.tool_outputs,

        "history": state.history + [{
            "agent": "Market Advisor",
            "tool_used": bool(tool_output),
            "output": final_opinion
        }]
    })
