"""
Find the Treasure Program
"""
import sys


# returns how many characters are in the file - BUT WHY?
def hide_treasure(file_path):
    """
                                --::-- Hide the Treasure --::--

    a. Create a file containing all numbers from 0, inclusive, to 9, inclusive.
    b. Each number is repeated for a random number of times (at least 1, at most 20).
    c. Once the program reaches the last "9", it will write "TREASURE".
    d. Then, the program will write the numbers in reverse order, from 9 to 0, for random repetitions.

    :param file_path: path to the "treasure" file
    :return: True
    """
    import random

    # list of numbers that MUST be included in the file
    # NO other numbers can be included in the file
    number_selection = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    min_repetitions = 1  # minimum number of times a number must be repeated in the file
    max_repetitions = 20  # maximum number of times a number can be repeated in the file

    with open(file_path, 'w') as file:  # 'write' permissions
        for num in number_selection:  # iterate through the list of numbers
            reps = random.randint(min_repetitions, max_repetitions)  # generate random number of repetitions
            file.write((str(num) * reps))  # write the number to the file the number of times generated

        file.write('TREASURE')  # write the word "TREASURE" to the file after the last number 9

        for num in number_selection[::-1]:  # iterate through the list of numbers in reverse order
            reps = random.randint(min_repetitions, max_repetitions)  # generate random number of repetitions again
            file.write(str(num) * reps)  # write the number to the file the number of times generated

    return True  # return True if the file was successfully created


# returns number of attempts made by user
def find_treasure(file_path):
    """
                                        --::-- Find the Treasure --::--

    a. Ask for user input to move right [1] or left [2].
    b. If the user inputs any other number, the program will ask for a valid input.
    c. The program will keep asking for input until the user finds the treasure.
    d. If the user moves too far to the right or left, the program will notify the user and ask for a valid input.

    :param file_path: path to where the treasure is hidden
    :return:
    """
    """ -------------------------------------- initialize variables --------------------------------------------- """
    # 'rb' permissions in order to perform nonzero cur-relative seeks and keep cursor in position
    file = open(file_path, "rb")

    # directional words are more readable than numbers
    right = 1  # move right
    left = 2  # move left

    guess_attempts = 0  # counts how many attempts the user has made at guessing the treasure's location
    treasure = 'TREASURE'  # used to compare letters of string to characters in the treasure file
    flag = False  # used to determine if the user has found the treasure

    welcome_message = '--::-- WELCOME TO THE TREASURE HUNT --::--\nLet\'s see if you can find the treasure!\n'

    is_treasure = 'Aye-aye, Captain! We found the TREASURE!'
    is_not_treasure = 'Argh... Keep lookin\' for that damn treasure...'
    """ --------------------------------------------------------------------------------------------------------- """
    print(welcome_message)

    while True:
        try:
            direction = int(input('Type a digit to move --:-- [Right: 1] [Left: 2]:\n'))

            if direction != right and direction != left:  # verify that direction of movement is valid
                print('Invalid input. Please type 1 or 2.')
                continue

            steps = int(input('How many times would you like to move (type a digit)?\n'))

        except ValueError:
            print('Invalid input. Please type a digit.')
            continue

        guess_attempts += 1  # increment guess attempts by 1 every time the user makes a guess

        try:
            if direction == right:
                file.seek(steps, 1)  # number from input relative to current position (to move right)
            else:  # direction == left:
                file.seek((steps * -1), 1)  # negative number from input relative to current position (to move left)
        except OSError:
            print('Oh-oh! You moved too far left. Please try again from where you stopped...')
            continue

        char = (file.read(1)).decode("utf-8")  # this moves cursor by 1 character forwards (to the right)
        file.seek(-1, 1)  # this moves cursor by 1 character backwards (to the left) to maintain actual position

        for letter in treasure:
            if letter == char:
                flag = True  # if the character is part of the word "TREASURE", set flag to True

        if flag:  # == true
            print(f'You just landed on... \n{char}!'  # print the character the user landed on
                  f'\n{is_treasure}'  # print the message that the user found the treasure
                  f'\nNumber of Guesses: {guess_attempts}'  # print the number of guesses the user made
                  f'\nCursor Position: {file.tell()}')  # print the cursor's position in the file
            break

        elif char == '':
            print('Oh-oh! You moved too far right. Please move left...')
            file.seek((steps * -1) + 1, 1)  # move cursor back to where it was before the user moved too far right

        else:  # if not in treasure
            print(f'You landed on... \n{char}.'
                  f'\n{is_not_treasure}'  # print the message that the user did not find the treasure
                  f'\nNumber of Guesses: {guess_attempts}')

    file.close()
    return guess_attempts  # return the number of attempts the user made at guessing the treasure's location


