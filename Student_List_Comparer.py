# Student List Comparer
# Version 0.1 25 September 2018
# Created by Jeff Mitchell
# Takes two lists of Student IDs and returns a list of those in List A that
# are missing from List B


import csv
import sys
import time


def check_repeat():
    """Return True or False for repeating another action.

    Returns:
        True if user wants to perform another action, False otherwise.
    """
    repeat = ''
    while repeat == '':
        repeat = input("\nDo you want to prepare another file? y/n --> ")
        if repeat != 'y' and repeat != 'n':
            print("\nThat is not a valid answer! Please try again.")
            repeat = ''
        elif repeat == 'y':
            return True
        else:
            return False


def check_review_warnings():
    """Return True or False for reviewing warning messages.

    Returns:
        True if user wants to review warning messages, False otherwise.
    """
    review = ''
    while review == '':
        review = input('\nDo you want to view the warning messages? y/n --> ')
        if review not in ('y', 'n'):
            print('\nThat is not a valid answer! Please try again.')
            review = ''
        elif review == 'y':
            return True
        else:
            return False


def compare_lists(file_a_data, file_b_data):
    """Return missing students.
    
    Returns students that are present in File A but missing from File B.
    
    Args:
        file_a_data (list): Student IDs from  File A.
        file_b_data (list): Student IDs from  File B.
        
    Returns:
        missing (list): Student ID's from File A that are missing from File B.
    """
    missing = []
    for student in file_a_data:
        if student not in file_b_data:
            missing.append(student)
    return missing


def confirm_files(o_file, r_files):
    """Print required files and have user press enter to continue.

    Args:
        o_file (str): Name of file that is being processed.
        r_files (list): List of files that need to be present.
    """
    num_files = len(r_files)
    if num_files == 1:
        text_f = 'this file is'
    else:
        text_f = 'these files are'
    print('\nTo process the {} the following files are required:\n'.format
          (o_file))
    for file in r_files:
        print(file)
    print('\nPlease make sure that {} in the required folder and are updated '
          'correctly before proceeding.'.format(text_f))
    input('\nPress the enter key to continue processing the {} file '
          '--> '.format(o_file))


def debug_list(test_list):
    """Print out contents of a list.

    Args:
        test_list (listt): List to be printed out.
    """
    i = 0
    while i < len(test_list):
        print('Item ' + str(i))
        print(str(test_list[i]))
        i += 1


def generate_time_string():
    """Generate a timestamp for file names.

    Returns:
        time_str (str): String of timestamp in the format yymmdd-hhmmss.
    """
    time_str = time.strftime('%y%m%d-%H%M%S')
    return time_str


def get_ids(file_data):
    """Extract Student IDs into a single list.
    
    Takes each Student ID that is an individual list and places the Student ID
    as a string into one list.
    
    Args:
        file_data (list): List of Student IDs, each as a list.
        
    Returns:
        student_ids (list): List of Student IDs stored as strings.
    """
    student_ids = []
    for student in file_data:
        student_ids.append(student[0])        
    return student_ids


def load_data(file_name):
    """Read data from a file.

    Args:
        file_name (str): The name of the file to be read.
        
    Returns:
        read_data (list): A list containing the data read from the file.
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.
    """
    read_data = []
    warnings = []
    # print('File name = ' + str(file_name))
    # Check that file exists
    valid_file = False
    while valid_file is False:
        try:
            file = open(file_name + '.csv', 'r')
        except IOError:
            print('The file does not exist. Check file name.')
            file_name = input('What is the name of the file? ')
        else:
            file.readline()
            reader = csv.reader(file, delimiter=',', quotechar='"')
            for row in reader:
                if row[0] not in (None, ''):
                    read_data.append(row)
            file.close()
            # Check data is correct
            for item in read_data:
                if len(item[0].strip()) != 9:
                    warnings.append(item)
            valid_file = True
    # print('Check loaded data:')
    # debug_list(read_data)
    # print('Length Load Data warnings: ' + str(len(warnings)))
    if len(warnings) > 0:
        return read_data, True, warnings
    else:
        return read_data, False, warnings


def main():
    low = 1
    high = 2
    repeat = True
    while repeat is True:
        try_again = False
        main_message()
        try:
            action = int(input('\nPlease enter the number for your '
                               'selection --> '))
        except ValueError:
            print('Please enter a number between {} and {}.'.format(low, high))
            try_again = True
        else:
            if int(action) < low or int(action) > high:
                print('\nPlease select from the available options ({} and {})'
                      .format(low, high))
                try_again = True
            elif action == low:
                process_compare_lists()
            elif action == high:
                print('\nIf you have generated any files, please find them '
                      'saved to disk. Goodbye.')
                sys.exit()
        if not try_again:
            repeat = check_repeat()
    print('\nPlease find your files saved to disk. Goodbye.')


