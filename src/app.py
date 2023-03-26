from flask import Flask, render_template, request
from score import bestPages, test

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    search_results = []
    if request.method == "POST":
        user_input = request.form.get("search_text")
        search_results = test(user_input)

    return render_template("index.html", search_results=search_results)

if __name__ == "__main__":
    app.run(debug=True)
