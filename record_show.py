import matplotlib.pyplot as plt
import json

f = open("./record/fitness.txt", "r")
data = json.loads(f.read())
f.close()
plt.plot(data)
plt.show()
