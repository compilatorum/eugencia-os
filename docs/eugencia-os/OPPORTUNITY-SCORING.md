# 🎯 OPPORTUNITY-SCORING — Modelo de Pontuação $S(o)$, Filtros Eliminatórios e Pipeline CRM

> **Objetivo:** Transformar o **Eugência OS** no sistema nervoso comercial da agência, garantindo que nenhuma bounty, gig, grant ou projeto de cliente entre na fila de execução sem antes passar por **dois filtros eliminatórios de segurança** e pelo **Score Multi-Critério de Compatibilidade $S(o) \in [0, 100]$**.

---

## 1. Os Dois Filtros Eliminatórios (Kill-Switches de Qualificação)

Antes de calcular a nota de uma oportunidade $o$, o **Business Development IA** e o **ProofGate** aplicam duas travas binárias obrigatórias:

1. 🛡️ **Filtro Eliminatório 1 — Sustentabilidade de Risco (`passes_risk_gate == True`):**
   - *Pergunta:* O trabalho exige assumir responsabilidade técnica, financeira, fiduciária ou de auditoria formal que a Eugência não deve assumir no estágio atual (Seção 3.3 do Mapa)?
   - *Ação se reprovado:* **Descarte imediato (`DISQUALIFIED_BY_RISK`)** ou reenquadramento estrito para escopo consultivo/teste sem custódia.
2. 💰 **Filtro Eliminatório 2 — Verificabilidade de Orçamento e Aceite (`passes_verified_budget_gate == True`):**
   - *Pergunta:* Há orçamento confirmado, pagador identificável, critério objetivo de aceite e prazo claro?
   - *Ação se reprovado:* **Retenção em `UNVERIFIED_LEAD`** — uma tarefa com alto fit técnico mas sem orçamento verificável não consome capacidade produtiva ($WIP_{\text{comercial}} \le 2$).

---

## 2. Equação do Score de Compatibilidade $S(o)$ (0 a 100)

Para toda oportunidade aprovada nos dois filtros eliminatórios, calcula-se:

$$\boxed{S(o) = 0.25 F + 0.20 R + 0.20 A + 0.15 E + 0.10 P + 0.10 C}$$

Onde cada vetor é avaliado na escala normalizada $[0, 100]$:

| Componente | Peso | Significado Operacional | Critério de Pontuação ($0 \rightarrow 100$) |
| :---: | :---: | :--- | :--- |
| **$F$ (Technical Fit)** | **25%** | Aderência às competências atuais (IA, Dados, Python/TS, Web3, QA) | `100` se utiliza stack dominada; `<40` se exige tecnologia inédita sem base |
| **$R$ (Remuneration & Margin)** | **20%** | Retorno financeiro esperado ($\text{EV}/h$) e margem de contribuição | `100` se $\text{EV}/h \ge \text{R\$ } 500/\text{h}$ e pagamento em BRL/PIX ou Stablecoin (USDC) |
| **$A$ (Selfware Accumulation)** | **20%** | Potencial de gerar ativo reutilizável ($\Delta S > 0$ / $\Delta A_t > 0$) | `100` se melhora diretamente o `ValueCurator OS`, `ProofGate`, `Card-Chat` ou `GrantOS` |
| **$E$ (Ergonomics & Effort)** | **15%** | Baixo atrito operacional, escopo fechado e prazo saudável | `100` para Sprint bem delimitado (5–14 dias); `<30` para escopo aberto ou plantão 24/7 |
| **$P$ (Portfolio & Proof-of-Work)** | **10%** | Potencial de fortalecer um dos 6 Casos Demonstrativos (`CASE-01`..`06`) | `100` se gera estudo de caso público verificável e sobe o nível $L_i \rightarrow L_5$ |
| **$C$ (Purpose Alignment)** | **10%** | Alinhamento com a tese de longo prazo da Eugência | `100` se converge com *Agentic Selfware & Verifiable Service Engineering* |

