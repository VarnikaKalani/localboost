// App.js
import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async (e) => {
    e.preventDefault();
    setError(null);
    if (!file) {
      setError("Please select a CSV file.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("http://127.0.0.1:5001/api/analyze", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Upload failed");
      }
      const data = await res.json();
      setAnalysisData(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>LocalBoost Analysis</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleUpload}>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button type="submit">Upload and Analyze</button>
      </form>

      {analysisData && (
        <div style={{ marginTop: 30 }}>
          <h2>Forecast Data</h2>
          <ul>
            {analysisData.forecast.map((f, idx) => (
              <li key={idx}>
                {f.date}: {f.value}
              </li>
            ))}
          </ul>
          <h2>Plots</h2>
          <div>
            <h3>Seasonal Decomposition</h3>
            <img
              src={`http://127.0.0.1:5001/${analysisData.seasonal_decomp_path}`}
              alt="Seasonal Decomposition"
              style={{ width: "80%", marginBottom: 20 }}
            />
          </div>
          <div>
            <h3>Forecast Plot</h3>
            <img
              src={`http://127.0.0.1:5001/${analysisData.forecast_plot_path}`}
              alt="Forecast Plot"
              style={{ width: "80%", marginBottom: 20 }}
            />
          </div>
          <div>
            <h3>Residuals Over Time</h3>
            <img
              src={`http://127.0.0.1:5001/${analysisData.residuals_time_path}`}
              alt="Residuals Over Time"
              style={{ width: "80%", marginBottom: 20 }}
            />
          </div>
          <div>
            <h3>Residual Distribution</h3>
            <img
              src={`http://127.0.0.1:5001/${analysisData.residuals_hist_path}`}
              alt="Residual Distribution"
              style={{ width: "80%", marginBottom: 20 }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
