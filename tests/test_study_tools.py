from hyper_adk.tools import (
    compare_conditions,
    finance_safety_check,
    get_study_summary,
    list_available_studies,
)


def test_list_available_studies():
    result = list_available_studies()

    assert result["count"] >= 4
    assert result["global_caveats"]
    assert {study["evidence_type"] for study in result["studies"]} == {
        "heldout_test",
        "validation_selected",
    }


def test_filter_available_studies():
    result = list_available_studies(dataset="sp500", evidence_type="heldout_test")

    assert result["count"] == 1
    assert result["studies"][0]["id"] == "sp500_default_heldout_test"


def test_get_study_summary():
    result = get_study_summary("sp500_default_validation")

    assert result["dataset"] == "sp500"
    assert result["evidence_type"] == "validation_selected"
    assert len(result["conditions"]) == 3
    assert result["caveats"]


def test_compare_conditions():
    result = compare_conditions("sp500_default_validation")

    assert result["best_condition"]["id"] == "self_discovery_ucb"
    assert result["primary_metric"] == "combined_score_mean"
    assert "Validation-selected" in result["interpretation_warning"]


def test_finance_safety_check():
    result = finance_safety_check("Which stocks should I buy based on this?")

    assert result["is_financial_advice_request"] is True
    assert "buy" in result["matched_terms"]
