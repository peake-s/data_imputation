import pandas as pd
import numpy as np
import time

from pytools import P

class imputers:
    
    def __init__(self, filename):
        self.fname = filename
        self.df = pd.read_csv(self.fname)
        self.complete_df = pd.read_csv('dataset_complete.csv')
        self.run_time = 0.0
        self.num_imputed = 0
        self.mae = 0.0
        self.df_vec = []

    def _mae_calc(self,locations):
        #extract locations of imputed values and compare
        for col in self.complete_df:
            for idx in locations:
                #loop over the array of locations
                self.mae += abs(self.df[col][idx] - self.complete_df[col][idx]) 
        
        self.mae = round((self.mae/self.num_imputed),4)
        
    
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
        
    def _find_missing(self):
        missing_pos = []
        missing_rows = []
        for (idx,col) in enumerate(self.df_vec):
            for (i,val) in enumerate(col):
                if val == '?':
                    self.df_vec[idx][i] = 1.0 
                    missing_pos.append(i)
                    missing_rows.append(i)
                    self.num_imputed += 1

                self.df_vec[idx][i] = float(self.df_vec[idx][i])
        return (missing_pos, missing_rows)

    def _to_vec(self):
        df_vec = self.df.to_numpy()
        #for col in self.df:
        #    df_vec[col] = self.df[col].to_numpy()
        return df_vec

    def _manhattan_distance(self,r, idx,idx_c,dfvec):
        #compare values across all objects]
        current = 1000
        val_to_replace = 0
        #loop over all rows except the one passed in
        for (i,row) in enumerate(dfvec):
            if i == idx:
                next
            distance = sum(abs(np.subtract(row,r)))
            if distance < current:
                current = distance
                val_to_replace = dfvec[i][idx_c]
        print(val_to_replace)
        return val_to_replace

    def _hot_deck_imputation(self):
        start = time.time()
        #indexes of the missing values
        self.df_vec = self._to_vec()
        locations,missing_rows = self._find_missing()
        
        
        #iterate over rows
        for (idx,row) in enumerate(self.df_vec):
            if idx in missing_rows:
                self.df_vec[idx][locations[idx]] = self._manhattan_distance(row, idx,locations[idx],self.df_vec)

        x = list(self.df)
        self.df = pd.DataFrame(self.df_vec,columns=x)

        end = time.time()
        self.run_time = (end - start) * 1000

        return locations
 
    def sv(self, filename): 
        self.df.to_csv(filename,index=False)

    def impute(self, type = None, missing = '0'):
        if type == "mean":
            locs = self._mean_imputation()
            self._mae_calc(locs)
            print(f"MAE_{missing}_{type} = {self.mae}")
            print(f"Runtime_{missing}_{type} = {self.run_time}")
        else:
            locs = self._hot_deck_imputation()
            self._mae_calc(locs)
            print(f"MAE_{missing}_{type} = {self.mae}")
            print(f"Runtime_{missing}_{type} = {self.run_time}")
        
        fname = f"V00907458_missing{missing}_imputed_{type}.csv"
        self.sv(fname)

def main():
    imp_mean_01 = imputers('dataset_missing01.csv')
    imp_mean_01.impute(type = 'mean',missing = '01')
    imp_mean_10 = imputers('dataset_missing10.csv')
    imp_mean_10.impute(type = 'mean',missing = '10')
    imp_hd_01 = imputers('dataset_missing01.csv')
    imp_hd_01.impute(type = 'hd',missing = '01')
    imp_hd_10 = imputers('dataset_missing10.csv')
    imp_hd_10.impute(type = 'hd',missing = '10')

if __name__ == '__main__':
    main()