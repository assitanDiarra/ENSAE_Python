import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

#read file - mortality
df_mort = pd.read_csv('mortality.csv', header=None,sep=';')
df_mort.columns=['Cancer_code', 'Sex', 'Age_bucket', 'Location', 'Year', 'Nb_deaths']
df_mort.describe()

plt.hist(df_mort['Location'], bins='auto')
plt.show()

#read age groups file (modified value 'age unknown' to 'unkown')
df_age = pd.read_csv('age.txt', header = None, sep=' ')
df_age.columns=['Age_bucket', 'Age']
df_age.head()

'''
#read file - incidence
df_inc = pd.read_csv('incidence.csv', header=None, sep=';', nrows=10000 )
df_inc.head()
df_inc.columns=['Cancer_code', 'Sex', 'Age_bucket', 'Country', 'Region', 'Ethnicity', 'Year', 'Nb_incidence' ]
df_inc.describe()
''' 

#read file - cancer codes
df_cancer = pd.read_csv('cancer_codes.csv', header=None, sep='\t')
df_cancer.columns = ['Cancer_code', 'Cancer_label']
df_cancer.head()

#merge age class df + main df
df1 = pd.merge(df_mort, df_age, how='left', left_on='Age_bucket', right_on='Age_bucket')


#read csv file - WorldBank indicators
df_wb = pd.read_csv('WorldBank_Data.csv', sep=',')
#calculate absolute values per age groups and per sex
df_wb['SP.POP.TOTL.FE.ZS'].describe() #total population female, percentage
#=> percentace is 0-100, use 100-female to get male
df_wb['SP.POP.TOTL'].describe() #total population, absolute value

#calculate new variables : transform percentage into absolute values for each group
#naming convention = old name without the .5Y at the end and without the SP in the beginning
df_wb['POP.0004.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.0004.FE.5Y']
df_wb['POP.0509.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.0509.FE.5Y']
df_wb['POP.1014.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.1014.FE.5Y']
df_wb['POP.1519.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.1519.FE.5Y']
df_wb['POP.2024.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.2024.FE.5Y']
df_wb['POP.2529.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.2529.FE.5Y']
df_wb['POP.3034.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.3034.FE.5Y']
df_wb['POP.3539.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.3539.FE.5Y']
df_wb['POP.4044.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.4044.FE.5Y']
df_wb['POP.4549.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.4549.FE.5Y']
df_wb['POP.5054.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.5054.FE.5Y']
df_wb['POP.5559.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.5559.FE.5Y']
df_wb['POP.6064.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.6064.FE.5Y']
df_wb['POP.6569.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.6569.FE.5Y']
df_wb['POP.7074.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.7074.FE.5Y']
df_wb['POP.7579.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.7579.FE.5Y']
df_wb['POP.80UP.FE']	=df_wb['SP.POP.TOTL']*df_wb['SP.POP.TOTL.FE.ZS']*df_wb['SP.POP.80UP.FE.5Y']
df_wb['POP.0004.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.0004.MA.5Y']
df_wb['POP.0509.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.0509.MA.5Y']
df_wb['POP.1014.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.1014.MA.5Y']
df_wb['POP.1519.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.1519.MA.5Y']
df_wb['POP.2024.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.2024.MA.5Y']
df_wb['POP.2529.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.2529.MA.5Y']
df_wb['POP.3034.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.3034.MA.5Y']
df_wb['POP.3539.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.3539.MA.5Y']
df_wb['POP.4044.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.4044.MA.5Y']
df_wb['POP.4549.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.4549.MA.5Y']
df_wb['POP.5054.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.5054.MA.5Y']
df_wb['POP.5559.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.5559.MA.5Y']
df_wb['POP.6064.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.6064.MA.5Y']
df_wb['POP.6569.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.6569.MA.5Y']
df_wb['POP.7074.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.7074.MA.5Y']
df_wb['POP.7579.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.7579.MA.5Y']
df_wb['POP.80UP.MA']	=df_wb['SP.POP.TOTL']*(100-df_wb['SP.POP.TOTL.FE.ZS'])*df_wb['SP.POP.80UP.MA.5Y']

#subsetting dataframe with columns to merge
df_mini = df_wb[['area','year','POP.0004.FE',	'POP.0509.FE',	'POP.1014.FE',	'POP.1519.FE',	'POP.2024.FE',	'POP.2529.FE',	'POP.3034.FE',	'POP.3539.FE',	'POP.4044.FE',	'POP.4549.FE',	'POP.5054.FE',	'POP.5559.FE',	'POP.6064.FE',	'POP.6569.FE',	'POP.7074.FE',	'POP.7579.FE',	'POP.80UP.FE',	'POP.0004.MA',	'POP.0509.MA',	'POP.1014.MA',	'POP.1519.MA',	'POP.2024.MA',	'POP.2529.MA',	'POP.3034.MA',	'POP.3539.MA',	'POP.4044.MA',	'POP.4549.MA',	'POP.5054.MA',	'POP.5559.MA',	'POP.6064.MA',	'POP.6569.MA',	'POP.7074.MA',	'POP.7579.MA',	'POP.80UP.MA']]

'''
#list of variable names about sex= female / male
df_mini.columns[df_mini.columns.str.endswith('FE')]
df_mini.columns[df_mini.columns.str.endswith('MA')]

#list of variable names about age_class = 0004
[col for col in df_mini.columns if col[4:8]=='0004']
'''

#reshaping
df_mini.set_index(['area', 'year'], inplace=True)
df_mini.columns = pd.MultiIndex.from_tuples(tuple(df_mini.columns.str.split(".")))

transf = df_mini.stack(level = [1,2]).reset_index()
transf.columns = ['Country', 'Year', 'Age_group', 'Sex', 'Population']

#match labels
'''
MA/FE -> 1/2
0004/0509/1014... -> 1/2/3...
!!!classes in worldbank folder cap at 80, mortality folder has more classes(17:80-84, 18:85+, 19:unknown)
'''
transf['Sex'].replace(['MA', 'FE'],[1,2], inplace=True)
transf['Age_group'].replace(['0004',	'0509',	'1014',	'1519',	'2024',	'2529',	'3034',	'3539',	'4044',	'4549',	'5054',	'5559',	'6064',	'6569',	'7074',	'7579'],
                              list(range(1, 17)), inplace=True)

#merge mortality data with population transformed dataframe
df = pd.merge(df_mort, 
              transf, 
              how='left', 
              left_on=['Location', 'Year', 'Age_bucket', 'Sex'], 
              right_on=['Country', 'Year', 'Age_group', 'Sex'])

#calculate mortality as a rate
df['Mortality_rate'] = df['Nb_deaths'] / df['Population']
df['Mortality_rate'].describe()


###############################
cancer='C80'
year=2000
loc='Jamaica'
df_mort[(df_mort['Cancer_code']==cancer) & (df_mort['Location']==loc) & (df_mort['Year']==2000) ]
df_mort.group_by()

#plot time series
cancer='C80'
plot_data = df_mort[df_mort['Cancer_code'] == cancer]
df_mort\
    .groupby([df_mort.Year.name, df_mort.Location.name])['Nb_deaths']\
    .sum()\
    .unstack()\
    .plot(figsize=(15,15))
