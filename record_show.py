import matplotlib.pyplot as plt
import json

f = open("./record/fitness.txt", "r")
data = json.loads(f.read())
f.close()
f = open("./record/time.txt", "r")
data2 = json.loads(f.read())
f.close()
# 시간-적합도
plt.title("fitness-time")
plt.xlabel("time")
plt.ylabel("fitness")
plt.plot(data2, data, "b")
plt.show()

# 세대-적합도
plt.title("fitness-gen")
plt.xlabel("gen")
plt.ylabel("fitness")
plt.plot(data, "r")
plt.show()

# 시간-적합도
plt.title("time-gen")
plt.xlabel("gen")
plt.ylabel("time")
plt.plot(data2, "g")
plt.show()
