# Pootsleague Flagset Glossary

A comprehensive guide to every flag used in the **pootsleague** flagset for Final Fantasy VI Worlds Collide randomizer.

## Overview

The pootsleague flagset is a competitive configuration that emphasizes balanced randomization across all game systems while maintaining reasonable difficulty scaling and accessibility.

## Full Command

```bash
python3 wc.py -i ffiii.smc -cg -oa 2.2.2.2.6.6.4.9.9 -ob 3.1.1.10.20.20 -oc 30.8.8.1.1.11.8 -od 59.1.1.11.31 -oe 62.1.1.11.44 -of 26.8.8.1.1.11.26 -og 28.10.10.1.1.11.13 -oh 9.1.1.11.19 -oi 31.10.10.1.1.11.3 -oj 8.1.1.11.0 -ok 14.1.1.11.57 -ol 16.1.1.11.59 -om 27.8.8.1.1.11.40 -on 7.1.1.11.40 -oo 48.10.10.1.1.2.9.9 -op 45.10.10.1.1.4.12.12 -oq 29.125.125.1.1.11.10 -or 37.1.1.11.48 -os 38.1.1.12.7 -ot 36.1.1.6.3.3 -sc1 random -sc2 random -sc3 random -sal -eu -csrp 80 125 -fst -brl -slr 4 5 -lmprp 75 125 -lel -srr 25 35 -rnl -rnc -sdr 1 3 -das -dda -dns -sch -scis -com 98989898989898989898989898 -rec1 28 -rec2 97 -xpm 3 -mpm 5 -gpm 5 -nxppd -lsced 2 -hmced 2 -xgced 2 -ase 2 -msl 40 -sed -bbs -drloc shuffle -stloc mix -be -bnu -res -fer 0 -escr 100 -dgne -wnz -mmnu -cmd -esr 2 5 -elr -ebr 82 -emprp 75 125 -emi -nm1 random -rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi -mmprp 75 125 -gp 5000 -smc 3 -sws 10 -sfd 10 -sto 3 -ieor 33 -ieror 33 -ir 9,26,27,28,82,96,148,156,162,209,211,228 -csb 5 12 -mca -stra -saw -sisr 30 -sprp 75 125 -sdm 5 -npi -sebr -snsb -ccsr 30 -chrm 0 0 -cms -cspp 2.1.4.4.0.0.0.3.3.4.5.3.3.5.1.0.6.1.0.3 -frw -wmhc -cor 100 -crr 100 -crvr 125 150 -crm -ari -anca -adeh -ame 1 -nmc -noshoes -nu -nfps -fs -fe -fvd -fr -fj -fbs -fedc -fc -ond -etn
```

---

## Settings

### `-cg` (Character Gating)
**Full flag:** `--character-gating`
**Description:** Events are locked until required characters are recruited. This creates a more structured progression compared to open world mode.

---

## Objectives

The pootsleague uses 20 different objectives (A through T), each with specific conditions and rewards. The format is: `-oX RESULT.ARGS.CONDITIONS_MIN.CONDITIONS_MAX.CONDITIONS...`

### Objective A: `-oa 2.2.2.2.6.6.4.9.9`
- **Result:** Unlock Final Kefka (ID 2)
- **Conditions Required:** 2-2 (must complete exactly 2 conditions)
- **Condition 1:** Type 2 (Characters, min_max=True) - Recruit 6 Characters (args: 6.6)
- **Condition 2:** Type 4 (Espers, min_max=True) - Find 9 Espers (args: 9.9)

### Objective B: `-ob 3.1.1.10.20.20`
- **Result:** Unlock KT Skip (ID 3)  
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 10 (Checks, min_max=True) - Complete 20 Checks (args: 20.20)

### Objective C: `-oc 30.8.8.1.1.11.8`
- **Result:** Learn SwdTechs (ID 30) - 8 SwdTechs (args: 8.8)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Doma Dream Awaken (arg: 8)

### Objective D: `-od 59.1.1.11.31`
- **Result:** Magitek Upgrade (ID 59)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)  
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Magitek Factory Finish (arg: 31)

### Objective E: `-oe 62.1.1.11.44`
- **Result:** Auto Life 3 (ID 62)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Mt. Zozo Dragon (arg: 44)

