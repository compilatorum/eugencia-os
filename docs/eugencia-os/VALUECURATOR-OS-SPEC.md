# 🏗️ VALUECURATOR-OS-SPEC — Especificação Técnica da Infraestrutura (7 Camadas)

> **Princípio Arquitetural:** Cada produto vertical (`card-chat`, `ProofGate`, `GrantOS`, `NeuroCoder`) possui sua própria interface enxuta, mas compartilha a mesma infraestrutura empresarial multi-tenant: o **ValueCurator OS (VOS)**.

---

## 1. Equação Arquitetural em Sete Camadas

$$VOS = I + B + AI + M + T + O + G$$

| Camada | Símbolo | Componente | Responsabilidade Técnica |
| :---: | :---: | :--- | :--- |
| **1. Identity** | $I$ | **Identity & Access** | Autenticação, usuários (`User`), organizações (`Organization`), workspaces (`Workspace`) e RBAC |
| **2. Business** | $B$ | **Billing & Entitlements** | Planos (`Subscription`), faturas (`Invoice`), carteira de créditos normalizados (`Usage`) e rate limits |
| **3. Intelligence** | $AI$ | **AI Gateway** | Roteamento ótimo de modelos ($M^*$), controle de custos, latência, fallback e telemetria de tokens |
| **4. Agents** | $O$ | **Agent & Workflow Runtime** | Registro e execução dos 7 agentes da Equipe Humano-IA e workflows com níveis de autonomia L0–L4 |
| **5. Memory** | $M$ | **Knowledge & RAG** | Persistência relacional (PostgreSQL/SQLite), memória semântica (`pgvector`), contexto e histórico |
| **6. Tools** | $T$ | **Integration Layer** | Conectores padronizados com GitHub, WhatsApp Business API, MercadoPago, Farcaster, Solana/Pyth/Jupiter e Emacs Org-mode |
| **7. Governance** | $G$ | **ProofGate & Observability** | Validação determinística de políticas, aprovação humana (*HITL*), recibos criptográficos (`Receipt`) e auditoria |

---

## 2. Modelo de Dados Multi-Tenant (Entidades Centrais)

O núcleo relacional suporta múltiplas organizações, múltiplos projetos por usuário e rastreabilidade completa de ponta a ponta:

1. **`Organization`**: Cliente B2B ou unidade interna (`id`, `name`, `slug`, `tier`, `credits_balance`, `credits_quota`, `created_at`).
2. **`User`**: Operador humano ou administrador (`id`, `org_id`, `email`, `name`, `role`).
3. **`Workspace`**: Ambiente isolado de operação (`id`, `org_id`, `name`, `cockpit_mode` [`hybrid`, `web`, `emacs`]).
4. **`Product`**: Produto contratado ou ativo no workspace (`id`, `code`, `name`, `cluster`, `commercial_unit`, `wip_active`, `setup_fee_brl`, `monthly_fee_brl`).
5. **`Agent`**: Agente especializado registrado (`id`, `role_code`, `name`, `responsibility`, `autonomy_level` [`L0`..`L4`], `default_model`).
6. **`Workflow`**: Processo automatizado (`id`, `product_id`, `name`, `steps_json`, `autonomy_level`, `tests_passed`, `evidences_count`, `controls_verified`).
7. **`Execution`**: Instância de execução de um workflow ou intenção (`id`, `workflow_id`, `org_id`, `status`, `model_used`, `credits_consumed`, `cost_brl`, `latency_ms`, `human_minutes`).
8. **`Usage`**: Razão contábil de consumo de créditos (`id`, `org_id`, `execution_id`, `tokens_in`, `tokens_out`, `credits_delta`, `reason`).
9. **`Subscription` & `Invoice`**: Gestão comercial recorrente (`id`, `org_id`, `plan_tier` [`Starter`, `Professional`, `Business`], `mrr_brl`, `status`).
10. **`Evidence`**: Artefato verificável de conclusão (`id`, `project_name`, `work_package`, `title`, `artifact_uri`, `commit_Or_pr`, `sha256_hash`, `verified`).
11. **`Approval` & `ProofGateReceipt`**: Registro de governança (`id`, `intent_id`, `domain`, `action`, `policy_status`, `requires_human`, `approved_by`, `receipt_hash`, `created_at`).

---

## 3. Especificação Formal da Camada 3: AI Gateway

O **AI Gateway** atua como controlador econômico e operacional de todas as chamadas de IA:

