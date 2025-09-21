from .sub_assignment_ui import subAssigmentCollapsibleUI
import gradio as gr
import os
import string
from controller.vietnamese_phonemizer import VietnamesePhonemizer
from controller.dictionary_loader import DictionaryLoader
from controller.syllable_counter import SyllableCounter
from controller.vietnamese_phonotactic_rules_analyzer import VietnamesePhonotacticRulesAnalyzer

PAGE_SIZE = 12

dict_loader = DictionaryLoader()
phonemizer = VietnamesePhonemizer()
syllable_counter = SyllableCounter(phonemizer)

def get_page(lines, page, page_size=PAGE_SIZE):
    start = page * page_size
    end = start + page_size
    return lines[start:end]

def get_letter_to_page_map(lines, page_size=PAGE_SIZE):
    letter_to_page = {}
    seen = set()
    for idx, line in enumerate(lines):
        if not line:
            continue
        first_char = line.split("\t")[0][:1].upper()
        if first_char not in seen and first_char.isalpha():
            seen.add(first_char)
            page = idx // page_size
            letter_to_page[first_char] = page
    return letter_to_page

# Custom CSS for square navigation buttons
custom_css = '''
    #nav-prev-btn, #nav-next-btn, #goto-btn {
        width: 32px !important;
        height: 32px !important;
        min-width: 32px !important;
        max-width: 32px !important;
        min-height: 32px !important;
        max-height: 32px !important;
        padding: 0 !important;
        margin: 2px !important;
        font-size: 16px !important;
        border-radius: 6px !important;
        box-sizing: border-box !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    #goto-input {
        width: 80px !important;
        height: 32px !important;
        font-size: 16px !important;
        margin: 2px !important;
        border-radius: 6px !important;
        box-sizing: border-box !important;
        text-align: center !important;
    }
'''


def assignment2_ui_2_1():
    ui = subAssigmentCollapsibleUI("2.1/ Số lượng âm tiết tiếng Việt khác nhau có trong từ điển", open=True)
    with ui.block:
        count = syllable_counter.count_unique_syllables([line.split("\t")[0] for line in dict_loader.get_lines() if line])
        written_syllables = set()
        for line in dict_loader.get_lines():
            if line:
                words = line.split("\t")[0].strip().split()
                written_syllables.update(words)
        written_syllables_str = ", ".join(sorted(written_syllables))
        gr.Textbox(value=str(count), label="Số lượng âm tiết duy nhất", interactive=False)
        gr.Textbox(value=written_syllables_str, label="Danh sách âm tiết duy nhất (cách nhau bởi dấu phẩy)", interactive=False)

def assignment2_ui_2_2():
    ui = subAssigmentCollapsibleUI("2.2/ Số lượng âm tiết khả dĩ có trong tiếng Việt tính theo tổ hợp", open=True)
    with ui.block:
        gr.Markdown("[Phụ âm đầu * Âm Đệm * Âm Chính * Âm Cuối * Thanh điệu]")

        n_onset = len(phonemizer.onset_map)
        n_glide = len(phonemizer.glide_map) + 1  # +1 for no-glide
        n_nucleus = len(phonemizer.nucleus_map)
        n_coda = len(phonemizer.coda_map) + 1    # +1 for no-coda
        n_tone = len(phonemizer.tone_map)

        with gr.Accordion(f"Bản đồ phụ âm đầu (onset) — Số lượng: {n_onset}", open=False):
            gr.Dataframe(
                headers=["Phụ âm đầu", "Phiên âm"],
                value=[[k, v] for k, v in phonemizer.onset_map.items()],
                interactive=False
            )
        with gr.Accordion(f"Bản đồ âm đệm (glide) — Số lượng: {len(phonemizer.glide_map)} (+1 không âm đệm) = {n_glide}", open=False):
            gr.Dataframe(
                headers=["Âm đệm", "Phiên âm"],
                value=[[k, v] for k, v in phonemizer.glide_map.items()],
                interactive=False
            )
        with gr.Accordion(f"Bản đồ âm chính (nucleus) — Số lượng: {n_nucleus}", open=False):
            gr.Dataframe(
                headers=["Âm chính", "Phiên âm"],
                value=[[k, v] if not isinstance(v, dict) else [k, str(v)] for k, v in phonemizer.nucleus_map.items()],
                interactive=False
            )
        with gr.Accordion(f"Bản đồ âm cuối (coda) — Số lượng: {len(phonemizer.coda_map)} (+1 không âm cuối) = {n_coda}", open=False):
            gr.Dataframe(
                headers=["Âm cuối", "Phiên âm"],
                value=[[k, v] for k, v in phonemizer.coda_map.items()],
                interactive=False
            )
        with gr.Accordion(f"Bản đồ thanh điệu (tone) — Số lượng: {n_tone}", open=False):
            gr.Dataframe(
                headers=["Thanh điệu", "Ký hiệu"],
                value=[[k, v] for k, v in phonemizer.tone_map.items()],
                interactive=False
            )

        possible_syllables = phonemizer.count_possible_syllables()
        formula_str = f"Số lượng âm tiết khả dĩ = onset * glide * nucleus * coda * tone = {n_onset} * {n_glide} * {n_nucleus} * {n_coda} * {n_tone} = {possible_syllables}"
        gr.Textbox(value=formula_str, label="Công thức tính số lượng âm tiết khả dĩ", interactive=False)

