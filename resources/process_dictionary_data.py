# -*- coding: utf-8 -*-
# This script removes non-Vietnamese words from VDic_uni.txt
# It validates tokens by Vietnamese syllable structure:
#   syllable = [onset] + [medial] + nucleus + [coda]
# and enforces tone <-> coda compatibility:
#   - syllables ending in stops (p, t, c/ch) are allowed only with "sắc" or "nặng" tones.

import os
import re
import unicodedata

# --- Configuration: phonotactic pieces (orthographic forms) ---
ONSETS = [
    "ngh", "ng", "gh", "kh", "ph", "th", "tr", "ch", "qu",
    "b", "c", "d", "đ", "g", "h", "k", "l", "m", "n", "nh",
    "p", "r", "s", "t", "v", "x", ""
]

MEDIALS = ["", "o", "u"]

NUCLEI = set([
    "a","ă","â","e","ê","i","o","ô","ơ","u","ư","y",
    "ai","ay","ao","au","âu","ây",
    "oi","ôi","ơi","oe","uê","ui","uy",
    "ia","iê","iu","ya","yê",
    "ua","uô","uơ","ưa","ươ","uâ",
    "oa","oă","oe","oai","oay","oă",
    "êu","eo","êu",
])

CODAS = ["ch","ng","nh","c","m","n","p","t",""]

STOP_CODAS = {"p","t","c","ch"}

VOWEL_BASES = set(list("aăâeêioôơuưy"))

TOKEN_ALPHABET_RE = re.compile(r"^[\w\-\u00C0-\u1EF9]+$", re.UNICODE)

_TONE_MARKS = {"\u0300","\u0301","\u0303","\u0309","\u0323"}


def get_tone(token: str) -> str:
    for ch in token:
        decomp = unicodedata.normalize("NFD", ch)
        for comb in decomp[1:]:
            if comb == "\u0301": return "sắc"
            if comb == "\u0300": return "huyền"
            if comb == "\u0309": return "hỏi"
            if comb == "\u0303": return "ngã"
            if comb == "\u0323": return "nặng"
    return "ngang"

def remove_tone_marks(token: str) -> str:
    out_chars = []
    for ch in token:
        decomp = unicodedata.normalize("NFD", ch)
        filtered = ''.join(c for c in decomp if c not in _TONE_MARKS)
        recomposed = unicodedata.normalize("NFC", filtered)
        out_chars.append(recomposed)
    return ''.join(out_chars)

def is_vietnamese_syllable(token: str) -> bool:
    if not token or not token.strip(): return False
    if not TOKEN_ALPHABET_RE.match(token): return False
    if "-" in token: return False

    tone = get_tone(token)
    base = remove_tone_marks(token).lower()

    for onset in sorted(ONSETS, key=len, reverse=True):
        if not base.startswith(onset): continue
        rest_after_onset = base[len(onset):]

        for coda in sorted(CODAS, key=len, reverse=True):
            if not rest_after_onset.endswith(coda): continue
            core = rest_after_onset[:len(rest_after_onset)-len(coda)] if coda else rest_after_onset

            allowed_medials = [""] if onset == "qu" else MEDIALS
            for medial in allowed_medials:
                if not core.startswith(medial): continue
                nucleus = core[len(medial):]
                if not nucleus: continue

                if nucleus not in NUCLEI: continue

                if onset == "c" and nucleus[0] in ("i","e","ê","y"): return False
                if onset == "k" and nucleus[0] not in ("i","e","ê"): return False
                if onset in ("g","ng") and nucleus[0] in ("e","ê","i"): return False
                if onset in ("gh","ngh") and nucleus[0] not in ("e","ê","i"): return False
                if onset == "q" and not core.startswith("u"): return False

                if nucleus == "y" and onset not in ("","ng","th","tr"): return False
                if coda in STOP_CODAS and tone not in ("sắc","nặng"): return False

                return True
    return False

def is_vietnamese_word(token: str) -> bool:
    return is_vietnamese_syllable(token)

def all_words_vietnamese(text: str) -> bool:
    tokens = [t for t in text.strip().split() if t]
    return all(is_vietnamese_word(t) for t in tokens) if tokens else False

# === Dictionary Cleaning ===
base_dir = os.path.dirname(__file__)
input_path = os.path.join(base_dir, "VDic_uni.txt")
output_path = os.path.join(base_dir, "VDic_uni_vietnamese.txt")

with open(input_path, encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for line in infile:
        if not line.strip(): continue
        word = line.split("\t")[0].strip()
        if all_words_vietnamese(word):
            outfile.write(line.lower())

print("Done. Cleaned file written to VDic_uni_vietnamese.txt.")
