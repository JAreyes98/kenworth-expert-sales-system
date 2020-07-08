import pandas as pd
import math

class DataFilter:

    def __init__(self, df, var1, var2):
        self.df = df
        self.variable1 = var1
        self.variable2 = var2        
    
    def filter_one(self):
        
        base_sale_year = 0

        weeks= []
        sales= []
        mean = self.df[self.variable2].mean()

        for i in range(0, self.df[self.variable2].count()):
            week = self.df[self.variable1][i]
            sale = self.df[self.variable2][i]
            
            if((math.fabs(self.df[self.variable2][i] - base_sale_year)) < (mean/2)):
                sales.append(sale)
            else:
                sales.append(0)
            
            base_sale_year = self.df[self.variable2][i]
            weeks.append(week)

        return pd.DataFrame({self.variable1:weeks, self.variable2:sales})

    def filter_two(self):
        base_sale_year = 0

        df = self.filter_one()

        ml = []
        ls = [[],[]]

        rowsNumber = df[self.variable2].count()

        for i in range(0, rowsNumber):
            week = df[self.variable1][i]
            sale = df[self.variable2][i]
            
            if(sale == 0):
                if(i != 0):
                    ml.append(ls)
                ls = [[],[]]
            else :
                ls[0].append(week)
                ls[1].append(sale)
            

        return ml

    def filter_three(self):
        lastList = self.filter_two()
        
        lastIndex = len(lastList) - 1
        
        df = pd.DataFrame({self.variable1:lastList[lastIndex][0], self.variable2:lastList[lastIndex][1]})

        return df

    def filter(self):
        return self.filter_three()