import pandas as pd
import numpy as np
import time

class imputers:
    
    def __init__(self, filename):
        self.fname = filename
        self.df = pd.read_csv(self.fname)
        self.mean_time = 0.0
        self.hot_time = 0.0

    def mae(self):
        pass
    
    def mean_imputation(self):
        start = time.time()
        sums = {}
        sum_val = {}
        count = 0
        for col in self.df:
            #vectorize for performance reasons
            sums[col] = self.df[col].to_numpy()
            sums[col] = [np.nan if item == '?' else item for item in sums[col]]
            sums[col] = [float(item) for item in sums[col]]
            sum_val[col] = np.nansum(sums[col])
            

        end = time.time()
        self.mean_time = (end - start)  * 1000
        print(self.mean_time)
        pass

    def hot_deck_imputation(self):
        pass

    def print_results(self):
        pass

    def sv(self, filename): 
        pass   

    def inspect(self):
        pass

def main():
    imp = imputers('dataset_missing01.csv')
    imp.mean_imputation()

if __name__ == '__main__':
    main()