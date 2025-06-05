import sqlite3

database = sqlite3.connect("databse.db")

cursor = database.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

cursor.execute("""
               
    CREATE TABLE IF NOT EXISTS data (
               
    CRN INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    Dmessage TEXT NOT NULL,

    encrypted TEXT NOT NULL
);
               
""")
## Get user input for manual entry
name=input("Enter entry name: ")
dmessage=input(f"Enter message for {name}: ")
encrypted=input(f"Enter encrypted message for {name}: ")

# Insert the data into the table
cursor.execute("""INSERT OR IGNORE INTO data 
               (name, Dmessage, encrypted)
               VALUES (?, ?, ?)""", (name, dmessage, encrypted))

# Get the CRN of the inserted data
new_crn = cursor.lastrowid

# Print the entry that was just added
print (f"\nAdded entry {name} at {new_crn}")

print ("\nWhat we have:")

cursor.execute("""SELECT * FROM data""")

dataint = cursor.fetchall()

for data in dataint:
    
    print(data)

database.commit()

database.close()
