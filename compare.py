import os
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
import numpy as np

# corrected_path = 'data/no_table/corrected_regex/'
# our_method_path = 'data/no_table/our_method/'
# tesseract_path = 'data/no_table/tesseract/'
corrected_path = 'data/table/corrected_regex/'
our_method_path = 'data/table/our_method/'
tesseract_path = 'data/table/tesseract/'
with open('data/table/result.txt','w+') as f:
    files = os.listdir(corrected_path)
    print(files)
    x = []
    y1 = []
    y2 = []
    i = 1
    for file in files:
        path_to_correct = os.path.join(corrected_path, file)
        print(path_to_correct)
        path_to_our_method = os.path.join(our_method_path, file)
        path_to_tesseract = os.path.join(tesseract_path, file)
        with open(path_to_correct,'r') as fread:
            correct = fread.read()
        with open(path_to_our_method, 'r') as fread:
            our_method = fread.read()
        with open(path_to_tesseract,'r') as fread:
            tesseract = fread.read()
        s1 = SequenceMatcher(lambda x: x == " ", our_method, correct)
        s2 = SequenceMatcher(lambda x: x == " ", tesseract, correct)
        y1.append(round(s1.ratio(), 2))
        y2.append(round(s2.ratio(), 2))
        x.append(i)
        f.write(file+'\t'+str(i)+'\t'+str(y1[-1])+'\t'+str(y2[-1])+'\n')
        i = i + 1
    y1_np = np.asarray(y1)
    y2_np = np.asarray(y2)
    np.save('data/no_table/y1.npy', y1_np)
    np.save('data/no_table/y2.npy', y2_np)
    y1_mean = round(np.mean(y1_np), 2)
    y2_mean = round(np.mean(y2_np),2)
    y1_error = round(np.std(y1, ddof=1),2)
    y2_error = round(np.std(y2, ddof=1),2)
    y1_mean_np = [y1_mean for i in range(0,len(x))]
    y2_mean_np = [y2_mean for i in range(0, len(x))]
    print(y1_mean)
    f.write(str(y1_mean)+'\t'+str(y1_error) + '\t'+str(y2_mean)+'\t'+str(y2_error))

    plt.plot(x, y1, label='eDMS', color='red')
    plt.plot(x, y2, label='Tesseract 4.0', color='blue')
    plt.plot(x, y1_mean_np, label='eDMS mean', color='orange', linestyle='--')
    plt.plot(x, y2_mean_np, label='Tesseract mean', color='green', linestyle='--')
    plt.plot()
    plt.ylabel('Similarity')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.legend()
    plt.show()
    plt.savefig('data/no_table/no_table.png')
    # plt.savefig('data/no_table/no_table.png')