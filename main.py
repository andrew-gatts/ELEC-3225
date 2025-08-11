#!/usr/bin/env python3
"""
Unified Tk GUI for Enigma + Bombe that calls your real module functions.

- Uses enigma.encrypt_message / enigma.decrypt_message (and DB_PATH if provided)
- Uses bombe.guess_offsets
- Avoids duplicating crypto logic in the GUI
- Allows pushing Bombe results back into the Enigma window

Project layout expected:
  <root>/
    enigma/
      __init__.py
      enigma.py        # exposes encrypt_message, decrypt_message, (optionally DB_PATH)
      rotor.py         # exposes class Rotor(offset:int)
      plugboard.py     # exposes class Plugboard (has a .letters list mapping)
    bombe/
      __init__.py
      bombe.py         # exposes guess_offsets
    gui.py             # (this file)

Run:
  python3 gui.py
"""
from __future__ import annotations

import re
import string
import tkinter as tk
from tkinter import messagebox, ttk

# --- Import your real library code ---
try:
    from enigma.enigma import (
        encrypt_message as enigma_encrypt,
        decrypt_message as enigma_decrypt,
    )
    try:
        # Prefer pulling DB_PATH from enigma.enigma if it exists
        from enigma.enigma import DB_PATH as ENIGMA_DB_PATH  # type: ignore
    except Exception:
        ENIGMA_DB_PATH = None  # some versions may not export this
    from enigma.rotor import Rotor as ERotor
    from enigma.plugboard import Plugboard as EPlugboard
except Exception as e:  # soft-fail so GUI can show a friendly error
    enigma_encrypt = None
    enigma_decrypt = None
    ENIGMA_DB_PATH = None
    ERotor = None
    EPlugboard = None

try:
    from bombe.bombe import guess_offsets as bombe_guess_offsets
except Exception as e:  # soft-fail
    bombe_guess_offsets = None

ALPHABET = string.ascii_uppercase

# add this new import near the top with the others
import importlib

# Try to pull a default dictionary from the backend module (several common names)
BOMBE_DEFAULT_DICTIONARY: list[str]
try:
    _bombe_mod = importlib.import_module('bombe.bombe')
    _dict = None
    for name in ('DEFAULT_DICTIONARY', 'DEFAULT_WORDS', 'DICTIONARY', 'WORDS'):
        if hasattr(_bombe_mod, name):
            candidate = getattr(_bombe_mod, name)
            if isinstance(candidate, (list, tuple)) and all(isinstance(x, str) for x in candidate):
                _dict = list(candidate)
                break
    if not _dict:
        # sensible fallback if backend doesn't expose a list
        _dict = ["THE", "AND", "TO", "OF", "YOU", "IS", "IN", "THAT", "IT", "FOR"]
    # uppercase + dedup while preserving order
    seen = set()
    BOMBE_DEFAULT_DICTIONARY = []
    for w in _dict:
        u = w.upper().strip()
        if u and u not in seen:
            seen.add(u)
            BOMBE_DEFAULT_DICTIONARY.append(u)
except Exception:
    BOMBE_DEFAULT_DICTIONARY = ["THE", "AND", "TO", "OF", "YOU", "IS", "IN", "THAT", "IT", "FOR"]


# ---------- Helpers to bridge GUI state <-> your libs ----------

def _build_eplugboard_from_pairs(pairs: str):
    """Build an enigma.plugboard.Plugboard from a string like "AB CD EF".
    We set both .letters (identity with symmetric swaps) and .mapping (if present).
    """
    if EPlugboard is None:
        return None

    tokens = re.findall(r"[A-Za-z]{2}", pairs or "")
    # Identity letters mapping a..z by default
    letters = [chr(ord('a') + i) for i in range(26)]
    mapping: dict[str, str] = {}
    used: set[str] = set()

    for tok in tokens:
        a, b = tok[0].lower(), tok[1].lower()
        if a == b or a in used or b in used:
            continue
        ai, bi = ord(a) - 97, ord(b) - 97
        letters[ai] = b
        letters[bi] = a
        mapping[a] = b
        mapping[b] = a
        used.add(a)
        used.add(b)

    pb = EPlugboard()
    # Be tolerant of class shapes; set existing fields only
    try:
        pb.letters = letters  # typical in your code
    except Exception:
        pass
    try:
        pb.mapping = mapping
    except Exception:
        pass
    return pb


