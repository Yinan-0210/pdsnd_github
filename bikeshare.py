import time
import pandas as pd
import numpy as np

#city list
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city
    while True:
        city = input("Please enter the city you want to analyze (Chicago, New York City, Washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please choose from Chicago, New York City, or Washington.")
    
    # Get user input for month
    while True:
        month = input("Please enter the month you want to filter by (all, January, February, ..., June): ").lower()
        if month in MONTHS:
            break
        else:
            print("Invalid month. Please choose from all, January, February, March, April, May, or June.")
    
    # Get user input for day of week
    while True:
        day = input("Please enter the day of the week you want to filter by (all, Monday, Tuesday, ..., Sunday): ").lower()
        if day in DAYS:
            break
        else:
            print("Invalid day. Please choose from all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday.")
    
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load the data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        month = MONTHS.index(month)
        
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # Display the most common month
    common_month = df['month'].mode()[0]
    print(f"The most common month is: {MONTHS[common_month].title()}")
    
    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"The most common day of the week is: {common_day}")
    
    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f"The most common start hour is: {common_hour}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")
    
    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {common_end_station}")
    
    # Display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' -> ' + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print(f"The most frequent combination of start station and end station trip is: {common_trip}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time is: {total_travel_time} seconds")
    
    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The mean travel time is: {mean_travel_time:.2f} seconds")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:\n", user_types)
    
    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:\n", gender_counts)
    except KeyError:
        print("\nNo gender information available for this city.")
    
    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest birth year: {earliest_birth_year}")
        print(f"Most recent birth year: {most_recent_birth_year}")
        print(f"Most common birth year: {most_common_birth_year}")
    except KeyError:
        print("\nNo birth year information available for this city.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data upon user request."""
    
    current_row = 0
    while True:
        show_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no.\n").lower()
        if show_data != 'yes':
            break
        if current_row >= len(df):
            print("No more data to display.")
            break
        print(df.iloc[current_row:current_row+5])
        current_row += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Prompt the user to see raw data
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()