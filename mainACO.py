from ACO import *
from GA import SIZEOF_MAP_X, SIZEOF_MAP_Y
import matplotlib.pyplot as plt
import operator
import time


def displayResult(route):
    ax.clear()
    lines_x = []
    lines_y = []
    for i in route:
        ax.plot(cityList[i].x, cityList[i].y, "bo", zorder=5)
        lines_x.append(cityList[i].x)
        lines_y.append(cityList[i].y)
    lines_x.append(cityList[0].x)
    lines_y.append(cityList[0].y)
    ax.plot(lines_x, lines_y, "r")
    plt.show()


def rankRoute124124(routeList):
    """거리가 가장 짧은 순으로 경로 배열"""
    routesResults = {}
    for i in range(len(routeList)):
        routesResults[i] = routeList[i].distance
    sorted_index = sorted(
        routesResults.items(), key=operator.itemgetter(1), reverse=False
    )
    return [routeList[i[0]] for i in sorted_index]


def rankRoute(routeList):
    """거리가 가장 짧은 순으로 경로 배열"""
    routesResults = {}
    for i in range(len(routeList)):
        routesResults[i] = routeList[i].route
    sorted_index = sorted(
        routesResults.items(), key=operator.itemgetter(1), reverse=False
    )
    return [[routeList[i[0]].route, routeList[i[0]].distance] for i in sorted_index]


def getDistance(route):
    distance = 0
    for i in range(len(route) - 1):
        distance += cityList[i].distance(cityList[i + 1])
    distance += cityList[i + 1].distance(cityList[0])
    return distance


fig, ax = plt.subplots()
plt.ion()
plt.xlim(0, SIZEOF_MAP_X)
plt.ylim(0, SIZEOF_MAP_Y)

# antList = [Ant(r.sample(cityListIndex, len(cityListIndex))) for i in range(100)]
antList: list[Ant] = []
record_ant = []
costMatrix = getCostMatrix(cityList)
pheromoneMatrix = np.ones([CITY_COUNT, CITY_COUNT]) * INIT_PHEROMONE
superFast = [[], 0]
record_fitness = []
record_time = []
start = time.time()
for i in range(300):
    print(i)
    # antList.append(Ant(r.sample(cityListIndex, len(cityListIndex))))
    # antList = [Ant(r.sample(cityListIndex, len(cityListIndex))) for i in range(100)]
    antList = [Ant(createRoadByACO(costMatrix, pheromoneMatrix)) for i in range(100)]
    for j in antList:
        updatePheromonMatrix(pheromoneMatrix, j)
    # print(i)
    # route = createRoadByACO(costMatrix, pheromoneMatrix)
    # record_ant.append([route, antList[i].distance])
    ranked = rankRoute(antList)
    fastest = ranked[0][0]
    fitness = 1 / ranked[0][1]
    if superFast[1] < fitness:
        superFast[0] = fastest
        superFast[1] = fitness
    for j in range(len(fastest)):
        a = fastest[j]
        if j + 1 < len(fastest):
            b = fastest[j + 1]
        else:
            b = fastest[0]
        pheromoneMatrix[a][b] += fitness * 50
        pheromoneMatrix[b][a] += fitness * 50
    displayResult(superFast[0])
    record_time.append(time.time() - start)
    record_fitness.append(superFast[1])
    plt.pause(0.01)
f = open("./record/fitnessACO.txt", "w")
f.writelines(str(record_fitness))
f.close()
f = open("./record/timeACO.txt", "w")
f.writelines(str(record_time))
f.close()