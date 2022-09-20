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
        col_len = self.df.shape[0]
        nan_count = 0
        for col in self.df:
            #vectorize for performance reasons
            sums[col] = self.df[col].to_numpy()
            #replace ? with nan. Probably a better way to do this as in not doing it at all
            sums[col] = [np.nan and nan_count + 1 if item == '?' else item for item in sums[col]]
            sums[col] = [float(item) for item in sums[col]]
            sum_val[col] = np.nansum(sums[col])/(col_len-nan_count)
        
        for key,vals in sums.items():
            #loop over dicitonary 
            #replace nan values with the mean
            for (idx,val) in enumerate(vals):
                if np.isnan(val):
                    sums[key][idx] = sum_val[key]
                    print(val)

        self.df = pd.DataFrame(sums)

        end = time.time()
        self.mean_time = (end - start)  * 1000
        print(f"Run time in ms {self.mean_time} to impute {self.filename}")
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
    imp = imputers('dataset_missing10.csv')
    imp.mean_imputation()

if __name__ == '__main__':
    main()