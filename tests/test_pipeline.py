from pipeline import load_prompt_file

def test_load_prompt_file(tmp_path):
    test_file = tmp_path / "prompts.txt"
    test_file.write_text("Hello Claude\nWhat is AI?")
    prompts = load_prompt_file.fn(str(test_file))
    assert prompts == ["Hello Claude", "What is AI?"]
