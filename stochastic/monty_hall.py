from random import choice


N = 100000

player_a_win = 0  # Palyer A sticks to the original choice.
player_b_win = 0  # Palyer B switches the door.


def monty_choice(prize, options):
    if prize[options[0]] == False and prize[options[1]] == False:
        return choice(options)

    return options[0] if prize[options[1]] == True else options[1]


for _ in range(N):
    prize = [False, False, False]
    prize[choice([0, 1, 2])] = True

    options = [0, 1, 2]
    player_choice = choice(options)
    options.remove(player_choice)
    options.remove(monty_choice(prize, options))

    if prize[player_choice]:
        player_a_win += 1
    if prize[options[0]]:
        player_b_win += 1


print(f"Player A: {player_a_win / N}")
print(f"Player B: {player_b_win / N}")