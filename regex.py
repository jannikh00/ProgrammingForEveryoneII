import re

# Program that tests if emails and phone numbers have a valid format after given
# definition

################################## NOTES ##################################

# I wasn't sure about the definitions from the assignment. I‘ve incorporated 
# some test cases that show what I interpreted as valid or as invalid. If you 
# let the program run, you can see which one's are which. If I misinterpreted
# anything, please let me know and give me the chance to do it right. Thanks :)

################################## FUNCTIONS ##################################

# function to test if email has a valid format
def validate_email(email):
    regex = "^[a-z0-9]+(.|_)?[a-z0-9]+@[a-z0-9]+.[a-z0-9]{2,3}$"
    search = re.search(regex, email)
    if search:
        return True
    else:
        return False

# function to test if phone number has a valid format
def validate_phone_number(phone_nr):
    regex = "^(\(\d{3}\)|\d{3})(-|\s)?\d{3}(-|\s)?\d{4}$"
    search = re.search(regex, phone_nr)
    if search:
        return True
    else:
        return False

################################## TESTING ##################################

# testing validate_email() function
mail_list = [
    "john.doe@example.com",
    "jane_smith123@example.co.uk",
    "alice123@example.org",
    "bob.smith@example.net",
    "david123_456@example.com",
    "user@example.info",
    "test.email@example.com",
    "123test@example.com",
    "abc123@example.com",
    "test_user123@example.com",
    "test.email123@example.com",
    "user_123@example.com",
    "user123_456@example.com",
    "user123@example.com",
    "user.123@example.com",
    "user_123@example.com",
    "user_123@example.co.uk",
    "user123@example.net",
    "user_123@example.org",
    "user_123@example.info",
    "user.123@example.com",
    "user.123@example.co.uk",
    "user.123@example.net",
    "user.123@example.org",
    "user.123@example.info",
    "1@example.com",
    "123@example.com",
    "1.2@example.com",
    "1_2@example.com",
    "1.2_3@example.com",
    "1.2_3@example.co.uk",
    "1.2_3@example.net",
    "1.2_3@example.org",
    "1.2_3@example.info"
]
print(f"\nNumber of email test cases: {len(mail_list)}\n")
true_cnt = 0
for i in mail_list:
    test = validate_email(i)
    if test:
        print(f"valid: {i}")
        true_cnt += 1
    else:
        print(f"invalid: {i}")
print(f"\nNumber of True values: {true_cnt}")
print(f"Number of False values: {len(mail_list)-true_cnt}\n")

print("---------------------------------------------------\n")

# testing validate_phone_number() function
nr_list = [
    "(123) 456-7890",
    "(123)456-7890",
    "(123)4567890",
    "123-456-7890",
    "1234567890",
    "123 456 7890",
    "123 4567890",
    "123456 7890",
    "(123)-456-7890",
    "(123 456-7890",
    "123-45-67890",
    "1234567",
    "1234-567-8901"
]
print(f"Number of phone number test cases: {len(nr_list)}\n")
true_cnt = 0
for i in nr_list:
    test = validate_phone_number(i)
    if test:
        print(f"valid: {i}")
        true_cnt += 1
    else:
        print(f"invalid: {i}")
print(f"\nNumber of True values: {true_cnt}")
print(f"Number of False values: {len(nr_list)-true_cnt}\n")