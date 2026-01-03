from langchain.tools import tool

@tool
def simulate_business_scenario(
    budget: float,
    risk_tolerance: str
) -> dict:
    """
    Simulates ROI, loss, and break-even timeline.
    """

    if budget < 20000:
        base_roi = 1.4
        break_even = 22
    elif budget < 50000:
        base_roi = 1.8
        break_even = 16
    else:
        base_roi = 2.6
        break_even = 12

    if risk_tolerance.lower() == "low":
        return {
            "best_case_roi": f"{base_roi}x",
            "worst_case_loss": "10%",
            "break_even_month": break_even + 4,
            "risk_level": "Low"
        }

    return {
        "best_case_roi": f"{base_roi + 0.6}x",
        "worst_case_loss": "35%",
        "break_even_month": break_even,
        "risk_level": "Medium"
    }
