import numpy as np
import math as m
import random as r
import operator
import matplotlib.pyplot as plt

# Setting
SIZEOF_MAP_X = 800
SIZEOF_MAP_Y = 800

CITY_COUNT = 200  # 도시 갯수 & 유전자 갯수
CHROMOSOME_SIZE = 700  # 염색체 크기
GENERATION_COUNT = 2000
SELECT_GENE_COUNT = 20
MUTATION_RATE = 0.02

# Class
class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def toArray(self) -> np.array:
        return np.array([self.x, self.y])

    def distance(self, city):
        return m.sqrt((self.x - city.x) ** 2 + (self.y - city.y) ** 2)

    def __str__(self) -> str:
        return f"City({self.x}, {self.y})"

class Fitness:
    def __init__(self, route: list[City]):
        self.route = route
        self.distance = 0
        self.value = 0

    def measureDistance(self):
        if self.distance != 0:  # 이미 측정되어있다면
            return self.distance
        pathDistance = 0
        for i in range(len(self.route)):
            fromCity = self.route[i]
            if i + 1 < len(self.route):
                toCity = self.route[i + 1]
            else:
                toCity = self.route[0]  # 마지막 도시 -> 시작 도시
            pathDistance += fromCity.distance(toCity)
        self.distance = pathDistance
        return self.distance

    def measureFitness(self):
        if self.value == 0:
            self.value = 1 / self.measureDistance()
        return self.value


class Gene:
    def __init__(self, cityList, isMix=True):
        if isMix:
            self.route = r.sample(cityList, len(cityList))  # 경로 무작위 배열
        else:
            self.route = cityList
        self.fitness = Fitness(self.route)


# Function
def getRandArray(a, b, length) -> np.array:
    """a ~ b중 length개의 정수 랜덤 반환"""
    return np.floor(np.random.rand(length) * (b - a + 1) + a)


def createChromosome(cityList) -> list[Gene]:
    return [Gene(cityList) for i in range(CHROMOSOME_SIZE)]


def measureGeneFitness(chromosome: list[Gene]):
    """적합도가 높은것 부터 순서대로 정렬  /  [ (index, fitness), ... ]"""
    for gene in chromosome:
        gene.fitness.measureFitness()


def displayRoute(route: list[City]):
    lines_x = []
    lines_y = []
    for i in route:
        plt.plot(i.x, i.y, "bo", zorder=5)
        lines_x.append(i.x)
        lines_y.append(i.y)
    plt.plot(lines_x, lines_y, "r")
    plt.xlim(0, SIZEOF_MAP_X)
    plt.ylim(0, SIZEOF_MAP_Y)
    plt.show()


def rankGenes(chromosome: list[Gene]):
    """적합도가 가장 높은 순으로 경로 배열"""
    fitnessResults = {}
    for i in range(len(chromosome)):
        fitnessResults[i] = chromosome[i].fitness.value
    sorted_index = sorted(
        fitnessResults.items(), key=operator.itemgetter(1), reverse=True
    )
    return [chromosome[i[0]] for i in sorted_index]


def breed(parent1, parent2):
    """두 유전자로 새로운 경로 생산"""
    child1 = []
    child2 = []

    geneA = int(r.random() * CITY_COUNT)
    geneB = int(r.random() * CITY_COUNT)

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    child1 = [parent1[i] for i in range(startGene, endGene)]
    child2 = [i for i in parent2 if i not in child1]

    return child1 + child2


def mutate(gene: Gene, mutationRate):
    indiviual = gene.route
    for swapped in range(len(indiviual)):
        if r.random() < mutationRate:
            swapWith = int(r.random() * len(indiviual))
            temp = indiviual[swapped]
            indiviual[swapped] = indiviual[swapWith]
            indiviual[swapWith] = temp
    return indiviual


def Crossover(ranked_genes: list[Gene]):
    selected_genes = ranked_genes[:SELECT_GENE_COUNT]
    result = []
    for i in range(CHROMOSOME_SIZE):
        gene1 = r.choice(selected_genes)
        gene2 = r.choice(selected_genes)
        result.append(Gene(breed(gene1.route, gene2.route), False))
    return result

def MutateChromosome(chromosome, mutationRate):
    result = []
    for i in range(len(chromosome)):
        mutatedGene = mutate(chromosome[i], mutationRate)
        result.append(Gene(mutatedGene, False))
    return result

def Generate(chromosome):
    ranked_genes = rankGenes(chromosome)
    crossovered_genes = Crossover(ranked_genes)
    mutated_genes = MutateChromosome(crossovered_genes, MUTATION_RATE)
    return mutated_genes
