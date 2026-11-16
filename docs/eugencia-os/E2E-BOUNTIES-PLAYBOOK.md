# 🎯 E2E-BOUNTIES-PLAYBOOK — Plano Estratégico & Tático de Bounties + Guia Visual E2E (Playwright)

> **Propósito:** Alinhar a execução de **Bounties (Dework / Superteam Earn / Gitcoin)** e **Pilotos B2B** com os **6 Eixos da Linha de Pesquisa** (*Agentic Selfware & Verifiable Service Engineering*) e as **4 Linhas de Financiamento**, dando vazão adaptativa aos **72 repositórios** do ecossistema **Compilatorum + ValueCurator** enquanto consolida propriedade intelectual própria ($\Delta A_t > 0$).

---

## 🧭 1. Outline Estratégico & Tático

- 🌐 **1.1. Inteligência de Oportunidades e Integração Dework em 3 Níveis**
  - **Nível 1 (Sincronização Nativa GitHub Issues $\leftrightarrow$ Dework):** Toda bounty selecionada é espelhada como Issue/Milestone em `compilatorum/*`, onde branches e Pull Requests atualizam automaticamente o estado da entrega.
  - **Nível 2 (Sondagem GraphQL Controlada):** Monitoramento de `https://api.dework.xyz/graphql` e `https://api.dework.xyz/health` via `scripts/e2e_playwright_bounties.py` (registrado em `data/dework_bounties_probe.json`), operando sem dependência cega de endpoints privados.
  - **Nível 3 (Priorização por Valor Esperado Horário — $\text{EV}/h$):**
    $$\text{EV}/h = \frac{\text{Recompensa (R\$)} \times P(\text{Aprovação})}{\text{Horas Estimadas de Preparo e Execução}}$$
- 🔬 **1.2. Simbiose Pesquisa $\leftrightarrow$ Financiamento $\leftrightarrow$ Repositórios**
  - **Eixo 1 (Cognição Aumentada, Flow & Ergonomia)** $\leftrightarrow$ `emacs`, `omni-dual-brain`, `planner`
  - **Eixo 2 (Engenharia de Contexto, Grafos, Memória & Orquestração)** $\leftrightarrow$ `governaut-os`, `lakehouse`, `oracle`, `proterol`
  - **Eixo 3 (Harness Engineering, Testes Adversariais & ProofGate)** $\leftrightarrow$ `value-curator`, `vc`, `harness-engineering`, `KAIROS-Engine`
  - **Eixo 4 (Service-as-a-Software & Productized Services)** $\leftrightarrow$ `card-chat`, `neurocoder-pwa`
  - **Eixo 5 (Reputação Verificável, Bounties, Grants & DeFi)** $\leftrightarrow$ `concurseiro-grants`, `farcaster-nexus`, `IPIT`, `maha-grid`
  - **Eixo 6 (Modelos Econômicos de Micro-Ventures Agentic)** $\leftrightarrow$ `invest-os`, `sovereign-budget`, `eidos-tokenization`

---

## 🎨 2. Diagramas Mermaid Coloridos e Renderizados

- **Diagrama 1 — Arquitetura de Fluxo (Pesquisa $\times$ Financiamento $\times$ 72 Repositórios):** `assets/mermaid_1_arquitetura_fluxo.png`
- **Diagrama 2 — Topologia das Bounties (`#B01`..`#B05`) e Acumulação $\Delta A_t$:** `assets/mermaid_2_bounties_pesquisa_financiamento.png`
- **Diagrama 3 — Máquina de Estados da Vazão Adaptativa:** `assets/mermaid_3_ciclo_adaptativo_repos.png`
- **Diagrama 4 — Sequência E2E com Validação ProofGate:** `assets/mermaid_4_sequencia_e2e_proofgate.png`

---

## 🖼️ 3. Roteiro do Teste End-to-End (Playwright) — 6 Telas Anotadas com Setas

1. **`assets/e2e_01_scada_portfolio_os.png`** — **Tela 1 (Portfolio OS & Grafo SCADA Cytoscape.js):**
   - Setas indicam como inspecionar nós no grafo, alternar entre ativos foco (`P0`/`P1`) e todos os 72 repositórios, filtrar por Cluster/Classe A–F e acionar o `Sync Emacs Org-Mode`.
2. **`assets/e2e_02_flow_inbox_equipe_ia.png`** — **Tela 2 (Flow Inbox & Equipe Humano-IA L0–L4):**
   - Setas indicam onde digitar a oportunidade/ideia, clicar em `+ Capturar no Flow` para triagem automática pelo *Chief of Staff IA* e promover a autonomia de workflows (`L0` $\rightarrow$ `L4`).
3. **`assets/e2e_03_ai_gateway_proofgate.png`** — **Tela 3 (ValueCurator OS — AI Gateway $M^*$ & ProofGate):**
   - Setas apontam para `Executar Roteamento M*`, `Submeter Intenção ao ProofGate` e o botão `Aprovar` (*Human-in-the-Loop*) na tabela de recibos criptográficos `SHA-256`.
4. **`assets/e2e_04_card_chat_commerce_agent.png`** — **Tela 4 (Motor 1 — Card-Chat AI Commerce Agent / Vespa TCG):**
   - Setas indicam a seleção de SKU no catálogo e os botões dos 3 cenários (`Venda Automática 8%`, `Retenção Gerente 18%` e `Ataque Prompt Injection 35%`).
5. **`assets/e2e_05_grantos_dework_bounties.png`** — **Tela 5 (GrantOS, Dework/Superteam Bounties & Grant Stacking):**
   - Setas destacam o ranking de oportunidades por `EV/h` (`#B01` a `#B06`) e a matriz `WP1`–`WP5` sem dupla cobrança.
6. **`assets/e2e_06_research_publishing_docs.png`** — **Tela 6 (Research OS, Build in Public & 9 Documentos `.MD`):**
   - Setas apontam para a tabela de experimentos (`E-001`..`E-003`) com cálculo de `Ergonomia`, o rascunho semanal do Farcaster baseado em evidências e o seletor dos 9 artefatos estratégicos.
