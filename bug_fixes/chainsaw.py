from memory.space import Bank, Reserve, Write
import instruction.asm as asm
import args

class Chainsaw:
    def __init__(self):
        if args.fix_chainsaw:
            self.mod()

    def mod(self):
        # chain saw tool handler (C2/2B30) rolls 1/4 to turn the attack into an instant death attack:
        #   JSR $4B5A (random), AND #$03, BNE normal_attack
        # the death version has 0 power and misses targets immune to instant death (C2/2252, $3AA1 bit 2)
        # so against immune targets 1/4 of chain saw uses do nothing
        # only roll for instant death if the target can be killed, otherwise always use the normal attack
        #
        # replaces the 5 bytes of random/AND with a long call, returns z flag set to use the death attack
        # a = 8-bit, x/y = 16-bit on entry
        # NOTE: in F0 because C2 free space is exhausted with the full pootsleague flagset
        src = [
            asm.PHP(),
            asm.PHX(),
            asm.PHY(),
            asm.SEP(0x30),                  # 8-bit a, x, y

            asm.LDA(0xb9, asm.DIR),         # a = monster targets mask
            asm.BEQ("CHECK_CHARACTERS"),
            asm.LDY(0x08, asm.IMM8),        # y = first monster entity index
            asm.BRA("FIND_TARGET"),

            "CHECK_CHARACTERS",
            asm.LDA(0xb8, asm.DIR),         # a = character targets mask
            asm.BEQ("ROLL"),                # no target chosen yet, keep vanilla behavior
            asm.LDY(0x00, asm.IMM8),        # y = first character entity index

            "FIND_TARGET",                  # y = entity index of lowest target bit
            asm.LSR(),
            asm.BCS("CHECK_IMMUNE"),
            asm.INY(),
            asm.INY(),
            asm.BRA("FIND_TARGET"),

            "CHECK_IMMUNE",
            asm.LDA(0x3aa1, asm.ABS_Y),
            asm.BIT(0x04, asm.IMM8),        # immune to instant death?
            asm.BNE("NORMAL_ATTACK"),
            asm.LDA(0x331c, asm.ABS_Y),
            asm.BPL("NORMAL_ATTACK"),       # death status blocked? (bit 7 clear)

            "ROLL",                         # vanilla random (C2/4B5A)
            asm.INC(0xbe, asm.DIR),
            asm.LDX(0xbe, asm.DIR),
            asm.LDA(0xc0fd00, asm.LNG_X),
            asm.BRA("RETURN"),

            "NORMAL_ATTACK",
            asm.LDA(0x01, asm.IMM8),        # nonzero after AND #$03 below

            "RETURN",
            asm.REP(0x10),                  # 16-bit x/y to restore full x/y
            asm.PLY(),
            asm.PLX(),
            asm.PLP(),
            asm.AND(0x03, asm.IMM8),        # z set = instant death attack (vanilla 1/4)
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "chain saw only roll instant death if target not immune")
        chainsaw_roll = space.start_address_snes

        space = Reserve(0x22b30, 0x22b34, "chain saw random instant death roll", asm.NOP())
        space.write(
            asm.JSL(chainsaw_roll),
        )
