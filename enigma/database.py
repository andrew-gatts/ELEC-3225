import sqlite3
import sys

DB_PATH = "database.db"

######################################
# Function to initialize the databse #
######################################
def init_db(db_path=DB_PATH):
    # Connect to the DB, print exisitng tables, and ensure table exists
    database = sqlite3.connect(db_path)
    cursor = database.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print("Existing tables:", cursor.fetchall())
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            CRN         INTEGER PRIMARY KEY AUTOINCREMENT,
            message     TEXT    NOT NULL,
            encrypted   TEXT    NOT NULL
        );       
    """)
    database.commit()
    return database

##################################
# Function to close the database #
##################################
def close_db(database: sqlite3.Connection):
    database.commit()
    database.close()

############################################
# Function to add an entry to the database #
############################################
def add_entry(database: sqlite3.Connection, message: str, encrypted: str):
## Get user input for manual entry
    cursor = database.cursor()
    # message=input(f"Enter message for {name}: ")
    # encrypted=input(f"Enter encrypted message for {name}: ")

    # Insert the data into the table
    cursor.execute(
        "INSERT OR IGNORE INTO data (message, encrypted) VALUES (?, ?)",
        (message, encrypted)
    )

    # Return the id of the entry
    return cursor.lastrowid

###################################
# Return all data in the database #
###################################
def print_all_entries(database: sqlite3.Connection):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM data")
    return cursor.fetchall()

##########################
# Search database by CRN #
##########################
def get_entry_by_crn(database: sqlite3.Connection, crn: int):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM data WHERE CRN = ?", (crn,))
    return cursor.fetchone()


def main():
    database = init_db(DB_PATH)
    args = sys.argv[1:]

    # Return "help" message if no arguments are specified
    if len(args) == 0 or args[0] != "test":
        print(f"Usage: database.py test [CRN]\n For testing only")
        sys.exit(1)

    # if just the "test" argument is passed prompt the
    # user and write to the database
    if len(args) == 1:
        message = input("What is the message: ")
        encrypted = input("What is the encrypted message: ")
        add_entry(database, message, encrypted)
        print("\nCurrent entries:")
        for row in print_all_entries(database):
            print(row)
    
    else:
        # if "test x" is passed read from the databse
        key = args[1]
        if key.isdigit():
            # if the variable passed is a number get entry via CRN
            row = get_entry_by_crn(database, int(key))
            if row:
                print(row)
            else:
                print(f"No entry with CRN = {key}")
        else:
            print(f"Need to pass CRN")

    close_db(database)

if __name__ == "__main__":
    main()

    