# separate csv columns into lists for iteration
# Server to later refactor the order of the records by lowest number of attempts
def columns_to_lists(file_path):
    """
                            --::-- Convert CSV Columns to Lists for Iteration --::--

    a. Read the CSV file and assign all data to 'rows' variable.
    b. Initiate three empty lists to store the data from each column.
    c. Iterate through the rows and append the data to the appropriate list.
    d. Return the three lists.
    * 'Rank' Column is not included in the lists because it is generated automatically in a for loop.

    :param file_path: path to where the treasure is hidden
    :return:
    """
    """ -------------------------------------- initialize variables --------------------------------------------- """

    import csv

    with open(file_path, 'r') as file:  # open file with 'read' permissions
        rows = csv.reader(file)     # read the file and assign all data to 'rows' variable
        next(rows, None)        # skip the header row

        # initiate empty lists to store values from filter file
        names = []  # list to store names
        attempts = []   # list to store number of attempts
        ids = []    # list to store IDs

        for row in rows:  # iterate through all rows in filter file
            names.append(row[1])  # append names (2nd column) to names list
            attempts.append(int(row[2]))  # append attempts (3rd column) to attempts list
            ids.append(int(row[3]))  # append id (4th column) to ids list

        # sort lists, by attempts, to match values in ascending order
        attempts, names, ids = zip(*sorted(zip(attempts, names, ids)))

        return names, attempts, ids


def get_user_details():
    """
                            --::-- User Details --::--

    a. Ask for user input to enter their name.
    b. If the user inputs any characters other than letters, the program will ask for a valid input.
    c. The program will keep asking for input until the user enters a valid name.
    d. If the user inputs "Enter", user_name will be assigned as "Anonymous".
    e. The program will ask for user input to enter their ID.
    f. If the user inputs any characters other than numbers, the program will ask for a valid input.
    g. The program will keep asking for input until the user enters a valid ID.
    h. If both inputs are valid, the program will return the user's name and ID.

    :return: user_name, user_id
    """
    """ -------------------------------------- initialize variables --------------------------------------------- """
    import re

    user_name = input('Please enter your name:\n')
    while True:
        if re.match('^[a-zA-Z]+$', user_name):  # verify that name is valid (only letters)
            break   # break out of loop if name is valid
        elif user_name == '':   # if user_name is empty, assign it as 'Anonymous'
            user_name = 'Anonymous'
        else:   # if name is not valid, ask for a valid name
            print('Invalid input. Please enter your name.')
            user_name = input('Please enter your name:\n')

    while True:
        try:    # verify that ID is valid (only numbers)
            user_id = int(input('Please enter your ID to start playing:\n'))
            return user_name, user_id
        except ValueError:  # if ID is not valid, ask for a valid ID
            print('Invalid input. Please type a digit.')    # print error message
            continue    # continue asking for input until a valid ID is entered


