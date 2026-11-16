# 📦 PRODUCT-CATALOG — Catálogo de Productized Services & Soluções

> **Princípio Comercial:** Não começamos vendendo plataformas monolíticas gigantes. Comercializamos pacotes enxutos (*Productized Services* e *Service-as-a-Software*) com escopo fechado, preço transparente, prazo definido, limites de consumo e critérios objetivos de aceite.

---

## 1. Linha de Produtos Inicial (Matriz de Ofertas)

| Código | Produto | Unidade Comercial | Entrega Principal | Modelo Comercial | Status / Prioridade |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **PRD-01** | **AI Commerce Agent** | Commerce (`card-chat`) | Operador comercial automatizado via WhatsApp com catálogo, recomendação e checkout | Setup + Mensalidade + Créditos | 🟢 **P1 (Motor 1 Ativo)** |
| **PRD-02** | **ProofGate / AI Agent Assurance** | Agent Assurance (`value-curator`) | Infraestrutura de segurança, Policy Engine determinístico, validação e recibos criptográficos para agentes | Piloto Pago + Licenciamento + API | 🟢 **P1 (Motor 2 Ativo)** |
| **PRD-03** | **Grant Intelligence** | Intelligence (`concurseiro-grants`) | Descoberta de oportunidades, verificação de elegibilidade, decomposição em Work Packages e monitoramento | Setup + Assinatura | 🟡 **P1/P2 (Pacote 3)** |
| **PRD-04** | **AI Knowledge Agent** | Agent Engineering (`promptcraft` + `lakehouse`) | Base de conhecimento estruturada, RAG verificável e consultas com citação de fontes | Setup + Mensalidade + Créditos | ⚪ **P2** |
| **PRD-05** | **AI Workflow Agent** | Agent Engineering (`omni-dual-brain`) | Automação de processos empresariais com aprovação humana (*Human-in-the-Loop*) | Setup + Mensalidade + Créditos | ⚪ **P2** |
| **PRD-06** | **Data Intelligence** | Data (`lakehouse`) | Integração de dados, pipelines ETL, armazenamento estruturado e dashboards executivos | Setup + Mensalidade | ⚪ **P2/P3** |

---

## 2. Especificação Detalhada dos Três Pacotes Prioritários

### 2.1. Pacote 1: AI Commerce Agent (Service-as-a-Software para Comércio Especializado)

- **Cliente-Alvo Inicial:** Lojas de cartas colecionáveis e TCG (1º caso real: **Vespa TCG** em Belo Horizonte), expansível para lojas de jogos, colecionáveis, comércio especializado, educação e catálogos consultivos.
- **Problema Resolvido:** O lojista perde horas respondendo perguntas repetitivas no WhatsApp, consultando estoque/preço manualmente e acompanhando status de pedidos e entregas.
- **Fluxo Comercial Padronizado:**
  $$\text{WhatsApp} \rightarrow \text{Agent} \rightarrow \text{Catalog} \rightarrow \text{Recommendation} \rightarrow \text{Checkout (MercadoPago)} \rightarrow \text{HumanHandoff}$$
- **Entregáveis Inclusos:**
  1. Agente conversacional integrado à WhatsApp Business API.
  2. Catálogo sincronizado com fonte confiável de estoque e preços.
  3. Módulo de FAQ automatizado da loja.
  4. Motor de recomendação consultiva de produtos.
  5. Integração de checkout com MercadoPago e cálculo de roteamento/entrega local.
  6. **Guardrail ProofGate Comercial:** Bloqueio determinístico contra alucinação de estoque, preços abaixo da tabela ou descontos fora da alçada autorizada.
  7. Transbordo inteligente (*Human Handoff*) para casos complexos.
  8. Registro completo de conversas e relatório comercial periódico.
- **Escopo Inicial Padronizado:** 1 loja, 1 catálogo estruturado, 1 número de WhatsApp Business e até 5 fluxos comerciais delimitados.
- **Prazo de Implantação (SLA):** 7 a 14 dias úteis.
- **Critério de Aceite:** Fluxo ponta a ponta testado em produção (consulta de item real $\rightarrow$ recomendação $\rightarrow$ geração de link de pagamento $\rightarrow$ handoff humano auditado) com zero alucinação de preço/estoque.

