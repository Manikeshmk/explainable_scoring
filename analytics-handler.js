/**
 * analytics-handler.js
 * Handles analytics data upload and visualization
 */

const AnalyticsHandler = {
  currentData: null,

  /**
   * Convert email-keyed object format to array format
   * Handles both: [{ student_name, ... }] and { email: { student_name, ... } }
   */
  normalizeData(section_data) {
    if (Array.isArray(section_data)) {
      return section_data; // Already in array format (sample JSON)
    }

    // Convert object format (actual JSON from local_grader.py) to array
    const normalized = [];
    for (const email in section_data) {
      if (typeof section_data[email] === "object") {
        const item = { ...section_data[email] };
        if (!item.email) item.email = email; // Add email if missing
        normalized.push(item);
      }
    }
    return normalized;
  },

  init() {
    const uploadZone = document.getElementById("analytics-upload-zone");
    const fileInput = document.getElementById("analytics-file-input");
    const uploadStatus = document.getElementById("upload-status");

    if (uploadZone && fileInput) {
      uploadZone.addEventListener("click", () => fileInput.click());
      uploadZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        uploadZone.style.background = "rgba(118, 104, 255, 0.1)";
        uploadZone.style.borderColor = "var(--primary)";
      });
      uploadZone.addEventListener("dragleave", () => {
        uploadZone.style.background = "";
        uploadZone.style.borderColor = "var(--border-glass)";
      });
      uploadZone.addEventListener("drop", (e) => {
        e.preventDefault();
        uploadZone.style.background = "";
        uploadZone.style.borderColor = "var(--border-glass)";
        if (e.dataTransfer.files.length > 0) {
          this.handleFileUpload(e.dataTransfer.files[0]);
        }
      });

      fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
          this.handleFileUpload(e.target.files[0]);
        }
      });
    }
  },

  handleFileUpload(file) {
    const uploadStatus = document.getElementById("upload-status");
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        this.currentData = data;
        uploadStatus.textContent = "✅ File loaded successfully!";
        uploadStatus.style.color = "var(--accent1)";
        this.displayAnalytics(data);
      } catch (err) {
        uploadStatus.textContent = "❌ Invalid JSON file: " + err.message;
        uploadStatus.style.color = "var(--danger)";
      }
    };

    reader.onerror = () => {
      uploadStatus.textContent = "❌ Error reading file";
      uploadStatus.style.color = "var(--danger)";
    };

    reader.readAsText(file);
  },

  displayAnalytics(data) {
    const container = document.getElementById("analytics-container");
    if (container) {
      container.classList.remove("hidden");
      window.scrollTo({ top: container.offsetTop - 100, behavior: "smooth" });
    }

    // Clear previous content
    document.getElementById("anomaly-section").innerHTML = "";
    document.getElementById("peer-section").innerHTML = "";
    document.getElementById("concept-section").innerHTML = "";
    document.getElementById("momentum-section").innerHTML = "";
    document.getElementById("curves-section").innerHTML = "";
    document.getElementById("coverage-section").innerHTML = "";

    // Display each section with normalized data
    // Support both naming conventions: semantic_coverage or coverage_metrics
    if (data.anomalies)
      this.renderAnomalies(this.normalizeData(data.anomalies));
    if (data.peer_comparison)
      this.renderPeerComparison(this.normalizeData(data.peer_comparison));
    if (data.concept_mastery)
      this.renderConceptMastery(this.normalizeData(data.concept_mastery));
    if (data.momentum) this.renderMomentum(this.normalizeData(data.momentum));
    if (data.learning_curves)
      this.renderLearningCurves(this.normalizeData(data.learning_curves));

    // Try both names for coverage data
    const coverageData = data.semantic_coverage || data.coverage_metrics;
    if (coverageData && Object.keys(coverageData).length > 0) {
      this.renderCoverage(this.normalizeData(coverageData));
    }
  },

  renderAnomalies(data) {
    const section = document.getElementById("anomaly-section");
    const students = Array.isArray(data) ? data : [data];

    let html = `<h2 style="grid-column: 1/-1; margin-bottom: 1.5rem;">⚠️ Anomaly Detection</h2>`;

    students.forEach((student, idx) => {
      if (!student) return;

      const anomalyCount = student.anomaly_points
        ? student.anomaly_points.length
        : 0;
      const hasAnomalies = student.anomalies_detected || false;
      const anomalyType = student.anomaly_type || "stable";
      const volatility =
        typeof student.volatility === "number" ? student.volatility : 0;

      html += `
                <div class="analytics-card glass-card">
                    <div class="card-header">
                        <h3 class="card-title">🔍 ${student.student_name || `Student ${idx + 1}`}</h3>
                        <span class="card-badge ${hasAnomalies ? "badge-danger" : "badge-success"}">
                            ${hasAnomalies ? "⚠️ Anomaly" : "✅ Normal"}
                        </span>
                    </div>

                    <div class="card-metrics">
                        <div class="metric-box">
                            <span class="metric-label">Pattern</span>
                            <span class="metric-value">${this.formatType(anomalyType)}</span>
                        </div>
                        <div class="metric-box">
                            <span class="metric-label">Anomaly Points</span>
                            <span class="metric-value">${anomalyCount}</span>
                        </div>
                        <div class="metric-box">
                            <span class="metric-label">Volatility</span>
                            <span class="metric-value">${volatility.toFixed(2)}</span>
                        </div>
                    </div>

                    ${
                      anomalyCount > 0
                        ? `
                        <div class="anomaly-list">
                            ${student.anomaly_points
                              .slice(0, 3)
                              .map((point) => {
                                const from =
                                  typeof point.from_score === "number"
                                    ? point.from_score.toFixed(2)
                                    : "N/A";
                                const to =
                                  typeof point.to_score === "number"
                                    ? point.to_score.toFixed(2)
                                    : "N/A";
                                const zscore =
                                  typeof point.z_score === "number"
                                    ? point.z_score.toFixed(1)
                                    : "N/A";
                                return `
                                <div class="anomaly-item ${point.type || "jump_up"}">
                                    <span class="item-label">Submission #${point.position || idx + 1}</span>
                                    <span class="item-change">${from} → ${to}</span>
                                    <span class="item-zscore">z=${zscore}</span>
                                </div>
                            `;
                              })
                              .join("")}
                        </div>
                    `
                        : ""
                    }
                </div>
            `;
    });

    section.innerHTML += html;
  },

  renderPeerComparison(data) {
    const section = document.getElementById("peer-section");
    const students = Array.isArray(data) ? data : [data];

    let html = `<h2 style="grid-column: 1/-1; margin-bottom: 1.5rem;">📊 Peer Comparison</h2>`;

    students.forEach((student, idx) => {
      if (!student) return;

      const scorePercentile =
        typeof student.final_score_percentile === "number"
          ? student.final_score_percentile
          : 50;
      const improvementPercentile =
        typeof student.improvement_percentile === "number"
          ? student.improvement_percentile
          : 50;
      const consistencyPercentile =
        typeof student.consistency_percentile === "number"
          ? student.consistency_percentile
          : 50;
      const finalScore =
        typeof student.final_score === "number"
          ? student.final_score.toFixed(2)
          : "N/A";

      html += `
                <div class="analytics-card glass-card">
                    <div class="card-header">
                        <h3 class="card-title">👤 ${student.student_name || `Student ${idx + 1}`}</h3>
                        <span class="card-badge badge-primary">${finalScore}</span>
                    </div>

                    <div class="percentile-chart">
                        <div class="percentile-row">
                            <label>Final Score</label>
                            <div class="percentile-bar">
                                <div class="percentile-fill" style="width: ${Math.max(0, Math.min(100, scorePercentile))}%"></div>
                            </div>
                            <span>${Math.round(scorePercentile)}th</span>
                        </div>
                        <div class="percentile-row">
                            <label>Improvement</label>
                            <div class="percentile-bar">
                                <div class="percentile-fill" style="width: ${Math.max(0, Math.min(100, improvementPercentile))}%"></div>
                            </div>
                            <span>${Math.round(improvementPercentile)}th</span>
                        </div>
                        <div class="percentile-row">
                            <label>Consistency</label>
                            <div class="percentile-bar">
                                <div class="percentile-fill" style="width: ${Math.max(0, Math.min(100, consistencyPercentile))}%"></div>
                            </div>
                            <span>${Math.round(consistencyPercentile)}th</span>
                        </div>
                    </div>

                    <div class="rank-info">
                        <div class="rank-item ${student.above_average_score ? "positive" : "negative"}">
                            ${student.above_average_score ? "✓ Above Average" : "✗ Below Average"} Score
                        </div>
                    </div>
                </div>
            `;
    });

    section.innerHTML += html;
  },

  renderConceptMastery(data) {
    const section = document.getElementById("concept-section");
    const students = Array.isArray(data) ? data : [data];

    let html = `<h2 style="grid-column: 1/-1; margin-bottom: 1.5rem;">🎯 Concept Mastery Timeline</h2>`;

    students.forEach((student, idx) => {
      if (!student) return;

      const conceptsGained = Array.isArray(student.concepts_gained)
        ? student.concepts_gained
        : [];
      const conceptsLost = Array.isArray(student.concepts_lost)
        ? student.concepts_lost
        : [];
      const stability =
        typeof student.concept_stability === "number"
          ? student.concept_stability * 100
          : 0;

      html += `
                <div class="analytics-card glass-card">
                    <div class="card-header">
                        <h3 class="card-title">📚 ${student.student_name || `Student ${idx + 1}`}</h3>
                        <span class="card-badge badge-accent2">${stability.toFixed(0)}% Stable</span>
                    </div>

                    <div class="concept-grid">
                        <div class="concept-box gained">
                            <span class="concept-label">✓ Gained (${conceptsGained.length})</span>
                            <div class="concept-tags">
                                ${conceptsGained
                                  .slice(0, 3)
                                  .map(
                                    (c) =>
                                      `<span class="tag tag-gained">${c}</span>`,
                                  )
                                  .join("")}
                            </div>
                        </div>
                        <div class="concept-box lost">
                            <span class="concept-label">✗ Lost (${conceptsLost.length})</span>
                            <div class="concept-tags">
                                ${conceptsLost
                                  .slice(0, 3)
                                  .map(
                                    (c) =>
                                      `<span class="tag tag-lost">${c}</span>`,
                                  )
                                  .join("")}
                            </div>
                        </div>
                    </div>
                </div>
            `;
    });

    section.innerHTML += html;
  },

  renderMomentum(data) {
    const section = document.getElementById("momentum-section");
    const students = Array.isArray(data) ? data : [data];

    let html = `<h2 style="grid-column: 1/-1; margin-bottom: 1.5rem;">⚡ Semantic Momentum & Prediction</h2>`;

    students.forEach((student, idx) => {
      if (!student) return;

      const momentum =
        typeof student.momentum === "number" ? student.momentum : 0;
      const nextScore =
        typeof student.predicted_next_score === "number"
          ? student.predicted_next_score.toFixed(2)
          : "N/A";
      const confidence =
        typeof student.prediction_confidence === "number"
          ? (student.prediction_confidence * 100).toFixed(0)
          : "0";
      const direction = momentum > 0.01 ? "📈" : momentum < -0.01 ? "📉" : "➡️";

      html += `
                <div class="analytics-card glass-card">
                    <div class="card-header">
                        <h3 class="card-title">${direction} ${student.student_name || `Student ${idx + 1}`}</h3>
                        <span class="card-badge badge-primary">${momentum > 0 ? "+" : ""}${momentum.toFixed(3)}</span>
                    </div>

                    <div class="momentum-metrics">
                        <div class="metric-box large">
                            <span class="metric-label">Current Momentum</span>
                            <span class="metric-value" style="color: ${momentum > 0 ? "var(--accent1)" : "var(--danger)"}">
                                ${momentum > 0 ? "+" : ""}${momentum.toFixed(3)}
                            </span>
                            <span class="metric-sublabel">per submission</span>
                        </div>
                        <div class="metric-box large">
                            <span class="metric-label">Next Score Prediction</span>
                            <span class="metric-value">${nextScore}</span>
                            <span class="metric-sublabel">${confidence}% confidence</span>
                        </div>
                    </div>

                    ${
                      student.mastery_predicted
                        ? `
                        <div class="mastery-box">
                            <span class="mastery-icon">🎓</span>
                            <span class="mastery-text">Estimated mastery in ${student.submissions_to_mastery || "N/A"} submissions</span>
                        </div>
                    `
                        : ""
                    }
                </div>
            `;
    });

    section.innerHTML += html;
  },

  renderLearningCurves(data) {
    const section = document.getElementById("curves-section");
    const students = Array.isArray(data) ? data : [data];

    let html = `<h2 style="grid-column: 1/-1; margin-bottom: 1.5rem;">📈 Multidimensional Learning Curves</h2>`;

    students.forEach((student, idx) => {
      if (!student) return;

      const canvasId = `learning-curve-${idx}`;
      const submissionCount = student.submission_count || 0;
      const accuracyAvg = student.accuracy_curve?.average || 0;
      const semanticAvg = (student.semantic_drift_curve?.average || 0) * 100;
      const consistencyAvg = (student.consistency_curve?.average || 0) * 100;
      const coverageAvg =
        (student.coverage_curves?.concept_coverage?.average || 0) * 100;

      html += `
                <div class="analytics-card glass-card" style="grid-column: span 2;">
                    <div class="card-header">
                        <h3 class="card-title">📊 ${student.student_name || `Student ${idx + 1}`}</h3>
                        <span class="card-badge badge-accent1">${submissionCount} submissions</span>
                    </div>

                    <div class="curve-metrics">
                        <div class="metric-box">
                            <span class="metric-label">Accuracy</span>
                            <span class="metric-value">${accuracyAvg.toFixed(2)}</span>
                            <span class="metric-trend">${student.accuracy_curve?.trend || "→"}</span>
                        </div>
                        <div class="metric-box">
                            <span class="metric-label">Semantic Alignment</span>
                            <span class="metric-value">${semanticAvg.toFixed(0)}%</span>
                            <span class="metric-trend">${student.semantic_drift_curve?.trend || "→"}</span>
                        </div>
                        <div class="metric-box">
                            <span class="metric-label">Consistency</span>
                            <span class="metric-value">${consistencyAvg.toFixed(0)}%</span>
                            <span class="metric-trend">${student.consistency_curve?.trend || "→"}</span>
                        </div>
                        <div class="metric-box">
                            <span class="metric-label">Coverage</span>
                            <span class="metric-value">${coverageAvg.toFixed(0)}%</span>
                            <span class="metric-trend">${student.coverage_curves?.concept_coverage?.trend || "→"}</span>
                        </div>
                    </div>

                    <canvas id="${canvasId}" class="learning-curve-canvas" width="800" height="300"></canvas>
                </div>
            `;
    });

    section.innerHTML += html;

    // Draw curves after rendering
    students.forEach((student, idx) => {
      if (!student) return;
      const canvasId = `learning-curve-${idx}`;
      const canvas = document.getElementById(canvasId);
      if (
        canvas &&
        AdvancedAnalytics &&
        AdvancedAnalytics.MultiDimensionalVisualizer
      ) {
        AdvancedAnalytics.MultiDimensionalVisualizer.drawLearningCurves(
          canvas,
          student,
        );
      }
    });
  },

  renderCoverage(data) {
    const section = document.getElementById("coverage-section");
    const students = Array.isArray(data) ? data : [data];

    let html = `<h2 style="grid-column: 1/-1; margin-bottom: 1.5rem;">📏 Semantic Coverage Metrics</h2>`;

    students.forEach((student, idx) => {
      if (!student) return;

      const coverage = student.coverage_scores || {};
      const lexical =
        typeof coverage.lexical_coverage === "number"
          ? coverage.lexical_coverage * 100
          : 0;
      const concept =
        typeof coverage.concept_coverage === "number"
          ? coverage.concept_coverage * 100
          : 0;
      const length =
        typeof coverage.length_coverage === "number"
          ? coverage.length_coverage * 100
          : 0;
      const diversity =
        typeof coverage.semantic_diversity === "number"
          ? coverage.semantic_diversity * 100
          : 0;
      const precision =
        typeof coverage.precision === "number" ? coverage.precision * 100 : 0;
      const overall =
        typeof coverage.overall_coverage === "number"
          ? coverage.overall_coverage * 100
          : 0;

      html += `
                <div class="analytics-card glass-card">
                    <div class="card-header">
                        <h3 class="card-title">🎓 ${student.student_name || `Student ${idx + 1}`}</h3>
                        <span class="card-badge badge-accent2">${overall.toFixed(0)}% Overall</span>
                    </div>

                    <div class="coverage-grid">
                        <div class="coverage-item">
                            <span class="coverage-label">Lexical Coverage</span>
                            <div class="coverage-bar">
                                <div class="coverage-fill" style="width: ${Math.max(0, Math.min(100, lexical))}%"></div>
                            </div>
                            <span class="coverage-value">${lexical.toFixed(0)}%</span>
                        </div>
                        <div class="coverage-item">
                            <span class="coverage-label">Concept Coverage</span>
                            <div class="coverage-bar">
                                <div class="coverage-fill" style="width: ${Math.max(0, Math.min(100, concept))}%"></div>
                            </div>
                            <span class="coverage-value">${concept.toFixed(0)}%</span>
                        </div>
                        <div class="coverage-item">
                            <span class="coverage-label">Length Coverage</span>
                            <div class="coverage-bar">
                                <div class="coverage-fill" style="width: ${Math.max(0, Math.min(100, length))}%"></div>
                            </div>
                            <span class="coverage-value">${length.toFixed(0)}%</span>
                        </div>
                        <div class="coverage-item">
                            <span class="coverage-label">Semantic Diversity</span>
                            <div class="coverage-bar">
                                <div class="coverage-fill" style="width: ${Math.max(0, Math.min(100, diversity))}%"></div>
                            </div>
                            <span class="coverage-value">${diversity.toFixed(0)}%</span>
                        </div>
                        <div class="coverage-item">
                            <span class="coverage-label">Precision</span>
                            <div class="coverage-bar">
                                <div class="coverage-fill" style="width: ${Math.max(0, Math.min(100, precision))}%"></div>
                            </div>
                            <span class="coverage-value">${precision.toFixed(0)}%</span>
                        </div>
                    </div>
                </div>
            `;
    });

    section.innerHTML += html;
  },

  formatType(type) {
    const typeMap = {
      jump_up: "📈 Sudden Jump Up",
      jump_down: "📉 Sudden Jump Down",
      oscillating: "〰️ Oscillating",
      stable_improvement: "✨ Steady Growth",
      stable_degradation: "⚠️ Steady Decline",
      gradual: "➡️ Gradual Change",
    };
    return typeMap[type] || type;
  },
};

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
  AnalyticsHandler.init();
});
