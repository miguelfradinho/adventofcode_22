from dataclasses import dataclass


@dataclass
class NoOp:
    _value: None = None
    _cycles: int = 1

    @property
    def value(self):
        return self._value

    @property
    def cycles(self):
        return self._cycles


@dataclass
class AddX:
    _value: int
    _cycles: int = 2

    @property
    def value(self):
        return self._value

    @property
    def cycles(self):
        return self._cycles


Instruction = AddX | NoOp


def parse_instructions(file_obj) -> list[Instruction]:
    insts: list[Instruction] = []
    with file_obj as f:
        for line in f:
            line: str = line.strip()
            if line.startswith("noop"):
                new_inst = NoOp()
            elif line.startswith("addx"):
                _, v = line.split(" ")
                new_inst = AddX(int(v))
            else:
                raise ValueError("error parsing in line", line)
            insts.append(new_inst)

    return insts


class CRT:
    height: int
    width: int

    def __init__(self):
        self.height = 6
        self.width = 40

        self._height_index = 1
        self._rows = []
        self._sprite_size = 3
        self._current_row = ""

    def _build_sprite(self, val: int):
        try:
            sprite_row = ["."] * self.width
            # middle position
            sprite_row[val] = "#"
            # one behind
            sprite_row[val - 1] = "#"
            # one forward
            sprite_row[(val + 1) % self.width] = "#"
        except IndexError:
            print(val)
            return None
        return sprite_row

    def show_screen(self):
        return "\n".join(self._rows)

    def draw(self, cpu_cycle, register_value):
        sprite_position = self._build_sprite(register_value)

        sprite_index = cpu_cycle % self.width - 1
        # append
        self._current_row += sprite_position[sprite_index]

        # we finished a row, so reset and add
        if cpu_cycle == (self._height_index * self.width):
            self._rows.append(self._current_row)
            self._current_row = ""
            self._height_index += 1


class CPU:
    _register: int
    _instructions: list[Instruction]
    _cycle: int
    _signal_strengths: list[int]
    _checkpoints: list[int]

    def __init__(self, instructions: list[Instruction], crt: CRT):
        self._register = 1
        self._inst_backup = instructions.copy()
        self._instructions = instructions
        self._cycle = 0
        self._signal_strengths = []
        self._checkpoints = [20, 60, 100, 140, 180, 220]
        self.crt = crt

    @property
    def strengths(self):
        return self._signal_strengths

    @property
    def register(self):
        return self._register

    @property
    def cycle(self):
        return self._cycle

    def update_signal(self):
        if self._cycle in self._checkpoints:
            # remove it
            self._checkpoints.pop(0)
            self._signal_strengths.append(self._register * self._cycle)

    def run(self):
        curr_inst = None
        pc_counter = 0

        while True:
            # update strengths
            self.update_signal()

            # if we have a instruction running
            if curr_inst is not None:
                # if we haven't finished process it, just increment the counter
                if self._cycle != pc_counter:
                    # current cycle
                    self._cycle += 1
                    # draw on screen
                    self.crt.draw(self.cycle, self.register)
                # check if we finished "processing" it
                else:
                    # if we finished, update the counter
                    pc_counter = 0
                    # add value for addx
                    if type(curr_inst) is AddX:
                        self._register += curr_inst.value
                    elif type(curr_inst) is NoOp:
                        pass
                    else:
                        raise ValueError("Wrong Instruction")
                    # reset the inst
                    curr_inst = None
                # move to next cycle
                continue
            else:
                # get next instruction
                try:
                    next_inst = self._instructions.pop(0)
                    # out of instructions
                except IndexError:
                    break

                # set the current instruction
                curr_inst = next_inst
                pc_counter = self._cycle + curr_inst.cycles

        print("CPU has finished running")


def day_10(file_obj):

    example_2 = open("sol_snake\example_10_2.txt", encoding="utf-8")
    # insts_ex_2 = parse_instructions(example_2)
    # program_ex_2 = CPU(insts_ex_2)
    # program_ex_2.run()

    # print(program_ex_2.strengths)
    # print(sum(program_ex_2.strengths))

    screen = CRT()
    insts = parse_instructions(file_obj)
    program = CPU(insts, screen)
    program.run()

    print(screen.show_screen())
    return sum(program.strengths)
