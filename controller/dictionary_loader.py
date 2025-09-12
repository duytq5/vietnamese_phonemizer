class DictionaryLoader:
    def __init__(self, path="resources/VDic_uni_vietnamese.txt"):
        self.path = path
        self.lines = self._load_dictionary()

    def _load_dictionary(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                return [line.strip() for line in f]
        except Exception as e:
            return [f"Error loading dictionary: {e}"]

    def get_lines(self):
        return self.lines

    def reload(self):
        self.lines = self._load_dictionary()
        return self.lines