def _erotors_from_spinboxes(gui) -> list:
    offs = []
    for sb in gui.rotor_spinboxes:
        try:
            offs.append(int(sb.get()) % 26)
        except Exception:
            offs.append(0)
    return [ERotor(o) for o in offs]


def _pairs_from_map(pb_map: dict[str, str]) -> str:
    """Turn {'a':'b','b':'a'} into 'AB' style pairs without dupes."""
    out = []
    used: set[str] = set()
    for a, b in pb_map.items():
        if a in used or b in used:
            continue
        if a == b:
            continue
        out.append((a + b).upper())
        used.add(a)
        used.add(b)
    return " ".join(out)


def _pb_map_from_pairs(pairs: str) -> dict[str, str]:
    m: dict[str, str] = {}
    tokens = re.findall(r"[A-Za-z]{2}", pairs or "")
    used: set[str] = set()
    for tok in tokens:
        a, b = tok[0].lower(), tok[1].lower()
        if a == b or a in used or b in used:
            continue
        m[a] = b
        m[b] = a
        used.add(a)
        used.add(b)
    return m


# ---------------- Enigma Window ----------------
class EnigmaMachineGUI(tk.Toplevel):
    def __init__(self, master: tk.Misc | None = None):
        super().__init__(master)
        self.title("Python Enigma Machine Simulator")
        self.geometry("750x720")
        self.configure(bg="#333333")

        # Running plaintext buffer used for per-key typing to match CLI stepping
        self._session_plain = ""

        self._build_ui()
        self._update_rotor_display()

    # ---- UI construction ----
    def _build_ui(self):
        # Lamp Board
        out_frame = tk.LabelFrame(self, text="Lamp Board", bg="#444444", fg="white", font=("Arial", 10, "bold"))
        out_frame.pack(pady=6, padx=10, fill="x")
        self.output_display = tk.Entry(
            out_frame,
            width=3,
            font=("Courier New", 48, "bold"),
            bg="#222222",
            fg="#FFD700",
            justify="center",
            bd=3,
            relief="sunken",
        )
        self.output_display.insert(0, "")
        self.output_display.config(state="readonly")
        self.output_display.pack(pady=6, padx=6)

        # Rotor settings
        rot_frame = tk.LabelFrame(self, text="Rotor Settings", bg="#444444", fg="white", font=("Arial", 10, "bold"))
        rot_frame.pack(pady=6, padx=10, fill="x")
        self.rotor_spinboxes = []
        for i in range(3):
            tk.Label(rot_frame, text=f"Rotor {i+1} Offset:", bg="#444444", fg="white").grid(row=0, column=i * 2, padx=6, pady=5)
            sb = tk.Spinbox(rot_frame, from_=0, to=25, width=5, bg="#555555", fg="white")
            sb.grid(row=0, column=i * 2 + 1, padx=4, pady=5)
            sb.delete(0, tk.END)
            sb.insert(0, "0")
            self.rotor_spinboxes.append(sb)
        tk.Button(
            rot_frame,
            text="Set Rotors",
            command=self._set_rotors,
            bg="#666666",
            fg="white",
            font=("Arial", 9, "bold"),
        ).grid(row=0, column=6, padx=8)

        # Readout labels for current (A..Z)
        self.rotor_display_labels = []
        for i in range(3):
            lbl = tk.Label(rot_frame, text=f"R{i+1}: A", bg="#444444", fg="white")
            lbl.grid(row=1, column=i * 2, columnspan=2, pady=3)
            self.rotor_display_labels.append(lbl)

        # Plugboard
        pb_frame = tk.LabelFrame(self, text="Plugboard Settings", bg="#444444", fg="white", font=("Arial", 10, "bold"))
        pb_frame.pack(pady=6, padx=10, fill="x")
        tk.Label(pb_frame, text="Swaps (e.g., AB CD EF):", bg="#444444", fg="white").pack(side="left", padx=5)
        self.plugboard_entry = tk.Entry(pb_frame, width=32, bg="#555555", fg="white")
        self.plugboard_entry.pack(side="left", padx=5, expand=True, fill="x")
        tk.Button(pb_frame, text="Apply", command=self._set_plugboard, bg="#666666", fg="white").pack(side="left", padx=5)

        # Keyboard (QWERTY layout)
        kb_frame = tk.LabelFrame(self, text="Input Keyboard", bg="#444444", fg="white", font=("Arial", 10, "bold"))
        kb_frame.pack(pady=6, padx=10, fill="x")
        layout = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        for row in layout:
            r = tk.Frame(kb_frame, bg="#444444")
            r.pack(pady=2)
            for ch in row:
                tk.Button(
                    r,
                    text=ch,
                    width=3,
                    height=1,
                    font=("Arial", 12, "bold"),
                    bg="#777777",
                    fg="white",
                    command=lambda c=ch: self._process_char(c),
                ).pack(side="left", padx=1, pady=1)

        # Message area
        msg_frame = tk.LabelFrame(self, text="Full Message", bg="#444444", fg="white", font=("Arial", 10, "bold"))
        msg_frame.pack(pady=6, padx=10, fill="both", expand=True)

        tk.Label(msg_frame, text="Input:", bg="#444444", fg="white").pack(anchor="w", padx=6, pady=2)
        self.input_message_text = tk.Text(msg_frame, height=4, width=64, font=("Courier New", 11), bg="#222222", fg="white", insertbackground="white")
        self.input_message_text.pack(padx=6, pady=4, fill="x")

        btns = tk.Frame(msg_frame, bg="#444444")
        btns.pack(pady=4)
        tk.Button(btns, text="Encrypt", command=self._encrypt_full_message, bg="#666666", fg="white").pack(side="left", padx=6)
        tk.Button(btns, text="Decrypt", command=self._decrypt_full_message, bg="#666666", fg="white").pack(side="left", padx=6)
        tk.Button(btns, text="Clear", command=self._clear_all, bg="#666666", fg="white").pack(side="left", padx=6)
        tk.Button(btns, text="Open Bombe", command=self._open_bombe_with_current, bg="#FF5722", fg="white").pack(side="left", padx=10)

        tk.Label(msg_frame, text="Output:", bg="#444444", fg="white").pack(anchor="w", padx=6, pady=2)
        self.output_message_text = tk.Text(msg_frame, height=4, width=64, font=("Courier New", 11), bg="#222222", fg="#FFD700", state="disabled")
        self.output_message_text.pack(padx=6, pady=4, fill="x")

    # ---- Behaviors ----
    def _update_rotor_display(self):
        offs = []
        for sb in self.rotor_spinboxes:
            try:
                offs.append(int(sb.get()) % 26)
            except Exception:
                offs.append(0)
        for i, off in enumerate(offs):
            self.rotor_display_labels[i].config(text=f"R{i+1}: {ALPHABET[off]}")

    def _set_rotors(self):
        try:
            for sb in self.rotor_spinboxes:
                v = int(sb.get())
                if not (0 <= v <= 25):
                    raise ValueError
            self._update_rotor_display()
            #messagebox.showinfo("Rotor Setup", "Rotors configured successfully!")
        except Exception:
            messagebox.showerror("Input Error", "Please enter valid integer offsets (0-25).")

    def _set_plugboard(self):
        # Validation occurs on use; just acknowledge
        #messagebox.showinfo("Plugboard", "Plugboard pairs recorded. They will be applied on encrypt/decrypt.")

    def _process_char(self, ch: str):
        if enigma_encrypt is None or ERotor is None:
            messagebox.showerror("Unavailable", "enigma package not available.")
            return
        if not ch or not ch.isalpha():
            return
        self._session_plain += ch.lower()
        pb = _build_eplugboard_from_pairs(self.plugboard_entry.get())
        rotors = _erotors_from_spinboxes(self)
        try:
            # Use your real encrypt function so stepping matches CLI
            if ENIGMA_DB_PATH is not None:
                ct = enigma_encrypt(self._session_plain, rotors, pb, ENIGMA_DB_PATH)
            else:
                ct = enigma_encrypt(self._session_plain, rotors, pb)
        except TypeError:
            # if signature differs (older version)
            ct = enigma_encrypt(self._session_plain, rotors, pb)
        except Exception as e:
            messagebox.showerror("Encrypt Failed", str(e))
            return

        last = (ct[-1] if ct else "").upper()
        self.output_display.config(state="normal")
        self.output_display.delete(0, tk.END)
        self.output_display.insert(0, last)
        self.output_display.config(state="readonly")

        self.output_message_text.config(state="normal")
        self.output_message_text.delete("1.0", "end")
        self.output_message_text.insert("1.0", ct.upper())
        self.output_message_text.config(state="disabled")

    def _encrypt_full_message(self):
        if enigma_encrypt is None:
            messagebox.showerror("Unavailable", "enigma package not available.")
            return
        msg = self.input_message_text.get("1.0", "end-1c").lower()
        pb = _build_eplugboard_from_pairs(self.plugboard_entry.get())
        rotors = _erotors_from_spinboxes(self)
        try:
            if ENIGMA_DB_PATH is not None:
                ct = enigma_encrypt(msg, rotors, pb, ENIGMA_DB_PATH)
            else:
                ct = enigma_encrypt(msg, rotors, pb)
        except TypeError:
            ct = enigma_encrypt(msg, rotors, pb)
        except Exception as e:
            messagebox.showerror("Encrypt Failed", str(e))
            return
        self.output_message_text.config(state="normal")
        self.output_message_text.delete("1.0", "end")
        self.output_message_text.insert("1.0", ct.upper())
        self.output_message_text.config(state="disabled")
        self._session_plain = msg

    def _decrypt_full_message(self):
        if enigma_decrypt is None:
            messagebox.showerror("Unavailable", "enigma package not available.")
            return
        msg = self.input_message_text.get("1.0", "end-1c").lower()
        pb = _build_eplugboard_from_pairs(self.plugboard_entry.get())
        rotors = _erotors_from_spinboxes(self)
        try:
            pt = enigma_decrypt(msg, rotors, pb)
        except Exception as e:
            messagebox.showerror("Decrypt Failed", str(e))
            return
        self.output_message_text.config(state="normal")
        self.output_message_text.delete("1.0", "end")
        self.output_message_text.insert("1.0", pt.upper())
        self.output_message_text.config(state="disabled")

    def _clear_all(self):
        self.input_message_text.delete("1.0", tk.END)
        self.output_message_text.config(state="normal")
        self.output_message_text.delete("1.0", tk.END)
        self.output_message_text.config(state="disabled")
        self.output_display.config(state="normal")
        self.output_display.delete(0, tk.END)
        self.output_display.config(state="readonly")
        for sb in self.rotor_spinboxes:
            sb.delete(0, tk.END)
            sb.insert(0, "0")
        self.plugboard_entry.delete(0, tk.END)
        self._session_plain = ""
        self._update_rotor_display()
        messagebox.showinfo("Cleared", "All settings and messages cleared!")

    def _open_bombe_with_current(self):
        # Ask the master app to launch Bombe, preloading whatever is in the input box
        ct = self.output_message_text.get("1.0", "end-1c").strip().lower()
        if not ct:
            ct = self.input_message_text.get("1.0", "end-1c").strip().lower()
        pairs = self.plugboard_entry.get().strip()
        if hasattr(self.master, "_launch_bombe_with_params"):
            self.master._launch_bombe_with_params(initial_ciphertext=ct, initial_pairs=pairs)


