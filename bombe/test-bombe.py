# test-bombe.py
import unittest
from bombe.bombe import (
    Rotor,
    add_mapping,
    plugboard_apply,
    decrypt_message,
    score_plaintext,
    guess_offsets,
    expand_unknowns
)

class TestRotor(unittest.TestCase):
    def test_offset_wrapping_and_show(self):
        r = Rotor(27)
        self.assertEqual(r.get_offset(), 1)
        self.assertEqual(r.show_position(), 1)

    def test_encrypt_decrypt_identity(self):
        msg = "Test!!"
        msg_enc = "vguv!!"
        storage = msg_enc
        for off in (0, 3, 25):
            r = Rotor(off)
            storage = r.decrypt(storage)
        self.assertEqual(storage, msg.lower())

class TestPlugboard(unittest.TestCase):
    def test_add_mapping(self):
        pb = {}
        self.assertTrue(add_mapping(pb, 'A', 'b'))
        self.assertFalse(add_mapping(pb, 'A', 'c'))  # cannot reuse
        self.assertFalse(add_mapping(pb, 'd', 'b'))  # cannot reuse
    def test_plugboard_apply(self):
        pb = {'a':'z','z':'a'}
        text = "AzBy"
        self.assertEqual(plugboard_apply(text, pb), "za by".replace(" ",""))

class TestPipeline(unittest.TestCase):
    def test_encrypt_decrypt_message(self):
        pb = {'x':'y','y':'x'}
        rotors = [Rotor(2), Rotor(4)]
        msg    = "Pack1!"
        ct     = "vgiq1!"
        pt     = decrypt_message(ct,    rotors, pb)
        self.assertEqual(pt, msg.lower())

class TestUnknownsAndScoring(unittest.TestCase):
    def test_expand_unknowns(self):
        patterns = ['?', '2', '?']
        combos = list(expand_unknowns(patterns))
        self.assertEqual(len(combos), 26 * 1 * 26)
        self.assertIn((0,2,0), combos)
    def test_score_plaintext(self):
        txt = "The cat and the dog."
        self.assertEqual(score_plaintext(txt, ["the","dog","mouse"]), 2)

class TestGuessOffsets(unittest.TestCase):
    def test_guess_offsets_simple(self):
        # ciphertext 'a' with unknown offset.  every offset decrypts to 'a'
        results = guess_offsets(
            ciphertext='a',
            rotor_pattern=['?'],
            plugboard_map={},
            dict_words=['a'],
            top_n=3
        )
        # best score=1, offset=0 should be first
        self.assertEqual(results[0][0], 1)
        self.assertEqual(results[0][1], (0,))
        self.assertEqual(results[0][2], 'a')

if __name__ == "__main__":
    unittest.main()