$$A(s) = \operatorname{Validate}\Big[\operatorname{Execute}\big(\operatorname{Route}(s)\big)\Big]$$

Onde $s$ é uma solicitação de serviço contendo `{task_type, min_quality, latency_sensitivity, risk_sensitivity, estimated_tokens, org_id}`.

### Algoritmo de Seleção Ótima de Modelo ($M^*$)

$$M^* = \arg\min_{m \in M_{\text{eligible}}} \Big[ C(m) + \lambda L(m) + \mu R(m) \Big] \quad \text{sujeito a} \quad Q(m) \ge Q_{\min}$$

Onde:
- $M_{\text{eligible}} = \{ m \in M \mid Q(m) \ge Q_{\min} \}$ filtra os modelos que atendem à qualidade mínima exigida pela tarefa.
- $C(m) \in [0, 1]$: Custo normalizado por 1k tokens do modelo $m$.
- $L(m) \in [0, 1]$: Latência média normalizada do modelo $m$, ponderada pelo coeficiente $\lambda \ge 0$.
- $R(m) \in [0, 1]$: Risco operacional (alucinação, instabilidade de schema ou dependência externa), ponderado por $\mu \ge 0$.

---

## 4. Especificação Formal da Camada 7: ProofGate Transversal

O **ProofGate** generaliza a arquitetura determinística de custódia/políticas do `value-curator` para **qualquer agente da Eugência**:

$$\text{Intent} \rightarrow \text{Policy} \rightarrow \text{Validation} \rightarrow \text{Approval} \rightarrow \text{Execution} \rightarrow \text{Receipt}$$

### Políticas Determinísticas pré-configuradas por Domínio:
1. **`card-chat` (Comércio Especializado):**
   - `max_discount_pct <= 10.0` (descontos acima de 10% exigem aprovação humana explícita; acima de 25% são bloqueados).
   - `verified_catalog_item == True` e `stock_available >= quantity` (impede venda de item sem estoque ou com preço inventado).
2. **`grantos` (Submissão de Grants):**
   - `has_mandatory_docs == True`, `single_funding_category == True` e `duplicate_submission == False` (impede dupla cobrança de mesmo entregável).
3. **`finance` (Tesouraria & Web3):**
   - `execution_mode == "APPROVAL_ONLY"` para movimentações de capital, verificando `fiduciary_buffer_ratio >= 1.20` e `defi_health_factor >= 1.50`.
4. **`neurocoder` (Engenharia de Software):**
   - `destructive_git_or_fs == False` e `clean_room_tests_passed == True` antes de deploy em branch principal.
5. **`farcaster` (Comunicação Pública):**
   - `backed_by_evidence_id != None` e `human_editorial_approved == True` (proíbe publicação automática sem evidência verificável e revisão humana).

### Emissão de Receipt Criptográfico
Toda avaliação gera um `ProofGateReceipt` imutável cujo hash é calculado de forma determinística:
$$\text{ReceiptHash} = \operatorname{SHA256}\big(\text{IntentJSON} \parallel \text{PolicyVersion} \parallel \text{ValidationDecision} \parallel \text{ApproverID} \parallel \text{TimestampISO}\big)$$

---

## 5. Máquina de Estados de Autonomia Progressiva (L0–L4)

Nenhum workflow inicia em autonomia total. A promoção de nível $L_n \rightarrow L_{n+1}$ é governada pela condição formal:

$$L_{n+1} \Leftarrow \text{Testes} \land \text{Evidências} \land \text{Controles}$$

| Nível | Estado | Operação | Critério Objetivo para Promoção ao Próximo Nível |
| :---: | :--- | :--- | :--- |
| **L0** | `Manual` | Humano executa integralmente | Procedimento documentado em template reproduzível |
| **L1** | `Assisted` | IA recomenda; humano executa | $\ge 5$ recomendações validadas + schema de entrada/saída definido |
| **L2** | `Supervised` | IA prepara a execução; humano aprova via ProofGate (`APPROVAL_ONLY`) | $\ge 15$ testes automatizados aprovados + $\ge 3$ evidências reais sem falha crítica |
| **L3** | `Guarded` | IA executa autonomamente dentro de limites estritos do Policy Engine | $\ge 50$ execuções auditadas com 100% de conformidade + kill-switch ativo |
| **L4** | `Autonomous` | Execução autônoma contínua com monitoramento e telemetria SCADA | Auditoria de segurança completa + margem de erro zero em operações críticas |