### Faixas de Decisão pelo Score $S(o)$:
- 🟢 **$S(o) \ge 75$ (`PRIORITY_EXECUTE`):** Candidatura / proposta imediata (desde que $WIP_{\text{comercial}} < 2$).
- 🟡 **$60 \le S(o) < 75$ (`TACTICAL_BACKLOG`):** Executar como gig de contingência de caixa quando houver janela livre.
- 🔴 **$S(o) < 60$ (`DECLINE_OR_ARCHIVE`):** Declinar para proteger o tempo de construção de *Selfware*.

---

## 3. Pipeline de CRM da Agência em 9 Estágios

$$\text{Discover} \rightarrow \text{Qualify} \rightarrow \text{Scope} \rightarrow \text{Propose} \rightarrow \text{Contract} \rightarrow \text{Deliver} \rightarrow \text{Accept} \rightarrow \text{Invoice} \rightarrow \text{Learn}$$

| Estágio | Entidade Principal | Campos Fundamentais Registrados no Eugência OS | Gate de Transição (ProofGate / HITL) |
| :---: | :--- | :--- | :--- |
| **1. `Discover`** | `Opportunity` | `id`, `source_channel`, `client_or_dao`, `problem_summary`, `raw_budget_brl`, `currency` | Captura via Flow Inbox ou Radar Semanal |
| **2. `Qualify`** | `OpportunityScore` | Vetores $(F, R, A, E, P, C)$, `score_s`, `passes_risk_gate`, `passes_verified_budget_gate` | Ambos os filtros eliminatórios `True` e $S(o) \ge 60$ |
| **3. `Scope`** | `WorkPackage` | `sprint_code` (`SPR-01`..`10`), `deliverables`, `effort_hours`, `acceptance_criteria`, `repo_target` | Escopo fechado e vinculado a repositório existente |
| **4. `Propose`** | `Proposal` | `version`, `price_brl` ($P = C_{\text{prod}} + C_{\text{risco}} + C_{\text{infra}} + M$), `milestones`, `valid_until` | Aprovação humana do preço e termos (`HITL`) |
| **5. `Contract`** | `Contract` | `payment_schedule`, `ip_ownership_clause`, `reusable_selfware_rights`, `wip_slot` | Verificação de $WIP_{\text{comercial}} \le 2$ e cláusula de IP |
| **6. `Deliver`** | `Delivery` | `branch_or_pr`, `tests_passed`, `artifact_uri`, `evidence_sha256`, `proofgate_receipt_id` | Suíte de testes aprovada no Harness + Recibo ProofGate |
| **7. `Accept`** | `Acceptance` | `accepted_by_client`, `acceptance_date`, `client_feedback`, `case_maturity_delta` | Confirmação formal de aceite contra os critérios do estágio 3 |
| **8. `Invoice`** | `Invoice` | `amount_brl`, `settlement_currency` (`BRL_PIX`, `USDC`), `gateway`, `net_margin_mc` | Pagamento liquidado e reconciliado no Revenue Ledger |
| **9. `Learn`** | `LearningLoop` | `extracted_component_delta_s`, `updated_case_id`, `farcaster_changelog_id` | Extração obrigatória de $\Delta S > 0$ para o ValueCurator OS |

---

## 4. Backlog de Implementação e Evolução do CRM (Status no Repositório)

- [x] **Módulo 1 (Motor de Scoring $S(o)$ + Kill-Switches):** Implementado em `backend/app/engine.py` (`score_opportunity`) e exposto em `POST /api/crm/score`.
- [x] **Módulo 2 (Catálogo dos 10 Sprints + Calculadora $P$):** Implementado em `backend/app/engine.py` (`list_service_sprints_and_cases`, `calculate_sprint_price`) e exposto em `POST /api/services/price-quote`.
- [x] **Módulo 3 (Vitrine dos 6 Casos PoW + Métrica *Portfolio Readiness*):** Implementado em `backend/app/engine.py` (`get_portfolio_readiness`) com cálculo ponderado $\frac{\sum w_i L_i}{5 \sum w_i}$.
- [x] **Módulo 4 (Pipeline CRM de 9 Estágios):** Tabela `crm_pipeline_deals` no SQLite/Postgres + progressão auditada `Discover -> ... -> Learn` (`POST /api/crm/advance`).
