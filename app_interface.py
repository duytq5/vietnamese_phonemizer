import gradio as gr
from interface.assignment1_interface import create_assignment1_demo
from interface.assignment2_interface import create_assignment2_demo

def create_demo():
    with gr.Blocks() as demo:
        with gr.Tab("Assignment #1"):
            assignment1 = create_assignment1_demo()
        with gr.Tab("Assignment #2"):
            assignment2 = create_assignment2_demo()
    return demo
