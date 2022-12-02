def get_file_name(exercise, ext="txt"):
    return f"input_{exercise}.{ext}"



def day_1_main(name):
    with open("input_day_1_main.txt", "r", encoding="utf-8") as f:
        # sepparate the groups and numbers by a different character, to make it easier
        raw_numbers = f.read().replace("\n\n",";").replace("\n",",")[:-1]
        # split the groups and sum the numbs
        elfs_totals = [sum(int(j) for j in i.split(",")) for i in raw_numbers.split(";")]
        
        return max(elfs_totals)

def main():
    print(day_1_main(get_file_name("day_1_main")))

main()