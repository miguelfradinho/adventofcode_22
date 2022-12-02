def get_file(exercise, ext="txt"):
    return open(f"input_{exercise}.{ext}", "r", encoding="utf-8")



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
    STOP = 2
    STOP_AT = f"{fun_prefix}{STOP}" 

    clean_globals = {k:v for k,v in globals().items() if k.startswith(fun_prefix)}
    for i in fun_names:
        if i == STOP_AT:
            break
        fun = clean_globals[i]
        print(f"{i} - {fun(i)}")
main()