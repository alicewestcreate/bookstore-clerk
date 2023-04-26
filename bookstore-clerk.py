"""
This program simulates a bookstore clerk. Users can enter, delete and search for books, and update quantity. 
It uses defensive programing techniques for to catch invalid user inputs. 

"""

import sqlite3

columns = ["self", "id", "title", "author", "quantity"]


class Database :
    # Initisalising databases class
    def __init__(self):
        self.db = sqlite3.connect(f"ebookstore_db") # Connects self to sqlite. 
        self.cursor = self.db.cursor() # Connects self to cursor method
        self.create_table() # Generates a table, at initialising stage. 
        self.db.commit() # Connects to commit method. 


    def define_column(self): 
        column_names = ["id", "title", "author", "quantity"]
        column_type = ["INTERGER", "TEXT"]
        print(column_names)
        return(column_names, column_type)
    

    def printItems(self, name, typee):
        return f"{name} {typee}"
    

    def integer_check(self): 
        while (True):
            try:
                quantity = int(input("Enter quantity: "))
                return quantity
            except ValueError:
                print("Invalid input. Please enter an a number.")
                continue


    def create_table(self):
        column_info = self.define_column()
        (column_names, column_type) = column_info
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS ebookstore({self.printItems(column_names[0], column_type[0])} PRIMARY KEY, {column_names[1]} {column_type[1]} , {column_names[2]} {column_type[1]} , {column_names[3]} {column_type[0]})")


    def insert_to_db(self, id, title, author, quantity):
        """
        This method, inset information in to the database.
        """
        self.cursor.execute("""
            INSERT INTO ebookstore(id, title, author, quantity) SELECT ?,?,?,? 
            WHERE NOT EXISTS (SELECT 1 FROM ebookstore WHERE id = ? AND title = ?) """, 
            (id, title, author, quantity, id, title,))
        print("Book Entered")
        self.db.commit()


    def add_book(self):
        """
        This method, get information from user, and calls the insert to database 
        """
        while (True): 
            try: 
                id = input("Enter Id")
                title = input("Enter title")
                author = input("Enter author")
                quantity = self.integer_check()

                self.insert_to_db(id, title, author, quantity)
                self.cursor.execute("""SELECT id, title, author, quantity FROM ebookstore WHERE id = ?""", (id,))
                book = self.cursor.fetchone()
                print("Book Added:", book)
                break
                
            except sqlite3.IntegrityError:
                print("ID already in use, try again")


    def update_quantity(self):
        """
        This method, gets user to enter book id, updates quantity entered, and prints out the updated item
        """
        while (True): 
            id = input("Enter book id: ")
            print("Searching For ID...:",id)
            self.cursor.execute("""SELECT id, title, author, quantity FROM ebookstore WHERE id = ?""", (id,))
            book = self.cursor.fetchone()
            if book != None:
                print("Book Select: \n", book)
                quantity = self.integer_check()
                self.cursor.execute("""UPDATE ebookstore SET quantity = ? WHERE id = ? """, (quantity,id,))
                self.db.commit()
                self.cursor.execute("""SELECT id, title, author, quantity FROM ebookstore WHERE id = ?""", (id,))
                book = self.cursor.fetchone()
                print("Updated Quantity: \n", book)
                break
            else: 
                print("No results found, try again")
                continue
   
    
    def delete_book(self):
        """
        This method gets user to enter book id, prints out item, and comfirms book is deleted.
        """
        id = input("Enter book id: ")
        self.cursor.execute("""SELECT id, title, author, quantity FROM ebookstore WHERE id = ?""", (id,))
        book = self.cursor.fetchone()
        print("Book Select: \n", book)
        self.cursor.execute("""DELETE FROM ebookstore WHERE id = ? """, (id,))
        print("Book Deleted: \n")
        self.db.commit()

    
    def search_book(self):
        """
        This method asks user which field to search in, and returns item(s) with corrosponding field.
        """
        while (True): 

            try: 
                search_by = int(input(""" Search by: 
1. ID
2. Title
3. Author
4. Exit """
))

                if search_by == 1:
                    search_item = "id"
                elif search_by == 2:
                    search_item = "title"
                elif search_by == 3:
                    search_item = "author"
                elif search_by == 4:
                    break
                else: 
                    print("Invalid entry, try again")
                    continue

                value = input(f"Enter {search_item}:")
                self.cursor.execute(F"SELECT id, title, author, quantity FROM ebookstore WHERE {search_item}=?", (value,))
                found = False
                
                for row in self.cursor:
                    print("\nItem Found",row[0], row[1], row[2], row[3])
                    found = True
                if not found:
                    print("No results found")
                    continue
                           
                break

            except ValueError:
                print()
                print("Invalid input, try again")
        

    def print_table(self): 
        """
        This method prints all items in table
        """
        self.cursor.execute('''SELECT id, title, author, quantity FROM ebookstore''')
        for row in self.cursor:
            print(row)


"""
Assigning database class to estore, and inserting initial books to the data base.  

"""

name = "ebookstore"
estore = Database()
estore.insert_to_db(3001, "A Tale of Two Cities", "Charles Dickens", 30)
estore.insert_to_db(3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40)
estore.insert_to_db(3003, "Harry", "J.K. Rowling", 40)
print("\nBooks Entered: ")
estore.print_table()

print("\n Welcome to bookstore, make a selection")


"""
User Menu 
"""
while (True): 
    try:
        option = int(input(""" Enter option: 
1. Enter book
2. Update book 
3. Delete book 
4. Search books 
5. See All 
0. Exit
:"""
    ))
        if option == 1:
            estore.add_book()
        elif option == 2:
            estore.update_quantity()
        elif option == 3:
            estore.delete_book()
        elif option == 4:
            estore.search_book()
        elif option == 5:
            estore.print_table()
        elif option == 0:
            exit()
        else:
            print("Incorrect entry try again. ")

    except ValueError: 
        print("Invalid entry, try again")

        