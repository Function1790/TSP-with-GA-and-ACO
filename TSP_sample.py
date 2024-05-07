import numpy as np
import math as m
import random as r
import operator


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


class Fitness:
    def __init__(self, route: list[City]):
        self.route = route
        self.distance = 0
        self.fitness = 0

    def routeDistance(self):
        """distance 계산"""
        if self.distance != 0:
            return
        pathDistance = 0
        for i in range(len(self.route)):
            fromCity = self.route[i]
            if i + 1 < len(self.route):
                toCity = self.route[i + 1]
            else:
                toCity = self.route[0]  # 마지막은 첫번째 경로와의 거리로 계산
            pathDistance += fromCity.distance(toCity)
        self.distance = pathDistance
        return self.distance

    def routeFitness(self):
        """fitness 계산"""
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness


def createRoute(cityList):
    """경로 무작위 배열"""
    route = r.sample(cityList, len(cityList))
    return route


def initialPopulation(popSize, cityList):
    population = [createRoute(cityList) for i in range(popSize)]
    return population


def rankRoutes(population):
    '''적합도가 가장 높은 순으로 경로 배열'''
    fitnessResults = {}
    for i in range(len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)

