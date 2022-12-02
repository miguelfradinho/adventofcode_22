import enum 
def get_file(exercise, ext="txt"):
    return open(f"input_{exercise}.{ext}", "r", encoding="utf-8")


def day_2(name):
    class Move_them(enum.StrEnum):
        ROCK = "A"
        PAPER = "B"
        SCISSORS = "C"
    class Move_me(enum.StrEnum):
        ROCK = "X"
        PAPER = "Y"
        SCISSORS = "Z"

    class Shape(enum.IntEnum):
        # Points for the shape
        ROCK = 1 
        PAPER = 2
        SCISSORS = 3
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

    def get_score(them, me) -> int:

        theirs, mine = get_move(them, Move_them),get_move(me,Move_me)
        
        return mine + get_outcome_as_win(theirs, mine)


    results = [] 
    with get_file(name) as f:
        results = [get_score(*line.strip().split(" ")) for line in f]
        return sum(results)

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
    STOP_AT = f"{fun_prefix}{STOP}" 

    clean_globals = {k:v for k,v in globals().items() if k.startswith(fun_prefix)}
    for i in fun_names:
        if i == STOP_AT:
            break
        fun = clean_globals[i]
        print(f"{i} - {fun(i)}")
main()