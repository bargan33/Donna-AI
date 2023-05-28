import openai

# GET API KEY
with open('keys/gpt_api_key.txt', 'r') as file:
    openai.api_key = file.read().strip()


class GPTCaller:
    @staticmethod
    def query_questions(questions: str, answers: str, requirements: str) -> int:
        query = f'''
        QUESTIONS:
        {questions}

        APPLICANT'S ANSWERS:
        {answers}

        COMPANY'S REQUIREMENTS:
        {requirements}
        '''

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": QUESTIONS_SYSTEM_CONTEXT
                },
                {
                    "role": "user",
                    "content": query
                }],
            max_tokens=2,
            temperature=0.33,
        )

        rating = response['choices'][0]['message']['content']
        return int(rating)

    @staticmethod
    def query_cv(path_to_file: str, query: str):
        return "ok"

    @staticmethod
    def query_programming_task_check(code: str, task: str):
        user_message = {
            "role": "user",
            "content": f"Task: {task}\n\nCode:\n{code}"
        }

        messages = TASK_CHECK_SYSTEM_CONTEXT.copy()
        messages.append(user_message)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=10,
            temperature=0.07,
            top_p=1
        )
        result = (response['choices'][0]['message']['content'])
        return result

    @staticmethod
    def query_programming_task_rate(code: str, task: str) -> int:
        user_message = {
            "role": "user",
            "content": f"Task: {task}\n\nCode:\n{code}"
        }

        messages = TASK_RATE_SYSTEM_CONTEXT.copy()
        messages.append(user_message)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=2,
            temperature=0.31,
            top_p=1
        )
        result = (response['choices'][0]['message']['content'])
        return int(result)

    @staticmethod
    def query_unit_test(code: str, test: str, task: str):
        user_message = {
            "role": "user",
            "content": f"TASK:\n{task}\n\nCODE:\n{code}\n\nUNIT TEST:\n{test}"
        }

        messages = UNIT_TEST_SYSTEM_CONTEXT.copy()
        messages.append(user_message)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=15,
            temperature=0.3,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return (response.choices[0].message['content'])


# System Context
QUESTIONS_SYSTEM_CONTEXT = '''
You are a recruiter in an IT company. You are reviewing applicants' survey answers and trying to determine who would be the best fit to the company, regardless of their programming skills. 
You will be given the survey questions and an applicant's answers, as well as the traits your company is looking for in a new employee, and your task is to provide a rating of how well this person fits to the company.
You know that applicants will do their best to paint a great image of themselves in hope of getting accepted, so try to take their responses with a grain of salt.
Rate the person's compatibility with the company on a 1-100 scale.
You answer should only include the rating, with no explanation, for example:
 "72"
'''

TASK_CHECK_SYSTEM_CONTEXT = [
    {
        "role": "system",
        "content": "You are an IT recruiter looking through an applicant's application. You evaluate whether the code they've written works as expected. Run a simulation with a few cases you deem appropriate and check if it works correctly. You answer with one word only: Correct or Incorrect."
    },
    {
        "role": "user",
        "content": "TASK: Write a function that takes in a list of numbers and returns the sum of all even numbers in the list.\n\nRequirements:\n\nThe function should be named 'sum_even_numbers' and take a single parameter, which is a list of integers.\nThe function should return an integer, which is the sum of all even numbers in the list.\nIf the list is empty or contains no even numbers, the function should return 0.\n\nCODE: \ndef sum_even_numbers(numbers):\n    even_sum = 0\n    for num in numbers:\n        if num % 2 == 0:\n            even_sum += num\n    return even_sum"
    },
    {
        "role": "assistant",
        "content": "Correct"
    },
    {
        "role": "user",
        "content": "TASK: Write a function that takes in a list of integers and returns the two numbers whose sum is closest to zero. If there are multiple pairs with the same closest sum, return the pair with the smallest absolute difference between the two numbers.\n\nRequirements:\n\nThe function should be named 'find_closest_sum_pair' and take a single parameter, which is a list of integers.\nThe function should return a tuple containing the two numbers whose sum is closest to zero.\nIf the list has less than two numbers, the function should return None.\nIf there are multiple pairs with the same closest sum, return the pair with the smallest absolute difference between the two numbers.\nThe order of the numbers in the tuple does not matter.\n\nCODE:\ndef find_closest_sum_pair(numbers):\n    if len(numbers) < 2:\n        return None\n    closest_sum = numbers[0] + numbers[1]\n    closest_pair = (numbers[0], numbers[1])\n    for i in range(len(numbers) - 1):\n        current_sum = numbers[i] + numbers[i+1]\n        if abs(current_sum) < abs(closest_sum):\n            closest_sum = current_sum\n            closest_pair = (numbers[i], numbers[i+1])\n    return closest_pair"
    },
    {
        "role": "assistant",
        "content": "Incorrect"
    }
]


