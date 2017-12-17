import pandas as pd
import numpy as np

#################################################
#read previously subset data from csv file
df3 = pd.read_csv('data.csv', header=0,sep=',', low_memory=False)

###lasso regression
'''
X_train, X_test, y_train, y_test = train_test_split(X_crime, y_crime,
                                                   random_state = 0)
'''
from sklearn.linear_model import Lasso
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

indicators = ['AG.LND.TOTL.K2',	'AG.LND.TOTL.UR.K2',	'AG.LND.AGRI.ZS',	'EG.ELC.ACCS.ZS',	'EN.ATM.CO2E.KT',	'NE.CON.TETC.CD',	'NE.EXP.GNFS.CD',	'NE.IMP.GNFS.CD',	'NV.AGR.TOTL.CD',	'NV.IND.MANF.CD',	'NV.SRV.TETC.CD',	'NY.GNS.ICTR.ZS',	'DT.ODA.OATL.CD',	'NE.CON.PETC.CD',	'NY.GDP.MKTP.CD',	'SP.POP.GROW',	'SP.POP.DPND',	'SP.POP.DPND.OL',	'SP.DYN.TFRT.IN',	'SP.DYN.TO65.FE.ZS',	'SP.DYN.TO65.MA.ZS',	'SP.DYN.IMRT.IN',	'SP.DYN.LE00.IN',	'SP.DYN.CONU.ZS',	'SN.ITK.DEFC.ZS',	'SH.XPD.TOTL.ZS',	'SH.TBS.INCD',	'SH.STA.MMRT.NE',	'SH.STA.BRTW.ZS',	'SH.PRV.SMOK.FE',	'SH.PRV.SMOK.MA',	'SH.MED.BEDS.ZS',	'SH.MED.NUMW.P3',	'SH.MED.PHYS.ZS',	'SH.HIV.1524.FE.ZS',	'SH.HIV.1524.MA.ZS',	'SM.POP.NETM',	'SL.UEM.TOTL.NE.ZS',	'SL.UEM.TOTL.ZS']
len(indicators)
X_scaled = scaler.fit_transform( df3[indicators].dropna(axis=1, how='all').fillna(0) )
#!!!TO DO: apply to df with NAs filled properly

y = df3['Mortality_rate'] #y is already scaled

linlasso = Lasso(alpha=0.005, max_iter = 10000).fit(X_scaled, y)

print('lasso regression linear model intercept: {}'
     .format(linlasso.intercept_))
print('lasso regression linear model coeff:\n{}'
     .format(linlasso.coef_))
print('Number of non-zero features: {}'
     .format(np.sum(linlasso.coef_ != 0)))
print('R-squared score (training): {:.3f}'
     .format(linlasso.score(X_scaled, y)))
'''print('R-squared score (test): {:.3f}\n'
     .format(linlasso.score(X_test_scaled, y_test)))'''
print('Features with non-zero weight (sorted by absolute magnitude):')

for e in sorted (list(zip(list(df3[indicators]), linlasso.coef_)),
                key = lambda e: -abs(e[1])):
    if e[1] != 0:
        print('\t{}, {:.3f}'.format(e[0], e[1]))       

'''Coefficients for alpha=0.05 (11 non zero features)        
        SN.ITK.DEFC.ZS, -7.530
        SL.UEM.TOTL.ZS, -3.163
        NV.AGR.TOTL.CD, -3.106
        SP.DYN.TO65.MA.ZS, -2.138
        AG.LND.AGRI.ZS, -1.616
        AG.LND.TOTL.K2, 1.421
        SH.XPD.TOTL.ZS, -0.941
        DT.ODA.OATL.CD, 0.664
        SH.MED.BEDS.ZS, 0.518
        SP.DYN.CONU.ZS, -0.508
        SL.UEM.TOTL.NE.ZS, -0.410  
        
Increasing number of iteration has no effect on the number of features.

R-squared is 0.003 for the training data set....        
'''

df3['Cancer_code'].unique()      

######### for one cancer
c = 'C80'
#df3[df3['Cancer_code'] == c][indicators].head()
X_scaled = scaler.fit_transform( df3[df3['Cancer_code'] == c][indicators].dropna(axis=1, how='all').fillna(0) )
y = df3[df3['Cancer_code'] == c]['Mortality_rate']
 
linlasso = Lasso(alpha=0.005, max_iter = 10000).fit(X_scaled, y)  
print('Number of non-zero features: {}'
     .format(np.sum(linlasso.coef_ != 0)))
print('R-squared score (training): {:.3f}'
     .format(linlasso.score(X_scaled, y)))

########### loop for several types of cancers
nb_cancers = len(df3['Cancer_code'].unique()) #74
cancer_types = list(df3['Cancer_code'].unique())[0:3]
for c in cancer_types:
    print("Cancer code: ", c)
    X_scaled = scaler.fit_transform( df3[df3['Cancer_code'] == c][indicators].dropna(axis=1, how='all').fillna(0) )
    y = df3[df3['Cancer_code'] == c]['Mortality_rate']
 
    linlasso = Lasso(alpha=0.005, max_iter = 10000).fit(X_scaled, y)  
    print('Number of non-zero features: {}'
          .format(np.sum(linlasso.coef_ != 0)))
    print('R-squared score (training): {:.3f}'
          .format(linlasso.score(X_scaled, y)))
    
########### put results in a list
nb_cancers = len(df3['Cancer_code'].unique())
cancer_types = list(df3['Cancer_code'].unique())
#initialize lists
lasso_cancer_codes = np.empty(nb_cancers, dtype=object)
lasso_r2 = np.empty(nb_cancers, dtype='float64')
lasso_nb_features = np.empty(nb_cancers, dtype='int')

i=0
for c in cancer_types:
    lasso_cancer_codes[i] = c

    X_scaled = scaler.fit_transform( df3[df3['Cancer_code'] == c][indicators].dropna(axis=1, how='all').fillna(0) )
    y = df3[df3['Cancer_code'] == c]['Mortality_rate']
 
    linlasso = Lasso(alpha=0.005, max_iter = 10000).fit(X_scaled, y)  
    lasso_nb_features[i] = np.sum(linlasso.coef_ != 0)
    lasso_r2[i] = linlasso.score(X_scaled, y)
    i = i+1

df_lasso = pd.DataFrame({'Cancer_code':lasso_cancer_codes, 'R2':lasso_r2, 'Nb_features':lasso_nb_features})   

'''
len(df3['Country'].unique())
len(df3.columns)
len(indicators)
R2 for each cancer type for years 2000 to 2005, 94 countries, 39 indicators
Best is:
Cancer_code	Nb_features	R2
C17	            33	        0.06857037645107067
C17 = small intestine
'''

#output file with percentages
df_lasso.to_csv(path_or_buf = 'lasso_choice_cancers.csv', sep=',', na_rep='')










