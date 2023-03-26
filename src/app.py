from flask import Flask, render_template, request
from score import bestPages
import urllib.parse

app = Flask(__name__)

def title_to_link(title):
    return "https://fr.wikipedia.org/wiki/" + title.replace(" ", "_")


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    alpha = 0.5
    gamma = 0.5
    user_input = ""

    if request.method == "POST":
        user_input = request.form.get("search_text")
        alpha = float(request.form.get("alpha", 0.5))
        gamma = float(request.form.get("gamma", 0.5))
        search_results = bestPages(alpha, gamma, user_input)
        results = [f"<p><a href=\"{title_to_link(sr)}\" target=\"_blank\" rel=\"noopener noreferrer\">{sr}</a></p>" for sr in search_results]

        if len(results) == 0:
            results = ["<p style=\"margin-top: 0px;margin-bottom: 0px;\">Aucun résultat trouvé...</p>"]

    return render_template("index.html", search_results=results, alpha=alpha, gamma=gamma, user_input=user_input)

if __name__ == "__main__":
    app.run()
