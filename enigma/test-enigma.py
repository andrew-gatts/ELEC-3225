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
        self.DB_PATH = "test-db.db"
        self.db = init_db(self.DB_PATH)

    def tearDown(self):
        try:
            self.db.close()
        except Exception:
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
                       
class TestDoubleLetters(unittest.TestCase):
    def setUp(self):
        self.rotors = [Rotor(0), Rotor(0), Rotor(0)]
        self.pb = Plugboard()  # identity by default
        self.DB_PATH = "file:enigma_unittest?mode=memory&cache=shared"
        self.db = init_db(self.DB_PATH)

    def tearDown(self):
        try:
            self.db.close()
        except Exception:
            pass

    def _roundtrip(self, pt: str):
        # Use the same pipeline functions you already test
        ct = en.encrypt_message(pt, self.rotors, self.pb, DB_PATH=self.DB_PATH)
        back = en.decrypt_message(ct, self.rotors, self.pb)
        return ct, back

    def test_adjacent_double_letters_roundtrip(self):
        for pt in ["letter", "balloon", "bookkeeper", "mississippi", "aabbcc", "HELLO  COFFEE!!"]:
            ct, back = self._roundtrip(pt)
            # Your pipeline lowercases letters
            self.assertEqual(back, pt.lower(), f"Roundtrip failed for {pt!r}: {ct!r} -> {back!r}")

    def test_same_letter_encrypts_to_different_when_adjacent(self):
        # With stepping, identical adjacent letters should encrypt to different ciphertext letters
        for pt in ["aa", "LL", "zz", "Mm"]:
            ct, back = self._roundtrip(pt)
            self.assertEqual(back, pt.lower())
            # Only check alphabetic characters
            letters = [c for c in ct if c.isalpha()]
            if len(letters) >= 2:
                self.assertNotEqual(letters[0], letters[1],
                                    f"Adjacent identical letters produced same ciphertext in {pt!r}: {ct!r}")


if __name__ == "__main__":
    unittest.main()
