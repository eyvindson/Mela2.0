from lukefi.metsi.domain.forestry_types import ForestCondition
from lukefi.metsi.domain.deadwood import DeadwoodInflowConfig, update_deadwood_pools
from lukefi.metsi.domain.natural_processes.grow_metsi import grow_metsi_fn
from lukefi.metsi.sim.generators import Event
from lukefi.metsi.sim.sim_configuration import Transition
from lukefi.metsi.sim.simulation_instruction import SimulationInstruction


control_structure = {
    "app_configuration": {
        "state_format": "vmi13",
        "run_modes": ["simulate"],
        "simulation_output_file": "simulation_results_deadwood_mvp",
    },
    "simulation_instructions": [
        SimulationInstruction(
            events=[
                Event(
                    treatment=update_deadwood_pools,
                    static_parameters={
                        "enabled": True,
                        "step": 5,
                        "deadwood_config": DeadwoodInflowConfig(
                            equation_set="repola",
                            include_harvest_residues=True,
                        ),
                    },
                    db_output=True,
                )
            ]
        )
    ],
    "transition": Transition(grow_metsi_fn),
    "end_condition": ForestCondition(lambda x: x.computational_unit.year >= 2050),
}

__all__ = ["control_structure"]
