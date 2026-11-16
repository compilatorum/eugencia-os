"""
HTTP / REST API Server for Eugência OS & ValueCurator OS.
Provides a unified API router that works both with FastAPI (when installed)
and with Python's built-in ThreadingHTTPServer / aiohttp (zero external runtime breakage).
Also serves the Web App / PWA frontend static bundle from frontend/dist or frontend/public.
"""
from __future__ import annotations
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, Any, Tuple
from urllib.parse import urlparse, parse_qs

from .engine import EugenciaEngine, BASE_DIR
from .models import (
    RouteRequest,
    ProofGateIntentRequest,
    ProofGateApprovalRequest,
    FlowInboxCreate,
    OpportunityCreate,
    CommerceSimulateRequest,
    WorkflowAutonomyUpdate,
)
from .org_sync import OrgModeSynchronizer

engine = EugenciaEngine()
org_sync = OrgModeSynchronizer(engine)
# Ensure initial Org files exist on startup
org_sync.export_all_to_org()

FRONTEND_DIST = BASE_DIR / "frontend" / "dist"


def dispatch_api_request(method: str, path: str, query: Dict[str, list], body: Dict[str, Any]) -> Tuple[int, Any]:
    """Pure dispatcher for all /api/* endpoints used by both HTTP server, FastAPI, and test suite."""
    try:
        if method == "GET" and path == "/api/health":
            return 200, {
                "status": "ok",
                "system": "Eugência OS & ValueCurator OS",
                "version": "1.0.0",
                "layers": ["Identity", "Business", "Intelligence (AI Gateway)", "Agents", "Memory", "Tools", "Governance (ProofGate)"],
            }

        if method == "GET" and path == "/api/portfolio/kpis":
            return 200, engine.get_kpis()

        if method == "GET" and path == "/api/portfolio/assets":
            cluster = query.get("cluster", [None])[0]
            asset_class = query.get("asset_class", [None])[0]
            owner = query.get("owner", [None])[0]
            priority = query.get("priority", [None])[0]
            assets = engine.get_portfolio_assets(cluster=cluster, asset_class=asset_class, owner=owner, priority=priority)
            return 200, {"count": len(assets), "assets": assets}

        if method == "GET" and path == "/api/portfolio/graph":
            include_archived = query.get("include_archived", ["false"])[0].lower() == "true"
            return 200, engine.get_scada_graph(include_archived=include_archived)

        if method == "POST" and path == "/api/gateway/route":
            req = RouteRequest(**body)
            return 200, engine.route_and_execute_ai(
                task_type=req.task_type,
                prompt_preview=req.prompt_preview,
                min_quality=req.min_quality,
                lambda_latency=req.lambda_latency,
                mu_risk=req.mu_risk,
                tokens_in=req.tokens_in,
                tokens_out=req.tokens_out,
                tools_invoked=req.tools_invoked,
                org_id=req.org_id,
            )

        if method == "GET" and path == "/api/proofgate/receipts":
            return 200, {"receipts": engine.list_proofgate_receipts()}

        if method == "POST" and path == "/api/proofgate/evaluate":
            req = ProofGateIntentRequest(**body)
            return 200, engine.evaluate_proofgate_intent(
                domain=req.domain,
                agent_role=req.agent_role,
                action=req.action,
                payload=req.payload,
                org_id=req.org_id,
                auto_approve_if_supervised=req.auto_approve_if_supervised,
            )

        if method == "POST" and path == "/api/proofgate/approve":
            req = ProofGateApprovalRequest(**body)
            return 200, engine.approve_proofgate_receipt(
                receipt_id=req.receipt_id,
                approver=req.approver,
                decision=req.decision,
                notes=req.notes,
            )

        if method == "GET" and path == "/api/flow-inbox":
            return 200, {"items": engine.list_flow_inbox()}

        if method == "POST" and path == "/api/flow-inbox":
            req = FlowInboxCreate(**body)
            item = engine.add_flow_inbox_item(content=req.content, source=req.source, category_hint=req.category_hint)
            org_sync.export_all_to_org()
            return 201, item

        if method == "GET" and path == "/api/opportunities":
            return 200, engine.list_opportunities()

        if method == "POST" and path == "/api/opportunities":
            req = OpportunityCreate(**body)
            opp = engine.create_opportunity(
                title=req.title,
                platform=req.platform,
                channel_type=req.channel_type,
                cluster=req.cluster,
                reward_brl=req.reward_brl,
                probability=req.probability,
                prep_hours=req.prep_hours,
                deadline=req.deadline,
                funding_category=req.funding_category,
                github_issue_url=req.github_issue_url,
            )
            org_sync.export_all_to_org()
            return 201, opp

        if method == "POST" and path == "/api/commerce/simulate":
            req = CommerceSimulateRequest(**body)
            return 200, engine.simulate_commerce_flow(
                customer_name=req.customer_name,
                message=req.message,
                sku=req.sku,
                quantity=req.quantity,
                requested_discount_pct=req.requested_discount_pct,
                org_id=req.org_id,
            )

        if method == "GET" and path == "/api/workflows":
            return 200, engine.list_workflows_and_agents()

        if method == "POST" and path == "/api/workflows/autonomy":
            req = WorkflowAutonomyUpdate(**body)
            return 200, engine.promote_workflow_autonomy(req.workflow_id, req.target_level)

        if method == "GET" and path == "/api/research":
            return 200, engine.get_research_and_publishing()

        if method == "GET" and path == "/api/docs":
            return 200, {"documents": engine.list_strategic_docs()}

        if method == "POST" and path == "/api/org/sync":
            res = org_sync.import_new_from_inbox_org()
            return 200, res

        if method == "GET" and path == "/api/traceability":
            return 200, engine.get_traceability_and_bounded_contexts()

        if method == "POST" and path == "/api/autonomy/calibrate":
            return 200, engine.compute_calibrated_autonomy(
                agent_id=body.get("agent_id", "agt:engineering"),
                task_risk=float(body.get("task_risk", 0.25)),
                calibrated_confidence=float(body.get("calibrated_confidence", 0.90)),
                evidences_count=int(body.get("evidences_count", 4)),
                permission_factor=float(body.get("permission_factor", 1.0)),
                high_stakes_domain=bool(body.get("high_stakes_domain", False)),
            )

        return 404, {"error": f"Endpoint {method} {path} not found"}
    except Exception as exc:
        return 400, {"error": str(exc)}


class EugenciaHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        pass

    def _send_json(self, status: int, payload: Any) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self) -> None:
        self._send_json(200, {"ok": True})

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            status, payload = dispatch_api_request("GET", parsed.path, parse_qs(parsed.query), {})
            self._send_json(status, payload)
            return

        # Serve static frontend files if built
        if FRONTEND_DIST.exists():
            rel = parsed.path.lstrip("/") or "index.html"
            target = (FRONTEND_DIST / rel).resolve()
            if not str(target).startswith(str(FRONTEND_DIST.resolve())) or not target.is_file():
                target = FRONTEND_DIST / "index.html"
            if target.is_file():
                ctype, _ = mimetypes.guess_type(str(target))
                data = target.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", ctype or "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return

        self._send_json(200, {"message": "Eugência OS API running. Visit /api/health or build frontend."})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            body = json.loads(raw_body) if raw_body.strip() else {}
        except json.JSONDecodeError:
            body = {}
        status, payload = dispatch_api_request("POST", parsed.path, parse_qs(parsed.query), body)
        self._send_json(status, payload)


def run_server(host: str = "127.0.0.1", port: int = 8765) -> None:
    httpd = ThreadingHTTPServer((host, port), EugenciaHTTPHandler)
    print(f"🧭 Eugência OS & ValueCurator OS Server running at http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
