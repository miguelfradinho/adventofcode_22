def get_file(exercise, ext="txt"):
    return open(f"input_{exercise}.{ext}", "r", encoding="utf-8")



def day_1(name):
    with get_file(name) as f:
        # sepparate the groups and numbers by a different character, to make it easier
        raw_numbers = f.read().replace("\n\n",";").replace("\n",",")[:-1]
        # split the groups and sum the numbs
        elfs_totals = [sum(int(j) for j in i.split(",")) for i in raw_numbers.split(";")]
        
        return max(elfs_totals)

def main():
    print(day_1("day_1_main"))

main()