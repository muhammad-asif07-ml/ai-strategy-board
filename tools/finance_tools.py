from langchain.tools import tool

@tool
def financial_projection(budget: float) -> str:
    """Evaluate financial feasibility based on budget size."""
    
    if budget < 10000:
        return "Budget too low. High chance of failure and delayed ROI."
    elif budget < 50000:
        return "Budget is moderate. ROI expected in 18–24 months."
    else:
        return "Strong budget. ROI expected within 12 months."
