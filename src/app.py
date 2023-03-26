from flask import Flask, render_template, request
from score import bestPages
import urllib.parse

app = Flask(__name__)

def title_to_link(title):
    return  "https://fr.wikipedia.org/wiki/" + title.replace(" ", "_")
    

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    alpha = 0.5
    gamma = 0.5

    if request.method == "POST":
        user_input = request.form.get("search_text")
        alpha = float(request.form.get("alpha", 0.5))
        gamma = float(request.form.get("gamma", 0.5))
        search_results = bestPages(alpha, gamma, user_input)
        results = [(sr, title_to_link(sr)) for sr in search_results]

    return render_template("index.html", search_results=results, alpha=alpha, gamma=gamma)

if __name__ == "__main__":
    app.run()
