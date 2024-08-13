def accept(rules, favorable_states, start, input):
    state = start
    try:
        for c in input:
            state = rules[(state, c)]
        return state in favorable_states
    except KeyError:
        return False


rules = {
    (3, "C"): 1,
    (1, "C"): 1,
    (1, "A"): 5,
    (5, "A"): 2,
    (2, "B"): 1,
    (2, "C"): 4,
}

favorable_state = {2}
start = 3

print(accept(rules, favorable_state, start, "CAAB"))
print(accept(rules, favorable_state, start, "CAABAA"))