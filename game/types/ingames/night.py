import dataclasses

@dataclasses.dataclass
class Player:
    stamina: float = 1
    fainted: bool = False
    foot_out: bool = False