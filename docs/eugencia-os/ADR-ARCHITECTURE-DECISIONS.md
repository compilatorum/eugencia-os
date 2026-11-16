# 📐 ADR-ARCHITECTURE-DECISIONS — Registros de Decisão Arquitetural

> Documenta as decisões de engenharia tomadas na implementação do **Eugência OS & ValueCurator OS** em resposta direta à especificação `~/eugencia.pdf` e ao Code Review / Gap Analysis.

---

## ADR-001: Separação em 6 Bounded Contexts e 7 Camadas VOS (Desacoplamento UI $\leftrightarrow$ Domínio)

- **Contexto:** Aplicações monolíticas acopladas em um único arquivo HTML misturam interface, autenticação e regras de negócio, impedindo testes isolados e uso simultâneo via CLI, Emacs Org-mode e Web App.
- **Decisão:** Estruturar o núcleo em Python (`backend/app/engine.py`, `backend/app/models.py`, `backend/app/org_sync.py`, `backend/app/server.py`) separado da camada de visualização (`frontend/dist/index.html`) e organizar o domínio nos **6 Bounded Contexts**:
  1. `01 · Selfware Core` (Identidade, Flow Inbox, Preferências, Limites de Autonomia e Sincronização Org-mode)
  2. `02 · Opportunity Intelligence` (Dework, Superteam, Gitcoin, Clientes B2B e Scoring $\text{EV}/h$)
  3. `03 · Construct Graph` (Grafo SCADA dos 72 repositórios, 6 clusters, Work Packages e dependências)
  4. `04 · Research & Experiment OS` (Experimentos `E-001`..`E-003`, Ergonomia e $\Delta A_t > 0$)
  5. `05 · Delivery & Agent Runtime` (7 Agentes Humano-IA, AI Gateway $M^*$, ProofGate e Autonomia Calibrada)
  6. `06 · Reputation & Treasury` (Publicações baseadas em evidências `SHA-256`, Revenue Ledger e Créditos)

---

## ADR-002: Segurança Multi-Tenant (RLS), Isolamento por Organização e Concorrência Otimista

- **Contexto:** Sistemas multi-tenant exigem isolamento estrito entre organizações (`Organization A` nunca pode ler ou alterar registros da `Organization B`), ausência total de senhas em texto puro ou credenciais padrão (`admin/1234`) e proteção contra sobrescrita concorrente.
- **Decisão:**
  1. Versionar políticas explícitas de **Row-Level Security (RLS)** para PostgreSQL/Supabase em `infra/supabase_rls_policies.sql` baseadas em `auth.uid()` e `organization_members`.
  2. No motor relacional (`engine.py`), impor validação de escopo `org_id` (`verify_tenant_access`) com testes negativos automatizados.
  3. Implementar controle otimista de concorrência (`expected_version`) e **Transactional Event Outbox** (`domain_events`) para rastrear a cadeia:
     $$\text{Construct} \rightarrow \text{Opportunity} \rightarrow \text{Experiment} \rightarrow \text{Delivery} \rightarrow \text{Evidence} \rightarrow \text{Reputation} \rightarrow \text{Revenue}$$

---

## ADR-003: Formalismo de Autonomia Calibrada $A(a,t) = f(R_t, C_a, E_t, P_t)$

- **Contexto:** A autonomia de um agente não deve ser binária, mas graduada conforme o risco da tarefa e as evidências acumuladas.
- **Decisão:** Implementar a equação formal de autonomia calibrada:
  $$A(a,t) = \operatorname{ clamp }_{[0,1]}\Big( C_a \cdot (1 - 0.65 R_t) \cdot \min(1.0, 0.5 + 0.1 E_t) \cdot P_t \Big)$$
  Mapeando o score contínuo $A(a,t)$ nas 6 faixas operacionais:
  1. `01_OBSERVE_AND_SUMMARIZE`
  2. `02_RECOMMEND_AND_PRIORITIZE`
  3. `03_PREPARE_ARTIFACTS`
  4. `04_EXECUTE_IN_SANDBOX`
  5. `05_EXECUTE_REVERSIBLE_WITH_APPROVAL` (`APPROVAL_ONLY` no ProofGate)
  6. `06_EXECUTE_AUTONOMOUS_WITHIN_LIMITS` (Sujeito a $R_t \le 0.30$ e políticas determinísticas)
