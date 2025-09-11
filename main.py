from vietnamese_phonemizer import VietnamesePhonemizer

def process_input(user_input):
    if not user_input:
        return "Please enter some text!"
    vietnamese_phonemizer = VietnamesePhonemizer()
    result = vietnamese_phonemizer.phonemize(user_input)
    return result

if __name__ == "__main__":
    from app_interface import create_demo
    demo = create_demo()
    demo.launch()