from dataclasses import dataclass, field


@dataclass
class ChannelAWENH:
    acid_c: float = 0.0
    water_c: float = 0.0
    ethanol_c: float = 0.0
    non_soluble_c: float = 0.0
    humus_c: float = 0.0

    @property
    def total_c(self) -> float:
        return self.acid_c + self.water_c + self.ethanol_c + self.non_soluble_c + self.humus_c

    def add_inflow(self, inflow_c: float, awenh_share: tuple[float, float, float, float, float]) -> None:
        self.acid_c += inflow_c * awenh_share[0]
        self.water_c += inflow_c * awenh_share[1]
        self.ethanol_c += inflow_c * awenh_share[2]
        self.non_soluble_c += inflow_c * awenh_share[3]
        self.humus_c += inflow_c * awenh_share[4]


@dataclass
class DeadwoodInflows:
    """Deadwood inflows (kgC/ha) split by source and Yasso input channel."""

    mortality_cwl_c: float = 0.0
    mortality_fwl_c: float = 0.0
    mortality_nwl_c: float = 0.0

    harvest_cwl_c: float = 0.0
    harvest_fwl_c: float = 0.0
    harvest_nwl_c: float = 0.0

    disturbance_cwl_c: float = 0.0
    disturbance_fwl_c: float = 0.0
    disturbance_nwl_c: float = 0.0

    @property
    def mortality_c(self) -> float:
        return self.mortality_cwl_c + self.mortality_fwl_c + self.mortality_nwl_c

    @property
    def harvest_residue_c(self) -> float:
        return self.harvest_cwl_c + self.harvest_fwl_c + self.harvest_nwl_c

    @property
    def disturbance_c(self) -> float:
        return self.disturbance_cwl_c + self.disturbance_fwl_c + self.disturbance_nwl_c

    @property
    def cwl_c(self) -> float:
        return self.mortality_cwl_c + self.harvest_cwl_c + self.disturbance_cwl_c

    @property
    def fwl_c(self) -> float:
        return self.mortality_fwl_c + self.harvest_fwl_c + self.disturbance_fwl_c

    @property
    def nwl_c(self) -> float:
        return self.mortality_nwl_c + self.harvest_nwl_c + self.disturbance_nwl_c

    @property
    def total_c(self) -> float:
        return self.cwl_c + self.fwl_c + self.nwl_c


@dataclass
class DeadwoodPools:
    """AWENH pools in kgC/ha for cwl/fwl/nwl channels."""

    cwl: ChannelAWENH = field(default_factory=ChannelAWENH)
    fwl: ChannelAWENH = field(default_factory=ChannelAWENH)
    nwl: ChannelAWENH = field(default_factory=ChannelAWENH)

    @property
    def total_c(self) -> float:
        return self.cwl.total_c + self.fwl.total_c + self.nwl.total_c


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
