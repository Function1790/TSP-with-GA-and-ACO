import matplotlib.pyplot as plt
import json
f=open("record.txt","r")
data=json.loads(f.read())
plt.plot(data)
plt.show()
