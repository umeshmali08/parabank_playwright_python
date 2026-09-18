from pathlib import Path
from html import escape
from datetime import datetime

_RESULTS = []


def pytest_sessionstart(session):
    _RESULTS.clear()


def pytest_runtest_logreport(report):
    if report.when == "call" or (report.failed and report.when in {"setup", "teardown"}):
        _RESULTS.append({
            "name": report.nodeid,
            "status": report.outcome,
            "duration": round(report.duration, 3),
            "error": str(report.longrepr) if report.failed else "",
        })


def pytest_sessionfinish(session, exitstatus):
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    passed = sum(1 for r in _RESULTS if r["status"] == "passed")
    failed = sum(1 for r in _RESULTS if r["status"] == "failed")
    skipped = sum(1 for r in _RESULTS if r["status"] == "skipped")
    total = len(_RESULTS)
    duration = round(sum(r["duration"] for r in _RESULTS), 2)

    cards = "".join(
        f"""
        <div class="test-card">
          <div>
            <div class="test-name">{escape(r['name'])}</div>
            <div class="duration">{r['duration']}s</div>
          </div>
          <span class="status {r['status']}">{r['status'].upper()}</span>
          {f'<pre>{escape(r["error"])}</pre>' if r["error"] else ''}
        </div>
        """
        for r in _RESULTS
    )

    html = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>ParaBank Automation Report</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    min-height: 100vh;
    font-family: Arial, sans-serif;
    color: #fff;
    background: radial-gradient(circle at top left, #4a2b1b, #111 50%, #1c1c1c);
    padding: 36px;
  }}
  h1 {{ color: #F48031; margin-bottom: 4px; }}
  .subtitle {{ opacity: .7; margin-bottom: 28px; }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }}
  .glass, .test-card {{
    background: rgba(255,255,255,.09);
    border: 1px solid rgba(255,255,255,.18);
    box-shadow: 0 8px 32px rgba(0,0,0,.25);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-radius: 16px;
  }}
  .glass {{ padding: 18px; }}
  .metric {{ font-size: 30px; font-weight: 700; margin-top: 5px; }}
  .accent, .passed {{ color: #F48031; }}
  .failed {{ color: #ff6464; }}
  .skipped {{ color: #d5d5d5; }}
  .test-card {{
    padding: 16px;
    margin: 12px 0;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 12px;
  }}
  .test-name {{ font-weight: 700; }}
  .duration {{ opacity: .7; margin-top: 5px; }}
  .status {{ font-weight: 800; }}
  pre {{
    grid-column: 1 / -1;
    white-space: pre-wrap;
    background: rgba(0,0,0,.25);
    padding: 12px;
    border-radius: 10px;
    overflow: auto;
  }}
</style>
</head>
<body>
  <h1>ParaBank Automation Dashboard</h1>
  <div class="subtitle">Generated {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
  <div class="grid">
    <div class="glass"><div>Total</div><div class="metric">{total}</div></div>
    <div class="glass"><div>Passed</div><div class="metric accent">{passed}</div></div>
    <div class="glass"><div>Failed</div><div class="metric">{failed}</div></div>
    <div class="glass"><div>Skipped</div><div class="metric">{skipped}</div></div>
    <div class="glass"><div>Duration</div><div class="metric">{duration}s</div></div>
  </div>
  <h2>Test Results</h2>
  {cards or '<div class="glass">No test results captured.</div>'}
</body>
</html>"""
    (report_dir / "index.html").write_text(html, encoding="utf-8")
