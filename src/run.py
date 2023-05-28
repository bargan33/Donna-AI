from init import create_app
with open("keys/flask_key.txt", "r") as flask_key:
    app_key = flask_key.read()

app = create_app()
app.config['SECRET_KEY'] = app_key

if __name__ == "__main__":
    app.run(debug=True)
