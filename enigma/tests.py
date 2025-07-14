import sys
import unittest

from rotor import Rotor
from plugboard import plugboard
from database import init_db, add_entry, close_db

# Using Unittest to test our code. https://docs.python.org/3/library/unittest.html

class EncryptionTests(unittest.TestCase):
    def setUp(self):
        # Use an in-memory database (if your init_db supports it) for fast, disposable tests
        try:
            self.db = init_db(":memory:")
        except TypeError:
            # fallback if init_db doesn’t take a path argument
            self.db = init_db()

    def tearDown(self):
        close_db(self.db)

    def test_plugboard_simple_swap(self):
        # ABCD with A<->B should become BACD
        self.assertEqual(plugboard("abcd", "a", "b"), "bacd")

    def test_rotor_offset_1(self):
        # Assuming rotor A→B, B→C, … Z→A for offset=1
        self.assertEqual(Rotor(1).encrypt("abc"), "bcd")

    def test_repeated_rotor(self):
        self.assertEqual(Rotor(1).encrypt("acc"), 'bde')

    def test_full_cycle_and_db(self):
        msg = "hello"
        # swap H↔E -> EHLLO
        pb = plugboard(msg, "h", "e")
        # then offset 2: E→G, H→J, L→N, N→P, O→Q => GJNNQ
        encrypted = Rotor(2).encrypt(pb)
        self.assertEqual(encrypted, "gjnnq")
        crn = add_entry(self.db, msg, encrypted)
        self.assertIsInstance(crn, int)

def run_tests():
    # explicitly build a suite just from EncryptionTests
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EncryptionTests))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    # exit non‐zero on failure so CI would catch it
    sys.exit(not result.wasSuccessful())

if __name__ == "__main__":
    run_tests()