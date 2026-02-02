#!/usr/bin/env python3
"""
USS Qualifier Dashboard Generator
Creates a modern, interactive web dashboard from JSON test reports.
"""
import json
import sys
from pathlib import Path
from datetime import datetime


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>USS Qualifier Test Results - {test_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            color: #2d3748;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header .meta {{
            color: #718096;
            font-size: 14px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card .label {{
            color: #718096;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .stat-card .value {{
            color: #2d3748;
            font-size: 36px;
            font-weight: bold;
        }}
        
        .stat-card.success .value {{
            color: #48bb78;
        }}
        
        .stat-card.failure .value {{
            color: #f56565;
        }}
        
        .stat-card.skipped .value {{
            color: #ed8936;
        }}
        
        .results-section {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .results-section h2 {{
            color: #2d3748;
            font-size: 24px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e2e8f0;
        }}
        
        .scenario {{
            margin-bottom: 20px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .scenario-header {{
            background: #f7fafc;
            padding: 16px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.2s;
        }}
        
        .scenario-header:hover {{
            background: #edf2f7;
        }}
        
        .scenario-header .title {{
            font-weight: 600;
            color: #2d3748;
            font-size: 16px;
        }}
        
        .scenario-header .badge {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .badge.success {{
            background: #c6f6d5;
            color: #22543d;
        }}
        
        .badge.failure {{
            background: #fed7d7;
            color: #742a2a;
        }}
        
        .badge.skipped {{
            background: #feebc8;
            color: #7c2d12;
        }}
        
        .scenario-body {{
            display: none;
            padding: 20px;
            background: white;
        }}
        
        .scenario.expanded .scenario-body {{
            display: block;
        }}
        
        .test-step {{
            margin-bottom: 16px;
            padding: 12px;
            background: #f7fafc;
            border-radius: 6px;
            border-left: 4px solid #cbd5e0;
        }}
        
        .test-step.passed {{
            border-left-color: #48bb78;
            background: #f0fff4;
        }}
        
        .test-step.failed {{
            border-left-color: #f56565;
            background: #fff5f5;
        }}
        
        .test-step .step-name {{
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 8px;
        }}
        
        .check-item {{
            padding: 8px 12px;
            margin: 4px 0;
            border-radius: 4px;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .check-item.passed {{
            background: #c6f6d5;
            color: #22543d;
        }}
        
        .check-item.failed {{
            background: #fed7d7;
            color: #742a2a;
        }}
        
        .check-item::before {{
            content: '✓';
            font-weight: bold;
        }}
        
        .check-item.failed::before {{
            content: '✗';
        }}
        
        .query-details {{
            margin-top: 12px;
            padding: 12px;
            background: white;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
        }}
        
        .query-details summary {{
            cursor: pointer;
            font-weight: 600;
            color: #4a5568;
            padding: 4px;
        }}
        
        .query-details summary:hover {{
            color: #2d3748;
        }}
        
        .query-info {{
            margin-top: 8px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }}
        
        .query-info .method {{
            display: inline-block;
            padding: 2px 8px;
            background: #4299e1;
            color: white;
            border-radius: 3px;
            font-weight: bold;
            margin-right: 8px;
        }}
        
        .query-info .url {{
            color: #2d3748;
        }}
        
        .query-info .status {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-weight: bold;
            margin-left: 8px;
        }}
        
        .query-info .status.success {{
            background: #c6f6d5;
            color: #22543d;
        }}
        
        .query-info .status.error {{
            background: #fed7d7;
            color: #742a2a;
        }}
        
        pre {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 12px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 12px;
            margin-top: 8px;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            padding: 20px;
            font-size: 14px;
        }}
        
        .expand-all {{
            background: #4299e1;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 20px;
            transition: background 0.2s;
        }}
        
        .expand-all:hover {{
            background: #3182ce;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{test_name}</h1>
            <div class="meta">
                <strong>Suite:</strong> {suite_type}<br>
                <strong>Started:</strong> {start_time}<br>
                <strong>Commit:</strong> {commit_hash}<br>
                <strong>Version:</strong> {codebase_version}
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card success">
                <div class="label">Passed Checks</div>
                <div class="value">{passed_count}</div>
            </div>
            <div class="stat-card failure">
                <div class="label">Failed Checks</div>
                <div class="value">{failed_count}</div>
            </div>
            <div class="stat-card skipped">
                <div class="label">Skipped Actions</div>
                <div class="value">{skipped_count}</div>
            </div>
            <div class="stat-card">
                <div class="label">Total Scenarios</div>
                <div class="value">{scenario_count}</div>
            </div>
        </div>
        
        <div class="results-section">
            <h2>Test Results</h2>
            <button class="expand-all" onclick="toggleAll()">Expand All</button>
            {scenarios_html}
        </div>
        
        <div class="footer">
            Generated by USS Qualifier Dashboard Generator
        </div>
    </div>
    
    <script>
        function toggleScenario(id) {{
            const scenario = document.getElementById(id);
            scenario.classList.toggle('expanded');
        }}
        
        let allExpanded = false;
        function toggleAll() {{
            const scenarios = document.querySelectorAll('.scenario');
            allExpanded = !allExpanded;
            scenarios.forEach(s => {{
                if (allExpanded) {{
                    s.classList.add('expanded');
                }} else {{
                    s.classList.remove('expanded');
                }}
            }});
            document.querySelector('.expand-all').textContent = allExpanded ? 'Collapse All' : 'Expand All';
        }}
    </script>
</body>
</html>
"""


def generate_dashboard(report_path: Path, output_path: Path = None):
    """Generate an interactive HTML dashboard from a JSON report."""
    
    print(f"[INFO] Reading report from: {report_path}")
    
    with open(report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract basic info
    report = data.get('report', {}).get('test_suite', {})
    test_name = report.get('name', 'USS Qualifier Test Results')
    suite_type = report.get('suite_type', 'N/A')
    start_time = report.get('start_time', 'N/A')
    commit_hash = data.get('commit_hash', 'N/A')[:8]
    codebase_version = data.get('codebase_version', 'N/A')
    
    # Calculate statistics
    passed_count = 0
    failed_count = 0
    skipped_count = 0
    scenario_count = 0
    
    scenarios_html = []
    
    for action_idx, action in enumerate(report.get('actions', [])):
        if 'skipped_action' in action:
            skipped_count += 1
            skipped = action['skipped_action']
            scenarios_html.append(f"""
            <div class="scenario" id="scenario-{action_idx}">
                <div class="scenario-header" onclick="toggleScenario('scenario-{action_idx}')">
                    <span class="title">⏭️ Skipped: {skipped.get('reason', 'Unknown reason')[:100]}</span>
                    <span class="badge skipped">Skipped</span>
                </div>
            </div>
            """)
            continue
        
        if 'test_scenario' not in action:
            continue
        
        scenario_count += 1
        scenario = action['test_scenario']
        scenario_name = scenario.get('name', f'Scenario {scenario_count}')
        scenario_successful = scenario.get('successful', True)
        
        # Build scenario HTML
        steps_html = []
        
        for case in scenario.get('cases', []):
            case_name = case.get('name', 'Test Case')
            
            for step in case.get('steps', []):
                step_name = step.get('name', 'Test Step')
                passed_checks = step.get('passed_checks', [])
                failed_checks = step.get('failed_checks', [])
                queries = step.get('queries', [])
                
                passed_count += len(passed_checks)
                failed_count += len(failed_checks)
                
                step_status = 'passed' if not failed_checks else 'failed'
                
                checks_html = []
                for check in passed_checks:
                    checks_html.append(f'<div class="check-item passed">{check.get("name", "Check")}</div>')
                for check in failed_checks:
                    checks_html.append(f'<div class="check-item failed">{check.get("name", "Check")}</div>')
                
                queries_html = []
                for query_idx, query in enumerate(queries):
                    req = query.get('request', {})
                    resp = query.get('response', {})
                    method = req.get('method', 'GET')
                    url = req.get('url', '')
                    status_code = resp.get('code', 0)
                    status_class = 'success' if 200 <= status_code < 300 else 'error'
                    
                    queries_html.append(f"""
                    <details class="query-details">
                        <summary>Query {query_idx + 1}: {query.get('query_type', 'API Call')}</summary>
                        <div class="query-info">
                            <span class="method">{method}</span>
                            <span class="url">{url}</span>
                            <span class="status {status_class}">{status_code}</span>
                        </div>
                    </details>
                    """)
                
                steps_html.append(f"""
                <div class="test-step {step_status}">
                    <div class="step-name">{step_name}</div>
                    {''.join(checks_html)}
                    {''.join(queries_html)}
                </div>
                """)
        
        badge_class = 'success' if scenario_successful else 'failure'
        badge_text = 'Passed' if scenario_successful else 'Failed'
        
        scenarios_html.append(f"""
        <div class="scenario" id="scenario-{action_idx}">
            <div class="scenario-header" onclick="toggleScenario('scenario-{action_idx}')">
                <span class="title">{scenario_name}</span>
                <span class="badge {badge_class}">{badge_text}</span>
            </div>
            <div class="scenario-body">
                {''.join(steps_html)}
            </div>
        </div>
        """)
    
    # Generate final HTML
    html = HTML_TEMPLATE.format(
        test_name=test_name,
        suite_type=suite_type,
        start_time=start_time,
        commit_hash=commit_hash,
        codebase_version=codebase_version,
        passed_count=passed_count,
        failed_count=failed_count,
        skipped_count=skipped_count,
        scenario_count=scenario_count,
        scenarios_html=''.join(scenarios_html)
    )
    
    # Determine output path
    if output_path is None:
        output_path = report_path.parent / 'dashboard.html'
    
    print(f"[INFO] Writing dashboard to: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[SUCCESS] Dashboard generated successfully!")
    print(f"  📊 {passed_count} passed checks")
    print(f"  ❌ {failed_count} failed checks")
    print(f"  ⏭️  {skipped_count} skipped actions")
    print(f"  📝 {scenario_count} test scenarios")
    print(f"\n[INFO] Open the dashboard: {output_path}")
    
    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate-dashboard.py <report.json> [output.html]")
        print("\nExample:")
        print("  python generate-dashboard.py ./output/airwayz_rid_test/report.json")
        print("  python generate-dashboard.py report.json custom-dashboard.html")
        sys.exit(1)
    
    report_path = Path(sys.argv[1])
    
    if not report_path.exists():
        print(f"[ERROR] Report file not found: {report_path}")
        sys.exit(1)
    
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    try:
        dashboard_path = generate_dashboard(report_path, output_path)
        
        # Try to open in browser (Windows)
        try:
            import subprocess
            subprocess.run(['start', str(dashboard_path)], shell=True, check=False)
        except:
            pass
            
    except Exception as e:
        print(f"[ERROR] Failed to generate dashboard: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
