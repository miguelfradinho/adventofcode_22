from enum import Enum
from dataclasses import dataclass
from typing import Literal


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


PreviousVariable = Literal["old"]
Operand = int | PreviousVariable


@dataclass
class Operation:
    operator: OperationType
    left: Operand
    right: Operand

    def __repr__(self):
        return f"<{self.left} {self.operator} {self.right}>"

    @staticmethod
    def parse(s: str) -> "Operation":
        # operations are always in the form of "<operand> <operation> <operand>"
        l: Operand
        t: Operand
        l, op, r = s.split(" ")
        # try casting for...idk?
        try:
            l = int(l)
        except ValueError:
            l = PreviousVariable

        try:
            r = int(r)
        except ValueError:
            r = PreviousVariable
        return Operation(left=l, operator=OperationType.from_string(op), right=r)


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
    return monkeys
