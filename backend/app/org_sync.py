"""
Bidirectional Synchronization between Eugência OS SQLite state and Emacs Org-mode files.
Maintains the hybrid cockpit (Emacs/Org-mode + Web App) described in Part 2, Sections 8 & 11.
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, Any, List
from .engine import EugenciaEngine, BASE_DIR, now_iso

ORG_DIR = BASE_DIR / "org"


class OrgModeSynchronizer:
    def __init__(self, engine: EugenciaEngine, org_dir: Path = ORG_DIR):
        self.engine = engine
        self.org_dir = Path(org_dir)
        self.org_dir.mkdir(parents=True, exist_ok=True)

    def export_all_to_org(self) -> Dict[str, str]:
        """Exports SQLite operational state to structured Emacs Org-mode files."""
        files_written: Dict[str, str] = {}

        # 1. org/inbox.org (Flow Inbox: Divergence <-> Convergence)
        inbox_items = self.engine.list_flow_inbox()
        inbox_lines = [
            "#+TITLE: Eugência OS — Flow Inbox (Divergência <-> Convergência)",
            "#+AUTHOR: João Nitzsche (Compilatorum / ValueCurator)",
            f"#+DATE: {now_iso()}",
            "#+STARTUP: overview",
            "#+TODO: FLOW(f) CURATED(c) IN_EXECUTION(e) | PROMOTED(p) PARKED(k) DONE(d)",
            "",
            "* 🌱 Laboratório de Exploração (Divergência Criativa)",
        ]
        for item in inbox_items:
            if "Divergence" in item["space"]:
                state = "CURATED" if item["status"] == "curated" else "PARKED"
                inbox_lines.extend([
                    f"** {state} {item['content']}  :{item['suggested_cluster'].replace(' ', '_')}:",
                    "   :PROPERTIES:",
                    f"   :ID:       {item['id']}",
                    f"   :SOURCE:   {item['source']}",
                    f"   :TYPE:     {item['classified_type']}",
                    f"   :DEST:     {item['suggested_destination']}",
                    f"   :AGENT:    {item['assigned_agent']}",
                    f"   :CREATED:  {item['created_at']}",
                    "   :END:",
                ])

        inbox_lines.extend(["", "* ⚙️ Linha de Execução (Convergência em Entregas)"])
        for item in inbox_items:
            if "Convergence" in item["space"]:
                state = "IN_EXECUTION" if item["status"] == "in_execution" else "PROMOTED"
                inbox_lines.extend([
                    f"** {state} {item['content']}  :{item['suggested_cluster'].replace(' ', '_')}:",
                    "   :PROPERTIES:",
                    f"   :ID:       {item['id']}",
                    f"   :SOURCE:   {item['source']}",
                    f"   :TYPE:     {item['classified_type']}",
                    f"   :DEST:     {item['suggested_destination']}",
                    f"   :AGENT:    {item['assigned_agent']}",
                    f"   :CREATED:  {item['created_at']}",
                    "   :END:",
                ])

        inbox_path = self.org_dir / "inbox.org"
        inbox_path.write_text("\n".join(inbox_lines) + "\n", encoding="utf-8")
        files_written["inbox.org"] = str(inbox_path)

        # 2. org/opportunities.org (Opportunity Intelligence & Grant Stacking)
        opp_data = self.engine.list_opportunities()
        opp_lines = [
            "#+TITLE: Eugência OS — Opportunity Intelligence & GrantOS",
            f"#+DATE: {now_iso()}",
            "#+TODO: QUALIFIED(q) PREPARING(p) ACTIVE_PILOT(a) | SUBMITTED(s) WON(w) ARCHIVED(x)",
            "",
            "* 🎯 Oportunidades Qualificadas (Clientes B2B, Grants & Bounties)",
        ]
        for o in opp_data["opportunities"]:
            st = o["status"].upper()
            opp_lines.extend([
                f"** {st} {o['title']} (EV: R$ {o['expected_value_brl']:.0f} | R$ {o['ev_per_hour_brl']:.0f}/h)",
                f"   DEADLINE: <{o['deadline']}>",
                "   :PROPERTIES:",
                f"   :ID:               {o['id']}",
                f"   :PLATFORM:         {o['platform']}",
                f"   :CHANNEL:          {o['channel_type']}",
                f"   :CLUSTER:          {o['cluster']}",
                f"   :REWARD_BRL:       {o['reward_brl']}",
                f"   :PROBABILITY:      {o['probability']}",
                f"   :PREP_HOURS:       {o['prep_hours']}",
                f"   :FUNDING_CATEGORY: {o['funding_category']}",
                f"   :GITHUB_ISSUE:     {o['github_issue_url'] or ''}",
                "   :END:",
            ])

        opp_lines.extend(["", "* 🧩 Grant Stacking — Work Packages (ProofGate / ValueCurator)"])
        for wp in opp_data["grant_stacking_work_packages"]:
            opp_lines.extend([
                f"** TODO [{wp['wp_code']}] {wp['deliverable']} ({wp['funding_category']})",
                "   :PROPERTIES:",
                f"   :ID:       {wp['id']}",
                f"   :LICENSE:  {wp['license']}",
                f"   :FUNDER:   {wp['target_funder']}",
                f"   :AMOUNT:   R$ {wp['amount_brl']:.0f}",
                f"   :STATUS:   {wp['status']}",
                "   :END:",
            ])

        opp_path = self.org_dir / "opportunities.org"
        opp_path.write_text("\n".join(opp_lines) + "\n", encoding="utf-8")
        files_written["opportunities.org"] = str(opp_path)

        # 3. org/portfolio.org (72 Repositories classified by Priority & Cluster)
        assets = self.engine.get_portfolio_assets()
        kpis = self.engine.get_kpis()
        port_lines = [
            "#+TITLE: Eugência OS — Portfolio OS (72 Repositórios & KPIs)",
            f"#+DATE: {now_iso()}",
            "",
            "* 📊 Indicadores Executivos da Eugência (E = H + S + A + G)",
            f"- *Score da Eugência (E):* {kpis['eugencia_formula']['E_total_score']} / 100",
            f"- *MRR Atual:* R$ {kpis['commercial']['mrr_brl']:.2f} ({kpis['commercial']['paying_clients']} clientes ativos)",
            f"- *Margem de Contribuição (MC):* R$ {kpis['financial']['contribution_margin_brl']:.2f} ({kpis['financial']['contribution_margin_pct']}%)",
            f"- *Alavancagem Recorrente (L = MRR / Horas):* R$ {kpis['operational']['L_mrr_per_human_hour']:.2f} / hora humana",
            f"- *Eficiência Computacional (rho = MRR / C_var):* {kpis['financial']['rho_computational_efficiency']}x",
            f"- *Regra WIP Comercial <= 2:* {kpis['operational']['wip_comercial_count']}/2 ({', '.join(kpis['operational']['wip_active_repos'])})",
            "",
            "* 🏛️ Ativos por Prioridade e Cluster (72 Repositórios)",
        ]
        for prio in ["P0", "P1", "P2", "P3"]:
            p_assets = [a for a in assets if a["priority"] == prio]
            port_lines.append(f"** Prioridade {prio} ({len(p_assets)} repositórios)")
            for a in p_assets:
                wip_tag = " :WIP_ACTIVE:" if a["wip_active"] else ""
                port_lines.extend([
                    f"*** {a['full_name']} [{a['asset_class']}]{wip_tag}",
                    "    :PROPERTIES:",
                    f"    :CLUSTER:        {a['cluster']}",
                    f"    :STAGE:          {a['stage']}",
                    f"    :AUTONOMY:       {a['autonomy_level']}",
                    f"    :MONETIZATION:   {a['monetization']}",
                    f"    :NEXT_MILESTONE: {a['next_milestone']}",
                    "    :END:",
                    f"    - Potencial: {a['product_potential']}",
                    f"    - Governança IP: {a['ip_governance']}",
                ])

        port_path = self.org_dir / "portfolio.org"
        port_path.write_text("\n".join(port_lines) + "\n", encoding="utf-8")
        files_written["portfolio.org"] = str(port_path)

        # 4. org/experiments.org (Research & Experiment OS + Evidences)
        res = self.engine.get_research_and_publishing()
        exp_lines = [
            "#+TITLE: Eugência OS — Research & Experiment OS",
            f"#+SUBTITLE: {res['research_line']}",
            f"#+DATE: {now_iso()}",
            "",
            f"* 🔬 Questão Central\n{res['central_question']}",
            "",
            "* 🧪 Experimentos Ativos",
        ]
        for e in res["experiments"]:
            exp_lines.extend([
                f"** {e['status']} [{e['code']}] {e['title']} (Ergonomia = {e['ergonomics_index']})",
                "   :PROPERTIES:",
                f"   :ID:        {e['id']}",
                f"   :AXIS:      {e['research_axis']}",
                f"   :AUTONOMY:  {e['autonomy_score']}",
                f"   :DELTA_A:   {e['artifacts_delta_a']}",
                "   :END:",
                f"   - *Hipótese:* {e['hypothesis']}",
            ])

        exp_lines.extend(["", "* 🔒 Evidências Verificáveis (ProofGate SHA-256)"])
        for ev in res["evidences"]:
            exp_lines.extend([
                f"** VERIFIED [{ev['id']}] {ev['title']}",
                "   :PROPERTIES:",
                f"   :EXPERIMENT: {ev['experiment_id']}",
                f"   :PROJECT:    {ev['project_name']}",
                f"   :WP:         {ev['work_package']}",
                f"   :ARTIFACT:   {ev['artifact_uri']}",
                f"   :SHA256:     {ev['sha256_hash']}",
                "   :END:",
            ])

        exp_path = self.org_dir / "experiments.org"
        exp_path.write_text("\n".join(exp_lines) + "\n", encoding="utf-8")
        files_written["experiments.org"] = str(exp_path)

        return files_written

    def import_new_from_inbox_org(self) -> Dict[str, Any]:
        """
        Parses org/inbox.org for any new headings added in Emacs without an :ID: property
        and ingests them into the Flow Inbox database, then re-exports clean IDs.
        """
        inbox_path = self.org_dir / "inbox.org"
        if not inbox_path.exists():
            self.export_all_to_org()
            return {"imported_count": 0, "imported_items": []}

        lines = inbox_path.read_text(encoding="utf-8").splitlines()
        existing_contents = {i["content"].strip() for i in self.engine.list_flow_inbox()}
        imported: List[Dict[str, Any]] = []

        heading_pattern = re.compile(r"^\*\*\s+(?:FLOW|CURATED|IN_EXECUTION|PROMOTED|PARKED|TODO|DONE)?\s*(.+?)(?:\s+:[^\s:]+:)?$")
        for idx, line in enumerate(lines):
            m = heading_pattern.match(line.strip())
            if not m:
                continue
            title = m.group(1).strip()
            # Check if next lines have :ID:
            window = "\n".join(lines[idx + 1 : idx + 6])
            if ":ID:" not in window and title and title not in existing_contents:
                item = self.engine.add_flow_inbox_item(content=title, source="emacs-org")
                imported.append(item)
                existing_contents.add(title)

        files = self.export_all_to_org()
        return {"imported_count": len(imported), "imported_items": imported, "synced_files": files}
