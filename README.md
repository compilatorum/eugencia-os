# 🧭 Eugência OS & ValueCurator OS (`~/eugencia-os`)

> **Plano Estratégico & Sistema Operacional de Carreira, Pesquisa, Selfware, Service-as-a-Software e Web3**
> Implementação integral do projeto especificado em [`~/eugencia.pdf`](file:///home/sukata/eugencia.pdf) para o ecossistema **Compilatorum + ValueCurator**.

---

## 🏛️ 1. Visão Geral da Arquitetura Implementada

$$E = H + S + A + G \qquad \text{e} \qquad VOS = I + B + AI + M + T + O + G$$

O projeto implementa simultaneamente:
1. **A Suíte Estratégica e Operacional `EUGENCIA-OS` (9 Artefatos em `docs/eugencia-os/`):**
   - [`PORTFOLIO-ASSETS-REGISTER.md`](docs/eugencia-os/PORTFOLIO-ASSETS-REGISTER.md) — Auditoria e classificação A–F dos **72 repositórios reais** (`59 compilatorum` + `13 smp-sandramariapereira`).
   - [`BUSINESS-ARCHITECTURE.md`](docs/eugencia-os/BUSINESS-ARCHITECTURE.md) — Arquitetura institucional, os 6 clusters econômicos, os 3 motores e a Equipe Humano-IA (7 papéis).
   - [`PRODUCT-CATALOG.md`](docs/eugencia-os/PRODUCT-CATALOG.md) — Catálogo de *Productized Services* (`AI Commerce Agent`, `ProofGate / AI Agent Assurance`, `Grant Intelligence`, etc.).
   - [`SELFWARE-STRATEGY.md`](docs/eugencia-os/SELFWARE-STRATEGY.md) — Lei de acumulação de capital intelectual ($A_{t+1} = A_t + \Delta A_t$, com $\Delta A_t > 0$) e governança de propriedade intelectual.
   - [`REVENUE-MODEL.md`](docs/eugencia-os/REVENUE-MODEL.md) — 5 modalidades de receita, sistema de créditos comerciais normalizados, margem de contribuição ($MC$) e pagamentos globais em 3 etapas.
   - [`GRANTOS-STRATEGY.md`](docs/eugencia-os/GRANTOS-STRATEGY.md) — Inteligência de capital, Superteam Earn, Gitcoin, integração Dework em 3 níveis e matriz de *Grant Stacking* (WP1–WP5 sem dupla cobrança).
   - [`VALUECURATOR-OS-SPEC.md`](docs/eugencia-os/VALUECURATOR-OS-SPEC.md) — Especificação das 7 camadas do núcleo multi-tenant, roteador ótimo do AI Gateway ($M^*$) e ProofGate transversal.
   - [`ROADMAP-90-DAYS.md`](docs/eugencia-os/ROADMAP-90-DAYS.md) — Plano executável em 6 fases (Dias 1–90) com critérios objetivos de conclusão.
   - [`EXPERIMENT-TRACKER.md`](docs/eugencia-os/EXPERIMENT-TRACKER.md) — Linha de pesquisa *Agentic Selfware & Verifiable Service Engineering* (`E-001`, `E-002`, `E-003`) e evidências SHA-256.
   - [`CRYPTOJOBS-MARKET-MAP.md`](docs/eugencia-os/CRYPTOJOBS-MARKET-MAP.md) — Mapa das 7 famílias de criptojobs compatíveis, matriz `Ativos -> Criptojobs -> Serviços`, canais (Superteam Earn, Dework, Gitcoin, Algora, LaborX, web3.career) e fronteiras de responsabilidade.
   - [`SERVICE-CATALOG.md`](docs/eugencia-os/SERVICE-CATALOG.md) — As 4 ofertas prioritárias da Eugência, os 10 Sprints de Escopo Fechado (`SPR-01`..`SPR-10`), fórmula de precificação ($P = C_{\text{prod}} + C_{\text{risco}} + C_{\text{infra}} + M_{\text{desejada}}$) e lei do duplo pagamento ($\Delta S > 0$).
   - [`FREELANCER-PROFILE.md`](docs/eugencia-os/FREELANCER-PROFILE.md) — Identidade institucional (Eugência + Compilatorum + ValueCurator), perfis bilingues (PT-BR & EN), divisão de trabalho humano-IA e os 6 Casos Demonstrativos Proof-of-Work (`CASE-01`..`CASE-06`) com métrica *Portfolio Readiness*.
   - [`OPPORTUNITY-SCORING.md`](docs/eugencia-os/OPPORTUNITY-SCORING.md) — Equação de compatibilidade $S(o) = 0.25F + 0.20R + 0.20A + 0.15E + 0.10P + 0.10C$, os 2 filtros eliminatórios e o Pipeline CRM de 9 estágios (`Discover -> ... -> Learn`).
   - [`RTM-TRACEABILITY-MATRIX.md`](docs/eugencia-os/RTM-TRACEABILITY-MATRIX.md) & [`ADR-ARCHITECTURE-DECISIONS.md`](docs/eugencia-os/ADR-ARCHITECTURE-DECISIONS.md) — Matriz de rastreabilidade ($F = 1.00$) e decisões arquiteturais.
   - [`E2E-BOUNTIES-PLAYBOOK.md`](docs/eugencia-os/E2E-BOUNTIES-PLAYBOOK.md) — Guia visual E2E Playwright (6 telas anotadas com setas + 4 diagramas Mermaid renderizados).

2. **O Núcleo Tecnológico `ValueCurator OS` & `Eugência OS` (`backend/`):**
   - **7 Camadas VOS:** Identity & Multi-tenancy (`Organization`, `User`, `Workspace`), Billing & Créditos Normalizados, **AI Gateway** ($M^* = \arg\min [C(m) + \lambda L(m) + \mu R(m)]$ sujeito a $Q(m) \ge Q_{\min}$), Agent & Workflow Runtime (autonomia progressiva `L0` a `L4`), Memory (SQLite/PostgreSQL), Tools e **ProofGate** ($\text{Intent} \rightarrow \text{Policy} \rightarrow \text{Validation} \rightarrow \text{Approval} \rightarrow \text{Execution} \rightarrow \text{Receipt}$).
   - **Módulos de Carreira e Venture Builder:** *Flow Inbox* (Divergência $\leftrightarrow$ Convergência), *Opportunity Intelligence CRM*, *Research & Experiment OS*, *Delivery & Card-Chat AI Commerce Simulator* e *Reputation & Publishing OS*.

3. **Cockpit Híbrido: Web App / PWA com Grafo SCADA Cytoscape.js (`frontend/dist/index.html`) + Emacs Org-mode (`org/` e `emacs/eugencia-os.el`):**
   - Painel SCADA interativo representando Holding $\rightarrow$ 6 Clusters $\rightarrow$ 72 Repositórios $\rightarrow$ Produtos $\rightarrow$ Clientes $\rightarrow$ Receita.
   - Sincronização bidirecional com `org/inbox.org`, `org/portfolio.org`, `org/opportunities.org` e `org/experiments.org`.

---

## 🚀 2. Como Executar e Utilizar

### 2.1. Iniciar o Servidor da API e Cockpit Web / PWA
```bash
python3 ~/eugencia-os/scripts/eugencia_cli.py serve --port 8765
```
Acesse **`http://127.0.0.1:8765`** no navegador (ou abra `~/eugencia-os/frontend/dist/index.html` diretamente em modo offline-first).

### 2.2. Comandos Rápidos via CLI
```bash
# Exibir os KPIs executivos da Eugência (E, MRR, MC, L, rho, WIP <= 2, Ergonomia)
python3 ~/eugencia-os/scripts/eugencia_cli.py kpis

# Capturar uma ideia ou oportunidade no Flow Inbox (e sincronizar com org/inbox.org)
python3 ~/eugencia-os/scripts/eugencia_cli.py capture "Nova oportunidade Superteam Earn para SDK do ProofGate"

# Sincronizar bidirecionalmente os arquivos Emacs Org-mode
python3 ~/eugencia-os/scripts/eugencia_cli.py sync-org

# Testar roteamento ótimo M* no AI Gateway
python3 ~/eugencia-os/scripts/eugencia_cli.py route --task commerce_chat --min-quality 0.80

# Simular pedido no Card-Chat (AI Commerce Agent - Vespa TCG)
python3 ~/eugencia-os/scripts/eugencia_cli.py simulate-commerce --sku TCG-PKM-151-BOX --qty 2 --discount 8
```

### 2.3. Integração no Emacs (`emacs/eugencia-os.el`)
Adicione ao seu `init.el` / `config.el`:
```elisp
(load-file "~/eugencia-os/emacs/eugencia-os.el")
(eugencia-os-mode 1)
;; Atalhos globais:
;; C-c e c -> Capturar item no Flow Inbox
;; C-c e s -> Sincronizar arquivos Org <-> Banco Eugência OS
;; C-c e k -> Exibir KPIs da Eugência no minibuffer
;; C-c e i -> Abrir org/inbox.org
;; C-c e p -> Abrir org/portfolio.org
;; C-c e o -> Abrir org/opportunities.org
;; C-c e x -> Abrir org/experiments.org
```

### 2.4. Executar a Suíte de Testes Automatizados
```bash
pytest ~/eugencia-os/backend/tests/test_eugencia.py -v
```
