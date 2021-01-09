from mephisto.cfa import CFG

from .fixtures import if_statement


def test_cfg():
    cfg = CFG().create(if_statement.simple_if)

    assert list(cfg.as_line()) == [(2, 3), (2, 5), (3, 7), (5, 7)]
