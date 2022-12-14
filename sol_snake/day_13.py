from typing import Union, IO, TypeVar

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

def day_13(file_obj):
    example = open("sol_snake\example_13.txt", encoding="utf-8")
    packet_pairs = parse_input(example)
    return packet_pairs
