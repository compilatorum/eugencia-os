# 🧪 EXPERIMENT-TRACKER — Registro Científico e Operacional de Experimentos

> **Linha de Pesquisa Permanente:** *Agentic Selfware & Verifiable Service Engineering — Engenharia de sistemas humano-IA para prestação de serviços verificáveis, adaptativos e economicamente sustentáveis.*
>
> **Questão Central:** Como transformar conhecimento, software e agentes de IA em serviços produtizados, preservando a autonomia criativa e assegurando qualidade, rastreabilidade e sustentabilidade econômica?

---

## 1. Métricas de Instrumentação Científica e Operacional

Todo experimento conduzido na Eugência é avaliado por seis indicadores empíricos e pela equação de ergonomia:

1. **$T_{\text{flow}\rightarrow\text{exp}}$:** Tempo decorrido entre a captura de uma ideia no *Flow Inbox* e a estruturação de um experimento executável.
2. **$N_{\text{opp}}$:** Quantidade de oportunidades qualificadas no *Opportunity Intelligence* (EV positivo e alinhamento com P0/P1).
3. **$N_{\text{deliveries}}$:** Entregas efetivamente concluídas com evidências verificáveis (commits, testes aprovados, recibos ProofGate).
4. **$H_{\text{human}}$:** Horas de intervenção humana operacional consumidas.
5. **$N_{\text{posts}}$:** Publicações técnicas derivadas exclusivamente de evidências reais (*Reputation OS*).
6. **$R_{\text{conv}}$:** Oportunidades convertidas em receita comercial ($\mathcal{R}_c + \mathcal{R}_s + \mathcal{R}_l$) ou financiamento ($\mathcal{R}_g$).

$$\text{Ergonomia} = \frac{\text{Valor Entregue} \times \text{Autonomia}}{\text{Esforço} + \text{Atrito} + \text{Sobrecarga}}$$

---

## 2. Experimentos Ativos (Ciclo Inicial)

### 🎯 Experimento `E-001` — Eugência OS como Infraestrutura de Transição Profissional
- **Status:** 🟢 `ACTIVE / RUNNING` (Ciclo de 14 dias)
- **Eixo de Investigação:** Eixo 1 (Cognição aumentada, flow e ergonomia humano-IA) & Eixo 2 (Engenharia de contexto, grafos e orquestração).
- **Hipótese:** Um sistema humano-IA híbrido (Emacs/Org-mode + Web App com grafo SCADA Cytoscape.js) de captura (*Flow Inbox*), curadoria, execução supervisionada e publicação baseada em evidências reduz o atrito entre exploração criativa e entregas profissionais em pelo menos 50%, mantendo $WIP_{\text{comercial}} \le 2$.
- **Metodologia:**
  1. Inventariar e podar os 72 repositórios reais em classes A–F (`Fase 0`).
  2. Operar a captura diária via *Flow Inbox* e sincronização bidirecional Org-mode $\leftrightarrow$ SQLite/FastAPI.
  3. Submeter todas as ações sensíveis dos 7 agentes da equipe ao pipeline **ProofGate**.
- **Artefatos Produzidos ($\Delta A_t$):**
  - Repositório completo `~/eugencia-os` (Backend FastAPI + Frontend React/Cytoscape.js + CLI + pacote Elisp `eugencia-os.el` + 9 documentos estratégicos).
  - Base estruturada com os 72 repositórios auditados.
- **Critério de Sucesso:** Conduzir um experimento real, preparar uma entrega profissional e gerar uma atualização pública verificável a partir de evidências reais sem sobrecarga administrativa ($\text{Ergonomia} \ge 2.0$).

---

### 🛒 Experimento `E-002` — Card-Chat como AI Commerce Agent Verificável (Vespa TCG)
- **Status:** 🟡 `READY / PHASE 2`
- **Eixo de Investigação:** Eixo 4 (*Service-as-a-Software* e *Productized Services*) & Eixo 3 (*Harness Engineering* e *ProofGate*).
- **Hipótese:** A integração de um agente conversacional no WhatsApp com catálogo determinístico, checkout MercadoPago e guardrail **ProofGate** (bloqueando descontos $> 10\%$ e alucinações de estoque) permite automatizar $> 70\%$ do atendimento consultivo de uma loja de TCG com zero erro financeiro.
- **Metodologia:**
  1. Conectar o fluxo $\text{WhatsApp} \rightarrow \text{Agent} \rightarrow \text{Catalog} \rightarrow \text{Recommendation} \rightarrow \text{Checkout} \rightarrow \text{HumanHandoff}$ ao AI Gateway e ao ProofGate.
  2. Executar bateria de testes adversariais (cliente tentando forçar desconto de 30% via prompt injection ou comprar carta sem estoque).
  3. Medir tempo humano economizado por pedido e margem de contribuição ($MC$).
- **Critério de Sucesso:** 100% de bloqueio de descontos não autorizados nos testes adversariais e validação em produção no contexto Vespa TCG.

---

### 🛡️ Experimento `E-003` — ProofGate-as-a-Service & Grant Stacking Web3
- **Status:** 🟡 `DESIGNED / PHASE 4`
- **Eixo de Investigação:** Eixo 3 (Testes experimentais e ProofGate) & Eixo 5 (Reputação verificável, bounties e grants descentralizados).
- **Hipótese:** Decompor o `value-curator` / ProofGate em Work Packages abertos (WP1 SDK, WP2 Testes Adversariais, WP3 Adaptador Solana em modo `APPROVAL_ONLY`) e módulos comerciais (WP4 API, WP5 Dashboard) permite financiar a infraestrutura aberta via Grants (Superteam / Security) enquanto comercializa *Agent Assurance* B2B sem dupla cobrança.
- **Metodologia:**
  1. Isolar o Policy Engine determinístico e o gerador de recibos criptográficos SHA-256/Ed25519.
  2. Empacotar o benchmark de testes adversariais para agentes financeiros e operacionais.
  3. Submeter proposta qualificada no Superteam Earn / Solana Foundation.
- **Critério de Sucesso:** Desenvolvedor externo integra o ProofGate em $< 30$ minutos, reproduz os testes e 1 proposta de grant é submetida com evidências verificáveis.

---

## 3. Registro de Resultados e Evidências Verificáveis

| ID Evidência | Experimento | Data | Descrição da Evidência | Artefato / Hash | Status ProofGate |
| :---: | :---: | :---: | :--- | :--- | :---: |
| `EV-001` | `E-001` | 2026-11-16 | Auditoria e classificação A–F dos 72 repositórios GitHub (`compilatorum` + `smp-sandramariapereira`) | `data/portfolio_assets.json` | ✅ Verificado |
| `EV-002` | `E-001` | 2026-11-16 | Implementação das 7 camadas do ValueCurator OS (AI Gateway $M^*$ + ProofGate + Multi-tenant DB) | `backend/app/` | ✅ Verificado |
| `EV-003` | `E-001` | 2026-11-16 | Construção do painel SCADA Portfolio OS com grafo Cytoscape.js e sincronização Emacs Org-mode | `frontend/src/` + `org/` | ✅ Verificado |
| `EV-004` | `E-002` | 2026-11-16 | Simulação e validação determinística de políticas para `card-chat` (guardrail de desconto e estoque) | `backend/tests/test_eugencia.py` | ✅ Verificado |