---

### 2.2. Pacote 2: ProofGate / AI Agent Assurance (Segurança e Governança para Agentes)

- **Cliente-Alvo:** DAOs, protocolos DeFi, gestores de tesouraria, desenvolvedores de agentes financeiros e empresas que operam agentes de IA em fluxos críticos.
- **Problema Resolvido:** Agentes autônomos podem executar transações fora do mandato, aplicar descontos indevidos, modificar infraestrutura sem permissão ou operar sobre dados desatualizados.
- **Pipeline de Execução Verificável:**
  $$\text{Intent} \rightarrow \text{Policy} \rightarrow \text{Validation} \rightarrow \text{Approval} \rightarrow \text{Execution} \rightarrow \text{Receipt}$$
- **Entregáveis Inclusos:**
  1. Diagnóstico de arquitetura agêntica e mapeamento de superfície de risco.
  2. Configuração de mandatos determinísticos no **Policy Engine** (limites financeiros, listas de permissão, janelas temporais, oráculos Pyth/fontes confiáveis).
  3. Operação inicial em modo **`APPROVAL_ONLY`** (a IA propõe a intenção; o ProofGate valida a política; a autoridade humana competente aprova).
  4. Bateria de testes adversariais (tentativas de bypass de limite, prompt injection, dados obsoletos).
  5. Emissão de **Receipts Criptográficos** (assinatura SHA-256 / Ed25519) para cada decisão.
  6. Dashboard de auditoria de eventos e relatório técnico de conformidade.
- **Critério de Aceite:** Um agente integrado submete intenções válidas e inválidas; 100% das intenções fora da política são bloqueadas deterministicamente e todas as execuções geram recibos verificáveis.

---

### 2.3. Pacote 3: Grant Intelligence (Sistema de Inteligência de Capital)

- **Cliente-Alvo:** Startups deep-tech, DAOs, coletivos de pesquisa, protocolos Web3 e organizações buscando financiamento não-dilutivo.
- **Problema Resolvido:** Alto custo de oportunidade para monitorar dezenas de programas de grants (Superteam, Gitcoin, W3F, Polkadot, editais públicos), validar elegibilidade e estruturar propostas técnicas.
- **Pipeline Operacional GrantOS:**
  $$\text{Project} \rightarrow \text{FundingThesis} \rightarrow \text{Opportunity} \rightarrow \text{WorkPackage} \rightarrow \text{Evidence} \rightarrow \text{Funding}$$
- **Entregáveis Inclusos:**
  1. Radar contínuo de oportunidades (Superteam Earn, Gitcoin, ecossistemas L1/L2, editais de inovação).
  2. Matriz de compatibilidade e cálculo de Valor Esperado (EV vs custo de preparação).
  3. Decomposição do roadmap do cliente em **Work Packages independentes (Grant Stacking)**, separando estritamente *Open Public Goods*, *Research & Validation*, *Shared Infrastructure* e *Commercial Product*.
  4. Dossiê de preparação documental e calendário de submissões.
  5. Acompanhamento de milestones e compilação de evidências verificáveis no GitHub.
- **Critério de Aceite:** Entrega do mapa de Grant Stacking + pelo menos 2 oportunidades qualificadas com escopo de Work Packages pronto para submissão.

---

## 3. Regra de Acumulação em Cada Entrega Comercial

Nenhum serviço é entregue de forma artesanal isolada. Conforme a lei de acumulação de Selfware ($A_{t+1} = A_t + \Delta A_t$, com $\Delta A_t > 0$), **toda implantação de produto deste catálogo deve produzir obrigatoriamente pelo menos um ativo reutilizável para o ValueCurator OS:**
1. Um novo conector/adaptador na camada de *Tools*;
2. Uma nova regra determinística no *ProofGate*;
3. Uma suíte de testes automatizados no *Harness*;
4. Um template de workflow documentado.
