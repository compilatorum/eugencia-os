# 💰 REVENUE-MODEL — Modelo Econômico, Créditos, Custos e Pagamentos Globais

> **Princípio Financeiro:** $\text{Revenue First} \rightarrow \text{Tokenization Later}$. Separar rigorosamente receita recorrente de clientes, consumo variável de recursos computacionais e financiamento por grants/bounties.

---

## 1. Composição das Fontes de Receita

A receita operacional comercial ($R$) combina cinco modalidades complementares:

$$R = R_{\text{setup}} + R_{\text{subscription}} + R_{\text{usage}} + R_{\text{licensing}} + R_{\text{managed}}$$

Na visão consolidada do ecossistema ($\mathcal{Y}$), somamos a captação não-dilutiva mantendo contabilidade separada:

$$\boxed{\mathcal{Y} = \mathcal{R}_c + \mathcal{R}_s + \mathcal{R}_l + \mathcal{R}_g}$$

Onde:
- **$\mathcal{R}_c$ (Receita de Clientes — Setup & Implantação):** Configuração inicial de agentes, integração de catálogos e adaptação de fluxos.
- **$\mathcal{R}_s$ (Assinaturas & Uso — SaaS / Service-as-a-Software):** Mensalidade da plataforma + créditos de execução computacional.
- **$\mathcal{R}_l$ (Licenciamento de Propriedade Intelectual):** Licenças empresariais do **ProofGate**, SDKs premium e contratos de *Agent Assurance*.
- **$\mathcal{R}_g$ (Grants, Bounties e Financiamento de Pesquisa):** Recursos captados via Superteam Earn, Gitcoin, W3F, Polkadot, Nouns e editais para entregas abertas (*Open Public Goods* e *Research*).

---

## 2. Tabela de Precificação Inicial (Validação de Disposição a Pagar)

| Produto / Pacote | Setup (Implantação) | Mensalidade Base | Franquia de Créditos Inclusa | Modelo de Excedente |
| :--- | :---: | :---: | :---: | :--- |
| **AI Commerce Starter** (`card-chat`) | R$ 1.500 – R$ 3.000 | R$ 400 – R$ 800 / mês | 500 créditos / mês | R$ 0,60 por crédito extra |
| **AI Commerce Pro** (`card-chat`) | R$ 3.000 – R$ 6.000 | R$ 800 – R$ 1.500 / mês | 2.000 créditos / mês | R$ 0,45 por crédito extra |
| **AI Knowledge Agent** | R$ 2.000 – R$ 5.000 | R$ 500 – R$ 1.200 / mês | 2.000 créditos / mês | R$ 0,45 por crédito extra |
| **Grant Intelligence** (`GrantOS`) | R$ 500 – R$ 1.500 | R$ 150 – R$ 500 / mês | 500 créditos / mês | R$ 0,60 por crédito extra |
| **ProofGate / Agent Assurance** | Piloto pago sob orçamento (R$ 5.000 – R$ 15.000) | Licenciamento + API (Business: 10.000 créditos) | 10.000 créditos / mês | Contrato B2B / Volume |

---

## 3. O Sistema de Créditos Normalizados (Camada 2: Billing & Entitlements)

Para proteger a margem contra uso desproporcional de modelos caros de IA, a assinatura base dá direito à disponibilidade da infraestrutura, enquanto a execução consome **Créditos Comerciais Normalizados**:

$$\text{Créditos Consumidos} = f(\text{tokens}, \text{modelo}, \text{ferramentas}, \text{execuções})$$

### Fórmula Operacional Implementada no ValueCurator OS:
$$\text{Créditos}(s) = \left\lceil \left(\frac{T_{\text{in}} + 2 \cdot T_{\text{out}}}{1000}\right) \cdot \omega_{\text{modelo}} + \sum_{k \in \text{Tools}} \gamma_k + \delta_{\text{proofgate}} \right\rceil$$

Onde:
- **$\omega_{\text{modelo}}$ (Peso do Modelo no AI Gateway):**
  - Modelos rápidos/econômicos (`gemini-flash-lite` / `haiku` / local SLM): $\omega = 0.25$
  - Modelos balanceados (`gemini-flash` / `sonnet`): $\omega = 1.00$
  - Modelos de raciocínio profundo (`gemini-pro` / `opus`): $\omega = 3.50$
