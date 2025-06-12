# calgary_dogs.py
# Conner Castle 
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.
import numpy as np 
import pandas as pd 

def get_user_input(data):
    """
    Handles input from a user, if the input is not in the dataset it raises an error. 

    Args: 
        data (pandas dataframe): The dataset with which to check if the user input is a part of. 

    Returns: 
        String: The uppercase of the user input, confirmed to be within the dataset. 
    """
    user_breed = input("Please input a dog breed to gather information about: ")
    if (user_breed.upper() not in data['Breed'].values):
        raise KeyError("Dog breed not found in the data. Please try again.")
    return user_breed.upper()


def main():
    """Controls input repeat loop, data calculation, and prints to console."""

    # Import data here
    pd.set_option("display.max_rows",None)
    data = pd.read_excel(r"CalgaryDogBreeds.xlsx") # Command for reading data from file into dataframe 
    print("ENSF 692 Dogs of Calgary")

    # User input stage
    # This is used as my repeater for incorrect input, as long as there is an error it will repeat indefinitely 
    while True:
        try:
            user_breed = get_user_input(data) 
        except KeyError as e:
            print(e)
        else: 
            break

    
    # Data anaylsis stage 
    user_selected_breed = data[data['Breed'] == user_breed] # Masking operation 
    
    # Find years where dog breed was in top 100 dog breeds 
    years_max = user_selected_breed['Year'].unique() 
    print(f'The {user_breed} was found in the top breeds for years: {years_max}.') 

    # Calculate and print the total 
    # number of registrations of the selected breed found in the dataset 
    print(f'There have been {user_selected_breed['Total'].sum()} {user_breed} dogs registered total.') 

    # Calculate and print the percentage of selected breed 
    # registrations out of the total percentage for each year (2021, 2022, 2023) 
    multi_data = data.set_index(['Breed','Year']) # Creation of multi index hierarchical data 
    total_registrations = multi_data.groupby(['Year']).aggregate('sum') # Groupby command 

    # Section to munge data and add individual percentages based on total reg that year 
    total_registrations = total_registrations.drop(['Month'],axis=1) 
    data_totals_added = pd.merge(multi_data,total_registrations,right_index=True,left_index=True,suffixes=['_breed','_year'])
    data_totals_added['Percent'] = data_totals_added['Total_breed']/data_totals_added['Total_year']*100
    
    # Section includes pandas computation commands 
    print(f'The {user_breed} was {data_totals_added.loc[user_breed,2021]['Percent'].sum()}% of top breeds in 2021.') 
    print(f'The {user_breed} was {data_totals_added.loc[user_breed,2022]['Percent'].sum()}% of top breeds in 2022.')
    print(f'The {user_breed} was {data_totals_added.loc[user_breed,2023]['Percent'].sum()}% of top breeds in 2023.')

    # Calculate and print the percentage of selected breed 
    # registrations out of the total three-year percentage 
    user_selected_total_percent = data_totals_added.loc[user_breed]['Total_breed'].sum()/total_registrations['Total'].sum()*100 
    print(f'The {user_breed} was {user_selected_total_percent} of top breeds across all years.')

    # Find and print the months that were most popular 
    # for the selected breed registrations. Print all months that tie
    idx = pd.IndexSlice
    user_data = data.set_index(['Breed']) 
    months = user_data.loc[idx[user_breed],idx[:]].groupby('Month').count()['Year']>1 # Use of index slice object 
    print(f'Most popular month(s) for {user_breed} dogs: ',end='')
    print(*months[months == True].index) # Masking to output anything that repeats 
    
if __name__ == '__main__':
    main()