def assignment2_ui_2_3():
    ui = subAssigmentCollapsibleUI(
        "2.3/ So sánh 2 con số (2.1) và (2.2) và giải thích lý do tại sao có sự chênh lệch này?",
        open=True
    )

    with ui.block:
        # folder of the current script
        script_dir = os.path.dirname(__file__)
        # go one level up to project root
        project_root = os.path.abspath(os.path.join(script_dir, ".."))
        # build relative path to resources
        md_path = os.path.join(project_root, "resources", "assignment2.3.md")

        # read content
        with open(md_path, encoding="utf-8") as f:
            md_content = f.read()

        gr.Markdown(md_content)

def assignment2_ui_2_4():
    ui = subAssigmentCollapsibleUI("2.4/ Phân tích quy luật ngữ âm - ngữ pháp - ngữ nghĩa của tiếng Việt", open=True)
    with ui.block:
        analyzer = VietnamesePhonotacticRulesAnalyzer(phonemizer, dict_loader)
        rules = analyzer.analyze_all_rules()
        gr.Markdown("\n".join(rules))

def create_assignment2_demo():
    with gr.Blocks(css=custom_css) as demo:
        gr.Markdown("# Đồ án giữa kỳ #2")
        gr.Markdown("### Thành viên:")
        gr.Markdown("* Trần Quang Duy - 24C12027")
        gr.Markdown("* Đỗ Hoài Nam - 24C12021")

        with gr.Accordion(f"Xem từng trang từ điển VDic_uni ({PAGE_SIZE} dòng/trang)", open=False):
            dict_lines = dict_loader.get_lines()
            total_pages = (len(dict_lines) + PAGE_SIZE - 1) // PAGE_SIZE
            page_state = gr.State(0)

            def render_page(page):
                page_lines = get_page(dict_lines, page)
                return [[line.split("\t")[0], line.split("\t")[-1]] for line in page_lines if line]

            dataframe = gr.Dataframe(
                headers=["Từ", "Loại"],
                value=render_page(0),
                interactive=False,
                wrap=True
            )

            page_label = gr.Markdown(f"Trang 1 / {total_pages}")

            def update_page(page):
                page = max(0, min(page, total_pages - 1))
                return render_page(page), f"Trang {page+1} / {total_pages}", page

            def goto_word(word):
                word = word.strip().lower()
                for idx, line in enumerate(dict_lines):
                    if line.split("\t")[0].lower().startswith(word) and word:
                        page = idx // PAGE_SIZE
                        return update_page(page)
                return update_page(0)

            with gr.Row(equal_height=True):
                prev_btn = gr.Button("Trang trước", elem_id="nav-prev-btn")
                goto_input = gr.Textbox(placeholder="Từ...", elem_id="goto-input", show_label=False)
                goto_btn = gr.Button("Go", elem_id="goto-btn")
                next_btn = gr.Button("Trang sau", elem_id="nav-next-btn")

            prev_btn.click(lambda page: update_page(page-1), inputs=page_state, outputs=[dataframe, page_label, page_state])
            next_btn.click(lambda page: update_page(page+1), inputs=page_state, outputs=[dataframe, page_label, page_state])
            goto_btn.click(lambda word: goto_word(word), inputs=goto_input, outputs=[dataframe, page_label, page_state])

    assignment2_ui_2_1()
    assignment2_ui_2_2()
    assignment2_ui_2_3()
    assignment2_ui_2_4()
    return demo
