from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username", "").strip()
    password = request.form.get("pwd", "").strip()

    if not username:
        return "<script>alert('Username cannot be empty.');window.history.back();</script>"
    if not password:
        return "<script>alert('Password cannot be empty.');window.history.back();</script>"
    if len(password) < 6:
        return "<script>alert('Password must be atleast 6 characters long.');window.history.back();</script>"

    return render_template("greeting.html", username=username)

if __name__ == "__main__":
    app.run(debug=True)
