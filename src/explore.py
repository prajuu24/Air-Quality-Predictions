import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data
file_path = "data/AirQuality.csv"
df = pd.read_csv(file_path, sep=';', decimal=',')

# Clean the data by dropping unnamed columns and null values
df = df.drop(['Unnamed: 15', 'Unnamed: 16'], axis=1)
df = df.dropna()

# Convert datetime properly
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df['Time'] = pd.to_datetime(df['Time'], format='%H.%M.%S').dt.time
df['DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))

# Create visualizations
plt.figure(figsize=(15, 10))

# Plot 1: Distribution of CO levels
plt.subplot(2, 2, 1)
sns.histplot(data=df['CO(GT)'], kde=True)
plt.title('Distribution of CO Levels')
plt.xlabel('CO Concentration')

# Plot 2: Time series of CO levels
plt.subplot(2, 2, 2)
plt.plot(df['DateTime'], df['CO(GT)'])
plt.title('CO Levels Over Time')
plt.xlabel('Time')
plt.ylabel('CO Concentration')
plt.xticks(rotation=45)

# Plot 3: Temperature vs CO levels
plt.subplot(2, 2, 3)
sns.scatterplot(data=df, x='T', y='CO(GT)')
plt.title('Temperature vs CO Levels')
plt.xlabel('Temperature')
plt.ylabel('CO Concentration')

# Plot 4: Correlation heatmap
plt.subplot(2, 2, 4)
numeric_columns = ['CO(GT)', 'PT08.S1(CO)', 'NMHC(GT)', 'C6H6(GT)', 'NOx(GT)', 'T', 'RH', 'AH']
correlation_matrix = df[numeric_columns].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')

plt.tight_layout()
plt.savefig('data/air_quality_analysis.png')
plt.show()

# Print summary statistics
print("\n=== Key Statistics ===")
print(df[['CO(GT)', 'T', 'RH', 'AH']].describe())

# Print correlation insights
print("\n=== Strong Correlations ===")
correlations = correlation_matrix['CO(GT)'].sort_values(ascending=False)
print(correlations)