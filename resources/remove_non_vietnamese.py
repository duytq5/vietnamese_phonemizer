# -*- coding: utf-8 -*-
# This script removes non-Vietnamese words from VDic_uni.txt and VDic_uni_<x>.txt files in VDic_uni_split
# It validates tokens by Vietnamese syllable structure:
#   syllable = [onset] + [medial] + nucleus + [coda]
# and enforces tone <-> coda compatibility:
#   - syllables ending in stops (p, t, c/ch) are allowed only with "sắc" or "nặng" tones.

import os
import re
import unicodedata

# --- Configuration: phonotactic pieces (orthographic forms) ---
ONSETS = [
    "ngh", "ng", "gh", "kh", "ph", "th", "tr", "ch", "qu",  # multi-letter onsets first
    "b", "c", "d", "đ", "g", "h", "k", "l", "m", "n", "nh",
    "p", "r", "s", "t", "v", "x", ""
]

MEDIALS = ["", "o", "u"]  # medial (glide) allowed after onset, except when onset == "qu"

# Basic vowel inventory and common diphthongs/triphthongs (orthographic forms after tone removal)
NUCLEI = set([
    # simple vowels
    "a", "ă", "â", "e", "ê", "i", "o", "ô", "ơ", "u", "ư", "y",
    # common diphthongs/triphthongs (not exhaustively enumerated but covers usual patterns)
    "ai","ay","ao","au","âu","ây",
    "oi","ôi","ơi","oe","uê","ui","uy",
    "ia","iê","iu","ya","yê",
    "ua","uô","uơ","ưa","ươ","uâ",
    "oa","oă","oe","oai","oay","oă",
    "êu","eo","êu",
    # allow simple single vowel as well (already above)
])

CODAS = ["ch", "ng", "nh", "c", "m", "n", "p", "t", ""]  # coda list with multi-letter forms first

# codas that are oral stops and restrict tones
STOP_CODAS = {"p", "t", "c", "ch"}

# quick set of base vowel characters used for nucleus validation (after tone removal)
VOWEL_BASES = set(list("aăâeêioôơuưy"))

# regex to roughly ensure tokens contain only letters/punctuation we expect (reject digits/punct-heavy tokens)
# keeps Vietnamese letters (precomposed) and ASCII letters and hyphen (we'll reject hyphenated tokens later).
TOKEN_ALPHABET_RE = re.compile(r"^[\w\-\u00C0-\u1EF9]+$", re.UNICODE)

# tone combining marks (NFD combining characters)
_TONE_MARKS = {"\u0300", "\u0301", "\u0303", "\u0309", "\u0323"}  # huyền, sắc, ngã, hỏi, nặng


BLACKLIST = {"cy", "qy", "py"}  # add more as discovered


def get_tone(token: str) -> str:
    """
    Return the tone name for the given token.
    If no tone mark found, returns 'ngang'.
    Possible returns: 'ngang', 'sắc', 'huyền', 'hỏi', 'ngã', 'nặng'
    """
    for ch in token:
        decomp = unicodedata.normalize("NFD", ch)
        for comb in decomp[1:]:
            if comb == "\u0301":
                return "sắc"
            if comb == "\u0300":
                return "huyền"
            if comb == "\u0309":
                return "hỏi"
            if comb == "\u0303":
                return "ngã"
            if comb == "\u0323":
                return "nặng"
    return "ngang"

def remove_tone_marks(token: str) -> str:
    """
    Remove only Vietnamese tone combining marks from a token while keeping other diacritics
    (breve, circumflex, horn, etc.). Implementation:
      - NFD normalize each character,
      - drop combining characters that are tone marks (0300,0301,0303,0309,0323),
      - NFC recompose.
    """
    out_chars = []
    for ch in token:
        decomp = unicodedata.normalize("NFD", ch)
        filtered = ''.join(c for c in decomp if c not in _TONE_MARKS)
        recomposed = unicodedata.normalize("NFC", filtered)
        out_chars.append(recomposed)
    return ''.join(out_chars)