### Objective F: `-of 26.8.8.1.1.11.26`
- **Result:** Learn Blitzes (ID 26) - 8 Blitzes (args: 8.8)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Lete River (arg: 26)

### Objective G: `-og 28.10.10.1.1.11.13`
- **Result:** Learn Lores (ID 28) - 10 Lores (args: 10.10)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Fanatic's Tower Leader (arg: 13)

### Objective H: `-oh 9.1.1.11.19`
- **Result:** Complete Checks (ID 9)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Floating Cont. Escape (arg: 19)

### Objective I: `-oi 31.10.10.1.1.11.3`
- **Result:** Learn Spells (ID 31) - 10 Spells (args: 10.10)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Burning House (arg: 3)

### Objective J: `-oj 8.1.1.11.0`
- **Result:** Complete Bosses (ID 8)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Ancient Castle (arg: 0)

### Objective K: `-ok 14.1.1.11.57`
- **Result:** Auto Safe (ID 14)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Zone Eater (arg: 57)

### Objective L: `-ol 16.1.1.11.59`
- **Result:** Auto Shell (ID 16)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Narshe Moogle Defense (arg: 59)

### Objective M: `-om 27.8.8.1.1.11.40`
- **Result:** Learn Dances (ID 27) - 8 Dances (args: 8.8)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Opera House Disruption (arg: 40)

### Objective N: `-on 7.1.1.11.40`
- **Result:** Complete Dragons (ID 7)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Opera House Disruption (arg: 40)

### Objective O: `-oo 48.10.10.1.1.2.9.9`
- **Result:** Vigor Random (ID 48) - +10 Vigor to random character (args: 10.10)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 2 (Characters, min_max=True) - Recruit 9 Characters (args: 9.9)

### Objective P: `-op 45.10.10.1.1.4.12.12`
- **Result:** MagPwr All (ID 45) - +10 Mag.Pwr to all characters (args: 10.10)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 4 (Espers, min_max=True) - Find 12 Espers (args: 12.12)

### Objective Q: `-oq 29.125.125.1.1.11.10`
- **Result:** Learn Rages (ID 29) - 125 Rages (args: 125.125)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Ebot's Rock (arg: 10)

### Objective R: `-or 37.1.1.11.48`
- **Result:** Dried Meat (ID 37)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 11 (Check, min_max=False) - Complete Serpent Trench (arg: 48)

### Objective S: `-os 38.1.1.12.7`
- **Result:** Exp. Egg (ID 38)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 12 (Quest, min_max=False) - Complete Suplex A Train (arg: 7)

### Objective T: `-ot 36.1.1.6.3.3`
- **Result:** Dragoon (ID 36)
- **Conditions Required:** 1-1 (must complete exactly 1 condition)
- **Condition 1:** Type 6 (Dragons, min_max=True) - Defeat 3 Dragons (args: 3.3)

---

## Starting Party

### `-sc1 random`, `-sc2 random`, `-sc3 random`
**Full flags:** `--start-char1 random`, `--start-char2 random`, `--start-char3 random`
**Description:** The first three starting party slots are filled with random characters. This creates variety in initial party composition while ensuring a party of 3.

---

## Characters

### `-sal`
**Full flag:** `--start-average-level`
**Description:** Recruited characters start at the average level of existing party members instead of their default level.

### `-eu`
**Full flag:** `--equipable-umaro`
**Description:** Umaro can access the equipment menu, allowing him to equip different gear instead of being restricted to his default bone club.

### `-csrp 80 125`
**Full flag:** `--character-stat-random-percent 80 125`
**Description:** Each character's base stats are randomized to 80-125% of their original values, creating stat diversity while maintaining relative character strengths.

---

## Commands & Abilities

### `-fst`
**Full flag:** `--fast-swdtech`
**Description:** SwdTech gauge charges four times faster, making SwdTechs much more practical to use.

### `-slr 4 5`
**Full flag:** `--start-lores-random 4 5`
**Description:** Start with 4-5 random lores already learned.

### `-lmprp 75 125`
**Full flag:** `--lores-mp-random-percent 75 125`
**Description:** Each lore's MP cost is set to 75-125% of its original cost.

### `-lel`
**Full flag:** `--lores-everyone-learns`
**Description:** Lores can be learned by characters without the Lore command.

### `-brl`
**Full flag:** `--bum-rush-last`
**Description:** Bum Rush can only be learned after learning every other blitz.

