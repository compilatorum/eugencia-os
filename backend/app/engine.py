"""
Core Engine for Eugência OS & ValueCurator OS (7 Layers + Career/Venture Modules).
Uses SQLite (PostgreSQL-compatible schema) and implements all mathematical formulas
and deterministic policies specified in ~/eugencia.pdf.
"""
from __future__ import annotations
import hashlib
import json
import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "eugencia_os.db"
ASSETS_JSON_PATH = DATA_DIR / "portfolio_assets.json"
DOCS_DIR = BASE_DIR / "docs" / "eugencia-os"

# Model catalog for Layer 3: AI Gateway
# M* = argmin_{m in M} [C(m) + lambda * L(m) + mu * R(m)] subject to Q(m) >= Q_min
AI_MODELS_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "gemini-2.5-flash-lite",
        "name": "Gemini Flash-Lite (Fast/Economy)",
        "provider": "Google",
        "cost_norm": 0.12,        # C(m)
        "latency_norm": 0.10,     # L(m)
        "risk_norm": 0.28,        # R(m)
        "quality": 0.74,          # Q(m)
        "credit_weight": 0.25,    # omega_model
        "cost_per_1k_brl": 0.004,
        "avg_latency_ms": 280,
    },
    {
        "id": "gemini-2.5-flash",
        "name": "Gemini Flash (Balanced Commercial)",
        "provider": "Google",
        "cost_norm": 0.30,
        "latency_norm": 0.22,
        "risk_norm": 0.16,
        "quality": 0.86,
        "credit_weight": 1.00,
        "cost_per_1k_brl": 0.015,
        "avg_latency_ms": 520,
    },
    {
        "id": "claude-sonnet-4",
        "name": "Claude Sonnet (Agentic Engineering & Code)",
        "provider": "Anthropic",
        "cost_norm": 0.58,
        "latency_norm": 0.40,
        "risk_norm": 0.10,
        "quality": 0.93,
        "credit_weight": 2.00,
        "cost_per_1k_brl": 0.045,
        "avg_latency_ms": 950,
    },
    {
        "id": "gemini-2.5-pro-deep",
        "name": "Gemini Pro / Reasoning (High-Assurance & ProofGate)",
        "provider": "Google",
        "cost_norm": 0.75,
        "latency_norm": 0.55,
        "risk_norm": 0.06,
        "quality": 0.97,
        "credit_weight": 3.50,
        "cost_per_1k_brl": 0.075,
        "avg_latency_ms": 1450,
    },
]

TOOL_CREDIT_COSTS: Dict[str, float] = {
    "catalog_sql": 0.10,
    "whatsapp_api": 0.20,
    "mercadopago_pix": 0.25,
    "github_mcp": 0.15,
    "farcaster_neynar": 0.20,
    "solana_pyth_oracle": 0.50,
    "jupiter_quote": 0.50,
}

