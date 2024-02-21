"""
extact numbers form a cvs file columns 5-9 starting at row 3
and save them in a list called 'numbers' -- sort the list
find the value x at wuch 6 values are greater than x.
print the value of x and the number of values greater than x
"""

import random
import csv

def Get_sorted_anime():
    Score = []
    Score= Score.sort()
    Episodes =[] 
    Episodes= Episodes.sort()	
    Ranked= []	
    Ranked = Ranked.sort()
    Popularity= []	
    Members = [36, 36, 46, 19, 24, 12, 19, 17, 42, 26, 43, 25, 19, 21, 48, 16, 47, 31, 28, 22, 56, 24, 45, 38, 35, 28, 51, 28, 35]
    Memebers = Members.sort()
    Favorites= []	
    Watching= []	
    Completed= []	
    OnHold= []	
    Dropped= []	
    Plan_to_Watch= []
    # Anime: G
    print("Anime: G - Members")
    Members=  [36, 36, 46, 19, 24, 12, 19, 17, 42, 26, 43, 25, 19, 21, 48, 16, 47, 31, 28, 22, 56, 24, 45, 38, 35, 28, 51, 28, 35]
    sorted_numbers = sorted(Members, reverse=True)
    print(sorted_numbers)

    # Anime: H
    print("\n\nAnime: H - Favorites")
    Favorites = [60, 30, 38, 20, 89, 38, 40, 61, 55, 51, 55, 57, 54, 44, 61, 23, 78, 47, 41, 69, 46, 18, 59, 36, 45, 28, 23, 61, 37]
    sorted_numbers = sorted(Favorites , reverse=True)
    print(sorted_numbers)

    # Anime: I
    print("\n\nAnime: I - Watching")
    Watching =[15, 27, 52, 28, 24, 66, 40, 55, 21, 47, 51, 43, 50, 58, 24, 41, 37, 23, 21, 42, 16, 43, 36, 32, 55, 69, 47, 42, 25]
    sorted_numbers = sorted(Watching, reverse=True)
    print(sorted_numbers)

    # Anime: J
    print("\n\nAnime: J - Completed")
    Completed = [43, 18, 25, 23, 36, 51, 14, 14, 38, 47, 46, 10, 15, 37, 41, 40, 52, 43, 58, 49, 28, 24, 33, 73, 38, 27, 25, 51, 23]
    sorted_numbers = sorted(Completed, reverse=True)
    print(sorted_numbers)

    # Anime: K
    print("\n\nAnime: K - On_Hold")
    On_Hold =  [29, 25, 50, 68, 28, 75, 26, 60, 18, 51, 57, 16, 12, 61, 28, 50, 54, 35, 64, 49, 20, 27, 65, 29, 31, 14, 58, 48, 37]
    sorted_numbers = sorted(On_Hold, reverse=True)
    print(sorted_numbers)
    
