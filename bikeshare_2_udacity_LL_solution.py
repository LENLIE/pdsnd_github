import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITY_LIST = ['chicago', 'new york', 'washington']

# Extracted from df:
# df['Start Time'].dt.strftime("%m/%y").unique().tolist()
# ['06/17', '05/17', '01/17', '03/17', '04/17', '02/17']
MONTH_LIST = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS_LIST = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('*'*80)
    print('Welcome, to this "Bikeshare Exploration Program"!')
    print('Let us explore some US bikeshare data!')
    print('*'*80)
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        try:
            city = str(input("\nWould you like to see data for 'Chicago', 'New York' or 'Washington'?\n").lower())
            if city.lower() in CITY_LIST:
                #df = pd.read_csv(CITY_DATA[city.lower()])
                break
            else:
                print(f"\nUnfortunately, there is not valid data for {city.title()}!")
                print("Please choose 'Chicago', 'New York' or 'Washington!")
        except ValueError:
            print("That is not a valid city.")

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input("\nPlease enter a 'month' or 'all' for all months.\n").lower())
            if month.lower() in MONTH_LIST or month.lower() == "all":
                break
            else:
                print(f"\nUnfortunately, there is not valid data for {month.title()}.")
                print("Please choose 'January', 'February', 'March', 'April', 'May' or 'June'!")

        except ValueError:
            print("That is not a valid month.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input("\nPlease enter a specific 'day' or 'all' for all days.\n").lower())
            if day.lower() in DAYS_LIST or day.lower() == "all":
                break
            else:
                print(f"\nUnfortunately, there is not valid data for {day.title()}.")
                print("Please choose 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'!")
        except ValueError:
            print("That is not a valid day.")

    print("\n")
    print('-'*100)
    print("Calculating 'Bikeshare' statistics for the following parameters:")
    print(f'City: {city.capitalize()} // Month: {month.capitalize()} // Day: {day.capitalize()}')
    print('-'*100)
    #return df
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from Start Time to create new column
    df['month'] = df['Start Time'].dt.month

    # extract weekday from Start Time to create new column
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # extract hour from Start Time to create new column
    df['hour'] = df['Start Time'].dt.hour

    #print(df['day_of_week'])


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTH_LIST.index(month.lower())+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\n')
    print('-'*100)
    print('Calculating The Most Frequent Times of Travel:')
    print('-'*100)

    start_time = time.time()

    # display the most common month
    #print(df[0:2][0:3])
    common_month = df["month"].mode()[0]
    common_month = MONTH_LIST[common_month-1]
    print(f"\nMost common month: '{common_month.capitalize()}'\n")

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"Most common day: '{common_day.capitalize()}'\n")

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print(f"Most common hour: '{common_hour}'\n")

    print("Calculation Time: %s seconds" % (time.time() - start_time))
    print("\n")


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('-'*100)
    print('Calculating The Most Popular Stations and Trip:')
    print('-'*100)
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    count_start_station = df["Start Station"].value_counts().max()
    print(f"\nStart Station: {common_start_station}")
    print(f"Total Count: {count_start_station}\n")


    # display most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    count_end_station = df["End Station"].value_counts().max()
    print(f"End Station: {common_end_station}")
    print(f"Total Count: {count_end_station}\n")


    # display most frequent combination of start station and end station trip
    df["start_end_combo"] = df["Start Station"] + " // " + df["End Station"]
    freq_combo = df["start_end_combo"].mode()[0]
    count_freq_combo = df["start_end_combo"].value_counts().max()

    #freq_meth = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)

    print(f"Start Station // End Station: {freq_combo}")
    print(f"Total Count: {count_freq_combo}")


    print("\nCalculation Time: %s seconds" % (time.time() - start_time))
    print("\n")


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('-'*100)
    print('Calculating Trip Duration:')
    print('-'*100)
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print(f"\nTotal Travel Time (Seconds): {total_travel_time}")

    # Copied from following source:
    # Source: https://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
    # total travel time conversion into days, hours, minutes, seconds
    tt = total_travel_time
    tt_days = divmod(tt, 86400)
    # days[0] = whole days and
    # days[1] = seconds remaining after those days
    tt_hours = divmod(tt_days[1], 3600)
    tt_minutes = divmod(tt_hours[1], 60)
    print(f"Total travel time (dd/hh/mm/ss): {tt_days[0]} Days, {tt_hours[0]} Hours, {tt_minutes[0]} Minutes, {tt_minutes[1]} Seconds")


    # display mean travel time
    avg_travel_time = df["Trip Duration"].mean()
    print(f"\nAverage Travel Time (Seconds): {avg_travel_time}")

    # Copied from following source:
    # Source: https://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
    # average travel time conversion into days, hours, minutes, seconds
    at = avg_travel_time
    at_days = divmod(at, 86400)
    # days[0] = whole days and
    # days[1] = seconds remaining after those days
    at_hours = divmod(at_days[1], 3600)
    at_minutes = divmod(at_hours[1], 60)
    print(f"Average Travel Time (dd/hh/mm/ss): {at_days[0]} Days, {at_hours[0]} Hours, {at_minutes[0]} Minutes, {at_minutes[1]} Seconds")


    print("\nCalculation Time: %s seconds" % (time.time() - start_time))
    print("\n")


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('-'*100)
    print('Calculating User Stats:')
    print('-'*100)
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"\nBreakdown of Users: \n{user_types}")

    # Display counts of gender

    if "Gender" in df:
        gender = df["Gender"].value_counts()
        print(f"\nBreakdown of gender: \n{gender}")
    else:
        print("\nBreakdown of Gender:")
        print("No gender data to share.")


    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        most_oldest_birth = df["Birth Year"].min()
        most_youngest_birth = df["Birth Year"].max()
        most_common_birth = df["Birth Year"].mode()[0]
        print(f"\nBreakdown of Year of Birth:")
        print(f"Most Oldest: {most_oldest_birth}")
        print(f"Most Youngest: {most_youngest_birth}")
        print(f"Most Common: {most_common_birth}")
    else:
        print("\nBreakdown of Year of Birth:")
        print("No birth data to share.")

    print("\nCalculation Time: %s seconds" % (time.time() - start_time))

def raw_data(df):
    """
    Displays raw data statistics based on user input
    """

    start = 0
    end = 5
    while True:
        raw_data = input("\nAre you interested to see some raw data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == "yes":
            print("\n")
            print('-'*100)
            print('Fetching Raw Data Statistics:')
            print('-'*100)
            start_time = time.time()

            print("\n")
            print(df[df.columns[0:-1]].iloc[start:end])
            print("\nCalculation Time: %s seconds" % (time.time() - start_time))
            start += 5
            end += 5
            
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter "yes" or "no".\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
