from utils.parser import parse_tasks

def test_parse_simple():
    text = 'Finish slides by Friday; email Sam today; read paper 30 minutes'
    tasks = parse_tasks(text)
    assert len(tasks) >= 3
