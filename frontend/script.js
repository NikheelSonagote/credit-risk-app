async function predict() {
  const data = {
    age: parseInt(document.getElementById("age").value),
    amount: parseInt(document.getElementById("amount").value),
    duration: parseInt(document.getElementById("duration").value),
    status: document.getElementById("status").value,

    // Default values for fields not in the HTML form
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

  try {
    const response = await fetch(
      "https://credit-risk-app-production-0929.up.railway.app/predict",
      {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      },
    );

    const result = await response.json();

    if (result.error) {
      document.getElementById("result").innerText = "Error: " + result.error;
    } else {
      document.getElementById("result").innerText =
        result.prediction === 1
          ? `Approved ✅ (Prob: ${result.probability})`
          : `Risky ❌ (Prob: ${result.probability})`;
    }
  } catch (err) {
    document.getElementById("result").innerText =
      "Server is offline or URL is wrong.";
  }
}
