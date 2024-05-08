from TSP import City, CITY_COUNT
import json
import numpy as np

f = open("./record/map.txt", "r")
map_data = json.loads(f.read())
f.close()
cityList = [City(i[0], i[1]) for i in map_data]


def getCostMatrix(cityList: list[City]):
    costMatrix = np.zeros([CITY_COUNT, CITY_COUNT])
    for i in range(CITY_COUNT):
        for j in range(i + 1, CITY_COUNT):
            distance = cityList[j].distance(cityList[i])
            costMatrix[i][j] = distance
            costMatrix[j][i] = distance
    return costMatrix
print(getCostMatrix(cityList))