def Get_sorted_movies():
    # # movies G
    # numbers = [92, 96, 89, 98, 19, 13, 94, 52, 95, 71, 60, 50, 27, 93, 97, 51, 75, 32, 30, 19, 10, 39, 26, 67, 54, 13, 71, 34, 64]
    # numbers = sorted(numbers, reverse=True)
    # print(numbers)

    # # movies H
    # numbers = [36, 48, 44, 66, 25, 35, 47, 26, 25, 55, 30, 25, 15, 25, 45, 42, 35, 46, 35, 65, 35, 43, 13, 35, 27, 14, 52, 17, 32]
    # sorted_numbers = sorted(numbers, reverse=True)
    # print(sorted_numbers)

    # # movies I
    # numbers = [42, 41, 36, 39, 20, 12, 38, 28, 32, 34, 46, 30, 17, 27, 50, 30, 29, 47, 21, 14, 15, 43, 19, 32, 26, 16, 28, 24, 27]
    # sorted_numbers = sorted(numbers, reverse=True)
    # print(sorted_numbers)

    # # movies J
    # numbers = [43, 42, 49, 38, 28, 32, 35, 31, 25, 30, 55, 30, 10, 36, 41, 46, 39, 52, 32, 20, 34, 40, 35, 34, 37, 45, 33, 32, 31]
    # sorted_numbers = sorted(numbers, reverse=True)
    # print(sorted_numbers)

    # # movies K
    # numbers = [39, 51, 29, 46, 67, 75, 21, 55, 21, 33, 46, 15, 13, 63, 35, 26, 54, 28, 61, 31, 18, 11, 79, 69, 57, 78, 69, 51, 37]
    # sorted_numbers = sorted(numbers, reverse=True)
    # print(sorted_numbers)
    
    ########
    ### Give Tables
    # Movies G
    print("Movies: G- IMDB")
    IMDB = [79, 77, 78, 75, 55, 63, 69, 61, 23, 59, 60, 66, 52, 72, 41, 63, 78, 71, 64, 40, 46, 49, 69, 67, 73, 49, 66, 64, 50]
    sorted_numbers = sorted(IMDB, reverse=True)
    print(sorted_numbers)

    # Movies H
    print("\n\nMovies: H - Hulu")
    Hulu = [46, 48, 44, 46, 25, 35, 47, 26, 25, 55, 30, 25, 15, 45, 45, 42, 35, 46, 35, 65, 35, 43, 13, 35, 27, 14, 52, 17, 32]
    sorted_numbers = sorted(Hulu, reverse=True)
    print(sorted_numbers)

    # Movies I
    print("\n\nMovies: I- Film_Comment")
    Film_Comment = [42, 41, 36, 39, 20, 12, 38, 28, 32, 34, 46, 30, 17, 27, 50, 30, 29, 47, 21, 14, 15, 43, 19, 32, 26, 16, 28, 24, 27]
    sorted_numbers = sorted(Film_Comment, reverse=True)
    print(sorted_numbers)

    # Movies J
    print("\n\nMovies: J - Roger_Ebert")
    Roger_Ebert = [43, 42, 49, 38, 28, 32, 35, 31, 25, 30, 55, 30, 10, 36, 41, 46, 39, 52, 32, 20, 34, 40, 35, 34, 37, 45, 33, 32, 31]
    sorted_numbers = sorted(Roger_Ebert, reverse=True)
    print(sorted_numbers)

    # Movies K
    print("\n\nMovies: K - PluggedIn")
    PluggedIn = [39, 51, 29, 46, 67, 75, 21, 55, 21, 33, 46, 15, 13, 63, 35, 26, 54, 28, 61, 31, 18, 11, 79, 69, 57, 78, 69, 51, 37]
    sorted_numbers = sorted(PluggedIn, reverse=True)
    print(sorted_numbers, "\n")

# ### CEREAL BAR
def Get_sorted_cereal():
    # # cereal G
    # numbers = [24, 23, 21, 55, 31, 40, 30, 50, 22, 21, 22, 19, 23, 41, 51, 60, 47, 53, 21, 33, 20, 41, 31, 21, 39, 10, 16, 38, 32]
    # sorted_numbers = sorted(numbers, reverse=True)
    # print(sorted_numbers)

    # # cereal H
    # numbers = [18, 42, 22, 12, 14, 25, 43, 23, 34, 37, 47, 34, 18, 12, 24, 17, 15, 21, 21, 42, 38, 43, 12, 31, 31, 18, 21, 52, 43]
    # sorted_numbers = sorted(numbers, reverse=True)
    # print(sorted_numbers)

    # # cereal I
    # numbers = [29, 22, 13, 22, 27, 46, 17, 15, 18, 21, 49, 21, 12, 25, 22, 35, 26, 23, 32, 23, 38, 33, 37, 12, 22, 45, 24, 42, 32]
    # sorted_numbers = sorted(numbers, reverse=True)
    # print(sorted_numbers)

    # # cereal J
    # numbers = [35, 15, 25, 29, 22, 15, 80, 42, 56, 25, 35, 50, 46, 25, 32, 65, 32, 26, 35, 45, 26, 20, 52, 32, 22, 22, 32, 22, 22]
    # sorted_numbers = sorted(numbers, reverse=True)
    # print(sorted_numbers)

    # # cereal K
    # numbers = [34, 18, 23, 30, 58, 37, 42, 53, 40, 53, 20, 30, 16, 11, 41, 13, 68, 32, 37, 22, 10, 18, 42, 65, 36, 44, 33, 43, 36]
    # sorted_numbers = sorted(numbers, reverse=True)
    # print(sorted_numbers)

    ########
    ### Give Tables
    # Cereal: G
    print("Cereal: G - Fiber")
    Fiber = [24, 23, 21, 55, 31, 40, 30, 50, 22, 21, 22, 19, 23, 41, 51, 60, 47, 53, 21, 33, 20, 41, 31, 21, 39, 10, 16, 38, 32]
    sorted_numbers = sorted(Fiber, reverse=True)
    print(sorted_numbers)

    # Cereal: H
    print("\n\nCereal: H - Carbo")
    Carbo = [18, 42, 22, 12, 14, 25, 43, 23, 34, 37, 47, 34, 18, 12, 24, 17, 15, 21, 21, 42, 38, 43, 12, 31, 31, 18, 21, 52, 43]
    sorted_numbers = sorted(Carbo, reverse=True)
    print(sorted_numbers)

    # Cereal: I
    print("\n\nCereal: I - Sugars")
    Sugars = [29, 22, 13, 22, 27, 46, 17, 15, 18, 21, 59, 21, 12, 53, 22, 35, 26, 23, 32, 23, 38, 33, 37, 12, 22, 45, 24, 42, 32]
    sorted_numbers = sorted(Sugars, reverse=True)
    print(sorted_numbers)

    # Cereal: J
    print("\n\nCereal: J- Potassium")
    Potassium = [35, 15, 25, 29, 22, 15, 80, 42, 56, 25, 35, 50, 46, 25, 32, 65, 32, 26, 35, 45, 26, 20, 52, 32, 22, 22, 32, 22, 22]
    sorted_numbers = sorted(Potassium, reverse=True)
    print(sorted_numbers)

    # Cereal: K
    print("\n\nCereal: K - Score")
    Score = [34, 18, 23, 30, 58, 37, 42, 53, 40, 53, 20, 30, 16, 11, 41, 13, 68, 32, 37, 22, 10, 18, 42, 65, 36, 44, 33, 43, 36]
    sorted_numbers = sorted(Score, reverse=True)
    print(sorted_numbers, "\n")

