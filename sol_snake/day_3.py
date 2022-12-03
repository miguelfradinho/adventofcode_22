def get_priority(char):
    if "a" <= char <= "z":
        return ord(char) - 96
    elif "A" <= char <= "Z":
        return ord(char) - 38
    else:
        raise ValueError("Wrong char")


def day_3(file_obj):
    rucksacks = [line.strip() for line in file_obj]

    item_types = []
    badges = []

    for bag in rucksacks:
        n_times = len(bag) // 2
        first_half, second_half = set(bag[:n_times]), set(bag[n_times:])
        common = first_half.intersection(second_half)
        item_types.extend(common)

    group_size = 3

    for i in range(0, len(rucksacks), group_size):
        group_bags = [set(r) for r in rucksacks[i : i + group_size]]
        badge_letter = group_bags[0].intersection(*group_bags[1:])
        badges.extend(badge_letter)

    return sum([get_priority(i) for i in item_types]), sum(
        [get_priority(i) for i in badges]
    )
