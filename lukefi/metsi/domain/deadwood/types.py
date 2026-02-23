from dataclasses import dataclass, field


@dataclass
class DeadwoodInflows:
    """Deadwood carbon inflows for one simulation step in kgC/ha."""

    mortality_c: float = 0.0
    harvest_residue_c: float = 0.0
    disturbance_c: float = 0.0

    @property
    def total_c(self) -> float:
        return self.mortality_c + self.harvest_residue_c + self.disturbance_c


@dataclass
class DeadwoodPools:
    """AWENH pools in kgC/ha for stand-level bookkeeping."""

    acid_c: float = 0.0
    water_c: float = 0.0
    ethanol_c: float = 0.0
    non_soluble_c: float = 0.0
    humus_c: float = 0.0

    @property
    def total_c(self) -> float:
        return self.acid_c + self.water_c + self.ethanol_c + self.non_soluble_c + self.humus_c

    def add_inflows(self, inflow_c: float, awenh_share: tuple[float, float, float, float, float]) -> None:
        self.acid_c += inflow_c * awenh_share[0]
        self.water_c += inflow_c * awenh_share[1]
        self.ethanol_c += inflow_c * awenh_share[2]
        self.non_soluble_c += inflow_c * awenh_share[3]
        self.humus_c += inflow_c * awenh_share[4]


@dataclass
class DeadwoodFluxes:
    input_c: float = 0.0
    decomposition_c: float = 0.0
    net_change_c: float = 0.0


@dataclass
class DeadwoodClassState:
    species_group: str
    snag: bool
    diameter_class: str
    years_since_death: int
    carbon_c: float


@dataclass
class DeadwoodState:
    pools: DeadwoodPools = field(default_factory=DeadwoodPools)
    latest_fluxes: DeadwoodFluxes = field(default_factory=DeadwoodFluxes)
