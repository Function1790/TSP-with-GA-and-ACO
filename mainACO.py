from ACO import *
from TSP import SIZEOF_MAP_X, SIZEOF_MAP_Y
import matplotlib.pyplot as plt


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


fig, ax = plt.subplots()
plt.ion()
plt.xlim(0, SIZEOF_MAP_X)
plt.ylim(0, SIZEOF_MAP_Y)

#antList = [Ant(r.sample(cityListIndex, len(cityListIndex))) for i in range(100)]
antList = []
costMatrix = getCostMatrix(cityList)
pheromoneMatrix = np.ones([CITY_COUNT, CITY_COUNT]) * INIT_PHEROMONE
for i in range(500000):
    antList.append(Ant(r.sample(cityListIndex, len(cityListIndex))))
    updatePheromonMatrix(pheromoneMatrix, antList[i])
    print(i)
    route = createRoadByACO(costMatrix, pheromoneMatrix)
    displayResult(route)
    plt.pause(0.01)