def main_message():
    """Print the menu of options."""
    print('\n\n*************==========================*****************')
    print('\nStudent List Comparer version 1.0')
    print('Created by Jeff Mitchell, 2018')
    print('\nOptions:')
    print('\n1 Compare two lists of Student IDs')
    print('2 Exit')


def print_missing(missing):
    """Print out missing students.

    Args:
        missing (listt): List to be printed out.
    """
    print('\nThe following students are missing from File B:\n')
    for student in missing:
        print('{}'.format(student))


def process_compare_lists():
    """Compare two lists of Student IDs.
    
    Find Student IDs in List A that are missing from List B.
    """
    warnings = ['\nProcessing Compare Lists Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Compare Lists.')
    print('\nFinds students that are present in File A but are missing from '
          'File B.')
    # Confirm the required files are in place
    required_files = ['File A', 'File B']
    confirm_files('Compare Lists', required_files)
    
    file_a_name = input('\nWhat is the name of File A? --> ')
    file_a_data, to_add, warnings_to_add = load_data(file_a_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Get name for File B and then load
    file_b_name = input('\nWhat is the name of File B? --> ')
    file_b_data, to_add, warnings_to_add = load_data(file_b_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a list of Student IDs for each data source
    file_a_data = get_ids(file_a_data)
    file_b_data = get_ids(file_b_data)
    # debug_list(file_b_data)
    # Compare the two lists and get missing
    missing = compare_lists(file_a_data, file_b_data)
    print_missing(missing)
    debug_list(missing)
    headings = 'StudentID'
    save_data_upload_csv(missing, headings, 'Missing_students_')
    process_warning_log(warnings, warnings_to_process)


def process_error_log(errors, source):
    """Process an Error log.

    Prints a list of fatal errors in the source data. Saves the errors to file
    and then exits the program.

    Args:
        errors (list): List of errors found in the source data.
        source (str): The name of the source data.
    """
    print('\nThe following errors have been identified in the ' + source
          + ' data: \n')
    for line in errors:
        print(line)
    current_time = generate_time_string()
    error_file = 'Error_log_' + '_' + current_time + '.txt'
    print('\nThe errors have been saved to the error log file.\n')
    save_error_log(source, errors, error_file)
    print('The program will now close. Please correct errors before'
          ' trying again.')
    input('Press enter key to exit. ')
    raise SystemExit


def process_warning_log(warnings, required):
    """Process a Warnings log.

    If required, prints a list of non-fatal errors in the source data. Saves
    the errors to file. If it is not required (e.g. there has not been any data
    appended to the warnings list) then the function returns without any
    action.

    Args:
        warnings (list): List of errors or potential issues found in the source
        data.
        required (str): If True the function will run, if False then it is
        skipped.
    """
    if not required:
        return
    print('\nThere were errors found in one or more of the data sources. '
          'You should check these errors and correct if necessary before '
          'using the generated files. If you correct the files, it is '
          'recommended that you run this program again to generate new '
          'output files from the correct data.')
    review = check_review_warnings()
    if review:
        for line in warnings:
            print(line)
    current_time = generate_time_string()
    warning_file = 'Warning_log_' + '_' + current_time + '.txt'
    print('\nThe warnings have been saved to the warning log file.\n')
    save_warning_log(warnings, warning_file)


def save_error_log(source, error_log, file_name):
    """Save to file the error log.

    Args:
        source (str): Name of the source file or data.
        error_log (list): The errors to be written.
        file_name (str): Name to save the file to.
    """
    try:
        open(file_name, 'w')
    except IOError:
        print('Error log could not be saved as it is not accessible.')
    else:
        FO = open(file_name, 'w')
        FO.write(str(source) + '\n')
        for line in error_log:
            FO.write(str(line) + '\n')
        FO.close()
        print('Error log has been saved to ' + str(file_name))


def save_warning_log(warning_log, file_name):
    """Save to file the warnings log.

    Args:
        warning_log (list): The errors to be written.
        file_name (str): Name to save the file to.
    """
    try:
        open(file_name, 'w')
    except IOError:
        print('Warning log could not be saved as it is not accessible.')
    else:
        FO = open(file_name, 'w')
        for line in warning_log:
            FO.write(str(line) + '\n')
        FO.close()
        print('Warnings log has been saved to ' + str(file_name))
    

if __name__ == '__main__':
    main()