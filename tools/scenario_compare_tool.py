# tools/scenario_compare_tool.py
from langchain.tools import tool

@tool
def compare_business_scenarios(budget: float) -> dict:
    """
    Compare low-risk vs high-risk business strategies.
    Returns structured data for decision making.
    """

    return {
        "low_risk_strategy": {
            "expected_roi": "1.5x",
            "worst_case_loss": "8%",
            "break_even_months": 20,
            "recommended_for": "Conservative businesses"
        },
        "high_risk_strategy": {
            "expected_roi": "3.2x",
            "worst_case_loss": "40%",
            "break_even_months": 10,
            "recommended_for": "Aggressive growth startups"
        },
        "final_hint": (
            "Low-risk provides stability, while high-risk offers faster growth "
            "but higher volatility."
        )
    }