def Get_sorted_candy():
    # Candy: G
    print("Candy: G - Nougat")
    Nougat= [15, 14, 17, 13, 30, 17, 17, 16, 33, 20, 19, 17, 27, 21, 15, 17, 27, 21, 19, 21, 24, 16, 21, 25, 26, 12, 17, 17, 19]
    sorted_numbers = sorted(Nougat, reverse=True)
    print(sorted_numbers)

    # Candy: H
    print("\n\nCandy: H - Hard")
    Hard= [51, 12, 34, 29, 17, 42, 58, 30, 47, 63, 30, 47, 29, 53, 27, 40, 53, 15, 58, 53, 35, 18, 43, 27, 24, 53, 30, 24, 53]
    sorted_numbers = sorted(Hard, reverse=True)
    print(sorted_numbers)

    # Candy: I
    print("\n\nCandy: I: Bar")
    Bar= [34, 27, 24, 34, 37, 31, 23, 20, 45, 24, 21, 34, 41, 31, 14, 32, 19, 13, 13, 19, 27, 33, 17, 22, 44, 21, 37, 23, 16]
    sorted_numbers = sorted(Bar, reverse=True)
    print(sorted_numbers)

    # Candy: J
    print("\n\nCandy: J: Pluribus")
    Pluribus= [63, 34, 17, 21, 46, 54, 28, 17, 36, 19, 12, 20, 24, 21, 26, 17, 32, 22, 64, 12, 10, 12, 45, 27, 37, 45, 54, 53, 57]
    sorted_numbers = sorted(Pluribus, reverse=True)
    print(sorted_numbers)

    # Candy: K
    print("\n\nCandy: K: SugarPercentage")
    SugarPercent= [22, 32, 60, 55, 33, 27, 70, 31, 84, 70, 35, 28, 70, 50, 30, 20, 27, 17, 55, 29, 14, 13, 38, 32, 39, 32, 23, 33, 49]
    sorted_numbers = sorted(SugarPercent, reverse=True)
    print(sorted_numbers , "\n")


def top_5_diff(members):
    top_5 = members[:5]
    print("Top 5: ", top_5)
    return (members[4] - members[5] > 1)

def diff_6_7(members):
    top_5 = members[:6]
    ancher = members[5] - members[6] + members[6] - 2
    print("Top 6: ", top_5, "Count the number of entries exceeding the value: ",ancher, ",next num",members[6] )
    return (ancher > members[6] )


def get_mid_value(members):
    index = len(members) // 2
    print("the middle number is: ", members[index])
    return members[index]

def diff_7_8(members):
    top_5 = members[:7]
    ancher = members[6] - members[7] + members[7] - 2
    print("Top 7: ", top_5, "Count the number of entries exceeding the value: ",ancher, ",next num",members[7] )
    return (ancher > members[7] )

def diff_8_9(members):
    top_5 = members[:8]
    ancher = members[7] - members[8] + members[8] - 2
    print("Top 8: ", top_5, "Count the number of entries exceeding the value: ",ancher, ",next num",members[8] )
    return (ancher > members[8] )

