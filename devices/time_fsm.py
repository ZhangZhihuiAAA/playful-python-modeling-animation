def accept(rules, favorable_states, start, input):
    state = start
    try:
        for c in input:
            state = rules[(state, c)]
        return state in favorable_states
    except KeyError:
        return False


def rules_range(state_from, state_to, min_char, max_char):
    r = range(ord(min_char), ord(max_char) + 1)
    return {(state_from, chr(u)): state_to for u in r}


# hours
rules = {(1, "2"): 2}
rules.update(rules_range(1, 3, "0", "1"))
rules.update(rules_range(2, 4, "0", "3"))
rules.update(rules_range(3, 4, "0", "9"))

# colon
rules.update({(4, ":"): 5})

# minutes
rules.update(rules_range(5, 6, "0", "5"))
rules.update(rules_range(6, 7, "0", "9"))

# colon
rules.update({(7, ":"): 8})

# seconds
rules.update(rules_range(8, 9, "0", "5"))
rules.update(rules_range(9, 10, "0", "9"))

# dot
rules.update({(10, "."): 11})

# milliseconds
rules.update(rules_range(11, 12, "0", "9"))
rules.update(rules_range(12, 13, "0", "9"))
rules.update(rules_range(13, 14, "0", "9"))

start = 1
favorable_states = {7, 10, 14}

print(accept(rules, favorable_states, start, "23:15"))  # True
print(accept(rules, favorable_states, start, "24:15"))  # False
print(accept(rules, favorable_states, start, "09:37"))  # True
print(accept(rules, favorable_states, start, "23:95"))  # False
print(accept(rules, favorable_states, start, "00:15:23"))  # True
print(accept(rules, favorable_states, start, "05:23:59.234"))  # True