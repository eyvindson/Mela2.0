import logging

from lukefi.metsi.domain.deadwood.types import ChannelAWENH, DeadwoodInflows, DeadwoodPools
from lukefi.metsi.domain.deadwood.yasso_backend import Yasso07Adapter


class _FakeYassoModule:
    class yasso:
        @staticmethod
        def mod5c(_params, _duration, _climate, stock, _infall, _diameter):
            return stock * 0.5


def test_binary_fallback_parity_mismatch_logs_warning_and_continues(caplog):
    adapter = Yasso07Adapter(prefer_binary=True, annual_decay_rate=0.0, parity_rel_tolerance=1e-4)
    adapter._load_y07_module = lambda: _FakeYassoModule()  # type: ignore
    pools = DeadwoodPools(cwl=ChannelAWENH(acid_c=10.0))

    with caplog.at_level(logging.WARNING):
        updated, _ = adapter.step(pools, DeadwoodInflows(), years=1)

    assert updated.total_c == 5.0
    assert "parity mismatch" in caplog.text
