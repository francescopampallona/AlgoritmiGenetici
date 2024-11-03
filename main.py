import copy
import random
from itertools import combinations
from operator import itemgetter

'''
Esempio di posizioni
queen_positions = [[False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False],
                   [False, False, False, True, False, False, False, False],
                   [True,  False, False, False, True, False, False, False],
                   [False, True, False, False, False, True, False, True],
                   [False, False, True, False, False, False, True, False],
                   [False, False, False, False, False, False, False, False]]
print(count_attacking_pairs(queen_positions))
'''
def initialize_random_queen_positions():
    # Crea una matrice 8x8 di False
    queen_positions = [[False for _ in range(8)] for _ in range(8)]


    # Metto una regina per riga ma in colonne scelte casualmente
    for row in range(8):
        colonna_casuale=random.randrange(8)
        queen_positions[row][colonna_casuale] = True

    return queen_positions

def count_attacking_pairs(queen_matrix):
    # Extract positions of queens
    positions = [(i, j) for i in range(8) for j in range(8) if queen_matrix[i][j]]

    attacking_pairs = 0

    # Check all pairs of queens to see if they attack each other
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            row1, col1 = positions[i]
            row2, col2 = positions[j]

            # Check if they're in the same row, column, or diagonal
            if row1 == row2 or col1 == col2 or abs(row1 - row2) == abs(col1 - col2):
                attacking_pairs += 1

    return attacking_pairs

def inizializza(dimensione):
    popolazione = []
    for i in range(dimensione):
        membro={
            'voto': 1000,
            'genoma': initialize_random_queen_positions()
        }
        popolazione.append(membro)
    return popolazione

def fitness(popolazione):
    for individuo in popolazione:
        individuo['voto']=count_attacking_pairs(individuo['genoma'])
    return popolazione

def selezione(popolazione):
    popolazione_ordinata = sorted(popolazione, key=itemgetter('voto'), reverse=False)
    return popolazione_ordinata[:4]

def crossover(popolazione):
    nuova_generazione=[]
    for papa, mamma in combinations(popolazione, 2):
        random_number = random.randrange(8)
        figlio1 = {
            'genoma': papa['genoma'][:random_number] + mamma['genoma'][random_number:],
            'voto': 1000
        }
        figlio2 = {
            'genoma': mamma['genoma'][:random_number] + papa['genoma'][random_number:],
            'voto': 1000
        }
        nuova_generazione.append(figlio1)
        nuova_generazione.append(figlio2)
    return nuova_generazione


def mutazione(popolazione):
    for individuo in popolazione:
        riga_casuale = random.randrange(8)
        posizioni_true = []
        posizioni_false = []

        # Trova le posizioni dei True e dei False nella riga casuale
        for j in range(8):
            if individuo['genoma'][riga_casuale][j]:
                posizioni_true.append(j)
            else:
                posizioni_false.append(j)

        # Esegue una mutazione solo se ci sono sia True che False
        if posizioni_true and posizioni_false:
            # Toglie un True a caso
            true_sel = random.choice(posizioni_true)
            individuo['genoma'][riga_casuale][true_sel] = False

            # Mette un True in una posizione False a caso
            false_sel = random.choice(posizioni_false)
            individuo['genoma'][riga_casuale][false_sel] = True

    return popolazione


def trova_conflitti(genoma):
    n = len(genoma)
    colonna = [0] * n
    principale = [0] * (2 * n)
    secondaria = [0] * (2 * n)
    conflitti = []

    for i in range(n):
        for j in range(n):
            if genoma[i][j]:
                colonna[j] += 1
                principale[i + j] += 1
                secondaria[i - j + n] += 1

    for i in range(n):
        for j in range(n):
            if genoma[i][j] and (colonna[j] > 1 or principale[i + j] > 1 or secondaria[i - j + n] > 1):
                conflitti.append((i, j))

    return conflitti


def mutazione_intelligente(popolazione):
    for individuo in popolazione:
        conflitti = trova_conflitti(individuo['genoma'])
        if conflitti:
            i, j = random.choice(conflitti)  # Scegli una regina in conflitto a caso
            # Trova una nuova posizione per la regina
            for nuova_col in range(8):
                if all(not row[nuova_col] for row in individuo['genoma']):
                    individuo['genoma'][i][j] = False
                    individuo['genoma'][i][nuova_col] = True
                    break  # Interrompe dopo aver trovato la prima colonna valida
    return popolazione


def evoluzione():
    popolazione=inizializza(8)
    migliore=popolazione[0]
    generazione=0
    while(count_attacking_pairs(migliore['genoma'])>0):
        popolazione = fitness(popolazione)
        popolazione = selezione(popolazione)
        if (popolazione[0]['voto'] < migliore['voto']):
            migliore = copy.deepcopy(popolazione[0])
        popolazione = crossover(popolazione)
        popolazione = mutazione(popolazione)
        popolazione = mutazione_intelligente(popolazione)
        generazione=generazione+1
        print(f"Generazione {generazione:3d} -  Voto migliore: {migliore['voto']:2d}")
    print(f"Il miglior genoma è {migliore['genoma']}")
    print(f"Voto: {count_attacking_pairs(migliore['genoma'])}")

evoluzione()