from flask import Flask, render_template, request
from score import bestPages

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    search_results = []
    alpha = 0.5
    gamma = 0.5

    if request.method == "POST":
        print("request.form")
        print(request.form)
        user_input = request.form.get("search_text")
        alpha = float(request.form.get("alpha", 0.5))
        gamma = float(request.form.get("gamma", 0.5))

        print("debug toto", user_input, alpha, gamma)
        search_results = bestPages(alpha, gamma, user_input)

    return render_template("index.html", search_results=search_results, alpha=alpha, gamma=gamma)

if __name__ == "__main__":
    app.run(debug=True)
