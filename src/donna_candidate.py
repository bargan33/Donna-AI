
from typing import List, Tuple
from gpt_caller import GPTCaller
from utils.string import is_question_code, is_question_unit_tests, is_question_full_name, is_question_email, is_question_phone_number, is_question_cv


class DonnaCandidate:
    def __init__(self, qa: List[Tuple[str, str]], requirements: str):
        self.qa = qa
        self.full_name = ''
        self.email = ''
        self.phone_number = ''
        self.soft_skill_rating = -1
        self.code_check = ""
        self.code_rating = -1
        self.unit_test_rating = ""
        self.requirements = requirements

        self.code_qa = ('', '')
        self.utest_qa = ('', '')
        self.cv = ''
        self.total_rating = -1

        # find code, unit tests
        unwanted = []
        for i in range(len(qa)):
            q, a = qa[i]
            if is_question_full_name(q):
                self.full_name = a
                unwanted.append(i)
            elif is_question_email(q):
                self.email = a
                unwanted.append(i)
            elif is_question_phone_number(q):
                self.phone_number = str(a)
                unwanted.append(i)
            elif is_question_code(q):
                self.code_qa = (q, a)
                unwanted.append(i)
            elif is_question_unit_tests(q):
                self.utest_qa = (q, a)
                unwanted.append(i)
            elif is_question_cv(q):
                self.cv = a
                unwanted.append(i)
        for ele in sorted(unwanted, reverse=True):
            del self.qa[ele]

    def evaluate(self):
        questions = '\n'.join([qa[0] for qa in self.qa])
        answers = '\n'.join([qa[1] for qa in self.qa])
        self.soft_skill_rating = GPTCaller.query_questions(
            questions, answers, self.requirements)
        task, code = self.code_qa  # tuple unfolding
        self.code_check = GPTCaller.query_programming_task_check(code, task)
        if (self.code_check == "Correct"):
            self.code_rating = GPTCaller.query_programming_task_rate(
                code, task)
            test_src = self.utest_qa[1]
            self.unit_test_rating = GPTCaller.query_unit_test(
                code, test_src, task)

        self.total_rating = self.soft_skill_rating + self.code_rating
        if (self.code_check == 'Correct'):
            self.total_rating += 50
        if (self.unit_test_rating == 'Correct'):
            self.total_rating += 50

    def to_dict(self) -> dict:
        return {
            'full_name': self.full_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'soft_skill_rating': self.soft_skill_rating,
            'code_check': self.code_check,
            'code_rating': self.code_rating,
            'utest_rating': self.unit_test_rating,
            'total_rating': self.total_rating,
            'cv': self.cv}

    @staticmethod
    def from_dict(candidate, requirements: str) -> dict:
        dc = DonnaCandidate([("", "")], requirements)
        dc.full_name = candidate['full_name']
        dc.email = candidate['email']
        dc.phone_number = candidate['phone_number']
        dc.soft_skill_rating = candidate['soft_skill_rating']
        dc.code_check = candidate['code_check']
        dc.code_rating = candidate['code_rating']
        dc.unit_test_rating = candidate['utest_rating']
        dc.total_rating = candidate['total_rating']
        dc.cv = candidate['cv']
        return dc

    def __repr__(self) -> str:
        res = "DonnaCandidate" + '\n'
        res += "\tFull QA: " + str(self.qa) + '\n'
        res += "\tCode QA: " + str(self.code_qa) + '\n'
        res += "\tUtest QA: " + str(self.utest_qa) + '\n'
        res += "\tFull Name: " + str(self.full_name) + '\n'
        res += "\tEmail: " + str(self.email) + '\n'
        res += "\tPhone number: " + str(self.phone_number) + '\n'
        res += "\tSoft Skill Rating: " + str(self.soft_skill_rating) + '\n'
        res += "\tCode Check: " + str(self.code_check) + '\n'
        res += "\tCode Rating: " + str(self.code_rating) + '\n'
        res += "\tUnit Test Rating: " + str(self.unit_test_rating) + '\n'
        res += "\tTotal Rating: " + str(self.total_rating) + '\n'
        res += "\tCV: " + str(self.cv == '') + '\n'
        return res
