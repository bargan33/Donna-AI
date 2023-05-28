from __future__ import annotations
from donna_session import DonnaSession
from donna_candidate import DonnaCandidate
from forms_caller import FormsCaller
from utils.string import extract_form_id_from_link
# from utils.file import save_to_json_file, parse_json_file
from time import sleep


class DonnaRanking:
    def __init__(self):
        self.form_id = ''
        self.comp_reqs = ''
        self.candidates = []

    def init(self, session: DonnaSession, comp_reqs: str):
        self.form_id = extract_form_id_from_link(session.forms_link)
        self.comp_reqs = comp_reqs
        fc = FormsCaller(self.form_id)
        QA = fc.get_qa()
        class_candidates = [DonnaCandidate(
            qa, self.comp_reqs) for qa in QA]
        self.candidates = [c.to_dict() for c in class_candidates]

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

    def to_dict(self) -> dict:
        return {
            'form_id': self.form_id,
            'comp_reqs': self.comp_reqs,
            'candidates': self.candidates
        }

    @staticmethod
    def from_dict(ranking_dict: dict) -> DonnaRanking:
        dr = DonnaRanking()
        dr.form_id = ranking_dict['form_id']
        dr.comp_reqs = ranking_dict['comp_reqs']
        dr.candidates = ranking_dict['candidates']
        return dr

    def sort(self):
        self.candidates = sorted(
            self.candidates, key=lambda d: d['total_rating'], reverse=True)
