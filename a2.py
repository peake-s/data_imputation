import pandas as pd
import numpy as np
import time

class imputers:
    
    def __init__(self, filename):
        self.fname = filename
        self.df = pd.read_csv(self.fname)
        self.complete_df = pd.read_csv('dataset_complete.csv')
        self.run_time = 0.0
        self.num_imputed = 0
        self.mae = 0.0

    def _mae_calc(self,locations):
        #extract locations of imputed values and compare
        for col in self.complete_df:
            for idx in locations:
                #loop over the array of locations
                self.mae += abs(self.df[col][idx] - self.complete_df[col][idx]) 
        
        self.mae = self.mae/self.num_imputed
        
    
    def _missing_count(self,data_vecs):
        count = 0
        for (idx,item) in enumerate(data_vecs):
            if item == '?':
                data_vecs[idx] = np.nan
                count += 1

            data_vecs[idx] = float(data_vecs[idx])

        return (count, data_vecs)

    def _mean_imputation(self):
        start = time.time()
        sums = {}
        sum_val = {}
        col_len = self.df.shape[0]
        nan_count = 0
        locations = []
        #self.df.replace('?',np.nan)
        for col in self.df:
            #vectorize for performance reasons
            sums[col] = self.df[col].to_numpy()
            nan_count,sums[col] = self._missing_count(sums[col])
            self.num_imputed+=nan_count
            sum_val[col] = round((np.nansum(sums[col])/(col_len-nan_count)),5)
        
        for key,vals in sums.items():
            #loop over dicitonary 
            #replace nan values with the mean
            for (idx,val) in enumerate(vals):
                if np.isnan(val):
                    sums[key][idx] = sum_val[key]
                    locations.append(idx)


        self.df = pd.DataFrame(sums)

        end = time.time()
        
        self.run_time = (end - start) * 1000
        
        return locations
        

    def _hot_deck_imputation(self):
        pass

    def sv(self, filename): 
        self.df.to_csv(filename)

    def impute(self, type = None, missing = '0'):
        if type == "mean":
            locs = self._mean_imputation()
            self._mae_calc(locs)
            print(f"MAE_{missing}_{type} = {self.mae:.4f}")
            print(f"Runtime_{missing}_{type} = {self.run_time}")
        else:
            locs = self._hot_deck_imputation()
            self._mae_calc(locs)
            print(f"MAE_{missing}_{type} = {self.mae:.4f}")
            print(f"Runtime_{missing}_{type} = {self.run_time}")

def main():
    imp = imputers('dataset_missing01.csv')
    imp.impute(type = 'mean',missing = '01')


if __name__ == '__main__':
    main()