from pyswip import Prolog

prolog = Prolog()

prolog.consult("loan_rules.pl")

result = list(
    prolog.query(
        "loan_eligible(30, 50000, salaried, 780, 10000)"
    )
)

print("Loan Eligibility:", result)

risk_result = list(
    prolog.query(
        "risk_level(780, 10000, 50000, Risk)"
    )
)

print("Risk Result:", risk_result)
