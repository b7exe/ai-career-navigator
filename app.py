from flask import Flask, render_template, request, jsonify
from logic.engine import analyze_interests, generate_roadmap

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/careers")
def careers():
    interests = request.args.get("q", "").strip()
    roles = analyze_interests(interests, top_n=6)
    return render_template("careers.html", roles=roles, interests=interests)


@app.route("/roadmap")
def roadmap():
    slug = request.args.get("role", "").strip()
    interests = request.args.get("q", "").strip()   # passed through for back-link
    data = generate_roadmap(slug)
    return render_template("roadmap.html", roadmap=data, interests=interests)


# ── Legacy routes (keep assessment & dashboard working) ────────────────────
@app.route("/assessment")
def assessment():
    return render_template("assessment.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