### `-srr 25 35`
**Full flag:** `--start-rages-random 25 35`
**Description:** Start with 25-35 random rages already learned.

### `-rnl`
**Full flag:** `--rages-no-leap`
**Description:** Gau cannot use the Leap command to learn new rages.

### `-rnc`
**Full flag:** `--rages-no-colosseum`
**Description:** Rages cannot be learned in the Colosseum.

### `-sdr 1 3`
**Full flag:** `--start-dances-random 1 3`
**Description:** Start with 1-3 random dances already learned.

### `-das`
**Full flag:** `--dances-all-shuffle`
**Description:** All dances are shuffled among their normal locations.

### `-dda`
**Full flag:** `--dances-dragoon-airship`
**Description:** Enable learning dances from the Falcon airship.

### `-dns`
**Full flag:** `--dances-no-stumble`
**Description:** Mog will not stumble when attempting to use Dance.

### `-sch`
**Full flag:** `--sketch-control-hack`
**Description:** Enable the Sketch/Control glitch fix.

### `-scis`
**Full flag:** `--sketch-control-improved-safety`
**Description:** Improved safety measures for Sketch and Control commands.

---

## Level Scaling

### `-lsced 2`
**Full flag:** `--level-scaling-ced 2`
**Description:** Enemies and bosses gain 2 levels for each Character recruited, Esper acquired, and Dragon defeated.

### `-hmced 2`
**Full flag:** `--hp-mp-scaling-ced 2`
**Description:** Enemy and boss HP/MP scales by a factor of 2 for each character recruited, esper acquired, and dragon defeated.

### `-xgced 2`
**Full flag:** `--xp-gp-scaling-ced 2`
**Description:** Enemy and boss EXP/GP scales by a factor of 2 for each character recruited, esper acquired, and dragon defeated.

### `-ase 2`
**Full flag:** `--ability-scaling-element 2`
**Description:** Enemy and boss abilities retain their element and increase in tier approximately every 5 levels (2+3), reaching max tier at level 40.

### `-msl 40`
**Full flag:** `--max-scale-level 40`
**Description:** Maximum level enemies can be scaled up to is 40 (distortion levels still apply on top of this).

### `-sed`
**Full flag:** `--scale-eight-dragons`
**Description:** Apply level scaling to the eight legendary dragons.

---

## Bosses

### `-bbs`
**Full flag:** `--boss-battles-shuffle`
**Description:** Boss battles are shuffled among their locations, so you might fight Ultros at Kefka's Tower or the Phantom Train boss in the Coliseum.

### `-drloc shuffle`
**Full flag:** `--dragon-boss-location shuffle`
**Description:** The eight dragon encounters are shuffled among boss locations.

### `-stloc mix`
**Full flag:** `--statue-boss-location mix`
**Description:** The three statue encounters (Doom, Poltrgeist, Goddess) are mixed with regular bosses and dragons.

### `-be`
**Full flag:** `--boss-experience`
**Description:** Boss battles award experience points instead of the usual 0 EXP.

### `-bnu`
**Full flag:** `--boss-no-undead`
**Description:** Removes the undead status from bosses, preventing instant death from healing items/spells.

---

## Encounters

### `-res`
**Full flag:** `--random-encounters-shuffle`
**Description:** Random encounters are shuffled between different areas.

### `-fer 0`
**Full flag:** `--fixed-encounters-random 0`
**Description:** Fixed encounters (Lete River, Serpent Trench, Mine Cart, etc.) are randomized with 0% boss replacement rate.

### `-escr 100`
**Full flag:** `--encounters-escapable-random 100`
**Description:** 100% of random encounters are escapable, including with Warp or Smoke Bombs.

---

## Espers

### `-esr 2 5`
**Full flag:** `--esper-spells-random 2 5`
**Description:** Each esper teaches 2-5 random spells instead of their original spell list.

### `-elr`
**Full flag:** `--esper-learnrates-random`
**Description:** The rates at which espers teach spells are randomized.

### `-ebr 82`
**Full flag:** `--esper-bonuses-random 82`
**Description:** Esper stat bonuses are randomized with an 82% chance of receiving a bonus.

### `-emprp 75 125`
**Full flag:** `--esper-mp-random-percent 75 125`
**Description:** Each esper's MP cost is set to 75-125% of its original cost.

