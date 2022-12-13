from enum import Enum
from dataclasses import dataclass

class OperationType(Enum):
    Multiplication = "*"
    Addition = "+"
    @staticmethod
    def from_string(s) -> "OperationType":
        match s:
            case OperationType.Addition:
                return OperationType.Addition
            case OperationType.Multiplication:
                return OperationType.Multiplication
            case _:
                raise NotImplementedError("Error parsing Operation: ", s)

@dataclass
class Operation:
    op_type : OperationType
    value : int

MonkeyId = int
TestNum = int
Item = int
StartItems = list[Item]
ThrowCondition = (bool, MonkeyId)
MonkeyConditions = list[ThrowCondition]
Monkey = (MonkeyId, StartItems , Operation, TestNum, MonkeyConditions)

def parse_monkey(lines : list[str]) -> Monkey:

    # first line is always id
    monke_id = int(lines.pop(0))
    # 2nd line always contains the items
    start_line = lines.pop(0).split(":")[-1].strip()
    start_items : StartItems = [int(i.strip()) for i in start_line.split(",")]

    # third line contains operation
    op_line = lines.pop(0).split("old ")[-1].strip()
    op_type, op_val = op_line.split(" ")
    monke_op : Operation = Operation(OperationType.from_string(op_type), int(op_val))

    # 4th line is always test
    monke_test : TestNum = int(lines.pop(0).split(" ")[-1].strip())

    # last lines are always the throw conditions
    monke_conds : MonkeyConditions = []

    for c in lines:
        cond_line = c.strip().split(" ")
        bool_val = True if cond_line[1] == "true" else False
        throw_to = int(cond_line[-1])
        cond : ThrowCondition = (bool_val, throw_to)
        monke_conds.append(cond)
    monke: Monkey = (monke_id, start_items, monke_op, monke_test, monke_conds)
    return monke

def day_11(file_obj):
    return None
