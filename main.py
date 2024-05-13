from GA import *
import matplotlib.pyplot as plt
import json


def displayResult(route):
    ax.clear()
    lines_x = []
    lines_y = []
    for i in route:
        ax.plot(i.x, i.y, "bo", zorder=5)
        lines_x.append(i.x)
        lines_y.append(i.y)
    lines_x.append(route[0].x)
    lines_y.append(route[0].y)
    ax.plot(lines_x, lines_y, "r")
    plt.show()


f = open("./record/map.txt", "r")
map_data = json.loads(f.read())
f.close()
cityList = [City(i[0], i[1]) for i in map_data]
# cityList = []
# for i in range(CITY_COUNT):
#    cityList.append(City(r.randint(0, SIZEOF_MAP_X), r.randint(0, SIZEOF_MAP_Y)))

chromosome = createChromosome(cityList)

fig, ax = plt.subplots()
plt.ion()
plt.xlim(0, SIZEOF_MAP_X)
plt.ylim(0, SIZEOF_MAP_Y)
record_fitness = []
for i in range(50):
    measureGeneFitness(chromosome)
    top_gene = rankGenes(chromosome)[0]
    route = top_gene.route
    record_fitness.append(top_gene.fitness.value)
    print(i + 1, top_gene.fitness.value)

    displayResult(route)
    plt.pause(0.00001)

    chromosome = Generate(chromosome)

f = open("./record/fitness.txt", "w")
f.writelines(str(record_fitness))
f.close()
displayResult(route)
plt.pause(10)
