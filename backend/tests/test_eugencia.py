"""
Comprehensive test suite for Eugência OS & ValueCurator OS.
Verifies:
  1. All 9 strategic EUGENCIA-OS governance artifacts (.md)
  2. Portfolio audit of the 72 real GitHub repositories & WIP <= 2 constraint
  3. Layer 3 AI Gateway formal optimization M* and credit accounting
  4. Layer 7 ProofGate deterministic policies & adversarial test suite across 5 domains
  5. Card-Chat AI Commerce Agent end-to-end flow (Vespa TCG)
  6. Progressive Autonomy promotion rule (L0 -> L4)
  7. Emacs Org-mode bidirectional synchronization
  8. REST API dispatcher endpoints
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.engine import EugenciaEngine
from app.org_sync import OrgModeSynchronizer
from app.server import dispatch_api_request


def test_nine_strategic_documents_exist():
    expected_docs = [
        "PORTFOLIO-ASSETS-REGISTER.md",
        "BUSINESS-ARCHITECTURE.md",
        "PRODUCT-CATALOG.md",
        "SELFWARE-STRATEGY.md",
        "REVENUE-MODEL.md",
        "GRANTOS-STRATEGY.md",
        "VALUECURATOR-OS-SPEC.md",
        "ROADMAP-90-DAYS.md",
        "EXPERIMENT-TRACKER.md",
    ]
    docs_dir = BASE_DIR / "docs" / "eugencia-os"
    for doc_name in expected_docs:
        p = docs_dir / doc_name
        assert p.exists(), f"Missing strategic document: {doc_name}"
        assert p.stat().st_size > 1500, f"Document {doc_name} is too short"


def test_portfolio_72_repos_and_wip_limit(tmp_path):
    engine = EugenciaEngine(db_path=tmp_path / "test.db")
    assets = engine.get_portfolio_assets()
    assert len(assets) == 72
    comp_count = sum(1 for a in assets if a["owner"] == "compilatorum")
    sandra_count = sum(1 for a in assets if a["owner"] == "smp-sandramariapereira")
    assert comp_count == 59
    assert sandra_count == 13

    kpis = engine.get_kpis()
    assert kpis["operational"]["wip_comercial_count"] <= 2
    assert kpis["operational"]["wip_compliant"] is True
    assert set(kpis["operational"]["wip_active_repos"]) == {"card-chat", "value-curator"}
    assert kpis["eugencia_formula"]["E_total_score"] > 70.0


def test_ai_gateway_model_selection_and_credits(tmp_path):
    engine = EugenciaEngine(db_path=tmp_path / "test.db")

    # Low quality requirement -> selects fast/economy model
    res_eco = engine.route_and_execute_ai(
        task_type="faq_lookup",
        prompt_preview="Qual o horário da loja?",
        min_quality=0.70,
        lambda_latency=0.8,
        mu_risk=0.2,
        tokens_in=200,
        tokens_out=100,
        tools_invoked=["catalog_sql"],
        org_id="org:vespa-tcg",
    )
    assert res_eco["selected_model"]["id"] == "gemini-2.5-flash-lite"
    assert res_eco["billing"]["credits_consumed"] >= 1

    # High quality requirement -> selects high-assurance model
    res_high = engine.route_and_execute_ai(
        task_type="policy_audit",
        prompt_preview="Auditar mandato DeFi Solana",
        min_quality=0.95,
        lambda_latency=0.1,
        mu_risk=1.5,
        tokens_in=1000,
        tokens_out=500,
        tools_invoked=["solana_pyth_oracle"],
        org_id="org:solana-dao-pilot",
    )
    assert res_high["selected_model"]["id"] == "gemini-2.5-pro-deep"
    assert res_high["billing"]["credits_consumed"] > res_eco["billing"]["credits_consumed"]


def test_proofgate_adversarial_policies_and_human_approval(tmp_path):
    engine = EugenciaEngine(db_path=tmp_path / "test.db")

    # 1. Card-Chat: <= 10% discount auto-executes
    r_ok = engine.evaluate_proofgate_intent(
        domain="card-chat",
        agent_role="Business Development IA",
        action="apply_discount",
        payload={"sku": "TCG-PKM-151-BOX", "quantity": 1, "stock_available": 10, "discount_pct": 8.0, "verified_catalog": True},
    )
    assert r_ok["policy_status"] == "PASSED"
    assert r_ok["execution_status"] == "EXECUTED"

    # 2. Card-Chat: 18% discount held for human approval
    r_hold = engine.evaluate_proofgate_intent(
        domain="card-chat",
        agent_role="Business Development IA",
        action="apply_discount",
        payload={"sku": "TCG-PKM-151-BOX", "quantity": 1, "stock_available": 10, "discount_pct": 18.0, "verified_catalog": True},
    )
    assert r_hold["policy_status"] == "HOLD_FOR_HUMAN"
    assert r_hold["approval_status"] == "PENDING_HUMAN"
    assert r_hold["execution_status"] == "HELD"

    # Approve via Human-in-the-Loop
    approved = engine.approve_proofgate_receipt(
        receipt_id=r_hold["receipt_id"],
        approver="sukata",
        decision="APPROVED",
        notes="Cliente VIP autorizado pela gerência.",
    )
    assert approved["approval_status"] == "APPROVED"
    assert approved["execution_status"] == "EXECUTED"

    # 3. Card-Chat Adversarial: > 25% discount or unverified catalog blocked
    r_block = engine.evaluate_proofgate_intent(
        domain="card-chat",
        agent_role="Business Development IA",
        action="apply_discount",
        payload={"sku": "FAKE-SKU", "quantity": 1, "stock_available": 0, "discount_pct": 40.0, "verified_catalog": False},
    )
    assert r_block["policy_status"] == "BLOCKED"
    assert r_block["execution_status"] == "BLOCKED"

    # 4. GrantOS Adversarial: Double-funding same Work Package blocked
    r_grant_block = engine.evaluate_proofgate_intent(
        domain="grantos",
        agent_role="Business Development IA",
        action="submit_grant",
        payload={"has_mandatory_docs": True, "duplicate_funding_for_same_wp": True, "proprietary_claimed_as_public_good": False},
    )
    assert r_grant_block["policy_status"] == "BLOCKED"

    # 5. Finance Adversarial: Fiduciary buffer < 1.20 blocked
    r_fin_block = engine.evaluate_proofgate_intent(
        domain="finance",
        agent_role="QA / ProofGate IA",
        action="execute_swap",
        payload={"fiduciary_buffer": 1.05, "health_factor": 1.80, "within_mandate": True},
    )
    assert r_fin_block["policy_status"] == "BLOCKED"

    # 6. Farcaster Adversarial: Publish without verifiable evidence blocked
    r_cast_block = engine.evaluate_proofgate_intent(
        domain="farcaster",
        agent_role="Communications IA",
        action="publish_cast",
        payload={"evidence_id": None},
    )
    assert r_cast_block["policy_status"] == "BLOCKED"


def test_commerce_agent_simulation_and_autonomy(tmp_path):
    engine = EugenciaEngine(db_path=tmp_path / "test.db")

    sim = engine.simulate_commerce_flow(
        customer_name="Cliente Teste",
        message="Quero 2 Booster Box Pokémon 151 no PIX",
        sku="TCG-PKM-151-BOX",
        quantity=2,
        requested_discount_pct=5.0,
    )
    assert sim["steps"]["6_checkout_mercadopago"]["status"] == "PIX_LINK_GENERATED"
    assert sim["steps"]["7_human_handoff"]["triggered"] is False

    # Test workflow autonomy promotion rule: L_{n+1} <= Testes ^ Evidencias ^ Controles
    # wf:commerce-order has 24 tests and 4 evidences -> can promote to L3, but L4 requires 50 tests
    promo_l4 = engine.promote_workflow_autonomy("wf:commerce-order", "L4")
    assert promo_l4["promoted"] is False
    # wf:proofgate-mandate has 131 tests and 5 evidences -> can promote to L4
    promo_pg_l4 = engine.promote_workflow_autonomy("wf:proofgate-mandate", "L4")
    assert promo_pg_l4["promoted"] is True


def test_org_mode_bidirectional_sync_and_api(tmp_path):
    engine = EugenciaEngine(db_path=tmp_path / "test.db")
    org_dir = tmp_path / "org"
    sync = OrgModeSynchronizer(engine, org_dir=org_dir)

    written = sync.export_all_to_org()
    assert "inbox.org" in written
    assert "portfolio.org" in written
    assert "opportunities.org" in written
    assert "experiments.org" in written

    # Append a new heading in Emacs format without :ID: and sync back
    inbox_file = org_dir / "inbox.org"
    content = inbox_file.read_text(encoding="utf-8")
    content += "\n** FLOW Criar conector Superteam Earn para bounties Solana\n"
    inbox_file.write_text(content, encoding="utf-8")

    res = sync.import_new_from_inbox_org()
    assert res["imported_count"] == 1
    assert res["imported_items"][0]["Suggested_cluster" if "Suggested_cluster" in res["imported_items"][0] else "suggested_cluster"] in ("GrantOS", "ValueCurator")

    # Test API dispatcher health & graph
    st, health = dispatch_api_request("GET", "/api/health", {}, {})
    assert st == 200 and health["status"] == "ok"

    st_g, graph = dispatch_api_request("GET", "/api/portfolio/graph", {}, {})
    assert st_g == 200 and len(graph["nodes"]) > 20


def test_multi_tenant_isolation_and_optimistic_concurrency(tmp_path):
    """
    Verifies ChatGPT Review Section 2.1 (negative tenant isolation test: Tenant A cannot access Tenant B)
    and Section 2.2 (optimistic concurrency control + Transactional Event Outbox).
    """
    import pytest
    engine = EugenciaEngine(db_path=tmp_path / "test_sec.db")

    # Positive check: same tenant or sovereign holding allowed
    assert engine.verify_tenant_access("org:vespa-tcg", "org:vespa-tcg") is True
    assert engine.verify_tenant_access("org:compilatorum", "org:vespa-tcg") is True

    # Negative check: Tenant A ('org:vespa-tcg') CANNOT access Tenant B ('org:solana-dao-pilot')
    with pytest.raises(PermissionError, match="VIOLAÇÃO RLS / MULTI-TENANT"):
        engine.verify_tenant_access("org:vespa-tcg", "org:solana-dao-pilot")

    # Transactional Outbox & Optimistic Concurrency Control
    ev1 = engine.record_domain_event(
        org_id="org:vespa-tcg",
        bounded_context="BC-05",
        event_stage="Delivery",
        entity_id="dlv:001",
        payload={"step": "initial_setup"},
        expected_version=0,
    )
    assert ev1["version"] == 1

    # Stale expected_version (0 instead of 1) must raise optimistic concurrency conflict
    with pytest.raises(ValueError, match="CONFLITO DE CONCORRÊNCIA OTIMISTA"):
        engine.record_domain_event(
            org_id="org:vespa-tcg",
            bounded_context="BC-05",
            event_stage="Evidence",
            entity_id="dlv:001",
            payload={"step": "stale_write"},
            expected_version=0,
        )


def test_bounded_contexts_and_fidelity_matrix(tmp_path):
    """
    Verifies ChatGPT Review Sections 4, 5, and 8:
    - 6 Bounded Contexts
    - Calibrated Autonomy A(a,t) = f(R_t, C_a, E_t, P_t)
    - Traceability Fidelity Score F == 1.00 (100%)
    """
    engine = EugenciaEngine(db_path=tmp_path / "test_rtm.db")
    rtm = engine.get_traceability_and_bounded_contexts()
    assert len(rtm["bounded_contexts"]) == 6
    assert rtm["fidelity_score_F"] == 1.0

    # High-stakes financial/grant task must always require human approval regardless of confidence
    cal_high_risk = engine.compute_calibrated_autonomy(
        agent_id="agt:bizdev",
        task_risk=0.75,
        calibrated_confidence=0.98,
        evidences_count=10,
        permission_factor=1.0,
        high_stakes_domain=True,
    )
    assert cal_high_risk["requires_human_approval"] is True
    assert cal_high_risk["operational_tier"] == "05_EXECUTE_REVERSIBLE_WITH_APPROVAL"

    # Low-risk, well-evidenced task can execute within deterministic limits
    cal_low_risk = engine.compute_calibrated_autonomy(
        agent_id="agt:engineering",
        task_risk=0.10,
        calibrated_confidence=0.95,
        evidences_count=6,
        permission_factor=1.0,
        high_stakes_domain=False,
    )
    assert cal_low_risk["requires_human_approval"] is False
    assert cal_low_risk["operational_tier"] == "06_EXECUTE_AUTONOMOUS_WITHIN_LIMITS"


def test_cryptojobs_opportunity_scoring_crm_and_readiness(tmp_path):
    """
    Verifies ChatGPT Cryptojobs & Career Architecture Upgrade:
      1. 4 new operational documents (CRYPTOJOBS-MARKET-MAP.md, SERVICE-CATALOG.md, FREELANCER-PROFILE.md, OPPORTUNITY-SCORING.md)
      2. Opportunity Compatibility Score S(o) = 0.25F + 0.20R + 0.20A + 0.15E + 0.10P + 0.10C + 2 Eliminatory Filters
      3. Sprint Pricing Formula P = C_prod + C_risco + C_infra + M_desejada + T_plataforma
      4. Portfolio Readiness metric across the 6 Proof-of-Work Showcase Cases (CASE-01..CASE-06)
      5. 9-Stage CRM Pipeline progression (Discover -> Qualify -> Scope -> Propose -> Contract -> Deliver -> Accept -> Invoice -> Learn)
    """
    docs_dir = BASE_DIR / "docs" / "eugencia-os"
    for new_doc in [
        "CRYPTOJOBS-MARKET-MAP.md",
        "SERVICE-CATALOG.md",
        "FREELANCER-PROFILE.md",
        "OPPORTUNITY-SCORING.md",
    ]:
        assert (docs_dir / new_doc).exists(), f"Missing {new_doc}"

    engine = EugenciaEngine(db_path=tmp_path / "test_crm.db")

    # 1. Opportunity Scoring S(o) with high compatibility
    sc_ok = engine.score_opportunity(
        fit_f=90.0,
        remuneration_r=80.0,
        accumulation_a=85.0,
        ergonomics_e=80.0,
        portfolio_p=90.0,
        purpose_c=95.0,
        passes_risk_gate=True,
        passes_verified_budget_gate=True,
    )
    # 0.25*90 + 0.20*80 + 0.20*85 + 0.15*80 + 0.10*90 + 0.10*95 = 22.5 + 16 + 17 + 12 + 9 + 9.5 = 86.0
    assert sc_ok["raw_score"] == 86.0
    assert sc_ok["decision_status"] == "PRIORITY_EXECUTE"

    # Kill-switch 1: fails risk gate (e.g. uncertified smart-contract formal audit or fund custody)
    sc_risk = engine.score_opportunity(
        fit_f=95.0,
        remuneration_r=95.0,
        accumulation_a=90.0,
        ergonomics_e=80.0,
        portfolio_p=90.0,
        purpose_c=90.0,
        passes_risk_gate=False,
        passes_verified_budget_gate=True,
    )
    assert sc_risk["decision_status"] == "DISQUALIFIED_BY_RISK"
    assert sc_risk["effective_score"] == 0.0

    # Kill-switch 2: fails verified budget gate
    sc_unverified = engine.score_opportunity(
        fit_f=85.0,
        remuneration_r=80.0,
        accumulation_a=85.0,
        ergonomics_e=80.0,
        portfolio_p=80.0,
        purpose_c=85.0,
        passes_risk_gate=True,
        passes_verified_budget_gate=False,
    )
    assert sc_unverified["decision_status"] == "UNVERIFIED_LEAD"

    # 2. Sprint Price Quote P (with 10% LaborX escrow fee test)
    quote = engine.calculate_sprint_price(
        prod_cost_brl=1200.0,
        risk_cost_brl=300.0,
        infra_cost_brl=100.0,
        target_margin_brl=1100.0,
        platform_fee_pct=10.0,
    )
    assert quote["base_price_brl"] == 2700.0
    assert quote["final_quoted_price_brl"] == 3000.0

    # 3. Portfolio Readiness & 9-Stage CRM Pipeline
    crm_data = engine.get_crm_pipeline_and_sprints()
    assert len(crm_data["sprints_catalog"]) == 10
    assert len(crm_data["pipeline_stages"]) == 9
    assert len(crm_data["portfolio_readiness"]["cases"]) == 6
    assert crm_data["portfolio_readiness"]["readiness_pct"] == 57.1

    advanced = engine.advance_crm_deal_stage(
        deal_id="crm:001",
        target_stage="Learn",
        extracted_delta_s="Conector genérico WhatsApp + Teste E2E ProofGate extraído para o VOS",
    )
    assert advanced["stage"] == "Learn"


