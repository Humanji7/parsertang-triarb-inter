from triarb.assets import DEFAULT_ASSETS, EXCLUDED_ASSETS, filter_assets


def test_filter_assets_excludes_high_liquid():
    filtered = filter_assets(DEFAULT_ASSETS + EXCLUDED_ASSETS, EXCLUDED_ASSETS)
    for asset in EXCLUDED_ASSETS:
        assert asset not in filtered


def test_default_assets_are_unique():
    assert len(DEFAULT_ASSETS) == len(set(DEFAULT_ASSETS))
