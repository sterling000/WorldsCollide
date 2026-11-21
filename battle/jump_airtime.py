from memory.space import Reserve
import args

class _JumpAirtime:
    '''Shorten how long a jumping character hangs in the air.

    Jump has no timer of its own and does not run on the main ATB gauge.  While a character is in
    the airborne mask $3f2c the battle loop routes them to C2/1193, which each tick adds half their
    ATB rate ($3ac8,x >> 1) to a second counter at $3ab4,x and lands them once its high byte reaches
    the per character threshold $322c,x.

    That threshold comes from a 30 entry table of per action delays at C2/067b, indexed by command
    id and applied at C2/03f6.  Every ordinary action is $10, the slower ones $20, and Jump is $e0
    - fourteen times a normal attack, which is the whole of the air time.  Air time in ticks is
    (delay * 256) / (atb rate / 2), so the entry scales it linearly and, being indexed by command,
    touches nothing but Jump.
    '''

    ACTION_DELAY_START = 0x2067b        # 30 entries, one per command id
    JUMP_COMMAND = 22
    VANILLA_DELAY = 0xe0

    @classmethod
    def delay(cls, percent):
        return max(min(cls.VANILLA_DELAY * percent // 100, 0xfe), 0x01)

    def __init__(self):
        if args.jump_airtime is None or args.jump_airtime == 100:
            return

        address = self.ACTION_DELAY_START + self.JUMP_COMMAND
        space = Reserve(address, address, "jump airtime action delay")
        space.write(self.delay(args.jump_airtime))

jump_airtime = _JumpAirtime()
