from langchain.tools import tool

@tool
def analyze_market(context: str) -> str:
    """
    Evaluate market competitiveness and opportunity.
    """
    context_lower = context.lower()

    if "gdpr" in context_lower:
        return "⚠️ GDPR compliance required. Legal cost will be high."
    if "strong competitors" in context_lower:
        return "⚠️ Market is saturated. Differentiation needed."
    if "emerging" in context_lower:
        return "✅ Emerging market with growth opportunity."

    return "ℹ️ Market is stable with moderate competition."
