from forms_caller import FormsCaller
import os


def test_get_qa():
    print(os.getcwd())
    url = '1fbog0GLT9gmdGR09MVUy13ZamgeSFr72sHioOoAi-BI'
    f = FormsCaller(url)
    assert f.get_qa()[0][0][0] != ''
