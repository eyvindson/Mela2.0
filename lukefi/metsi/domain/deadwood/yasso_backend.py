from dataclasses import dataclass
from typing import Callable

from lukefi.metsi.domain.deadwood.types import DeadwoodPools, DeadwoodInflows, DeadwoodFluxes


@dataclass(frozen=True)
class YassoClimate:
    temperature_c: float
    precipitation_mm: float
    temperature_amplitude_c: float


FINLAND_STATIC_CLIMATE = YassoClimate(
    temperature_c=3.5,
    precipitation_mm=600.0,
    temperature_amplitude_c=13.0,
)


class YassoBackend:
    def step(self, pools: DeadwoodPools, inflows: DeadwoodInflows, years: int) -> tuple[DeadwoodPools, DeadwoodFluxes]:
        raise NotImplementedError


@dataclass
class Yasso07Adapter(YassoBackend):
    """Deterministic placeholder backend with climate-ready interface."""

    annual_decay_rate: float = 0.03
    awenh_share: tuple[float, float, float, float, float] = (0.3, 0.25, 0.15, 0.2, 0.1)
    climate_default: YassoClimate = FINLAND_STATIC_CLIMATE
    climate_provider: Callable[[], YassoClimate] | None = None

    def _resolve_climate(self) -> YassoClimate:
        return self.climate_provider() if self.climate_provider is not None else self.climate_default

    def _climate_decay_multiplier(self, climate: YassoClimate) -> float:
        # Keep a deterministic MVP relation, but expose climate dependency for future stand-wise forcing.
        temp_term = 1.0 + max(min((climate.temperature_c - 3.5) * 0.01, 0.15), -0.15)
        precipitation_term = 1.0 + max(min((climate.precipitation_mm - 600.0) / 10000.0, 0.08), -0.08)
        amplitude_term = 1.0 + max(min((climate.temperature_amplitude_c - 13.0) * 0.005, 0.08), -0.08)
        return temp_term * precipitation_term * amplitude_term

    def step(self, pools: DeadwoodPools, inflows: DeadwoodInflows, years: int) -> tuple[DeadwoodPools, DeadwoodFluxes]:
        climate = self._resolve_climate()
        annual_decay_rate = self.annual_decay_rate * self._climate_decay_multiplier(climate)

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
            acid_loss = updated.acid_c * annual_decay_rate
            water_loss = updated.water_c * annual_decay_rate
            ethanol_loss = updated.ethanol_c * annual_decay_rate
            non_soluble_loss = updated.non_soluble_c * annual_decay_rate
            humus_loss = updated.humus_c * annual_decay_rate

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
