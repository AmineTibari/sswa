
from flask import Flask, render_template, request
from sqli.perform_injection import perform_injection


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def appinterface():

    if request.method == "POST":
        url = request.form["url"]
        scan_type = request.form["scan_type"]

        if scan_type == "SQLi":
            result = perform_injection(url)



        return render_template("interface.html", result=result, url=url)

    return render_template("interface.html", result=None)


if __name__ == "__main__":
    app.run(debug=True)
