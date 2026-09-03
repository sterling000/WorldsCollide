from objectives.results._objective_result import *

# Top the morph gauge off when the objective completes.  Morph cannot even be selected until the
# gauge is above 15 (C2/5326), so without this the reward could be unusable on a drained gauge.
# battle/permanent_morph.py is what actually stops the morph from expiring.
def _fill_morph_gauge():
    morph_gauge_address = 0x1cf6

    src = [
        asm.LDA(0xff, asm.IMM8),
        asm.STA(morph_gauge_address, asm.ABS),
        asm.RTL(),
    ]
    space = Write(Bank.F0, src, "permanent morph fill morph gauge")
    return space.start_address
fill_morph_gauge = _fill_morph_gauge()

class Field(field_result.Result):
    def src(self):
        return [
            field.LongCall(START_ADDRESS_SNES + fill_morph_gauge),
        ]

class Battle(battle_result.Result):
    def src(self):
        return [
            asm.JSL(START_ADDRESS_SNES + fill_morph_gauge),
        ]

class Result(ObjectiveResult):
    NAME = "Permanent Morph"
    def __init__(self):
        super().__init__(Field, Battle)
