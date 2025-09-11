import gradio as gr
import string

PAGE_SIZE = 12

def load_dictionary():
    try:
        with open("resources/VDic_uni.txt", encoding="utf-8") as f:
            lines = [line.strip() for line in f]
        return lines
    except Exception as e:
        return [f"Error loading dictionary: {e}"]

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

def create_assignment2_demo():
    with gr.Blocks(css=custom_css) as demo:
        gr.Markdown("# Đồ án giữa kỳ #2")
        gr.Markdown("### Số lượng âm tiết tiếng Việt khác nhau có trong từ điển.")
        gr.Markdown("### Thành viên:")
        gr.Markdown("* Trần Quang Duy - 24C12027")
        gr.Markdown("* Đỗ Hoài Nam - 24C12021")

        with gr.Accordion(f"Xem từng trang từ điển VDic_uni ({PAGE_SIZE} dòng/trang)", open=False):
            dict_lines = load_dictionary()
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
    return demo
