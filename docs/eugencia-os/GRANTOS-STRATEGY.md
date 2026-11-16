# 🌱 GRANTOS-STRATEGY — Estratégia de Financiamento, Bounties e Grant Stacking

> **Filosofema do Capital Não-Dilutivo:** O grant financia a externalidade positiva (bens públicos abertos, segurança e pesquisa); o cliente comercial paga pelo benefício privado que recebe (hospedagem, SLA, operação gerenciada e funcionalidades proprietárias).

---

## 1. Os Cinco Canais de Aquisição de Capital

Não tratamos financiamento Web3 e subvenções como um mercado monolítico. Cada canal remunera uma natureza específica de entrega:

| Canal | Objetivo Estratégico | Aplicação no Portfólio Compilatorum / ValueCurator | Previsibilidade |
| :--- | :--- | :--- | :---: |
| **1. Customers (Clientes B2B)** | Financiar soluções comerciais e validar PMF | `card-chat` (AI Commerce Agent) e pilotos pagos do `ProofGate` | Alta (MRR) |
| **2. Licensing (Licenciamento)** | Monetizar propriedade intelectual (Core IP) | API de validação **ProofGate**, SDKs empresariais e contratos *Agent Assurance* | Média/Alta |
| **3. Grants (Subvenções)** | Financiar entregas de interesse público e de ecossistema | SDKs abertos, testes adversariais de segurança, adaptadores de dados e pesquisa | Média (Por Milestones) |
| **4. Bounties (Tarefas Remuneradas)** | Remunerar entregas técnicas específicas de curto prazo | Implementações pontuais, integrações Solana/DeFi e ferramentas de ecossistema | Variável |
| **5. Hackathons** | Obter premiação, visibilidade, tração comunitária e contatos | Protótipos rápidos e MVPs demonstráveis (Colosseum Solana, ETHGlobal) | Esporádica |

---

## 2. O Modelo Operacional GrantOS

Construído sobre a arquitetura do repositório `concurseiro-grants`, o **GrantOS** opera como um sistema de inteligência de capital:

$$\text{Project} \rightarrow \text{FundingThesis} \rightarrow \text{Opportunity} \rightarrow \text{WorkPackage} \rightarrow \text{Evidence} \rightarrow \text{Funding}$$

### 2.1. Classificação Anti-Dupla-Cobrança (Cinco Categorias Estritas)
Para manter integridade ética e contratual absoluta, todo *Work Package* é classificado em **uma única categoria exclusiva** (proibindo financiar duas vezes a mesma entrega ou apresentar código proprietário fechado como bem público):
1. `OPEN_PUBLIC_GOODS` — Bibliotecas, SDKs e padrões 100% open source (MIT/Apache-2.0).
2. `RESEARCH_AND_VALIDATION` — Benchmarks, testes adversariais, papers e relatórios experimentais abertos.
3. `SHARED_INFRASTRUCTURE` — Conectores, indexadores, adaptadores de oráculos e tooling de ecossistema.
4. `COMMERCIAL_PRODUCT` — Hospedagem gerenciada, dashboards multi-tenant, suporte e integrações privadas (financiado exclusivamente por **Clientes e Licenciamento**).
5. `CONTRIBUTOR_COMPENSATION` — Bounties e tarefas distribuídas para colaboradores na comunidade.

---

## 3. Matriz de Grant Stacking (Decomposição por Work Packages)

### Caso Exemplar: `value-curator` / ProofGate

| Work Package | Entrega Técnica Delimitada | Categoria GrantOS | Licença | Fonte de Financiamento Alvo |
| :---: | :--- | :--- | :---: | :--- |
| **WP1** | SDK TypeScript aberto de especificação de intents e políticas para agentes | `OPEN_PUBLIC_GOODS` | MIT | **Grant de Developer Tooling** (Superteam / Solana Foundation) |
| **WP2** | Suíte aberta de testes adversariais e benchmark de segurança para agentes financeiros | `RESEARCH_AND_VALIDATION` | Apache-2.0 | **Grant de Segurança** (Security Grants / Audit Funds) |
| **WP3** | Adaptadores on-chain Solana (Anchor program + Pyth Oracle + Jupiter quotes em modo seguro) | `SHARED_INFRASTRUCTURE` | Apache-2.0 | **Grant de Ecossistema Solana** (Superteam Earn / Colosseum) |
| **WP4** | API Hospedada Multi-Tenant do ProofGate com SLA e AI Gateway integrado | `COMMERCIAL_PRODUCT` | Proprietária | **Receita de Clientes B2B** (Assinatura + Créditos) |
| **WP5** | Dashboard Executivo de Auditoria, Compliance e Aprovação *Human-in-the-Loop* | `COMMERCIAL_PRODUCT` | Proprietária | **Receita Comercial & Licenciamento Empresarial** |

