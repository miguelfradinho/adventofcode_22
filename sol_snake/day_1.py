def day_1(file_obj):
    with file_obj as f:
        # sepparate the groups and numbers by a different character, to make it easier
        raw_numbers = f.read().replace("\n\n", ";").replace("\n", ",")[:-1]
        # split the groups and sum the numbs
        elfs_totals = [
            sum(int(j) for j in i.split(",")) for i in raw_numbers.split(";")
        ]

        elfs_totals.sort(reverse=True)

        return elfs_totals[0], sum(elfs_totals[:3])
