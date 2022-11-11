# %%
import pandas as pd
def encryption_func (df:pd.DataFrame,prime_numbers=[83,97])->pd.DataFrame:
    def bloom_grams(x,grams=3)->str:
        s=["0"]*max(prime_numbers)
        #padding
        copy_x=" "*(grams-1)+str(x)+" "*(grams-1)
        for index in range(grams-1,len(copy_x)):
            curr_str=copy_x[index-grams+1:index+1]
            val=hash(curr_str)
            for i in prime_numbers:
                s[val%i]="1"
        return "".join(s)
    return df.applymap(bloom_grams)    

# %%
