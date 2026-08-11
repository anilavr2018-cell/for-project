-- new.sql
-- TrackIt CLI - Database Schema for Git Commit Audit Tracking

-- 1. Commits Table
CREATE TABLE IF NOT EXISTS commits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    commit_hash VARCHAR(40) UNIQUE NOT NULL,
    author_name VARCHAR(255),
    commit_message TEXT,
    committed_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tracked Files Table
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path VARCHAR(500) UNIQUE NOT NULL
);

-- 3. Junction Table: Links commits to the files touched
CREATE TABLE IF NOT EXISTS commit_files (
    commit_id INTEGER NOT NULL,
    file_id INTEGER NOT NULL,
    PRIMARY KEY (commit_id, file_id),
    FOREIGN KEY (commit_id) REFERENCES commits(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
);

-- 4. Daily Work Audits Table (Caches the calculated summary metrics)
CREATE TABLE IF NOT EXISTS daily_audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_date DATE UNIQUE NOT NULL,
    total_commits INTEGER DEFAULT 0,
    est_active_minutes INTEGER DEFAULT 0,
    files_touched_count INTEGER DEFAULT 0,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for optimal lookup speeds on CLI searches
CREATE INDEX IF NOT EXISTS idx_commits_committed_at ON commits(committed_at);
CREATE INDEX IF NOT EXISTS idx_files_path ON files(file_path);
CREATE INDEX IF NOT EXISTS idx_audits_date ON daily_audits(audit_date);

-- View: Quick Daily Work Summary matching the CLI output
CREATE VIEW IF NOT EXISTS v_daily_summary AS
SELECT 
    DATE(c.committed_at) AS work_date,
    COUNT(DISTINCT c.id) AS total_commits,
    COUNT(DISTINCT cf.file_id) AS total_files_touched
FROM commits c
LEFT JOIN commit_files cf ON c.id = cf.commit_id
GROUP BY DATE(c.committed_at);