from enum import Enum
from dataclasses import dataclass
from typing import Optional
import math


class OperationType(Enum):
    Multiplication = "*"
    Addition = "+"

    @staticmethod
    def from_string(s) -> "OperationType":
        match s:
            case OperationType.Addition.value:
                return OperationType.Addition
            case OperationType.Multiplication.value:
                return OperationType.Multiplication
            case _:
                raise NotImplementedError("Error parsing Operation: ", s)

    def __str__(self):
        return self.value


@dataclass
class Operation:
    operator: OperationType
    constant: Optional[int] = None
    square: bool = False

    @staticmethod
    def parse(s: str) -> "Operation":

        # left hand side is always the old variable, so we only need to check the 2nd side
        _, op, r = s.split(" ")
        operator = OperationType.from_string(op)
        try:
            # try to create one with the constant
            r = int(r)
            return Operation(operator, int(r))
            # Fails when it's to multiply the old value, so, square
        except ValueError:
            return Operation(operator, None, True)


MonkeyId = int
Item = int
MonkeyItems = list[Item]


@dataclass
class DivisionTest:
    value: int
    true_throw: MonkeyId
    false_throw: MonkeyId

    def __repr__(self):
        return f"<val={self.value}, true=Monkey_{self.true_throw}, false=Monkey_{self.true_throw}>"


class Monkey:
    def __init__(
        self, id: MonkeyId, start_items: MonkeyItems, op: Operation, test: DivisionTest
    ):
        self.id = id
        self.items = start_items
        """ Worry level for each item the monkey is currently holding, in the ORDER they will be inspected"""
        self.operation = op
        self.test = test

    def __repr__(self):
        return f"Monkey<id={self.id}, items={self.items}, operation={self.operation}, test={self.test}>"


def parse_monkey(lines: list[str]) -> Monkey:
    # first line is always id
    monke_id = int(lines.pop(0).strip("Monkey").strip(":").strip())
    # 2nd line always contains the items
    start_line = lines.pop(0).split(":")[-1].strip()
    start_items: MonkeyItems = [int(i.strip()) for i in start_line.split(",")]


    # third line contains operation
    op_line = lines.pop(0).split("= ")[-1].strip()
    monke_op = Operation.parse(op_line)

    # 4th line is always the value to divide, followed by the throw conditions
    test_val = int(lines.pop(0).split(" ")[-1].strip())
    true_return_to = int(lines.pop(0).split(" ")[-1].strip())
    false_return_to = int(lines.pop(0).split(" ")[-1].strip())
    monke_test = DivisionTest(test_val, true_return_to, false_return_to)

    monke = Monkey(monke_id, start_items, monke_op, monke_test)
    return monke


def calculate_worry(old_value: int, op: Operation) -> int:
    # easy case
    if op.operator is OperationType.Addition:
        return old_value + op.constant
    # hard case
    elif op.operator is OperationType.Multiplication:
        # old variable
        if not op.square:
            return old_value * op.constant
        else:
            return old_value * old_value
    else:
        raise ValueError("wrong operator")


def parse_input(file_obj) -> list[Monkey]:
    monkeys: list[Monkey] = []
    with file_obj as f:
        monkey_lines: list[str] = []
        for line in f.read().split("\n"):
            line = line.strip()
            # blank line means new monkey?
            if line == "":
                curr_monkey = parse_monkey(monkey_lines)
                monkeys.append(curr_monkey)
                monkey_lines = []
                continue
            else:
                monkey_lines.append(line)
    return monkeys


def day_11(file_obj):
    example = open("sol_snake\example_11.txt", encoding="utf-8")
    monkeys = parse_input(example)

    total_rounds = 20

    monkey_inspections: dict[MonkeyId, int] = {}
    monkey_round_items: dict[int, (MonkeyId, MonkeyItems)] = {}
    # The process of each monkey taking a single turn is called a round.
    for curr_round in range(total_rounds):
        # The monkeys take turns inspecting and throwing items
        for monkey in monkeys:
            # On a single monkey's turn, it inspects and throws all the items
            # it is holding one at a time and in the order listed.
            while True:
                try:
                    old_worry = monkey.items.pop(0)
                except IndexError:
                    # out of items
                    break
                # first, note down the inspection (which is equal to the number of elements in the items)
                monkey_inspections[monkey.id] = monkey_inspections.get(monkey.id, 0) + 1

                # apply the operation
                new_worry = calculate_worry(old_worry, monkey.operation)

                # After each monkey inspects an item BUT BEFORE it tests your worry level
                # your Worry level is divided by 3 and rounded down to the nearest int
                final_worry = math.floor(new_worry / 3)

                # check division
                divisible = final_worry % monkey.test.value == 0
                if divisible:
                    next_monkey = monkey.test.true_throw
                else:
                    next_monkey = monkey.test.false_throw
                # Throw to monkey
                monkeys[next_monkey].items.append(final_worry)
        # at the end of each round, add the current items
        monkey_round_items[curr_round] = [(m.id, m.items) for m in monkeys]

    print(monkey_inspections)

    # after all rounds ended, check the monkey_business
    first_max_key = max(monkey_inspections, key=monkey_inspections.get)
    # and pop it
    first_max = monkey_inspections.pop(first_max_key)
    # find the second max
    second_max_key = max(monkey_inspections, key=monkey_inspections.get)
    second_max = monkey_inspections.pop(second_max_key)
    return first_max * second_max
