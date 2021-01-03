# Pandas introductory lesson
#%%
import pandas as pd 


df = pd.read_excel('sample_pivot.xlsx', parse_dates=['Date']) 

print(df.head(10))
print(df.tail())

#%%
# This gave us a summary of the Sales field by Region. 
# The default parameter for aggfunc is mean. 
# Because of this, the Sales field in the resulting dataframe is 
# the average of Sales per Region.
sales_by_region = pd.pivot_table(df, index = 'Region', values = 'Sales') 
print(sales_by_region)


# %%
# Now specify the aggregation function as "sum" and you get the total sales
# per region:
total_by_region = pd.pivot_table(df, index = 'Region', values = 'Sales', aggfunc='sum') 
#print(total_by_region.sort(['Sales'], ascending = [1]))
new = total_by_region.sort_values(['Sales'], ascending=[1])
print(df['Sales']*2)

# %%
# Now go and construct a pivot table where the sales are aggregated 
# according to clothing type:


# %% 
# It is easy to add a column to a pandas dataframe:
df.head()

df['Average unit cost'] = df['Sales']/df['Units']

df.head()


# %% Multi index pivot table

multi_index = pd.pivot_table(df, index = ['Region', 'Type'], values = 'Sales', aggfunc = 'sum') 
print(multi_index)



# %%
# Now that we’ve created our first few pivot tables, let’s explore 
# how to filter the data. Let’s create a dataframe that 
# generates the mean Sale price by Region:

avg_region_price = pd.pivot_table(df, index = 'Region', values = 'Sales')

# Now, say we wanted to filter the dataframe to only include Regions 
# where the average sale price was over 450, we could write:
avg_region_price[avg_region_price['Sales'] > 450]

# We can also apply multiple conditions, such as filtering to show only 
# sales greater than 450 or less than 430. I know this is a strange 
# example, but it’s just illustrative:
avg_region_price[(avg_region_price['Sales'] > 450) | (avg_region_price['Sales'] < 430)]


# %% 
#Adding columns to a pivot table in Pandas can add another 
# dimension to the tables. Based on the description we provided 
# in our earlier section, the Columns parameter allows us to 
# add a key to aggregate by. For example, if we wanted to see 
# the number of units sold by Type and by Region, we could write:

#columns_example = pd.pivot_table(df, index = 'Type', columns = 'Region', values = 'Units', aggfunc = 'sum') 
#print(columns_example)
#columns_example.plot(kind='bar')

print(sales_by_region.index) #.plot(kind='pie')

df = pd.DataFrame({'mass': [0.330, 4.87 , 5.97],
                   'radius': [2439.7, 6051.8, 6378.1]},
                  index=['Mercury', 'Venus', 'Earth'])
plot = df.plot.pie(y='mass', figsize=(5, 5))
# %%
