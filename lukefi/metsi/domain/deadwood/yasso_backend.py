from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Callable

import numpy as np

from lukefi.metsi.domain.deadwood.types import ChannelAWENH, DeadwoodFluxes, DeadwoodInflows, DeadwoodPools

ML_PARAM = np.array(
    (-0.70359426736831665, -5.6810555458068848, -0.2613542377948761, -0.02810959704220295, 0.48885279893875122,
     0.019057683646678925, 0.96963745355606079, 0.98725599050521851, 0.0028432635590434074, 0.0033964612521231174,
     1.3993703760206699e-05, 1.7966924133361317e-05, 0.01218125969171524, 0.0027778467629104853, 0.012695553712546825,
     0.97138279676437378, 0.098731838166713715, -0.001571640488691628, 0.17000000178813934, -0.001500000013038516,
     0.17000000178813934, -0.001500000013038516, 0.17000000178813934, -0.001500000013038516, 0.0,
     -1.2716917991638184, 0.0, 101.82534790039062, 260.0, -0.15269890427589417, -0.00039342229138128459,
     -0.33000001311302185, 0.0, 0.0, -0.0014966174494475126, 0.0042703705839812756, 0.0, 0.0,
     -1.7084113359451294, 0.8585553765296936, -0.30680140852928162, 0.0, 0.58340001106262207, 1.0,
     10299.29296875),
    dtype=np.float32,
)


@dataclass(frozen=True)
class YassoClimate:
    temperature_c: float
    precipitation_mm: float
    temperature_amplitude_c: float


FINLAND_STATIC_CLIMATE = YassoClimate(temperature_c=3.5, precipitation_mm=600.0, temperature_amplitude_c=13.0)
LOGGER = logging.getLogger(__name__)


class YassoBackend:
    def step(self, pools: DeadwoodPools, inflows: DeadwoodInflows, years: int) -> tuple[DeadwoodPools, DeadwoodFluxes]:
        raise NotImplementedError


@dataclass
class Yasso07Adapter(YassoBackend):
    annual_decay_rate: float = 0.03
    awenh_share: tuple[float, float, float, float, float] = (0.3, 0.25, 0.15, 0.2, 0.1)
    climate_default: YassoClimate = FINLAND_STATIC_CLIMATE
    climate_provider: Callable[[], YassoClimate] | None = None
    prefer_binary: bool = True
    cwl_diameter_cm: float = 10.0
    fwl_diameter_cm: float = 2.0
    parity_rel_tolerance: float = 1e-4

    def _resolve_climate(self) -> YassoClimate:
        return self.climate_provider() if self.climate_provider is not None else self.climate_default

    def _load_y07_module(self):
        dead_dir = Path(__file__).resolve().parents[4] / "dead"
        if str(dead_dir) not in __import__("sys").path:
            __import__("sys").path.append(str(dead_dir))
        try:
            import y07  # type: ignore

            return y07
        except Exception:
            return None

    def _apply_binary(self, channel: ChannelAWENH, inflow_c: float, duration: float, climate: YassoClimate, diameter: float, y07_module):
        stock = np.array([channel.acid_c, channel.water_c, channel.ethanol_c, channel.non_soluble_c, channel.humus_c], dtype=np.float32)
        infall = np.array([inflow_c * self.awenh_share[0], inflow_c * self.awenh_share[1], inflow_c * self.awenh_share[2], inflow_c * self.awenh_share[3], 0.0], dtype=np.float32) / duration
        cl = np.array([climate.temperature_c, climate.precipitation_mm, climate.temperature_amplitude_c], dtype=np.float32)
        return y07_module.yasso.mod5c(ML_PARAM, duration, cl, stock, infall, np.float32(diameter))

    def _apply_fallback(self, channel: ChannelAWENH, inflow_c: float, years: int, climate: YassoClimate) -> ChannelAWENH:
        updated = ChannelAWENH(channel.acid_c, channel.water_c, channel.ethanol_c, channel.non_soluble_c, channel.humus_c)
        updated.add_inflow(inflow_c, self.awenh_share)
        temp_mult = 1.0 + max(min((climate.temperature_c - 3.5) * 0.01, 0.15), -0.15)
        rate = self.annual_decay_rate * temp_mult
        for _ in range(years):
            updated.acid_c *= (1.0 - rate)
            updated.water_c *= (1.0 - rate)
            updated.ethanol_c *= (1.0 - rate)
            updated.non_soluble_c *= (1.0 - rate)
            updated.humus_c *= (1.0 - rate)
        return updated

    def step(self, pools: DeadwoodPools, inflows: DeadwoodInflows, years: int) -> tuple[DeadwoodPools, DeadwoodFluxes]:
        climate = self._resolve_climate()
        y07_module = self._load_y07_module() if self.prefer_binary else None

        if y07_module is not None:
            cwl = self._apply_binary(pools.cwl, inflows.cwl_c, float(years), climate, self.cwl_diameter_cm, y07_module)
            fwl = self._apply_binary(pools.fwl, inflows.fwl_c, float(years), climate, self.fwl_diameter_cm, y07_module)
            nwl = self._apply_binary(pools.nwl, inflows.nwl_c, float(years), climate, 0.0, y07_module)
            updated = DeadwoodPools(
                cwl=ChannelAWENH(*[float(v) for v in cwl]),
                fwl=ChannelAWENH(*[float(v) for v in fwl]),
                nwl=ChannelAWENH(*[float(v) for v in nwl]),
            )

            parity = DeadwoodPools(
                cwl=self._apply_fallback(pools.cwl, inflows.cwl_c, years, climate),
                fwl=self._apply_fallback(pools.fwl, inflows.fwl_c, years, climate),
                nwl=self._apply_fallback(pools.nwl, inflows.nwl_c, years, climate),
            )
            ref = max(abs(updated.total_c), 1e-9)
            rel_err = abs(updated.total_c - parity.total_c) / ref
            if rel_err > self.parity_rel_tolerance:
                LOGGER.warning(
                    "Yasso binary/fallback parity mismatch rel_err=%s exceeds tolerance=%s; continuing with binary backend",
                    rel_err,
                    self.parity_rel_tolerance,
                )
        else:
            updated = DeadwoodPools(
                cwl=self._apply_fallback(pools.cwl, inflows.cwl_c, years, climate),
                fwl=self._apply_fallback(pools.fwl, inflows.fwl_c, years, climate),
                nwl=self._apply_fallback(pools.nwl, inflows.nwl_c, years, climate),
            )

        fluxes = DeadwoodFluxes(
            input_c=inflows.total_c,
            decomposition_c=max(0.0, pools.total_c + inflows.total_c - updated.total_c),
            net_change_c=updated.total_c - pools.total_c,
        )
        return updated, fluxes