### `-emi`
**Full flag:** `--esper-mastered-icon`
**Description:** Adds an icon to show when all spells have been learned from an esper.

---

## Natural Magic

### `-nm1 random`, `-nm2 random`
**Full flags:** `--natural-magic1 random`, `--natural-magic2 random`
**Description:** Terra's and Celes' natural magic are assigned to random characters instead of their original owners.

### `-rnl1`, `-rnl2`
**Full flags:** `--random-natural-levels1`, `--random-natural-levels2`
**Description:** Randomize the levels at which the first and second natural magic sets are learned.

### `-rns1`, `-rns2`
**Full flags:** `--random-natural-spells1`, `--random-natural-spells2`
**Description:** Randomize which spells are learned naturally for both natural magic sets.

### `-nmmi`
**Full flag:** `--natural-magic-menu-indicator`
**Description:** Add an indicator to the status menu for characters with natural magic.

---

## Experience, Magic Points, Gold

### `-xpm 3`
**Full flag:** `--xp-mult 3`
**Description:** Multiply experience gained by 3x.

### `-mpm 5`
**Full flag:** `--mp-mult 5`
**Description:** Multiply magic points gained by 5x.

### `-gpm 5`
**Full flag:** `--gp-mult 5`
**Description:** Multiply gold gained by 5x.

### `-nxppd`
**Full flag:** `--no-exp-party-divide`
**Description:** Experience is not divided by the number of surviving party members - each member gets full EXP.

---

## Items

### `-ieor 33`
**Full flag:** `--item-equipable-original-random 33`
**Description:** Characters have a 33% chance of being able to equip each item they previously could not equip.

### `-ieror 33`
**Full flag:** `--item-equipable-relic-original-random 33`
**Description:** Characters have a 33% chance of being able to equip each relic they previously could not equip.

### `-ir 9,26,27,28,82,96,148,156,162,209,211,228`
**Full flag:** `--item-rewards`
**Description:** Specifies exact items that will appear as check rewards: ValiantKnife (9), Illumina (26), Ragnarok (27), Atma Weapon (28), Dice (82), Flame Shld (96), Force Armor (148), Minerva (156), Snow Muffler (162), Genji Glove (209), Offering (211), Exp. Egg (228).

### `-csb 5 12`
**Full flag:** `--cursed-shield-battles 5 12`
**Description:** The Cursed Shield requires 5-12 battles to uncurse instead of the original 256.

### `-mca`
**Full flag:** `--moogle-charm-all`
**Description:** All characters can wear Moogle Charm relics to prevent random battles.

### `-stra`
**Full flag:** `--swdtech-runic-all`
**Description:** All weapons enable both SwdTech and Runic commands.

### `-saw`
**Full flag:** `--stronger-atma-weapon`
**Description:** Atma Weapon is moved to a higher tier and its damage divisor is reduced from 64 to 32.

---

## Shops

### `-sisr 30`
**Full flag:** `--shop-inventory-shuffle-random 30`
**Description:** Shop inventories are randomized with 30% random replacement rate after shuffling by type.

### `-sprp 75 125`
**Full flag:** `--shop-prices-random-percent 75 125`
**Description:** Item prices are set to 75-125% of their original cost.

### `-sdm 5`
**Full flag:** `--shop-dried-meat 5`
**Description:** 5 shops will contain dried meat items.

### `-npi`
**Full flag:** `--no-priceless-items`
**Description:** Assigns proper values to items that normally sell for 1 gold (recommended with random inventory).

### `-sebr`
**Full flag:** `--shops-expensive-breakable-rods`
**Description:** Breakable rods (Poison, Fire, Ice, Thunder, Gravity, Pearl) have their base prices increased.

### `-snsb`
**Full flag:** `--shops-no-super-balls`
**Description:** Super Balls are not sold in shops.

---

## Misc Magic

### `-mmprp 75 125`
**Full flag:** `--magic-mp-random-percent 75 125`
**Description:** Each magic spell's MP cost is set to 75-125% of its original cost.

---

## Starting Gold/Items

### `-gp 5000`
**Full flag:** `--gold 5000`
**Description:** Start the game with 5000 gold.

### `-smc 3`
**Full flag:** `--start-moogle-charms 3`
**Description:** Start with 3 Moogle Charms (overrides No Moogle Charms challenge).

### `-sws 10`
**Full flag:** `--start-warp-stones 10`
**Description:** Start with 10 Warp Stones.

