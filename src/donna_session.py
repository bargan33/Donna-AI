from __future__ import annotations
from utils.file import parse_json_file, save_to_json_file
from utils.string import no_whitespace, extract_form_id_from_link
from forms_caller import FormsCaller
import os
import re
import shutil

DEFAULT_COMP_REQS = '''
A person who is good at coordinating large projects, excells at
 teamwork and has at least some programming experience
'''


class DonnaSession:
    def __init__(self, session_dir_address: str):
        self.dir_path = session_dir_address
        self.config = parse_json_file(
            self.dir_path + '/donna_session_config.json')

        self.name = self.config['session_name']
        self.forms_link = self.config['forms_link']
        self.comp_reqs = self.config['comp_reqs']
        self.qa = [()]
        if os.path.exists(self.dir_path + '/QA.json'):
            self.qa = parse_json_file(self.dir_path + '/QA.json')

    def refresh(self) -> str:
        forms_caller = FormsCaller(
            extract_form_id_from_link(self.forms_link))
        self.qa = forms_caller.get_qa()
        save_to_json_file(self.qa,
                          self.dir_path + '/QA.json')

    @staticmethod
    def create_new_session(session_name: str, path_to_serde: str, forms_url: str, comp_reqs=DEFAULT_COMP_REQS) -> DonnaSession:
        if not os.path.exists(path_to_serde + session_name):
            os.mkdir(path_to_serde + session_name)
            assert (no_whitespace(path_to_serde + session_name))
            json_dict = {'session_name': session_name,
                         'forms_link': forms_url,
                         'comp_reqs': comp_reqs}
            save_to_json_file(json_dict, path_to_serde +
                              session_name + '/donna_session_config.json')
        return DonnaSession(path_to_serde + session_name)

    @staticmethod
    def remove_session(path_to_session: str):
        shutil.rmtree(path_to_session)

    def __repr__(self) -> str:
        res = "DonnaSession\n"
        res += "name:" + self.name + '\n'
        res += "dir_path:" + self.dir_path + '\n'
        res += "forms_link:" + self.forms_link + '\n'
        res += "comp_reqs:" + self.comp_reqs + '\n'
        res += "QA:" + str(self.qa) + '\n'
        return res
