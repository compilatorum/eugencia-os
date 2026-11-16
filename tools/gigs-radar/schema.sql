PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS sources (
 source_id TEXT PRIMARY KEY, name TEXT NOT NULL, source_type TEXT NOT NULL,
 endpoint TEXT, auth_required INTEGER NOT NULL DEFAULT 0, terms_notes TEXT,
 last_checked_at TEXT, status TEXT NOT NULL DEFAULT 'active'
);
CREATE TABLE IF NOT EXISTS opportunities (
 opportunity_id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES sources(source_id),
 external_id TEXT, title TEXT NOT NULL, organization TEXT, opportunity_type TEXT NOT NULL,
 category TEXT, description TEXT, location TEXT, remote_scope TEXT, eligible_regions TEXT,
 compensation_min REAL, compensation_max REAL, compensation_currency TEXT,
 compensation_type TEXT, deadline_text TEXT, deadline_at TEXT, published_at TEXT,
 source_url TEXT NOT NULL, apply_url TEXT, status TEXT NOT NULL, raw_tags TEXT,
 eligibility_gaps TEXT, first_seen_at TEXT NOT NULL, last_seen_at TEXT NOT NULL,
 UNIQUE(source_id, external_id)
);
CREATE TABLE IF NOT EXISTS opportunity_scores (
 opportunity_id TEXT PRIMARY KEY REFERENCES opportunities(opportunity_id) ON DELETE CASCADE,
 technical_fit INTEGER NOT NULL, contract_fit INTEGER NOT NULL, geography_fit INTEGER NOT NULL,
 payment_fit INTEGER NOT NULL, selfware_leverage INTEGER NOT NULL, ergonomics_fit INTEGER NOT NULL,
 confidence INTEGER NOT NULL, score_total REAL NOT NULL, disposition TEXT NOT NULL,
 rationale TEXT NOT NULL, scoring_version TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS funnel_events (
 event_id INTEGER PRIMARY KEY AUTOINCREMENT,
 opportunity_id TEXT NOT NULL REFERENCES opportunities(opportunity_id) ON DELETE CASCADE,
 stage TEXT NOT NULL, event_at TEXT NOT NULL, notes TEXT
);
CREATE TABLE IF NOT EXISTS collection_runs (
 run_id INTEGER PRIMARY KEY AUTOINCREMENT, started_at TEXT NOT NULL, finished_at TEXT,
 source_id TEXT REFERENCES sources(source_id), records_seen INTEGER DEFAULT 0,
 records_inserted INTEGER DEFAULT 0, errors TEXT
);
CREATE TABLE IF NOT EXISTS profile_dimensions (
 dimension TEXT PRIMARY KEY, weight REAL NOT NULL,
 current_evidence TEXT NOT NULL, confidence TEXT NOT NULL
);
CREATE VIEW IF NOT EXISTS v_ranked_opportunities AS
 SELECT o.*, s.technical_fit, s.contract_fit, s.geography_fit, s.payment_fit,
 s.selfware_leverage, s.ergonomics_fit, s.confidence, s.score_total,
 s.disposition, s.rationale
 FROM opportunities o JOIN opportunity_scores s USING(opportunity_id)
 ORDER BY s.score_total DESC;
