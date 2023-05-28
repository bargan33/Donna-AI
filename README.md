# Set Up
```
    python -m venv venv
    pip install -r requirements-dev.txt
```


# API Keys
Within the `src/` and `test/` there needs to be a `keys/` folder, containing two files:
`google_api_key.json` and `GPT_API_KEY.txt`.

# Run tests
Make sure the keys are set up
```
    cd tests/
    pytest
```