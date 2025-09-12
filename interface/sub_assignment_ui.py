import gradio as gr

class subAssigmentCollapsibleUI:
    def __init__(self, label, open=False):
        self.label = label
        self.open = open
        self.block = gr.Accordion(label, open=open)

    def fill_content(self):
        # To be filled by user
        pass
