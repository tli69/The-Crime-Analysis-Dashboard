from data import *
import matplotlib.pyplot as plt
import seaborn as sns
 
def plot_crime_trend(df):
    # Convert the 'date' column to datetime data type
    df['date'] = pd.to_datetime(df['date'])

    # Extract the year and month from the 'date' column
    df['year_month'] = df['date'].dt.to_period('M')

    # Group by year and month and count the number of crimes in each period
    crime_trend = df.groupby('year_month').size().reset_index(name='count')

    # Convert 'year_month' values to string format for plotting
    crime_trend['year_month'] = crime_trend['year_month'].astype(str)

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Plot Scatter chart
    ax1.scatter(crime_trend['year_month'], crime_trend['count'], color='b', label='Scatter', alpha=0.5)
    ax1.set_title('Crime Trend Over Time (Scatter)')
    ax1.set_xlabel('Year-Month')
    ax1.set_ylabel('Number of Crimes')
    ax1.legend()

    # Plot Line chart
    ax2.plot(crime_trend['year_month'], crime_trend['count'], color='r', label='Line')
    ax2.set_title('Crime Trend Over Time (Line)')
    ax2.set_xlabel('Year-Month')
    ax2.set_ylabel('Number of Crimes')
    ax2.legend()

    # Adjust layout
    plt.tight_layout()

    # Show the plot
    plt.show()

def plot_crime_by_day(df):
    # Code to plot the crime distribution by day of the week (Example 2)
    df['day_of_week'] = df['date'].dt.day_name()
    crime_by_day = df['day_of_week'].value_counts()

    plt.figure(figsize=(8, 6))
    crime_by_day.plot(kind='bar', color='skyblue')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Crimes')
    plt.title('Crime Distribution by Day of the Week')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()

def plot_crime_by_time(df):
    # Code to plot the crime distribution by time of day (Example 3)
    df['hour'] = df['date'].dt.hour

    plt.figure(figsize=(8, 6))
    plt.hist(df['hour'], bins=24, color='orange', edgecolor='black')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Crimes')
    plt.title('Crime Distribution by Time of Day')
    plt.xticks(range(24))
    plt.grid(axis='y')
    plt.show()

def plot_top_locations(df):
    # Code to plot the top locations for different crime types (Example 4)
    top_locations = df['block'].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    top_locations.plot(kind='barh', color='green')
    plt.xlabel('Number of Crimes')
    plt.ylabel('Location')
    plt.title('Top 10 Locations for Different Crime Types')
    plt.grid(axis='x')
    plt.show()

def plot_crime_comparison(df):
    df['month'] = df['date'].dt.month

    crime_comparison = df.groupby(['month', 'primary_type']).size().unstack()

    plt.figure(figsize=(12, 8))
    ax = crime_comparison.plot(kind='bar', stacked=True)
    
    plt.xlabel('Month')
    plt.ylabel('Number of Crimes')
    plt.title('Crime Comparison by Primary Type')
    plt.grid(axis='y')
    plt.xticks(rotation=0)

    # Add legend outside of the plot area and increase font size for better visibility
    plt.legend(title='Crime Type', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='medium')
    ax.legend_.get_title().set_fontsize('large')

    plt.tight_layout()
    plt.show()