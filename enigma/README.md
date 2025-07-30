# Enigma

All of the enigma code is stored here. To run the CLI enigma:

```
python3 enigma.py
```

## enigma.py

This is the main enigma file that combines all of the fucntions together and makes them work

## database.py

This is the database management function. Allows the user to read and write from the database. It is mainly just used to store previous results.

## plugboard.py

This contains the plugboard class. Allowing the user to swap letters with memory of the swapped letters. It also performs the swapping

## rotor.py

This contains the rotor class. This rotates through the letters as they are passed through. This is the main encryption of the machine

## tests.py

Contains the testing code for the enigma funcitons. Tests all of the functions with known good results in memory. Can be called with:

```
python3 -m unittest tests.py
```