### Mapeamento de Canais Prioritários por Projeto do Portfólio

| Projeto | Entrega Financiável | Canal Prioritário |
| :--- | :--- | :--- |
| **ValueCurator / ProofGate** | Segurança de agentes autônomos, Policy Engine e execução verificável | **Solana / Superteam Earn** (Grants & Bounties) + **Security Grants** |
| **Farcaster Commons Lab (`farcaster-nexus` + `IPIT`)** | Conversão de interações comunitárias em contribuições verificáveis | **Gitcoin Grants** / Financiamento Comunitário / RetroPGF |
| **Promptcraft** | Schemas abertos de engenharia de contexto e proveniência de prompts | **Developer Tooling Grants** |
| **Lakehouse** | Adaptadores de dados multimodais e interoperabilidade | **Filecoin / The Graph** Ecosystem Grants |
| **Maha Grid / Governaut-OS** | Governança agêntica L0–L5 e simulação cadCAD de propostas DAO | **W3F / Polkadot OpenGov / Nouns** |
| **AROS (`prompt-audiofeedback`)** | Pesquisa aplicada em biofeedback vocal idiográfico | Editais de Pesquisa e Inovação (FAPEMIG / FINEP / CNPq) |

---

## 4. Estratégia para Dework, Superteam Earn e Gitcoin

### 4.1. Prioridade de Plataformas Ativas
1. **Superteam Earn (Prioridade #1 para Web3):** Monitoramento semanal de *Bounties* de desenvolvimento, *Projects* e *Instagrants* no ecossistema Solana, diretamente alinhados ao stack Rust/Anchor/TypeScript do `value-curator` e `eidos-tokenization`.
2. **Gitcoin Grants (Prioridade #2 para Bens Públicos):** Participação estruturada conforme o calendário de rodadas (GG rounds) com os componentes *Open Core* (`promptcraft`, `governaut-os`, `farcaster-nexus`).

### 4.2. Integração com Dework em Três Níveis (Sem Dependência Cega de API Interna)
Embora existam evidências do endpoint GraphQL (`https://api.dework.xyz/graphql` e `/health`), ele não possui contrato público de estabilidade documentado para depender dele como infraestrutura crítica imediata. Adotamos a estratégia graduada:

| Nível | Abordagem Técnica | Decisão Operacional |
| :---: | :--- | :--- |
| **Nível 1** | **GitHub Issues $\leftrightarrow$ Sincronização Nativa Dework:** Issues viram tarefas, PRs atualizam status e pagamentos ocorrem via carteira/Gnosis Safe | ✅ **Implementado e Ativo Agora** |
| **Nível 2** | **Introspecção Controlada GraphQL:** Testes isolados de leitura, paginação e rate-limit sem bloqueio operacional | 🔍 **Modo Investigação no Opportunity Engine** |
| **Nível 3** | **Adaptador Próprio com Fallback e Logs:** Conector resiliente na Camada 6 do VOS com fallback para ingestão via GitHub/Markdown | 🛠️ **Ativado sob Demanda** |

---

## 5. Sinergia Farcaster + GitHub + GrantOS

$$\text{Interaction (Farcaster)} \rightarrow \text{Contribution (GitHub PR/Commit)} \rightarrow \text{Evidence (ProofGate/Tests)} \rightarrow \text{Recognition (Reputation OS)} \rightarrow \text{Funding (Grants & Clientes)}$$

- **Farcaster (`farcaster-nexus`):** Canal de distribuição orgânica, demonstrações públicas (*build in public*), validação de hipóteses com a comunidade e atração de colaboradores/clientes.
- **GitHub (`compilatorum`):** Fonte canônica da verdade para commits, PRs, releases, execução de testes automatizados e comprovação de entregas de *Work Packages*.
