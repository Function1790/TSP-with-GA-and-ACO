from GA import City, CITY_COUNT
import json
import numpy as np
import random as r

f = open("./record/map.txt", "r")
map_data = json.loads(f.read())
f.close()
cityList = [City(i[0], i[1]) for i in map_data]
cityListIndex = [i for i in range(len(map_data))]

INFLUENCE_ALPHA = 1  # 페로몬 영향
INFLUENCE_BETA = 1  # 거리 영향
INIT_PHEROMONE = 0.5  # 초기 페로몬
VOLATILIZATION_FACTOR = 0.05  # 휘발 계수
VALUE_OF_Q0 = 0.5


class Ant:
    def __init__(self, route):
        self.route = route  # 경로
        self.distance = 0  # 거리
        self.pheromone = 0  # 페로몬 값 = 1 / 거리

    def measureDistance(self, cityList):
        if self.distance != 0:  # 거리가 측정되었다면
            return self.distance

        totalDistance = 0
        for i in range(len(self.route)):
            fromCityIndex = self.route[i]
            if i + 1 < len(self.route):
                toCityIndex = self.route[i + 1]
            else:
                toCityIndex = self.route[0]
            totalDistance += cityList[fromCityIndex].distance(cityList[toCityIndex])
        self.distance = totalDistance
        return self.distance

    def measurePheromone(self, cityList):
        if self.pheromone == 0:
            self.pheromone = 1 / self.measureDistance(cityList)
        return self.pheromone

    def addPheromoneTo(self, matrix, cityList):
        if self.pheromone == 0:
            self.measurePheromone(cityList)
        for i in self.route:
            fromCityIndex = self.route[i]
            if i + 1 < len(self.route):
                toCityIndex = self.route[i + 1]
            else:
                toCityIndex = self.route[0]
            matrix[fromCityIndex][toCityIndex] *= VOLATILIZATION_FACTOR
            matrix[toCityIndex][fromCityIndex] *= VOLATILIZATION_FACTOR
            matrix[fromCityIndex][toCityIndex] += (
                1 - VOLATILIZATION_FACTOR
            ) * self.pheromone
            matrix[toCityIndex][fromCityIndex] += (
                1 - VOLATILIZATION_FACTOR
            ) * self.pheromone
        return matrix


def getCostMatrix(cityList: list[City]):
    costMatrix = np.zeros([CITY_COUNT, CITY_COUNT])
    for i in range(CITY_COUNT):
        for j in range(i + 1, CITY_COUNT):
            distance = cityList[j].distance(cityList[i])
            costMatrix[i][j] = distance
            costMatrix[j][i] = distance
    return costMatrix


def getPheromonMatrix(antList: list[Ant]):
    pheromonMatrix = np.ones([CITY_COUNT, CITY_COUNT]) * INIT_PHEROMONE
    for i in antList:
        pheromonMatrix = i.addPheromoneTo(pheromonMatrix, cityList)
    return pheromonMatrix


def updatePheromonMatrix(pheromonMatrix, ant: Ant):
    pheromonMatrix = ant.addPheromoneTo(pheromonMatrix, cityList)


def getProbability(pheromone, distance):
    return (pheromone**INFLUENCE_ALPHA) * ((1 / distance) ** INFLUENCE_BETA)


def getProbabilityIndex(probabilities) -> int:
    """누적합을 이용한 확률 선발"""
    prefixSum = 0
    randValue = r.random()
    # print(np.round(np.array(probabilities)*100))
    for i in range(len(probabilities)):
        # ex) probabilities = [0.2, 0.3, 0.4, 0.1], randValue= 0.76
        # i=0 -> (0, 0.2) | i=1 -> (0.2, 0.5) | i=3 -> *(0.5, 0.9)*
        # return 3
        prefixSum += probabilities[i]
        if randValue < prefixSum:
            return i


def selectNextIndex(currentIndex, routeSample, pheromoneMatrix, costMatrix):
    probabilities = []
    totalProbability = 0
    for i in routeSample:
        _pheromone = pheromoneMatrix[currentIndex][i]
        _distance = costMatrix[currentIndex][i]
        probability = getProbability(_pheromone, _distance)
        probabilities.append(probability)
        totalProbability += probability

    # 조건부 확률로 업데이트
    if len(probabilities) == 1:
        return 0
    probabilities = [i / totalProbability for i in probabilities]

    chanceOfQ0 = r.random()
    if chanceOfQ0 < VALUE_OF_Q0:
        maxProbability = max(probabilities)
        maxIndex = -1
        for i in range(len(probabilities)):
            if maxProbability == probabilities[i]:
                maxIndex = i
                break
        return maxIndex
    # routeSample의 조건부 확률에 따른 index 추출
    return getProbabilityIndex(probabilities)


def createRoadByACO(costMatrix, pheromoneMatrix):
    routeSample = cityListIndex.copy()
    resultRoute = []
    resultRoute.append(routeSample.pop(r.randint(0, len(routeSample) - 1)))
    for i in range(len(routeSample)):
        _index = selectNextIndex(
            resultRoute[i], routeSample, pheromoneMatrix, costMatrix
        )
        resultRoute.append(routeSample.pop(_index))
    return resultRoute
