from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import List, Tuple


class FormsCaller:
    def __init__(self, form_id: str, credentials_file_path='keys/google_api_key.json'):
        self.form_id = form_id  # ID of your Google Form

        SCOPES = ['https://www.googleapis.com/auth/forms',
                  'https://www.googleapis.com/auth/drive']

        CREDENTIALS = service_account.Credentials.from_service_account_file(
            credentials_file_path, scopes=SCOPES
        )

        self.service = build('forms', 'v1', credentials=CREDENTIALS)


    def __query_questions(self) -> dict:
        return self.service.forms().get(formId=self.form_id).execute()

    def __parse_questions(self) -> dict:
        questions = {}
        for item in self.__query_questions()['items']:
            questions[item["questionItem"]['question']
                      ["questionId"]] = item["title"]
        return questions

    def __query_answers(self) -> dict:
        return self.service.forms().responses().list(formId=self.form_id).execute()

    def get_qa(self) -> List[List[Tuple[str, str]]]:
        questions = self.__parse_questions()
        responses = self.__query_answers()['responses']
        entries = []
        for response in responses:
            paired_qa = []
            for q in questions:
                paired_qa.append(
                    (questions[q], response['answers'][q]['textAnswers']['answers'][0]['value']))
            entries.append(paired_qa)
        return entries