# add new record to csv file and evaluate next action based on how many records exist already
# return lists: names, attempts, ids and also return user's name, attempts and id
def increment_records(file_path, user_attempts, user_name, user_id):
    """
                            --::-- Increment Results to the Records File --::--
    a. If the file does not exist, create it and add the header row.
    b. If the file exists but has 0 records, add a new record to the file as rank #1.
    c. If the file exists and has 1 or more records:
        1. Add new record to the file.
        2. Assign the lowest rank in the file to the new record.
    d. Call the 'columns_to_lists' function to convert the CSV columns to lists for iteration.
    e. Assign the lists to variables by index from the returned lists.

    :param file_path: where top ten records are stored
    :param user_attempts: guess attempts number made by user
    :param user_name: prompt for user's name once function is called
    :param user_id: prompt for user's ID once function is called
    :return: lists of existing names, guess attempts, and ids already in the records file,
            as well as current user's name, guess attempts and id
    """
    import os
    import csv

    """--------------------------- create files on chosen paths if they do not exist yet ----------------------------"""

    if not os.path.exists(file_path):  # check if treasure file exists
        with open(file_path, 'w', newline='') as file:  # open/create file with 'write' permissions
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Rank', 'Name', 'Guesses', 'ID'])  # write header
        # use 'newline' to avoid blank lines between rows

    """------------------------- verify how many records exist and assign value to variable -------------------------"""

    with open(file_path, 'r') as file:  # open file with 'read' permissions
        treasure_data = csv.reader(file)    # read the file and assign all data to 'treasure_data' variable
        next(treasure_data, None)   # skip the header row
        num_of_records = len(list(treasure_data))   # count the number of records in the file

    """----------------------------------------- appending results to file ------------------------------------------"""

    if num_of_records == 0:     # if there are no records in the file
        with open(file_path, 'a', newline='') as file:  # open file with 'append' permissions
            append_records = csv.writer(file)
            append_records.writerow(['#1', user_name, user_attempts, user_id])  # rank is 1 because there are no records

    elif 1 <= num_of_records <= 10:     # if there are 1-10 records in the file
        with open(file_path, 'a', newline='') as file:  # open file with 'append' permissions
            records_append = csv.writer(file)
            records_append.writerow([f'#{num_of_records + 1}', user_name, user_attempts, user_id])
            # rank is 1 more than number of records
            # serves only as placeholder before refactoring/rearranging records

    names_attempts_ids = columns_to_lists(file_path)  # separate records to lists
    names = names_attempts_ids[0]  # names list
    attempts = names_attempts_ids[1]  # attempts list
    ids = names_attempts_ids[2]  # ids list

    return names, attempts, ids, user_name, user_attempts, user_id


# Organise records in ascending order by "attempts"
# Overwrite the records file with the updated records
def update_records(names_list, attempts_list, ids_list, temp_file_path, file_path):
    """
                        --::-- Treasure Hunt Records --::--
    a. Create a temporary file to store the records in ascending order.
    b. Write the header row to the temporary file (same as treasure file).
    c. Iterate through the lists and write the records to the temporary file.
        * Records are now in ascending order by 'attempts' because of the sorting in the 'columns_to_lists' function.
    d. Iterate through the temporary file and write the records to the treasure file.

    :param names_list: list of names from records file
    :param attempts_list: list of attempts from records file
    :param ids_list: list of ids from records file
    :param temp_file_path: temporary file path to store records
    :param file_path: where top ten records are stored
    :return: success message
    """
    import csv

    """----------------------------------- appending results by correct rank order ----------------------------------"""

    print('Wait while records are being updated...')

    rank = 1    # initiate rank variable as 1 for 1st place

    with open(temp_file_path, 'w', newline='') as file:
        temp_writer = csv.writer(file)
        temp_writer.writerow(['Rank', 'Name', 'Guesses', 'ID'])     # write header

        if len(attempts_list) <= 10:    # if there are 10, or less, records
            for index in range(len(attempts_list)):     # perform iteration for each record
                temp_writer.writerow([f'#{rank}', names_list[index], attempts_list[index], ids_list[index]])
                rank += 1

        elif len(attempts_list) >= 11:  # if there are more than 10 records
            for index in range(10):    # perform iteration for only the first 10 records (with the lowest attempts)
                temp_writer.writerow([f'#{rank}', names_list[index], attempts_list[index], ids_list[index]])
                rank += 1

    """------------------------------- overwriting records file with the updated records ----------------------------"""

    with open(temp_file_path, 'r') as temp_file, \
            open(file_path, 'w', newline='') as records_file:
        # open temp file with 'read' permissions | open records file with 'write' permissions

        rows = csv.reader(temp_file)    # read the temp file and assign all data to 'rows' variable
        records_writer = csv.writer(records_file)

        for row in rows:    # iterate through the rows in the temp file
            records_writer.writerow(row)    # write the rows to the records file

    return 'Records have been successfully updated.'


