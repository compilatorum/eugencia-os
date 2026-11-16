#!/usr/bin/env python3
"""
Eugência OS Command-Line Interface & Emacs Cockpit Bridge.
Usage:
  python3 scripts/eugencia_cli.py kpis
  python3 scripts/eugencia_cli.py capture "Nova ideia ou oportunidade..."
  python3 scripts/eugencia_cli.py sync-org
  python3 scripts/eugencia_cli.py route --task commerce_chat --min-quality 0.80
  python3 scripts/eugencia_cli.py proofgate --domain card-chat --discount 18
  python3 scripts/eugencia_cli.py simulate-commerce --sku TCG-PKM-151-BOX --qty 2 --discount 8
  python3 scripts/eugencia_cli.py serve --port 8765
"""
import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.engine import EugenciaEngine
from app.org_sync import OrgModeSynchronizer
from app.server import run_server


def main() -> None:
    parser = argparse.ArgumentParser(description="Eugência OS & ValueCurator OS CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("kpis", help="Exibe os KPIs executivos da Eugência (E = H + S + A + G, L, rho, MC, WIP)")

    p_cap = sub.add_parser("capture", help="Captura um item no Flow Inbox e sincroniza com org/inbox.org")
    p_cap.add_argument("content", help="Texto da ideia, hipótese, oportunidade ou tarefa")
    p_cap.add_argument("--source", default="cli", help="Fonte da captura (cli, emacs-org, whatsapp)")

    sub.add_parser("sync-org", help="Sincroniza bidirecionalmente os arquivos Emacs Org-mode (org/*.org)")

    p_route = sub.add_parser("route", help="Executa o roteamento ótimo M* no AI Gateway")
    p_route.add_argument("--task", default="commerce_chat")
    p_route.add_argument("--min-quality", type=float, default=0.80)
    p_route.add_argument("--lambda-latency", type=float, default=0.4)
    p_route.add_argument("--mu-risk", type=float, default=0.5)

    p_pg = sub.add_parser("proofgate", help="Avalia uma intenção no pipeline ProofGate")
    p_pg.add_argument("--domain", default="card-chat", choices=["card-chat", "grantos", "finance", "neurocoder", "farcaster"])
    p_pg.add_argument("--discount", type=float, default=8.0)

    p_sim = sub.add_parser("simulate-commerce", help="Simula o fluxo completo do Card-Chat AI Commerce Agent")
    p_sim.add_argument("--sku", default="TCG-PKM-151-BOX")
    p_sim.add_argument("--qty", type=int, default=2)
    p_sim.add_argument("--discount", type=float, default=8.0)

    p_srv = sub.add_parser("serve", help="Inicia o servidor HTTP/API e Cockpit Web")
    p_srv.add_argument("--host", default="127.0.0.1")
    p_srv.add_argument("--port", type=int, default=8765)

    args = parser.parse_args()
    engine = EugenciaEngine()
    sync = OrgModeSynchronizer(engine)

    if args.cmd == "kpis":
        k = engine.get_kpis()
        print(
            f"🧭 Eugência E={k['eugencia_formula']['E_total_score']} | "
            f"MRR=R$ {k['commercial']['mrr_brl']:.0f} ({k['commercial']['paying_clients']} clientes) | "
            f"MC=R$ {k['financial']['contribution_margin_brl']:.0f} ({k['financial']['contribution_margin_pct']}%) | "
            f"L=R$ {k['operational']['L_mrr_per_human_hour']:.1f}/h | "
            f"rho={k['financial']['rho_computational_efficiency']}x | "
            f"WIP={k['operational']['wip_comercial_count']}/2 ({', '.join(k['operational']['wip_active_repos'])}) | "
            f"Ergonomia={k['operational']['ergonomics_index']}"
        )
    elif args.cmd == "capture":
        item = engine.add_flow_inbox_item(args.content, source=args.source)
        sync.export_all_to_org()
        print(f"✅ Capturado [{item['id']}] -> {item['space']} | Agente: {item['assigned_agent']} | Destino: {item['suggested_destination']}")
    elif args.cmd == "sync-org":
        res = sync.import_new_from_inbox_org()
        print(f"🔄 Org-mode sincronizado ({res['imported_count']} novos itens importados de inbox.org; 4 arquivos .org atualizados)")
    elif args.cmd == "route":
        res = engine.route_and_execute_ai(
            task_type=args.task,
            prompt_preview=f"CLI route test for {args.task}",
            min_quality=args.min_quality,
            lambda_latency=args.lambda_latency,
            mu_risk=args.mu_risk,
            tokens_in=500,
            tokens_out=250,
            tools_invoked=["catalog_sql"],
            org_id="org:compilatorum",
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.cmd == "proofgate":
        res = engine.evaluate_proofgate_intent(
            domain=args.domain,
            agent_role="Engineering IA",
            action="cli_policy_check",
            payload={"discount_pct": args.discount, "verified_catalog": True, "stock_available": 10, "quantity": 1},
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.cmd == "simulate-commerce":
        res = engine.simulate_commerce_flow(
            customer_name="Cliente CLI",
            message=f"Pedido {args.qty}x {args.sku} com {args.discount}% de desconto",
            sku=args.sku,
            quantity=args.qty,
            requested_discount_pct=args.discount,
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.cmd == "serve":
        run_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
