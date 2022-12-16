from typing import Union, IO, TypeVar, Optional

TData = TypeVar("TData", int, list)
PacketData = list[TData]

class Pair:
    left: PacketData
    right: PacketData
    def __init__(self, *, left,right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"<l=({self.left}), r=({self.right})>"
def parse_input_packet(line):
    # extremely lazy mode (and insecure as well)
    return eval(line)

def parse_input(file_obj : IO):
    # Each pair is separated by a blank line
    # We could read all lines and do replacement, but input file seems large enough to justify using
    # the buffered approach

    total_pairs = []
    with file_obj as f:
        pair = []
        while True:
            line = f.readline()
            # EOF
            if line == "":
                break
            # remove new lines
            clean = line.strip()
            # separator, so we got our pair
            if clean == "":
                total_pairs.append(Pair(left=pair[0], right=pair[1]))
                pair = []
            else:
                # we don't, so parse the packet 
                packet = parse_input_packet(clean)
                pair.append(packet)
    return total_pairs

def compare_values(left: PacketData, right : PacketData) -> Optional[bool]:

    # if they both have the same type
    if type(left) == type(right):
        # both are integers
        if type(left) == int:
            # If the left integer is higher than the right integer, the inputs are not in the right order.
            if left > right:
                return False
            # if they're equal, we need a way of skipping, so, we'll return None
            elif left == right:
                return None
            # Otherwise, the inputs are the same integer; continue checking the next part of the input.
            return True
        # both are lists
        elif type(left) == list:
            # compare each value
            for i in range(len(left)):
                curr_left = left[i]
                # if right side happens to have less items, then we should return false
                try:
                    curr_right = right[i]
                except IndexError:
                    return False
                curr_res = compare_values(curr_left, curr_right)
                # check if it's None, if yes, then just keep doing it, cuz we won't reach a conclusion
                if curr_res is None:
                    continue
                return curr_res
            # if we reached here, and right side still has more items, then we are correct
            if len(left) < len(right):
                return True
            # if we reached here, we didn't reach a conclusion, so return None
            return None
    # If exactly one value is an integer, convert the integer to a list which contains that integer as its only value
    if type(left) == int:
        return compare_values([left], right)
    elif type(right) == int:
        return compare_values(left, [right])
    else:
        raise ValueError("we should never reach here", left, right)


def day_13(file_obj):
    #example = open("sol_snake\example_13.txt", encoding="utf-8")
    packet_pairs = parse_input(file_obj)

    correct_pairs = []

    # for each pair
    for i in range(len(packet_pairs)):
        curr_pair = packet_pairs[i]
        left = curr_pair.left
        right = curr_pair.right

        pair_is_correct = compare_values(left, right)
        if pair_is_correct:
            correct_pairs.append(i+1)

    print(correct_pairs)
    return sum(correct_pairs)
