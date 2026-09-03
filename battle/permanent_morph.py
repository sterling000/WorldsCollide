from memory.space import Bank, START_ADDRESS_SNES, Reserve, Write
import instruction.asm as asm

import data.event_bit as event_bit
import objectives

class _PermanentMorph:
    '''Stop the morph timer from running out while the Permanent Morph objective is complete.

    Using Morph divides $ffff by the morph gauge ($1cf6) to get a per tick drain rate, capped at
    $0800, and stores it in $3f32 (C2/0B01).  $3f30 is the 16 bit morph remaining counter, seeded
    at $ffff.  Once per tick the battle loop calls C2/1211 for whichever character is morphed
    ($3ee2) to subtract the drain rate from the counter; the morph ends on underflow.

    Skipping that subtraction leaves the counter at $ffff, so the morph never expires.  The gauge
    is topped back up in the same routine because C2/0B36 scales it down by $3f31 / 256 (the
    fraction of morph time consumed) whenever a morph ends.
    '''
    MORPH_REMAINING = 0x3f30    # 16 bit, counts down from $ffff
    MORPH_DRAIN_RATE = 0x3f32   # subtracted from MORPH_REMAINING once per tick
    MORPH_GAUGE = 0x1cf6        # persistent 0-255 gauge charged by magic points

    def __init__(self):
        self.permanent_morph_name = "Permanent Morph"
        branch_name = self.permanent_morph_name.upper().replace(' ', '_')

        src = self.get_branch_if_objective_complete_src(branch_name)
        src += [
            # original replaced code
            f"NO_{branch_name}",
            asm.A16(),
            asm.SEC(),
            asm.LDA(self.MORPH_REMAINING, asm.ABS),
            asm.SBC(self.MORPH_DRAIN_RATE, asm.ABS),
            asm.STA(self.MORPH_REMAINING, asm.ABS),
            asm.A8(),                               # sep/rep leave the carry alone
            asm.RTL(),                              # caller branches on carry to end the morph

            branch_name,
            asm.LDA(0xff, asm.IMM8),
            asm.STA(self.MORPH_GAUGE, asm.ABS),     # keep the gauge full so morph stays selectable
            asm.SEC(),                              # carry set, the morph has not run out
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "permanent morph drain morph timer")
        drain_morph_timer = space.start_address

        space = Reserve(0x21211, 0x2121e, "drain morph timer", asm.NOP())
        space.write(
            asm.JSL(START_ADDRESS_SNES + drain_morph_timer),
        )

    def get_branch_if_objective_complete_src(self, branch_name):
        src = []
        if self.permanent_morph_name in objectives.results:
            for objective in objectives.results[self.permanent_morph_name]:
                objective_event_bit = event_bit.objective(objective.id)
                bit = event_bit.bit(objective_event_bit)
                address = event_bit.address(objective_event_bit)

                src += [
                    asm.LDA(address, asm.ABS),
                    asm.AND(2 ** bit, asm.IMM8),
                    asm.BNE(branch_name),
                ]
        return src

permanent_morph = _PermanentMorph()
