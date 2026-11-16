#!/usr/bin/env python3
"""
Builds the production Web App / PWA Cockpit bundle in frontend/dist/index.html.
Pre-hydrates the bundle with the live SQLite/JSON state (all 72 GitHub repositories,
KPIs, SCADA graph nodes/edges, 7 agents, workflows, ProofGate receipts, Flow Inbox,
Opportunities, Grant Stacking WPs, Experiments, and the 9 Strategic Markdown Documents)
AND connects dynamically to the FastAPI/HTTP backend at /api/* when served via HTTP.
"""
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.engine import EugenciaEngine
from app.org_sync import OrgModeSynchronizer


def build_bundle() -> None:
    engine = EugenciaEngine()
    sync = OrgModeSynchronizer(engine)
    sync.export_all_to_org()

    initial_state = {
        "kpis": engine.get_kpis(),
        "assets": engine.get_portfolio_assets(),
        "graph": engine.get_scada_graph(include_archived=False),
        "workflows_data": engine.list_workflows_and_agents(),
        "receipts": engine.list_proofgate_receipts(),
        "inbox": engine.list_flow_inbox(),
        "opportunities_data": engine.list_opportunities(),
        "research": engine.get_research_and_publishing(),
        "docs": engine.list_strategic_docs(),
    }

    state_json = json.dumps(initial_state, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Eugência OS & ValueCurator OS — SCADA Cockpit</title>
  <link rel="manifest" href="/manifest.json" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.30.2/cytoscape.min.js"></script>
  <style>
    :root {{
      --bg-0: #050911;
      --bg-1: #0b1322;
      --bg-2: #111d33;
      --bg-3: #192947;
      --border: #23385e;
      --text-0: #f1f5f9;
      --text-1: #cbd5e1;
      --text-2: #94a3b8;
      --emerald: #10b981;
      --cyan: #06b6d4;
      --purple: #8b5cf6;
      --amber: #f59e0b;
      --rose: #f43f5e;
      --blue: #3b82f6;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace;
      background: radial-gradient(circle at top right, #0f1b33 0%, var(--bg-0) 65%);
      color: var(--text-0);
      min-height: 100vh;
      line-height: 1.5;
    }}
    header {{
      background: rgba(11, 19, 34, 0.92);
      border-bottom: 1px solid var(--border);
      padding: 14px 24px;
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(10px);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-icon {{
      width: 42px;
      height: 42px;
      border-radius: 10px;
      background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(6,182,212,0.25));
      border: 1px solid var(--emerald);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      box-shadow: 0 0 18px rgba(16,185,129,0.25);
    }}
    .brand h1 {{
      font-size: 18px;
      font-weight: 700;
      letter-spacing: 0.3px;
      color: #fff;
    }}
    .brand p {{
      font-size: 12px;
      color: var(--text-2);
    }}
    .formula-pill {{
      background: rgba(139, 92, 246, 0.14);
      border: 1px solid rgba(139, 92, 246, 0.45);
      color: #ddd6fe;
      padding: 6px 12px;
      border-radius: 999px;
      font-size: 12px;
      font-family: monospace;
    }}
    .nav-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      padding: 12px 24px;
      background: var(--bg-1);
      border-bottom: 1px solid var(--border);
    }}
    .tab-btn {{
      background: var(--bg-2);
      color: var(--text-1);
      border: 1px solid var(--border);
      padding: 8px 15px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 13px;
      font-weight: 600;
      transition: all 0.15s ease;
    }}
    .tab-btn:hover {{
      border-color: var(--cyan);
      color: #fff;
    }}
    .tab-btn.active {{
      background: linear-gradient(135deg, rgba(16,185,129,0.22), rgba(6,182,212,0.22));
      border-color: var(--emerald);
      color: #fff;
      box-shadow: 0 0 14px rgba(16,185,129,0.25);
    }}
    main {{
      max-width: 1560px;
      margin: 0 auto;
      padding: 20px 24px 60px;
    }}
    .kpi-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}
    .kpi-card {{
      background: var(--bg-1);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 16px;
      position: relative;
      overflow: hidden;
    }}
    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; width: 4px; height: 100%;
      background: var(--emerald);
    }}
    .kpi-card.cyan::before {{ background: var(--cyan); }}
    .kpi-card.purple::before {{ background: var(--purple); }}
    .kpi-card.amber::before {{ background: var(--amber); }}
    .kpi-label {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: var(--text-2);
    }}
    .kpi-val {{
      font-size: 22px;
      font-weight: 700;
      margin: 4px 0;
      color: #fff;
    }}
    .kpi-sub {{
      font-size: 11.5px;
      color: var(--text-2);
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1.35fr 1fr;
      gap: 18px;
    }}
    .grid-equal {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }}
    @media (max-width: 1024px) {{
      .grid-2, .grid-equal {{ grid-template-columns: 1fr; }}
    }}
    .panel {{
      background: var(--bg-1);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 18px;
      margin-bottom: 18px;
    }}
    .panel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px solid rgba(35, 56, 94, 0.6);
      flex-wrap: wrap;
      gap: 8px;
    }}
    .panel-title {{
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    #cy-graph {{
      width: 100%;
      height: 500px;
      background: #060b15;
      border: 1px solid var(--border);
      border-radius: 10px;
    }}
    .badge {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      font-family: monospace;
    }}
    .badge-p0, .badge-emerald {{ background: rgba(16,185,129,0.18); color: #34d399; border: 1px solid rgba(16,185,129,0.4); }}
    .badge-p1, .badge-cyan {{ background: rgba(6,182,212,0.18); color: #22d3ee; border: 1px solid rgba(6,182,212,0.4); }}
    .badge-p2, .badge-purple {{ background: rgba(139,92,246,0.18); color: #c4b5fd; border: 1px solid rgba(139,92,246,0.4); }}
    .badge-p3, .badge-amber {{ background: rgba(245,158,11,0.16); color: #fbbf24; border: 1px solid rgba(245,158,11,0.4); }}
    .badge-rose {{ background: rgba(244,63,94,0.18); color: #fda4af; border: 1px solid rgba(244,63,94,0.4); }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12.5px;
    }}
    th, td {{
      text-align: left;
      padding: 9px 10px;
      border-bottom: 1px solid rgba(35, 56, 94, 0.5);
      vertical-align: top;
    }}
    th {{
      color: var(--text-2);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 11px;
      background: rgba(17, 29, 51, 0.6);
    }}
    tr:hover td {{
      background: rgba(25, 41, 71, 0.35);
    }}
    input, select, textarea {{
      background: var(--bg-0);
      border: 1px solid var(--border);
      color: var(--text-0);
      padding: 8px 11px;
      border-radius: 7px;
      font-size: 13px;
      width: 100%;
    }}
    button.btn-primary {{
      background: linear-gradient(135deg, #10b981, #059669);
      color: #fff;
      border: none;
      padding: 9px 16px;
      border-radius: 7px;
      font-weight: 600;
      cursor: pointer;
      font-size: 13px;
    }}
    button.btn-secondary {{
      background: var(--bg-2);
      color: var(--text-0);
      border: 1px solid var(--cyan);
      padding: 7px 13px;
      border-radius: 7px;
      font-weight: 600;
      cursor: pointer;
      font-size: 12px;
    }}
    .form-row {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 10px;
      margin-bottom: 12px;
    }}
    .code-box {{
      background: #040810;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      font-family: monospace;
      font-size: 12px;
      white-space: pre-wrap;
      color: #a7f3d0;
      max-height: 420px;
      overflow-y: auto;
    }}
    .hidden {{ display: none !important; }}
    .filter-bar {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }}
    .filter-bar > * {{ width: auto; min-width: 160px; }}
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="brand-icon">🧭</div>
      <div>
        <h1>EUGÊNCIA OS & VALUECURATOR OS</h1>
        <p>Compilatorum Holding · Selfware · Service-as-a-Software · ProofGate · Web3</p>
      </div>
    </div>
    <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
      <span class="formula-pill">E = H + S + A + G</span>
      <span class="formula-pill">VOS = I + B + AI + M + T + O + G</span>
      <span class="formula-pill">WIP_comercial &le; 2</span>
      <button class="btn-secondary" onclick="syncOrgMode()">🔄 Sync Emacs Org-Mode</button>
    </div>
  </header>

  <nav class="nav-tabs">
    <button class="tab-btn active" onclick="switchTab('scada', this)">📊 1. Portfolio OS & Grafo SCADA (72 Repos)</button>
    <button class="tab-btn" onclick="switchTab('flow', this)">🌊 2. Flow Inbox & Equipe Humano-IA (L0–L4)</button>
    <button class="tab-btn" onclick="switchTab('vos', this)">🛡️ 3. ValueCurator OS: AI Gateway (M*) & ProofGate</button>
    <button class="tab-btn" onclick="switchTab('commerce', this)">🛒 4. Motor 1: Card-Chat (AI Commerce Agent)</button>
    <button class="tab-btn" onclick="switchTab('grantos', this)">🌱 5. GrantOS, Oportunidades & Modelo de Receita</button>
    <button class="tab-btn" onclick="switchTab('docs', this)">📚 6. Research OS, Build in Public & 9 Artefatos .MD</button>
  </nav>

  <main>
    <!-- Global KPI Strip -->
    <section class="kpi-strip" id="kpi-strip"></section>

    <!-- TAB 1: SCADA Portfolio OS -->
    <section id="tab-scada" class="tab-section">
      <div class="grid-2">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">🕸️ Grafo SCADA — Software Industry 5.0 (Cytoscape.js)</div>
            <div style="display:flex; gap:6px;">
              <button class="btn-secondary" onclick="renderGraph(false)">Ativos Foco (Sem Archive)</button>
              <button class="btn-secondary" onclick="renderGraph(true)">Todos os 72 Repos</button>
            </div>
          </div>
          <div id="cy-graph"></div>
          <p style="font-size:11.5px; color:var(--text-2); margin-top:8px;">
            💡 Clique em qualquer nó do grafo (Holding, Cluster, Repositório, Produto ou Cliente) para inspecionar dependências, estágio, classe A–F e modelo de monetização.
          </p>
        </div>
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">🔍 Inspetor de Nó & Governança de Ativo</div>
          </div>
          <div id="node-inspector" class="code-box" style="min-height:240px;">Selecione um nó no grafo SCADA ao lado...</div>
          <div style="margin-top:14px;">
            <div class="panel-title" style="margin-bottom:8px;">⚖️ Regra de Foco Comercial (WIP &le; 2)</div>
            <div id="wip-box" class="code-box" style="color:#fde68a;"></div>
          </div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">🗂️ Registro Geral de Ativos Digitais (PORTFOLIO-ASSETS-REGISTER — 72 Repositórios)</div>
          <div class="filter-bar">
            <input type="text" id="repo-search" placeholder="Filtrar por nome ou descrição..." oninput="renderRepoTable()" />
            <select id="repo-cluster" onchange="renderRepoTable()">
              <option value="">Todos os 6 Clusters</option>
              <option value="ValueCurator">ValueCurator</option>
              <option value="NeuroCoder">NeuroCoder</option>
              <option value="GrantOS">GrantOS</option>
              <option value="Capital Intelligence">Capital Intelligence</option>
              <option value="GeoIA">GeoIA</option>
              <option value="AROS">AROS</option>
            </select>
            <select id="repo-class" onchange="renderRepoTable()">
              <option value="">Todas as Classes (A–F)</option>
              <option value="A — Core IP">A — Core IP</option>
              <option value="B — Open Core">B — Open Core</option>
              <option value="C — Commercial">C — Commercial</option>
              <option value="D — Internal Tool">D — Internal Tool</option>
              <option value="E — Research">E — Research</option>
              <option value="F — Archive">F — Archive</option>
            </select>
            <select id="repo-owner" onchange="renderRepoTable()">
              <option value="">Todos os Espaços GitHub</option>
              <option value="compilatorum">compilatorum (59)</option>
              <option value="smp-sandramariapereira">smp-sandramariapereira (13)</option>
            </select>
          </div>
        </div>
        <div style="overflow-x:auto; max-height:480px; overflow-y:auto;">
          <table>
            <thead>
              <tr>
                <th>Repositório</th>
                <th>Cluster</th>
                <th>Stage</th>
                <th>Classe A–F</th>
                <th>Prioridade</th>
                <th>Próximo Milestone</th>
                <th>Monetização & IP</th>
              </tr>
            </thead>
            <tbody id="repo-tbody"></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- TAB 2: Flow Inbox & Human-AI Team -->
    <section id="tab-flow" class="tab-section hidden">
      <div class="grid-2">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">📥 Flow Inbox Universal (Divergência &harr; Convergência)</div>
          </div>
          <p style="font-size:12.5px; color:var(--text-2); margin-bottom:12px;">
            Capture ideias, hipóteses, problemas de clientes ou oportunidades sem interromper seu estado de flow. O Chief of Staff IA classifica automaticamente entre <b>Laboratório de Exploração</b> e <b>Linha de Execução</b> e sincroniza com <code>~/eugencia-os/org/inbox.org</code>.
          </p>
          <div class="form-row">
            <input type="text" id="flow-input" placeholder="Ex: Criar adaptador Pyth Oracle para o ProofGate ou explorar hipótese de grafo Farcaster..." />
            <select id="flow-source" style="max-width:180px;">
              <option value="cockpit">Web Cockpit</option>
              <option value="emacs-org">Emacs Org-mode</option>
              <option value="whatsapp">WhatsApp</option>
              <option value="github">GitHub Issue</option>
            </select>
            <button class="btn-primary" onclick="submitFlowInbox()">+ Capturar no Flow</button>
          </div>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Conteúdo Capturado</th>
                <th>Espaço (Flow vs Execução)</th>
                <th>Cluster & Destino</th>
                <th>Agente Responsável</th>
              </tr>
            </thead>
            <tbody id="flow-tbody"></tbody>
          </table>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">🤖 Equipe Operacional Humano-IA (7 Papéis Especializados)</div>
          </div>
          <table>
            <thead>
              <tr>
                <th>Agente</th>
                <th>Responsabilidade</th>
                <th>Autonomia</th>
                <th>Modelo Padrão</th>
              </tr>
            </thead>
            <tbody id="agents-tbody"></tbody>
          </table>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">🎚️ Autonomia Progressiva dos Workflows (L0 Manual &rarr; L4 Autonomous)</div>
          <span class="formula-pill">L_{{n+1}} &Leftarrow; Testes &and; Evidências &and; Controles</span>
        </div>
        <table>
          <thead>
            <tr>
              <th>Workflow</th>
              <th>Domínio ProofGate</th>
              <th>Nível Atual</th>
              <th>Testes Aprovados</th>
              <th>Evidências</th>
              <th>Pipeline de Execução</th>
              <th>Promover Autonomia</th>
            </tr>
          </thead>
          <tbody id="workflows-tbody"></tbody>
        </table>
        <div id="autonomy-feedback" style="margin-top:10px; font-size:12.5px; color:#34d399;"></div>
      </div>
    </section>

    <!-- TAB 3: ValueCurator OS (AI Gateway & ProofGate) -->
    <section id="tab-vos" class="tab-section hidden">
      <div class="grid-equal">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">⚡ Camada 3: AI Gateway — Roteador Ótimo de Modelos (M*)</div>
            <span class="formula-pill">M* = argmin [C(m) + &lambda;L(m) + &mu;R(m)] s.t. Q(m) &ge; Q_min</span>
          </div>
          <div class="form-row">
            <div>
              <label style="font-size:11px; color:var(--text-2);">Tarefa (task_type)</label>
              <select id="gw-task">
                <option value="commerce_chat">Atendimento Card-Chat (WhatsApp)</option>
                <option value="code_review">Engenharia / Harness Code Review</option>
                <option value="policy_audit">Auditoria Crítica ProofGate</option>
                <option value="grant_analysis">Triagem de Edital GrantOS</option>
              </select>
            </div>
            <div>
              <label style="font-size:11px; color:var(--text-2);">Qualidade Mínima (Q_min: 0.70–0.96)</label>
              <input type="number" id="gw-qmin" value="0.80" step="0.05" min="0.50" max="0.97" />
            </div>
            <div>
              <label style="font-size:11px; color:var(--text-2);">Peso Latência (&lambda;)</label>
              <input type="number" id="gw-lambda" value="0.5" step="0.1" />
            </div>
            <div>
              <label style="font-size:11px; color:var(--text-2);">Peso Risco (&mu;)</label>
              <input type="number" id="gw-mu" value="0.6" step="0.1" />
            </div>
          </div>
          <div class="form-row">
            <div>
              <label style="font-size:11px; color:var(--text-2);">Tokens Entrada / Saída</label>
              <input type="number" id="gw-tokens" value="800" step="100" />
            </div>
            <div>
              <label style="font-size:11px; color:var(--text-2);">Organização Multi-Tenant</label>
              <select id="gw-org">
                <option value="org:vespa-tcg">Vespa TCG (Starter - 500 créd.)</option>
                <option value="org:collector-bh">Arena Colecionáveis (Pro - 2.000 créd.)</option>
                <option value="org:solana-dao-pilot">Solana Treasury DAO (Business - 10.000 créd.)</option>
              </select>
            </div>
            <div style="display:flex; align-items:flex-end;">
              <button class="btn-primary" style="width:100%;" onclick="runAiGateway()">Executar Roteamento M*</button>
            </div>
          </div>
          <div id="gw-result" class="code-box">Clique em "Executar Roteamento M*" para calcular o modelo ótimo e debitar créditos normalizados...</div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">🛡️ Camada 7: ProofGate — Validação Determinística & Receipts</div>
            <span class="formula-pill">Intent &rarr; Policy &rarr; Validation &rarr; Approval &rarr; Execution &rarr; Receipt</span>
          </div>
          <div class="form-row">
            <div>
              <label style="font-size:11px; color:var(--text-2);">Domínio de Política</label>
              <select id="pg-domain" onchange="updatePgPreset()">
                <option value="card-chat">card-chat (Limite de Desconto & Estoque)</option>
                <option value="finance">finance (Mandato DeFi & Buffer Soberano &ge; 1.20x)</option>
                <option value="grantos">grantos (Anti-Dupla-Cobrança de Work Package)</option>
                <option value="neurocoder">neurocoder (Proteção de Deploy & Testes Limpos)</option>
                <option value="farcaster">farcaster (Publicação Exige Evidência SHA-256)</option>
              </select>
            </div>
            <div>
              <label style="font-size:11px; color:var(--text-2);">Ação Proposta pela IA</label>
              <input type="text" id="pg-action" value="apply_discount" />
            </div>
          </div>
          <div style="margin-bottom:10px;">
            <label style="font-size:11px; color:var(--text-2);">Payload JSON da Intenção</label>
            <textarea id="pg-payload" rows="4">{{"sku": "TCG-PKM-151-BOX", "quantity": 2, "stock_available": 14, "discount_pct": 16.0, "verified_catalog": true}}</textarea>
          </div>
          <button class="btn-primary" onclick="evaluateProofGate()">Submeter Intenção ao ProofGate</button>
          <div id="pg-eval-output" class="code-box" style="margin-top:10px;"></div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">📜 Livro-Razão de Recibos Criptográficos ProofGate (Auditoria & Aprovação Humana HITL)</div>
        </div>
        <table>
          <thead>
            <tr>
              <th>Receipt ID</th>
              <th>Domínio & Ação</th>
              <th>Status da Política</th>
              <th>Razões de Validação</th>
              <th>Aprovação</th>
              <th>Execução</th>
              <th>SHA-256 Hash</th>
              <th>Ação Humana</th>
            </tr>
          </thead>
          <tbody id="receipts-tbody"></tbody>
        </table>
      </div>
    </section>

    <!-- TAB 4: Motor 1 - Card-Chat AI Commerce Agent -->
    <section id="tab-commerce" class="tab-section hidden">
      <div class="grid-2">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">🛒 Simulador Operacional: AI Commerce Agent (Card-Chat / Vespa TCG)</div>
            <span class="formula-pill">WhatsApp &rarr; Agent &rarr; Catalog &rarr; Recommendation &rarr; Checkout &rarr; HumanHandoff</span>
          </div>
          <p style="font-size:12.5px; color:var(--text-2); margin-bottom:12px;">
            Teste o primeiro produto comercial (Motor 1 de receita imediata). O agente não inventa preços nem estoque, utiliza o AI Gateway e submete descontos ao ProofGate antes de emitir o link PIX do MercadoPago.
          </p>
          <div class="form-row">
            <div>
              <label style="font-size:11px; color:var(--text-2);">Cliente WhatsApp</label>
              <input type="text" id="cm-customer" value="Lucas (Colecionador BH)" />
            </div>
            <div>
              <label style="font-size:11px; color:var(--text-2);">Produto do Catálogo Vespa TCG</label>
              <select id="cm-sku">
                <option value="TCG-PKM-151-BOX">Booster Box Pokémon 151 (R$ 420 | Est: 14)</option>
                <option value="TCG-MTG-LOTR-COLLECTOR">MTG Tales of Middle-earth Collector Box (R$ 1.890 | Est: 4)</option>
                <option value="TCG-YGO-RA02-BOX">Yu-Gi-Oh! Rarity Collection II Box (R$ 540 | Est: 9)</option>
                <option value="TCG-OP-OP05-BOX">One Piece OP-05 Booster Box (R$ 690 | Est: 6)</option>
                <option value="SKU-ALUCINADO-999">SKU Inexistente (Testar Bloqueio de Alucinação)</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div>
              <label style="font-size:11px; color:var(--text-2);">Quantidade</label>
              <input type="number" id="cm-qty" value="2" min="1" max="50" />
            </div>
            <div>
              <label style="font-size:11px; color:var(--text-2);">Desconto Solicitado (%) — [&le;10% Auto | 10–25% HITL | &gt;25% Bloqueado]</label>
              <input type="number" id="cm-discount" value="8.0" step="1" min="0" max="60" />
            </div>
          </div>
          <div style="margin-bottom:12px;">
            <label style="font-size:11px; color:var(--text-2);">Mensagem Recebida no WhatsApp Business API</label>
            <input type="text" id="cm-msg" value="Oi! Quero fechar 2 Booster Box Pokémon 151 no PIX com 8% de desconto e entrega em BH." />
          </div>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <button class="btn-primary" onclick="runCommerceSim(8.0)">Cenário 1: Venda Automática (8% desc.)</button>
            <button class="btn-secondary" onclick="runCommerceSim(18.0)">Cenário 2: Retenção p/ Gerente (18% desc.)</button>
            <button class="btn-secondary" onclick="runCommerceSim(35.0)">Cenário 3: Ataque Prompt Injection (35% desc.)</button>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">📲 Telemetria do Fluxo Comercial & Guardrail ProofGate</div>
          </div>
          <div id="cm-output" class="code-box" style="min-height:310px;">Execute um dos cenários ao lado para inspecionar o pipeline ponta a ponta...</div>
        </div>
      </div>
    </section>

    <!-- TAB 5: GrantOS, Opportunities & Revenue Model -->
    <section id="tab-grantos" class="tab-section hidden">
      <div class="grid-2">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">🎯 Opportunity Intelligence CRM (Superteam, Gitcoin, Dework/GitHub & Clientes B2B)</div>
            <span class="formula-pill">Project &rarr; FundingThesis &rarr; Opportunity &rarr; WorkPackage &rarr; Evidence &rarr; Funding</span>
          </div>
          <table>
            <thead>
              <tr>
                <th>Oportunidade</th>
                <th>Canal / Plataforma</th>
                <th>Recompensa</th>
                <th>Prob.</th>
                <th>EV (R$)</th>
                <th>EV / Hora</th>
                <th>Categoria GrantOS</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="opps-tbody"></tbody>
          </table>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">🧩 Grant Stacking Matrix — Decomposição sem Dupla Cobrança (ProofGate WP1–WP5)</div>
          </div>
          <p style="font-size:12px; color:var(--text-2); margin-bottom:10px;">
            O grant financia a externalidade positiva (SDK aberto, testes adversariais e adaptadores Solana); o cliente comercial paga pelo benefício privado (API hospedada multi-tenant e Dashboard).
          </p>
          <table>
            <thead>
              <tr>
                <th>WP</th>
                <th>Entregável Delimitado</th>
                <th>Categoria Exclusiva</th>
                <th>Licença</th>
                <th>Financiador Alvo</th>
              </tr>
            </thead>
            <tbody id="wps-tbody"></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- TAB 6: Research OS, Build in Public & 9 Strategic Docs -->
    <section id="tab-docs" class="tab-section hidden">
      <div class="grid-2">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">🔬 Research & Experiment OS + Evidências SHA-256</div>
            <span class="formula-pill">Ergonomia = (Valor &times; Autonomia) / (Esforço + Atrito + Sobrecarga)</span>
          </div>
          <table>
            <thead>
              <tr>
                <th>Código</th>
                <th>Experimento</th>
                <th>Status</th>
                <th>Ergonomia</th>
                <th>Ativo Reutilizável Gerado (&Delta;A_t &gt; 0)</th>
              </tr>
            </thead>
            <tbody id="exps-tbody"></tbody>
          </table>
          <div style="margin-top:14px;">
            <div class="panel-title" style="margin-bottom:8px;">📣 Reputation & Publishing OS — Radar Semanal Derivado de Evidências Reais</div>
            <div id="radar-preview" class="code-box"></div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">📚 Artefatos Estratégicos EUGENCIA-OS (9 Documentos Operacionais)</div>
            <select id="doc-selector" onchange="renderSelectedDoc()" style="max-width:320px;"></select>
          </div>
          <div id="doc-viewer" class="code-box" style="min-height:420px; color:#e2e8f0;"></div>
        </div>
      </div>
    </section>
  </main>

  <script>
    window.__INITIAL_STATE__ = {state_json};
    let STATE = window.__INITIAL_STATE__;
    let cyInstance = null;

    async function apiCall(path, method = 'GET', body = null) {{
      try {{
        const opts = {{ method, headers: {{ 'Content-Type': 'application/json' }} }};
        if (body) opts.body = JSON.stringify(body);
        const res = await fetch(path, opts);
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return await res.json();
      }} catch (err) {{
        console.warn('Offline/Static mode fallback for', path, err);
        return null;
      }}
    }}

    function switchTab(tabId, btn) {{
      document.querySelectorAll('.tab-section').forEach(el => el.classList.add('hidden'));
      document.getElementById('tab-' + tabId).classList.remove('hidden');
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      if (tabId === 'scada' && cyInstance) {{
        setTimeout(() => cyInstance.resize(), 50);
      }}
    }}

    function renderKpis() {{
      const k = STATE.kpis;
      const strip = document.getElementById('kpi-strip');
      strip.innerHTML = `
        <div class="kpi-card">
          <div class="kpi-label">Fórmula da Eugência (E = H+S+A+G)</div>
          <div class="kpi-val">${{k.eugencia_formula.E_total_score}} / 100</div>
          <div class="kpi-sub">H:${{k.eugencia_formula.H_human_capital}} · S:${{k.eugencia_formula.S_selfware_ip}} · A:${{k.eugencia_formula.A_agent_runtime}} · G:${{k.eugencia_formula.G_governance_proofgate}}</div>
        </div>
        <div class="kpi-card cyan">
          <div class="kpi-label">MRR & Clientes Ativos</div>
          <div class="kpi-val">R$ ${{k.commercial.mrr_brl.toLocaleString('pt-BR')}}</div>
          <div class="kpi-sub">${{k.commercial.paying_clients}} clientes · Total faturado: R$ ${{k.commercial.total_billed_brl.toLocaleString('pt-BR')}}</div>
        </div>
        <div class="kpi-card purple">
          <div class="kpi-label">Margem de Contribuição (MC)</div>
          <div class="kpi-val">R$ ${{k.financial.contribution_margin_brl.toLocaleString('pt-BR')}} (${{k.financial.contribution_margin_pct}}%)</div>
          <div class="kpi-sub">Eficiência &rho; = ${{k.financial.rho_computational_efficiency}}x sobre custos variáveis</div>
        </div>
        <div class="kpi-card amber">
          <div class="kpi-label">Alavancagem (L = MRR / Horas)</div>
          <div class="kpi-val">R$ ${{k.operational.L_mrr_per_human_hour}} / h</div>
          <div class="kpi-sub">Alavancagem Global: R$ ${{k.operational.eugencia_leverage_ratio}}/h · Ergonomia: ${{k.operational.ergonomics_index}}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Portfólio Auditado & ProofGate</div>
          <div class="kpi-val">${{k.engineering_and_governance.total_repositories}} Repos</div>
          <div class="kpi-sub">${{k.engineering_and_governance.compilatorum_repos}} compilatorum + ${{k.engineering_and_governance.shared_sandra_repos}} Sandra · ${{k.engineering_and_governance.tests_passing_total}} testes</div>
        </div>
        <div class="kpi-card cyan">
          <div class="kpi-label">Pipeline GrantOS (EV Ponderado)</div>
          <div class="kpi-val">R$ ${{k.grants_and_capital.pipeline_expected_value_brl.toLocaleString('pt-BR')}}</div>
          <div class="kpi-sub">${{k.grants_and_capital.qualified_opportunities}} oportunidades qualificadas</div>
        </div>
      `;

      document.getElementById('wip-box').textContent =
        `Status WIP Comercial: ${{k.operational.wip_comercial_count}} / ${{k.operational.wip_comercial_limit}} ` +
        `(${{k.operational.wip_compliant ? '✅ CONFORME REGRA WIP <= 2' : '⚠️ VIOLAÇÃO WIP'}})\n` +
        `Motores Comerciais Ativos: ${{k.operational.wip_active_repos.join(' + ')}}\n` +
        `Motor Interno P0: harness-engineering + emacs + omni-dual-brain`;
    }}

    async function renderGraph(includeArchived = false) {{
      if (includeArchived) {{
        const fresh = await apiCall('/api/portfolio/graph?include_archived=true');
        if (fresh) STATE.graph = fresh;
      }} else {{
        const fresh = await apiCall('/api/portfolio/graph?include_archived=false');
        if (fresh) STATE.graph = fresh;
      }}

      const container = document.getElementById('cy-graph');
      if (typeof cytoscape === 'undefined') {{
        container.innerHTML = '<div style="padding:20px; color:#94a3b8;">Grafo SCADA carregado em modo tabular (' + STATE.graph.nodes.length + ' nós e ' + STATE.graph.edges.length + ' conexões).</div>';
        return;
      }}

      const elements = [...STATE.graph.nodes, ...STATE.graph.edges];
      cyInstance = window.cyInstance = cytoscape({{
        container,
        elements,
        style: [
          {{
            selector: 'node',
            style: {{
              'label': 'data(label)',
              'color': '#f8fafc',
              'font-size': '10px',
              'text-wrap': 'wrap',
              'text-max-width': '110px',
              'text-valign': 'bottom',
              'text-margin-y': 5,
              'background-color': '#3b82f6',
              'border-width': 2,
              'border-color': '#93c5fd',
              'width': 28,
              'height': 28
            }}
          }},
          {{
            selector: 'node[type = "holding"]',
            style: {{ 'background-color': '#10b981', 'border-color': '#a7f3d0', 'width': 48, 'height': 48, 'font-weight': 'bold', 'font-size': '12px' }}
          }},
          {{
            selector: 'node[type = "cluster"]',
            style: {{ 'background-color': '#8b5cf6', 'border-color': '#ddd6fe', 'width': 38, 'height': 38, 'font-weight': 'bold' }}
          }},
          {{
            selector: 'node[type = "product"]',
            style: {{ 'background-color': '#f59e0b', 'border-color': '#fde68a', 'shape': 'round-rectangle', 'width': 40, 'height': 30 }}
          }},
          {{
            selector: 'node[type = "client"]',
            style: {{ 'background-color': '#06b6d4', 'border-color': '#cffafe', 'shape': 'diamond', 'width': 36, 'height': 36 }}
          }},
          {{
            selector: 'node[?wip_active]',
            style: {{ 'border-width': 4, 'border-color': '#10b981', 'background-color': '#059669' }}
          }},
          {{
            selector: 'edge',
            style: {{
              'width': 1.5,
              'line-color': '#334155',
              'target-arrow-color': '#475569',
              'target-arrow-shape': 'triangle',
              'curve-style': 'bezier'
            }}
          }}
        ],
        layout: {{ name: 'cose', padding: 30, animate: false }}
      }});

      cyInstance.on('tap', 'node', function(evt) {{
        const d = evt.target.data();
        document.getElementById('node-inspector').textContent = JSON.stringify(d, null, 2);
      }});
    }}

    function renderRepoTable() {{
      const q = (document.getElementById('repo-search').value || '').toLowerCase();
      const cl = document.getElementById('repo-cluster').value;
      const ac = document.getElementById('repo-class').value;
      const ow = document.getElementById('repo-owner').value;

      const filtered = STATE.assets.filter(a => {{
        if (cl && a.cluster !== cl) return false;
        if (ac && a.asset_class !== ac) return false;
        if (ow && a.owner !== ow) return false;
        if (q && !(a.full_name.toLowerCase().includes(q) || (a.description || '').toLowerCase().includes(q) || a.product_potential.toLowerCase().includes(q))) return false;
        return true;
      }});

      const tbody = document.getElementById('repo-tbody');
      tbody.innerHTML = filtered.map(a => `
        <tr>
          <td>
            <a href="${{a.html_url}}" target="_blank" style="color:#38bdf8; font-weight:600; text-decoration:none;">${{a.full_name}}</a>
            ${{a.wip_active ? '<span class="badge badge-emerald">WIP ATIVO</span>' : ''}}
            <div style="font-size:11px; color:var(--text-2);">${{a.language}} · ${{a.private ? '🔒 Private' : '🌐 Public'}}</div>
          </td>
          <td><b>${{a.cluster}}</b><br/><span style="font-size:11px; color:var(--text-2);">${{a.commercial_unit}}</span></td>
          <td><span class="badge badge-cyan">${{a.stage}}</span></td>
          <td><span class="badge badge-purple">${{a.asset_class}}</span></td>
          <td><span class="badge badge-${{a.priority.toLowerCase()}}">${{a.priority}}</span></td>
          <td>${{a.next_milestone}}</td>
          <td>
            <div>${{a.monetization}}</div>
            <div style="font-size:10.5px; color:var(--text-2); margin-top:3px;">${{a.owner === 'smp-sandramariapereira' ? '⚠️ Espaço compartilhado Sandra (verificar IP)' : '✅ Holding Compilatorum'}}</div>
          </td>
        </tr>
      `).join('');
    }}

    function renderFlowAndAgents() {{
      const ftbody = document.getElementById('flow-tbody');
      ftbody.innerHTML = STATE.inbox.map(i => `
        <tr>
          <td><code>${{i.id}}</code></td>
          <td><b>${{i.content}}</b><br/><span style="font-size:11px; color:var(--text-2);">Fonte: ${{i.source}} · ${{i.created_at}}</span></td>
          <td><span class="badge ${{i.space.includes('Convergence') ? 'badge-emerald' : 'badge-purple'}}">${{i.space}}</span></td>
          <td><b>${{i.suggested_cluster}}</b> &rarr; ${{i.suggested_destination}}</td>
          <td>${{i.assigned_agent}}</td>
        </tr>
      `).join('');

      const atbody = document.getElementById('agents-tbody');
      atbody.innerHTML = STATE.workflows_data.agents.map(ag => `
        <tr>
          <td><b>${{ag.icon}} ${{ag.name}}</b></td>
          <td>${{ag.responsibility}}</td>
          <td><span class="badge badge-cyan">${{ag.autonomy_level}}</span></td>
          <td><code>${{ag.default_model}}</code></td>
        </tr>
      `).join('');

      const wtbody = document.getElementById('workflows-tbody');
      wtbody.innerHTML = STATE.workflows_data.workflows.map(wf => `
        <tr>
          <td><b>${{wf.name}}</b></td>
          <td><code>${{wf.domain}}</code></td>
          <td><span class="badge badge-emerald">${{wf.autonomy_level}} (${{wf.autonomy_meta.name || ''}})</span></td>
          <td>${{wf.tests_passed}} testes</td>
          <td>${{wf.evidences_count}} evidências</td>
          <td style="font-size:11px; color:var(--text-2);">${{wf.steps.join(' &rarr; ')}}</td>
          <td>
            <select onchange="promoteWorkflow('${{wf.id}}', this.value)" style="width:120px;">
              <option value="">Promover...</option>
              <option value="L1">L1 Assisted</option>
              <option value="L2">L2 Supervised</option>
              <option value="L3">L3 Guarded</option>
              <option value="L4">L4 Autonomous</option>
            </select>
          </td>
        </tr>
      `).join('');
    }}

    async function submitFlowInbox() {{
      const content = document.getElementById('flow-input').value.trim();
      const source = document.getElementById('flow-source').value;
      if (!content) return;
      const created = await apiCall('/api/flow-inbox', 'POST', {{ content, source }});
      if (created) {{
        STATE.inbox.unshift(created);
        document.getElementById('flow-input').value = '';
        renderFlowAndAgents();
      }}
    }}

    async function promoteWorkflow(workflow_id, target_level) {{
      if (!target_level) return;
      const res = await apiCall('/api/workflows/autonomy', 'POST', {{ workflow_id, target_level }});
      if (res) {{
        document.getElementById('autonomy-feedback').textContent = res.reason;
        const wfFresh = await apiCall('/api/workflows');
        if (wfFresh) {{
          STATE.workflows_data = wfFresh;
          renderFlowAndAgents();
        }}
      }}
    }}

    async function runAiGateway() {{
      const payload = {{
        task_type: document.getElementById('gw-task').value,
        prompt_preview: 'Solicitação via Cockpit Eugência OS',
        min_quality: parseFloat(document.getElementById('gw-qmin').value),
        lambda_latency: parseFloat(document.getElementById('gw-lambda').value),
        mu_risk: parseFloat(document.getElementById('gw-mu').value),
        tokens_in: parseInt(document.getElementById('gw-tokens').value, 10),
        tokens_out: 350,
        tools_invoked: ['catalog_sql', 'whatsapp_api'],
        org_id: document.getElementById('gw-org').value
      }};
      const res = await apiCall('/api/gateway/route', 'POST', payload);
      if (res) {{
        document.getElementById('gw-result').textContent = JSON.stringify(res, null, 2);
      }}
    }}

    function updatePgPreset() {{
      const dom = document.getElementById('pg-domain').value;
      const presets = {{
        'card-chat': {{ action: 'apply_discount', payload: {{ sku: 'TCG-PKM-151-BOX', quantity: 2, stock_available: 14, discount_pct: 16.0, verified_catalog: true }} }},
        'finance': {{ action: 'execute_mandate_swap', payload: {{ protocol: 'Jupiter/Solana', amount_usd: 3000, fiduciary_buffer: 1.32, health_factor: 1.78, within_mandate: true }} }},
        'grantos': {{ action: 'submit_grant_proposal', payload: {{ work_package: 'WP1', has_mandatory_docs: true, duplicate_funding_for_same_wp: false, proprietary_claimed_as_public_good: false }} }},
        'neurocoder': {{ action: 'git_deploy_production', payload: {{ repo: 'card-chat', destructive_action: true, tests_passed: true }} }},
        'farcaster': {{ action: 'publish_weekly_cast', payload: {{ evidence_id: 'EV-001', channel: '/compilatorum' }} }}
      }};
      const p = presets[dom];
      if (p) {{
        document.getElementById('pg-action').value = p.action;
        document.getElementById('pg-payload').value = JSON.stringify(p.payload, null, 2);
      }}
    }}

    async function evaluateProofGate() {{
      let parsedPayload = {{}};
      try {{
        parsedPayload = JSON.parse(document.getElementById('pg-payload').value);
      }} catch (e) {{
        alert('JSON inválido no payload');
        return;
      }}
      const res = await apiCall('/api/proofgate/evaluate', 'POST', {{
        domain: document.getElementById('pg-domain').value,
        agent_role: 'Engineering IA',
        action: document.getElementById('pg-action').value,
        payload: parsedPayload
      }});
      if (res) {{
        document.getElementById('pg-eval-output').textContent = JSON.stringify(res, null, 2);
        const rFresh = await apiCall('/api/proofgate/receipts');
        if (rFresh) {{
          STATE.receipts = rFresh.receipts;
          renderReceipts();
        }}
      }}
    }}

    async function approveReceipt(receipt_id, decision) {{
      const res = await apiCall('/api/proofgate/approve', 'POST', {{
        receipt_id,
        approver: 'sukata (Human Authority)',
        decision,
        notes: 'Decisão registrada no Cockpit Eugência OS'
      }});
      if (res) {{
        const rFresh = await apiCall('/api/proofgate/receipts');
        if (rFresh) {{
          STATE.receipts = rFresh.receipts;
          renderReceipts();
        }}
      }}
    }}

    function renderReceipts() {{
      const tbody = document.getElementById('receipts-tbody');
      tbody.innerHTML = STATE.receipts.map(r => `
        <tr>
          <td><code>${{r.id}}</code></td>
          <td><b>${{r.domain}}</b> · <code>${{r.action}}</code></td>
          <td><span class="badge ${{r.policy_status === 'PASSED' ? 'badge-emerald' : (r.policy_status === 'BLOCKED' ? 'badge-rose' : 'badge-amber')}}">${{r.policy_status}}</span></td>
          <td style="font-size:11.5px;">${{(r.validation_reasons || []).join('<br/>')}}</td>
          <td><span class="badge badge-cyan">${{r.approval_status}}</span><br/><span style="font-size:10.5px; color:var(--text-2);">${{r.approved_by || 'Aguardando Humano'}}</span></td>
          <td><b>${{r.execution_status}}</b></td>
          <td><code style="font-size:10.5px;">${{r.receipt_hash.slice(0, 16)}}...</code></td>
          <td>
            ${{r.approval_status === 'PENDING_HUMAN' ? `
              <button class="btn-primary" style="padding:4px 8px; font-size:11px;" onclick="approveReceipt('${{r.id}}', 'APPROVED')">Aprovar</button>
              <button class="btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="approveReceipt('${{r.id}}', 'REJECTED')">Rejeitar</button>
            ` : '—'}}
          </td>
        </tr>
      `).join('');
    }}

    async function runCommerceSim(discountOverride = null) {{
      if (discountOverride !== null) {{
        document.getElementById('cm-discount').value = discountOverride;
      }}
      const payload = {{
        customer_name: document.getElementById('cm-customer').value,
        sku: document.getElementById('cm-sku').value,
        quantity: parseInt(document.getElementById('cm-qty').value, 10),
        requested_discount_pct: parseFloat(document.getElementById('cm-discount').value),
        message: document.getElementById('cm-msg').value
      }};
      const res = await apiCall('/api/commerce/simulate', 'POST', payload);
      if (res) {{
        document.getElementById('cm-output').textContent = JSON.stringify(res, null, 2);
        const rFresh = await apiCall('/api/proofgate/receipts');
        if (rFresh) {{
          STATE.receipts = rFresh.receipts;
          renderReceipts();
        }}
      }}
    }}

    function renderGrantOsAndResearch() {{
      const otbody = document.getElementById('opps-tbody');
      otbody.innerHTML = STATE.opportunities_data.opportunities.map(o => `
        <tr>
          <td><b>${{o.title}}</b><br/><span style="font-size:11px; color:var(--text-2);">Prazo: ${{o.deadline}}</span></td>
          <td>${{o.platform}} (${{o.channel_type}})</td>
          <td>R$ ${{o.reward_brl.toLocaleString('pt-BR')}}</td>
          <td>${{(o.probability * 100).toFixed(0)}}%</td>
          <td><b>R$ ${{o.expected_value_brl.toLocaleString('pt-BR')}}</b></td>
          <td><span class="badge badge-emerald">R$ ${{o.ev_per_hour_brl}}/h</span></td>
          <td><code>${{o.funding_category}}</code></td>
          <td><span class="badge badge-cyan">${{o.status}}</span></td>
        </tr>
      `).join('');

      const wptbody = document.getElementById('wps-tbody');
      wptbody.innerHTML = STATE.opportunities_data.grant_stacking_work_packages.map(w => `
        <tr>
          <td><b>${{w.wp_code}}</b></td>
          <td>${{w.deliverable}}</td>
          <td><span class="badge ${{w.funding_category === 'COMMERCIAL_PRODUCT' ? 'badge-amber' : 'badge-emerald'}}">${{w.funding_category}}</span></td>
          <td><code>${{w.license}}</code></td>
          <td>${{w.target_funder}} (R$ ${{w.amount_brl.toLocaleString('pt-BR')}})</td>
        </tr>
      `).join('');

      const etbody = document.getElementById('exps-tbody');
      etbody.innerHTML = STATE.research.experiments.map(e => `
        <tr>
          <td><b>${{e.code}}</b></td>
          <td><b>${{e.title}}</b><br/><span style="font-size:11px; color:var(--text-2);">${{e.hypothesis}}</span></td>
          <td><span class="badge badge-emerald">${{e.status}}</span></td>
          <td><b>${{e.ergonomics_index}}</b></td>
          <td>${{e.artifacts_delta_a}}</td>
        </tr>
      `).join('');

      document.getElementById('radar-preview').textContent = STATE.research.weekly_radar_draft.farcaster_cast_preview;

      const sel = document.getElementById('doc-selector');
      sel.innerHTML = STATE.docs.map((d, idx) => `<option value="${{idx}}">${{d.filename}} (${{(d.size_bytes/1024).toFixed(1)}} KB)</option>`).join('');
      renderSelectedDoc();
    }}

    function renderSelectedDoc() {{
      const idx = parseInt(document.getElementById('doc-selector').value || '0', 10);
      const doc = STATE.docs[idx];
      if (doc) {{
        document.getElementById('doc-viewer').textContent = doc.content;
      }}
    }}

    async function syncOrgMode() {{
      const res = await apiCall('/api/org/sync', 'POST', {{}});
      if (res) {{
        alert('Sincronização Emacs Org-mode concluída! Arquivos atualizados em ~/eugencia-os/org/');
      }} else {{
        alert('Arquivos Org-mode já exportados em ~/eugencia-os/org/');
      }}
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      renderKpis();
      renderRepoTable();
      renderFlowAndAgents();
      renderReceipts();
      renderGrantOsAndResearch();
      renderGraph(false);
    }});
  </script>
</body>
</html>
"""
    dist_dir = BASE_DIR / "frontend" / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    out_file = dist_dir / "index.html"
    out_file.write_text(html, encoding="utf-8")
    print(f"Built PWA Cockpit bundle at {out_file} ({len(html.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    build_bundle()
