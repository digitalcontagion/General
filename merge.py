import os
import pandas as pd

seed =  r'r'
def dirwalk(seed):
    with open('outfile.csv', 'w') as fout:
        for (paths, directory, files) in os.walk(seed):
            for file in files:
                a = pd.read_csv(file)
                b = b.dropna(axis=1)
                merged = a.merge(b, on='title')
                merged.to_csv("output.csv", index=False)


dirwalk(seed)




