import os
from typing import Dict, Any
from coding_trainer_ai.analytics_studio.models import StudentAnalytics, DailyRoutine


class WebStudioServer:
    """
    Generates a single-page Web Studio UI dashboard (HTML/CSS/JS)
    with glassmorphism aesthetic, dark mode, Inter typography, and interactive grade analytics.
    """

    def generate_html_dashboard(
        self, analytics: StudentAnalytics, routine: DailyRoutine
    ) -> str:
        topic_rows = ""
        for tg in analytics.topic_grades:
            badge_icon = "🏆" if tg.grade_label == "Distinction" else ("📜" if tg.grade_label == "Merit" else ("✅" if tg.grade_label == "Pass" else "❌"))
            topic_rows += f"""
            <div class="topic-card">
              <div class="topic-header">
                <span class="topic-title">{badge_icon} {tg.topic_name}</span>
                <span class="topic-badge" style="background: {tg.color_hex}22; color: {tg.color_hex}; border: 1px solid {tg.color_hex}44;">
                  {tg.grade_label} ({tg.score_percentage}%)
                </span>
              </div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {tg.score_percentage}%; background: {tg.color_hex};"></div>
              </div>
            </div>
            """

        routine_cards = ""
        for t in routine.tasks:
            routine_cards += f"""
            <div class="task-card">
              <h3>{t.title}</h3>
              <p>{t.details}</p>
              <div class="task-footer">
                <span class="task-duration">⏱️ {t.duration_minutes} Minutes</span>
                <button class="btn-primary" onclick="alert('Starting {t.title}!')">Launch Session</button>
              </div>
            </div>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Coding Trainer AI - UK MSc Distinction Web Studio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #0f172a;
      --card-bg: rgba(30, 41, 59, 0.7);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent-purple: #8b5cf6;
      --accent-blue: #3b82f6;
      --accent-green: #22c55e;
      --border-color: rgba(255, 255, 255, 0.1);
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Inter', sans-serif;
    }}
    body {{
      background-color: var(--bg-dark);
      color: var(--text-main);
      padding: 2rem;
      min-height: 100vh;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border-color);
      margin-bottom: 2rem;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 1rem;
    }}
    .brand h1 {{
      font-size: 1.8rem;
      font-weight: 800;
      background: linear-gradient(135deg, #a855f7, #3b82f6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .stat-badge {{
      background: rgba(139, 92, 246, 0.2);
      border: 1px solid rgba(139, 92, 246, 0.4);
      color: #c084fc;
      padding: 0.5rem 1rem;
      border-radius: 9999px;
      font-weight: 600;
      font-size: 0.9rem;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
    }}
    .card {{
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: 1rem;
      padding: 1.5rem;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
    }}
    .card h2 {{
      font-size: 1.3rem;
      margin-bottom: 1rem;
      color: var(--text-main);
    }}
    .topic-card {{
      margin-bottom: 1rem;
    }}
    .topic-header {{
      display: flex;
      justify-content: space-between;
      margin-bottom: 0.4rem;
    }}
    .topic-title {{
      font-weight: 600;
      font-size: 0.95rem;
    }}
    .topic-badge {{
      font-size: 0.8rem;
      padding: 0.2rem 0.6rem;
      border-radius: 0.4rem;
      font-weight: 700;
    }}
    .progress-bar-bg {{
      background: rgba(255, 255, 255, 0.08);
      height: 8px;
      border-radius: 4px;
      overflow: hidden;
    }}
    .progress-bar-fill {{
      height: 100%;
      border-radius: 4px;
      transition: width 0.4s ease;
    }}
    .task-card {{
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border-color);
      border-radius: 0.8rem;
      padding: 1rem;
      margin-bottom: 1rem;
    }}
    .task-card h3 {{
      font-size: 1rem;
      margin-bottom: 0.4rem;
      color: #38bdf8;
    }}
    .task-card p {{
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-bottom: 0.8rem;
    }}
    .task-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .task-duration {{
      font-size: 0.8rem;
      color: #a855f7;
      font-weight: 600;
    }}
    .btn-primary {{
      background: linear-gradient(135deg, #8b5cf6, #3b82f6);
      color: white;
      border: none;
      padding: 0.4rem 1rem;
      border-radius: 0.5rem;
      font-weight: 600;
      cursor: pointer;
      font-size: 0.85rem;
    }}
    .btn-primary:hover {{
      opacity: 0.9;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand">
        <h1>🧠 Coding Trainer AI</h1>
        <span class="stat-badge">🎓 UK MSc Studio</span>
      </div>
      <div>
        <span class="stat-badge">Predicted Result: {analytics.predicted_grade}</span>
      </div>
    </header>

    <div class="grid-2">
      <div class="card">
        <h2>📊 UK MSc Predicted Grade Heatmap</h2>
        <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1.5rem;">
          Candidate: <strong>{analytics.user_name}</strong> ({analytics.background})
        </p>
        {topic_rows}
      </div>

      <div class="card">
        <h2>⏱️ Daily 15-Minute Micro-Study Routine</h2>
        <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1.5rem;">
          Date: <strong>{routine.date_str}</strong> | Target: 15 Mins Daily Power Session
        </p>
        {routine_cards}
      </div>
    </div>
  </div>
</body>
</html>
"""
        return html_content

    def export_html_file(
        self, analytics: StudentAnalytics, routine: DailyRoutine, output_path: str
    ) -> str:
        html = self.generate_html_dashboard(analytics, routine)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path
