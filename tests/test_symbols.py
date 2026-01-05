from triarb.symbols import build_inst_id


def test_build_inst_id_okx():
    assert build_inst_id("okx", "ADA", "USDT") == "ADA-USDT"


def test_build_inst_id_gate():
    assert build_inst_id("gate", "ADA", "USDT") == "ADA_USDT"
