<<<<<<< HEAD
import datetime
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }
#use the boolean variable continue_code in case the user changes their mind and wants to "quit"
continue_code = True
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n(Input is not case sensitive)')
    # get user input for city (Chicago, New York, Washington). HINT: Use a while loop to handle invalid inputs
    # add global boolean variable continue_code to decide whether to continue with the report or not.
    global continue_code
    city=""
    month=""
    day=""
    while True:
        city = input('Enter the name of the city to analyze(Chicago, New York, Washington) or Quit to exit:').title()
        if city in ('Chicago', 'New York', 'Washington'):
            break
        elif city.title() in ('Quit','Q'):
            continue_code = False
            return "No city selected","No month selected", "No day selected"

        else:
            continue

    # get user input for month (All, January, February, ... , June)
    while True:
        #try:
        #convert all inputs to title case
        month = input('Please enter a valid month name, fron January to June or all(All, January, February, ... , June) or "Quit" to exit:').title()
        if month in ("All", "January", "February", "March", "April", "May","June"):
            break
        elif city.title() in ('Quit','Q'):
            return city,"No month selected", "No day selected"
            continue_code = False
        else:
            continue

    while True:
        #try:
        day = input('Please enter a valid month name, fron Sunday to Monday or all(All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) or Quit:').title()
        if day in ("All", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"):
            break
        elif city.title() in ('Quit','Q'):
            return city,month, "No day selected"
            continue_code = False
        else:
            continue

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df[ "Start Time"].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = datetime.datetime.now()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = months[month-1]
    print('Most popular month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nMost popular day:', popular_day)

    # display the most common start hour
    ## extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    ## find the most popular hour
    popular_hour = df['hour'].mode()[0]
    #use the formatting below to convert the integer hour to am or pm time format
    formated_populat_hour = '{:02d}:00{}'.format((popular_hour-1)%12+1,'AM' if popular_hour < 12 else 'PM')
    print('\nMost Popular Hour:', formated_populat_hour)

    print("\nThis took %s seconds." % (datetime.datetime.now() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = datetime.datetime.now()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost popular end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    #create a new column in df with the combination of start and end stations
    df['start_end_combination'] = df['Start Station'] + ' - ' + df['End Station']
    #use mode function to find the most common start-end station combo
    popular_station_combo = df['start_end_combination'].mode()[0]
    print('\nMost frequent combination of start station and end station trip:', popular_station_combo)

    print("\nThis took %s seconds." % (datetime.datetime.now() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = datetime.datetime.now()

    #Convert End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # display total travel time
    df['trip_time'] =  df['End Time'] - df['Start Time']
    total_time = df['trip_time'].sum()
    print('Total travel time:', total_time)

    # display mean travel time
    mean_time = df['trip_time'].mean()
    print( "\nMean travel time: %s" % str(mean_time).split('.')[0] )


    print("\nThis took %s seconds." % (datetime.datetime.now() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = datetime.datetime.now()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print ("User Type Counts:",user_types.to_string())

    # Display counts of gender
    if city != 'Washington':
        Gender = df["Gender"].value_counts()
        print ("\nGender Counts:",Gender.to_string())


    # Display earliest, most recent, and most common year of birth
    if city != 'Washington':
        earliest_dob = df["Birth Year"].min()
        most_recent_dob = df["Birth Year"].max()
        most_common_dob = df['Birth Year'].mode()[0]
        print ("\nEarliest year of birth:\n",int(earliest_dob))
        print ("\nMost recent year of birth:\n",int(most_recent_dob))
        print ("\nMost common year of birth:\n",int(most_common_dob))

    print("\nThis took %s seconds." % (datetime.datetime.now() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ Ask user if they want to see 5 lines of raw data
        Continue to ask for subsequent 5 lines until user
        says the no"""
    df= df.rename(columns={df.columns[0]:'id'})
    i=0
#convert the user input to lower case using lower() function

    raw = input('\nWould you like to see the first 5 rows of the data? Enter yes or no?:\n').lower()
    pd.set_option('display.max_columns',200)
    while True:
        if raw in ('no','n'):
            break
        elif raw in ('yes','ye','y'):
            print('\nData shown reflects any filters previously applied to the original dataset...\n')
            print(df[i:i+5].head())
            raw = input('\nWould you like to see the next 5 rows of the data? Enter yes or no?:\n').lower() # TO DO: convert the user input to lower case using lower() function
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
    global continue_code
    while True:
        city, month, day = get_filters()
        if continue_code == True:
            df = load_data(city, month, day)
            df_all = load_data(city, "All", "All")
        if continue_code == True:
            time_stats(df_all)
        if continue_code == True:
            station_stats(df)
        if continue_code == True:
            trip_duration_stats(df)
        if continue_code == True:
            user_stats(df,city)
        if continue_code == True:
            display_raw_data(df)
        if continue_code == True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() not in ('yes','ye','y'):
                break
        else:
            break


if __name__ == "__main__":
	main()
||||||| 733a6c1
=======
import datetime
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }
#use the boolean variable continue_code in case the user changes their mind and wants to "quit"
continue_code = True
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n(Input is not case sensitive)')
    # get user input for city (Chicago, New York, Washington). HINT: Use a while loop to handle invalid inputs
    global continue_code
    city=""
    month=""
    day=""
    while True:
        city = input('Enter the name of the city to analyze(Chicago, New York, Washington) or Quit to exit:').title()
        if city in ('Chicago', 'New York', 'Washington'):
            break
        elif city.title() in ('Quit','Q'):
            continue_code = False
            return "No city selected","No month selected", "No day selected"

        else:
            continue

    # get user input for month (All, January, February, ... , June)
    while True:
        #try:
        #convert all inputs to title case
        month = input('Please enter a valid month name, fron January to June or all(All, January, February, ... , June) or "Quit" to exit:').title()
        if month in ("All", "January", "February", "March", "April", "May","June"):
            break
        elif city.title() in ('Quit','Q'):
            return city,"No month selected", "No day selected"
            continue_code = False
        else:
            continue

    while True:
        #try:
        day = input('Please enter a valid month name, fron Sunday to Monday or all(All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) or Quit:').title()
        if day in ("All", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday") or 
           day in ("A","S","T","W","Th","F","S","Su"):  #added ability to enter abbreviations for days of the week
            break
        elif city.title() in ('Quit','Q'):
            return city,month, "No day selected"
            continue_code = False
        else:
            continue

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df[ "Start Time"].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = datetime.datetime.now()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = months[month-1]
    print('Most popular month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nMost popular day:', popular_day)

    # display the most common start hour
    ## extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    ## find the most popular hour
    popular_hour = df['hour'].mode()[0]
    #use the formatting below to convert the integer hour to am or pm time format
    formated_populat_hour = '{:02d}:00{}'.format((popular_hour-1)%12+1,'AM' if popular_hour < 12 else 'PM')
    print('\nMost Popular Hour:', formated_populat_hour)

    print("\nThis took %s seconds." % (datetime.datetime.now() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = datetime.datetime.now()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost popular end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    #create a new column in df with the combination of start and end stations
    df['start_end_combination'] = df['Start Station'] + ' - ' + df['End Station']
    #use mode function to find the most common start-end station combo
    popular_station_combo = df['start_end_combination'].mode()[0]
    print('\nMost frequent combination of start station and end station trip:', popular_station_combo)

    print("\nThis took %s seconds." % (datetime.datetime.now() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = datetime.datetime.now()

    #Convert End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # display total travel time
    df['trip_time'] =  df['End Time'] - df['Start Time']
    total_time = df['trip_time'].sum()
    print('Total travel time:', total_time)

    # display mean travel time
    mean_time = df['trip_time'].mean()
    print( "\nMean travel time: %s" % str(mean_time).split('.')[0] )


    print("\nThis took %s seconds." % (datetime.datetime.now() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = datetime.datetime.now()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print ("User Type Counts:",user_types.to_string())

    # Display counts of gender
    if city != 'Washington':
        Gender = df["Gender"].value_counts()
        print ("\nGender Counts:",Gender.to_string())


    # Display earliest, most recent, and most common year of birth
    if city != 'Washington':
        earliest_dob = df["Birth Year"].min()
        most_recent_dob = df["Birth Year"].max()
        most_common_dob = df['Birth Year'].mode()[0]
        print ("\nEarliest year of birth:\n",int(earliest_dob))
        print ("\nMost recent year of birth:\n",int(most_recent_dob))
        print ("\nMost common year of birth:\n",int(most_common_dob))

    print("\nThis took %s seconds." % (datetime.datetime.now() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ Ask user if they want to see 5 lines of raw data
        Continue to ask for subsequent 5 lines until user
        says the no"""
    df= df.rename(columns={df.columns[0]:'id'})
    i=0
#convert the user input to lower case using lower() function

    raw = input('\nWould you like to see the first 5 rows of the data? Enter yes or no?:\n').lower()
    pd.set_option('display.max_columns',200)
    while True:
        if raw in ('no','n'):
            break
        elif raw in ('yes','ye','y'):
            print('\nData shown reflects any filters previously applied to the original dataset...\n')
            print(df[i:i+5].head())
            raw = input('\nWould you like to see the next 5 rows of the data? Enter yes or no?:\n').lower() # TO DO: convert the user input to lower case using lower() function
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
    global continue_code
    while True:
        city, month, day = get_filters()
        if continue_code == True:
            df = load_data(city, month, day)
            df_all = load_data(city, "All", "All")
        if continue_code == True:
            time_stats(df_all)
        if continue_code == True:
            station_stats(df)
        if continue_code == True:
            trip_duration_stats(df)
        if continue_code == True:
            user_stats(df,city)
        if continue_code == True:
            display_raw_data(df)
        if continue_code == True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() not in ('yes','ye','y'):
                break
        else:
            break


if __name__ == "__main__":
	main()
>>>>>>> refactoring
