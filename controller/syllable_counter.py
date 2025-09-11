from controller.vietnamese_phonemizer import VietnamesePhonemizer

class SyllableCounter:
    def __init__(self, phonemizer_instance):
        if not isinstance(phonemizer_instance, VietnamesePhonemizer):
            raise TypeError("phonemizer_instance must be an instance of VietnamesePhonemizer.")
        self.phonemizer = phonemizer_instance
        self.unique_phonemic_syllables = set()

    def count_unique_syllables(self, dictionary_words):
        if not isinstance(dictionary_words, list):
            raise TypeError("dictionary_words must be a list of strings.")
        
        if not dictionary_words:
            return 0

        self.unique_phonemic_syllables = set()

        for word_entry in dictionary_words:
            # Only use the first field (before tab) and split by spaces to get syllables
            syllables = word_entry.split("\t")[0].strip().split()
            for syllable in syllables:
                phonemic_syllable = self.phonemizer.phonemize(syllable)
                if phonemic_syllable:
                    self.unique_phonemic_syllables.add(phonemic_syllable)
        
        return len(self.unique_phonemic_syllables)

    def get_unique_syllables(self):
        return self.unique_phonemic_syllables