def approx_avg(members):
    approx_avg = ((members[0]) + members[-1]) // 2 
    for i in members:
        if i == approx_avg:
            print("Approximate Average:", approx_avg, ", maximum value:",members[0], ", minimum value:", members[-1])
            return True, "Approximate Average is in list"
    print("Approximate Average: not in list ", approx_avg)
    return  False,"Approximate Average is not in list"
   

def get_sorted_and_refined_anime():
    anime_table_columns_5_to_9 = {
        "Members": [60, 56, 53, 51, 50, 48, 45, 40, 37, 36, 36, 35, 35, 31, 28, 28, 28, 26, 25, 24, 24, 22, 21, 19, 19, 19, 17, 16, 12],
        "Favorites": [89, 80, 78, 75, 73, 68, 65, 60, 57, 55, 55, 54, 50, 47, 46, 45, 44, 41, 40, 38, 38, 37, 36, 30, 28, 23, 23, 20, 11] ,
        "Watching": [71, 70, 68, 65, 62, 59, 56, 53, 47, 47, 43, 43, 42, 42, 41, 40, 37, 36, 32, 28, 27, 25, 24, 24, 23, 21, 21, 16, 15],
        "Completed":  [74, 73, 70, 65, 63, 59, 56, 45, 42, 41, 41, 40, 38, 38, 37, 36, 33, 28, 27, 25, 25, 24, 23, 23, 18, 15, 14, 14, 10],
        "On_Hold": [75, 73, 71, 70, 68, 65, 62, 59, 52, 51, 50, 50, 49, 45, 37, 35, 31, 29, 29, 28, 28, 27, 26, 25, 20, 18, 17, 16, 15]
    }
    return anime_table_columns_5_to_9

def get_sorted_candy_data():
    candy_data = {
    "G - Nougat": [36, 33, 30, 30, 28, 26, 24, 21, 21, 21, 21, 20, 19, 19, 19, 17, 17, 17, 17, 17, 17, 17, 16, 16, 15, 15, 14, 13, 12],
    "H - Hard": [64, 63, 62, 61, 60, 57, 54, 51, 48, 47, 47, 43, 42, 40, 38, 34, 30, 30, 30, 29, 29, 27, 27, 24, 24, 18, 17, 15, 12],
    "I - Bar": [48, 47, 42, 41, 40, 37, 34, 31, 29, 27, 27, 27, 27, 27, 24, 24, 23, 23, 22, 21, 21, 20, 19, 19, 17, 16, 14, 13, 14],
    "J - Pluribus": [64, 63, 62, 61, 60, 57, 54, 50, 48, 37, 34, 34, 32, 28, 27, 26, 24, 22, 21, 21, 20, 19, 17, 17, 17, 12, 12, 12, 10],
    "K - SugarPercentage": [84, 83, 82, 81, 80, 75, 70, 65, 48, 39, 37, 35, 33, 33, 32, 32, 32, 31, 30, 29, 28, 27, 27, 23, 22, 20, 17, 14, 12]
    }
    return candy_data

def get_sorted_cereal_data():
    cereal_data = {
    "G - Fiber": [60, 55, 54, 53, 51, 48, 45, 40, 39, 39, 35, 33, 32, 31, 31, 30, 24, 23, 23, 22, 22, 21, 21, 21, 21, 20, 19, 16, 10],
    "H - Carbo": [56, 54, 53, 53, 52, 48, 45, 40, 35, 34, 34, 31, 31, 25, 24, 23, 22, 21, 21, 21, 18, 18, 18, 17, 15, 14, 12, 12, 12],
    "I - Sugars": [60, 57, 56, 55, 52, 49, 45, 41, 36, 32, 32, 29, 27, 26, 24, 23, 23, 22, 22, 22, 22, 21, 21, 18, 17, 15, 13, 12, 12],
    "J - Potassium": [80, 76, 76, 72, 70, 67, 55, 47, 39, 35, 35, 32, 32, 32, 32, 29, 26, 26, 25, 25, 25, 22, 22, 22, 22, 22, 20, 15, 15],
    "K - Score": [68, 65, 58, 53, 53, 49, 45, 41, 40, 40, 40, 39, 37, 36, 36, 34, 33, 32, 30, 30, 23, 22, 20, 18, 18, 16, 13, 11, 10]
    }
    return cereal_data