TASK_RATE_SYSTEM_CONTEXT = [
    {
        "role": "system",
        "content": "You are an IT recruiter grading applicant's code submissions. Your task is to grade the submitted code in terms of its quality - it has already been detected that the code works to achieve the specified task. You will be provided with the application task and the applicant's code, and you will be supposed to evaluate, giving a score on a scale of 1-100, with 1 being terribly written code, and 100 being perfectly written code. The specific points you are to consider are: Code Optimization (35 points), Time and Space Complexity (15 points), Redundancy (10 points), Scalability (10 points), Code Conciseness and Readability (35 points), Formatting (10 points), Comments and Documentation (10 points), Code Structure (15 points), Adherence to Best Practices (30 points), Code Safety (10 points), Use of Appropriate Data Structures and Libraries (10 points), Modularity and Maintainability (10 points). Answer only with the point total of the code, for example: '87', do not write any explanations, I only need the overall score."
    },
    {
        "role": "user",
        "content": "Task: Write a function that takes in a list of strings and returns a new list with the strings sorted in descending order of their lengths. If two or more strings have the same length, maintain their relative order in the original list.\n\nCode:\ndef sort_strings_by_length(strings):\n    return sorted(strings, key=len, reverse=True)"
    },
    {
        "role": "assistant",
        "content": "95"
    },
    {
        "role": "user",
        "content": "Task: Write a function that takes in a list of strings and returns a new list with the strings sorted in descending order of their lengths. If two or more strings have the same length, maintain their relative order in the original list.\n\nCode:\nfrom operator import itemgetter\n\ndef sort_strings_by_length(strings):\n    return sorted(strings, key=itemgetter(len, strings.index), reverse=True)"
    },
    {
        "role": "assistant",
        "content": "70"
    },
    {
        "role": "user",
        "content": "Task: Write a function that takes in a list of integers and returns a new list containing only the even numbers from the original list.\n\nCode:\ndef get_even_numbers(numbers):\n    even_numbers = []\n    for i in range(len(numbers)):\n        if numbers[i] % 2 == 0:\n            even_numbers.append(numbers[i])\n    return even_numbers"
    }
]


