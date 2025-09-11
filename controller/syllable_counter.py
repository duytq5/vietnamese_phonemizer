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
            print("Không có từ nào trong từ điển để phân tích.")
            return 0

        self.unique_phonemic_syllables = set()

        for word_entry in dictionary_words:
            # Use the phonemizer to convert the word entry into phonemic syllables
            phonemic_representation = self.phonemizer.phonemize(word_entry)
            
            # The phonemize method returns a string of phonemic syllables separated by spaces.
            individual_phonemic_syllables = phonemic_representation.split(' ')
            
            for syllable in individual_phonemic_syllables:
                if syllable:
                    self.unique_phonemic_syllables.add(syllable)
        
        return len(self.unique_phonemic_syllables)

    def get_unique_syllables(self):
        return self.unique_phonemic_syllables