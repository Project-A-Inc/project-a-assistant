
from project_a_assistant.utils import safe_json_list, truncate

def test_safe_json_list():
    assert safe_json_list('{"tools": ["a"]}') == ["a"]
    assert safe_json_list('nonsense') == []

def test_truncate():
    long = '{' + '"k":"v",'*2000 + '"e":1}'
    assert isinstance(truncate(long), str)
