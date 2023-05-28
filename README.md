# Overview

`Donna AI` is an applet meant for simplifying the IT recruitment process. 
Using the Forms API the recruiter can set up a session, simply by clicking 'new session' and entering the Forms link. 
Donna then downloads all relevant data and analyzes it to give the recruiter a suitable overview of how the applicants present themselves in relation to others.

## Forms Keywords
There are a few keywords to be used within the form questions for specific data recognition within the api (Most are self-explanatory):
```
[Full name] candidate responds with his/her full name

[E-mail] - Candidate responds with his/her email

[Phone number] - Candidate responds with phone number.

[Coding Task] - contains a coding task. Does NOT require a solution, though it does of course need to be solvable. If the solution proves to be correct via a call to GPT, it is evaluated in terms of code cleanliness and efficiency.

[Unit Test] - if the coding task proves to be correct, the applicant's unit testing abilities can be put to test. Evaluated on a correct/incorrect basis, seeing only if the test covers the coding task completely.

[CV] - must contain the applicant's CV in text format. We have a pdf parser, but figured it would be unnecessary to get the point across, since parsing would be an extra step to test and implement. 

Lastly, everything else is interpreted as a soft skill and is evaluated via a GPT call, taking into account recruiter-specified company requirements.

```

## Interpreting the results
By clicking onto a session one can see the results. 
Then, by clicking 'evaluate' we can see how the applicants have been rated by the AI system.
Results can be sorted by any parameter: Either alphabetically by name/email, or numerically through their various scores (soft skill scores/coding scores/total scores et cetera). Moreover, a chat session with GPT can be started from the session results view to ask any questions about a given applicant's CV.


# Set up for use
```
    python -m venv venv
    pip install -r requirements.txt
```

## API Keys
Within the `src/` and `test/` there needs to be a `keys/` folder, containing two files:
`google_api_key.json` and `GPT_API_KEY.txt`.

## API's
Make sure the `Google Forms` and `Openai` api's are set up correctly. 


## Testing
To see if the app works correctly, you may test it using the `pytest` framework. See 'set up for development' for more details.

# Set up for development
```
    python -m venv venv
    pip install -r requirements-dev.txt
```

## API Keys
Within the `src/` and `test/` there needs to be a `keys/` folder, containing two files:
`google_api_key.json` and `GPT_API_KEY.txt`.

## API's
Make sure the `Google Forms` and `Openai` api's are set up correctly. 

## Run tests
Make sure the keys are set up

```
    cd tests/
    pytest
```
