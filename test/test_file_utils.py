from utils.file import save_to_json_file, parse_json_file
import os


def test_save_read_json():
    test_d = {"a": 1, "b": 2}
    fname = "test_read_save.json"
    save_to_json_file(test_d, fname)
    assert os.path.exists(fname)
    test_r = parse_json_file(fname)

    os.remove(fname)

    assert test_r['a'] == 1 and test_r['b'] == 2
