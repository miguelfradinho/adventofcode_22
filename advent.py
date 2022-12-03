import enum 
def get_file(exercise, ext="txt"):
    return open(f"input_{exercise}.{ext}", "r", encoding="utf-8")

def day_3(name):
    def get_priority(char):
        if "a" <= char <= "z":
            return ord(char)-96
        elif "A" <= char <= "Z":
            return ord(char)-38
        else:
            raise ValueError("Wrong char")

    rucksacks = [line.strip() for line in get_file(name)]
    
    item_types = []
    badges = []
    
    for bag in rucksacks:
        n_times = len(bag)//2
        first_half, second_half = set(bag[:n_times]), set(bag[n_times:])
        common = first_half.intersection(second_half)            
        item_types.extend(common)

    group_size = 3

    for i in range(0, len(rucksacks), group_size):
        group_bags = [set(r) for r in rucksacks[i:i+group_size]]
        badge_letter = group_bags[0].intersection(*group_bags[1:])
        badges.extend(badge_letter)

    return sum([get_priority(i) for i in item_types]), sum([get_priority(i) for i in badges]), 

def day_2(name):
    class Move_them(enum.StrEnum):
        ROCK = "A"
        PAPER = "B"
        SCISSORS = "C"
    class Move_me(enum.StrEnum):
        ROCK = "X"
        PAPER = "Y"
        SCISSORS = "Z"
    class Move_Result(enum.StrEnum):
        # Points for the outcome
        LOSS = "X"
        DRAW = "Y"
        WIN = "Z"
    
    class Shape(enum.IntEnum):
        # Points for the shape
        ROCK = 1 
        PAPER = 2
        SCISSORS = 3

        def __invert__(self) -> int:
            if self is Shape.ROCK:
                return Shape.PAPER
            if self is Shape.PAPER:
                return Shape.SCISSORS
            if self is Shape.SCISSORS:
                return Shape.ROCK
        def __xor__(self, __n: int) -> int:
            if self is Shape.ROCK:
                return Shape.SCISSORS
            if self is Shape.PAPER:
                return Shape.ROCK
            if self is Shape.SCISSORS:
                return Shape.PAPER
    
    class Outcome(enum.IntEnum):
        # Points for the outcome
        LOSS = 0
        DRAW = 3
        WIN = 6 
    
    def get_move(move, move_map : Move_them | Move_me) -> Shape:       
        match move:
            case move_map.ROCK:
                return Shape.ROCK
            case move_map.PAPER:
                return Shape.PAPER
            case move_map.SCISSORS:
                return Shape.SCISSORS
            case _:
                raise ValueError("Invalid argument", move, move_map)

    
    def get_result(move, move_map : Move_Result) -> Shape:       
        match move:
            case move_map.LOSS:
                return Outcome.LOSS
            case move_map.DRAW:
                return Outcome.DRAW
            case move_map.WIN:
                return Outcome.WIN
            case _:
                raise ValueError("Invalid argument", move, move_map)

    def get_outcome_as_win(them : Shape, me : Shape) -> Outcome:
        if them == me:
            return Outcome.DRAW
        if them is Shape.ROCK:
            if me is Shape.PAPER:
                return Outcome.WIN
            return Outcome.LOSS
        
        if them is Shape.PAPER:
            if me is Shape.SCISSORS:
                return Outcome.WIN
            return Outcome.LOSS

        if them is Shape.SCISSORS:
            if me is Shape.ROCK:
                return Outcome.WIN
            return Outcome.LOSS


    def get_outcome_as_result(them : Shape, result : Outcome) -> Shape: 
        if result is Outcome.DRAW:
            return them 

        elif result is Outcome.WIN:
            return ~them
        
        elif result is Outcome.LOSS:
            return them^0 

        else:
            raise ValueError(them, result)


    results_as_win = []
    results_as_outcome = [] 
    with get_file(name) as f:
        for line in f:
            clean_line = line.strip()
            col1, col2 = clean_line.split(" ")
            
            theirs = get_move(col1, Move_them)
            
            # Moves as col2 = Move to win
            mine = get_move(col2, Move_me)
            results_as_win.append(mine + get_outcome_as_win(theirs,mine))
            
            # Moves as col2 = end result 
            res = get_result(col2, Move_Result)
            results_as_outcome.append(res + get_outcome_as_result(theirs,res))
        
        assert len(results_as_win) == len(results_as_outcome)

        return sum(results_as_win), sum(results_as_outcome)

def day_1(name):
    with get_file(name) as f:
        # sepparate the groups and numbers by a different character, to make it easier
        raw_numbers = f.read().replace("\n\n",";").replace("\n",",")[:-1]
        # split the groups and sum the numbs
        elfs_totals = [sum(int(j) for j in i.split(",")) for i in raw_numbers.split(";")]
        
        elfs_totals.sort(reverse=True)

        return elfs_totals[0], sum(elfs_totals[:3])

def main():
    fun_prefix = "day_"
    fun_names = [f"{fun_prefix}{i}" for i in range(1, 26)]
    STOP = 3
    STOP_AT = f"{fun_prefix}{STOP+1}" 

    clean_globals = {k:v for k,v in globals().items() if k.startswith(fun_prefix)}
    for i in fun_names:
        if i == STOP_AT:
            break
        fun = clean_globals[i]
        print(f"{i} - {fun(i)}")
main()