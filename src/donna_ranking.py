from __future__ import annotations
from donna_session import DonnaSession
from donna_candidate import DonnaCandidate
from forms_caller import FormsCaller
from utils.string import extract_form_id_from_link
from utils.file import save_to_json_file, parse_json_file
from time import sleep


class DonnaRanking:
    def __init__(self):
        self.form_id = ''
        self.comp_reqs = ''
        self.candidates = []

    def init(self, session: DonnaSession):
        self.form_id = extract_form_id_from_link(session.forms_link)
        self.comp_reqs = session.comp_reqs
        self.dir_path = session.dir_path
        fc = FormsCaller(self.form_id)
        QA = fc.get_qa()
        class_candidates = [DonnaCandidate(
            qa, self.comp_reqs) for qa in QA]
        self.candidates = [c.to_dict() for c in class_candidates]
        self.to_json(self.dir_path + '/donna_ranking.json')

    def evaluate(self):
        fc = FormsCaller(self.form_id)
        QA = fc.get_qa()
        class_candidates = [DonnaCandidate(
            qa, self.comp_reqs) for qa in QA]
        for c in class_candidates:
            c.evaluate()
            print('waiting so we don\'t overload the api')
            sleep(20)
        self.candidates = [c.to_dict() for c in class_candidates]
        self.to_json(self.dir_path + '/donna_ranking.json')

    def to_dict(self) -> dict:
        return {
            'form_id': self.form_id,
            'comp_reqs': self.comp_reqs,
            'dir_path': self.dir_path,
            'candidates': self.candidates
        }

    def to_json(self, path_to_json_file: str):
        save_to_json_file(self.to_dict(), path_to_json_file)

    @staticmethod
    def from_json(path_to_json_file: str) -> DonnaRanking:
        json_dict = parse_json_file(path_to_json_file)
        return DonnaRanking.from_dict(json_dict)

    @staticmethod
    def from_dict(ranking_dict: dict) -> DonnaRanking:
        dr = DonnaRanking()
        dr.form_id = ranking_dict['form_id']
        dr.comp_reqs = ranking_dict['comp_reqs']
        dr.dir_path = ranking_dict['dir_path']
        dr.candidates = ranking_dict['candidates']
        return dr

    def sort(self):
        self.candidates = sorted(
            self.candidates, key=lambda d: d['total_rating'], reverse=True)
