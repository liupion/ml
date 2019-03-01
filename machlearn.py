import os
import pandas as pd
import requests
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

PATH = r'./'
# for i in df.columns:
#     if i == 'class': continue
#     print(int(j/2),j%2)
#     ax[int(j/2)][j%2].hist(df[i], color='g',alpha=0.8)
#     ax[int(j/2)][j % 2].set_xlabel(i)
#     ax[int(j/2)][j % 2].set_title(i)
#     ax[int(j/2)][j % 2].grid(True)
#     j += 1
# plt.tight_layout()
# plt.show()



# plt.subplot(121)
# plt.scatter(df['sepal length'],df['sepal width'])
# plt.title(u"散点图")
# plt.xlabel('sepal length')
# plt.ylabel('sepal width')
# plt.grid(True)
# plt.subplot(122)
# plt.scatter(df['petal length'],df['petal width'])
# plt.show()

# r = requests.get('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data')
#
# with open(PATH + 'iris.data', 'w') as f:
#     f.write(r.text)

df = pd.read_csv(PATH + 'iris.data',
                 names=['sepal length', 'sepal width','petal length', 'petal width', 'class'])

# print(df.loc[:10,[x for x in df.columns if 'width' in x]])

# fig, ax = plt.subplots(2, 2, figsize=(10,6))
# j = 0

# label = [x for x in df.columns if x!='class']
# ver_y = [df[df['class']=='Iris-versicolor'][x].mean() for x in label]
# vir_y = [df[df['class']=='Iris-virginica'][x].mean() for x in label]
# set_y = [df[df['class']=='Iris-setosa'][x].mean() for x in label]
# x = np.arange(len(label))
# plt.bar(x,vir_y,bottom=set_y,color='c')
# plt.bar(x,set_y,bottom=ver_y,color='y')
# plt.bar(x,ver_y,color='b')
# plt.xticks(x,label,fontsize=12)
# plt.title("均值")
# plt.legend(df['class'].unique())
# plt.show()

# sns.pairplot(df,hue='class')
# plt.show()

# fig, ax = plt.subplots(2, 2, figsize=(7, 7))
# sns.set(style='white', palette='muted')
# sns.violinplot(x=df['class'], y=df['sepal length'], ax=ax[0,0])
# sns.violinplot(x=df['class'], y=df['sepal width'], ax=ax[0,1])
# sns.violinplot(x=df['class'], y=df['petal length'], ax=ax[1,0])
# sns.violinplot(x=df['class'], y=df['petal width'], ax=ax[1,1])
# fig.suptitle('Violin Plots', fontsize=16, y=1.03)
# for i in ax.flat:
#     plt.setp(i.get_xticklabels())
# fig.tight_layout()
# plt.show()
#
# df['wide petal'] = df['petal width'].apply(lambda x:1 if x>1.3 else 0)
# df['sepal area'] = df.apply(lambda x:x['sepal length']*x['sepal width'],axis=1)
# dd = df.applymap(lambda x:np.log(x) if isinstance(x,float) else x)
#
# print(df.groupby('class')['petal width'].agg({'delta':lambda x:x.max()-x.min(),
#            'max':np.max,'min':np.min}))

# plt.scatter(df['sepal width'][:50],df['sepal length'][:50])
# plt.xlabel('sepal width')
# plt.ylabel('sepal length')
# plt.grid(True)
# plt.show()

# y = df['sepal length'][:50]
# x = df['sepal width'][:50]
# X =sm.add_constant(x)
#
# results = sm.OLS(y,X).fit()
# print(results.summary())
#
# plt.scatter(x,y,label='data point',color='r')
# plt.plot(x,results.fittedvalues,label='regression line')
# plt.legend(loc=4)
# plt.show()

clf = RandomForestClassifier(max_depth=5,n_estimators=10)
x = df.iloc[:,:4]
y = df.iloc[:,4]
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=.3)
clf.fit(x_train,y_train)
y_pred = clf.predict(x_test)
rf = pd.DataFrame(list(zip(y_pred,y_test)),columns=['predict','actual'])

rf['correct']=rf.apply(lambda x:1 if x['predict']==x['actual'] else 0,axis=1)
print(rf)
print(rf['correct'].sum()/rf['correct'].count())

f_importances = clf.feature_importances_

f_names=df.columns[:4]
print(f_importances)

f_std = np.std([tree.feature_importances_ for tree in clf.estimators_], axis=0)
zz = zip(f_importances, f_names, f_std)
print(zz)
zzs = sorted(zz, key=lambda x: x[0], reverse=True)
imps = [x[0] for x in zzs]
labels = [x[1] for x in zzs]
errs = [x[2] for x in zzs]
plt.bar(range(len(f_importances)), imps, color="r", yerr=errs,align="center")
plt.xticks(range(len(f_importances)), labels);
plt.show()


