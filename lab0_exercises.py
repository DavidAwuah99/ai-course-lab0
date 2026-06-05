import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

"""
Exercise 4:NumPy Operations
"""

#Task 1
matrix = np.ones((5,5))

matrix[1:4,1:4]=0

print("Task 1: ")
print(matrix)


#Task 2
np.random.seed(42)
random_data = np.random.randn(100,3)

means= np.mean(random_data, axis=0)
stds= np.std(random_data, axis=0)

normalized_data = (random_data-means)/stds

print("\nTask2: ")
print("Column means: ")
print(np.mean(normalized_data, axis=0))

print("\nStandard Deviations for Columns: ")
print(np.std(normalized_data, axis=0))


#Task 3

X = np.random.randn(50, 3)
true_theta = np.array([2.5,-1.2,3.7])
y = X @ true_theta + np.random.randn(50) * 0.1

theta_hat = np.linalg.inv(X.T @ X) @ X.T @ y

print("\nTask 3:")
print("Estimated coefficients: ")
print(theta_hat)

print("\nTrue coefficients: ")
print(true_theta)

"""
Exercise 2:Pandas Data Analysis
"""

np.random.seed(42)
n_students = 200

data = {
    'student_id': range(1000, 1000 + n_students),'major': np.random.choice(['CS', 'Math', 'Physics', 'Biology'], n_students),'year': np.random.choice([1,2,3,4], n_students),'exam_score': np.random.normal(75,10,n_students).clip(0,100),'assignments_completed': np.random.randint(0,11,n_students),
    'hours_studied': np.random.normal(15,5,n_students).clip(1,40)
}

df = pd.DataFrame(data)

df.loc[np.random.choice(n_students,10), 'exam_score'] = np.nan
df.loc[np.random.choice(n_students, 5), 'hours_studied'] = np.nan

print(df.info())
print(df.describe())

print("\nMissing values: ")
print(df.isnull().sum())

df['exam_score'] = df.groupby('major')['exam_score'].transform(lambda x: x.fillna(x.median()))

avg_scores = df.groupby('major')['exam_score'].mean()
print(avg_scores)

best_major = avg_scores.idxmax()
print("Best Major: ", best_major)

correlation = df['hours_studied'].corr(df['exam_score'])
print("Correlation: ", correlation)

df['performance'] = pd.cut(df['exam_score'],bins=[0,70,80,90,100],labels = ['Needs improvement', 'Average', 'Good', 'Excellent'],include_lowest = True )


analysis = df.groupby(['major','year']).agg(
    num_students=('student_id', 'count'),
    avg_score=('exam_score', 'mean'),
    avg_hours= ('hours_studied', 'mean')
)

print(analysis)

top5 = df.nlargest(5, 'exam_score')
print(top5)

pivot = pd.pivot_table(
    df,
    values='exam_score',
    index= 'major',
    columns='year',
    aggfunc='mean'
)

print(pivot)



"""Exercise 3:Data Visualization """

#Task 1

plt.figure(figsize=(14,5))

plt.subplot(1,2,1)
sns.histplot(df['exam_score'], kde = True)
plt.title("Exam scores by major")

plt.tight_layout()
plt.show()


#Task 2

plt.figure(figsize=(10,6))

sns.scatterplot(data=df,x='hours_studied',y='exam_score',hue='major')

sns.regplot(data=df,x='hours_studied',y='exam_score',scatter=False)

plt.title("Hours Studied vs Exam Score")
plt.show()


#Task 3 

fig,axes = plt.subplots(2,2,figsize=(15,10))

avg_scores.plot(kind='bar', ax=axes[0,0])
axes[0,0].set_title("Average Score by Major")


sns.countplot(data=df, x='year', ax = axes[0,1])
axes[0,1].set_title("Student by Year")

sns.heatmap(df.select_dtypes(include=np.number).corr(),annot=True,ax=axes[1,0])

axes[1,0].set_title("Correlation Matrix")

sns.violinplot(data=df,x='performance',y='exam_score',ax=axes[1,1])

axes[1,1].set_title("Performance Distribution")

plt.tight_layout()
plt.show()



"""
Exercise 7: Integration Challenge

"""

np.random.seed(42)
n_customers =500

ages = np.random.randint(18,70,n_customers)
income = np.random.normal(50000, 20000, n_customers).clip(15000, 150000)
purchase_freq = np.random.poisson(5, n_customers)
avg_purchase_value = np.random.normal(100,30,n_customers).clip(10,500)

customers = pd.DataFrame({
    'age': ages,
    'income': income,
    'purchase_frequency': purchase_freq,
    'avg_purchase_value': avg_purchase_value
})

max_frequency = customers['purchase_frequncy'].max()

customers['churn_risk'] = (
    1-customers['purchase_frequncy']/max_frequency
)

customers['CLV'] = (
    customers['purchase_frequncy'] * customers['avg_purchase_value'] * (1+customers['churn_risk'])
)



customers['age_group'] = pd.cut(
    customers['age'],
    bins= [18,25,35,50,70],
    labels= ['18-25', '26-35', '36-50', '51-70']
)



summary = customers.groupby('age_group').agg(
    num_customers = ('age','count'),
    avg_income = ('income','mean'),
    avg_clv= ('CLV', 'mean'),
    total_clv= ('CLV', 'sum')
)

print(summary)



threshold= customers['CLV'].quantile(0.9)

top_customers = customers[
    customers['CLV'] >= threshold
]

print(top_customers)



plt.figure(figsize=(10,6))
sns.scatterplot(
    data=customers,
    x='income',
    y='CLV',
    hue='age_group'
)
plt.title("Income vs CLV")
plt.show()


plt.figure(figsize=(8,5))
customers.groupby('age_group')['CLV'].mean().plot(kind='bar')
plt.title("Average CLV by Age Group")
plt.show()


plt.figure(figsize=(8,6))
sns.heatmap(
    customers.select_dtypes(include=np.number).corr(),
    annot=True
)
plt.title("Customer Correlation Matrix")
plt.show()