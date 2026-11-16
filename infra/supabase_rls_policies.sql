-- ============================================================================
-- Eugência OS & ValueCurator OS — PostgreSQL / Supabase Schema & RLS Policies
-- Addresses ChatGPT Review Section 2.1 (P0 Security & Multi-Tenant Isolation)
-- and Section 2.2 (Optimistic Concurrency & Transactional Event Outbox)
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 1. Core Multi-Tenant Identity (Supabase Auth Integration)
CREATE TABLE IF NOT EXISTS public.organizations (
    id TEXT PRIMARY KEY DEFAULT ('org:' || uuid_generate_v4()::text),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    plan_tier TEXT NOT NULL DEFAULT 'Starter',
    credits_quota INTEGER NOT NULL DEFAULT 500,
    credits_used INTEGER NOT NULL DEFAULT 0,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.organization_members (
    org_id TEXT NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL, -- Maps directly to Supabase auth.uid()
    role TEXT NOT NULL CHECK (role IN ('owner', 'admin', 'operator', 'viewer')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (org_id, user_id)
);

-- 2. Bounded Context 01..06 Operational Tables (with org_id scope & optimistic version)
CREATE TABLE IF NOT EXISTS public.flow_inbox (
    id TEXT PRIMARY KEY DEFAULT ('flw:' || uuid_generate_v4()::text),
    org_id TEXT NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    source TEXT NOT NULL,
    space TEXT NOT NULL,
    classified_type TEXT NOT NULL,
    suggested_cluster TEXT NOT NULL,
    suggested_destination TEXT NOT NULL,
    assigned_agent TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'curated',
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.proofgate_receipts (
    id TEXT PRIMARY KEY DEFAULT ('rcp:' || uuid_generate_v4()::text),
    org_id TEXT NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    domain TEXT NOT NULL,
    agent_role TEXT NOT NULL,
    action TEXT NOT NULL,
    payload_json JSONB NOT NULL,
    policy_status TEXT NOT NULL,
    validation_reasons_json JSONB NOT NULL,
    requires_human BOOLEAN NOT NULL DEFAULT true,
    approval_status TEXT NOT NULL,
    approved_by TEXT,
    execution_status TEXT NOT NULL,
    receipt_hash TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3. Transactional Event Outbox:
-- Construct -> Opportunity -> Experiment -> Delivery -> Evidence -> Reputation -> Revenue
CREATE TABLE IF NOT EXISTS public.domain_events_outbox (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id TEXT NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    bounded_context TEXT NOT NULL,
    event_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    payload_json JSONB NOT NULL,
    published BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 4. Enable Row-Level Security (RLS) on All Private Tables (Zero Cross-Tenant Leakage)
ALTER TABLE public.organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.organization_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.flow_inbox ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.proofgate_receipts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.domain_events_outbox ENABLE ROW LEVEL SECURITY;

-- Helper function to check membership for current authenticated Supabase user
CREATE OR REPLACE FUNCTION public.user_belongs_to_org(target_org_id TEXT)
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1
    FROM public.organization_members
    WHERE org_id = target_org_id
      AND user_id = auth.uid()
  );
$$;

-- Strict Tenant Isolation Policies
CREATE POLICY org_isolation_select ON public.organizations
    FOR SELECT USING (public.user_belongs_to_org(id));

CREATE POLICY flow_inbox_tenant_isolation ON public.flow_inbox
    FOR ALL
    USING (public.user_belongs_to_org(org_id))
    WITH CHECK (public.user_belongs_to_org(org_id));

CREATE POLICY proofgate_tenant_isolation ON public.proofgate_receipts
    FOR ALL
    USING (public.user_belongs_to_org(org_id))
    WITH CHECK (public.user_belongs_to_org(org_id));

CREATE POLICY outbox_tenant_isolation ON public.domain_events_outbox
    FOR ALL
    USING (public.user_belongs_to_org(org_id))
    WITH CHECK (public.user_belongs_to_org(org_id));
