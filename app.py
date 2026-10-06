from flask import Flask, render_template, request
from pyswip import Prolog
import sqlite3

app = Flask(__name__)

# Connect Python with Prolog
prolog = Prolog()
prolog.consult("loan_rules.pl")


# ---------------- DATABASE ----------------

def create_database():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            income REAL,
            employment TEXT,
            credit_score INTEGER,
            debt REAL,
            loan_amount REAL,
            eligibility TEXT,
            risk TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():

    return render_template("index.html")

# ---------------- VIEW APPLICATIONS ----------------

@app.route("/applications")
def applications():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications")

    applications = cursor.fetchall()

    conn.close()

    return render_template(
        "applications.html",
        applications=applications
    )
# ---------------- CHECK LOAN ----------------

@app.route("/check", methods=["POST"])
def check_loan():

    name = request.form["name"]
    age = int(request.form["age"])
    income = float(request.form["income"])
    employment = request.form["employment"]
    credit_score = int(request.form["credit_score"])
    debt = float(request.form["debt"])
    loan_amount = float(request.form["loan_amount"])


    # ---------- PROLOG ELIGIBILITY ----------

    eligible = list(
        prolog.query(
            f"loan_eligible({age}, {income}, "
            f"{employment}, {credit_score}, {debt})"
        )
    )


    if eligible:

        eligibility = "Eligible"


        # ---------- RISK ----------

        risk_result = list(
            prolog.query(
                f"risk_level({credit_score}, "
                f"{debt}, {income}, Risk)"
            )
        )

        if risk_result:
            risk = str(risk_result[0]["Risk"])
        else:
            risk = "high"


        # ---------- REASONS ----------

        reasons = []

        result = prolog.query(
            f"reason({age}, {income}, {employment}, "
            f"{credit_score}, {debt}, Reason)"
        )

        for item in result:
            reasons.append(str(item["Reason"]))

        result.close()


    else:

        eligibility = "Not Eligible"
        risk = "high"

        reasons = []


        # ---------- FAILED CONDITIONS ----------

        if age < 21 or age > 60:

            reasons.append(
                "Age must be between 21 and 60"
            )


        if income < 25000:

            reasons.append(
                "Monthly income must be at least 25000"
            )


        if employment not in [
            "salaried",
            "self_employed"
        ]:

            reasons.append(
                "Employment type is not accepted"
            )


        if credit_score < 650:

            reasons.append(
                "Credit score must be at least 650"
            )


        if debt > income * 0.5:

            reasons.append(
                "Existing debt is too high compared to income"
            )


    # ---------- SAVE TO DATABASE ----------

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications
        (
            name,
            age,
            income,
            employment,
            credit_score,
            debt,
            loan_amount,
            eligibility,
            risk
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        income,
        employment,
        credit_score,
        debt,
        loan_amount,
        eligibility,
        risk
    ))

    conn.commit()
    conn.close()


    # ---------- SHOW RESULT ----------

    return render_template(
        "result.html",
        name=name,
        age=age,
        income=income,
        employment=employment,
        credit_score=credit_score,
        debt=debt,
        loan_amount=loan_amount,
        eligibility=eligibility,
        risk=risk,
        reasons=reasons
    )


# ---------------- RUN FLASK ----------------

if __name__ == "__main__":

    create_database()

    app.run(debug=True)
