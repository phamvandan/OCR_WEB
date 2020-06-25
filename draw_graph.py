import matplotlib.pyplot as plt
import numpy as np

x =[]
y1 = []
y2 = []
with open('data/no_table/result.txt', 'r') as f_read:
    # x.append(f_read.read('%d'))
    # y1.append(f_read.read('%f'))
    # y2.append(f_read.read('%f'))
    for line in f_read:
        x_cur = int(line.split()[0])
        y1_cur = float(line.split()[1])
        y2_cur = float(line.split()[2])
        x.append(x_cur)
        y1.append(y1_cur)
        y2.append(y2_cur)
# plt.subplots_adjust(right=0.7)
# plt.tight_layout(rect=[0,0,0.75,1])
plt.plot(x, y1, label='eDMS', color='red')
plt.plot(x, y2, label='Tesseract 4.0', color='blue')
y1_std = np.std(y1, ddof=1)
y2_std = np.std(y2, ddof=1)
print(y1_std,y2_std)
# y1_mean_np = [np.mean(y1) for i in range(0,len(y1)) ]
# y2_mean_np = [np.mean(y2) for i in range(0,len(y1)) ]
# plt.plot(x, y1_mean_np, label='eDMS mean', color='orange', linestyle='--')
# plt.plot(x, y2_mean_np, label='Tesseract mean', color='green', linestyle='--')
plt.plot()
plt.ylabel('Word Error Rate')
plt.xlabel('Skew Angle')
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
# plt.legend(bbox_to_anchor=(1.04,1), loc='upper left')
plt.legend()
plt.show()
plt.savefig('data/no_table/no_table.png',bbox_inches="tight")