from ACO import *
from GA import SIZEOF_MAP_X, SIZEOF_MAP_Y
import matplotlib.pyplot as plt
import operator


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


def rankRoute(routeList):
    """거리가 가장 짧은 순으로 경로 배열"""
    routesResults = {}
    for i in range(len(routeList)):
        routesResults[i] = routeList[i][1]
    sorted_index = sorted(
        routesResults.items(), key=operator.itemgetter(1), reverse=False
    )
    return [routeList[i[0]] for i in sorted_index]


fig, ax = plt.subplots()
plt.ion()
plt.xlim(0, SIZEOF_MAP_X)
plt.ylim(0, SIZEOF_MAP_Y)

# antList = [Ant(r.sample(cityListIndex, len(cityListIndex))) for i in range(100)]
antList: list[Ant] = []
record_ant = []
costMatrix = getCostMatrix(cityList)
pheromoneMatrix = np.ones([CITY_COUNT, CITY_COUNT]) * INIT_PHEROMONE
for i in range(500000):
    antList.append(Ant(r.sample(cityListIndex, len(cityListIndex))))
    updatePheromonMatrix(pheromoneMatrix, antList[i])
    print(i)
    route = createRoadByACO(costMatrix, pheromoneMatrix)
    record_ant.append([route, antList[i].distance])
    ranked = rankRoute(record_ant)

    displayResult(ranked[0][0])
    plt.pause(0.01)