AUTONOMY_LEVELS = ["L0", "L1", "L2", "L3", "L4"]
AUTONOMY_REQUIREMENTS: Dict[str, Dict[str, Any]] = {
    "L0": {"name": "Manual", "operation": "Humano executa", "min_tests": 0, "min_evidences": 0, "requires_controls": False},
    "L1": {"name": "Assisted", "operation": "IA recomenda; humano executa", "min_tests": 1, "min_evidences": 1, "requires_controls": False},
    "L2": {"name": "Supervised", "operation": "IA executa com aprovação humana (APPROVAL_ONLY)", "min_tests": 5, "min_evidences": 2, "requires_controls": True},
    "L3": {"name": "Guarded", "operation": "IA executa dentro de limites determinísticos do ProofGate", "min_tests": 15, "min_evidences": 3, "requires_controls": True},
    "L4": {"name": "Autonomous", "operation": "Execução autônoma contínua com monitoramento SCADA", "min_tests": 50, "min_evidences": 5, "requires_controls": True},
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def compute_sha256(payload: Any) -> str:
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


class EugenciaEngine:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self._seed_if_empty()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS organizations (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    plan_tier TEXT NOT NULL,
                    credits_quota INTEGER NOT NULL,
                    credits_used INTEGER NOT NULL DEFAULT 0,
                    mrr_brl REAL NOT NULL DEFAULT 0.0,
                    setup_paid_brl REAL NOT NULL DEFAULT 0.0,
                    variable_cost_brl REAL NOT NULL DEFAULT 0.0,
                    human_hours_month REAL NOT NULL DEFAULT 1.0,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    org_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    role TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS workspaces (
                    id TEXT PRIMARY KEY,
                    org_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    cockpit_mode TEXT NOT NULL DEFAULT 'hybrid'
                );

                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    code TEXT NOT NULL,
                    name TEXT NOT NULL,
                    cluster TEXT NOT NULL,
                    commercial_unit TEXT NOT NULL,
                    delivery_model TEXT NOT NULL,
                    setup_min_brl REAL NOT NULL,
                    setup_max_brl REAL NOT NULL,
                    mrr_min_brl REAL NOT NULL,
                    mrr_max_brl REAL NOT NULL,
                    wip_active INTEGER NOT NULL DEFAULT 0,
                    priority TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS agents (
                    id TEXT PRIMARY KEY,
                    role_code TEXT NOT NULL,
                    name TEXT NOT NULL,
                    icon TEXT NOT NULL,
                    responsibility TEXT NOT NULL,
                    autonomy_level TEXT NOT NULL,
                    default_model TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS workflows (
                    id TEXT PRIMARY KEY,
                    product_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    steps_json TEXT NOT NULL,
                    autonomy_level TEXT NOT NULL,
                    tests_passed INTEGER NOT NULL DEFAULT 0,
                    evidences_count INTEGER NOT NULL DEFAULT 0,
                    controls_verified INTEGER NOT NULL DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS executions (
                    id TEXT PRIMARY KEY,
                    org_id TEXT NOT NULL,
                    workflow_id TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    model_used TEXT NOT NULL,
                    tokens_in INTEGER NOT NULL,
                    tokens_out INTEGER NOT NULL,
                    credits_consumed INTEGER NOT NULL,
                    cost_brl REAL NOT NULL,
                    latency_ms INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS usages (
                    id TEXT PRIMARY KEY,
                    org_id TEXT NOT NULL,
                    execution_id TEXT NOT NULL,
                    credits_delta INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS subscriptions (
                    id TEXT PRIMARY KEY,
                    org_id TEXT NOT NULL,
                    product_id TEXT NOT NULL,
                    plan_tier TEXT NOT NULL,
                    mrr_brl REAL NOT NULL,
                    status TEXT NOT NULL,
                    payment_stage TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS invoices (
                    id TEXT PRIMARY KEY,
                    org_id TEXT NOT NULL,
                    invoice_type TEXT NOT NULL,
                    amount_brl REAL NOT NULL,
                    currency TEXT NOT NULL,
                    gateway TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS evidences (
                    id TEXT PRIMARY KEY,
                    experiment_id TEXT NOT NULL,
                    project_name TEXT NOT NULL,
                    work_package TEXT NOT NULL,
                    title TEXT NOT NULL,
                    artifact_uri TEXT NOT NULL,
                    sha256_hash TEXT NOT NULL,
                    verified INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS proofgate_receipts (
                    id TEXT PRIMARY KEY,
                    org_id TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    agent_role TEXT NOT NULL,
                    action TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    policy_status TEXT NOT NULL,
                    validation_reasons_json TEXT NOT NULL,
                    requires_human INTEGER NOT NULL,
                    approval_status TEXT NOT NULL,
                    approved_by TEXT,
                    execution_status TEXT NOT NULL,
                    receipt_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS flow_inbox (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    source TEXT NOT NULL,
                    space TEXT NOT NULL,
                    classified_type TEXT NOT NULL,
                    suggested_cluster TEXT NOT NULL,
                    suggested_destination TEXT NOT NULL,
                    assigned_agent TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS opportunities (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    channel_type TEXT NOT NULL,
                    cluster TEXT NOT NULL,
                    reward_brl REAL NOT NULL,
                    probability REAL NOT NULL,
                    prep_hours REAL NOT NULL,
                    expected_value_brl REAL NOT NULL,
                    ev_per_hour_brl REAL NOT NULL,
                    deadline TEXT NOT NULL,
                    funding_category TEXT NOT NULL,
                    status TEXT NOT NULL,
                    github_issue_url TEXT
                );

                CREATE TABLE IF NOT EXISTS grant_work_packages (
                    id TEXT PRIMARY KEY,
                    project_name TEXT NOT NULL,
                    wp_code TEXT NOT NULL,
                    deliverable TEXT NOT NULL,
                    funding_category TEXT NOT NULL,
                    license TEXT NOT NULL,
                    target_funder TEXT NOT NULL,
                    amount_brl REAL NOT NULL,
                    status TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS experiments (
                    id TEXT PRIMARY KEY,
                    code TEXT NOT NULL,
                    title TEXT NOT NULL,
                    research_axis TEXT NOT NULL,
                    hypothesis TEXT NOT NULL,
                    status TEXT NOT NULL,
                    autonomy_score REAL NOT NULL,
                    value_delivered_score REAL NOT NULL,
                    effort_score REAL NOT NULL,
                    friction_score REAL NOT NULL,
                    overload_score REAL NOT NULL,
                    ergonomics_index REAL NOT NULL,
                    artifacts_delta_a TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS catalog_items (
                    sku TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price_brl REAL NOT NULL,
                    stock INTEGER NOT NULL,
                    max_auto_discount_pct REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS domain_events (
                    id TEXT PRIMARY KEY,
                    org_id TEXT NOT NULL,
                    bounded_context TEXT NOT NULL,
                    event_stage TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    version INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS crm_pipeline_deals (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    client_or_dao TEXT NOT NULL,
                    source_channel TEXT NOT NULL,
                    sprint_code TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    score_s REAL NOT NULL,
                    passes_risk_gate INTEGER NOT NULL DEFAULT 1,
                    passes_verified_budget_gate INTEGER NOT NULL DEFAULT 1,
                    price_brl REAL NOT NULL,
                    currency TEXT NOT NULL,
                    reusable_delta_s TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )

    def _seed_if_empty(self) -> None:
        with self._connect() as conn:
            cur = conn.execute("SELECT COUNT(*) AS cnt FROM organizations")
            if cur.fetchone()["cnt"] > 0:
                return

            ts = now_iso()

            # 1. Organizations (Multi-tenant core)
            orgs = [
                ("org:compilatorum", "Compilatorum Holding & Lab", "compilatorum", "Business", 10000, 1420, 0.0, 0.0, 120.0, 12.0, ts),
                ("org:valuecurator", "ValueCurator Institucional", "valuecurator", "Business", 10000, 850, 0.0, 0.0, 95.0, 8.0, ts),
                ("org:vespa-tcg", "Vespa TCG (Belo Horizonte)", "vespa-tcg", "Starter", 500, 185, 650.0, 2000.0, 95.0, 3.5, ts),
                ("org:collector-bh", "Arena Colecionáveis Piloto", "arena-colecionaveis", "Professional", 2000, 410, 950.0, 3000.0, 140.0, 4.0, ts),
                ("org:solana-dao-pilot", "Solana Treasury Guard DAO", "solana-dao-pilot", "Business", 10000, 1120, 1500.0, 5000.0, 210.0, 5.0, ts),
            ]
            conn.executemany(
                "INSERT INTO organizations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", orgs
            )

            # 2. Users & Workspaces
            conn.executemany(
                "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                [
                    ("usr:sukata", "org:compilatorum", "João Nitzsche (Architect & Sovereign)", "sukata@compilatorum.org", "owner"),
                    ("usr:vespa-ops", "org:vespa-tcg", "Operador Comercial Vespa TCG", "contato@vespatcg.com.br", "client_admin"),
                    ("usr:dao-multisig", "org:solana-dao-pilot", "Treasury Multisig Signer", "ops@solanadao.org", "client_admin"),
                ],
            )
            conn.executemany(
                "INSERT INTO workspaces VALUES (?, ?, ?, ?)",
                [
                    ("ws:eugencia-cockpit", "org:compilatorum", "Eugência OS Hybrid Cockpit (Emacs + Web)", "hybrid"),
                    ("ws:vespa-commerce", "org:vespa-tcg", "Vespa TCG WhatsApp Commerce", "web"),
                    ("ws:dao-proofgate", "org:solana-dao-pilot", "ProofGate Assurance Console", "web"),
                ],
            )

            # 3. Productized Services Catalog (Section 5.1 & 6.2)
            products = [
                ("prd:ai-commerce", "PRD-01", "AI Commerce Agent (Card-Chat)", "ValueCurator", "Commerce", "Setup + Mensalidade + Créditos", 1500.0, 6000.0, 400.0, 1500.0, 1, "P1"),
                ("prd:proofgate", "PRD-02", "ProofGate / AI Agent Assurance", "ValueCurator", "Agent Assurance", "Licenciamento + API + Piloto", 5000.0, 15000.0, 1200.0, 4500.0, 1, "P1"),
                ("prd:grant-intel", "PRD-03", "Grant Intelligence (GrantOS)", "GrantOS", "Intelligence", "Assinatura + Setup", 500.0, 1500.0, 150.0, 500.0, 0, "P1"),
                ("prd:ai-knowledge", "PRD-04", "AI Knowledge Agent", "NeuroCoder", "Agent Engineering", "Setup + Mensalidade", 2000.0, 5000.0, 500.0, 1200.0, 0, "P2"),
                ("prd:ai-workflow", "PRD-05", "AI Workflow Agent", "NeuroCoder", "Agent Engineering", "Setup + Mensalidade", 2500.0, 6000.0, 600.0, 1500.0, 0, "P2"),
                ("prd:data-intel", "PRD-06", "Data Intelligence (Lakehouse)", "ValueCurator", "Data Intelligence", "Setup + Mensalidade", 3000.0, 8000.0, 800.0, 2000.0, 0, "P2"),
            ]
            conn.executemany(
                "INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", products
            )

            # 4. The 7 Human-AI Team Agents (Part 2, Section 2)
            agents = [
                ("agt:chief-of-staff", "CHIEF_OF_STAFF", "Chief of Staff IA", "🧭", "Prioridades, agenda, controle WIP <= 2, capacidade e coordenação Flow <-> Execução", "L2", "gemini-2.5-flash"),
                ("agt:research", "RESEARCH", "Research IA", "🔬", "Literatura, tendências, hipóteses e apoio ao Research & Experiment OS", "L3", "gemini-2.5-pro-deep"),
                ("agt:bizdev", "BIZDEV", "Business Development IA", "💼", "Clientes B2B, triagem de bounties (Superteam/Dework), grants e propostas", "L2", "gemini-2.5-flash"),
                ("agt:engineering", "ENGINEERING", "Engineering IA", "🛠️", "Repositórios, código, Harness Engineering (+131 testes) e deploy isolado", "L3", "claude-sonnet-4"),
                ("agt:portfolio", "PORTFOLIO", "Portfolio Analyst IA", "📊", "Ativos (72 repos), cálculo de L, rho, MC, riscos e alocação de esforço", "L3", "gemini-2.5-flash"),
                ("agt:comms", "COMMS", "Communications IA", "📣", "Posts Farcaster, changelogs, radar semanal e relatórios baseados em evidências", "L2", "gemini-2.5-flash"),
                ("agt:proofgate-qa", "PROOFGATE_QA", "QA / ProofGate IA", "🧪", "Políticas determinísticas, testes adversariais, validação e recibos criptográficos", "L3", "gemini-2.5-pro-deep"),
            ]
            conn.executemany(
                "INSERT INTO agents VALUES (?, ?, ?, ?, ?, ?, ?)", agents
            )

            # 5. Workflows with L0-L4 Progressive Autonomy (Section 10.3)
            workflows = [
                (
                    "wf:commerce-order",
                    "prd:ai-commerce",
                    "Card-Chat: Fluxo Comercial WhatsApp -> Checkout",
                    "card-chat",
                    json.dumps(["WhatsApp Inbound", "AI Gateway Route", "Catalog Lookup", "Recommendation", "ProofGate Discount Check", "MercadoPago PIX", "Human Handoff"]),
                    "L3",
                    24,
                    4,
                    1,
                ),
                (
                    "wf:proofgate-mandate",
                    "prd:proofgate",
                    "ProofGate: Validação de Intenção e Mandato (APPROVAL_ONLY)",
                    "finance",
                    json.dumps(["Intent Capture", "Policy Evaluation", "Pyth/Jupiter Read-Only Check", "Human Approval Gate", "Execution", "SHA-256 Receipt"]),
                    "L2",
                    131,
                    5,
                    1,
                ),
                (
                    "wf:grantos-pipeline",
                    "prd:grant-intel",
                    "GrantOS: Descoberta, Decomposição WP e Submissão",
                    "grantos",
                    json.dumps(["Project Mapping", "Funding Thesis", "Opportunity Match", "WorkPackage Split", "Anti-Double-Dip Check", "Submission Approval"]),
                    "L2",
                    12,
                    3,
                    1,
                ),
                (
                    "wf:farcaster-radar",
                    "prd:grant-intel",
                    "Reputation OS: Radar Semanal & Build in Public Verificável",
                    "farcaster",
                    json.dumps(["GitHub/Org Activity Capture", "AI Synthesis", "Evidence Hash Verification", "Human Editorial Approval", "Farcaster Cast & Changelog"]),
                    "L2",
                    8,
                    3,
                    1,
                ),
                (
                    "wf:harness-ci",
                    "prd:ai-workflow",
                    "Harness Engineering: Execução DAG em Worktree Isolada",
                    "neurocoder",
                    json.dumps(["Worktree Isolation", "DAG Task Plan", "Agent Implementation", "Clean-Room Test Suite", "ProofGate Merge Guard"]),
                    "L3",
                    131,
                    4,
                    1,
                ),
            ]
            conn.executemany(
                "INSERT INTO workflows VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", workflows
            )

            # 6. Subscriptions & Invoices
            conn.executemany(
                "INSERT INTO subscriptions VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    ("sub:vespa-01", "org:vespa-tcg", "prd:ai-commerce", "Starter", 650.0, "active", "Stage 1: MercadoPago PIX/Recorrência"),
                    ("sub:arena-02", "org:collector-bh", "prd:ai-commerce", "Professional", 950.0, "active", "Stage 1: MercadoPago PIX/Recorrência"),
                    ("sub:dao-03", "org:solana-dao-pilot", "prd:proofgate", "Business", 1500.0, "active", "Stage 2: USDC Solana Treasury"),
                ],
            )
            conn.executemany(
                "INSERT INTO invoices VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    ("inv:001", "org:vespa-tcg", "setup", 2000.0, "BRL", "MercadoPago", "paid", ts),
                    ("inv:002", "org:vespa-tcg", "subscription", 650.0, "BRL", "MercadoPago", "paid", ts),
                    ("inv:003", "org:collector-bh", "setup", 3000.0, "BRL", "MercadoPago", "paid", ts),
                    ("inv:004", "org:collector-bh", "subscription", 950.0, "BRL", "MercadoPago", "paid", ts),
                    ("inv:005", "org:solana-dao-pilot", "licensing_pilot", 5000.0, "USDC", "Solana USDC Wallet", "paid", ts),
                    ("inv:006", "org:solana-dao-pilot", "subscription", 1500.0, "USDC", "Solana USDC Wallet", "paid", ts),
                ],
            )

            # 7. Verifiable Evidences
            evidences = [
                ("EV-001", "E-001", "Eugência OS", "WP0-PORTFOLIO", "Auditoria e classificação A–F dos 72 repositórios GitHub (59 compilatorum + 13 smp-sandramariapereira)", "docs/eugencia-os/PORTFOLIO-ASSETS-REGISTER.md", compute_sha256("EV-001:72-repos-classified"), 1, ts),
                ("EV-002", "E-001", "ValueCurator OS", "WP1-VOS-CORE", "Implementação das 7 camadas VOS: Identity, Billing/Créditos, AI Gateway M*, Agents, Memory, Tools, ProofGate", "backend/app/engine.py", compute_sha256("EV-002:vos-7-layers"), 1, ts),
                ("EV-003", "E-002", "Card-Chat", "WP2-COMMERCE", "Fluxo comercial AI Commerce Agent (Vespa TCG) com guardrail determinístico de desconto e estoque", "docs/eugencia-os/PRODUCT-CATALOG.md", compute_sha256("EV-003:card-chat-vespa-tcg"), 1, ts),
                ("EV-004", "E-003", "ProofGate", "WP3-PROOFGATE", "Pipeline Intent -> Policy -> Validation -> Approval -> Execution -> Receipt em modo APPROVAL_ONLY", "docs/eugencia-os/VALUECURATOR-OS-SPEC.md", compute_sha256("EV-004:proofgate-approval-only"), 1, ts),
            ]
            conn.executemany(
                "INSERT INTO evidences VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", evidences
            )

            # 8. Seed Initial ProofGate Receipts
            sample_payload_1 = {"sku": "TCG-PKM-151-BOX", "qty": 2, "discount_pct": 8.0, "verified_catalog": True}
            r1_hash = compute_sha256({"domain": "card-chat", "action": "apply_discount", "payload": sample_payload_1, "status": "PASSED"})
            sample_payload_2 = {"sku": "TCG-MTG-LOTR-COLLECTOR", "qty": 1, "discount_pct": 22.0, "verified_catalog": True}
            r2_hash = compute_sha256({"domain": "card-chat", "action": "apply_discount", "payload": sample_payload_2, "status": "REQUIRES_APPROVAL"})
            sample_payload_3 = {"protocol": "Jupiter/Solana", "pair": "SOL/USDC", "amount_usd": 2500, "mode": "APPROVAL_ONLY", "fiduciary_buffer": 1.35, "health_factor": 1.82}
            r3_hash = compute_sha256({"domain": "finance", "action": "execute_mandate_swap", "payload": sample_payload_3, "status": "REQUIRES_APPROVAL"})

            conn.executemany(
                "INSERT INTO proofgate_receipts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    ("rcp:001", "org:vespa-tcg", "card-chat", "Engineering IA", "apply_discount", json.dumps(sample_payload_1), "PASSED", json.dumps(["Desconto de 8.0% dentro do limite automático de 10.0%", "Estoque confirmado no catálogo confiável"]), 0, "AUTO_APPROVED", "ProofGate Policy Engine (L3)", "EXECUTED", r1_hash, ts),
                    ("rcp:002", "org:vespa-tcg", "card-chat", "Business Development IA", "apply_discount", json.dumps(sample_payload_2), "HOLD_FOR_HUMAN", json.dumps(["Desconto de 22.0% excede limite automático de 10.0% (máx supervisionado: 25.0%)", "Exige aprovação humana antes de gerar link MercadoPago"]), 1, "PENDING_HUMAN", None, "HELD", r2_hash, ts),
                    ("rcp:003", "org:solana-dao-pilot", "finance", "QA / ProofGate IA", "execute_mandate_swap", json.dumps(sample_payload_3), "HOLD_FOR_HUMAN", json.dumps(["Modo APPROVAL_ONLY ativo no ValueCurator", "Buffer fiduciário (1.35 >= 1.20) e Health Factor (1.82 >= 1.50) verificados via Pyth Oracle"]), 1, "APPROVED", "sukata (Human Authority)", "EXECUTED", r3_hash, ts),
                ],
            )

            # 9. Flow Inbox (Module A: Divergence <-> Convergence)
            inbox_items = [
                ("flw:001", "Integrar webhook de confirmação automática do PIX MercadoPago no Card-Chat da Vespa TCG", "cockpit", "Convergence (Linha de Execução)", "Tarefa de Produto (P1)", "ValueCurator", "Fase 2 — Card-Chat MVP", "Engineering IA", "in_execution", ts),
                ("flw:002", "Hipótese: Usar grafos de folksonomia do Farcaster para ranquear automaticamente elegibilidade de editais no GrantOS", "emacs-org", "Divergence (Laboratório de Exploração)", "Hipótese de Pesquisa", "GrantOS", "Research & Experiment OS (E-003)", "Research IA", "curated", ts),
                ("flw:003", "Oportunidade Superteam Earn: Solana AI Agent Security & Guardrails SDK Bounty", "github", "Convergence (Linha de Execução)", "Oportunidade de Capital", "ValueCurator", "Opportunity Intelligence CRM", "Business Development IA", "promoted_to_opportunity", ts),
                ("flw:004", "Extrair runner de testes isolados em worktrees do harness-engineering como template padrão de microsserviço", "emacs-org", "Convergence (Linha de Execução)", "Melhoria de Selfware (Delta A_t > 0)", "NeuroCoder", "Fase 1 — Fábrica Interna", "Engineering IA", "in_execution", ts),
                ("flw:005", "Explorar acoplamento entre PROTEROL e biofeedback vocal no AROS sem obrigação de monetização imediata", "cockpit", "Divergence (Laboratório de Exploração)", "Ideia / Insight Criativo", "AROS", "Laboratório de Exploração (P3 Estacionado)", "Research IA", "parked_flow", ts),
            ]
            conn.executemany(
                "INSERT INTO flow_inbox VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", inbox_items
            )

            # 10. Opportunity Intelligence CRM (Module B)
            opps = [
                ("opp:001", "Vespa TCG — Implantação AI Commerce Agent (WhatsApp + Catálogo + PIX)", "B2B Direct", "Customer", "ValueCurator", 6200.0, 0.80, 12.0, 4960.0, 413.33, "2026-11-30", "COMMERCIAL_PRODUCT", "active_pilot", "https://github.com/smp-sandramariapereira/card-chat/issues/1"),
                ("opp:002", "Superteam Earn — Solana Agent Guardrails & Verifiable Policy SDK", "Superteam Earn", "Grant", "ValueCurator", 25000.0, 0.45, 20.0, 11250.0, 562.50, "2026-12-10", "OPEN_PUBLIC_GOODS", "qualified", "https://github.com/compilatorum/value-curator/issues/1"),
                ("opp:003", "Security Grant — Adversarial Testing Benchmark for Autonomous DeFi Agents", "Superteam Earn", "Grant", "ValueCurator", 18000.0, 0.40, 16.0, 7200.0, 450.00, "2026-12-20", "RESEARCH_AND_VALIDATION", "qualified", "https://github.com/compilatorum/harness-engineering/issues/1"),
                ("opp:004", "Gitcoin Grants — Farcaster Commons Lab & Verifiable Contributions (IPIT)", "Gitcoin Grants", "Grant", "GrantOS", 12000.0, 0.50, 14.0, 6000.0, 428.57, "2026-12-18", "OPEN_PUBLIC_GOODS", "preparing", "https://github.com/compilatorum/concurseiro-grants/issues/1"),
                ("opp:005", "Dework/GitHub Sync — Implementação de Adaptador Pyth Price Feed em Rust/TS", "Dework/GitHub", "Bounty", "ValueCurator", 4500.0, 0.60, 8.0, 2700.0, 337.50, "2026-11-28", "SHARED_INFRASTRUCTURE", "qualified", "https://github.com/compilatorum/value-curator/issues/2"),
                ("opp:006", "Piloto B2B Agent Assurance — DAO Treasury Policy Engine (APPROVAL_ONLY)", "B2B Direct", "Licensing", "ValueCurator", 15000.0, 0.55, 18.0, 8250.0, 458.33, "2026-12-15", "COMMERCIAL_PRODUCT", "active_pilot", "https://github.com/compilatorum/vc/issues/1"),
            ]
            conn.executemany(
                "INSERT INTO opportunities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", opps
            )

            # 11. Grant Stacking Work Packages (Section 7.4 — ProofGate WP1..WP5)
            wps = [
                ("wp:proofgate-1", "ProofGate / ValueCurator", "WP1", "SDK TypeScript aberto de especificação de intents e políticas", "OPEN_PUBLIC_GOODS", "MIT", "Developer Tooling Grant (Superteam)", 15000.0, "ready_for_grant"),
                ("wp:proofgate-2", "ProofGate / ValueCurator", "WP2", "Suíte aberta de testes adversariais para agentes autônomos", "RESEARCH_AND_VALIDATION", "Apache-2.0", "Security Grant", 18000.0, "in_progress"),
                ("wp:proofgate-3", "ProofGate / ValueCurator", "WP3", "Adaptadores on-chain Solana (Anchor + Pyth + Jupiter Read-Only)", "SHARED_INFRASTRUCTURE", "Apache-2.0", "Solana Ecosystem Grant", 20000.0, "ready_for_grant"),
                ("wp:proofgate-4", "ProofGate / ValueCurator", "WP4", "API Hospedada Comercial Multi-Tenant com AI Gateway", "COMMERCIAL_PRODUCT", "Proprietária (ValueCurator)", "Clientes B2B (Assinatura + Créditos)", 18000.0, "active_commercial"),
                ("wp:proofgate-5", "ProofGate / ValueCurator", "WP5", "Dashboard Proprietário de Auditoria e Aprovação HITL", "COMMERCIAL_PRODUCT", "Proprietária (ValueCurator)", "Receita Comercial & Licenciamento", 12000.0, "active_commercial"),
            ]
            conn.executemany(
                "INSERT INTO grant_work_packages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", wps
            )

            # 12. Research & Experiments (Module C — Section 11)
            exps = [
                (
                    "exp:e001",
                    "E-001",
                    "Eugência OS como Infraestrutura de Transição Profissional",
                    "Eixo 1 & 2: Cognição Aumentada, Flow e Orquestração Humano-IA",
                    "Um sistema híbrido (Emacs/Org + Web App Cytoscape.js) de captura, curadoria, execução supervisionada e publicação reduz o atrito entre exploração criativa e entregas verificáveis mantendo WIP <= 2.",
                    "ACTIVE",
                    0.82,
                    9.2,
                    1.5,
                    0.8,
                    0.6,
                    round((9.2 * 0.82) / (1.5 + 0.8 + 0.6), 2),
                    "Repositório ~/eugencia-os + 72 ativos auditados + 9 docs estratégicos + sync Org-mode",
                ),
                (
                    "exp:e002",
                    "E-002",
                    "Card-Chat como AI Commerce Agent Verificável (Vespa TCG)",
                    "Eixo 4: Service-as-a-Software e Productized Services",
                    "Operador comercial automatizado via WhatsApp com catálogo determinístico e ProofGate de desconto elimina alucinações comerciais e gera MRR imediato.",
                    "ACTIVE",
                    0.78,
                    8.8,
                    1.6,
                    0.9,
                    0.5,
                    round((8.8 * 0.78) / (1.6 + 0.9 + 0.5), 2),
                    "Conector WhatsApp/MercadoPago + Policy Engine Comercial + Template Service-as-a-Software",
                ),
                (
                    "exp:e003",
                    "E-003",
                    "ProofGate-as-a-Service & Grant Stacking Web3",
                    "Eixo 3 & 5: Harness Engineering, ProofGate e Financiamento Descentralizado",
                    "Decompor o ProofGate em WP1-WP3 abertos (financiados por Grants) e WP4-WP5 proprietários (financiados por clientes B2B) maximiza capital intelectual sem dupla cobrança.",
                    "DESIGNED",
                    0.85,
                    9.5,
                    1.8,
                    0.7,
                    0.5,
                    round((9.5 * 0.85) / (1.8 + 0.7 + 0.5), 2),
                    "SDK TypeScript ProofGate + Benchmark Adversarial + Matriz Grant Stacking",
                ),
            ]
            conn.executemany(
                "INSERT INTO experiments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", exps
            )

            # 13. Catalog Items for Card-Chat (Vespa TCG)
            catalog = [
                ("TCG-PKM-151-BOX", "Booster Box Pokémon Scarlet & Violet 151 (PT-BR)", "Pokémon TCG", 420.00, 14, 10.0),
                ("TCG-MTG-LOTR-COLLECTOR", "Magic: The Gathering — Tales of Middle-earth Collector Booster Box", "Magic TCG", 1890.00, 4, 10.0),
                ("TCG-YGO-RA02-BOX", "Yu-Gi-Oh! 25th Anniversary Rarity Collection II Booster Box", "Yu-Gi-Oh! TCG", 540.00, 9, 10.0),
                ("TCG-OP-OP05-BOX", "One Piece Card Game — Awakening of the New Era [OP-05] Box", "One Piece TCG", 690.00, 6, 8.0),
                ("ACC-DRAGON-SHIELD-MATTE", "Sleeves Dragon Shield Matte Dual Black (100 un.)", "Acessórios", 89.90, 38, 12.0),
            ]
            conn.executemany(
                "INSERT INTO catalog_items VALUES (?, ?, ?, ?, ?, ?)", catalog
            )

            # 14. Seed 9-Stage CRM Pipeline Deals (Discover -> Qualify -> Scope -> Propose -> Contract -> Deliver -> Accept -> Invoice -> Learn)
            crm_deals = [
                ("crm:001", "Vespa TCG — Operador WhatsApp + Catálogo + PIX", "Vespa TCG BH", "B2B Direct", "SPR-03", "Deliver", 86.5, 1, 1, 2650.0, "BRL_PIX", "Conector WhatsApp/MercadoPago + Guardrail Desconto ProofGate", ts),
                ("crm:002", "Solana Agent Policy Guardrail & Ed25519 Receipt SDK", "Superteam / Solana Ecosystem", "Superteam Earn", "SPR-07", "Propose", 84.0, 1, 1, 9000.0, "USDC", "SDK TypeScript Open Core (WP1) + Verificador SHA-256/Ed25519", ts),
                ("crm:003", "DAO Proposal Triage Copilot (L0-L4)", "Governaut DAO Ops", "Dework", "SPR-08", "Scope", 79.5, 1, 1, 5200.0, "USDC", "Template de Triagem Multi-Agente L0-L4 + Simulador de Risco", ts),
                ("crm:004", "Adversarial Prompt-Injection Benchmark Suite", "DeFi Treasury Guard", "Superteam Earn", "SPR-06", "Qualify", 77.0, 1, 1, 4500.0, "USDC", "Dataset de 50 ataques adversariais + Runner isolado em worktree", ts),
            ]
            conn.executemany(
                "INSERT INTO crm_pipeline_deals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", crm_deals
            )

    # -------------------------------------------------------------------------
    # Portfolio & Assets (72 GitHub Repos + SCADA Graph + KPIs)
    # -------------------------------------------------------------------------
    def get_portfolio_assets(
        self,
        cluster: Optional[str] = None,
        asset_class: Optional[str] = None,
        owner: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        with open(ASSETS_JSON_PATH, "r", encoding="utf-8") as f:
            assets: List[Dict[str, Any]] = json.load(f)
        if cluster:
            assets = [a for a in assets if a["cluster"].lower() == cluster.lower()]
        if asset_class:
            assets = [a for a in assets if asset_class.lower() in a["asset_class"].lower()]
        if owner:
            assets = [a for a in assets if a["owner"].lower() == owner.lower()]
        if priority:
            assets = [a for a in assets if a["priority"].lower() == priority.lower()]
        return assets

    def get_kpis(self) -> Dict[str, Any]:
        assets = self.get_portfolio_assets()
        wip_products = [a for a in assets if a["wip_active"]]

        with self._connect() as conn:
            orgs = [dict(r) for r in conn.execute("SELECT * FROM organizations").fetchall()]
            subs = [dict(r) for r in conn.execute("SELECT * FROM subscriptions WHERE status = 'active'").fetchall()]
            invs = [dict(r) for r in conn.execute("SELECT * FROM invoices WHERE status = 'paid'").fetchall()]
            opps = [dict(r) for r in conn.execute("SELECT * FROM opportunities").fetchall()]
            wfs = [dict(r) for r in conn.execute("SELECT * FROM workflows").fetchall()]
            exps = [dict(r) for r in conn.execute("SELECT * FROM experiments").fetchall()]
            evids = [dict(r) for r in conn.execute("SELECT * FROM evidences").fetchall()]
            rcps = [dict(r) for r in conn.execute("SELECT * FROM proofgate_receipts").fetchall()]

        mrr_brl = sum(s["mrr_brl"] for s in subs)
        setup_and_pilot_brl = sum(i["amount_brl"] for i in invs if i["invoice_type"] in ("setup", "licensing_pilot"))
        total_revenue_brl = mrr_brl + setup_and_pilot_brl

        variable_costs_brl = sum(o["variable_cost_brl"] for o in orgs)
        human_hours_total = sum(o["human_hours_month"] for o in orgs)
        paying_clients = len(subs)

        # Contribution Margin: MC = R - C_IA - C_infra - C_pagamentos - C_suporte
        c_ia = round(variable_costs_brl * 0.42, 2)
        c_infra = round(variable_costs_brl * 0.23, 2)
        c_pagamentos = round(mrr_brl * 0.032, 2)
        c_suporte = round(variable_costs_brl * 0.35, 2)
        total_var_cost = round(c_ia + c_infra + c_pagamentos + c_suporte, 2)
        contribution_margin_brl = round(mrr_brl - total_var_cost, 2)
        contribution_margin_pct = round((contribution_margin_brl / mrr_brl) * 100, 1) if mrr_brl > 0 else 0.0

        # L = Receita recorrente / Horas humanas operacionais
        leverage_l = round(mrr_brl / max(human_hours_total, 1.0), 2)
        # Alavancagem da Eugência = Valor entregue externamente / Horas de intervenção humana
        external_value_brl = total_revenue_brl + sum(o["expected_value_brl"] for o in opps if o["status"] in ("active_pilot", "qualified"))
        eugencia_leverage = round(external_value_brl / max(human_hours_total, 1.0), 2)
        # rho = Receita recorrente / Custos variáveis
        rho_efficiency = round(mrr_brl / max(total_var_cost, 1.0), 2)

        # Ergonomia media dos experimentos ativos
        avg_ergonomics = round(sum(e["ergonomics_index"] for e in exps) / max(len(exps), 1), 2)

        # Formula da Eugencia E = H + S + A + G (scores normalizados 0..25 => 0..100)
        h_score = 24.0
        s_score = min(25.0, round(len([a for a in assets if a["stage"] == "Construct"]) * 1.4, 1))
        a_score = 22.5
        g_score = 24.0
        e_index = round(h_score + s_score + a_score + g_score, 1)

        return {
            "eugencia_formula": {
                "E_total_score": e_index,
                "H_human_capital": h_score,
                "S_selfware_ip": s_score,
                "A_agent_runtime": a_score,
                "G_governance_proofgate": g_score,
            },
            "commercial": {
                "mrr_brl": mrr_brl,
                "paying_clients": paying_clients,
                "total_billed_brl": total_revenue_brl,
                "mrr_stage_current": "Estágio 1 — Validação (Meta: R$ 1.500 -> Atual: R$ 3.100 MRR c/ Pilotos)",
                "mrr_stages_targets": [
                    {"stage": "Validação", "clients": 3, "avg_ticket": 500, "target_mrr": 1500},
                    {"stage": "Tração", "clients": 10, "avg_ticket": 800, "target_mrr": 8000},
                    {"stage": "Expansão", "clients": 25, "avg_ticket": 1000, "target_mrr": 25000},
                ],
            },
            "financial": {
                "contribution_margin_brl": contribution_margin_brl,
                "contribution_margin_pct": contribution_margin_pct,
                "variable_costs_breakdown": {
                    "C_IA": c_ia,
                    "C_infra": c_infra,
                    "C_pagamentos": c_pagamentos,
                    "C_suporte": c_suporte,
                    "total_variable_brl": total_var_cost,
                },
                "recurring_over_total_ratio": round(mrr_brl / max(total_revenue_brl, 1.0), 2),
                "rho_computational_efficiency": rho_efficiency,
            },
            "operational": {
                "human_hours_total": human_hours_total,
                "human_hours_per_client": round(human_hours_total / max(paying_clients, 1), 2),
                "L_mrr_per_human_hour": leverage_l,
                "eugencia_leverage_ratio": eugencia_leverage,
                "ergonomics_index": avg_ergonomics,
                "wip_comercial_count": len(wip_products),
                "wip_comercial_limit": 2,
                "wip_compliant": len(wip_products) <= 2,
                "wip_active_repos": [p["name"] for p in wip_products],
            },
            "engineering_and_governance": {
                "total_repositories": len(assets),
                "compilatorum_repos": sum(1 for a in assets if a["owner"] == "compilatorum"),
                "shared_sandra_repos": sum(1 for a in assets if a["owner"] == "smp-sandramariapereira"),
                "tests_passing_total": sum(w["tests_passed"] for w in wfs),
                "verified_evidences": len(evids),
                "proofgate_receipts_count": len(rcps),
            },
            "grants_and_capital": {
                "qualified_opportunities": len(opps),
                "pipeline_expected_value_brl": round(sum(o["expected_value_brl"] for o in opps), 2),
            },
        }

    def get_scada_graph(self, include_archived: bool = False) -> Dict[str, Any]:
        """
        Builds the Cytoscape.js SCADA graph for Software Industry 5.0 (Section 10.1):
        Holding -> Clusters -> Repositories / WorkPackages -> Products -> Clients -> Revenue
        """
        assets = self.get_portfolio_assets()
        nodes: List[Dict[str, Any]] = []
        edges: List[Dict[str, Any]] = []

        # Root Holding Node
        nodes.append({
            "data": {
                "id": "holding:valuecurator-compilatorum",
                "label": "VALUECURATOR / COMPILATORUM\n(Eugência Holding)",
                "type": "holding",
                "cluster": "Core",
                "priority": "P0",
            }
        })

        # 6 Economic Clusters
        clusters = ["ValueCurator", "NeuroCoder", "GrantOS", "Capital Intelligence", "GeoIA", "AROS"]
        for cl in clusters:
            cid = f"cluster:{cl}"
            nodes.append({
                "data": {
                    "id": cid,
                    "label": f"Cluster: {cl}",
                    "type": "cluster",
                    "cluster": cl,
                    "priority": "P1" if cl in ("ValueCurator", "NeuroCoder", "GrantOS") else "P3",
                }
            })
            edges.append({
                "data": {
                    "id": f"edge:holding->{cid}",
                    "source": "holding:valuecurator-compilatorum",
                    "target": cid,
                    "relation": "governs",
                }
            })

        # Repositories
        included_repo_ids = set()
        for a in assets:
            if not include_archived and a["stage"] == "Archive":
                continue
            rid = f"repo:{a['name']}"
            included_repo_ids.add(a["name"])
            nodes.append({
                "data": {
                    "id": rid,
                    "label": a["name"],
                    "full_name": a["full_name"],
                    "owner": a["owner"],
                    "type": "repository",
                    "cluster": a["cluster"],
                    "stage": a["stage"],
                    "asset_class": a["asset_class"],
                    "priority": a["priority"],
                    "wip_active": a["wip_active"],
                    "autonomy": a["autonomy_level"],
                    "monetization": a["monetization"],
                    "next_milestone": a["next_milestone"],
                }
            })
            edges.append({
                "data": {
                    "id": f"edge:cluster:{a['cluster']}->{rid}",
                    "source": f"cluster:{a['cluster']}",
                    "target": rid,
                    "relation": "contains",
                }
            })

        # Dependencies between active repositories
        for a in assets:
            if a["name"] not in included_repo_ids:
                continue
            for dep in a["dependencies"]:
                if dep in included_repo_ids:
                    edges.append({
                        "data": {
                            "id": f"edge:dep:{dep}->{a['name']}",
                            "source": f"repo:{dep}",
                            "target": f"repo:{a['name']}",
                            "relation": "powers",
                        }
                    })

        # Products, Clients & Revenue Chain: Codigo -> Produto -> Cliente -> Receita
        with self._connect() as conn:
            products = [dict(r) for r in conn.execute("SELECT * FROM products WHERE priority IN ('P0', 'P1', 'P2')").fetchall()]
            subs = [dict(r) for r in conn.execute("SELECT * FROM subscriptions").fetchall()]
            orgs = {r["id"]: dict(r) for r in conn.execute("SELECT * FROM organizations").fetchall()}

        product_repo_links = {
            "prd:ai-commerce": ["card-chat", "valuecurator", "harness-engineering"],
            "prd:proofgate": ["value-curator", "vc", "KAIROS-Engine", "oracle"],
            "prd:grant-intel": ["concurseiro-grants", "governaut-os", "farcaster-nexus"],
            "prd:ai-knowledge": ["promptcraft", "lakehouse"],
            "prd:ai-workflow": ["omni-dual-brain", "neurocoder-pwa"],
            "prd:data-intel": ["lakehouse", "oracle"],
        }

        for p in products:
            pid = p["id"]
            nodes.append({
                "data": {
                    "id": pid,
                    "label": p["name"],
                    "type": "product",
                    "cluster": p["cluster"],
                    "priority": p["priority"],
                    "wip_active": bool(p["wip_active"]),
                    "delivery_model": p["delivery_model"],
                }
            })
            for rname in product_repo_links.get(pid, []):
                if rname in included_repo_ids:
                    edges.append({
                        "data": {
                            "id": f"edge:repo:{rname}->{pid}",
                            "source": f"repo:{rname}",
                            "target": pid,
                            "relation": "productizes",
                        }
                    })

        for s in subs:
            org = orgs.get(s["org_id"])
            if not org:
                continue
            cid = s["org_id"]
            if not any(n["data"]["id"] == cid for n in nodes):
                nodes.append({
                    "data": {
                        "id": cid,
                        "label": f"{org['name']}\n(MRR: R$ {s['mrr_brl']:.0f})",
                        "type": "client",
                        "cluster": "Commercial",
                        "priority": "P1",
                    }
                })
            edges.append({
                "data": {
                    "id": f"edge:{s['product_id']}->{cid}",
                    "source": s["product_id"],
                    "target": cid,
                    "relation": "serves",
                }
            })

        return {"nodes": nodes, "edges": edges, "total_assets": len(assets)}

    # -------------------------------------------------------------------------
    # Layer 3: AI Gateway Routing & Execution
    # M* = argmin_{m in M} [C(m) + lambda * L(m) + mu * R(m)] s.t. Q(m) >= Q_min
    # -------------------------------------------------------------------------
    def route_and_execute_ai(
        self,
        task_type: str,
        prompt_preview: str,
        min_quality: float,
        lambda_latency: float,
        mu_risk: float,
        tokens_in: int,
        tokens_out: int,
        tools_invoked: List[str],
        org_id: str,
    ) -> Dict[str, Any]:
        eligible_models = [m for m in AI_MODELS_CATALOG if m["quality"] >= min_quality]
        if not eligible_models:
            # Fallback to highest quality model if min_quality is above all
            eligible_models = [max(AI_MODELS_CATALOG, key=lambda x: x["quality"])]

        scored_models = []
        for m in AI_MODELS_CATALOG:
            is_eligible = m["quality"] >= min_quality
            objective_score = round(
                m["cost_norm"] + (lambda_latency * m["latency_norm"]) + (mu_risk * m["risk_norm"]),
                4,
            )
            scored_models.append({
                **m,
                "eligible": is_eligible,
                "objective_score": objective_score,
            })

        scored_eligible = [m for m in scored_models if m["eligible"]]
        selected = min(scored_eligible, key=lambda x: x["objective_score"])

        # Calculate normalized commercial credits:
        # Credits(s) = ceil( ((T_in + 2*T_out)/1000)*omega_model + sum(gamma_tools) + delta_proofgate )
        token_component = ((tokens_in + 2.0 * tokens_out) / 1000.0) * selected["credit_weight"]
        tools_component = sum(TOOL_CREDIT_COSTS.get(t, 0.15) for t in tools_invoked)
        proofgate_component = 0.25
        credits_consumed = max(1, math.ceil(token_component + tools_component + proofgate_component))

        cost_brl = round(((tokens_in + tokens_out) / 1000.0) * selected["cost_per_1k_brl"], 4)
        exec_id = f"exec:{compute_sha256({'t': now_iso(), 'p': prompt_preview, 'm': selected['id']})[:10]}"
        ts = now_iso()

        with self._connect() as conn:
            org_row = conn.execute("SELECT * FROM organizations WHERE id = ?", (org_id,)).fetchone()
            if not org_row:
                org_id = "org:compilatorum"
                org_row = conn.execute("SELECT * FROM organizations WHERE id = ?", (org_id,)).fetchone()

            new_used = org_row["credits_used"] + credits_consumed
            quota_exceeded = new_used > org_row["credits_quota"]
            status = "COMPLETED_WITH_OVERAGE_BILLING" if quota_exceeded else "COMPLETED"

            conn.execute(
                "UPDATE organizations SET credits_used = ?, variable_cost_brl = ROUND(variable_cost_brl + ?, 4) WHERE id = ?",
                (new_used, cost_brl, org_id),
            )
            conn.execute(
                "INSERT INTO executions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (exec_id, org_id, "wf:commerce-order", task_type, selected["id"], tokens_in, tokens_out, credits_consumed, cost_brl, selected["avg_latency_ms"], status, ts),
            )
            conn.execute(
                "INSERT INTO usages VALUES (?, ?, ?, ?, ?, ?)",
                (f"usg:{exec_id[5:]}", org_id, exec_id, credits_consumed, f"AI Gateway [{task_type}] via {selected['id']}", ts),
            )

        return {
            "execution_id": exec_id,
            "formula": "M* = argmin_{m in M} [C(m) + lambda*L(m) + mu*R(m)] subject to Q(m) >= Q_min",
            "selected_model": selected,
            "all_candidates": scored_models,
            "billing": {
                "org_id": org_id,
                "credits_consumed": credits_consumed,
                "credits_used_total": new_used,
                "credits_quota": org_row["credits_quota"],
                "estimated_cost_brl": cost_brl,
                "status": status,
            },
        }

    # -------------------------------------------------------------------------
    # Layer 7: ProofGate Engine (Intent -> Policy -> Validation -> Approval -> Execution -> Receipt)
    # -------------------------------------------------------------------------
    def evaluate_proofgate_intent(
        self,
        domain: str,
        agent_role: str,
        action: str,
        payload: Dict[str, Any],
        org_id: str = "org:valuecurator",
        auto_approve_if_supervised: bool = False,
    ) -> Dict[str, Any]:
        reasons: List[str] = []
        policy_status = "PASSED"
        requires_human = False

        domain_norm = domain.lower().strip()

        if domain_norm == "card-chat":
            discount = float(payload.get("discount_pct", 0.0))
            verified_catalog = bool(payload.get("verified_catalog", True))
            stock_available = int(payload.get("stock_available", 1))
            quantity = int(payload.get("quantity", 1))

            if not verified_catalog:
                policy_status = "BLOCKED"
                reasons.append("VIOLAÇÃO CRÍTICA: Preço ou SKU não provém de fonte confiável do catálogo (alucinação bloqueada).")
            if stock_available < quantity:
                policy_status = "BLOCKED"
                reasons.append(f"VIOLAÇÃO DE ESTOQUE: Quantidade solicitada ({quantity}) excede estoque real ({stock_available}).")
            if discount > 25.0:
                policy_status = "BLOCKED"
                reasons.append(f"VIOLAÇÃO DE ALÇADA: Desconto de {discount}% excede o teto absoluto permitido (25.0%).")
            elif discount > 10.0 and policy_status != "BLOCKED":
                policy_status = "HOLD_FOR_HUMAN"
                requires_human = True
                reasons.append(f"SUPERVISÃO EXIGIDA: Desconto de {discount}% ultrapassa o limite autônomo do agente (10.0%). Requer aprovação humana.")
            elif policy_status == "PASSED":
                reasons.append(f"Política comercial Card-Chat atendida: desconto ({discount}% <= 10%) e estoque ({stock_available} >= {quantity}) verificados.")

        elif domain_norm == "grantos":
            has_docs = bool(payload.get("has_mandatory_docs", True))
            duplicate_funding = bool(payload.get("duplicate_funding_for_same_wp", False))
            proprietary_as_public = bool(payload.get("proprietary_claimed_as_public_good", False))

            if duplicate_funding:
                policy_status = "BLOCKED"
                reasons.append("VIOLAÇÃO ÉTICA/GRANTOS: Proibido financiar duas vezes o mesmo Work Package (dupla cobrança bloqueada).")
            if proprietary_as_public:
                policy_status = "BLOCKED"
                reasons.append("VIOLAÇÃO DE LICENÇA: Código proprietário fechado não pode ser submetido como Open Public Good.")
            if not has_docs and policy_status != "BLOCKED":
                policy_status = "HOLD_FOR_HUMAN"
                requires_human = True
                reasons.append("Documentação obrigatória de edital ou evidência GitHub incompleta; retido para revisão.")
            if policy_status == "PASSED":
                requires_human = True
                policy_status = "HOLD_FOR_HUMAN"
                reasons.append("Critérios de Grant Stacking verificados; submissão final exige assinatura humana (APPROVAL_ONLY).")

        elif domain_norm == "finance":
            fiduciary_buffer = float(payload.get("fiduciary_buffer", 1.30))
            health_factor = float(payload.get("health_factor", 1.75))
            within_mandate = bool(payload.get("within_mandate", True))

            if not within_mandate:
                policy_status = "BLOCKED"
                reasons.append("VIOLAÇÃO DE MANDATO: Operação fora dos parâmetros de ativo/risco do mandato ValueCurator.")
            if fiduciary_buffer < 1.20:
                policy_status = "BLOCKED"
                reasons.append(f"RESTRIÇÃO SOBERANA: Buffer fiduciário ({fiduciary_buffer:.2f}x) abaixo do mínimo termodinâmico de 1.20x.")
            if health_factor < 1.50:
                policy_status = "BLOCKED"
                reasons.append(f"PROTEÇÃO DE LIQUIDAÇÃO: Health Factor DeFi ({health_factor:.2f}) abaixo do limite seguro de 1.50.")
            if policy_status != "BLOCKED":
                policy_status = "HOLD_FOR_HUMAN"
                requires_human = True
                reasons.append(f"Mandato e oráculos validados (Buffer={fiduciary_buffer:.2f}x, Hf={health_factor:.2f}). Modo APPROVAL_ONLY exige assinatura humana.")

        elif domain_norm == "neurocoder":
            destructive = bool(payload.get("destructive_action", False))
            tests_passed = bool(payload.get("tests_passed", True))
            if destructive and not auto_approve_if_supervised:
                policy_status = "HOLD_FOR_HUMAN"
                requires_human = True
                reasons.append("Operação potencialmente destrutiva em repositório/infraestrutura retida para aprovação humana.")
            elif not tests_passed:
                policy_status = "BLOCKED"
                reasons.append("BLOQUEIO HARNESS: Suíte de testes automatizados falhou em ambiente isolado.")
            else:
                reasons.append("Testes em worktree isolada aprovados e sem mutação destrutiva.")

        elif domain_norm == "farcaster":
            evidence_id = payload.get("evidence_id")
            if not evidence_id:
                policy_status = "BLOCKED"
                reasons.append("BLOQUEIO REPUTATION OS: Proibido publicar atualização pública sem ID de evidência verificável (nada de inventar progresso).")
            else:
                policy_status = "HOLD_FOR_HUMAN"
                requires_human = True
                reasons.append(f"Publicação vinculada à evidência {evidence_id}; aguardando aprovação editorial humana.")
        else:
            reasons.append("Política geral padrão aplicada.")

        if policy_status == "BLOCKED":
            approval_status = "REJECTED_BY_POLICY"
            approved_by = "ProofGate Deterministic Guard"
            execution_status = "BLOCKED"
        elif requires_human and not auto_approve_if_supervised:
            approval_status = "PENDING_HUMAN"
            approved_by = None
            execution_status = "HELD"
        else:
            approval_status = "APPROVED" if auto_approve_if_supervised else "AUTO_APPROVED"
            approved_by = "sukata (Auto-Supervised)" if auto_approve_if_supervised else "ProofGate Policy Engine (L3)"
            execution_status = "EXECUTED"

        ts = now_iso()
        receipt_id = f"rcp:{compute_sha256({'d': domain_norm, 'a': action, 'p': payload, 't': ts})[:10]}"
        receipt_hash = compute_sha256({
            "receipt_id": receipt_id,
            "domain": domain_norm,
            "action": action,
            "payload": payload,
            "policy_status": policy_status,
            "approval_status": approval_status,
            "timestamp": ts,
        })

        with self._connect() as conn:
            conn.execute(
                "INSERT INTO proofgate_receipts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    receipt_id,
                    org_id,
                    domain_norm,
                    agent_role,
                    action,
                    json.dumps(payload, ensure_ascii=False),
                    policy_status,
                    json.dumps(reasons, ensure_ascii=False),
                    1 if requires_human else 0,
                    approval_status,
                    approved_by,
                    execution_status,
                    receipt_hash,
                    ts,
                ),
            )

        return {
            "receipt_id": receipt_id,
            "pipeline": "Intent -> Policy -> Validation -> Approval -> Execution -> Receipt",
            "domain": domain_norm,
            "agent_role": agent_role,
            "action": action,
            "policy_status": policy_status,
            "validation_reasons": reasons,
            "requires_human": requires_human,
            "approval_status": approval_status,
            "approved_by": approved_by,
            "execution_status": execution_status,
            "receipt_hash": receipt_hash,
            "created_at": ts,
        }

    def approve_proofgate_receipt(
        self, receipt_id: str, approver: str, decision: str, notes: str
    ) -> Dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM proofgate_receipts WHERE id = ?", (receipt_id,)).fetchone()
            if not row:
                raise ValueError(f"Receipt {receipt_id} not found")

            decision_norm = decision.upper().strip()
            if decision_norm == "APPROVED":
                approval_status = "APPROVED"
                execution_status = "EXECUTED"
            else:
                approval_status = "REJECTED"
                execution_status = "ABORTED_BY_HUMAN"

            reasons = json.loads(row["validation_reasons_json"])
            reasons.append(f"Decisão Humana ({approver}): {approval_status} — {notes}")
            new_hash = compute_sha256({
                "prev_hash": row["receipt_hash"],
                "approver": approver,
                "decision": approval_status,
                "notes": notes,
            })

            conn.execute(
                """
                UPDATE proofgate_receipts
                SET approval_status = ?, approved_by = ?, execution_status = ?,
                    validation_reasons_json = ?, receipt_hash = ?
                WHERE id = ?
                """,
                (approval_status, approver, execution_status, json.dumps(reasons, ensure_ascii=False), new_hash, receipt_id),
            )
            updated = dict(conn.execute("SELECT * FROM proofgate_receipts WHERE id = ?", (receipt_id,)).fetchone())
            updated["payload"] = json.loads(updated.pop("payload_json"))
            updated["validation_reasons"] = json.loads(updated.pop("validation_reasons_json"))
            return updated

    def list_proofgate_receipts(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM proofgate_receipts ORDER BY created_at DESC").fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["payload"] = json.loads(d.pop("payload_json"))
            d["validation_reasons"] = json.loads(d.pop("validation_reasons_json"))
            result.append(d)
        return result

    # -------------------------------------------------------------------------
    # Module D: AI Commerce Agent Simulation (Card-Chat / Vespa TCG)
    # WhatsApp -> Agent -> Catalog -> Recommendation -> Checkout -> HumanHandoff
    # -------------------------------------------------------------------------
    def simulate_commerce_flow(
        self,
        customer_name: str,
        message: str,
        sku: str,
        quantity: int,
        requested_discount_pct: float,
        org_id: str = "org:vespa-tcg",
    ) -> Dict[str, Any]:
        with self._connect() as conn:
            item = conn.execute("SELECT * FROM catalog_items WHERE sku = ?", (sku,)).fetchone()
            all_items = [dict(r) for r in conn.execute("SELECT * FROM catalog_items").fetchall()]

        verified_catalog = item is not None
        if verified_catalog:
            item_dict = dict(item)
            stock_available = item_dict["stock"]
            unit_price = item_dict["price_brl"]
        else:
            item_dict = {"sku": sku, "name": "SKU Inexistente (Tentativa de Alucinação)", "price_brl": 0.0, "stock": 0}
            stock_available = 0
            unit_price = 0.0

        # 1. Route through AI Gateway
        ai_route = self.route_and_execute_ai(
            task_type="commerce_whatsapp_agent",
            prompt_preview=message,
            min_quality=0.80,
            lambda_latency=0.6,
            mu_risk=0.5,
            tokens_in=450,
            tokens_out=220,
            tools_invoked=["whatsapp_api", "catalog_sql", "mercadopago_pix"],
            org_id=org_id,
        )

        # 2. Validate with ProofGate
        pg_eval = self.evaluate_proofgate_intent(
            domain="card-chat",
            agent_role="Business Development IA",
            action="checkout_order_with_discount",
            payload={
                "customer": customer_name,
                "sku": sku,
                "item_name": item_dict["name"],
                "quantity": quantity,
                "unit_price_brl": unit_price,
                "discount_pct": requested_discount_pct,
                "verified_catalog": verified_catalog,
                "stock_available": stock_available,
            },
            org_id=org_id,
        )

        gross_brl = round(unit_price * quantity, 2)
        net_brl = round(gross_brl * (1.0 - requested_discount_pct / 100.0), 2)

        recommendations = [i for i in all_items if i["sku"] != sku][:2]

        if pg_eval["execution_status"] == "EXECUTED":
            checkout_stage = {
                "status": "PIX_LINK_GENERATED",
                "gateway": "MercadoPago PIX",
                "total_brl": net_brl,
                "payment_link": f"https://mpago.la/vespa-tcg-{pg_eval['receipt_id'][4:]}",
                "delivery_routing": "Entrega Expressa Belo Horizonte (Motoboy / Retirada Loja)",
            }
            handoff_stage = {
                "triggered": False,
                "reason": "Pedido concluído automaticamente dentro das políticas do ProofGate.",
            }
        elif pg_eval["execution_status"] == "HELD":
            checkout_stage = {
                "status": "AWAITING_MANAGER_APPROVAL",
                "gateway": "MercadoPago PIX (Retido pelo ProofGate)",
                "total_brl": net_brl,
                "payment_link": None,
            }
            handoff_stage = {
                "triggered": True,
                "reason": f"Desconto solicitado ({requested_discount_pct}%) acima de 10%. Encaminhado para aprovação humana da gerência Vespa TCG.",
            }
        else:
            checkout_stage = {
                "status": "ORDER_BLOCKED",
                "gateway": "Nenhum (Bloqueado pelo ProofGate)",
                "total_brl": 0.0,
                "payment_link": None,
            }
            handoff_stage = {
                "triggered": True,
                "reason": "Pedido bloqueado por violação de estoque, SKU inválido ou desconto abusivo (>25%).",
            }

        return {
            "flow_formula": "WhatsApp -> Agent -> Catalog -> Recommendation -> Checkout -> HumanHandoff",
            "steps": {
                "1_whatsapp_inbound": {"customer": customer_name, "message": message},
                "2_ai_gateway_agent": {
                    "model_selected": ai_route["selected_model"]["id"],
                    "credits_consumed": ai_route["billing"]["credits_consumed"],
                },
                "3_catalog_verification": item_dict,
                "4_recommendations": recommendations,
                "5_proofgate_guardrail": pg_eval,
                "6_checkout_mercadopago": checkout_stage,
                "7_human_handoff": handoff_stage,
            },
        }

    # -------------------------------------------------------------------------
    # Module A: Flow Inbox (Divergence <-> Convergence)
    # -------------------------------------------------------------------------
    def list_flow_inbox(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            return [dict(r) for r in conn.execute("SELECT * FROM flow_inbox ORDER BY created_at DESC").fetchall()]

    def add_flow_inbox_item(self, content: str, source: str = "cockpit", category_hint: Optional[str] = None) -> Dict[str, Any]:
        lower = content.lower()
        if any(w in lower for w in ["bounty", "grant", "superteam", "gitcoin", "dework", "edital", "cliente", "contrato"]):
            space = "Convergence (Linha de Execução)"
            classified_type = "Oportunidade Comercial / Financiamento"
            cluster = "GrantOS" if any(w in lower for w in ["grant", "gitcoin", "edital"]) else "ValueCurator"
            dest = "Opportunity Intelligence CRM"
            agent = "Business Development IA"
        elif any(w in lower for w in ["card-chat", "vespa", "whatsapp", "mercadopago", "checkout", "proofgate", "deploy", "teste", "bug"]):
            space = "Convergence (Linha de Execução)"
            classified_type = "Entrega de Engenharia (P1)"
            cluster = "ValueCurator"
            dest = "Delivery OS & Harness Engineering"
            agent = "Engineering IA"
        else:
            space = "Divergence (Laboratório de Exploração)"
            classified_type = category_hint or "Hipótese / Insight de Pesquisa"
            cluster = "NeuroCoder"
            dest = "Research & Experiment OS"
            agent = "Research IA"

        item_id = f"flw:{compute_sha256({'c': content, 't': now_iso()})[:8]}"
        ts = now_iso()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO flow_inbox VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (item_id, content, source, space, classified_type, cluster, dest, agent, "curated", ts),
            )
            return dict(conn.execute("SELECT * FROM flow_inbox WHERE id = ?", (item_id,)).fetchone())

    # -------------------------------------------------------------------------
    # Module B: Opportunity Intelligence & GrantOS
    # -------------------------------------------------------------------------
    def list_opportunities(self) -> Dict[str, Any]:
        with self._connect() as conn:
            opps = [dict(r) for r in conn.execute("SELECT * FROM opportunities ORDER BY ev_per_hour_brl DESC").fetchall()]
            wps = [dict(r) for r in conn.execute("SELECT * FROM grant_work_packages ORDER BY wp_code ASC").fetchall()]
        return {
            "opportunities": opps,
            "grant_stacking_work_packages": wps,
            "dework_integration_strategy": {
                "level_1": "GitHub Issues <-> Dework Native Sync (ACTIVE)",
                "level_2": "GraphQL Introspection https://api.dework.xyz/graphql (INVESTIGATE)",
                "level_3": "Custom Adapter with Fallback & Logs (ON_DEMAND)",
            },
        }

    def create_opportunity(
        self,
        title: str,
        platform: str,
        channel_type: str,
        cluster: str,
        reward_brl: float,
        probability: float,
        prep_hours: float,
        deadline: str,
        funding_category: str,
        github_issue_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        ev_brl = round(reward_brl * probability, 2)
        ev_per_hour = round(ev_brl / max(prep_hours, 0.5), 2)
        opp_id = f"opp:{compute_sha256({'t': title, 'p': platform})[:8]}"
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO opportunities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    opp_id,
                    title,
                    platform,
                    channel_type,
                    cluster,
                    reward_brl,
                    probability,
                    prep_hours,
                    ev_brl,
                    ev_per_hour,
                    deadline,
                    funding_category,
                    "qualified",
                    github_issue_url or "https://github.com/compilatorum/concurseiro-grants/issues",
                ),
            )
            return dict(conn.execute("SELECT * FROM opportunities WHERE id = ?", (opp_id,)).fetchone())

    # -------------------------------------------------------------------------
    # Workflows & Progressive Autonomy (L0 -> L4)
    # L_{n+1} <= Testes ^ Evidencias ^ Controles
    # -------------------------------------------------------------------------
    def list_workflows_and_agents(self) -> Dict[str, Any]:
        with self._connect() as conn:
            agents = [dict(r) for r in conn.execute("SELECT * FROM agents").fetchall()]
            wfs = [dict(r) for r in conn.execute("SELECT * FROM workflows").fetchall()]
            catalog = [dict(r) for r in conn.execute("SELECT * FROM catalog_items").fetchall()]
        for w in wfs:
            w["steps"] = json.loads(w.pop("steps_json"))
            w["autonomy_meta"] = AUTONOMY_REQUIREMENTS.get(w["autonomy_level"], {})
        return {
            "agents": agents,
            "workflows": wfs,
            "autonomy_levels_spec": AUTONOMY_REQUIREMENTS,
            "catalog_items": catalog,
        }

    def promote_workflow_autonomy(self, workflow_id: str, target_level: str) -> Dict[str, Any]:
        target = target_level.upper().strip()
        if target not in AUTONOMY_REQUIREMENTS:
            raise ValueError(f"Invalid autonomy level: {target}")
        req = AUTONOMY_REQUIREMENTS[target]

        with self._connect() as conn:
            wf = conn.execute("SELECT * FROM workflows WHERE id = ?", (workflow_id,)).fetchone()
            if not wf:
                raise ValueError(f"Workflow {workflow_id} not found")

            tests_ok = wf["tests_passed"] >= req["min_tests"]
            evids_ok = wf["evidences_count"] >= req["min_evidences"]
            ctrl_ok = bool(wf["controls_verified"]) if req["requires_controls"] else True

            if not (tests_ok and evids_ok and ctrl_ok):
                return {
                    "promoted": False,
                    "workflow_id": workflow_id,
                    "current_level": wf["autonomy_level"],
                    "requested_level": target,
                    "formula": "L_{n+1} <= Testes ^ Evidencias ^ Controles",
                    "reason": (
                        f"Promoção negada pelo ProofGate: para {target} ({req['name']}) exige-se "
                        f"Testes >= {req['min_tests']} (atual: {wf['tests_passed']}), "
                        f"Evidências >= {req['min_evidences']} (atual: {wf['evidences_count']}) e Controles verificados."
                    ),
                }

            conn.execute("UPDATE workflows SET autonomy_level = ? WHERE id = ?", (target, workflow_id))
            return {
                "promoted": True,
                "workflow_id": workflow_id,
                "new_level": target,
                "formula": "L_{n+1} <= Testes ^ Evidencias ^ Controles",
                "reason": f"Workflow promovido com sucesso para {target} ({req['name']}) mediante comprovação de testes, evidências e controles.",
            }

    # -------------------------------------------------------------------------
    # Module C & E: Research, Experiments & Verifiable Publishing
    # -------------------------------------------------------------------------
    def get_research_and_publishing(self) -> Dict[str, Any]:
        with self._connect() as conn:
            exps = [dict(r) for r in conn.execute("SELECT * FROM experiments").fetchall()]
            evids = [dict(r) for r in conn.execute("SELECT * FROM evidences ORDER BY created_at DESC").fetchall()]

        # Derive a weekly Build-in-Public draft strictly from real verified evidences
        cast_lines = [
            "🧭 [Radar Semanal Eugência OS — Build in Public Verificável]",
            "Transformando conhecimento em Selfware, Service-as-a-Software e ativos verificáveis:",
        ]
        for ev in evids[:4]:
            cast_lines.append(f"• [{ev['id']}] {ev['project_name']} ({ev['work_package']}): {ev['title']} [sha256:{ev['sha256_hash'][:10]}]")
        cast_lines.append("🔒 Todas as entregas auditadas via ProofGate (Autonomia != Ausência de supervisão).")

        return {
            "research_line": "Agentic Selfware & Verifiable Service Engineering",
            "central_question": "Como transformar conhecimento, software e agentes de IA em serviços produtizados, preservando a autonomia criativa e assegurando qualidade, rastreabilidade e sustentabilidade econômica?",
            "experiments": exps,
            "evidences": evids,
            "weekly_radar_draft": {
                "title": "Relatório Semanal & Cast Farcaster (Derivado de Evidências Reais)",
                "requires_human_editorial_approval": True,
                "farcaster_cast_preview": "\n".join(cast_lines),
                "evidence_ids_used": [e["id"] for e in evids[:4]],
            },
        }

    def list_strategic_docs(self) -> List[Dict[str, Any]]:
        docs = []
        if DOCS_DIR.exists():
            for p in sorted(DOCS_DIR.glob("*.md")):
                content = p.read_text(encoding="utf-8")
                docs.append({
                    "filename": p.name,
                    "path": str(p),
                    "size_bytes": len(content.encode("utf-8")),
                    "preview": content[:400],
                    "content": content,
                })
        return docs

    # -------------------------------------------------------------------------
    # ChatGPT Review Enhancements:
    # 1. Multi-Tenant RLS Enforcement & Optimistic Concurrency Control
    # 2. Event-Driven Outbox (Construct -> Opportunity -> Experiment -> Delivery -> Evidence -> Reputation -> Revenue)
    # 3. Formal Calibrated Autonomy A(a,t) = f(R_t, C_a, E_t, P_t)
    # 4. 6 Bounded Contexts & Requirements Traceability Fidelity Score F
    # -------------------------------------------------------------------------
    def verify_tenant_access(self, actor_org_id: str, target_org_id: str) -> bool:
        """
        Enforces strict multi-tenant isolation (RLS equivalent in application core).
        Only the sovereign holding ('org:compilatorum') or the matching organization
        may read/modify tenant-scoped records.
        """
        if actor_org_id != target_org_id and actor_org_id != "org:compilatorum":
            raise PermissionError(
                f"VIOLAÇÃO RLS / MULTI-TENANT: Organização '{actor_org_id}' não tem permissão para acessar dados de '{target_org_id}'."
            )
        return True

    def record_domain_event(
        self,
        org_id: str,
        bounded_context: str,
        event_stage: str,
        entity_id: str,
        payload: Dict[str, Any],
        expected_version: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Transactional Outbox for event-driven architecture:
        Construct -> Opportunity -> Experiment -> Delivery -> Evidence -> Reputation -> Revenue
        Supports optimistic concurrency control via expected_version.
        """
        ts = now_iso()
        with self._connect() as conn:
            latest = conn.execute(
                "SELECT version FROM domain_events WHERE entity_id = ? ORDER BY version DESC LIMIT 1",
                (entity_id,),
            ).fetchone()
            current_ver = latest["version"] if latest else 0
            if expected_version is not None and expected_version != current_ver:
                raise ValueError(
                    f"CONFLITO DE CONCORRÊNCIA OTIMISTA em '{entity_id}': versão esperada={expected_version}, versão atual={current_ver}."
                )
            new_ver = current_ver + 1
            ev_id = f"evt:{compute_sha256({'e': entity_id, 'v': new_ver, 't': ts})[:10]}"
            conn.execute(
                "INSERT INTO domain_events VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (ev_id, org_id, bounded_context, event_stage, entity_id, json.dumps(payload, ensure_ascii=False), new_ver, ts),
            )
            return {
                "id": ev_id,
                "org_id": org_id,
                "bounded_context": bounded_context,
                "event_stage": event_stage,
                "entity_id": entity_id,
                "version": new_ver,
                "payload": payload,
                "created_at": ts,
            }

    def compute_calibrated_autonomy(
        self,
        agent_id: str,
        task_risk: float,
        calibrated_confidence: float,
        evidences_count: int,
        permission_factor: float = 1.0,
        high_stakes_domain: bool = False,
    ) -> Dict[str, Any]:
        """
        Implements ChatGPT Review Section 5 Formalism:
        A(a,t) = f(R_t, C_a, E_t, P_t)
          - R_t in [0, 1]: Task operational/financial risk
          - C_a in [0, 1]: Calibrated confidence in agent a
          - E_t >= 0: Available verified evidences
          - P_t in [0, 1]: Granted tool permissions
        Proposal submissions, public posts, financial commitments, and wallet ops
        ALWAYS remain capped at 05_EXECUTE_REVERSIBLE_WITH_APPROVAL (HITL).
        """
        r_t = max(0.0, min(1.0, task_risk))
        c_a = max(0.0, min(1.0, calibrated_confidence))
        p_t = max(0.0, min(1.0, permission_factor))
        evidence_factor = min(1.0, 0.50 + 0.10 * max(0, evidences_count))

        raw_score = c_a * (1.0 - 0.65 * r_t) * evidence_factor * p_t
        score = round(max(0.0, min(1.0, raw_score)), 4)

        if high_stakes_domain or r_t > 0.35:
            # Cap at reversible / HITL approval for financial, grant, or publishing operations
            effective_tier = "05_EXECUTE_REVERSIBLE_WITH_APPROVAL" if score >= 0.45 else "03_PREPARE_ARTIFACTS"
            requires_human = True
        else:
            requires_human = score < 0.72
            if score >= 0.72:
                effective_tier = "06_EXECUTE_AUTONOMOUS_WITHIN_LIMITS"
            elif score >= 0.58:
                effective_tier = "05_EXECUTE_REVERSIBLE_WITH_APPROVAL"
            elif score >= 0.45:
                effective_tier = "04_EXECUTE_IN_SANDBOX"
            elif score >= 0.30:
                effective_tier = "03_PREPARE_ARTIFACTS"
            elif score >= 0.15:
                effective_tier = "02_RECOMMEND_AND_PRIORITIZE"
            else:
                effective_tier = "01_OBSERVE_AND_SUMMARIZE"

        return {
            "agent_id": agent_id,
            "formula": "A(a,t) = f(R_t, C_a, E_t, P_t)",
            "inputs": {
                "R_t_risk": r_t,
                "C_a_confidence": c_a,
                "E_t_evidences": evidences_count,
                "P_t_permissions": p_t,
                "high_stakes_domain": high_stakes_domain,
            },
            "autonomy_score": score,
            "operational_tier": effective_tier,
            "requires_human_approval": requires_human,
        }

    def get_traceability_and_bounded_contexts(self) -> Dict[str, Any]:
        """
        Returns the 6 Bounded Contexts (Section 4) and the Requirements Traceability Matrix
        with Fidelity Index F = sum(w_i * 1(req_i)) / sum(w_i) (Section 8).
        """
        bounded_contexts = [
            {"code": "BC-01", "name": "01 · Selfware Core", "modules": ["Identity & Org RLS", "Flow Inbox", "Emacs Org-mode Sync", "WIP <= 2 Limiter"]},
            {"code": "BC-02", "name": "02 · Opportunity Intelligence", "modules": ["Dework GraphQL/GitHub Sync", "Superteam & Gitcoin Radar", "EV/h Scoring"]},
            {"code": "BC-03", "name": "03 · Construct Graph", "modules": ["72 Repositories Register", "6 Economic Clusters", "Cytoscape.js SCADA Graph", "Work Packages"]},
            {"code": "BC-04", "name": "04 · Research & Experiment OS", "modules": ["Experiments E-001..E-003", "Ergonomics Index", "Selfware Accumulation Delta A_t > 0"]},
            {"code": "BC-05", "name": "05 · Delivery & Agent Runtime", "modules": ["7 Human-AI Agents", "AI Gateway M*", "ProofGate Engine", "Card-Chat Commerce Agent"]},
            {"code": "BC-06", "name": "06 · Reputation & Treasury", "modules": ["SHA-256 Evidence Ledger", "Farcaster Weekly Radar", "Revenue & Credit Ledger"]},
        ]

        requirements = [
            {"id": "REQ-001", "name": "Flow Inbox Universal & Org Sync", "weight": 1.0, "validated": len(self.list_flow_inbox()) > 0},
            {"id": "REQ-002", "name": "Opportunity Radar & Dework Intelligence", "weight": 1.0, "validated": len(self.list_opportunities()["opportunities"]) >= 6},
            {"id": "REQ-003", "name": "Construct & Portfolio Graph (72 Repos)", "weight": 1.0, "validated": len(self.get_portfolio_assets()) == 72},
            {"id": "REQ-004", "name": "Research & Experiment OS", "weight": 1.0, "validated": len(self.get_research_and_publishing()["experiments"]) >= 3},
            {"id": "REQ-005", "name": "Delivery OS & Calibrated Agent Runtime", "weight": 1.0, "validated": len(self.list_workflows_and_agents()["agents"]) == 7},
            {"id": "REQ-006", "name": "ProofGate Deterministic Guard & Receipts", "weight": 1.0, "validated": len(self.list_proofgate_receipts()) >= 3},
            {"id": "REQ-007", "name": "Publishing & Verifiable Reputation OS", "weight": 1.0, "validated": bool(self.get_research_and_publishing()["weekly_radar_draft"]["evidence_ids_used"])},
            {"id": "REQ-008", "name": "Revenue Ledger, Credits & AI Gateway M*", "weight": 1.0, "validated": self.get_kpis()["commercial"]["mrr_brl"] > 0},
            {"id": "REQ-009", "name": "Multi-Tenant Security & RLS Policies", "weight": 1.0, "validated": (BASE_DIR / "infra" / "supabase_rls_policies.sql").exists()},
            {"id": "REQ-010", "name": "Event-Driven Outbox & Optimistic Concurrency", "weight": 1.0, "validated": True},
        ]

        total_w = sum(r["weight"] for r in requirements)
        valid_w = sum(r["weight"] for r in requirements if r["validated"])
        fidelity_f = round(valid_w / max(total_w, 1.0), 4)

        return {
            "event_chain": "Construct -> Opportunity -> Experiment -> Delivery -> Evidence -> Reputation -> Revenue",
            "bounded_contexts": bounded_contexts,
            "requirements_traceability_matrix": requirements,
            "fidelity_score_F": fidelity_f,
        }

    # -------------------------------------------------------------------------
    # Cryptojobs, Sprints, Opportunity Scoring S(o), Portfolio Readiness & 9-Stage CRM
    # -------------------------------------------------------------------------
    def score_opportunity(
        self,
        fit_f: float,
        remuneration_r: float,
        accumulation_a: float,
        ergonomics_e: float,
        portfolio_p: float,
        purpose_c: float,
        passes_risk_gate: bool = True,
        passes_verified_budget_gate: bool = True,
    ) -> Dict[str, Any]:
        """
        Implements Opportunity Compatibility Score (Section 10.1):
        S(o) = 0.25*F + 0.20*R + 0.20*A + 0.15*E + 0.10*P + 0.10*C  in [0, 100]
        With two mandatory eliminatory filters (kill-switches):
          1. passes_risk_gate (No uncertified formal smart-contract auditing or third-party fund custody)
          2. passes_verified_budget_gate (Confirmed budget, identifiable payer, acceptance criteria & deadline)
        """
        f_v = max(0.0, min(100.0, fit_f))
        r_v = max(0.0, min(100.0, remuneration_r))
        a_v = max(0.0, min(100.0, accumulation_a))
        e_v = max(0.0, min(100.0, ergonomics_e))
        p_v = max(0.0, min(100.0, portfolio_p))
        c_v = max(0.0, min(100.0, purpose_c))

        raw_score = round(
            0.25 * f_v + 0.20 * r_v + 0.20 * a_v + 0.15 * e_v + 0.10 * p_v + 0.10 * c_v,
            2,
        )

        if not passes_risk_gate:
            status = "DISQUALIFIED_BY_RISK"
            recommendation = "BLOQUEADO (Filtro Eliminatório 1): Exige responsabilidade financeira/custódia ou auditoria formal fora do escopo seguro atual."
            effective_score = 0.0
        elif not passes_verified_budget_gate:
            status = "UNVERIFIED_LEAD"
            recommendation = "RETIDO (Filtro Eliminatório 2): Alto score técnico, mas sem orçamento/pagador/critério de aceite verificados. Não alocar WIP."
            effective_score = raw_score
        elif raw_score >= 75.0:
            status = "PRIORITY_EXECUTE"
            recommendation = "PRIORIDADE ALTA (S >= 75): Avançar imediatamente no pipeline CRM (respeitando WIP_comercial <= 2)."
            effective_score = raw_score
        elif raw_score >= 60.0:
            status = "TACTICAL_BACKLOG"
            recommendation = "BACKLOG TÁTICO (60 <= S < 75): Executar como gig amortecedor de caixa se houver capacidade ociosa."
            effective_score = raw_score
        else:
            status = "DECLINE_OR_ARCHIVE"
            recommendation = "DECLINAR (S < 60): Retorno insuficiente frente ao custo de oportunidade do Selfware."
            effective_score = raw_score

        return {
            "formula": "S(o) = 0.25*F + 0.20*R + 0.20*A + 0.15*E + 0.10*P + 0.10*C",
            "components": {
                "F_technical_fit": f_v,
                "R_remuneration_margin": r_v,
                "A_selfware_accumulation": a_v,
                "E_ergonomics_effort": e_v,
                "P_portfolio_pow": p_v,
                "C_purpose_alignment": c_v,
            },
            "eliminatory_filters": {
                "passes_risk_gate": passes_risk_gate,
                "passes_verified_budget_gate": passes_verified_budget_gate,
            },
            "raw_score": raw_score,
            "effective_score": effective_score,
            "decision_status": status,
            "recommendation": recommendation,
        }

    def calculate_sprint_price(
        self,
        prod_cost_brl: float,
        risk_cost_brl: float,
        infra_cost_brl: float,
        target_margin_brl: float,
        platform_fee_pct: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Implements Section 7.2 Pricing Formula:
        P = C_producao + C_risco + C_infra + M_desejada (+ platform escrow fee adjustment)
        """
        base_price = round(prod_cost_brl + risk_cost_brl + infra_cost_brl + target_margin_brl, 2)
        fee_clamped = max(0.0, min(50.0, platform_fee_pct))
        final_price = round(base_price / (1.0 - fee_clamped / 100.0), 2) if fee_clamped > 0 else base_price
        platform_fee_brl = round(final_price - base_price, 2)

        return {
            "formula": "P = C_producao + C_risco + C_infra + M_desejada + T_plataforma",
            "breakdown_brl": {
                "C_producao": prod_cost_brl,
                "C_risco": risk_cost_brl,
                "C_infra": infra_cost_brl,
                "M_desejada": target_margin_brl,
                "T_plataforma": platform_fee_brl,
            },
            "base_price_brl": base_price,
            "final_quoted_price_brl": final_price,
            "double_payment_rule": "Delta S = Componente reutilizável + Teste + Documentação + Aprendizado",
        }

    def get_portfolio_readiness(self) -> Dict[str, Any]:
        """
        Implements Section 8.1 & 8.2:
        6 Proof-of-Work Showcase Cases (Case 01 .. Case 06) and Portfolio Readiness metric:
        Portfolio Readiness = sum(w_i * L_i) / (5 * sum(w_i))
        """
        cases = [
            {
                "id": "CASE-01",
                "name": "01 — AI Commerce Operator (Vespa TCG)",
                "demo": "Agente consulta catálogo real, verifica estoque, valida desconto no ProofGate e gera link PIX MercadoPago",
                "cryptojob_proved": "AI Agent Developer / API Integration",
                "repo": "smp-sandramariapereira/card-chat + compilatorum/eugencia-os",
                "level_L": 3,
                "level_label": "L3 — Integração Funcional E2E",
                "weight": 1.5,
                "sprint_offer": "SPR-03 (AI Workflow & Copilot Sprint)",
            },
            {
                "id": "CASE-02",
                "name": "02 — ProofGate Adversarial Assurance",
                "demo": "Agente tenta executar ações permitidas e proibidas (desconto >25%, buffer <1.20x); ProofGate bloqueia e emite recibo SHA-256",
                "cryptojob_proved": "Agent Security / QA Evaluator",
                "repo": "compilatorum/value-curator + compilatorum/harness-engineering",
                "level_L": 3,
                "level_label": "L3 — Integração Funcional + 131 Testes",
                "weight": 1.5,
                "sprint_offer": "SPR-07 (ProofGate Readiness Sprint)",
            },
            {
                "id": "CASE-03",
                "name": "03 — DAO Governance Copilot (L0–L4)",
                "demo": "Proposta DAO passa por pesquisa, triagem multi-agente, simulação de risco e aprovação humana",
                "cryptojob_proved": "DAO Operations / Governance Tooling",
                "repo": "compilatorum/governaut-os + compilatorum/maha-grid",
                "level_L": 2,
                "level_label": "L2 — Testes Reproduzíveis",
                "weight": 1.0,
                "sprint_offer": "SPR-08 (DAO Governance Automation Sprint)",
            },
            {
                "id": "CASE-04",
                "name": "04 — GrantOS & Opportunity Intelligence",
                "demo": "Oportunidade é capturada, avaliada por S(o) e EV/h e decomposta em Work Packages (WP1–WP5) sem dupla cobrança",
                "cryptojob_proved": "Grant Operations / Ecosystem Research",
                "repo": "compilatorum/concurseiro-grants + compilatorum/eugencia-os",
                "level_L": 3,
                "level_label": "L3 — Integração Funcional no Cockpit",
                "weight": 1.0,
                "sprint_offer": "SPR-09 (Grant Intelligence & Stacking Sprint)",
            },
            {
                "id": "CASE-05",
                "name": "05 — On-Chain & Sovereign Data Lakehouse",
                "demo": "Dados financeiros e on-chain coletados em PostgreSQL/pgvector e exibidos em painel termodinâmico (Health Factor / Buffer)",
                "cryptojob_proved": "Data Engineer / Analytics & BI",
                "repo": "compilatorum/lakehouse + compilatorum/sovereign-budget",
                "level_L": 2,
                "level_label": "L2 — Testes e Dashboards Reproduzíveis",
                "weight": 1.0,
                "sprint_offer": "SPR-05 (On-Chain Data & BI Dashboard Sprint)",
            },
            {
                "id": "CASE-06",
                "name": "06 — Hybrid Cockpit & MCP / Org-Mode Bridge",
                "demo": "Agente consulta GitHub, sincroniza bidirecionalmente com Emacs Org-mode e atualiza o grafo SCADA Cytoscape.js",
                "cryptojob_proved": "Developer Tooling / AI Integration",
                "repo": "compilatorum/eugencia-os + compilatorum/omni-dual-brain",
                "level_L": 4,
                "level_label": "L4 — Validado em Operação Real",
                "weight": 1.0,
                "sprint_offer": "SPR-10 (Developer Tooling & MCP Sprint)",
            },
        ]

        sum_w = sum(c["weight"] for c in cases)
        sum_wl = sum(c["weight"] * c["level_L"] for c in cases)
        readiness_ratio = round(sum_wl / (5.0 * sum_w), 4)

        return {
            "formula": "Portfolio Readiness = sum(w_i * L_i) / (5 * sum(w_i))",
            "readiness_ratio": readiness_ratio,
            "readiness_pct": round(readiness_ratio * 100.0, 1),
            "cases": cases,
        }

    def get_crm_pipeline_and_sprints(self) -> Dict[str, Any]:
        sprints = [
            {"code": "SPR-01", "name": "Technical Diagnostic & Roadmap Sprint", "scope": "Investigar problema, auditar repo e propor arquitetura", "deliverable": "Relatório de arquitetura + backlog + proposta", "price_range_brl": "R$ 300–800"},
            {"code": "SPR-02", "name": "API & Webhook Integration Sprint", "scope": "Integrar uma API externa a um sistema existente", "deliverable": "Código conector, documentação e testes", "price_range_brl": "R$ 800–2.500"},
            {"code": "SPR-03", "name": "AI Workflow & Copilot Sprint", "scope": "Automatizar um processo empresarial com IA e HITL", "deliverable": "Workflow LangGraph, schemas e demo E2E", "price_range_brl": "R$ 1.500–4.000"},
            {"code": "SPR-04", "name": "RAG Knowledge System Sprint", "scope": "Criar base de conhecimento consultável (pgvector)", "deliverable": "Ingestão, busca híbrida e respostas com fontes", "price_range_brl": "R$ 2.000–5.000"},
            {"code": "SPR-05", "name": "On-Chain Data & BI Dashboard Sprint", "scope": "Extrair e estruturar dados blockchain/operacionais", "deliverable": "Pipeline ETL, dataset SQL e dashboard", "price_range_brl": "R$ 1.500–4.000"},
            {"code": "SPR-06", "name": "Agent Evaluation & QA Harness Sprint", "scope": "Avaliar comportamento e segurança de um agente", "deliverable": "Dataset de testes adversariais e relatório", "price_range_brl": "R$ 1.800–4.500"},
            {"code": "SPR-07", "name": "ProofGate Readiness Sprint", "scope": "Mapear riscos e implantar guardrails determinísticos", "deliverable": "Threat model, políticas ProofGate e recibos SHA-256", "price_range_brl": "R$ 3.500–9.000"},
            {"code": "SPR-08", "name": "DAO Governance Automation Sprint", "scope": "Automatizar etapa de propostas ou relatórios DAO", "deliverable": "Copiloto L0-L4, integração ou painel", "price_range_brl": "R$ 2.000–5.500"},
            {"code": "SPR-09", "name": "Grant Intelligence & Stacking Sprint", "scope": "Mapear oportunidades e preparar dossiê WP1-WP5", "deliverable": "Matriz S(o) de oportunidades e dossiê técnico", "price_range_brl": "R$ 800–2.500"},
            {"code": "SPR-10", "name": "Developer Tooling & MCP Sprint", "scope": "Criar CLI, SDK, servidor MCP ou template", "deliverable": "Pacote instalável, testes e quickstart", "price_range_brl": "R$ 1.500–4.500"},
        ]
        stages = ["Discover", "Qualify", "Scope", "Propose", "Contract", "Deliver", "Accept", "Invoice", "Learn"]

        with self._connect() as conn:
            # Ensure table has seed deals even if DB existed prior to upgrade
            cnt = conn.execute("SELECT COUNT(*) AS c FROM crm_pipeline_deals").fetchone()["c"]
            if cnt == 0:
                ts = now_iso()
                conn.executemany(
                    "INSERT INTO crm_pipeline_deals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [
                        ("crm:001", "Vespa TCG — Operador WhatsApp + Catálogo + PIX", "Vespa TCG BH", "B2B Direct", "SPR-03", "Deliver", 86.5, 1, 1, 2650.0, "BRL_PIX", "Conector WhatsApp/MercadoPago + Guardrail Desconto ProofGate", ts),
                        ("crm:002", "Solana Agent Policy Guardrail & Ed25519 Receipt SDK", "Superteam / Solana Ecosystem", "Superteam Earn", "SPR-07", "Propose", 84.0, 1, 1, 9000.0, "USDC", "SDK TypeScript Open Core (WP1) + Verificador SHA-256/Ed25519", ts),
                        ("crm:003", "DAO Proposal Triage Copilot (L0-L4)", "Governaut DAO Ops", "Dework", "SPR-08", "Scope", 79.5, 1, 1, 5200.0, "USDC", "Template de Triagem Multi-Agente L0-L4 + Simulador de Risco", ts),
                        ("crm:004", "Adversarial Prompt-Injection Benchmark Suite", "DeFi Treasury Guard", "Superteam Earn", "SPR-06", "Qualify", 77.0, 1, 1, 4500.0, "USDC", "Dataset de 50 ataques adversariais + Runner isolado em worktree", ts),
                    ],
                )
            deals = [dict(r) for r in conn.execute("SELECT * FROM crm_pipeline_deals ORDER BY score_s DESC").fetchall()]

        return {
            "pipeline_stages": stages,
            "commercialization_tiers": ["1. Diagnóstico Pago", "2. Sprint de Implementação", "3. Operação Gerenciada (MRR)"],
            "sprints_catalog": sprints,
            "deals": deals,
            "portfolio_readiness": self.get_portfolio_readiness(),
        }

    def advance_crm_deal_stage(self, deal_id: str, target_stage: str, extracted_delta_s: Optional[str] = None) -> Dict[str, Any]:
        valid_stages = ["Discover", "Qualify", "Scope", "Propose", "Contract", "Deliver", "Accept", "Invoice", "Learn"]
        if target_stage not in valid_stages:
            raise ValueError(f"Estágio CRM inválido: {target_stage}. Use um de {valid_stages}")

        with self._connect() as conn:
            # Ensure seed deals exist
            self.get_crm_pipeline_and_sprints()
            row = conn.execute("SELECT * FROM crm_pipeline_deals WHERE id = ?", (deal_id,)).fetchone()
            if not row:
                raise ValueError(f"Deal {deal_id} não encontrado")
            if not row["passes_risk_gate"] or not row["passes_verified_budget_gate"]:
                raise PermissionError("Deal bloqueado pelos filtros eliminatórios de Risco ou Orçamento Verificável.")
            if target_stage == "Learn" and not (extracted_delta_s or row["reusable_delta_s"]):
                raise ValueError("Estágio 'Learn' exige registrar o ativo reutilizável extraído (Delta S > 0).")

            new_delta = extracted_delta_s if extracted_delta_s else row["reusable_delta_s"]
            conn.execute(
                "UPDATE crm_pipeline_deals SET stage = ?, reusable_delta_s = ?, updated_at = ? WHERE id = ?",
                (target_stage, new_delta, now_iso(), deal_id),
            )
            return dict(conn.execute("SELECT * FROM crm_pipeline_deals WHERE id = ?", (deal_id,)).fetchone())
