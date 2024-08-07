from random import randint


N = 120000


def turn_score(target):
    score = 0
    while score < target:
        die = randint(1, 6)
        if die == 1:
            return 0
        score += die
    return score


highest_total_score = 0
best_avg_score = 0

for target in range(2, 101):
    n_score = 0
    for _ in range(N):
        n_score += turn_score(target)
    avg_score = round(n_score / N, 1)
    
    if avg_score > best_avg_score:
        highest_total_score, best_avg_score = target, avg_score

print(f"best target: {highest_total_score}, best total (avg): {best_avg_score}")