UNIT_TEST_SYSTEM_CONTEXT = [
    {
        "role": "system",
        "content": (
            "You are an IT recruiter looking through an applicant's application. "
            "You evaluate an applicant's unit test for a task they have been given to do. "
            "You are provided with: the task itself, the applicant's code, the applicant's unit test. "
            "Check whether the unit test is correctly written. "
            "You answer with one word only: Correct or Incorrect."
        ),
    },
    {
        "role": "user",
        "content": (
            "TASK:\n"
            "Design a function named find_second_largest in Python that will accept a list of integers "
            "and return the second largest number in the list. Assume that the input list will contain "
            "at least two unique integers.\n\n"
            "CODE:\n"
            "def find_second_largest(numbers):\n"
            "    if len(numbers) < 2:\n"
            "        return None\n"
            "    max_num = second_max = float('-inf')\n"
            "    for num in numbers:\n"
            "        if num > max_num:\n"
            "            second_max = max_num\n"
            "            max_num = num\n"
            "        elif num > second_max and num < max_num:\n"
            "            second_max = num\n"
            "    return second_max\n\n"
            "UNIT TEST:\n"
            "import unittest\n\n"
            "class TestFindSecondLargest(unittest.TestCase):\n"
            "    def test_find_second_largest(self):\n"
            "        self.assertEqual(find_second_largest([1, 2, 3, 4, 5]), 4)\n"
            "        self.assertEqual(find_second_largest([-1, -2, -3, -4, -5]), -2)\n"
            "        self.assertEqual(find_second_largest([5, 5, 4, 4, 3, 3, 2, 2, 1]), 4)\n"
            "        self.assertEqual(find_second_largest([9, 10, 1, 8, 7, 6, 5, 4, 3, 2, 1]), 9)\n"
            "        self.assertEqual(find_second_largest([1, 1, 2, 2]), 1)\n\n"
            "if __name__ == '__main__':\n"
            "    unittest.main()"
        ),
    },
    {"role": "assistant", "content": "Correct"},
    {
        "role": "user",
        "content": (
            "TASK:\n"
            "Write a Python function named is_palindrome that checks whether a given string is a palindrome or not. "
            "A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward "
            "and backward (ignoring spaces, punctuation, and capitalization).\n\n"
            "CODE:\n"
            "def is_palindrome(s):\n"
            "    s = ''.join(char for char in s if char.isalnum()).lower()\n"
            "    return s == s[::-1]\n\n"
            "UNIT TEST:\n"
            "import unittest\n\n"
            "class TestIsPalindrome(unittest.TestCase):\n"
            "    def test_is_palindrome(self):\n"
            "        self.assertEqual(is_palindrome('Able was I ere I saw Elba'), True)\n"
            "        self.assertEqual(is_palindrome('A man a plan a canal Panama'), True)\n"
            "        self.assertEqual(is_palindrome('Was it a car or a cat I saw'), True)\n"
            "        self.assertEqual(is_palindrome('No lemon no melon'), True)\n"
            "        self.assertEqual(is_palindrome('Red roses run no risk sir on Nurse\\'s order'), True)\n"
            "        self.assertEqual(is_palindrome('Random string'), False)\n\n"
            "if __name__ == '__main__':\n"
            "    unittest.main()"
        ),
    },
    {"role": "assistant", "content": "Correct"},
    {
        "role": "user",
        "content": (
            "TASK:\n"
            "Write a Python function named is_palindrome that checks whether a given string is a palindrome or not. "
            "A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward "
            "and backward (ignoring spaces, punctuation, and capitalization).\n\n"
            "CODE:\n"
            "def is_palindrome(s):\n"
            "    s = ''.join(char for char in s if char.isalnum()).lower()\n"
            "    return s == s[::-1]\n\n"
            "UNIT TEST:\n"
            "import unittest\n\n"
            "class TestIsPalindrome(unittest.TestCase):\n"
            "    def test_is_palindrome(self):\n"
            "        self.assertEqual(is_palindrome('Able was I ere I saw Elba'), False)\n"
            "        self.assertEqual(is_palindrome('A man a plan a canal Panama'), False)\n"
            "        self.assertEqual(is_palindrome('Was it a car or a cat I saw'), False)\n"
            "        self.assertEqual(is_palindrome('No lemon no melon'), False)\n"
            "        self.assertEqual(is_palindrome('Red roses run no risk sir on Nurse\\'s order'), False)\n"
            "        self.assertEqual(is_palindrome('Random string'), True)\n\n"
            "if __name__ == '__main__':\n"
            "    unittest.main()"
        ),
    },
    {"role": "assistant", "content": "Incorrect"},
]
