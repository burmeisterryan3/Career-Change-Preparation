import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
"
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    prompt = "\nFrom which city would you like to explore data?\n" \
             + "Type \"Chicago\", \"New York City\", or \"Washington\".\n"
    error_prompt = "\nInvalid city name. Please select \"chicago\", \"new york city\"" \
                     + ", or \"washington\".\nFrom which of these cities would you " \
                     + "like to explore data?\n"
    cities = CITY_DATA.keys()

    city = input(prompt).lower()
    while city not in cities:
        city = input(error_prompt).lower()

    # get user input for month (all, january, february, ... , june)
    prompt = "\nFrom which month would you like to explore data? Select \"all\" if " \
             + "you would like to view data for all months.\n"
    error_prompt = "\nInvalid month. Please select a month between January and June " \
                    + "or select \"all\" if you would like to view data for all " \
                    + "months.\nFrom which of these months would you like to select " \
                    + "data?\n"
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    month = input(prompt).lower()
    while month not in months:
        month = input(error_prompt).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    prompt = "\nFrom which day of the week would you like to explore data? Select " \
             + "\"all\" if you would like to view data for all days of the " \
             + "week.\n"
    error_prompt = "\nInvalid day. Please select a day of the week, e.g. Monday or " \
                   + "Thursday, or select \"all\" if you would like to view data for " \
                   + "all days of the week.\nFrom which day of the week would you " \
                   + "like to select data?\n"
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    day = input(prompt).lower()
    while day.lower() not in days:
        day = input(error_prompt).lower()

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()], parse_dates=["Start Time", "End Time"])
    df.rename(columns={'Unnamed: 0': ''}, inplace=True)

    # convert the Start Time column to datetime
    # df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() # OR dayofweek for number
    # df['day_of_week'] = df['Start Time'].dt.day_of_week

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        # days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        # df = df[df['day_of_week'] == days_of_week.index(day.title())]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[df['month'].mode()[0] - 1]
    print('Most Common Start Month:', popular_month.title())

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Start Day:', popular_day)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df["Start Time"].dt.hour
    # find the most common hour (from 0 to 23)
    popular_hour =df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_sstation = df['Start Station'].mode()[0]
    print('Most Common Start Station:', popular_sstation)

    # display most commonly used end station
    popular_estation = df['End Station'].mode()[0]
    print('Most Common End Station:', popular_estation)

    # display most frequent combination of start station and end station trip
    popular_station_combo = df.value_counts(subset=['Start Station',
                                                    'End Station']).index[0]
    print('Most Common Start and End Station Combination:\n'
          + '     Start Station: {}\n'.format(popular_station_combo[0])
          + '     End Station: {}\n'.format(popular_station_combo[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_seconds = df['Trip Duration'].sum()
    mm, ss = divmod(total_seconds, 60)
    hh, mm = divmod(mm, 60)
    print('Total Travel Time: {} hours, {} minutes, {} seconds'.format(hh, mm, round(ss)))

    # display mean travel time
    mean_seconds = df['Trip Duration'].mean()
    mm, ss = divmod(mean_seconds, 60)
    print('Mean Travel Time: {} minutes, {} seconds'.format(mm, round(ss)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    user_types = user_type_counts.index
    print("Counts by User Type:")
    for i in range(user_type_counts.size):
        print("    {}: {}".format(user_types[i], user_type_counts[i]))
    print()

    # Display counts of gender
    user_gender_counts = df['Gender'].value_counts()
    user_genders = user_gender_counts.index
    print("Counts by User Gender:")
    for i in range(user_gender_counts.size):
        print("    {}: {}".format(user_genders[i], user_gender_counts[i]))
    print("    Unspecified: {}\n".format(df['Gender'].isna().sum()))
    print()

    # Display earliest, most recent, and most common year of birth
    print("Earliest Birth Year: {}".format(int(df['Birth Year'].min())))
    print("Most Recent Birth Year: {}".format(int(df['Birth Year'].max())))
    print("Most Common Birth Year: {}".format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_ind_trip_data(df):
    """Displays five trips until the user wants."""

    current_row = 0
    num_trips = df.shape[0]
    prompt = '\nWould you like to see individual trip data? Type "yes" or "no".\n'

    while True:
        display_ind_trip = input(prompt)
        if display_ind_trip == "yes":
            for row in range(current_row, current_row + 5):
                print(df.iloc[row].to_string() + '\n')
            current_row += 5

            # If current_row exices number of rows, would cause error. Stop loop.
            if current_row > num_trips:
                print('All trips have been displayed!\n')
                break
        elif display_ind_trip == "no":
            break
        else:
            print("Invalid input!\n")

def main():
    print('\nHello! Let\'s explore some US bikeshare data!')

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_ind_trip_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\n\nGood bye!\n')
            break


if __name__ == "__main__":
	main()
