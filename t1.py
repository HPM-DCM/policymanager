import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

labels = ['China', 'Swiss', 'USA', 'UK', 'Laos', 'Spain']
X = [222, 42, 455, 664, 454, 334]
fig = plt.figure()
plt.pie(X, labels=labels, autopct='%1.2f%%')  # 画饼图（数据，数据对应的标签，百分数保留两位小数点）
plt.title("Pie chart")
plt.savefig("PieChart.jpg")
plt.show()