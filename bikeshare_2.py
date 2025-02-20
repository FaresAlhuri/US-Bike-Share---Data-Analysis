import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_input = input("Enter a city name (e.g. chicago, new york city or washington)\nCity:\t")
        if city_input in CITY_DATA:
            print("\n\nYou Entered:", city_input)
            break
        else:
            print("\nInvalid Input! Please try again:")


    # get user input for month (all, january, february, ... , june)
    while True:
        month_input = input("\n\nEnter a month name (e.g. all, January, February, March etc.)\nMonth:\t")
        if month_input in list(calendar.month_name[1:]) or month_input == 'all':
            print("\n\nYou Entered:", month_input)
            break
        else:
            print("\nInvalid Input! Please try again:")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        dayname = input("\n\nEnter the day of the week (e.g. all,  Monday, Tuesday etc.)\nDay:\t")
        if dayname in list(calendar.day_name) or dayname == 'all':
            print("\n\nYou Entered:", dayname)
            break
        else:
            print("\nInvalid Input! Please try again:")


    print('-'*40)
    return city_input, month_input, dayname


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
    filepath = CITY_DATA.get(city)

    if filepath:
        df = pd.read_csv(filepath)
    else:
        return None


     # Convert 'Start Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extract month and day of the week from 'Start Time'
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        # Convert month name to month number (e.g., January -> 1)
        month_num = list(calendar.month_name).index(month)
        df = df[df['Month'] == month_num]

    # Filter by day of the week if applicable
    if day != 'all':
        df = df[df['Day of Week'] == day]

    # Print the first few rows of the filtered DataFrame
    print(df.head())
    print('-'*40)
    print("\n")
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print(f"Month:\t{calendar.month_name[most_common_month]}\n")

    # display the most common day of week
    most_common_day = df['Day of Week'].mode()[0]
    print(f"Day:\t{most_common_day}\n")
    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    most_common_hour = df['Hour'].mode()[0]
    print(f"Most Frequent Hour of the Day:\t{most_common_hour}.00\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\n')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print(f"Popular Start Station:\t{start_station}\n")
    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print(f"Popular End Station:\t{end_station}\n")

    # display most frequent combination of start station and end station trip
    trip_count = df.groupby(['Start Station' , 'End Station']).size()

    frequent_trip = trip_count.idxmax()

    trip_count = trip_count.max()
    print(f"The Most Popular Trip was from '{frequent_trip[0]}' to '{frequent_trip[1]}' with {trip_count} trips.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\n')

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    df['Start Hour'] = df['Start Time'].dt.hour
    df['End Hour'] = df['End Time'].dt.hour
    df['Travel Time'] = df['End Hour'] - df['Start Hour']

    tot_time = df['Travel Time'].sum()
    print(f"Total Travel time:\t{tot_time} hours\n")
    # display mean travel time
    ave_time = df['Trip Duration'].mean()
    ave_time = ave_time /60
    ave_time = round(ave_time, 4)
    print(f"Average Travel time:\t{ave_time} minutes\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\n')

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count =  df['User Type'].value_counts()
    print(f"User Counts:\n{user_count}\n")

    # Display counts of gender
    if city != 'washington':
        gender_count =  df['Gender'].value_counts()
        print(f"User Counts:\n{gender_count}\n")

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        print(f"earliest Birth Year :   \t{df['Birth Year'].min()}\n")
        print(f"Most recent Birth Year :\t{df['Birth Year'].max()}\n")
        print(f"Most common Birth Year :\t{df['Birth Year'].mode()[0]}\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
