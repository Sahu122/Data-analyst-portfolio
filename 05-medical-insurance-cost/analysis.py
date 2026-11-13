import numpy as np
import pandas as pd
import seaborn as sns
import  matplotlib.pyplot as plt

df = pd.read_excel("insurance.xlsx")
print(df.head())

# print("shape:",df.shape)
# print(df.isnull().sum())
# print("Duplicates:", df.duplicated().sum())

df = df.drop_duplicates()
# print("Shape after removing duplicates:",df.shape)

df['age_group'] = pd.cut(
    df['age'],
    bins=[17,25,35,45,55,64],
    labels=['18-25','26-35','36-45','46-55','56-64']
)

df['bmi_category'] = pd.cut(
    df['bmi'],
    bins=[0,18.5,25,30,100],
    labels=['Underweight','Normal','Overweight','Obese'],
    right=False
)

df['has_children'] = np.where(df['children']>0,'Yes','No')

print(df.head())
print(df['age_group'].value_counts())
print(df['bmi_category'].value_counts())
print(df['has_children'].value_counts())


print("\n1. Smoker vs Non-smoker")
print(df.groupby('smoker')['charges'].mean().round(2))

print("\n2. Age Group wise")
print(df.groupby('age_group', observed=True)['charges'].mean().round(2))

print("\n3. BMI Category wise")
print(df.groupby('bmi_category', observed=True)['charges'].mean().round(2))

print("\n4. Region wise")
print(df.groupby('region')['charges'].mean().round(2).sort_values(ascending=False))

print("\n5. Male vs Female")
print(df.groupby('sex')['charges'].mean().round(2))

print("\n6. Smoker + BMI Category")
print(df.groupby(['smoker', 'bmi_category'], observed=True)['charges'].mean().round(2))

print("\n7. Correlation")
print(df.corr(numeric_only=True)['charges'].round(2))

df['smoker_flag'] = np.where(df['smoker'] == 'yes', 1, 0)
print(df.corr(numeric_only=True)['charges'].round(2))

# # export (sabse last)
# df.to_excel('insurance_clean.xlsx', index=False)
df = df.info()
print(df)