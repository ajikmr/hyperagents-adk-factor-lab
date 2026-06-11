"""Finance-safety helper tools."""

from __future__ import annotations


ADVICE_TERMS = (
    "buy",
    "sell",
    "short",
    "hold",
    "portfolio allocation",
    "which stock",
    "what stock",
    "recommend",
    "trade",
)


def finance_safety_check(user_request: str) -> dict[str, object]:
    """Classify whether a request asks for financial advice.

    Args:
        user_request: User request text to classify.
    """

    normalized = user_request.lower()
    matched_terms = [term for term in ADVICE_TERMS if term in normalized]
    is_advice_request = bool(matched_terms)
    return {
        "is_financial_advice_request": is_advice_request,
        "matched_terms": matched_terms,
        "required_behavior": (
            "Refuse to provide investment advice and redirect to research methodology, "
            "risk analysis, or evidence caveats."
            if is_advice_request
            else "Proceed with research-only analysis while preserving caveats."
        ),
        "standard_disclaimer": (
            "HyperAgents-ADK provides research workflow support only and does not "
            "recommend buying, selling, shorting, or holding securities."
        ),
    }
