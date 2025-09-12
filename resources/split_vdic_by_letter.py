# This script splits VDic_uni.txt into multiple files by first letter
import os
import string

input_path = r"c:\Workspace\HCMUS\Voice Processing\vietnamese_phonemizer\resources\VDic_uni.txt"
out_dir = r"c:\Workspace\HCMUS\Voice Processing\vietnamese_phonemizer\resources\VDic_uni_split"

# Prepare file handles for each letter
def get_postfix(word):
    # Remove leading whitespace and get first character (case-insensitive)
    word = word.strip()
    if not word:
        return None
    c = word[0].lower()
    if c in string.ascii_lowercase:
        return c
    elif c.isalpha():
        return c
    else:
        return 'other'

handles = {}

with open(input_path, encoding="utf-8") as infile:
    for line in infile:
        if not line.strip():
            continue
        word = line.split("\t")[0]
        postfix = get_postfix(word)
        if postfix is None:
            postfix = 'other'
        out_path = os.path.join(out_dir, f"VDic_uni_{postfix}.txt")
        if postfix not in handles:
            handles[postfix] = open(out_path, "w", encoding="utf-8")
        handles[postfix].write(line)

for f in handles.values():
    f.close()
print("Done splitting VDic_uni.txt by first letter.")
