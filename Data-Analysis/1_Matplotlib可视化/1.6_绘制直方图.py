# 假如你获取了250部电影的市场（如列表a），希望统计出这些电影时长的分布状态（比如市场为100分钟到120分钟的电影数量，出现的频率等）等信息，你应该如何呈现这些数据？
# 有个问题：如果极差除以组距得到组数为浮点数的话，bins应该取多少才能保证直方图图块和坐标系对齐呢？
# 还有个问题：为什么bins已经取了整数还是实际图表中还是对不齐？
from matplotlib import pyplot as plt
from matplotlib import font_manager
import seaborn as sns


a=[142, 171, 142, 110, 116, 194, 125, 195, 148, 93, 165, 103, 171, 98, 97, 169, 95, 125, 109, 101, 86, 175, 117, 90, 112, 152, 116, 132, 238, 105, 163, 161, 201, 126, 127, 96, 96, 139, 125, 122, 119, 87, 155, 118, 157, 127, 152, 117, 139, 128, 202, 179, 89, 114, 137, 178, 141, 107, 135, 124, 150, 136, 133, 132, 166, 106, 132, 109, 89, 169, 92, 117, 130, 94, 174, 111, 229, 130, 154, 127, 118, 113, 138, 96, 126, 99, 130, 162, 87, 105, 177, 122, 89, 90, 143, 134, 132, 115, 130, 132, 134, 134, 111, 130, 102, 107, 127, 149, 90, 120, 101, 173, 111, 102, 92, 97, 98, 165, 106, 125, 124, 118, 113, 45, 98, 141, 102, 128, 94, 121, 80, 97, 138, 95, 92, 103, 100, 91, 139, 129, 117, 123, 170, 130, 89, 103, 108, 95, 163, 115, 207, 117, 65, 132, 140, 118, 98, 108, 115, 110, 117, 89, 141, 135, 122, 120, 100, 106, 113, 121, 107, 98, 108, 107, 129, 114, 116, 95, 161, 90, 133, 81, 101, 134, 81, 123, 127, 99, 137, 109, 118, 132, 99, 113, 103, 146, 103, 106, 117, 109, 189, 88, 137, 104, 118, 108, 133, 85, 149, 98, 237, 87, 97, 153, 88, 93, 94, 99, 158, 147, 108, 97, 165, 143, 122, 119, 102, 94, 120, 89, 115, 124, 107, 159, 104, 108, 111, 136, 128, 157, 69, 123, 106, 118, 144, 135, 102, 105, 136, 115]
print(max(a))
print(min(a))

# 计算组数
d = 3  #组距
num_bins = (max(a)-min(a))//d
print(num_bins)

plt.figure(figsize=(20,15),dpi=150)

plt.hist(a,color="grey",edgecolor="black",bins=num_bins)
plt.grid(alpha=0.2,linestyle="--")

plt.xticks(range(min(a),max(a)+d,d))
plt.yticks(range(0,20))

plt.show()

