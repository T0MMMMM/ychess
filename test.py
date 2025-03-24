import time
from itertools import permutations

users_file = [4, 5, 1, 6, 7]


def get_elo_by_id(user_id):
    return user_id * 500

def matchmaking():
    sort_by_elo()
    matches = matchmaking_optimal()
    print(matches)



def sort_by_elo():
    for i in range(len(users_file)):
        for j in range(len(users_file)-1):
            if get_elo_by_id(users_file[i]) < get_elo_by_id(users_file[j]):
                users_file[i], users_file[j] = users_file[j], users_file[i]


def matchmaking_optimal():
    if len(users_file) < 2:
        return None  

    best_match = None
    min_total_gap: float = float('inf')

    for perm in permutations(users_file):
        total_gap = calcul_total_gap(perm)

        if total_gap < min_total_gap:
            min_total_gap = total_gap
            best_match = [(perm[i], perm[i+1]) for i in range(0, len(perm) - 1, 2)]

    return best_match


def calcul_total_gap(perm):
    total_gap = 0
    for i in range(0, len(perm) - 1, 2):
        joueur1, joueur2 = perm[i], perm[i + 1]
        gap = abs(get_elo_by_id(joueur1) - get_elo_by_id(joueur2))  # Différence de niveau entre les deux joueurs
        total_gap += gap  # On additionne cet écart au total
    return total_gap


while True:
    print(users_file)
    time.sleep(5)  # Vérifier toutes les 5 secondes
    matchmaking()
