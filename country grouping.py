import pandas as pd
import numpy as np

#read csv file - WorldBank indicators
df_wb = pd.read_csv('WorldBank_Data.csv', sep=',')
#select one year
df_wb = df_wb[df_wb['year']==2015]

#df_wb['SP.POP.TOTL'].head()

#read csv file - groups of countries
df_groups = pd.read_csv('countries_groups.csv', sep=',')

#df_wb[['area_code', 'area']].head()
'''
checky = pd.merge(df_wb[['area_code', 'area']], 
         df_groups, how='left', 
         left_on='area', right_on='Group')
#ok : merging by labels provides exact matches
'''

#select codes that don't represent countries in order to exclude them
tmp = pd.merge(df_wb[['area_code', 'area']], 
         df_groups, how='inner', 
         left_on='area', right_on='Group')['area_code']

# df_wb[df_wb['area_code'] in list(tmp)] #doesn't work!!!

#df_wb[-df_wb['area_code'].isin(tmp)][['area_code', 'area']].head(50)
#ok : only countries per se, no groups

#exclude codes corresponding to groups, not countries
df_wb = df_wb[-df_wb['area_code'].isin(tmp)]

#set country name as index
df_wb.set_index('area',inplace=True)
#drop redundant columns (keep only indicator columns)
#df_wb.drop(['area_code', 'year'],axis=1,inplace=True)
df_wb.drop(['year'],axis=1,inplace=True)

#df_wb.shape #=> 218 rows (countries), 872 columns(indicators)
#df_wb.shape[0] #select number of rows

#check for each indicator how many missing values there are
cutoff = 0.25
nb_na = df_wb.isnull().sum() #returns a Series object
df_na = pd.DataFrame({'indicator':nb_na.index, 'na_nb':nb_na.values}) #put in a dataframe
df_na.sort_values(by=['na_nb'], ascending=False, inplace=True) #sort descending
df_na['na_pct'] = df_na['na_nb'] / df_wb.shape[0] #calculate percentage of missing values 
#df_na[df_na['na_pct'] < cutoff].count() #255 = number of indicators to be kept
df_na['flag_keep_indicator'] = np.where(df_na['na_pct'] < cutoff,1,0) #flag indicators to keep 
     
#eliminate indicators with too many missing values
df_na[df_na['flag_keep_indicator']==1][['indicator','flag_keep_indicator']] #columns to be kept
all_columns = pd.DataFrame({'indicator':df_wb.columns}) #all columns
keep_columns = pd.merge(df_na[df_na['flag_keep_indicator']==1],
                        all_columns,
                        how = 'inner', left_on='indicator', right_on='indicator')
#df_wb.loc[:, keep_columns['indicator']].head()
df_wb = df_wb.loc[:, keep_columns['indicator']] #keep specified columns from the list
#df_wb.shape #=> 218 rows (countries), 225 columns(indicators)

#check for each country how many missing values it has
nb_indic = df_wb.shape[1] #225
df_na_country = pd.DataFrame({'country': df_wb.T.isnull().sum().index, 'na_nb':df_wb.T.isnull().sum().values})
df_na_country.sort_values(by=['na_nb'], ascending=False, inplace=True)


##examine correlations between indicators
#1
#pd.scatter_matrix(df_wb, alpha = 0.3, figsize = (14,8), diagonal = 'kde')
#crashes my program

#2
import matplotlib.pyplot as plt
plt.matshow(df_wb.corr())

#3
import seaborn as sns
f, ax = plt.subplots(figsize=(15, 15))
corr = df_wb.corr()
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)


##############################PCA
#subset features, fill missing values !!!! replace by forward with last available year!!!
X = df_wb.drop(['area_code'],axis=1,inplace=False).fillna(df_wb.mean())
#standardize features
from sklearn.preprocessing import StandardScaler
X_std = StandardScaler().fit_transform(X)

from sklearn.decomposition import PCA
pca = PCA(n_components=2)

np.set_printoptions(precision=3) #set number of decimals
np.set_printoptions(suppress=True) # suppress scientific notation for small numbers
print(pca.explained_variance_ratio_[0:9])
#the first 2 components explain 27.5% + 16.2% = 43.7% of the variance

#plot number of components to consider against proportion of explained variance
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance')

#plot countries in 2D space
projected = pca.fit_transform(X_std)
plt.scatter(projected[:, 0], projected[:, 1])
plt.xlabel('component 1')
plt.ylabel('component 2')
#=>KO: no clear grouping emerges


############################## unsupervised clustering - DBSCAN
#http://scikit-learn.org/stable/modules/clustering.html#dbscan
from sklearn.cluster import DBSCAN
#db = DBSCAN(eps=0.3, min_samples=10).fit(X_std)
db = DBSCAN().fit(X_std)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print('Nb clusters: %d' % n_clusters_)
#=> KO: no clusters formed

plt.hist(labels, bins=5)
plt.show()
#=> KO: one single cluster


######grouping countries
#read Excel of country groups
df_groups = pd.read_excel(io='CLASS.xls', sheet_name='List of economies'
              ,header = 4)
#df_groups.columns
df_groups.drop(['x', 'x.1', 'X'],axis=1,inplace=True) #remove unwanted columns
df_groups = df_groups.loc[1:, df_groups.columns] #remove unwanted rows

inc = df_groups.groupby(['Income group'], axis=0)       
groupby_inc = df_groups['Code'].groupby(df_groups['Income group'])                  
#list(groupby_inc)[0]
'''
for code, group in groupby_inc: 
    print(code)
    print(group)
    
0 - High income
1 - Low income
2 - Lower middle income
3 - Upper middle income
'''
list(groupby_inc)[0][1]
list(groupby_inc)[1][1]


#################
from sklearn.cluster import KMeans
clus = KMeans(4)
clus.fit(X_std)
KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
    n_clusters=4, n_init=10, n_jobs=1, precompute_distances='auto',
    random_state=None, tol=0.0001, verbose=0)
pred = clus.predict(X_std)
set(pred)

centers = clus.cluster_centers_.T
import matplotlib.pyplot as plt
fig, ax = plt.subplots(centers.shape[1], 1, figsize=(10,10))
x = list(range(0,centers.shape[0]))
for i in range(centers.shape[1]):
    ax[i].bar (x, centers[:,i], width=2.0)
    ax[i].set_ylabel("cluster %d" % i)


