import sys
import unittest

from rotor import Rotor
from plugboard import Plugboard
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

    def test_plugboard_class(self):
        pb = Plugboard()
        # Default: no change
        self.assertEqual(pb.apply_plugboard("xyz123 a b c!"), "xyz123 a b c!")

        # ABCD with A<->B should become BACD
        i, j = pb.letters.index('a'), pb.letters.index('b')
        pb.letters[i], pb.letters[j] = pb.letters[j], pb.letters[i]
        self.assertEqual(pb.apply_plugboard("abcd"), "bacd")

        # Reset
        pb.reset()
        self.assertEqual(pb.letters[0], 'a')
        self.assertEqual(pb.letters[1], 'b')
        self.assertEqual(pb.apply_plugboard("ab"), "ab")

    def test_show_config_prints_active_swaps(self):
        pb = Plugboard()
        pb.letters[0], pb.letters[25] = 'z', 'a'
        buf = sys.stdout = type(sys.stdout)(sys.stdout)
        from io import StringIO
        buf = StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf

        pb.show_config()

        sys.stdout = old_stdout
        output = buf.getvalue()
        self.assertIn("a↔z", output)
        

    def test_rotor_offset_1(self):
        # Assuming rotor A→B, B→C, … Z→A for offset=1
        self.assertEqual(Rotor(1).encrypt("abc"), "bcd")

    def test_repeated_rotor(self):
        r = Rotor(1)
        cases = [("abc", "bcd"), ("acc", "bde")]
        for inp, out in cases:
            with self.subTest(inp=inp):
                self.assertEqual(r.encrypt(inp), out)

    def test_full_cycle_and_db(self):
        msg = "hello"
        # swap H↔E -> EHLLO
        pb = Plugboard()
        # Swap h <-> e
        i, j = pb.letters.index('h'), pb.letters.index('e')
        pb.letters[i], pb.letters[j] = pb.letters[j], pb.letters[i]
        # -> ehllo
        swapped = pb.apply_plugboard(msg)
        self.assertEqual(swapped, "ehllo")

        # then offset 2: E→G, H→J, L→N, N→P, O→Q => GJNNQ
        encrypted = Rotor(2).encrypt(swapped)
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
    unittest.main(verbosity=2)