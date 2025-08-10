#!/usr/bin/env python3
from itertools import product
import re

# ------------------------- ROTOR -------------------------
class Rotor:
    def __init__(self, offset: int = 0):
        # Creates an array of all of the letters
        self.letters = [chr(i + ord('a')) for i in range(26)]
        self.offset = offset % 26

    def set_offset(self, offset: int):
        self.offset = offset % 26

    def get_offset(self) -> int:
        return self.offset

    def decrypt(self, encrypted_message: str) -> str:
        # Decrypt function to undo the encryption
        decrypted = []
        prev_enc_index = None  # index of previous encrypted letter (after all processing)

        for char in encrypted_message.lower():
            if char in self.letters:
                cur_enc_index = self.letters.index(char)

                # assume no bump
                orig_index = (cur_enc_index - self.offset) % 26
                pre_bump_index = (orig_index + self.offset) % 26

                # if a bump happened during encryption, then the pre_bump result
                # equals the previous encrypted letter index
                if prev_enc_index is not None and pre_bump_index == prev_enc_index:
                    # undo the +1 bump
                    orig_index = (cur_enc_index - 0 - self.offset) % 26

                decrypted.append(self.letters[orig_index])
                prev_enc_index = cur_enc_index
            else:
                decrypted.append(char)
                prev_enc_index = None

        return ''.join(decrypted)

    def show_position(self):
        return self.offset


# ------------------------- PLUGBOARD -------------------------
def add_mapping(plugboard_map: dict, a: str, b: str) -> bool:
    # Add symmetric mapping a<->b if neither is already used
    a = a.lower(); b = b.lower()
    if a in plugboard_map or b in plugboard_map:
        return False
    plugboard_map[a] = b
    plugboard_map[b] = a
    return True


def plugboard_apply(text: str, plugboard_map: dict) -> str:
    return ''.join(plugboard_map.get(ch, ch) for ch in text.lower())


def decrypt_message(ciphertext: str, rotors: list[Rotor], plugboard_map: dict) -> str:
    # Undo plugboard first
    msg = plugboard_apply(ciphertext, plugboard_map)
    # Backwards through rotors using decrypt
    for r in reversed(rotors):
        msg = r.decrypt(msg)
    # Final plugboard
    msg = plugboard_apply(msg, plugboard_map)
    return msg


# ------------------------- GUESSING UTILITIES -------------------------
def expand_unknowns(pattern_list):
    # pattern_list like ['?', '5', '?'] -> iterator of all tuples
    iterables = []
    for p in pattern_list:
        if p == "?":
            iterables.append(range(26))
        else:
            iterables.append([int(p) % 26])
    return product(*iterables)


def score_plaintext(pt: str, words: list[str]) -> int:
    # Simple word counter using word boundaries
    pt_up = pt.upper()
    count = 0
    for w in words:
        if not w:
            continue
        if re.search(r"\b" + re.escape(w.upper()) + r"\b", pt_up):
            count += 1
    return count


def guess_offsets(ciphertext: str,
                  rotor_pattern: list[str],
                  plugboard_map: dict,
                  dict_words: list[str],
                  top_n: int = 10) -> list[tuple[int, tuple[int, ...], str]]:
    # Brute-force unknown offsets. Returns top_n results sorted by score.
    # Each result is (score, offsets_tuple, plaintext)
    results = []
    for combo in expand_unknowns(rotor_pattern):
        # Build rotors fresh for each combo
        rotors = [Rotor(o) for o in combo]
        pt = decrypt_message(ciphertext, rotors, plugboard_map)
        s = score_plaintext(pt, dict_words)
        results.append((s, combo, pt))

    results.sort(key=lambda x: (-x[0], x[1]))

    print(f"\nTop {top_n} candidates:")
    for s, combo, pt in results[:top_n]:
        print(f"Offsets {combo} | Score={s}\n{pt}\n")

    return results[:top_n]


# ------------------------- CLI / MAIN -------------------------
def array_match():
    # Replicates the earlier array_Match idea: compare ciphertext against a crib and list mismatches.
    message_crypt = input("Type in the enigma message you wish to decrypt: ").lower()
    decoder_machine = input("What do you think the message is (crib)? ").lower()

    crypt_len = len([c for c in message_crypt if c.isalpha()])
    guess_len = len([c for c in decoder_machine if c.isalpha()])
    diff = crypt_len - guess_len
    print("Length difference:", diff)

    poss_combo = []
    for y in range(diff + 1):
        for x in range(y, guess_len + y):
            if x < len(message_crypt) and (x - y) < len(decoder_machine):
                if message_crypt[x].isalpha() and decoder_machine[x - y].isalpha():
                    if message_crypt[x] != decoder_machine[x - y]:
                        poss_combo.append([message_crypt[x], decoder_machine[x - y]])
    print("Possible pairs:", poss_combo)
    return poss_combo

# -------------------------- MAIN --------------------------
def main():
    print("\n === Bombe ===")
    plugboard = {}

    # default: 3 rotors, offsets unknown initially
    rotor_pattern = ["0", "0", "0"]

    # Initialize choice at 1 to get menu (anything but 0)
    choice = 1

    while choice != 0:
        print("\nMenu:\n"
              " 1) Set rotor offsets (use ? for unknowns)\n"
              " 2) Enter plugboard pairs\n"
              " 4) Decrypt message\n"
              " 5) Guess unknown offsets\n"
              " 6) Crib helper (array_match)\n"
              " 0) Quit")
        choice = int(input("Select: "))

        match choice:
            case 1:
                r1 = input("Rotor 1 offset (0-25 or ?): ").strip()
                r2 = input("Rotor 2 offset (0-25 or ?): ").strip()
                r3 = input("Rotor 3 offset (0-25 or ?): ").strip()
                rotor_pattern = [r1, r2, r3]
                print("Pattern set:", rotor_pattern)

            case 2:
                while True:
                    pair = input("Add plugboard pair (e.g. AB), blank to stop: ").lower().strip()
                    if not pair:
                        break
                    if len(pair) != 2 or not pair.isalpha():
                        print("Invalid pair")
                        continue
                    if add_mapping(plugboard, pair[0], pair[1]):
                        print("Added:", pair)
                    else:
                        print("Already mapped or invalid")



            case 4:  
                ct = input("Ciphertext: ")
                if '?' in rotor_pattern:
                    print("You have unknown offsets. Set them or use guessing.")
                    continue
                offsets = [int(x) % 26 for x in rotor_pattern]
                rotors = [Rotor(o) for o in offsets]
                pt = decrypt_message(ct, rotors, plugboard)
                print("Plaintext:", pt)

            case 5:
                ct = input("Ciphertext to test: ")
                pat_in = input("Pattern (comma-separated, ?=unknown) or blank to reuse current: ").strip()
                if pat_in:
                    rotor_pattern = [p.strip() for p in pat_in.split(',')]

                words_in = input("Dictionary words comma-separated (blank = default): ").strip()
                if words_in:
                    dict_words = [w.strip() for w in words_in.split(',') if w.strip()]
                else:
                    dict_words = ["THE", "AND", "TO", "OF", "YOU", "IS", "IN", "THAT", "IT", "FOR"]

                top_n = input("Show top how many? [10]: ").strip() or '10'
                top_n = int(top_n)

                guess_offsets(ct, rotor_pattern, plugboard, dict_words, top_n)

            case 6:
                array_match()

            case _:
                print("Unknown choice.")

    print("Bye!")


if __name__ == '__main__':
    main()
