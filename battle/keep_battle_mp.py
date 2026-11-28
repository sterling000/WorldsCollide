from memory.space import Bank, Reserve, Write
import instruction.asm as asm
import args

# In vanilla, battle-menu setup (C2/532C) zeroes a character's in-battle
# current and max MP unless one of their four commands qualifies: Lore, or
# Magic/X-Magic with at least one spell known or an esper equipped.  The
# zeroed MP is what blocks MP-drain criticals (Illumina, Ragnarok, Rune
# Edge, Punisher) - the crit code (C2/3F22) has no command check of its
# own, it simply cannot pay its MP cost - and battle-end writeback
# (C2/496E) skips MP while max MP is zero, keeping the field stat intact.
#
# With randomized commands a character can lack the Magic command entirely
# yet still have MP, equip espers and learn spells.  Keep such a
# character's battle MP live whenever the battle menu WOULD show a Magic
# command for them - the same per-character test C2/5429 uses to blank it:
# $F6 (number of spells known, built by C2/568D just before this runs;
# party-mirrored for Gogo) or $F7 (equipped esper, $FF = none).  Umaro and
# guests keep zeroed MP ($F6 = 0, $F7 = $FF).  Leaving max MP nonzero also
# activates the battle-end writeback, so MP spent on criticals persists to
# the field, exactly as it already does for magic users.

#
# Fork changes: the routine lives in F0 (called with JSL) because C2 free
# space is exhausted with the full pootsleague flagset, and with -eue
# (equipable umaro espers) Umaro also keeps his battle MP.

UMARO = 0x0d

def mod():
    src = [
        asm.LSR(0xf8, asm.DIR),      # carry = vanilla qualifying-command flag
        asm.BCS("KEEP_MP"),
        asm.LDA(0xf6, asm.DIR),      # number of spells known
        asm.BNE("KEEP_MP"),
        asm.LDA(0xf7, asm.DIR),      # equipped esper ($ff = none)
        asm.INC(),
        asm.BNE("KEEP_MP"),
        asm.LDA(0x05, asm.S),        # character offset: X pushed at C2/532C
                                     # entry, under P ($04,S) and our long
                                     # return address ($01-$03,S)
        asm.TAX(),
    ]
    if args.equipable_umaro_espers:
        src += [
            asm.LDA(0x3ed8, asm.ABS_X),  # character id
            asm.CMP(UMARO, asm.IMM8),
            asm.BEQ("KEEP_MP"),
        ]
    src += [
        asm.REP(0x20),
        asm.STZ(0x3c08, asm.ABS_X),  # zero current MP
        asm.STZ(0x3c30, asm.ABS_X),  # zero max MP
        asm.SEP(0x20),
        "KEEP_MP",
        asm.RTL(),
    ]
    space = Write(Bank.F0, src, "battle menu keep mp when magic would show")
    keep_mp = space.start_address_snes

    space = Reserve(0x253f9, 0x25407, "battle menu zero mp when no magic", asm.NOP())
    space.write(
        asm.JSL(keep_mp),
    )
    # fall through to the vanilla epilogue at C2/5408 (PLP, PLX, RTS)

mod()
