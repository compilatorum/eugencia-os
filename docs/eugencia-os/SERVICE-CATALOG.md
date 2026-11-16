# 💼 SERVICE-CATALOG — Catálogo de Ofertas, Sprints de Gigs e Precificação

> **Princípio de Comercialização:** A unidade de venda da Eugência não é a "hora de programação", nem um cargo abstrato. É o **Pacote de Entrega Verificável** comercializado em três degraus progressivos:
> $$\text{1. Diagnóstico Pago} \longrightarrow \text{2. Sprint de Implementação} \longrightarrow \text{3. Operação Gerenciada (MRR)}$$

---

## 1. As Quatro Ofertas Prioritárias da Agência

### 🥇 Oferta 1: AI Automation & Agent Integration (Prioridade 1 — Mercado Amplo Web2 & Web3)
- **Proposta de Valor:** Transformar rotinas manuais de atendimento, vendas, triagem e operações em workflows automatizados e auditáveis com agentes de IA.
- **Entregáveis:** Agentes conversacionais e operacionais (WhatsApp, Web, Telegram, Discord), integração com APIs/CRMs/MercadoPago, bases de conhecimento RAG (`pgvector`), conectores MCP e aprovação humana (*HITL*).
- **Ativos Base Reutilizados:** `omni-dual-brain`, `card-chat`, `promptcraft`, `lakehouse`, `eugencia-os`.

### 🥈 Oferta 2: Web3 Data & Protocol Integration (Prioridade 1 — Ecossistemas Cripto)
- **Proposta de Valor:** Conectar aplicações, DAOs e equipes a dados on-chain, oráculos e protocolos com pipelines confiáveis e visualizações claras.
- **Entregáveis:** Pipelines ETL on-chain/off-chain, modelagem PostgreSQL/Lakehouse, integração com RPCs, Pyth Oracle e Jupiter, dashboards executivos e relatórios analíticos.
- **Ativos Base Reutilizados:** `lakehouse`, `oracle`, `value-curator`, `sovereign-html-mockups`.

### 🥉 Oferta 3: AI Agent Assurance / ProofGate Readiness (Diferenciação B2B & Licenciamento)
- **Proposta de Valor:** Impedir que agentes de IA executem ações fora de alçada, alucinem dados críticos ou violem mandatos financeiros/operacionais.
- **Entregáveis:** Mapeamento de riscos (*Threat Model*), configuração determinística do **Policy Engine (ProofGate)**, bateria de testes adversariais no **Harness**, modo de execução `APPROVAL_ONLY` e recibos criptográficos `SHA-256`.
- **Ativos Base Reutilizados:** `value-curator`, `vc`, `harness-engineering`, `KAIROS-Engine`.

### 🏅 Oferta 4: Grant & Governance Intelligence (Nicho Especializado Web3 / DAOs)
- **Proposta de Valor:** Estruturar a captação não-dilutiva e a governança operacional de projetos, protocolos e coletivos de pesquisa.
- **Entregáveis:** Mapeamento e scoring de oportunidades ($S(o)$), decomposição em *Work Packages* sem dupla cobrança (*Grant Stacking*), dossiês técnicos, automação de triagem de propostas DAO (`L0`–`L4`) e relatórios de evidências.
- **Ativos Base Reutilizados:** `concurseiro-grants`, `governaut-os`, `maha-grid`, `farcaster-nexus`.

---

## 2. Os Dez Pacotes de Gigs / Sprints de Escopo Fechado

Para converter criptojobs e demandas de clientes em entregas rápidas (5 a 14 dias) sem escopo aberto:

