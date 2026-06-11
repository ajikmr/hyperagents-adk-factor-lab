from hyper_engine.smoke_data import REQUIRED_COLUMNS, list_smoke_datasets, load_panel


def test_smoke_datasets_exist_and_have_expected_shape():
    result = list_smoke_datasets()

    assert result["count"] == 2
    dataset_ids = {dataset["id"] for dataset in result["datasets"]}
    assert dataset_ids == {"sp500_smoke", "csi300_smoke"}

    for dataset in result["datasets"]:
        assert set(dataset["splits"]) == {"train", "val", "test"}
        assert dataset["splits"]["val"]["symbols"] == 48
        assert dataset["splits"]["val"]["dates"] == 45


def test_load_panel_schema():
    panel = load_panel("sp500_smoke", "val")

    assert list(panel.columns) == REQUIRED_COLUMNS
    assert len(panel) == 48 * 45
    assert panel["symbol"].nunique() == 48
    assert panel["date"].nunique() == 45
    assert panel["close"].min() > 0
