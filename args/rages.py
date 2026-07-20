def name():
    return "Rages"

def parse(parser):
    from data.rages import Rages

    rages = parser.add_argument_group("Rages")

    rages.add_argument("-srr", "--start-rages-random", default = None, type = int,
                       nargs = 2, metavar = ("MIN", "MAX"), choices = range(Rages.RAGE_COUNT),
                       help = "Start with random rages learned")

    rages.add_argument("-rnl", "--rages-no-leap", action = "store_true",
                       help = "Leap not available on the Veldt. Rages learnable after every battle")

    rages.add_argument("-rnc", "--rages-no-charm", action = "store_true",
                       help = "Charm ability not available from Nightshade rage")

    rages.add_argument("-rsc", "--rage-special-chance", default = None, type = int,
                       metavar = "PERCENT", choices = range(101),
                       help = "Percent chance that Rage uses the monster's special attack instead of Fight (vanilla: 50)")

def process(args):
    args._process_min_max("start_rages_random")

def flags(args):
    flags = ""

    if args.start_rages_random:
        flags += f" -srr {args.start_rages_random_min} {args.start_rages_random_max}"

    if args.rages_no_leap:
        flags += " -rnl"

    if args.rages_no_charm:
        flags += " -rnc"

    if args.rage_special_chance is not None:
        flags += f" -rsc {args.rage_special_chance}"

    return flags

def options(args):
    start_rages = "Original"
    if args.start_rages_random:
        start_rages = f"Random {args.start_rages_random_min}-{args.start_rages_random_max}"

    rage_special_chance = "Original (50%)"
    if args.rage_special_chance is not None:
        rage_special_chance = f"{args.rage_special_chance}%"

    return [
        ("Start Rages", start_rages, "start_rages"),
        ("No Leap", args.rages_no_leap, "rages_no_leap"),
        ("No Charm", args.rages_no_charm, "rages_no_charm"),
        ("Rage Special Chance", rage_special_chance, "rage_special_chance"),
    ]

def menu(args):
    entries = options(args)
    for index, entry in enumerate(entries):
        key, value, unique_name = entry
        if key == "Start Rages":
            value = value.replace("Random ", "")
            entries[index] = (key, value, unique_name)
    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