| Código | Pacote da Eugência (Sprint) | Escopo Fechado | Entrega Verificável (Critério de Aceite) | Faixa Inicial (R$) |
| :---: | :--- | :--- | :--- | :---: |
| **`SPR-01`** | **Technical Diagnostic & Roadmap Sprint** | Investigar problema, auditar arquitetura atual e desenhar plano de implantação | Documento de arquitetura + Backlog priorizado + Proposta de Sprint | **R$ 300 – R$ 800** |
| **`SPR-02`** | **API & Webhook Integration Sprint** | Integrar uma API externa (WhatsApp, pagamento, RPC, CRM) a um sistema existente | Conector versionado + Documentação + Suíte de testes de integração | **R$ 800 – R$ 2.500** |
| **`SPR-03`** | **AI Workflow & Copilot Sprint** | Automatizar um processo empresarial com agente LangGraph e aprovação HITL | Workflow executável + Schemas JSON + Demonstração E2E gravada | **R$ 1.500 – R$ 4.000** |
| **`SPR-04`** | **RAG Knowledge System Sprint** | Estruturar base documental consultável com PostgreSQL/`pgvector` e citações | Pipeline de ingestão + API de busca híbrida + Respostas auditadas com fonte | **R$ 2.000 – R$ 5.000** |
| **`SPR-05`** | **On-Chain Data & BI Dashboard Sprint** | Extrair, transformar e visualizar dados de um protocolo, carteira ou operação | Pipeline ETL + Schema SQL + Dashboard interativo com métricas de negócio | **R$ 1.500 – R$ 4.000** |
| **`SPR-06`** | **Agent Evaluation & QA Harness Sprint** | Avaliar confiabilidade de um agente com casos de borda e ataques adversariais | Dataset de avaliação + Runner automatizado + Relatório de falhas e correções | **R$ 1.800 – R$ 4.500** |
| **`SPR-07`** | **ProofGate Readiness Sprint** | Mapear riscos de um agente e implantar guardrails determinísticos e recibos | Threat model + Políticas ProofGate ativas + Testes adversariais aprovados | **R$ 3.500 – R$ 9.000** |
| **`SPR-08`** | **DAO Governance Automation Sprint** | Automatizar uma etapa do ciclo de propostas, triagem ou relatório de DAO | Bot/Agente integrado + Painel de acompanhamento + Recibos de decisão | **R$ 2.000 – R$ 5.500** |
| **`SPR-09`** | **Grant Intelligence & Stacking Sprint** | Mapear financiamentos compatíveis e estruturar projeto em Work Packages | Matriz de oportunidades qualificadas + Decomposição WP1–WP5 + Dossiê técnico | **R$ 800 – R$ 2.500** |
| **`SPR-10`** | **Developer Tooling & MCP Sprint** | Construir CLI, SDK TypeScript/Python, servidor MCP ou template reutilizável | Pacote instalável + Testes automatizados + Guia Quickstart com exemplos | **R$ 1.500 – R$ 4.500** |

---

## 3. Fórmulas de Precificação e Margem

### 3.1. Precificação de Projetos e Sprints Fechados ($P$)
Em vez de vender horas brutas, cada Sprint é precificado pela equação:

$$P = C_{\text{produção}} + C_{\text{risco}} + C_{\text{infra}} + M_{\text{desejada}} + T_{\text{plataforma}}$$

Onde:
- **$C_{\text{produção}}$:** Horas humanas estimadas $\times$ taxa-base interna + custo de inferência/agentes durante o build.
- **$C_{\text{risco}}$:** Prêmio de complexidade técnica, incerteza de integração e garantia de correção.
- **$C_{\text{infra}}$:** Custos de ambiente de testes, RPCs, banco de dados e hospedagem.
- **$M_{\text{desejada}}$:** Margem líquida para financiar a evolução do *Selfware* próprio da Eugência.
- **$T_{\text{plataforma}}$:** Taxa de marketplace/escrow quando aplicável (ex.: 10% no LaborX, 0% em B2B direto / Superteam).

### 3.2. Margem de Contribuição na Operação Gerenciada ($MC$)
Para contratos que evoluem do Sprint para mensalidade recorrente (*Managed Service* de R$ 300 a R$ 1.500+/mês):

$$MC = R - C_{\text{IA}} - C_{\text{infra}} - C_{\text{suporte}} - C_{\text{pagamentos}}$$

---

## 4. Lei do Duplo Pagamento (Regra de Reaproveitamento $\Delta S$)

> **Filosofema:** Cada trabalho externo deve pagar duas vezes — **uma em dinheiro ($\mathcal{R}$), outra em capital intelectual ($\Delta S$)**. A segunda remuneração só é legítima quando respeita integralmente a confidencialidade, a licença e os direitos contratuais do cliente.

$$\Delta S = \text{Componente Genérico Reutilizável} + \text{Suíte de Testes} + \text{Documentação Padrão} + \text{Aprendizado Operacional}$$

Ao encerrar qualquer um dos 10 Sprints (`SPR-01` a `SPR-10`), o estágio `Learn` do CRM exige registrar qual conector, template ou regra de validação genérica foi incorporado ao **ValueCurator OS**.
