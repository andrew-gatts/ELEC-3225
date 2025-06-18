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
    print("Existing tables:", cursor.fetchall())
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            CRN         INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            message     TEXT    NOT NULL,
            encrypted   TEXT    NOT NULL
        );       
    """)
    database.commit()
    return database

##################################
# Function to close the database #
##################################
def close_db(database):
    database.commit()
    database.close()

############################################
# Function to add an entry to the database #
############################################
def add_entry(database, *args):
## Get user input for manual entry
    cursor = database.cursor()
    name=input("Enter entry name: ")
    message=input(f"Enter message for {name}: ")
    encrypted=input(f"Enter encrypted message for {name}: ")

    # Insert the data into the table
    cursor.execute(
        "INSERT OR IGNORE INTO data (name, message, encrypted) VALUES (?, ?, ?)",
        (name, message, encrypted)
    )

    # Return the id of the entry
    return cursor.lastrowid()

###################################
# Return all data in the database #
###################################
def print_all_entries(database):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM data")
    return cursor.fetchall()

##########################
# Search database by CRN #
##########################
def get_entry_by_crn(database, crn):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM data WHERE CRN = ?", (crn,))
    return cursor.fetchone()

###########################
# Search database by Name #
###########################
def get_entry_by_name(database, name):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM data WHERE name = ?", (name,))
    return cursor.fetchone()

def main():
    database = init_db()
    args = sys.argv[1:]

    # Return "help" message if no arguments are specified
    if len(args) == 0 or args[0] != "test":
        print(f"Usage: database.py test [CRN|name]\n For testing only")
        sys.exit(1)

    # if just the "test" argument is passed prompt the
    # user and write to the database
    if len(args) == 1:
        add_entry(database)
        print("\nCurrent entries:")
        for row in print_all_entries(database):
            print(row)
    
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
        # if the variable passed is a name get entry with name
        row = get_entry_by_name(database, key)
        if row:
            for r in row:
                print(r)
        else:
            print(f"No entries found with name = '{key}'")
        
    close_db(database)

if __name__ == "__main__":
    main()

    
