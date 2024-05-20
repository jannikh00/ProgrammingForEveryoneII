# Python program that uses the requests library for getting data from an URL and
# posting data to an URL.


################################### IMPORTING ###################################
import requests

################################### FUNCTIONS ###################################

# get request function
def get_request(url):
    r = requests.get(url)
    print("\nStatus Code:\n", r)
    print("\nHeaders:\n", r.headers)
    print("\nFirst 500 characters:\n", r.text[:500])

# post request function
def post_request(url, dict):
    r = requests.post(url, data=dict)
    print("\nStatus Code:\n", r)
    print("\nHeaders:\n", r.headers)
    print("\nFirst 500 characters:\n", r.text[:500])


################################### TESTING ###################################

# Creating variables for functions
example_url = 'https://jsonplaceholder.typicode.com/posts'
example_dict = {"userId": 1, "id": 100, "title": "askfj asdf khweifhqo aslfd sa", "body": "asfha a;shdqwh asjdfha; sw23"}

# Calling functions
print("\nTesting get_request function:")
get_request(example_url)
print("\n-------------------------------------------------------------------------------------------------------")
print("\nTesting post_request function:")
post_request(example_url, example_dict)
