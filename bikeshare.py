import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_input(input_str,input_type):
    """
    check the validity of user input.
    input_str: is the input of the user
    input_type: is the type of input: 1 = city, 2 = month, 3 = day
    """
    while True:
        input_read=input(input_str).lower()
        try:
            if input_read in ['chicago','new york city','washington'] and input_type == 1:
                break
            elif input_read in ['january','february','march','april','may','june','all'] and input_type ==2:
                break
            elif input_read in ['sunday','monday','tuesday','wednesday','thursday','friday','all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print("Sorry,your input should be: chicago,new york city or washington")
                if input_type == 2:
                    print("Sorry your input should be:january,february,march,april,may,june or all")
                if input_type == 3:
                    print("Sorry, your input should be: sunday, ...friday, saturday or all")
        except ValueError:
            print("Sorry,your input is wrong")
    return input_read

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Args:
        None.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = check_input("Would you like to see the data for chicago,new york city, or washington?\n",1)
    # TO DO: get user input for month (all, january, february, ... , june)
    month = check_input("Which Month (all, january, ...june)?\n",2)
    #get user input for day of week (all,monday,tuesday, ...sunday)
    day = check_input("Which Day? (all, monday, tuesday, ...sunday)\n",3)
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time']= pd.to_datetime(df['Start Time'])
    df['month']= df['Start Time'].dt.month
    df['day_of_week']= df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month)+1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day]
    
    return df
    
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"Most Common Month(1 = January,...,6 = June): {most_common_month}")

    # TO DO: display the most common day of week
    df['day_of_week']= df['Start Time'].dt.week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print(most_common_day_of_week)

    # TO DO: display the most common start hour
    df['hour']= df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
                          
    print(f"The most commonly used start station:{common_start_station}.")

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"\nThe most commonly used end station:{common_end_station}.")
    # TO DO: display most frequent combination of start station and end station trip
    df['Start To End']=df['Start Station'].str.cat(df['End Station'],sep='to')
    combo = df['Start To End'].mode()[0]
    
    print(f"\nThe most frequent combination of trips are from {combo}.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time =df['Trip Duration'].sum()
    minute,second = divmod(total_travel_time,60)
    hour,minute = divmod(minute,60)
    print(f"The total travel time is {hour}hours,{minute}minutes and {second}seconds.")
          
    # TO DO: display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())
    mins,sec = divmod(mean_travel_time,60)
    if mins > 60:
        hrs, mins = divmod(mins,60)
        print(f"\nThe mean travel time is {hrs}hours,{mins}minutes and {sec}seconds.")
    else:
        print(f"\nThe mean travel time is {mins}minutes and {sec}seconds.")
          
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"The types of users by number are given below:\n\n{user_types}")


    # TO DO: Display counts of gender
    try:
          gender = df['Gender'].value_counts()
          print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
          print("\nThere is no 'Gender' column in this file.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
          earliest = int(df['Birth Year'].min())
          recent = int(df['Birth Year'].max())
          common_year = int(df['Birth Year'].mode()[0])
          print(f"\nThe earliest year of birth:{earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth:{common_year}")
    except:
        print("There are no birth year details in this file.")
        print(f"\nThis took{(time.time() - start_time)}seconds.")
        print('-'*40)

def data(df):
    BIN_RESPONSE_LIST =['yes','no']
    rdata = ''
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nDo you want to see the raw data? Yes or No\n")
        print("\nAccepted responses: \nYes or yes\nNo or no")
        rdata =input().lower()
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nYou typed the wrong word.Please type Yes or No.")
            print("\nRestarting...\n")
    while rdata == 'yes':
        print("Do you want to see more? Yes or No")
        counter += 5
        rdata = input().lower()
        if rdata == "yes":
            print(df[counter:counter+5])
        elif rdata != "yes":
            break
    print('-'*40)
def main():
    while True:
        city,month,day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    
if __name__ == "__main__":
        main()
