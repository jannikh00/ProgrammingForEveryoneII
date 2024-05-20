# Python program that has a function named 'put_request'
# and a function named 'delete_request'. The program also
# Calls to the 'put_request' and 'delete_request' functions 
# using a publicly available API.

################################ IMPORTING ################################
import requests

################################ FUNCTIONS ################################
# Put Function
def put_request(url, data_dict):
    r = requests.put(url, json=data_dict)
    # Printing Responses
    print("Responses:")
    print(f"\nStatus: {r.status_code}")
    print("\nHeader:")
    for key, value in r.headers.items():
        print(f"{key}: {value}")
    print("\nBody:")
    print(f"{r.text}")

# Delete Function
def delete_request(url):
    r = requests.delete(url)
    # Printing Responses
    print("Responses:")
    print(f"\nStatus: {r.status_code}")
    print("\nHeader:")
    for key, value in r.headers.items():
        print(f"{key}: {value}")

################################ TESTS ################################
if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts/1"
    dict = {"title": "This is not your title anymore.",
            "body": "This is not your body anymore."}

    # Testing Put Function
    print("\nPut Function Test:\n")
    put_request(url, dict)
    print("\n"+"-"*60+"\n")

    # Testing Delete Function
    print("Delete Function Test:\n")
    delete_request(url)