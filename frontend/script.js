async function predict() {
  const data = {
    age: parseInt(document.getElementById("age").value),
    amount: parseInt(document.getElementById("amount").value),
    duration: parseInt(document.getElementById("duration").value),
    status: document.getElementById("status").value,

    credit_history: "existing paid",
    purpose: "car",
    savings: "little",
    employment_duration: "1<=X<4",
    installment_rate: 2,
    personal_status_sex: "male single",
    other_debtors: "none",
    present_residence: 2,
    property: "real estate",
    other_installment_plans: "none",
    housing: "own",
    number_credits: 1,
    job: "skilled",
    people_liable: 1,
    telephone: "yes",
    foreign_worker: "yes",
  };

  const response = await fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();

  document.getElementById("result").innerText =
    result.prediction === 1
      ? "Approved ✅ (Prob: " + result.probability + ")"
      : "Risky ❌ (Prob: " + result.probability + ")";
}