# ---------------- Bombe Window ----------------
class BombeGUI(tk.Toplevel):
    def __init__(self, master: tk.Misc | None = None, enigma_window: EnigmaMachineGUI | None = None,
                 initial_ciphertext: str | None = None, initial_pairs: str | None = None):
        super().__init__(master)
        self.title("Bombe Machine")
        self.geometry("980x680")
        self.configure(bg="#222222")

        self.enigma_window = enigma_window
        self._last_ciphertext: str | None = None
        self._last_pb_map: dict[str, str] | None = None

        self._build_ui()

        # Prefill if provided
        if initial_ciphertext:
            self.ciphertext_entry.insert(0, initial_ciphertext)
        if initial_pairs:
            self.plugboard_entry.insert(0, initial_pairs)

    def _build_ui(self):
        main = tk.Frame(self, bg="#222222", padx=10, pady=10)
        main.pack(fill="both", expand=True)

        # --- Inputs ---
        inp = tk.LabelFrame(main, text="Bombe Settings", bg="#333333", fg="white", font=("Arial", 10, "bold"))
        inp.pack(pady=6, padx=6, fill="x")

        # ciphertext
        tk.Label(inp, text="Ciphertext:", bg="#333333", fg="white").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.ciphertext_entry = tk.Entry(inp, width=76, font=("Courier New", 10), bg="#111111", fg="white", insertbackground="white")
        self.ciphertext_entry.grid(row=0, column=1, columnspan=4, sticky="ew", padx=5, pady=3)

        # dictionary (prefilled from backend)
        tk.Label(inp, text="Dictionary Words (comma-separated):", bg="#333333", fg="white").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.dictionary_entry = tk.Entry(inp, width=76, font=("Courier New", 10), bg="#111111", fg="white", insertbackground="white")
        #self.dictionary_entry.insert(-1, ", ".join(BOMBE_DEFAULT_DICTIONARY))
        self.dictionary_entry.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=3)
        tk.Button(inp, text="Reset to Backend", command=self._reset_dictionary, bg="#555555", fg="white").grid(row=1, column=4, padx=5, pady=3)

        # plugboard
        tk.Label(inp, text="Plugboard Swaps (e.g., AB CD):", bg="#333333", fg="white").grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.plugboard_entry = tk.Entry(inp, width=76, font=("Courier New", 10), bg="#111111", fg="white", insertbackground="white")
        self.plugboard_entry.grid(row=2, column=1, columnspan=4, sticky="ew", padx=5, pady=3)

        # rotor pattern offsets (0–25 or '?'), like CLI
        tk.Label(inp, text="Rotor Offsets (0-25 or ?):", bg="#333333", fg="white").grid(row=3, column=0, sticky="w", padx=5, pady=3)
        self.r_off_1 = tk.Entry(inp, width=4, bg="#111111", fg="white", justify="center")
        self.r_off_2 = tk.Entry(inp, width=4, bg="#111111", fg="white", justify="center")
        self.r_off_3 = tk.Entry(inp, width=4, bg="#111111", fg="white", justify="center")
        for i, e in enumerate((self.r_off_1, self.r_off_2, self.r_off_3), start=1):
            e.insert(0, "?")
            e.grid(row=3, column=i, padx=2, pady=3)

        tk.Button(inp, text="Run Bombe", command=self._run_bombe,
                  bg="#555555", fg="white", font=("Arial", 10, "bold"), relief="raised").grid(row=3, column=4, padx=8, pady=3)

        # --- Results ---
        out = tk.LabelFrame(main, text="Results", bg="#333333", fg="white", font=("Arial", 10, "bold"))
        out.pack(pady=6, padx=6, fill="both", expand=True)

        cols = ("score", "offsets", "plaintext")
        self.results_view = ttk.Treeview(out, columns=cols, show="headings")
        self.results_view.heading("score", text="Score")
        self.results_view.heading("offsets", text="Offsets (r1,r2,r3)")
        self.results_view.heading("plaintext", text="Plaintext Preview")
        self.results_view.column("score", width=70, anchor="center")
        self.results_view.column("offsets", width=160, anchor="center")
        self.results_view.column("plaintext", width=700, anchor="w")
        self.results_view.pack(fill="both", expand=True, padx=6, pady=6)

        btns = tk.Frame(main, bg="#222222")
        btns.pack(fill="x", padx=6, pady=4)
        tk.Button(btns, text="Apply Selected to Enigma", command=self._apply_selected_to_enigma, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        tk.Button(btns, text="Open/Focus Enigma", command=self._ensure_enigma_window, bg="#607D8B", fg="white").pack(side="left", padx=5)

    def _reset_dictionary(self):
        self.dictionary_entry.delete(0, tk.END)
        self.dictionary_entry.insert(0, ", ".join(BOMBE_DEFAULT_DICTIONARY))

    def _ensure_enigma_window(self):
        if self.enigma_window and self.enigma_window.winfo_exists():
            try:
                self.enigma_window.deiconify()
                self.enigma_window.lift()
                self.enigma_window.focus_set()
                return
            except Exception:
                pass
        if hasattr(self.master, "_launch_enigma"):
            self.master._launch_enigma()
            self.enigma_window = getattr(self.master, "_enigma_window", None)
        else:
            messagebox.showwarning("Enigma Not Available", "Could not open the Enigma window from here.")

    def _read_rotor_pattern(self) -> list[str] | None:
        vals = [self.r_off_1.get().strip(), self.r_off_2.get().strip(), self.r_off_3.get().strip()]
        pat: list[str] = []
        for v in vals:
            if v == "":
                v = "?"
            if v != "?":
                try:
                    iv = int(v)
                except Exception:
                    messagebox.showerror("Rotor Error", f"Invalid rotor value '{v}'. Use 0-25 or '?'.")
                    return None
                if not (0 <= iv <= 25):
                    messagebox.showerror("Rotor Error", f"Rotor offset out of range: {iv} (0-25)")
                    return None
                v = str(iv)
            pat.append(v)
        return pat

    def _run_bombe(self):
        ciphertext = self.ciphertext_entry.get().strip().lower()
        dictionary_words_str = self.dictionary_entry.get().strip().lower()
        plugboard_pairs_str = self.plugboard_entry.get().strip().lower()
        if not ciphertext:
            messagebox.showwarning("Input Error", "Please enter ciphertext to analyze.")
            return

        rotor_pattern = self._read_rotor_pattern()
        if rotor_pattern is None:
            return

        # Merge backend dictionary with any extra words typed by the user (additive)
        base_words = [w.lower() for w in BOMBE_DEFAULT_DICTIONARY]
        extras = [w.strip().lower() for w in dictionary_words_str.split(',') if w.strip()]
        
        # Dedup while preserving order: backend first, then extras not already present
        seen = set(base_words)
        dict_words = list(base_words)
        for w in extras:
            if w not in seen:
                dict_words.append(w)
                seen.add(w)
        pb_map = _pb_map_from_pairs(plugboard_pairs_str)

        # Clear previous
        for iid in self.results_view.get_children():
            self.results_view.delete(iid)

        if bombe_guess_offsets is None:
            messagebox.showerror("Unavailable", "bombe.bombe not available.")
            return

        try:
            results = bombe_guess_offsets(ciphertext, rotor_pattern, pb_map, dict_words, top_n=10)
        except Exception as e:
            messagebox.showerror("Bombe Failed", str(e))
            return

        if not results:
            messagebox.showinfo("No Results", "No candidates found.")
            return

        for (score, offsets, plaintext) in results:
            preview = plaintext.strip().replace("\n", " ")
            if len(preview) > 160:
                preview = preview[:157] + "..."
            self.results_view.insert("", "end", values=(score, f"{offsets}", preview))

        self._last_ciphertext = ciphertext
        self._last_pb_map = pb_map

    def _apply_selected_to_enigma(self):
        sel = self.results_view.selection()
        if not sel:
            messagebox.showinfo("Select a Row", "Choose a result row first.")
            return
        vals = self.results_view.item(sel[0], "values")
        if len(vals) < 2:
            messagebox.showerror("Internal Error", "Selected row has no offsets.")
            return
        offsets_text = vals[1]  # e.g. "(3, 17, 8)"
        try:
            nums = [int(x) for x in re.findall(r"-?\d+", offsets_text)]
            if len(nums) != 3:
                raise ValueError
            offsets = tuple(n % 26 for n in nums)
        except Exception:
            messagebox.showerror("Parse Error", f"Could not parse offsets: {offsets_text}")
            return

        self._ensure_enigma_window()
        enigma = self.enigma_window
        if not enigma or not enigma.winfo_exists():
            messagebox.showwarning("Enigma Not Available", "Open the Enigma window first.")
            return

        # apply offsets to Enigma spinboxes
        try:
            for i, off in enumerate(offsets):
                sb = enigma.rotor_spinboxes[i]
                sb.delete(0, tk.END)
                sb.insert(0, str(off))
            enigma._update_rotor_display()
        except Exception as e:
            messagebox.showerror("Rotor Error", f"Failed to apply offsets: {e}")
            return

        # apply plugboard from last run
        try:
            pairs_str = _pairs_from_map(self._last_pb_map or {})
            enigma.plugboard_entry.delete(0, tk.END)
            enigma.plugboard_entry.insert(0, pairs_str)
            enigma._set_plugboard()
        except Exception as e:
            messagebox.showerror("Plugboard Error", f"Failed to apply plugboard: {e}")
            return

        # decrypt in Enigma window
        try:
            if self._last_ciphertext:
                enigma.input_message_text.delete("1.0", "end")
                enigma.input_message_text.insert("1.0", self._last_ciphertext.upper())
                enigma._decrypt_full_message()
                messagebox.showinfo("Applied", f"Applied offsets {offsets} and plugboard to Enigma and ran decrypt.")
        except Exception as e:
            messagebox.showerror("Decrypt Error", f"Failed to decrypt in Enigma: {e}")

    def _ensure_enigma_window(self):
        if self.enigma_window and self.enigma_window.winfo_exists():
            try:
                self.enigma_window.deiconify()
                self.enigma_window.lift()
                self.enigma_window.focus_set()
                return
            except Exception:
                pass
        # Ask the main app to create/focus one
        if hasattr(self.master, "_launch_enigma"):
            self.master._launch_enigma()
            self.enigma_window = getattr(self.master, "_enigma_window", None)
        else:
            messagebox.showwarning("Enigma Not Available", "Could not open the Enigma window from here.")

    """def _run_bombe(self):
        ciphertext = self.ciphertext_entry.get().strip().lower()
        dictionary_words_str = self.dictionary_entry.get().strip().lower()
        plugboard_pairs_str = self.plugboard_entry.get().strip().lower()
        if not ciphertext:
            messagebox.showwarning("Input Error", "Please enter ciphertext to analyze.")
            return
        dict_words = [w.strip() for w in dictionary_words_str.split(',') if w.strip()] or [w.lower() for w in self.default_dictionary]
        pb_map = _pb_map_from_pairs(plugboard_pairs_str)

        # Clear previous
        for iid in self.results_view.get_children():
            self.results_view.delete(iid)

        if bombe_guess_offsets is None:
            messagebox.showerror("Unavailable", "bombe.bombe not available.")
            return

        try:
            results = bombe_guess_offsets(ciphertext, ['?','?','?'], pb_map, dict_words, top_n=10)
        except Exception as e:
            messagebox.showerror("Bombe Failed", str(e))
            return

        if not results:
            messagebox.showinfo("No Results", "No candidates found.")
            return

        for (score, offsets, plaintext) in results:
            preview = plaintext.strip().replace("\n", " ")
            if len(preview) > 140:
                preview = preview[:137] + "..."
            self.results_view.insert("", "end", values=(score, f"{offsets}", preview))

        self._last_ciphertext = ciphertext
        self._last_pb_map = pb_map"""

    def _apply_selected_to_enigma(self):
        sel = self.results_view.selection()
        if not sel:
            messagebox.showinfo("Select a Row", "Choose a result row first.")
            return
        vals = self.results_view.item(sel[0], "values")
        if len(vals) < 2:
            messagebox.showerror("Internal Error", "Selected row has no offsets.")
            return
        offsets_text = vals[1]  # e.g. "(3, 17, 8)"
        try:
            # Safe parse: pull integers out of the tuple string
            nums = [int(x) for x in re.findall(r"-?\d+", offsets_text)]
            if len(nums) != 3:
                raise ValueError
            offsets = tuple(n % 26 for n in nums)
        except Exception:
            messagebox.showerror("Parse Error", f"Could not parse offsets: {offsets_text}")
            return

        self._ensure_enigma_window()
        enigma = self.enigma_window
        if not enigma or not enigma.winfo_exists():
            messagebox.showwarning("Enigma Not Available", "Open the Enigma window first.")
            return

        # Apply offsets to spinboxes
        try:
            for i, off in enumerate(offsets):
                sb = enigma.rotor_spinboxes[i]
                sb.delete(0, tk.END)
                sb.insert(0, str(off))
            enigma._update_rotor_display()
        except Exception as e:
            messagebox.showerror("Rotor Error", f"Failed to apply offsets: {e}")
            return

        # Apply plugboard pairs reconstructed from last run
        try:
            pairs_str = _pairs_from_map(self._last_pb_map or {})
            enigma.plugboard_entry.delete(0, tk.END)
            enigma.plugboard_entry.insert(0, pairs_str)
            enigma._set_plugboard()
        except Exception as e:
            messagebox.showerror("Plugboard Error", f"Failed to apply plugboard: {e}")
            return

        # Put ciphertext into Enigma and decrypt
        try:
            if self._last_ciphertext:
                enigma.input_message_text.delete("1.0", "end")
                enigma.input_message_text.insert("1.0", self._last_ciphertext.upper())
                enigma._decrypt_full_message()
                messagebox.showinfo("Applied", f"Applied offsets {offsets} and plugboard to Enigma and ran decrypt.")
        except Exception as e:
            messagebox.showerror("Decrypt Error", f"Failed to decrypt in Enigma: {e}")


# ---------------- Main launcher ----------------
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enigma Tools")
        self.geometry("320x220")
        self.configure(bg="#1A1A1A")

        self._enigma_window: EnigmaMachineGUI | None = None

        main_frame = tk.Frame(self, bg="#1A1A1A", padx=20, pady=20)
        main_frame.pack(expand=True)

        tk.Label(main_frame, text="Select a Tool:", bg="#1A1A1A", fg="white", font=("Arial", 14, "bold")).pack(pady=14)

        tk.Button(
            main_frame,
            text="Enigma Machine",
            command=self._launch_enigma,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            padx=10,
            pady=5,
        ).pack(pady=8)

        tk.Button(
            main_frame,
            text="Bombe Machine",
            command=self._launch_bombe,
            bg="#FF5722",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            padx=10,
            pady=5,
        ).pack(pady=8)

    # Launchers
    def _launch_enigma(self):
        if self._enigma_window and self._enigma_window.winfo_exists():
            self._enigma_window.deiconify()
            self._enigma_window.lift()
            self._enigma_window.focus_set()
            return
        self._enigma_window = EnigmaMachineGUI(self)
        self._enigma_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: (self._enigma_window.destroy(), setattr(self, "_enigma_window", None)),
        )
        self._enigma_window.grab_set()
        self._enigma_window.wait_visibility()
        self._enigma_window.focus_set()

    def _launch_bombe(self):
        b = BombeGUI(self, enigma_window=self._enigma_window)
        b.grab_set()
        b.wait_window(b)

    def _launch_bombe_with_params(self, initial_ciphertext: str | None, initial_pairs: str | None):
        b = BombeGUI(self, enigma_window=self._enigma_window, initial_ciphertext=initial_ciphertext, initial_pairs=initial_pairs)
        b.grab_set()
        b.wait_window(b)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