def is_vietnamese_syllable(token: str) -> bool:
    """Check whether a single-token string is a valid Vietnamese syllable."""
    if not token or not token.strip():
        return False

    if not TOKEN_ALPHABET_RE.match(token):
        return False
    if "-" in token:
        return False

    tone = get_tone(token)
    base = remove_tone_marks(token).lower()

    for onset in sorted(ONSETS, key=len, reverse=True):
        if not base.startswith(onset):
            continue
        rest_after_onset = base[len(onset):]

        for coda in sorted(CODAS, key=len, reverse=True):
            if not rest_after_onset.endswith(coda):
                continue
            core = rest_after_onset[:len(rest_after_onset)-len(coda)] if coda else rest_after_onset

            allowed_medials = [""] if onset == "qu" else MEDIALS
            for medial in allowed_medials:
                if not core.startswith(medial):
                    continue
                nucleus = core[len(medial):]
                if not nucleus:
                    continue

                # --- Rule 3: nucleus must be valid ---
                if nucleus not in NUCLEI:
                    continue

                # --- Rule 1: onset–nucleus compatibility ---
                if onset == "c" and nucleus[0] in ("i", "e", "ê", "y"):
                    return False
                if onset == "k" and nucleus[0] not in ("i", "e", "ê"):
                    return False
                if onset in ("g", "ng") and nucleus[0] in ("e", "ê", "i"):
                    return False
                if onset in ("gh", "ngh") and nucleus[0] not in ("e", "ê", "i"):
                    return False
                if onset == "q" and not core.startswith("u"):
                    return False

                # --- Rule 4: y usage ---
                if nucleus == "y" and onset not in ("", "ng", "th", "tr"):
                    return False

                # --- Rule 2: tone–coda compatibility ---
                if coda in STOP_CODAS and tone not in ("sắc", "nặng"):
                    return False

                # Passed all rules
                return True

    return False


def all_words_vietnamese(text: str) -> bool:
    """
    Return True if every whitespace-separated token in text is a valid Vietnamese syllable.
    (This function treats each token as a syllable; multi-syllable tokens or phrases should be split.)
    """
    tokens = [t for t in text.strip().split() if t]
    return all(is_vietnamese_word(t) for t in tokens) if tokens else False


def is_vietnamese_word(token: str) -> bool:
    """Final check: valid syllable structure, tone rules, and not blacklisted."""
    if not is_vietnamese_syllable(token):
        return False
    # if remove_tone_marks(token).lower() in BLACKLIST:
    #     return False
    return True

# === Dictionary Cleaning ===
base_dir = os.path.dirname(__file__)  # folder where this script is located
input_path = os.path.join(base_dir, "VDic_uni.txt")
output_path = os.path.join(base_dir, "VDic_uni_vietnamese.txt")

with open(input_path, encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for line in infile:
        if not line.strip():
            continue
        word = line.split("\t")[0].strip()
        if all_words_vietnamese(word):
            outfile.write(line)

# Clean the split files as well
split_dir = os.path.join(base_dir, "VDic_uni_split")
if os.path.isdir(split_dir):
    for fname in os.listdir(split_dir):
        if not fname.startswith("VDic_uni_") or not fname.endswith(".txt"):
            continue
        fpath = os.path.join(split_dir, fname)
        with open(fpath, encoding="utf-8") as infile:
            lines = infile.readlines()
        kept = []
        for line in lines:
            fields = line.strip().split("\t")
            word = fields[0].strip() if fields else ""
            if all_words_vietnamese(word):
                kept.append(line)
        with open(fpath, "w", encoding="utf-8") as outfile:
            outfile.writelines(kept)

print("Done. Cleaned file written to VDic_uni_vietnamese.txt and split files updated.")
