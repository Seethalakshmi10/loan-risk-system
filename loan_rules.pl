% =========================================
% LOAN ELIGIBILITY & RISK ASSESSMENT SYSTEM
% =========================================

% ---------- AGE RULE ----------

age_eligible(Age) :-
    Age >= 21,
    Age =< 60.


% ---------- INCOME RULE ----------

income_eligible(Income) :-
    Income >= 25000.


% ---------- EMPLOYMENT RULE ----------

employment_eligible(salaried).

employment_eligible(self_employed).


% ---------- CREDIT SCORE RULE ----------

credit_eligible(Score) :-
    Score >= 650.


% ---------- DEBT RULE ----------

debt_eligible(Debt, Income) :-
    Debt =< Income * 0.5.


% ---------- OVERALL ELIGIBILITY ----------

loan_eligible(Age, Income, Employment, Score, Debt) :-
    age_eligible(Age),
    income_eligible(Income),
    employment_eligible(Employment),
    credit_eligible(Score),
    debt_eligible(Debt, Income).


% =========================================
% RISK ASSESSMENT
% =========================================

% LOW RISK

risk_level(Score, Debt, Income, low) :-
    Score >= 750,
    Debt =< Income * 0.3.


% MEDIUM RISK

risk_level(Score, Debt, Income, medium) :-
    Score >= 650,
    Score < 750,
    Debt =< Income * 0.5.


% HIGH RISK - LOW CREDIT SCORE

risk_level(Score, _, _, high) :-
    Score < 650.


% HIGH RISK - HIGH DEBT

risk_level(_, Debt, Income, high) :-
    Debt > Income * 0.5.


% =========================================
% REASONS
% =========================================

reason(Age, _, _, _, _, 'Age is within the acceptable range') :-
    age_eligible(Age).

reason(_, Income, _, _, _, 'Income meets the minimum requirement') :-
    income_eligible(Income).

reason(_, _, Employment, _, _, 'Employment type is acceptable') :-
    employment_eligible(Employment).

reason(_, _, _, Score, _, 'Credit score meets the minimum requirement') :-
    credit_eligible(Score).

reason(_, Income, _, _, Debt, 'Existing debt is within the acceptable limit') :-
    debt_eligible(Debt, Income).