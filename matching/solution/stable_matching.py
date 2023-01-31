import sys
from collections import deque

###### CLEAN INPUT ######
men_pref = {}
women_pref = {}
people = {}

filename = sys.argv[1]
with open(filename, 'r') as f:
    for line in f.readlines():
        line_split = line.split()
        if not line_split:
            continue
        if ":" in line:
                key, *val = line_split
                val = list(map(int, val))
                key = int(key.replace(':', ''))
                if key % 2 == 0:
                    women_pref[key] = dict(zip(val, range(len(val))))
                else:
                    men_pref[key] = val
        if line_split[0].isnumeric():
            people[int(line_split[0])] = line_split[1]


def stable_matching(men_pref, women_pref):
    unmarried_men = deque(men_pref.keys())
    man_fiancée = dict.fromkeys(men_pref.keys(), None)
    woman_current = dict.fromkeys(women_pref.keys(), None)
    next_proposals = dict.fromkeys(men_pref.keys(), 0)

    while unmarried_men:
        man = unmarried_men.pop()
        his_preferences = men_pref[man]
        woman = his_preferences[next_proposals[man]]
        next_proposals[man] += 1
        fiancé = woman_current[woman]

        if fiancé is not None:
            if women_pref[woman][man] < women_pref[woman][fiancé]:
                woman_current[woman], man_fiancée[man] = man, woman
                unmarried_men.append(fiancé)
            else:
                unmarried_men.append(man)
        else:
            woman_current[woman], man_fiancée[man] = man, woman


    return man_fiancée


with open(filename.replace('-in.txt', '-test.out.txt'), 'w') as f:
    pairs = stable_matching(men_pref, women_pref)
    for key, value in pairs.items():
        f.write(f"{people[key]} -- {people[value]}\n")
    f.write("")