- **$\gamma_k$ (Custo de Ferramenta Externa):** Busca em catálogo SQL ($0.1$), chamada WhatsApp API ($0.2$), consulta oráculo/Web3 ($0.5$).
- **$\delta_{\text{proofgate}}$ (Validação Determinística e Receipt Criptográfico):** $0.25$ crédito por intenção auditada.

### Planos de Franquia de Créditos:
- **Starter:** `500 créditos / mês` (Ideal para 1 loja de comércio especializado com ~1.500 interações otimizadas via roteamento econômico).
- **Professional:** `2.000 créditos / mês` (Operação intensa com recomendações consultivas e relatórios).
- **Business / Enterprise:** `10.000 créditos / mês` (Multi-agentes, ProofGate B2B de alto volume e workflows complexos).

---

## 4. Margem de Contribuição e Simulação de Estágios de MRR

Faturamento automatizado não é sinônimo de lucro líquido. Cada cliente e produto é monitorado pela **Margem de Contribuição ($MC$)**:

$$MC = R - C_{\text{IA}} - C_{\text{infra}} - C_{\text{pagamentos}} - C_{\text{suporte}}$$

Onde:
- $C_{\text{IA}}$: Custo variável de tokens/inferência nos provedores de LLM.
- $C_{\text{infra}}$: Banco de dados (Postgres/Supabase), cache (Redis), hospedagem (Oracle Cloud Always Free / VPS).
- $C_{\text{pagamentos}}$: Taxas de processamento (MercadoPago PIX/Cartão ~1%–4,99%, Stripe ou gas Web3).
- $C_{\text{suporte}}$: Horas humanas operacionais dedicadas a implantação, ajustes e aprovação supervisionada.

### Metas de Validação Comercial em Três Estágios (MRR)

| Estágio | Clientes Pagantes Ativos | Ticket Mensal Médio | MRR Alvo | Custos Variáveis Estimados ($C_{\text{var}}$) | Margem de Contribuição ($MC$) | Eficiência ($\rho = \text{MRR}/C_{\text{var}}$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Validação** | 3 clientes | R$ 500 | **R$ 1.500 / mês** | R$ 250 / mês | R$ 1.250 (83,3%) | $6.0\times$ |
| **2. Tração** | 10 clientes | R$ 800 | **R$ 8.000 / mês** | R$ 1.200 / mês | R$ 6.800 (85,0%) | $6.67\times$ |
| **3. Expansão** | 25 clientes | R$ 1.000 | **R$ 25.000 / mês** | R$ 3.500 / mês | R$ 21.500 (86,0%) | $7.14\times$ |

> **Regra de Escala (Seção 12.6):** A meta imediata é conquistar os **3 primeiros clientes pagantes** (Estágio de Validação), identificar padrões comuns, padronizar o setup para menos de 4 horas humanas por cliente e só então escalar para o Estágio de Tração.

---

## 5. Arquitetura de Pagamentos Globais e Web3 em Três Etapas

Separamos rigorosamente **(1) Receber pagamentos**, **(2) Executar operações financeiras** e **(3) Tokenizar direitos**:

1. **Etapa 1 — Faturamento Convencional Imediato (Dias 1–40):**
   - **Brasil:** MercadoPago (PIX automatizado, links de pagamento e assinaturas recorrentes) integrado diretamente ao `card-chat` e ao faturamento da ValueCurator.
   - **Internacional:** Stripe / Invoice convencional com contratos claros de prestação de serviços.
2. **Etapa 2 — Liquidação Internacional em Stablecoins (Dias 41–75):**
   - Recebimento de Bounties, Grants (Superteam / Gitcoin) e clientes Web3 internacionais em **USDC** (Solana / EVM).
   - Carteira empresarial segregada, reconciliação automática de transações e contabilidade multi-moeda (BRL/USD/USDC) via `sovereign-budget` (mantendo a restrição termodinâmica $\Phi_{\text{buffer}} \ge 1.20$).
3. **Etapa 3 — Instrumentos On-Chain e Licenciamento Programável (Pós-Validação Comercial):**
   - Smart contracts (Anchor/Solana no `value-curator` e SPL Token-2022 no `eidos-tokenization`) para verificação on-chain de licenças do ProofGate e *Revenue Share* automatizado em repositórios coautorados, apenas quando houver demanda comercial comprovada e enquadramento jurídico definido.
