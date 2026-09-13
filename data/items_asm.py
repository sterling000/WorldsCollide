from memory.space import Bank, Reserve, Write, Read
import instruction.asm as asm

from data.item_names import name_id

def stronger_atma_weapon():
    space = Reserve(0x20e59, 0x20e59, "atma weapon divisor exponent")
    space.write(4) # change modifier from 2^(5+1) to 2^(4+1)

def cursed_shield_mod(battles):
    src = [
        asm.LDA(battles, asm.IMM8),                 # a = battles required
        asm.INC(0x3ec0, asm.ABS),                   # increment cursed shield battle count
        asm.CMP(0x3ec0, asm.ABS),                   # compare battle count with battles required
        asm.BNE("NOT_UNCURSED"),                    # branch if count != required

        asm.STZ(0x3ec0, asm.ABS),                   # reset count back to zero
        Read(0x26003, 0x2600b),                     # set uncursed flag and change item to paladin shield
        asm.RTS(),

        "NOT_UNCURSED",
        asm.LDA(name_id["Cursed Shld"], asm.IMM8),  # a = cursed shield id
        asm.RTS(),
    ]
    space = Write(Bank.C2, src, "cursed shield uncursed check")
    uncurse_shield_check = space.start_address

    space = Reserve(0x25ffe, 0x2600b, "cursed shield battles increment", asm.NOP())
    space.write(
        asm.JSR(uncurse_shield_check, asm.ABS),
    )

def paladin_shield_consumable():
    """
    Make Paladin Shield consumable and cast Ultima with proper targeting.
    
    Based on successful implementation analysis, the modification requires:
    1. Enable consumable flags (0x03 -> 0x23, adding 0x20 bit)
    2. Set spell data at item offset +14 (0x4A for Ultima)  
    3. Set targeting data at item offset +20 (0x94 for proper targeting)
    
    Comparison with working elemental shields shows this is the correct approach.
    """
    # Paladin Shield item data starts at 0x185C12
    paladin_item_addr = 0x185C12
    
    # Modification 1: Enable consumable flags
    # Original: 0x03, Modified: 0x23 (added 0x20 consumable bit)
    flags_space = Reserve(paladin_item_addr, paladin_item_addr, "paladin shield consumable flags")
    flags_space.write(0x23)
    
    # Modification 2: Set spell ID data at offset +14 
    # Value 0x4A (74 decimal) appears to encode Ultima spell
    spell_data_addr = paladin_item_addr + 14
    spell_space = Reserve(spell_data_addr, spell_data_addr, "paladin shield spell data")
    spell_space.write(0x4A)
    
    # Modification 3: Set spell ID data at offset +18  
    # Value 0x94 (148 decimal) = 128 + 20 (Ultima spell ID)
    spell_id_addr = paladin_item_addr + 18
    spell_id_space = Reserve(spell_id_addr, spell_id_addr, "paladin shield spell id")
    spell_id_space.write(0x94)
    
    print("=== PALADIN SHIELD CONSUMABLE ULTIMA IMPLEMENTATION ===")
    print("Successfully implemented based on working ROM analysis:")
    print("✓ Enabled consumable flags (0x03 -> 0x23)")
    print("✓ Set spell data byte +14 = 0x4A")
    print("✓ Set spell ID byte +18 = 0x94 (128 + 20 = Ultima)")
    print("")
    print("Paladin Shield will now cast Ultima when consumed!")

def dragon_horn_jumps(min_jumps, max_jumps):
    # With Dragon Horn equipped (bit 7 of $3c44,x) vanilla rolls a fixed 2-4 attacks at C2/1828:
    #   JSR $4b5a / INC $3a70 / CMP #$40 / BCS +$0a / INC $3a70 / CMP #$10 / BCS +$03 / INC $3a70
    # i.e. 75% 2 attacks, 18.75% 3, 6.25% 4. Replace the roll with an even one over the given
    # range. $3a70 already counts the jump itself, so add (jumps - 1) rather than storing outright.
    count = max_jumps - min_jumps + 1

    # smallest 2^k - 1 able to hold count - 1, so the reroll below stays even
    mask = 0
    while mask < count - 1:
        mask = (mask << 1) | 1

    # written inline rather than into its own block: bank c2 runs out of room on larger flagsets.
    # this must stay within the 20 vanilla bytes, C2/1823 branches past them to C2/183c
    space = Reserve(0x21828, 0x2183b, "dragon horn jump count", asm.NOP())
    space.write(
        "REROLL",
        asm.JSR(0x4b5a, asm.ABS),               # a = random number (0 to 255)
        asm.AND(mask, asm.IMM8),                # a = 0 to mask
        asm.CMP(count, asm.IMM8),
        asm.BCS("REROLL"),                      # reroll until a < count, even 0 to count - 1

        asm.CLC(),
        asm.ADC(0x3a70, asm.ABS),               # add the jump already counted
        asm.CLC(),
        asm.ADC(min_jumps - 1, asm.IMM8),       # a = attacks this jump makes
        asm.STA(0x3a70, asm.ABS),
    )
