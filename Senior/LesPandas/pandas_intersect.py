#%%
#https://www.kdnuggets.com/2019/11/set-operations-applied-pandas-dataframes.html

import pandas as pd
import numpy as np

#Create a DataFrame
df1 = {
    'Subject':['semester1','semester2','semester3','semester4','semester1',
               'semester2','semester3'],
   'Score':[62,47,55,74,31,77,85]}

df2 = {
    'Subject':['semester1','semester2','semester3','semester4'],
   'Score':[90,47,85,74]}


df1 = pd.DataFrame(df1,columns=['Subject','Score'])
df2 = pd.DataFrame(df2,columns=['Subject','Score'])

print(df1)
print(df2)

#%%

intersected_df = pd.merge(df1, df2, how='inner')
print(intersected_df)
# %%

#(1)-Defining the DataFrames

# 1.1 Python students
P = pd.DataFrame ({"name":["Elizabeth","Darcy"],
        "email":["bennet@xyz.com","darcy@acmecorpus.com"]})

# 1.2 SQL students
S = pd.DataFrame ({"name":["Bingley","Elizabeth"],
        "email": ["bingley@xyz.com","bennet@xyz.com"]})




# %%

#(2)-Performing set operations

# 2.1 Union
all_students = pd.concat([P, S], ignore_index = True)
all_students = all_students.drop_duplicates()

# %%

# 2.2 Intersection
sql_and_python = P.merge(S)


# %%
# 2.3 Difference
python_only = P[P.email.isin(S.email) == False]
sql_only = S[S.email.isin(P.email) == False]
# %%

# Skryf na Excel toe
all_students.to_excel('aldiestudente.xlsx')
# %%

# Import alle modules


# Import all files
# List all operation to be run on the files
# 1. 