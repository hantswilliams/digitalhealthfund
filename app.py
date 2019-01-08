from flask import Flask, render_template   

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/thesis")
def thesis():
    return render_template("thesis.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)