def get_sorted_movie_data():
    movies_data = {
    "G - IMDB": [90, 88, 87, 86, 85, 80, 75, 72, 68, 68, 67, 66, 66, 64, 64, 63, 63, 61, 60, 59, 56, 52, 50, 49, 49, 46, 41, 40, 22],
    "H - Hulu": [64, 60, 52, 48, 47, 46, 46, 46, 45, 45, 44, 43, 42, 38, 35, 35, 35, 35, 32, 30, 27, 26, 25, 25, 25, 17, 15, 14, 12],
    "I - Film_Comment": [50, 48, 47, 46, 45, 42, 39, 36, 33, 33, 32, 32, 31, 30, 29, 28, 28, 27, 27, 26, 24, 21, 20, 19, 17, 16, 15, 14, 12],
    "J - Roger_Ebert": [56, 55, 54, 53, 52, 48, 45, 43, 40, 39, 38, 37, 36, 35, 35, 34, 34, 33, 32, 32, 32, 31, 31, 30, 30, 28, 25, 20, 10],
    "K - PluggedIn": [80, 79, 78, 77, 76, 71, 68, 65, 57, 55, 54, 51, 51, 48, 45, 39, 37, 35, 33, 31, 29, 28, 26, 21, 21, 18, 15, 13, 10]
    }
    return movies_data

def to_qualify(table: dict):
    """
    need: 6,7,8 - gaps of 2 or more for each in each (Count the number of entries in the Y Column that exceed a value of X. )
    have a noticable gap: 3+ between 6th and 5th (Top 5)

    """
    # need is top 5 diff from 5th to 6th
    # diff from 6th to 7th
    # diff from 7th to 8th
    # approx average easy to calculate (maximum+ minimum)/2 - whole number - number needs to be in list
    for anime, values in table.items():
        print(f"Anime: {anime}", values)
        print("Top 5 diff: ", top_5_diff(values))
        print("Diff 6-7: ", diff_6_7(values))
        print("Diff 7-8: ", diff_7_8(values))
        print("Approx average: ", approx_avg(values))
        get_mid_value(values)
        print("\n")

def validate_data(data: dict):
    # Iterate through each key-value pair in the data dictionary
    for key, value in data.items():
        if not isinstance(value, list):
            print(f"Error: Value for key '{key}' is not a list.")
            return False
        
        if len(value) != len(data[list(data.keys())[0]]):
            print(f"Error: Length of data for key '{key}' does not match other data lengths.")
            return False

        if not all(isinstance(item, int) for item in value):
            print(f"Error: Values for key '{key}' contain non-integer elements.")
            return False
        
        if not all(item >= 0 for item in value):
            print(f"Error: Values for key '{key}' contain negative numbers.")
            return False
        
        # Additional checks can be added here
        
    return True

def randomize_dictionary_values(my_dict: dict):
    # Iterate through each key-value pair in the dictionary
    for key, value in my_dict.items():
        # Check if the value is a list
        if isinstance(value, list):
            # Shuffle the list in place
            random.shuffle(value)
            # Update the dictionary item
            my_dict[key] = value
        else:
            print(f"Value for key '{key}' is not a list and will not be shuffled.")

    # Print out the modified dictionary nicely
    print("Randomized Dictionary:")
    for key, value in my_dict.items():
        print(f"{key}: {value}")



# candy_data = get_sorted_candy_data()
# cereal_data = get_sorted_cereal_data()
# anime_data = get_sorted_and_refined_anime()
# movies_data = get_sorted_movie_data()

# validate_data(get_sorted_candy_data())
# validate_data(get_sorted_cereal_data())
# validate_data(get_sorted_movie_data())
to_qualify(get_sorted_and_refined_anime())

# to_qualify(get_sorted_movie_data())
# randomized_anime= randomize_dictionary_values(candy_data)
# members = [19, 35, 26, 16, 19, 40, 28, 50, 21, 24, 60, 31, 51, 12, 36, 56, 48, 24, 19, 36, 35, 22, 28, 17, 53, 28, 37, 45, 25]
# watching = [62, 56, 24, 24, 21, 53, 32, 23, 21, 47, 47, 59, 16, 28, 70, 71, 36, 15, 42, 43, 40, 25, 37, 43, 42, 68, 65, 27, 41]
# Generate a list with 0.9 correlation coefficient
# correlated_list = [int(0.9 * x) for x in watching]
# print(correlated_list)



# randomized_cereal= randomize_dictionary_values(cereal_data)
# randomized_candy= randomize_dictionary_values(candy_get)
# randomized_movies= randomize_dictionary_values(movies_data)

# validate_data(movies_data)






