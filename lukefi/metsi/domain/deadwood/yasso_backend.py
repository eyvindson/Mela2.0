from dataclasses import dataclass

from lukefi.metsi.domain.deadwood.types import DeadwoodPools, DeadwoodInflows, DeadwoodFluxes


class YassoBackend:
    def step(self, pools: DeadwoodPools, inflows: DeadwoodInflows, years: int) -> tuple[DeadwoodPools, DeadwoodFluxes]:
        raise NotImplementedError


@dataclass
class Yasso07Adapter(YassoBackend):
    """Deterministic placeholder backend for phase-0 integration tests."""

    annual_decay_rate: float = 0.03
    awenh_share: tuple[float, float, float, float, float] = (0.3, 0.25, 0.15, 0.2, 0.1)

    def step(self, pools: DeadwoodPools, inflows: DeadwoodInflows, years: int) -> tuple[DeadwoodPools, DeadwoodFluxes]:
        updated = DeadwoodPools(
            acid_c=pools.acid_c,
            water_c=pools.water_c,
            ethanol_c=pools.ethanol_c,
            non_soluble_c=pools.non_soluble_c,
            humus_c=pools.humus_c,
        )

        updated.add_inflows(inflows.total_c, self.awenh_share)

        decomposition_c = 0.0
        for _ in range(years):
            acid_loss = updated.acid_c * self.annual_decay_rate
            water_loss = updated.water_c * self.annual_decay_rate
            ethanol_loss = updated.ethanol_c * self.annual_decay_rate
            non_soluble_loss = updated.non_soluble_c * self.annual_decay_rate
            humus_loss = updated.humus_c * self.annual_decay_rate

            updated.acid_c -= acid_loss
            updated.water_c -= water_loss
            updated.ethanol_c -= ethanol_loss
            updated.non_soluble_c -= non_soluble_loss
            updated.humus_c -= humus_loss

            decomposition_c += acid_loss + water_loss + ethanol_loss + non_soluble_loss + humus_loss

        fluxes = DeadwoodFluxes(
            input_c=inflows.total_c,
            decomposition_c=decomposition_c,
            net_change_c=updated.total_c - pools.total_c,
        )

        return updated, fluxes
