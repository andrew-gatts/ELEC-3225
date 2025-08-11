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
        ct     = "wilu1!"
        pt     = decrypt_message(ct,    rotors, pb)
        self.assertEqual(pt, msg.lower())

class TestUnknownsAndScoring(unittest.TestCase):
    def test_expand_unknowns(self):
        patterns = ['?', '2', '?']
        combos = list(expand_unknowns(patterns))
        self.assertEqual(len(combos), 26 * 1 * 26)
        self.assertIn((0,2,0), combos)

    def test_score_plaintext(self):
        # tiny sanity check
        words = ["hello", "world"]
        self.assertEqual(score_plaintext("hello", words), 1)
        self.assertEqual(score_plaintext("hello world", words), 2)
        self.assertEqual(score_plaintext("HELL0 W0RLD", words), 0)

    # --- helper: generate ciphertext consistent with step-before-decode ---
    def encrypt_with_stepping(self, plaintext: str, offsets: tuple[int, ...]) -> str:
        """
        Mirror of your decrypt_message stepping:
        - step BEFORE each character
        - then run FORWARD through rotors applying +offset (Caesar)
        Plugboard is omitted (use {} in tests) to keep this deterministic.
        """
        local = [o % 26 for o in offsets]  # do not mutate objects under test

        def step():
            # rightmost rotor steps every char; carry left on wrap
            for i in range(len(local) - 1, -1, -1):
                local[i] = (local[i] + 1) % 26
                if local[i] != 0:
                    break

        out = []
        for ch in plaintext.lower():
            if 'a' <= ch <= 'z':
                step()
                x = ord(ch) - 97
                # forward through rotors (encryption): +offset for each rotor
                for off in local:
                    x = (x + off) % 26
                out.append(chr(97 + x))
            else:
                out.append(ch)
        return ''.join(out)

    def test_guess_offsets_simple(self):
        """
        With step-before-decode, a one-letter ciphertext 'a' is maximized at offset 25,
        because the first step turns offset 25 -> effective 0 for that character.
        """
        results = guess_offsets(
            ciphertext='a',
            rotor_pattern=['?'],
            plugboard_map={},
            dict_words=['a'],
            top_n=3
        )
        # best is score=1, offset=(25,), plaintext='a'
        self.assertEqual(results[0][0], 1)
        self.assertEqual(results[0][1], (25,))
        self.assertEqual(results[0][2], 'a')

    def test_guess_offsets_larger_phrase(self):
        """
        Larger, deterministic case:
        - Choose a plaintext with multiple dictionary words
        - Encrypt it locally with the same stepping convention
        - Ensure guess_offsets recovers the right offsets and plaintext
        """
        target_offsets = (0, 6)  # two-rotor case keeps brute force to 26*26
        plaintext = "attack at dawn"
        ciphertext = self.encrypt_with_stepping(plaintext, target_offsets)

        results = guess_offsets(
            ciphertext=ciphertext,
            rotor_pattern=['?', '?'],
            plugboard_map={},  # keep empty to match helper
            dict_words=['attack', 'at', 'dawn'],
            top_n=3
        )

        # Top candidate should be the true one
        self.assertGreaterEqual(results[0][0], 3)             # matched all three words
        self.assertEqual(results[0][1], target_offsets)        # recovered offsets
        self.assertEqual(results[0][2], plaintext)             # recovered plaintext


if __name__ == "__main__":
    unittest.main()

