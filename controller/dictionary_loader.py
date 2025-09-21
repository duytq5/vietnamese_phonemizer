class DictionaryLoader:
    def __init__(self, path="resources/VDic_uni_vietnamese.txt", tagset_path="resources/VnQTAG_POSTagset.txt"):
        self.path = path
        self.lines = self._load_dictionary()
        self.pos_tag_definitions = self._load_pos_tag_definitions(tagset_path)

    def _load_dictionary(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                return [line.strip() for line in f]
        except Exception as e:
            return [f"Error loading dictionary: {e}"]

    def _load_pos_tag_definitions(self, tagset_path):
        tag_defs = {}
        try:
            with open(tagset_path, encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("\t")
                    # Accept lines with at least 3 columns: tag, alt_tag, Vietnamese, English
                    if len(parts) >= 3:
                        tag = parts[1].strip() if parts[1].strip() else parts[0].strip()
                        vn_desc = parts[2].strip()
                        en_desc = parts[3].strip() if len(parts) > 3 else ""
                        tag_defs[tag.lower()] = {"vn": vn_desc, "en": en_desc}
        except Exception as e:
            tag_defs["ERROR"] = {"vn": f"Error loading tagset: {e}", "en": ""}
        return tag_defs

    def get_lines(self):
        return self.lines

    def get_pos_tag_definitions(self):
        """Return the POS tag definitions as a dictionary: {tag: {vn, en}}"""
        return self.pos_tag_definitions

    def reload(self):
        self.lines = self._load_dictionary()
        return self.lines
    
    def get_pos_tag_definition(self, tag, lang=None):
        """
        Return the definition for a given POS tag string.
        If lang is 'vn' or 'en', return only that description.
        If not found, returns None.
        """
        defn = self.pos_tag_definitions.get(tag)
        if defn is None:
            return None
        if lang in ('vn', 'en'):
            result = defn.get(lang)
            return result
        return defn
