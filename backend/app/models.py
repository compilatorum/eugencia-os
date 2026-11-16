"""
Domain models and formal equations for Eugência OS & ValueCurator OS (7 Layers).
Implements:
  - Layer 1 (Identity): Organization, User, Workspace
  - Layer 2 (Business): Subscription, Invoice, Usage, Normalized Credits
  - Layer 3 (Intelligence): AI Gateway Model Routing M* = argmin [C(m) + lambda*L(m) + mu*R(m)] s.t. Q(m) >= Q_min
  - Layer 4 (Agents): Agent (7 Human-AI roles), Workflow (L0-L4 progressive autonomy), Execution
  - Layer 5 (Memory): RepositoryAsset (72 repos), FlowInboxItem, Experiment
  - Layer 6 (Tools): Opportunity (Superteam, Gitcoin, Dework/GitHub), WorkPackage (Grant Stacking)
  - Layer 7 (Governance): ProofGateIntent, ProofGateReceipt, Evidence, Approval
"""
from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class RouteRequest(BaseModel):
    task_type: str = Field(default="commerce_chat", description="Type of task: commerce_chat, code_review, grant_analysis, policy_audit, research_synthesis")
    prompt_preview: str = Field(default="Consultar disponibilidade de booster box Pokémon no estoque")
    min_quality: float = Field(default=0.75, ge=0.0, le=1.0, description="Minimum required quality Q_min")
    lambda_latency: float = Field(default=0.4, ge=0.0, le=5.0, description="Latency weight lambda")
    mu_risk: float = Field(default=0.5, ge=0.0, le=5.0, description="Operational risk weight mu")
    tokens_in: int = Field(default=600, ge=1)
    tokens_out: int = Field(default=300, ge=1)
    tools_invoked: List[str] = Field(default_factory=lambda: ["catalog_sql"])
    org_id: str = Field(default="org:vespa-tcg")


class ProofGateIntentRequest(BaseModel):
    domain: str = Field(..., description="card-chat | grantos | finance | neurocoder | farcaster")
    agent_role: str = Field(default="Engineering IA")
    action: str = Field(..., description="Action identifier, e.g., apply_discount, submit_grant, execute_swap, git_deploy, publish_cast")
    payload: Dict[str, Any] = Field(default_factory=dict)
    org_id: str = Field(default="org:valuecurator")
    auto_approve_if_supervised: bool = Field(default=False)


class ProofGateApprovalRequest(BaseModel):
    receipt_id: str
    approver: str = Field(default="sukata (Human Authority)")
    decision: str = Field(default="APPROVED", description="APPROVED or REJECTED")
    notes: str = Field(default="Verificado manualmente no cockpit Eugência OS.")


class FlowInboxCreate(BaseModel):
    content: str
    source: str = Field(default="cockpit", description="cockpit | emacs-org | whatsapp | github | farcaster")
    category_hint: Optional[str] = None


class OpportunityCreate(BaseModel):
    title: str
    platform: str = Field(..., description="Superteam Earn | Gitcoin Grants | Dework/GitHub | B2B Direct | W3F/Polkadot")
    channel_type: str = Field(..., description="Bounty | Grant | Hackathon | Customer | Licensing")
    cluster: str = Field(default="ValueCurator")
    reward_brl: float = Field(default=5000.0, ge=0.0)
    probability: float = Field(default=0.35, ge=0.0, le=1.0)
    prep_hours: float = Field(default=8.0, ge=0.5)
    deadline: str = Field(default="2026-12-15")
    funding_category: str = Field(default="OPEN_PUBLIC_GOODS")
    github_issue_url: Optional[str] = None


class CommerceSimulateRequest(BaseModel):
    customer_name: str = Field(default="Cliente TCG BH")
    message: str = Field(default="Quero 2 Booster Box Scarlet & Violet 151 com 8% de desconto no PIX")
    sku: str = Field(default="TCG-PKM-151-BOX")
    quantity: int = Field(default=2, ge=1)
    requested_discount_pct: float = Field(default=8.0, ge=0.0, le=100.0)
    org_id: str = Field(default="org:vespa-tcg")


class WorkflowAutonomyUpdate(BaseModel):
    workflow_id: str
    target_level: str = Field(..., description="L0 | L1 | L2 | L3 | L4")
