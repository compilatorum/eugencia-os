# Eugência — Web3 + AI Gigs Radar

SQLite schema and collector for discovering, comparing and qualifying Web3/AI gigs, bounties, contracts and relevant roles against the Eugência profile.

## Files
- schema.sql — normalized SQLite schema, source registry, scoring, funnel history and ranked view.
- collector.py — Python 3 collector using only the standard library.
- The initial SQLite snapshot (2026-11-16) is attached to the ChatGPT conversation as a downloadable artifact; it contains four opportunities, source registry, profile weights and funnel history.

## Quick start
1. Create an empty database: `python3 collector.py --db eugencia_crypto_ai_gigs.sqlite --init-only`
2. Collect fresh listings: `python3 collector.py --db eugencia_crypto_ai_gigs.sqlite`
3. Query the ranking: `sqlite3 eugencia_crypto_ai_gigs.sqlite "SELECT title, organization, opportunity_type, score_total, disposition FROM v_ranked_opportunities;"`

## Optional credentials
- WEB3CAREER_API_TOKEN — required for Web3.career API. Keep private; never commit it.
- SUPERTEAM_EARN_API_KEY — required for the official Superteam Earn agent-eligible listings endpoint. The collector never registers an agent or submits work.

Remote OK, Himalayas and Remotive are fetched without credentials. Provider attribution and rate-limit notes are documented in the sources table.

## Scoring model — profile-v1
`S(o) = 0.25T + 0.20C + 0.15G + 0.15P + 0.15R + 0.10E`
- T: technical fit (AI agents, MCP, APIs, Postgres, RAG, testing/harness, Web3/data).
- C: contract/gig fit (bounty/project/contract preferred; full-time secondary).
- G: geography and remote eligibility (Brazil-compatible; restricted countries penalized).
- P: payment clarity and collectability (explicit reward, escrow, milestones).
- R: reusable selfware leverage (adapter, tests, template, benchmark, documentation).
- E: ergonomics (async, bounded scope, low WIP, autonomy).

Scores are heuristics, not probabilities of winning or hiring. Seed scores are evidence-weighted; fresh collector scores are marked `heuristic-v0.1` and must be manually verified.

## Funnel
`DISCOVER → VERIFY → QUALIFY → SCOPE → PROPOSE → CONTRACT → DELIVER → ACCEPT → INVOICE → LEARN`

Do not move an opportunity from DISCOVER to QUALIFY until the individual listing, eligibility, deadline, deliverables, acceptance criteria, payer and payout terms are checked. Keep commercial WIP at two or fewer.

## Snapshot notes (2026-11-16)
- Two Superteam Earn opportunities appeared on the Backend Bounties category page. Individual listing URLs and full terms were not captured; they are marked for verification, not ready-to-apply.
- Remote OK's Supabase AI Tooling listing is a full-time global-remote role, not a gig. It is retained as a comparator because it overlaps MCP, agents, evals, TypeScript and Postgres. Its 5+ years software-engineering requirement and compensation need verification.
- Himalayas' Lead AI Engineer listing was explicitly US-only and required 8+ years software engineering plus 2+ years production GenAI; it is excluded from the active funnel.

## Sources and usage constraints
- Remote OK: https://remoteok.com/api — attribute Remote OK and link original listings.
- Himalayas: https://himalayas.app/jobs/api — cursor pagination preferred.
- Remotive: https://remotive.com/api/remote-jobs — attribute/link Remotive; recommended maximum four fetches per day.
- Web3.career: https://web3.career/api/v1 — token required; follow-link attribution; do not alter apply_url.
- Superteam Earn: https://superteam.fun/api/agents/listings/live — authenticated agent endpoint; no agent registration or submission is performed.

The database is for personal research, not a public job-board mirror. Re-check every opportunity on its original site before applying.
