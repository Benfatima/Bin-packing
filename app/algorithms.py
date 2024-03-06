import random
import numpy as np

def initialiser_loups(nombre_loups, dimension, capacite_maximale):
    return np.random.randint(0, capacite_maximale + 1, (nombre_loups, dimension))


def fitness_loup(loup, objets, capacite_bin):
    bins = [[] for _ in range(len(loup))]

    for objet_taille in objets:
        index_min_bin = np.argmin(loup)

        # Comparer la taille de l'objet avec la capacité restante du bin
        if objet_taille <= loup[index_min_bin]:
            bins[index_min_bin].append(objet_taille)
            loup[index_min_bin] -= objet_taille
        else:
            # Gérer le cas où la capacité restante du bin n'est pas suffisante
            # (peut être adapté selon les exigences du problème)
            index_min_bin = np.argmin([sum(bin) for bin in bins])
            bins[index_min_bin].append(objet_taille)
            loup[index_min_bin] += objet_taille

    surcapacite_totale = sum(max(0, sum(bin) - capacite_bin) for bin in bins)

    # Ajouter la liste des bacs avec leurs contenus à la valeur de fitness
    return surcapacite_totale, bins


def mise_a_jour_position(loup_alpha, loup_beta, loup_delta, a, A, C ,capacite_maximale):
    D_alpha = abs(C * loup_alpha - loup_alpha)
    D_beta = abs(C * loup_beta - loup_beta)
    D_delta = abs(C * loup_delta - loup_delta)

    nouvelle_position = (loup_alpha - a * D_alpha +
                         loup_beta - a * D_beta +
                         loup_delta - a * D_delta) / 3.0

    # Normaliser les valeurs pour rester dans l'intervalle des capacités
    nouvelle_position = np.clip(nouvelle_position, 0, capacite_maximale)

    return nouvelle_position

def algorithme_loups(objets, capacite_bin, nombre_loups, nombre_iterations):
    dimension = len(objets)
    loups = initialiser_loups(nombre_loups, dimension,capacite_bin)

    for iteration in range(nombre_iterations):
        for i in range(nombre_loups):
            fitness = fitness_loup(loups[i], objets, capacite_bin)
            alpha, beta, delta = sorted(range(len(loups)), key=lambda x: fitness_loup(loups[x], objets, capacite_bin))[:3]

            a = 2.0 - iteration * (2.0 / nombre_iterations)  # Mise à jour du coefficient d'atténuation

            nouvelle_position = mise_a_jour_position(loups[alpha], loups[beta], loups[delta], a, np.random.rand(dimension), np.random.rand(dimension),capacite_bin)
            loups[i] = nouvelle_position

        meilleur_loup = min(loups, key=lambda x: fitness_loup(x, objets, capacite_bin))
        meilleur_fitness = fitness_loup(meilleur_loup, objets, capacite_bin)

    return meilleur_loup, meilleur_fitness

def best_fit_heuristic(objets, capacite_bin):
    # Tri des objets par ordre décroissant de taille
    objets_tries = sorted(objets, reverse=True)

    # Initialisation des bins avec le premier objet
    bins = [[objets_tries[0]]]

    # Placement des objets restants
    for objet in objets_tries[1:]:
        bin_trouve = False

        # Parcours des bins existants pour trouver le meilleur fit
        for bin in bins:
            if sum(bin) + objet <= capacite_bin:
                bin.append(objet)
                bin_trouve = True
                break

        # Création d'un nouveau bin si aucun fit n'est trouvé
        if not bin_trouve:
            bins.append([objet])

    return bins
def initialiser_population(taille_population, objets, capacite_bin):
    population = []

    for _ in range(taille_population):
        individu = best_fit_heuristic(objets, capacite_bin)
        population.append(individu)

    return population


def fitness(individu, capacite_bin):
    nombre_boites_utilisees = len([bac for bac in individu if bac])  # Nombre de bacs non vides
    return 1 / (1 + nombre_boites_utilisees)

def selection_par_roulette(population, fitness_values):
    probabilites = np.array(fitness_values) / sum(fitness_values)
    indice_selectionne = np.random.choice(range(len(population)), p=probabilites)
    return population[indice_selectionne]


def croisement(parent1, parent2):
    point_crossover = random.randint(1, len(parent1) - 1)
    enfant = parent1[:point_crossover] + [objet for objet in parent2 if objet not in parent1[:point_crossover]]
    return enfant


def mutation(individu, taux_mutation):
    for i in range(len(individu)):
        if random.random() < taux_mutation:
            j = random.randint(0, len(individu) - 1)
            individu[i], individu[j] = individu[j], individu[i]
    return individu


def algorithme_genetique(objets, capacite_bin, taille_population, taux_mutation, nombre_generations):
    population = initialiser_population(taille_population, objets, capacite_bin)

    for generation in range(nombre_generations):
        fitness_values = [fitness(individu, capacite_bin) for individu in population]

        nouvelle_population = []
        for _ in range(taille_population // 2):
            parent1 = selection_par_roulette(population, fitness_values)
            parent2 = selection_par_roulette(population, fitness_values)

            enfant1 = croisement(parent1, parent2)
            enfant2 = croisement(parent2, parent1)

            enfant1 = mutation(enfant1, taux_mutation)
            enfant2 = mutation(enfant2, taux_mutation)

            nouvelle_population.extend([enfant1, enfant2])

        population = nouvelle_population

    meilleure_solution = max(population, key=lambda individu: fitness(individu, capacite_bin))
    nombre_boites_utilisees = 1 / fitness(meilleure_solution, capacite_bin) - 1

    return meilleure_solution, nombre_boites_utilisees