# Check if user's name is already in the records file
def is_user_top_10(user_name, user_attempts, user_id, file_path):
    """
                        --::-- Check if User is in Top 10 --::--

    a. Call 'columns_to_lists' function and assign each list to a variable.
    b. Check if user's name, attempts and ID exist in the records file.
        1. If ALL those values exist, return success message to user.
        2. If ANY of those values do not exist, return fail message to user.

    :param user_name: user's name
    :param user_attempts: user's guess attempts
    :param user_id: user's id
    :param file_path: where top ten records are stored
    :return: message indicating if user is in top 10 or not
    """
    is_first = f'Congratulations, {user_name}! You are 1st place! :)'
    is_top_3 = f'Congratulations, {user_name}! You are in the top 3! :)'
    is_top_10 = f'Alrighty, {user_name}! You made it to the top 10! :)'
    is_not_top_10 = f'{user_name}, you did not make the top 10... :( Keep trying, mate!'

    names_attempts_ids = columns_to_lists(file_path)  # separate records' columns to lists
    names = names_attempts_ids[0]  # list of names
    attempts = names_attempts_ids[1]  # list of attempts
    ids = names_attempts_ids[2]  # list of ids

    if user_name in names and user_attempts in attempts and user_id in ids:     # if all values exist
        if user_attempts == attempts[0]:
            return is_first
        elif user_attempts == attempts[1] or user_attempts == attempts[2]:
            return is_top_3
        else:
            return is_top_10
    else:
        return is_not_top_10    # return fail message


# Display the top 10 records
def display_top_10(file_path):
    """
                        --::-- Display Top 10 List --::--

    a. While loop in case user provides invalid input; continue looping until input is valid.
    b. If user inputs 'y' or 'Y', display the top 10 records.
    c. If user inputs 'n' or 'N', quit the program.

    :param file_path: where top ten records are stored
    :return: top 10 records if Y, quit message if N.
    """
    csv_file = open(file_path, 'r')
    top_10 = csv_file.read()
    top_10_viewer = f'---- :: TREASURE HUNT - TOP 10 RESULTS :: ----\n{top_10}\n'

    quit_message = 'Thank you for playing Treasure Hunt! See you next time :)'

    while True:
        # ask user if they want to view top 10 records
        is_view_top_10 = input('Would you like to view the top ten results? [Y/N]\n')
        if is_view_top_10.upper() == 'Y':   # if user inputs 'y' or 'Y'
            return top_10_viewer
        elif is_view_top_10.upper() == 'N':    # if user inputs 'n' or 'N'
            return quit_message
        else:  # if input is not Y or N
            print('Invalid input. Please type "Y" or "N".')


# MAIN PROGRAM #

# Get command-line arguments to set paths to txt files
treasure_path = sys.argv[1]
records_path = sys.argv[2]
temporary_records_path = sys.argv[3]

# File Paths #
# treasure_path = 'C:/Users/Dell/Desktop/Treasure_File.txt'
# records_path = "C:/Users/Dell/Desktop/Treasure_Hunt_Records.csv"
# temporary_records_path = "C:/Users/Dell/Desktop/temp_records.csv"

# Call hide_treasure() function, returns True if file is created, False if file already exists
hide_treasure(treasure_path)

# Call get_user_details() function, returns user's name and ID
user_name_id = get_user_details()
u_name = user_name_id[0]
u_id = user_name_id[1]

# Call find_treasure() function, returns user's attempts
guesses = find_treasure(treasure_path)

# Call increment_records() function, returns usernames, user attempts, and user IDs, lists of previous records
records_file_column = increment_records(records_path, guesses, u_name, u_id)
list_names = records_file_column[0]
list_attempts = records_file_column[1]
list_ids = records_file_column[2]
username = records_file_column[3]
user_attempts_num = records_file_column[4]
user_id_num = records_file_column[5]

# Call update_records() function, returns success message if records are updated
print(update_records(list_names, list_attempts, list_ids, temporary_records_path, records_path))

# Call is_user_top_10() function, returns message indicating if user is in top 10 or not
print(is_user_top_10(username, user_attempts_num, user_id_num, records_path))

# Call display_top_10() function, returns top 10 records if Y, quit message if N
print(display_top_10(records_path))
