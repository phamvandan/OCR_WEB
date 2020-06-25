import numpy as np

y1_no_table = np.load('data/no_table/y1.npy')
y2_no_table = np.load('data/no_table/y2.npy')
y1_table = np.load('data/table/y1.npy')
y2_table = np.load('data/table/y2.npy')
y1_np = np.concatenate([y1_no_table, y2_no_table])
y2_np = np.concatenate([y1_table, y2_table])

y1_mean = round(np.mean(y1_np), 2)
y2_mean = round(np.mean(y2_np),2)
y1_error = round(np.std(y1_np, ddof=1),2)
y2_error = round(np.std(y2_np, ddof=1),2)

with open('data/result.txt','w+') as fw:
	fw.write(str(y1_mean)+'\t'+str(y1_error) + '\t'+str(y2_mean)+'\t'+str(y2_error))