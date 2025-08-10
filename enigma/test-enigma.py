# test-enigma.py — matches current code, verifies DB integration
import unittest
from pathlib import Path
import sys
import tempfile
import os

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from enigma.rotor import Rotor
from enigma.plugboard import Plugboard
from enigma import enigma as en
from enigma.database import init_db, print_all_entries

class TestRotor(unittest.TestCase):
    def test_offset_and_show(self):
        r = Rotor(0)
        self.assertEqual(r.get_offset(), 0)
        r.set_offset(26)
        self.assertEqual(r.get_offset(), 0)
        self.assertEqual(r.show_position(), 0)

    def test_encrypt_decrypt_roundtrip(self):
        # Use inputs that won't trigger consecutive duplicate-encrypt shift
        for off in (0, 3, 25):
            r = Rotor(off)
            plain = "xyz abc!"
            self.assertEqual(r.decrypt(r.encrypt(plain)), plain.lower())

class TestPlugboard(unittest.TestCase):
    def test_apply_identity(self):
        pb = Plugboard()
        self.assertEqual(pb.apply_plugboard("Abc! Z"), "abc! z")

    def test_apply_simple_swap(self):
        pb = Plugboard()
        # Simulate swapping 'a' <-> 'b' by swapping positions 0 and 1
        pb.letters[0], pb.letters[1] = pb.letters[1], pb.letters[0]
        self.assertEqual(pb.apply_plugboard("Abc!"), "bac!")

class TestEnigmaPipelineWithDB(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(prefix="enigma_test_", suffix=".db", delete=False)
        self.DB_PATH = self.tmp.name
        self.tmp.close()

    def tearDown(self):
        try:
            os.remove(self.DB_PATH)
        except OSError:
            pass

    def test_encrypt_decrypt_and_db_write(self):
        rotors = [Rotor(1), Rotor(2), Rotor(3)]
        pb = Plugboard()
        pt = "Enigma!"
        ct = en.encrypt_message(pt, rotors, pb, DB_PATH=self.DB_PATH)
        # decrypt
        back = en.decrypt_message(ct, rotors, pb)
        # rotor/plugboard pipeline lowercases letters
        self.assertEqual(back, pt.lower())
        # check a DB row was written with (message, encrypted)
        db = init_db(self.DB_PATH)
        rows = print_all_entries(db)
        db.close()
        self.assertTrue(any((row[1] == pt and row[2] == ct) for row in rows), "DB row not found for (message, encrypted)")

if __name__ == "__main__":
    unittest.main()
