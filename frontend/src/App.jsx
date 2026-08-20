import { Activity, AlertCircle, HeartPulse, Loader2 } from "lucide-react";
import { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

const startingForm = {
  age: 54,
  sex: "female",
  bmi: 31,
  systolic_bp: 145,
  diastolic_bp: 92,
  hba1c: 6.1,
  smoker: false,
  family_history: true,
  activity_level: "medium",
};

function App() {
  const [form, setForm] = useState(startingForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function updateField(name, value) {
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        throw new Error("The API could not calculate risk for those values.");
      }

      setResult(await response.json());
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="intro">
        <div>
          <p className="eyebrow">Beginner Full-Stack ML Demo</p>
          <h1>HealthRisk AI</h1>
          <p className="subtitle">
            A simple, explainable risk calculator for practicing React,
            FastAPI, validation, and basic model thinking.
          </p>
        </div>
        <div className="intro-badge">
          <HeartPulse size={28} />
          <span>Educational screening tool</span>
        </div>
      </section>

      <section className="workspace">
        <form className="panel form-panel" onSubmit={handleSubmit}>
          <div className="panel-heading">
            <Activity size={22} />
            <h2>Patient Inputs</h2>
          </div>

          <div className="form-grid">
            <NumberField
              label="Age"
              name="age"
              value={form.age}
              min="18"
              max="100"
              onChange={updateField}
            />
            <SelectField
              label="Sex"
              name="sex"
              value={form.sex}
              options={["female", "male", "other"]}
              onChange={updateField}
            />
            <NumberField
              label="BMI"
              name="bmi"
              value={form.bmi}
              min="12"
              max="70"
              step="0.1"
              onChange={updateField}
            />
            <NumberField
              label="HbA1c"
              name="hba1c"
              value={form.hba1c}
              min="3.5"
              max="15"
              step="0.1"
              onChange={updateField}
            />
            <NumberField
              label="Systolic BP"
              name="systolic_bp"
              value={form.systolic_bp}
              min="80"
              max="240"
              onChange={updateField}
            />
            <NumberField
              label="Diastolic BP"
              name="diastolic_bp"
              value={form.diastolic_bp}
              min="40"
              max="140"
              onChange={updateField}
            />
            <SelectField
              label="Activity"
              name="activity_level"
              value={form.activity_level}
              options={["low", "medium", "high"]}
              onChange={updateField}
            />
          </div>

          <div className="checks">
            <label>
              <input
                type="checkbox"
                checked={form.smoker}
                onChange={(event) => updateField("smoker", event.target.checked)}
              />
              Current smoker
            </label>
            <label>
              <input
                type="checkbox"
                checked={form.family_history}
                onChange={(event) =>
                  updateField("family_history", event.target.checked)
                }
              />
              Family history
            </label>
          </div>

          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? <Loader2 className="spin" size={18} /> : <HeartPulse size={18} />}
            Calculate Risk
          </button>
        </form>

        <section className="panel result-panel" aria-live="polite">
          <div className="panel-heading">
            <AlertCircle size={22} />
            <h2>Result</h2>
          </div>

          {error && <p className="error">{error}</p>}

          {!result && !error && (
            <div className="empty-state">
              <p>Enter values and calculate a sample risk estimate.</p>
            </div>
          )}

          {result && (
            <div className="result-content">
              <div className={`risk-score ${result.category.toLowerCase()}`}>
                <span>{result.category} Risk</span>
                <strong>{result.risk_percent}%</strong>
              </div>

              <div>
                <h3>Top Factors</h3>
                {result.top_factors.length > 0 ? (
                  <ul className="factor-list">
                    {result.top_factors.map((factor) => (
                      <li key={factor.name}>
                        <span>{factor.name}</span>
                        <meter min="0" max="2" value={factor.impact} />
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="muted">No major risk factors in this sample.</p>
                )}
              </div>

              <div>
                <h3>Simple Tips</h3>
                <ul className="tips">
                  {result.tips.map((tip) => (
                    <li key={tip}>{tip}</li>
                  ))}
                </ul>
              </div>

              <p className="disclaimer">{result.disclaimer}</p>
            </div>
          )}
        </section>
      </section>
    </main>
  );
}

function NumberField({ label, name, value, onChange, ...inputProps }) {
  return (
    <label className="field">
      <span>{label}</span>
      <input
        {...inputProps}
        type="number"
        value={value}
        onChange={(event) => onChange(name, Number(event.target.value))}
      />
    </label>
  );
}

function SelectField({ label, name, value, options, onChange }) {
  return (
    <label className="field">
      <span>{label}</span>
      <select
        value={value}
        onChange={(event) => onChange(name, event.target.value)}
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}

export default App;
