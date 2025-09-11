import gradio as gr
from controller.vietnamese_phonemizer import VietnamesePhonemizer

def process_input(user_input):
    if not user_input:
        return "Please enter some text!"
    vietnamese_phonemizer = VietnamesePhonemizer()
    result = vietnamese_phonemizer.phonemize(user_input)
    return result

def create_assignment1_demo():
    with gr.Blocks() as demo:
        gr.Markdown("# Đồ án giữa kỳ #1")
        gr.Markdown("### Hãy viết chương trình phiên âm âm vị học với đầu vào là một câu tiếng Việt và đầu ra là chuỗi các âm tiết đã được phiên âm âm vị học.")
        gr.Markdown("### Thành viên:")
        gr.Markdown("* Trần Quang Duy - 24C12027")
        gr.Markdown("* Đỗ Hoài Nam - 24C12021")

        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(
                    label="Đầu vào",
                    placeholder="Enter text here...",
                    lines=2
                )
                submit_btn = gr.Button("Process Input", variant="primary")

        output_block = gr.Textbox(
            label="Phiên âm",
            lines=5,
            interactive=False
        )

        submit_btn.click(
            fn=process_input,
            inputs=input_text,
            outputs=output_block
        )
    return demo
