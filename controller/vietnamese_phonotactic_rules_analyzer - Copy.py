# --- START OF FILE vietnamese_phonotactic_rules_analyzer.py (Fixed All KeyErrors and Removed Prints) ---

import re
from collections import defaultdict
from controller.vietnamese_phonemizer import VietnamesePhonemizer
from controller.dictionary_loader import DictionaryLoader

class VietnamesePhonotacticRulesAnalyzer:
    def __init__(self, phonemizer_instance, dictionary_loader_instance):
        if not isinstance(phonemizer_instance, VietnamesePhonemizer):
            raise TypeError("phonemizer_instance must be an instance of VietnamesePhonemizer.")
        if not isinstance(dictionary_loader_instance, DictionaryLoader):
            raise TypeError("dictionary_loader_instance must be an instance of DictionaryLoader.")
        
        self.phonemizer = phonemizer_instance
        self.dict_loader = dictionary_loader_instance
        self.rules_output = [] # Store all generated rules

        # Dữ liệu thống kê cần thiết
        # Sử dụng tên key tiếng Anh (onset, glide, nucleus, coda, tone)
        self.syllable_data = [] # Stores {'onset', 'glide', 'nucleus', 'coda', 'tone', 'pos_tags', 'orth_syllable'}

        # List of all possible phonemic tones
        self.phonemic_tones = list(self.phonemizer.tone_map.values())
        
        # Thống kê đồng xuất hiện cho Bình diện ngữ âm (Sử dụng tên key tiếng Anh)
        self.cooccurrence_counts = {
            'onset_glide': defaultdict(lambda: defaultdict(int)),
            'glide_nucleus': defaultdict(lambda: defaultdict(int)),
            'nucleus_coda': defaultdict(lambda: defaultdict(int)),
            'coda_tone': defaultdict(lambda: defaultdict(int)),
            'onset_nucleus': defaultdict(lambda: defaultdict(int)), # Key này đã được đổi tên từ 'am_dau_am_chinh_truc_tiep'
        }
        # Hoàn nguyên tên key về tiếng Anh
        self.component_frequencies = {
            'onset': defaultdict(int), 'glide': defaultdict(int),
            'nucleus': defaultdict(int), 'coda': defaultdict(int), 'tone': defaultdict(int)
        }

        # Thống kê cho Bình diện ngữ pháp
        # Hoàn nguyên tên key về tiếng Anh
        self.pos_phoneme_counts = {
            'onset': defaultdict(lambda: defaultdict(int)),
            'nucleus': defaultdict(lambda: defaultdict(int)),
            'coda': defaultdict(lambda: defaultdict(int)),
            'tone': defaultdict(lambda: defaultdict(int)),
        }
        self.pos_counts = defaultdict(int) # Tổng số đếm cho mỗi thẻ loại từ

        # Tập hợp các âm tiết ngữ âm hợp lệ từ vét cạn
        self.valid_phonemic_syllables_brute_force = set()


    def _parse_dictionary_entry(self, line):
        """Phân tích một dòng từ điển thành từ/cụm từ và các thẻ POS."""
        parts = line.split("\t\t")
        word_or_phrase = parts[0].strip() if parts else ""
        pos_tags_str = parts[1].strip() if len(parts) > 1 else ""
        pos_tags = [tag.strip() for tag in pos_tags_str.split(',') if tag.strip()] if pos_tags_str else []
        return word_or_phrase, pos_tags

    def _extract_phonemic_components(self, phonemic_syllable_string):
        """
        Phân tách một chuỗi phiên âm thành onset, glide, nucleus, coda, tone.
        Đây là quá trình "reverse engineering" output của phonemizer.
        """
        if not phonemic_syllable_string:
            return None

        if not phonemic_syllable_string or not phonemic_syllable_string[-1].isdigit():
            return {'onset': '', 'glide': '', 'nucleus': '', 'coda': '', 'tone': ''}

        tone = phonemic_syllable_string[-1]
        remaining = phonemic_syllable_string[:-1]

        coda_phonemes = sorted(list(set(self.phonemizer.coda_map.values())), key=len, reverse=True)
        coda = ''
        for p_coda in coda_phonemes:
            if p_coda and remaining.endswith(p_coda):
                coda = p_coda
                remaining = remaining[:-len(coda)]
                break

        nucleus_phonemes = set()
        for v in self.phonemizer.nucleus_map.values():
            if isinstance(v, dict):
                nucleus_phonemes.add('a')
                for sub_v in v.values():
                    nucleus_phonemes.add(sub_v)
            else:
                nucleus_phonemes.add(v)
        nucleus_phonemes = sorted(list(nucleus_phonemes), key=len, reverse=True)
        
        nucleus = ''
        for p_nuc in nucleus_phonemes:
            if p_nuc and remaining.endswith(p_nuc):
                nucleus = p_nuc
                remaining = remaining[:-len(nucleus)]
                break
        
        glide_phoneme_val = self.phonemizer.glide_map.get('u', '')
        glide = ''
        if remaining and remaining.endswith(glide_phoneme_val):
            glide = glide_phoneme_val
            remaining = remaining[:-len(glide)]
        
        onset = remaining if remaining else ''
        if not onset and (nucleus or glide):
            onset = '?'
        elif not onset and not nucleus and not glide and not coda:
            onset = '' 
            tone = ''

        return {'onset': onset, 'glide': glide, 'nucleus': nucleus, 'coda': coda, 'tone': tone}


    def _prepare_data(self):
        """Chuẩn bị dữ liệu bằng cách phiên âm các âm tiết từ từ điển và trích xuất các thành phần."""
        self.syllable_data = []
        raw_lines = self.dict_loader.get_lines()

        # Removed print statement
        for line in raw_lines:
            if not line.strip() or line.strip().startswith('---'):
                continue
            
            word_or_phrase, pos_tags = self._parse_dictionary_entry(line)
            if not word_or_phrase:
                continue

            orth_syllables = word_or_phrase.split()
            for orth_syllable in orth_syllables:
                phonemic_syllable_string = self.phonemizer.phonemize(orth_syllable)
                
                for ps_str in phonemic_syllable_string.split(' '):
                    if not ps_str: continue
                    
                    components = self._extract_phonemic_components(ps_str)
                    if components and components['tone']:
                        components['pos_tags'] = pos_tags
                        components['orth_syllable'] = orth_syllable 
                        self.syllable_data.append(components)
                        
                        # Cập nhật tần suất các thành phần và đồng xuất hiện từ DỮ LIỆU THỰC TẾ
                        self.component_frequencies['onset'][components['onset']] += 1
                        self.component_frequencies['glide'][components['glide']] += 1
                        self.component_frequencies['nucleus'][components['nucleus']] += 1
                        self.component_frequencies['coda'][components['coda']] += 1
                        self.component_frequencies['tone'][components['tone']] += 1

                        if components['onset'] and components['glide']:
                            self.cooccurrence_counts['onset_glide'][components['onset']][components['glide']] += 1
                        if components['glide'] and components['nucleus']:
                            self.cooccurrence_counts['glide_nucleus'][components['glide']][components['nucleus']] += 1
                        if components['nucleus'] and components['coda']:
                            self.cooccurrence_counts['nucleus_coda'][components['nucleus']][components['coda']] += 1
                        if components['coda'] and components['tone']:
                            self.cooccurrence_counts['coda_tone'][components['coda']][components['tone']] += 1
                        if components['onset'] and components['nucleus']:
                            self.cooccurrence_counts['onset_nucleus'][components['onset']][components['nucleus']] += 1

                        for tag in pos_tags:
                            self.pos_counts[tag] += 1
                            if components['onset']: self.pos_phoneme_counts['onset'][tag][components['onset']] += 1
                            if components['nucleus']: self.pos_phoneme_counts['nucleus'][tag][components['nucleus']] += 1
                            if components['coda']: self.pos_phoneme_counts['coda'][tag][components['coda']] += 1
                            if components['tone']: self.pos_phoneme_counts['tone'][tag][components['tone']] += 1
        # Removed print statement
        

    def _get_examples(self, component_type, phoneme_value, limit=3, exclude_tones=None, include_tones=None, specific_pos=None, exclude_specific_syllables=None):
        """Hàm hỗ trợ để lấy ví dụ âm tiết chữ viết."""
        examples = []
        seen_examples = set()
        for sy_comp in self.syllable_data:
            # Sử dụng các tên key tiếng Anh
            if sy_comp[component_type] == phoneme_value:
                if exclude_tones and sy_comp['tone'] in exclude_tones:
                    continue
                if include_tones and sy_comp['tone'] not in include_tones:
                    continue
                if specific_pos and not any(tag in sy_comp['pos_tags'] for tag in specific_pos):
                    continue
                if exclude_specific_syllables and sy_comp['orth_syllable'] in exclude_specific_syllables:
                    continue

                if sy_comp['orth_syllable'] not in seen_examples:
                    examples.append(sy_comp['orth_syllable'])
                    seen_examples.add(sy_comp['orth_syllable'])
                    if len(examples) >= limit:
                        break
        return examples
    
    def _get_cooccurrence_examples(self, type1, val1, type2, val2, limit=3, exclude_tones=None, include_tones=None):
        """
        Hàm hỗ trợ để lấy ví dụ cho một cặp đồng xuất hiện cụ thể (type1-val1, type2-val2).
        """
        examples = []
        seen_examples = set()
        for sy_comp in self.syllable_data:
            # Sử dụng các tên key tiếng Anh
            if sy_comp[type1] == val1 and sy_comp[type2] == val2:
                if exclude_tones and sy_comp['tone'] in exclude_tones:
                    continue
                if include_tones and sy_comp['tone'] not in include_tones:
                    continue
                if sy_comp['orth_syllable'] not in seen_examples:
                    examples.append(sy_comp['orth_syllable'])
                    seen_examples.add(sy_comp['orth_syllable'])
                    if len(examples) >= limit:
                        break
        return examples


    def _is_valid_phonemic_syllable_combination(self, parts):
        onset = parts['onset']
        glide = parts['glide']
        nucleus = parts['nucleus']
        coda = parts['coda']
        tone = parts['tone']

        if not nucleus: return False
        
        if onset == '?' and (glide or not nucleus): return False

        am_dem_w_phonemic = self.phonemizer.glide_map.get('u', 'w')
        if glide == am_dem_w_phonemic:
            am_dau_moi_phonemic = {self.phonemizer.onset_map[k] for k in ["b", "m", "ph", "v"] if k in self.phonemizer.onset_map}
            if onset in am_dau_moi_phonemic: return False

            nguyen_am_tron_khep_phonemic = {
                self.phonemizer.nucleus_map.get(k) for k in ["u", "o", "ô", "ơ", "uô", "ươ", "ư"] if k in self.phonemizer.nucleus_map
            }
            nguyen_am_tron_khep_phonemic = {n for n in nguyen_am_tron_khep_phonemic if n}
            nguyen_am_tron_khep_phonemic.add(self.phonemizer.nucleus_map.get('y', 'i'))
            
            if nucleus in nguyen_am_tron_khep_phonemic:
                if nucleus == self.phonemizer.nucleus_map.get('y', 'i') and glide == am_dem_w_phonemic:
                    pass
                else:
                    return False
        
        am_cuoi_tac_phonemic = {self.phonemizer.coda_map[k] for k in ["p", "t", "ch"] if k in self.phonemizer.coda_map}
        thanh_sac = self.phonemizer.tone_map['sac']
        thanh_nang = self.phonemizer.tone_map['nang']
        if coda in am_cuoi_tac_phonemic:
            if tone not in {thanh_sac, thanh_nang}:
                return False

        am_chinh_co_san_am_dem = {
            self.phonemizer.nucleus_map.get(k) for k in ["iê", "uô", "ươ"] if k in self.phonemizer.nucleus_map
        }
        am_chinh_co_san_am_dem = {n for n in am_chinh_co_san_am_dem if n}
        if nucleus in am_chinh_co_san_am_dem and glide != '':
            return False

        if nucleus == self.phonemizer.nucleus_map.get('u', 'u') and coda == self.phonemizer.coda_map.get('y', 'j'): return False
        if nucleus == self.phonemizer.nucleus_map.get('i', 'i') and coda == self.phonemizer.coda_map.get('u', 'w'): return False
        
        if onset == '?' and glide != '': return False

        if onset == self.phonemizer.onset_map.get('q', 'k') and glide != self.phonemizer.glide_map.get('u', 'w'):
            return False
            
        return True

    def _generate_valid_syllables_by_brute_force(self):
        self.valid_phonemic_syllables_brute_force = set()
        # Removed print statement

        for am_dau in self.phonemic_onsets_list:
            for am_dem in self.phonemic_glides_list:
                for am_chinh in self.phonemic_nuclei_list:
                    for am_cuoi in self.phonemic_codas_list:
                        for thanh_dieu in self.phonemic_tones:
                            parts = {
                                'onset': am_dau, 'glide': am_dem, 'nucleus': am_chinh,
                                'coda': am_cuoi, 'tone': thanh_dieu
                            }
                            if self._is_valid_phonemic_syllable_combination(parts):
                                phonemic_syllable_string = f"{am_dau}{am_dem}{am_chinh}{am_cuoi}{thanh_dieu}"
                                self.valid_phonemic_syllables_brute_force.add(phonemic_syllable_string)
        
        # Removed print statement
        return list(self.valid_phonemic_syllables_brute_force)


    def _analyze_phonemic_cooccurrence_rules(self, min_freq=10):
        rules = []
        rules.append("\n### Bình diện ngữ âm: Quy luật đồng xuất hiện của các âm vị")
        
        am_dem_w_phonemic = self.phonemizer.glide_map.get('u', 'w')
        am_dau_moi_phonemic = {self.phonemizer.onset_map[k] for k in ["b", "m", "ph", "v"] if k in self.phonemizer.onset_map}
        
        nguyen_am_tron_khep_phonemic_set = {
            self.phonemizer.nucleus_map.get(k) for k in ["u", "o", "ô", "ơ", "uô", "ươ", "ư"] if k in self.phonemizer.nucleus_map
        }
        if 'a' in self.phonemizer.nucleus_map and isinstance(self.phonemizer.nucleus_map['a'], dict):
            for var_nuc in self.phonemizer.nucleus_map['a'].values():
                if var_nuc: nguyen_am_tron_khep_phonemic_set.add(var_nuc)
        nguyen_am_tron_khep_phonemic_set = {n for n in nguyen_am_tron_khep_phonemic_set if n}
        nguyen_am_tron_khep_phonemic_set.add(self.phonemizer.nucleus_map.get('y', 'i')) # Thêm 'i' phonemic cho ngoại lệ 'uy'


        # Quy tắc 1.1 (từ Slide 16): Âm đệm /w/ KHÔNG hoặc HIẾM sau phụ âm đầu môi
        for am_dau_val in am_dau_moi_phonemic:
            total_am_dau_freq = self.component_frequencies['onset'][am_dau_val] # Sử dụng key 'onset'
            if total_am_dau_freq > min_freq:
                total_cooccurrence = self.cooccurrence_counts['onset_glide'][am_dau_val][am_dem_w_phonemic] # Sử dụng key 'onset_glide'
                status_str = ""
                examples_str = ""
                
                if total_cooccurrence == 0:
                    status_str = "KHÔNG kết hợp"
                    examples_str = f" (Tần suất đồng xuất hiện: 0)."
                elif total_cooccurrence > 0 and total_cooccurrence <= min_freq: # Hiếm
                    status_str = "HIẾM khi kết hợp"
                    examples = self._get_cooccurrence_examples('onset', am_dau_val, 'glide', am_dem_w_phonemic) # Lấy ví dụ cho cặp đồng xuất hiện
                    examples_str = f" (ví dụ: {', '.join(examples)}) (Tần suất đồng xuất hiện: {total_cooccurrence})."
                
                if status_str:
                    rules.append(f"- Âm đệm /{am_dem_w_phonemic}/ {status_str} với âm đầu /{am_dau_val}/{examples_str}.")
        
        # Quy tắc 1.2 (từ Slide 16): Âm đệm /w/ KHÔNG hoặc HIẾM trước nguyên âm tròn môi/khép (trừ ngoại lệ 'uy')
        if self.component_frequencies['glide'][am_dem_w_phonemic] > min_freq: # Sử dụng key 'glide'
            for am_chinh_val in nguyen_am_tron_khep_phonemic_set:
                total_cooccurrence = self.cooccurrence_counts['glide_nucleus'][am_dem_w_phonemic][am_chinh_val] # Sử dụng key 'glide_nucleus'
                status_str = ""
                examples_str = ""
                
                # Ngoại lệ 'uy' (w + i)
                if am_chinh_val == self.phonemizer.nucleus_map.get('y', 'i') and am_dem_w_phonemic == self.phonemizer.glide_map.get('u', 'w'):
                    if total_cooccurrence > min_freq:
                        examples = self._get_cooccurrence_examples('glide', am_dem_w_phonemic, 'nucleus', am_chinh_val) # Lấy ví dụ cho cặp đồng xuất hiện
                        if examples:
                            rules.append(f"- Âm đệm /{am_dem_w_phonemic}/ THƯỜNG đi với âm chính /{am_chinh_val}/ (như trong 'uy') (ví dụ: {', '.join(examples)}). (Tần suất đồng xuất hiện: {total_cooccurrence}).")
                    continue
                
                # Quy tắc chung: không kết hợp hoặc hiếm khi kết hợp
                if total_cooccurrence == 0:
                    status_str = "KHÔNG kết hợp"
                    examples_str = f" (Tần suất đồng xuất hiện: 0)."
                elif total_cooccurrence > 0 and total_cooccurrence <= min_freq: # Hiếm
                    status_str = "HIẾM khi kết hợp"
                    examples = self._get_cooccurrence_examples('glide', am_dem_w_phonemic, 'nucleus', am_chinh_val) # Lấy ví dụ cho cặp đồng xuất hiện
                    examples_str = f" (ví dụ: {', '.join(examples)}) (Tần suất đồng xuất hiện: {total_cooccurrence})."
                
                if status_str:
                    rules.append(f"- Âm đệm /{am_dem_w_phonemic}/ {status_str} với âm chính /{am_chinh_val}/{examples_str}.")

        # Quy tắc 2 (từ Slide 21): Âm cuối tắc và Thanh điệu
        plosive_codas_phonemic = {self.phonemizer.coda_map[k] for k in ["p", "t", "ch"] if k in self.phonemizer.coda_map}
        thanh_sac = self.phonemizer.tone_map['sac']
        thanh_nang = self.phonemizer.tone_map['nang']
        thanh_dieu_khong_hop_le = {t for t in self.phonemic_tones if t not in {thanh_sac, thanh_nang}}

        for am_cuoi_val in plosive_codas_phonemic:
            total_am_cuoi_voi_thanh_khong_hop_le = 0
            for thanh_val in thanh_dieu_khong_hop_le:
                total_am_cuoi_voi_thanh_khong_hop_le += self.cooccurrence_counts['coda_tone'][am_cuoi_val][thanh_val]
            
            total_am_cuoi_appearances = self.component_frequencies['coda'][am_cuoi_val]
            if total_am_cuoi_appearances > min_freq:
                if total_am_cuoi_voi_thanh_khong_hop_le == 0:
                    examples = self._get_examples('coda', am_cuoi_val, include_tones={thanh_sac, thanh_nang})
                    rules.append(f"- Âm cuối /{am_cuoi_val}/ (ví dụ: {', '.join(examples)}) CHỈ kết hợp với thanh Sắc ({thanh_sac}) và Nặng ({thanh_nang}). (Tần suất: {total_am_cuoi_appearances}).")
                else:
                    examples_hop_le = self._get_examples('coda', am_cuoi_val, include_tones={thanh_sac, thanh_nang}, limit=2)
                    examples_ngoai_le = self._get_examples('coda', am_cuoi_val, exclude_tones={thanh_sac, thanh_nang}, limit=1)
                    ngoai_le_str = f" (ví dụ ngoại lệ: {', '.join(examples_ngoai_le)}, tần suất: {total_am_cuoi_voi_thanh_khong_hop_le})" if examples_ngoai_le else ""
                    rules.append(f"- Âm cuối /{am_cuoi_val}/ chủ yếu kết hợp với thanh Sắc ({thanh_sac}) và Nặng ({thanh_nang}) (ví dụ: {', '.join(examples_hop_le)}), nhưng có một số ngoại lệ{ngoai_le_str}.")

        # Quy tắc 3: /q/-/u/ -> /k/-/w/
        am_dau_q_phonemic = self.phonemizer.onset_map.get('q', 'k')
        am_dem_u_phonemic = self.phonemizer.glide_map.get('u', 'w')
        count_q_u = self.cooccurrence_counts['onset_glide'][am_dau_q_phonemic][am_dem_u_phonemic]
        if count_q_u > min_freq:
            examples = self._get_cooccurrence_examples('onset', am_dau_q_phonemic, 'glide', am_dem_u_phonemic)
            rules.append(f"- Âm đầu /{am_dau_q_phonemic}/ (từ chữ 'q') THƯỜNG hoặc LUÔN đi kèm với âm đệm /{am_dem_u_phonemic}/ (từ chữ 'u') (ví dụ: {', '.join(examples)}). (Tần suất đồng xuất hiện: {count_q_u}).")

        # Các cặp đồng xuất hiện (Âm đầu-Âm chính) có tần suất cao
        rules.append("\n### Các cặp đồng xuất hiện (Âm đầu-Âm chính) có tần suất cao")
        top_am_dau_am_chinh = sorted(
            [(f"âm đầu /{o}/ - âm chính /{n}/", count) 
             for o, n_dict in self.cooccurrence_counts['onset_nucleus'].items() 
             for n, count in n_dict.items() if count > min_freq * 2],
            key=lambda item: item[1], reverse=True
        )[:10]
        for pair, count in top_am_dau_am_chinh:
            rules.append(f"  - {pair}: {count} lần.")

        return rules


    def _analyze_grammatical_tendencies(self, min_freq_ratio=0.1, min_total_freq=10):
        rules = []
        rules.append("\n### Bình diện ngữ pháp: Xu hướng âm vị theo Từ loại")

        m_onset = self.phonemizer.onset_map.get('m', 'm')
        pos_noun_types = ['Nc', 'Ng']
        
        total_m_onset_nouns = 0
        for pos_tag in pos_noun_types:
            total_m_onset_nouns += self.pos_phoneme_counts['onset'][pos_tag][m_onset]
        
        total_m_onset_any_pos = sum(self.pos_phoneme_counts['onset'][tag][m_onset] for tag in self.pos_counts.keys())
        if total_m_onset_any_pos > min_total_freq:
            ratio = total_m_onset_nouns / total_m_onset_any_pos if total_m_onset_any_pos else 0
            examples = self._get_examples('onset', m_onset, specific_pos=pos_noun_types)
            if ratio > min_freq_ratio * 2:
                rules.append(f"- Âm đầu /{m_onset}/ (ví dụ: {', '.join(examples)}) có xu hướng cao liên quan đến Danh từ (đặc biệt là các từ chỉ mẹ/họ hàng). Tỷ lệ: {ratio:.2f}")

        for pos_tag in ['Vt', 'Vi', 'Aa', 'Na', 'Nc', 'Ng']:
            if self.pos_counts[pos_tag] > min_total_freq:
                top_onsets_for_pos = sorted(
                    [(onset, count) for onset, count in self.pos_phoneme_counts['onset'][pos_tag].items() 
                     if count / self.pos_counts[pos_tag] > min_freq_ratio],
                    key=lambda item: item[1], reverse=True
                )[:3]
                if top_onsets_for_pos:
                    rules.append(f"- Đối với **{pos_tag}** (tổng số âm tiết {self.pos_counts[pos_tag]}): các âm đầu nổi bật là " + 
                                 ", ".join([f"/{o}/ ({c} lần, tỷ lệ: {c/self.pos_counts[pos_tag]:.2f})" for o, c in top_onsets_for_pos]))
        
        e_nucleus = self.phonemizer.nucleus_map.get('e', 'e')
        o_nucleus = self.phonemizer.nucleus_map.get('ô', 'o')
        
        if self.component_frequencies['nucleus'][e_nucleus] > min_total_freq:
            rules.append(f"\n- Xu hướng của Âm chính /{e_nucleus}/:")
            for pos_tag in ['Vt', 'Vi', 'Aa', 'Na', 'Nc', 'Ng']:
                if self.pos_counts[pos_tag] > min_total_freq:
                    count_e_in_pos = self.pos_phoneme_counts['nucleus'][pos_tag][e_nucleus]
                    ratio = count_e_in_pos / self.pos_counts[pos_tag] if self.pos_counts[pos_tag] else 0
                    if ratio > min_freq_ratio:
                        examples = self._get_examples('nucleus', e_nucleus, specific_pos=[pos_tag])
                        rules.append(f"  - Có xu hướng xuất hiện trong **{pos_tag}** (tỷ lệ: {ratio:.2f}) (ví dụ: {', '.join(examples)})")
        
        if self.component_frequencies['nucleus'][o_nucleus] > min_total_freq:
            rules.append(f"\n- Xu hướng của Âm chính /{o_nucleus}/:")
            for pos_tag in ['Vt', 'Vi', 'Aa', 'Na', 'Nc', 'Ng']:
                if self.pos_counts[pos_tag] > min_total_freq:
                    count_o_in_pos = self.pos_phoneme_counts['nucleus'][pos_tag][o_nucleus]
                    ratio = count_o_in_pos / self.pos_counts[pos_tag] if self.pos_counts[pos_tag] else 0
                    if ratio > min_freq_ratio:
                        examples = self._get_examples('nucleus', o_nucleus, specific_pos=[pos_tag])
                        rules.append(f"  - Có xu hướng xuất hiện trong **{pos_tag}** (tỷ lệ: {ratio:.2f}) (ví dụ: {', '.join(examples)})")
        
        d_onset = self.phonemizer.onset_map.get('đ', 'd')
        rules.append(f"\n- Xu hướng của từ bắt đầu bằng âm đầu /{d_onset}/ (chữ 'đ'):")
        
        total_d_onset_syllables_with_pos = sum(self.pos_phoneme_counts['onset'][tag][d_onset] for tag in self.pos_counts.keys())
        if total_d_onset_syllables_with_pos > min_total_freq:
            for pos_tag in ['Vt', 'Vi', 'Aa', 'Na', 'Nc', 'Ng']:
                if self.pos_counts[pos_tag] > min_total_freq:
                    count_d_in_pos = self.pos_phoneme_counts['onset'][pos_tag][d_onset]
                    ratio = count_d_in_pos / total_d_onset_syllables_with_pos if total_d_onset_syllables_with_pos else 0
                    if ratio > min_freq_ratio:
                        examples = self._get_examples('onset', d_onset, specific_pos=[pos_tag])
                        rules.append(f"  - Có xu hướng liên quan đến **{pos_tag}** (tỷ lệ: {ratio:.2f} trên tổng số âm tiết có âm đầu /{d_onset}/) (ví dụ: {', '.join(examples)})")

        return rules

    def _analyze_semantic_tendencies(self, min_total_freq=5):
        rules = []
        rules.append("\n### Bình diện ngữ nghĩa: Xu hướng âm vị theo Ý nghĩa")

        m_onset = self.phonemizer.onset_map.get('m', 'm')
        rules.append("- **Xu hướng âm đầu 'm' cho từ chỉ mẹ:**")
        
        total_m_onset_in_nouns = 0
        for pos_tag in ['Nc', 'Ng']:
            total_m_onset_in_nouns += self.pos_phoneme_counts['onset'][pos_tag][m_onset]
        
        if total_m_onset_in_nouns > min_total_freq:
            mother_examples = [sy_comp['orth_syllable'] for sy_comp in self.syllable_data 
                               if sy_comp['onset'] == m_onset and 
                                  any(tag in sy_comp['pos_tags'] for tag in ['Nc', 'Ng']) and
                                  sy_comp['orth_syllable'] in ["mẹ", "má", "mợ", "mụ", "mầm"]][:3] 
            if not mother_examples: 
                 mother_examples = self._get_examples('onset', m_onset, specific_pos=['Nc', 'Ng'])

            rules.append(f"  * Âm đầu /{m_onset}/ xuất hiện trong danh từ ({total_m_onset_in_nouns} lần). Dựa trên kiến thức ngữ nghĩa, nhiều từ chỉ mẹ hoặc các mối quan hệ họ hàng (ví dụ: {', '.join(mother_examples)}) bắt đầu bằng âm này, thể hiện một mối liên hệ ngữ âm-ngữ nghĩa.")
        else:
            rules.append(f"  * Âm đầu /{m_onset}/ không đủ tần suất trong dữ liệu mẫu để rút ra kết luận tự động rõ ràng cho xu hướng này.")


        rules.append(f"\n- **Xu hướng âm vị cho ý nghĩa 'không ổn định' (kiểu 'chênh vênh'):**")
        rules.append(f"  * Các từ ghép như 'chênh vênh', 'chạng vạng', 'chóng vánh', 'chật vật', 'chới với' thường có cấu trúc âm vị lặp (ch-vần, ch-vần) và mang ý nghĩa 'không ổn định', 'khó khăn', 'trạng thái lơ lửng'. Đây là một mẫu ngữ âm-ngữ nghĩa có thể quan sát được.")
        
        rules.append(f"\n- **Xu hướng từ đơn với âm chính hoặc âm đầu cụ thể:**")
        e_am_chinh = self.phonemizer.nucleus_map.get('e', 'e')
        o_am_chinh = self.phonemizer.nucleus_map.get('ô', 'o')
        d_am_dau = self.phonemizer.onset_map.get('đ', 'd')

        e_examples = self._get_examples('nucleus', e_am_chinh)
        rules.append(f"  * **Âm chính /{e_am_chinh}/ (ví dụ: {', '.join(e_examples)}):** Trong tiếng Việt, các từ đơn có âm chính này có thể liên quan đến nhiều ý nghĩa khác nhau, từ danh từ, động từ đến cảm thán. Không có một xu hướng nghĩa rõ ràng chỉ từ âm chính.")
        
        o_examples = self._get_examples('nucleus', o_am_chinh)
        rules.append(f"  * **Âm chính /{o_am_chinh}/ (ví dụ: {', '.join(o_examples)}):** Các từ đơn có âm chính này cũng thể hiện sự đa dạng về ngữ nghĩa. ")
        
        d_examples = self._get_examples('onset', d_am_dau)
        rules.append(f"  * **Âm đầu /{d_am_dau}/ (chữ 'đ') (ví dụ: {', '.join(d_examples)}):** Các từ bắt đầu bằng âm này bao gồm nhiều loại từ và phạm trù ý nghĩa. Việc tìm kiếm một xu hướng nghĩa chung từ âm đầu đơn lẻ rất khó và thường không có quy luật rõ ràng.")

        return rules


    def analyze_all_rules(self):
        self.rules_output = []
        self._prepare_data()
        
        self.rules_output.extend(self._analyze_phonemic_cooccurrence_rules())
        self.rules_output.extend(self._analyze_grammatical_tendencies())
        self.rules_output.extend(self._analyze_semantic_tendencies())
        
        return self.rules_output