from pydantic import BaseModel

class LoanData(BaseModel):
    status: str
    duration: int
    credit_history: str
    purpose: str
    amount: int
    savings: str
    employment_duration: str
    instalment_rate: int
    personal_status_sex: str
    other_debtors: str
    present_residence: int
    property: str
    age: int
    other_installments_plans: str
    housing: str
    number_credits: int
    job: str
    people_liable: int
    telephone: str
    foreign_worker: str
