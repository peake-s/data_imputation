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
        end = time.time()

        self.mean_time = (end - start) * 1000
        pass

    def hot_deck_imputation(self):
        pass

    def print_results(self):
        pass

    def sv(self, filename): 
        pass   

    def inspect(self):
        pass


