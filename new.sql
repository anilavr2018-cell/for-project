---

```sql
-- DevTrack Database Schema (`new.sql` / `schema.sql`)

-- 1. Developers Table
CREATE TABLE IF NOT EXISTS developers (
    developer_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Projects Table
CREATE TABLE IF NOT EXISTS projects (
    project_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    repo_url VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Daily Summary / Audit Logs
CREATE TABLE IF NOT EXISTS daily_work_audits (
    audit_id SERIAL PRIMARY KEY,
    developer_id INT REFERENCES developers(developer_id) ON DELETE CASCADE,
    project_id INT REFERENCES projects(project_id) ON DELETE CASCADE,
    work_date DATE NOT NULL,
    total_commits INT DEFAULT 0,
    estimated_active_minutes INT DEFAULT 0,
    files_touched_count INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_dev_project_date UNIQUE (developer_id, project_id, work_date)
);

-- 4. Commit History & File Tracking
CREATE TABLE IF NOT EXISTS commit_logs (
    commit_id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(project_id) ON DELETE CASCADE,
    developer_id INT REFERENCES developers(developer_id) ON DELETE CASCADE,
    commit_hash VARCHAR(40) UNIQUE NOT NULL,
    commit_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    commit_message TEXT,
    files_changed TEXT[], -- List of touched file paths
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Work Schedules & Tasks
CREATE TABLE IF NOT EXISTS work_schedules (
    schedule_id SERIAL PRIMARY KEY,
    developer_id INT REFERENCES developers(developer_id) ON DELETE CASCADE,
    project_id INT REFERENCES projects(project_id) ON DELETE CASCADE,
    task_title VARCHAR(200) NOT NULL,
    planned_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'In Progress', 'Completed', 'Deferred')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Task Reminders
CREATE TABLE IF NOT EXISTS task_reminders (
    reminder_id SERIAL PRIMARY KEY,
    schedule_id INT REFERENCES work_schedules(schedule_id) ON DELETE CASCADE,
    reminder_time TIMESTAMP WITH TIME ZONE NOT NULL,
    is_triggered BOOLEAN DEFAULT FALSE,
    message VARCHAR(255) NOT NULL
);

-- Indexes for performance on analytics queries
CREATE INDEX IF NOT EXISTS idx_commit_logs_date ON commit_logs(commit_timestamp);
CREATE INDEX IF NOT EXISTS idx_audits_date ON daily_work_audits(work_date);
CREATE INDEX IF NOT EXISTS idx_schedules_date ON work_schedules(planned_date);