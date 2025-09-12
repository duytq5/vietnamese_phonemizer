# This script removes non-Vietnamese words from VDic_uni_<x>.txt files in VDic_uni_split
# It uses a regex-based heuristic for Vietnamese words, NOT just skipping 'Np'.
import os
import re
import os
import re

# Vietnamese word pattern: letters (with diacritics), spaces, hyphens
vietnamese_pattern = re.compile(r"^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ\s]+$")

def contains_vietnamese_vowel(s):
    # Danh sách nguyên âm tiếng Việt (cả chữ thường và chữ hoa)
    vowels = "aăâeêioôơuưyAĂÂEÊIOÔƠUƯY"
    # Kiểm tra từng ký tự trong chuỗi
    for char in s:
        if char in vowels:
            return True
    return False


def is_vietnamese_word(word):
    # Remove words with hyphen
    if '-' in word:
        return False
    if not contains_vietnamese_vowel(word):
        return False

    # Remove words containing z, f, w, j (case-insensitive)
    if any(c in word.lower() for c in ['z', 'f', 'w', 'j']):
        return False

    # Common non-Vietnamese patterns (deduplicated)
    non_vn_patterns = [
        # 1. Cụm phụ âm đầu không có trong tiếng Việt
    "br","bl","cl","cr","dr","fr","gr","pr","trh",
    "sk","sl","sm","sn","sp","sq","sr","st","sv","sw",
    "gl","gn","kn","kr","pl","pn","ps","pt","wr","wh",
    "xk","xr","xt","xz","zz","fl","vl","zl","ml","ql",

    # 2. Cụm phụ âm cuối không tồn tại trong tiếng Việt
    "mb","mp","nd","nt","ngh","nk","nc","nhk","nhs","nhc","nhm","nhn",
    "ld","lk","lm","ln","lp","lt","lv","lz","lx",
    "rb","rd","rg","rk","rl","rm","rn","rp","rs","rt","rv","rx",
    "sb","sd","sg","sk","sl","sm","sn","sp","sr","st","sv","sx","sz",
    "tb","tc","td","tf","tg","tk","tl","tm","tn","tp","tr","ts","tv","tx","tz",
    "zz","xx","ss","vv","ff","dd","bb","cc","gg","hh","jj","kk","ll","mm","nn","pp","qq","rr","yy",

    # 3. Cụm phụ âm ba (triple clusters – không có trong TV)
    "str","spl","spr","scr","shr","skl","scl","smr",
    "trn","trm","trd","grd","grm","grn","drm","drn","drd",
    "brn","brm","brd","crn","crm","crd","frn","frm","frd",
    "prn","prm","prd","krn","krm","krd","pln","plm","pld",

    # 4. Cụm với phụ âm Đ/đ không tồn tại
    "đr","đl","đm","đn","đp","đt","đv","đx","đg","đh","đk","đs","đq","đz",
    "rd","ld","md","nd","sd","td","vd","zd","qd",

        # 2. Nguyên âm bất hợp lệ
         # u + phụ âm không hợp lệ
    "ub", "ud", "uđ", "ug", "uh", "uk", "ul", "uq", "ur", "us", "uv", "ux", "uz", "uf", "uw", "uj",

    # e +
    "eb", "ed", "eđ", "eg", "eh", "ek", "el", "eq", "er", "es", "ev", "ex", "ez", "ef", "ew", "ej",

    # o +
    "ob", "od", "ođ", "og", "oh", "ok", "ol", "oq", "or", "os", "ov", "ox", "oz", "of", "ow", "oj",

    # a +
    "ab", "ad", "ađ", "ag", "ah", "ak", "al", "aq", "ar", "as", "av", "ax", "az", "af", "aw", "aj",

    # i +
    "ib", "id", "iđ", "ig", "ih", "ik", "il", "iq", "ir", "is", "iv", "ix", "iz", "if", "iw", "ij",

    # y +
    "yb", "yd", "yđ", "yg", "yh", "yk", "yl", "yq", "yr", "ys", "yv", "yx", "yz", "yf", "yw", "yj",

        # 3. Vần/chuỗi ngoại lai
        "ar", "or", "ur", "yl", "og", "oó", "axit", "yu",
        "aa", "aă", "aâ", "ae", "aê", "ai", "ao", "aô", "aơ", "au", "aư", "ay",
    "ăa", "ăă", "ăâ", "ăe", "ăê", "ăi", "ăo", "ăô", "ăơ", "ău", "ăư", "ăy",
    "âa", "âă", "ââ", "âe", "âê", "âi", "âo", "âô", "âơ", "âu", "âư", "ây",
    "ee", "ei", "eo", "eô", "eơ", "eu", "eư", "ey",
    "êa", "êă", "êâ", "ee", "êê", "êi", "êo", "êô", "êơ", "êu", "êư", "êy",
    "ii", "io", "iô", "iơ", "iu", "iư", "iy",
    "oo", "oô", "oơ", "ou", "oư", "oy",
    "ôa", "ôă", "ôâ", "ôe", "ôi", "ôo", "ôô", "ôơ", "ôu", "ôư", "ôy",
    "ơa", "ơă", "ơâ", "ơe", "ơi", "ơo", "ơô", "ơơ", "ơu", "ơư", "ơy",
    "uu", "uy", "uâ", "uă", "ue", "uê", "uo", "uô", "uơ", "uư",
    "ưa", "ưă", "ưâ", "ưe", "ưê", "ưi", "ưo", "ưô", "ươ", "ưu", "ươ", "ưy",
    "yy",

    # Phụ âm đứng liền nhau không hợp lệ
    "bb","cc","dd","ff","gg","hh","jj","kk","ll","mm","nn",
    "pp","qq","rr","ss","tt","vv","ww","xx","yy","zz",
    
    # Một số tổ hợp phụ âm không có trong tiếng Việt
    "bk","dq","fx","gz","hz","jt","kv","lw","mz","pq","rx","sy","tz",

        # 4. Âm tiết kết thúc sai thanh
        "ut", "et", "ot", "at", "it", "yt",
        "up", "ep", "op", "ap", "ip", "yp",
        "uc", "ec", "oc", "ac", "ic", "yc",

        # 5. Trigram bất hợp lệ
        "ace", "aci", "aco", "acu", "acb",
        "ica", "ice", "ici", "ico", "icu",
        "eca", "ece", "eci", "eco", "ecu",
        "eau", "iou", "eon", "ena", "cre",
        "uou", "oau",
        "eth", "eta", "eto", "eti", "ete", "etx",
        "oma", "ome", "omi", "omo", "omu",
        "ami", "ame", "amo", "amu", "amp", "amy",

        # 6. Phụ âm đôi/cuối bất hợp lệ
        "ds", "gs", "ls", "ms", "ns", "rs", "vs", "xs", "zs",
        "aa","bb","cc","dd","ee","ff","gg","hh","ii","jj","kk","ll",
        "mm","nn","oo","pp","qq","rr","ss","tt","uu","vv","ww","xx","yy","zz", "mn",
        "cd", "chx", "cn", "cp", "cs", "cy",
         "đb", "bđ",
    "đc", "cđ",
    "đf", "fđ",
    "đg", "gđ",
    "đh", "hđ",
    "đj", "jđ",
    "đk", "kđ",
    "đl", "lđ",
    "đm", "mđ",
    "đn", "nđ",
    "đp", "pđ",
    "đq", "qđ",
    "đr", "rđ",
    "đs", "sđ",
    "đt", "tđ",
    "đv", "vđ",
    "đw", "wđ",
    "đx", "xđ",
    "đy", "yđ",
    "đz", "zđ",
     "ôa", "ôă", "ôâ", "ôe", "ôi", "ôê", "ôo", "ôô", "ôơ", "ôu", "ôư", "ôy",
    "aô", "ăô", "âô", "eô", "iô", "oô", "ôô", "ơô", "uô", "ưô", "yô",

            "He","Li","Be","Ne","Na","Mg","Al","Si","Cl","Ar","Ca",
        "Sc","Ti","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge",
        "As","Se","Br","Kr","Rb","Sr","Zr","Nb","Mo","Tc","Ru",
        "Rh","Pd","Ag","Cd","In","Sn","Sb","Te","Xe","Cs","Ba",
        "La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho",
        "Er","Tm","Yb","Lu","Hf","Ta","Re","Os","Ir","Pt","Au",
        "Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th",
        "Pa","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No",
        "Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh",
        "Fl","Mc","Lv","Ts","Og", "Ct"
    ]


    word_lower = word.lower()
    if any(pat in word_lower for pat in non_vn_patterns):
        return False
    return bool(vietnamese_pattern.match(word))

# Clean the original dictionary and write to a new file
input_path = r"c:\Workspace\HCMUS\Voice Processing\vietnamese_phonemizer\resources\VDic_uni.txt"
output_path = r"c:\Workspace\HCMUS\Voice Processing\vietnamese_phonemizer\resources\VDic_uni_vietnamese.txt"
with open(input_path, encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for line in infile:
        if not line.strip():
            continue
        word = line.split("\t")[0].strip()
        if is_vietnamese_word(word):
            outfile.write(line)

# Optionally, still clean the split files as before
split_dir = r"c:\Workspace\HCMUS\Voice Processing\vietnamese_phonemizer\resources\VDic_uni_split"
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
            if is_vietnamese_word(word):
                kept.append(line)
        with open(fpath, "w", encoding="utf-8") as outfile:
            outfile.writelines(kept)
        if is_vietnamese_word(word):
            kept.append(line)
    with open(fpath, "w", encoding="utf-8") as outfile:
        outfile.writelines(kept)
print("Done. Cleaned file written to VDic_uni_vietnamese.txt and split files updated.")
