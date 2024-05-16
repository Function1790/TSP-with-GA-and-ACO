import matplotlib.pyplot as plt
import json

#GA
f = open("./record/fitness.txt", "r")
data = json.loads(f.read())
f.close()
f = open("./record/time.txt", "r")
data2 = json.loads(f.read())
f.close()

#ACO
f = open("./record/fitnessACO.txt", "r")
dataACO = json.loads(f.read())
f.close()
f = open("./record/timeACO.txt", "r")
data2ACO = json.loads(f.read())
f.close()

# 시간-적합도
plt.title("fitness-time")
plt.xlabel("time")
plt.ylabel("fitness")
plt.plot(data2, data, "b", label="GA") # GA
plt.plot(data2ACO, dataACO, "r", label="ACO") # ACO
plt.legend()
plt.show()

# 세대-적합도
plt.title("fitness-gen")
plt.xlabel("gen")
plt.ylabel("fitness")
plt.plot(data, "b", label="GA") # GA
plt.plot(dataACO, "r", label="ACO") # ACO
plt.legend()
plt.show()

# 시간-적합도
plt.title("time-gen")
plt.xlabel("gen")
plt.ylabel("time")
plt.plot(data2, "b", label="GA") # GA
plt.plot(data2ACO, "r", label="ACO") # ACO
plt.legend()
plt.show()
