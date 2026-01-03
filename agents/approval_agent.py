from langgraph.types import interrupt
from state.shared_state import StrategyState

def approval_agent(state: StrategyState):
    """
    Interrupts the graph when risk tolerance is LOW
    and waits for human approval from the UI.
    """
    return interrupt({
        "message": "⚠️ Risk tolerance is LOW. Human approval is required.",
        "state": state.dict()
    })
