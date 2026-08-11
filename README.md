# DevTrack: Version Control & Developer Productivity Dashboard

**DevTrack** (CLI: `trackit`) is a lightweight developer productivity and version control auditing tool. It integrates local Git repositories with a centralized SQL backend to track commit frequency, active coding hours, modified files, and scheduled tasks.

---

## 🚀 Features

- **Automated Commit Tracking:** Parses local `git log` output to extract commit timestamps and touched files.
- **Active Time Estimation:** Automatically calculates developer focus time based on commit gaps and session duration.
- **File-Level Auditing:** Deep-dive analysis into specific project files over custom date ranges.
- **SQL Analytics Integration:** Store developer performance metrics, work schedules, and task reminders for Power BI or React dashboards.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python 3.9+
- PostgreSQL or MySQL database
- Git installed and configured locally

### 2. Dependencies
Install required Python packages:

```bash
pip install typer rich