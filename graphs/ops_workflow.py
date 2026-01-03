from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from state.shared_state import StrategyState

from agents.market_agent import market_agent
from agents.risk_agent import risk_agent
from agents.finance_agent import finance_agent
from agents.strategy_agent import strategy_agent
from agents.approval_agent import approval_agent


def approval_router(state: StrategyState) -> str:
    return "human_approval" if state.risk_tolerance.lower() == "low" else "auto_approve"


def build_workflow():
    graph = StateGraph(StrategyState)

    graph.add_node("market", market_agent)
    graph.add_node("risk", risk_agent)
    graph.add_node("finance", finance_agent)
    graph.add_node("strategy", strategy_agent)
    graph.add_node("human_approval", approval_agent)
    graph.add_node("auto_approve", lambda s: s)

    graph.add_edge(START, "market")
    graph.add_edge("market", "risk")
    graph.add_edge("risk", "finance")
    graph.add_edge("finance", "strategy")

    graph.add_conditional_edges(
        "strategy",
        approval_router,
        {
            "human_approval": "human_approval",
            "auto_approve": "auto_approve",
        }
    )

    graph.add_edge("human_approval", END)
    graph.add_edge("auto_approve", END)
    
    # Persistance
    
    checkpointer = InMemorySaver()
    return graph.compile(checkpointer=checkpointer)
