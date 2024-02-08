"""
extact numbers form a cvs file columns 5-9 starting at row 3
and save them in a list called 'numbers' -- sort the list
find the value x at wuch 6 values are greater than x.
print the value of x and the number of values greater than x
"""

import csv


# # MOVIES === Gradiant
# # movies G
# numbers = [92, 96, 89, 98, 19, 13, 94, 52, 95, 71, 60, 50, 27, 93, 97, 51, 75, 32, 30, 19, 10, 39, 26, 67, 54, 13, 71, 34, 64]
# sorted_numbers = sorted(numbers, reverse=True)
# print(sorted_numbers)

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

# ### CEREAL BAR
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
print(sorted_numbers, "\n")

########
### Give Tables
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




