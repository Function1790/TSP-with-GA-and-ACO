from GA import SIZEOF_MAP_X, SIZEOF_MAP_Y, CITY_COUNT
import matplotlib.pyplot as plt
import random as r

cityList = []
for i in range(CITY_COUNT):
    cityList.append([r.randint(0, SIZEOF_MAP_X), r.randint(0, SIZEOF_MAP_Y)])
    plt.plot(cityList[i][0], cityList[i][1], "ro")

print(cityList)
plt.show()
