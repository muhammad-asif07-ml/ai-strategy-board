from langchain.tools import tool

@tool
def assess_risk(budget: float, risk_tolerance: str) -> str:
    """
    Assess financial and regulatory risk.
    """
    risk_tolerance = risk_tolerance.lower()

    if risk_tolerance == "low" and budget < 30000:
        return "❌ Risk too high for low tolerance. Human approval required."
    if risk_tolerance == "high" and budget < 15000:
        return "⚠️ Risk acceptable but budget is very tight."
    
    return "✅ Risk level acceptable."
