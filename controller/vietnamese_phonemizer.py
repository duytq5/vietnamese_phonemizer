
import re

class VietnamesePhonemizer:
  def __init__(self):
    # Dấu
    self.tone_map = {
      "ngang": "1",
      "huyen": "2",
      "nga": "3",
      "hoi": "4",
      "sac": "5",
      "nang": "6",
    }

    # Phụ âm đầu và âm vị
    self.onset_map = {
      "b": "b",
      "m": "m",
      "n": "n",
      "ph": "f",
      "v": "v",
      "t": "t",
      "th": "t\u02bc",
      "đ": "d",
      "d": "d",
      "gi": "d",
      "r": "ʐ",
      "x": "s",
      "s": "ʂ",
      "ch": "c",
      "tr": "ʈ",
      "nh": "ɲ",
      "l": "l",
      "k": "k",
      "q": "k",
      "c": "k",
      "kh": "\u03C7",
      "ngh": "ŋ",
      "ng": "ŋ",
      "gh": "ɣ",
      "g": "ɣ",
      "h": "h",
      "": ""
    }
    # Dùng để xoá dấu cho ký tự
    self.remove_tone_map = {
      'á': 'a', 'à': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
      'ắ': 'ă', 'ằ': 'ă', 'ẳ': 'ă', 'ẵ': 'ă', 'ặ': 'ă',
      'ấ': 'â', 'ầ': 'â', 'ẩ': 'â', 'ẫ': 'â', 'ậ': 'â',
      'é': 'e', 'è': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
      'ế': 'ê', 'ề': 'ê', 'ể': 'ê', 'ễ': 'ê', 'ệ': 'ê',
      'í': 'i', 'ì': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
      'ó': 'o', 'ò': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
      'ố': 'ô', 'ồ': 'ô', 'ổ': 'ô', 'ỗ': 'ô', 'ộ': 'ô',
      'ớ': 'ơ', 'ờ': 'ơ', 'ở': 'ơ', 'ỡ': 'ơ', 'ợ': 'ơ',
      'ú': 'u', 'ù': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
      'ứ': 'ư', 'ừ': 'ư', 'ử': 'ư', 'ữ': 'ư', 'ự': 'ư',
      'ý': 'y', 'ỳ': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
      'a': 'a', 'ă': 'ă', 'â': 'â',
      'e': 'e', 'ê': 'ê',
      'i': 'i',
      'o': 'o', 'ô': 'ô', 'ơ': 'ơ',
      'u': 'u', 'ư': 'ư',
      'y': 'y'
    }

    # Ký tự là phụ âm và chỉ có 1 chữ cái
    self.single_onset = {"b", "m", "v", "đ", "d", "r", "x", "s", "l", "q", "h", "t", "g", "c", "n", "k"}

    # Ký tự có thể là phụ âm và có thể có 2 chữ cái
    self.possible_double_onset = {"t", "g", "c", "n", "k"}
    self.double_onset = {"ph", "th", "ch", "tr", "nh", "kh", "ngh", "ng", "gh"}
    # Ký tự có thể là phụ âm và có thể có 3 chữ cái
    self.possible_triple_onset = {"ng"}
    self.triple_onset = {"ngh"}

    self.glide_map = {
      "o": "u\u032e",
      "u": "u\u032e",
    }

    # bảng âm chính và phiên âm
    # a là trường hợp đặc biệt có thể có tới 3 cách phiêm
    self.nucleus_map = {
      "y": "i",
      "i": "i",
      "ê": "e",
      "e": "ɛ",
      "ư": "ɯ",
      "u": "u",
      "ơ": "ɤ",
      "ô": "o",
      "ôô": "o",
      "o": "ɔ\u0306",
      "oo": "ɔ",
      "a": {
        "u": "ă",
        "y": "ă",
        "nh": "ɛ\u0306",
        "ch": "ɛ\u0306"
        # default "a"
      },
      "ă": "ă",
      "iê": "ie",
      "yê": "ie",
      "ia": "ie",
      "ya": "ie",
      "ươ": "ɯɤ",
      "ưa": "ɯɤ",
      "uô": "uo",
      "ua": "uo",
      "â": "ɤ\u0303"
    }

    self.glide_nucleus_mapping = {
      "o": {
        "e", "é", "è", "ẽ", "ẻ", "ẹ",
        "a", "á", "à", "ã", "ả", "ạ",
        "ă", "ắ", "ằ", "ẵ", "ẳ", "ặ"
      },
      "u": {
        "y", "ý", "ỳ", "ỹ", "ỷ", "ỵ",
        "ê", "ế", "ề", "ễ", "ể", "ệ",
        "ơ", "ớ", "ờ", "ỡ", "ở", "ợ",
        "â", "ấ", "ầ", "ẫ", "ẩ", "ậ"
      }
    }
    self.coda_map = {
      "m": "m",
      "n": "n",
      "p": "p",
      "t": "t",
      "nh": "ŋ",
      "ng": "ŋ",
      "ch": "k",
      "c": "k",
      "o": "w",
      "u": "w",
      "y": "j",
      "i": "j"
    }


  def phonemize(self, text: str) -> str:
    text = text.strip()
    curr = ""
    chars = []
    for char in text:
      if char == " ":
        if curr:
          chars.append(curr)
          curr = ""
      else:
        curr += char
    if curr:
      chars.append(curr)
    result = []
    for char in chars:
      phenemized_word = self._phonemize(char)
      result.append(phenemized_word)
    return " ".join(result)

  def check_tone(self, char):
    if char in "áắấéếóốíúớ":
      return "sac"
    elif char in "àằầòồèềìùờ":
      return "huyen"
    elif char in "ãẫẵõỗĩẽễũỡ":
      return "nga"
    elif char in "ảẩẳẻểỏổỉủở":
      return "hoi"
    elif char in "ạặậịọộẹệụợ":
      return "nang"
    return None

  def find_onset(self, word):
    if word[0].lower() not in self.single_onset:
      return ""
    elif word[0].lower() in self.possible_double_onset:
      if word[:2].lower() in self.double_onset:
        if word[:3].lower() in self.triple_onset:
          return word[:3]
        else:
          return word[:2]
      else:
        return word[:1]
    else:
      return word[0]

  def find_glide(self, word, onset):
    val = word[:1]
    if val not in self.glide_map:
      return ""
    else:
      if onset == "q":
        if val == "u":
          return val
        else:
          raise Exception("Invalid word")
      else:
        if len(word) < 2:
          return ""
        next_char = word[1]
        if next_char in self.glide_nucleus_mapping[val]:
          return val
        else:
          return ""


  def find_nucleus(self, word):
    val = word[:2]
    if val.lower() in self.nucleus_map:
      return val[:2]
    return val[:1]

  # TODO: handle some special char
  def _phonemize(self, word: str):
    tone = "ngang"
    for c in word:
      tone_ = self.check_tone(c)
      if tone_ is not None:
        tone = tone_
    word = list(word)
    word = [self.remove_tone_map[x] if x in self.remove_tone_map else x for x in word]
    word = "".join(word)
    onset = self.find_onset(word)
    word = word.removeprefix(onset)
    glide = self.find_glide(word, onset)
    word = word.removeprefix(glide)
    nucleus = self.find_nucleus(word)
    coda = word.removeprefix(nucleus)
    extra = ""
    if coda and coda[-1] in {",", "."}:
      extra = coda[-1]
      coda = coda[:-1]
    res = ""
    res += self.onset_map[onset.lower()]
    res += self.glide_map.get(glide.lower(), "")
    nucleus_value = self.nucleus_map.get(nucleus.lower(), "")
    if isinstance(nucleus_value, dict):
      coda_value = self.coda_map.get(coda.lower(), "")
      nucleus_val = nucleus_value.get(coda.lower(), "a")
      res += nucleus_val + coda_value
    else:
      res += nucleus_value
      res += self.coda_map.get(coda.lower(), "")
    res += self.tone_map[tone.lower()]
    res += extra
    return res
