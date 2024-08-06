from oltreai_core.utils.io_utils import read_text, read_yaml, write_yaml


def test_write_read_yaml(tmp_path):
    data = {"key": "value"}
    file_path = tmp_path / "data.yaml"

    # Test write_yaml
    write_yaml(file_path, data)
    assert file_path.is_file()

    # Test read_yaml
    read_data = read_yaml(file_path)
    assert read_data == data


def test_read_text(tmp_path):
    text = "Hello, World!"
    file_path = tmp_path / "text.txt"
    file_path.write_text(text)

    # Test read_text
    rd_text = read_text(file_path)
    assert rd_text == text
