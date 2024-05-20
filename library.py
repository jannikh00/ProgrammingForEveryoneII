# Python program that creates a database using the sqlite3 module, working with the created database

##################################### IMPORTING #####################################
import sqlite3

##################################### AUXILIARY FUNCTION #####################################

# function that prints data that's currently collected by cursor
def printing_results(cursor):
    # fetching selected data
    results = cursor.fetchall()
    # printing data line by line
    for i in results:
        print(i)
    # inserting a blank line after every loop for better readability
    print("\n")

##################################### MAIN #####################################
if __name__ == '__main__':
    # creating database and connecting to it
    conn = sqlite3.connect('library.db')

    # cursor used to navigate through the database
    c = conn.cursor()

    # creating table books, which is the frame for the collected data
    with conn:
        c.execute("""CREATE TABLE books(
                id integer,
                title text,
                author text,
                publication_year integer,
                genre text,
                PRIMARY KEY (id)
                )""")
    
    # inserting values into the table
    with conn:
        c.execute("""INSERT INTO books(id, title, author, publication_year, genre)
                VALUES 
                    ('1', 'To Kill a Mockingbird', 'Harper Lee', '1960', 'Classic'),
                    ('2', '1984', 'George Orwell', '1949', 'Dystopian'),
                    ('3', 'Pride and Prejudice', 'Jane Austen', '1813', 'Romance'),
                    ('4', 'The Great Gatsby', 'F. Scott Fitzgerald', '1925', 'Classic'),
                    ('5', 'The Catcher in the Rye', 'J.D. Salinger', '1951', 'Coming-of-Age'),
                    ('6', 'Harry Potter and the Sorcerer’s Stone', 'J.K. Rowling', '1997', 'Fantasy'),
                    ('7', 'The Hobbit', 'J.R.R. Tolkien', '1937', 'Fantasy'),
                    ('8', 'The Lord of the Rings', 'J.R.R. Tolkien', '1954', 'Fantasy'),
                    ('9', 'The Chronicles of Narnia', 'C.S. Lewis', '1950', 'Fantasy'),
                    ('10', 'Brave New World', 'Aldous Huxley', '1932', 'Dystopian'),
                    ('11', 'Frankenstein', 'Mary Shelley', '1818', 'Science Fiction'),
                    ('12', 'The Hitchhiker’s Guide to the Galaxy', 'Douglas Adams', '1979', 'Science Fiction');
                """)
    
    # selecting all information about all books in the table
    c.execute("SELECT * FROM books;")   
    printing_results(c)
    
    # selecting all information about all books with the genre 'Fantasy'
    with conn:
        c.execute("""SELECT * FROM books
                WHERE genre = 'Fantasy';
                """)
    printing_results(c)

    # updating the publication year of 'The Catcher in the Rye' with the id '5' with a fake year and printing the result
    with conn:
        c.execute("UPDATE books SET publication_year = 2022 WHERE id = 5;")
    c.execute("SELECT * FROM books;")
    printing_results(c)

    # deleting the book 'The Lord of the Rings' with the id '8' and printing the result
    with conn:
        c.execute("DELETE FROM books WHERE id = 8;")
    c.execute("SELECT * FROM books;")
    printing_results(c)

    # closing connection to database
    conn.close()