### `-sfd 10`
**Full flag:** `--start-fenix-downs 10`
**Description:** Start with 10 Fenix Downs.

### `-sto 3`
**Full flag:** `--start-tools 3`
**Description:** Start with 3 different random tools.

---

## Commands

### `-com 98989898989898989898989898`
**Full flag:** `--commands`
**Description:** Specifies exact command assignments for each character (2 digits per character). "98" represents "Random Unique Command" - each character gets a random command assignment with no duplicates.

### `-rec1 28`, `-rec2 97`
**Full flags:** `--random-exclude-command1 28`, `--random-exclude-command2 97`
**Description:** Excludes specific commands from random assignment: ID 28 = "Possess", ID 97 = "None Command". This prevents characters from getting these commands when randomized.

---

## Challenges

### `-nmc`
**Full flag:** `--no-moogle-charms`
**Description:** Moogle Charms will not appear in coliseum, auction, shops, chests, or events.

### `-noshoes`
**Full flag:** `--no-sprint-shoes`
**Description:** Sprint Shoes will not appear in coliseum, auction, shops, or chests.

### `-nu`
**Full flag:** `--no-ultima`
**Description:** Ultima cannot be learned from espers, items, or natural magic.

### `-nfps`
**Full flag:** `--no-free-paladin-shields`
**Description:** Paladin and Cursed Shields will not appear in coliseum, auction, shops, chests, or events (Narshe WOR exclusive).

---

## Graphics

The pootsleague includes numerous character sprite and palette customizations. These flags control visual appearance but don't affect gameplay balance:

### `-dgne`, `-wnz`, `-mmnu`, `-cmd`
**Description:** Various character sprite modifications for visual variety.

### `-ccsr 30`
**Full flag:** `--character-color-shuffle-random 30`
**Description:** Character colors are shuffled with 30% randomization.

### `-chrm 0 0`
**Full flag:** `--character-replacement-mode 0 0`
**Description:** Character replacement settings for sprite variations.

### `-cms`
**Full flag:** `--character-multiparts-sprites`
**Description:** Enable multi-part character sprites.

### `-cspp 2.1.4.4.0.0.0.3.3.4.5.3.3.5.1.0.6.1.0.3`
**Full flag:** `--character-sprite-palette-pairs`
**Description:** Specific sprite and palette combinations for each character.

### `-frw`, `-wmhc`
**Description:** Additional graphics modifications for character appearance.

### Color Randomization: `-cor 100`, `-crr 100`, `-crvr 125 150`, `-crm`
**Description:** Various color randomization settings with specific ranges and modes.

### Graphics Exclusions: `-ari`, `-anca`, `-adeh`, `-ame 1`
**Description:** Excludes certain graphics modifications or sets specific modes.

---

## Final Flags

### `-fs`, `-fe`, `-fvd`, `-fr`, `-fj`, `-fbs`, `-fedc`, `-fc`
**Description:** Various final graphics and sprite settings that complete the visual customization.

### `-ond`
**Full flag:** `--original-name-display`
**Description:** Display original character names in party and party select menus.

### `-etn`
**Full flag:** `--event-timers-none`
**Description:** Removes timers from Collapsing House, Opera House, and Floating Continent events.

---

## Summary

The pootsleague flagset creates a comprehensive randomized experience with:
- **20 varied objectives** providing multiple paths to victory with specific rewards like ability unlocks and stat bonuses
- **Balanced scaling** that increases difficulty as you progress through character/esper/dragon acquisition
- **Random character abilities** while maintaining equipment diversity through percentage-based randomization
- **Economic balance** through shop and item randomization with controlled price ranges
- **Visual variety** through extensive sprite customization
- **Quality of life** improvements like faster SwdTech charging, timer removal, and experience bonuses

This flagset is designed for competitive play where consistency and balance are prioritized over extreme randomization or difficulty spikes. The objectives system provides clear goals while the scaling ensures appropriate challenge progression.

---

## Technical Notes

This glossary was created by analyzing the World's Collide randomizer source code, specifically:
- `/args/` modules for flag definitions
- `/constants/` modules for ID mappings (objectives, items, characters, etc.)
- The actual pootsleague command string for accurate flag parsing

All objective rewards, condition types, item IDs, and character/esper mappings have been verified against the codebase constants.