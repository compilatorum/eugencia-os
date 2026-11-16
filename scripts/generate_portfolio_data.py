#!/usr/bin/env python3
"""
Curates and classifies all 72 repositories from compilatorum and smp-sandramariapereira
according to the Eugência OS / ValueCurator strategic framework (Sections 2, 8, and 9 of eugencia.pdf).
Generates:
  - data/portfolio_assets.json
  - docs/eugencia-os/PORTFOLIO-ASSETS-REGISTER.md
"""
import json
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_REPOS_PATH = BASE_DIR / "data" / "github_repos_raw.jsonl"
ASSETS_JSON_PATH = BASE_DIR / "data" / "portfolio_assets.json"
REGISTER_MD_PATH = BASE_DIR / "docs" / "eugencia-os" / "PORTFOLIO-ASSETS-REGISTER.md"

# Explicit strategic classification rules per repository name based on eugencia.pdf
CURATED_OVERRIDES: Dict[str, Dict[str, Any]] = {
    # Motor 1: Card-Chat (Receita Comercial Imediata - P1)
    "card-chat": {
        "cluster": "ValueCurator",
        "commercial_unit": "Commerce",
        "stage": "Construct",
        "asset_class": "C — Commercial",
        "asset_type": "Commercial",
        "priority": "P1",
        "product_potential": "Alta (Motor 1: AI Commerce Agent — Service-as-a-Software para Vespa TCG e varejo especializado)",
        "dependencies": ["valuecurator", "harness-engineering", "WhatsApp Business API", "MercadoPago", "PostgreSQL/Redis"],
        "evidence": "README funcional c/ WhatsApp Business API, Node.js/TS, Gemini, catálogo e roteamento em BH (Vespa TCG)",
        "next_milestone": "Resolver divergência Node.js vs Python, integrar ProofGate de descontos e MercadoPago (Dias 22–40)",
        "monetization": "Setup (R$ 1.500–6.000) + Mensalidade (R$ 400–1.500) + Créditos de IA",
        "autonomy_level": "L2",
        "wip_active": True,
    },
    # Motor 2: ValueCurator / ProofGate (Ativo Estratégico Web3 - P1)
    "value-curator": {
        "cluster": "ValueCurator",
        "commercial_unit": "Agent Assurance",
        "stage": "Construct",
        "asset_class": "A — Core IP",
        "asset_type": "Core IP / Open Core",
        "priority": "P1",
        "product_potential": "Muito Alta (Motor 2: ProofGate-as-a-Service — segurança, validação e governança de agentes)",
        "dependencies": ["vc", "KAIROS-Engine", "oracle", "Anchor/Solana", "Pyth", "Jupiter"],
        "evidence": "SDK TypeScript, Smart Contract Anchor/Rust, Policy Engine determinístico, receipts criptográficos, demo Devnet/Mainnet APPROVAL_ONLY",
        "next_milestone": "Empacotar ProofGate API + SDK documentado + testes adversariais em modo APPROVAL_ONLY (Dias 56–75)",
        "monetization": "Licenciamento + API + Pilotos B2B (Agent Assurance) + Security/Solana Grants (WP1–WP3)",
        "autonomy_level": "L3",
        "wip_active": True,
    },
    "valuecurator": {
        "cluster": "ValueCurator",
        "commercial_unit": "Agent Assurance",
        "stage": "Construct",
        "asset_class": "A — Core IP",
        "asset_type": "Core IP",
        "priority": "P1",
        "product_potential": "Alta (Monorepo compartilhado ValueCurator + KAIROS-Engine + discovery-agent)",
        "dependencies": ["KAIROS-Engine", "value-curator", "vc"],
        "evidence": "Monorepo pnpm com apps, packages, docs e infraestrutura compartilhada",
        "next_milestone": "Alinhar titularidade jurídica/IP e extrair módulos para o ValueCurator OS (Dias 41–55)",
        "monetization": "Núcleo compartilhado VOS + Licenciamento B2B",
        "autonomy_level": "L2",
        "wip_active": False,
    },
    "vc": {
        "cluster": "ValueCurator",
        "commercial_unit": "Holding Core",
        "stage": "Construct",
        "asset_class": "A — Core IP",
        "asset_type": "Core IP",
        "priority": "P1",
        "product_potential": "Estratégico (Núcleo estratégico: ontologia, curadoria, governança e arquitetura VOS)",
        "dependencies": ["value-curator", "oracle", "proterol"],
        "evidence": "Especificações de governança, ontologia de curadoria de valor e modelos formais",
        "next_milestone": "Consolidar contratos de dados das 7 camadas do ValueCurator OS",
        "monetization": "Retenção de IP / Infraestrutura base da Holding",
        "autonomy_level": "L2",
        "wip_active": False,
    },
    "KAIROS-Engine": {
        "cluster": "ValueCurator",
        "commercial_unit": "Agent Assurance",
        "stage": "Construct",
        "asset_class": "A — Core IP",
        "asset_type": "Core IP",
        "priority": "P1",
        "product_potential": "Alta (Motor de execução e decisão multicapital KAIROS)",
        "dependencies": ["valuecurator", "oracle"],
        "evidence": "Implementação TypeScript no espaço compartilhado com integração ValueCurator",
        "next_milestone": "Formalizar licenciamento e fronteira de IP entre Compilatorum e espaço compartilhado",
        "monetization": "Core IP embarcado no ValueCurator OS",
        "autonomy_level": "L2",
        "wip_active": False,
    },
    "oracle": {
        "cluster": "ValueCurator",
        "commercial_unit": "Agent Assurance",
        "stage": "Experiment",
        "asset_class": "A — Core IP",
        "asset_type": "Core IP",
        "priority": "P1",
        "product_potential": "Média/Alta (ORACLE·GEN: Computação Oracular Generativa e Kernel Epistemológico)",
        "dependencies": ["vc", "lakehouse", "value-curator"],
        "evidence": "Especificação arquitetural e kernel epistemológico em Python",
        "next_milestone": "Integrar como provedor de validação e contexto verificável no ProofGate",
        "monetization": "Componente de infraestrutura interna / Core IP",
        "autonomy_level": "L1",
        "wip_active": False,
    },
    # Motor 3: Harness Engineering / NeuroCoder (Produtividade Interna - P0/P2)
    "harness-engineering": {
        "cluster": "NeuroCoder",
        "commercial_unit": "Agent Engineering",
        "stage": "Construct",
        "asset_class": "D — Internal Tool",
        "asset_type": "Internal / Open Core",
        "priority": "P0",
        "product_potential": "Muito Alta como Fábrica Interna (Motor 3: Orquestração DAG, worktrees, memória, +131 testes)",
        "dependencies": ["promptcraft", "neurocoder-pwa", "planner"],
        "evidence": "Arquitetura integrada TypeScript com DAG, Graphify, agentes em equipe, worktrees e suíte de testes",
        "next_milestone": "Reproduzir os +131 testes em ambiente limpo e padronizar templates de microsserviços (Dias 8–21)",
        "monetization": "Redução de horas humanas (aumento de Alavancagem L) + futuro Grant de Security/Tooling",
        "autonomy_level": "L3",
        "wip_active": False,
    },
    "neurocoder-pwa": {
        "cluster": "NeuroCoder",
        "commercial_unit": "Agent Engineering",
        "stage": "Experiment",
        "asset_class": "C — Commercial",
        "asset_type": "Commercial",
        "priority": "P2",
        "product_potential": "Alta (Interface PWA para engenharia de IA e automação assistida)",
        "dependencies": ["harness-engineering", "promptcraft", "planner"],
        "evidence": "Protótipo TypeScript PWA de codificação agêntica",
        "next_milestone": "Conectar ao AI Gateway do ValueCurator OS na Fase 3",
        "monetization": "AI Workflow / Engineering Agent (Setup + Mensalidade)",
        "autonomy_level": "L2",
        "wip_active": False,
    },
    "promptcraft": {
        "cluster": "NeuroCoder",
        "commercial_unit": "Agent Engineering",
        "stage": "Construct",
        "asset_class": "B — Open Core",
        "asset_type": "OSS / Internal",
        "priority": "P2",
        "product_potential": "Alta (Schemas reutilizáveis Open Core + pipeline privado de curadoria + extração comercial)",
        "dependencies": ["harness-engineering", "proterol"],
        "evidence": "Promptcraft Studio HTML/JS + meta-prompts estruturados e biblioteca de templates",
        "next_milestone": "Separar schemas públicos (Open Core para Developer Tooling Grants) do pipeline interno",
        "monetization": "Developer Tooling Grants + AI Knowledge Agent",
        "autonomy_level": "L2",
        "wip_active": False,
    },
    "planner": {
        "cluster": "NeuroCoder",
        "commercial_unit": "Agent Engineering",
        "stage": "Experiment",
        "asset_class": "D — Internal Tool",
        "asset_type": "Internal",
        "priority": "P2",
        "product_potential": "Média (Gestão visual de contexto Human-AI Pair Programming e Self-Verbs)",
        "dependencies": ["harness-engineering", "context-planner-pwa"],
        "evidence": "Interface web interativa construída e avaliada no relatório de mockups soberanos",
        "next_milestone": "Incorporar conceitos de Self-Verbs ao Flow Inbox do Eugência OS",
        "monetization": "Produtividade interna (Selfware)",
        "autonomy_level": "L1",
        "wip_active": False,
    },
    "emacs": {
        "cluster": "NeuroCoder",
        "commercial_unit": "Agent Engineering",
        "stage": "Construct",
        "asset_class": "D — Internal Tool",
        "asset_type": "Internal",
        "priority": "P0",
        "product_potential": "Essencial para Ergonomia (Cockpit Cognitivo Emacs + Org-mode + Magit + HITL)",
        "dependencies": ["omni-dual-brain"],
        "evidence": "Configuração Emacs Lisp + dashboards PWA de servidor Emacs",
        "next_milestone": "Integrar modo eugencia-os.el com sincronização bidirecional Org <-> SQLite/FastAPI",
        "monetization": "Produtividade interna e redução de atrito cognitivo",
        "autonomy_level": "L2",
        "wip_active": False,
    },
    "omni-dual-brain": {
        "cluster": "NeuroCoder",
        "commercial_unit": "Agent Engineering",
        "stage": "Construct",
        "asset_class": "A — Core IP",
        "asset_type": "Core IP / Internal",
        "priority": "P1",
        "product_potential": "Alta (Cérebro Único com Duas Fronteiras: LangGraph + MCP + WhatsApp Debounce + Emacs HITL)",
        "dependencies": ["emacs", "harness-engineering", "farcaster-nexus"],
        "evidence": "Arquitetura Python integrando LangGraph, MCP (GitHub/Neynar/KarmaHQ), WhatsApp e Emacs HITL",
        "next_milestone": "Utilizar como referência do Agent Runtime (Camada 4) e Tools Layer (Camada 6) do VOS",
        "monetization": "Infraestrutura base para AI Workflow Agent e AI Commerce Agent",
        "autonomy_level": "L3",
        "wip_active": False,
    },
    # Cluster GrantOS (Financiamento e Inteligência de Capital - P1)
    "concurseiro-grants": {
        "cluster": "GrantOS",
        "commercial_unit": "Intelligence",
        "stage": "Construct",
        "asset_class": "C — Commercial",
        "asset_type": "Commercial / Internal",
        "priority": "P1",
        "product_potential": "Alta (Sistema de inteligência de capital: Project -> FundingThesis -> Opportunity -> WorkPackage -> Evidence -> Funding)",
        "dependencies": ["governaut-os", "DAO", "farcaster-nexus", "IPIT"],
        "evidence": "Concurseiro de Grants v2.0 com taxonomia de 5 categorias e experimento Farcaster x IPIT",
        "next_milestone": "Alimentar módulo Opportunity Intelligence do Eugência OS e estruturar Grant Stacking do ProofGate",
        "monetization": "Captação própria de Grants + pacote comercial Grant Intelligence (Setup R$ 500–1.500 + R$ 150–500/mês)",
        "autonomy_level": "L2",
        "wip_active": False,
    },
    "governaut-os": {
        "cluster": "GrantOS",
        "commercial_unit": "Intelligence",
        "stage": "Construct",
        "asset_class": "B — Open Core",
        "asset_type": "OSS / Commercial",
        "priority": "P1",
        "product_potential": "Alta (Orquestração Multi-Agente L0–L5 para ciclo completo de DAO Proposals e governança Web4)",
        "dependencies": ["concurseiro-grants", "DAO", "value-curator"],
        "evidence": "Repositório local e remoto com pacote Python governaut_os e suíte de testes pytest",
        "next_milestone": "Reutilizar modelo de níveis de autonomia L0–L5 na governança do Eugência OS",
        "monetization": "Grants de Governança DAO + consultoria/licenciamento para DAOs",
        "autonomy_level": "L3",
        "wip_active": False,
    },
    "DAO": {
        "cluster": "GrantOS",
        "commercial_unit": "Intelligence",
        "stage": "Experiment",
        "asset_class": "E — Research",
        "asset_type": "OSS",
        "priority": "P2",
        "product_potential": "Média (Estruturas de governança descentralizada e tesouraria)",
        "dependencies": ["governaut-os", "concurseiro-grants"],
        "evidence": "Artefatos e desenhos de governança coletiva",
        "next_milestone": "Manter como referência para clientes DAO do pacote ProofGate / Agent Assurance",
        "monetization": "Indireta via ProofGate B2B para DAOs",
        "autonomy_level": "L1",
        "wip_active": False,
    },
    "maha-grid": {
        "cluster": "GrantOS",
        "commercial_unit": "Intelligence",
        "stage": "Construct",
        "asset_class": "E — Research",
        "asset_type": "OSS / Research",
        "priority": "P2",
        "product_potential": "Alta para Grants (Governança Agêntica, Farcaster Mini App Frames v2, cadCAD, Kit de Grants W3F/Polkadot/Nouns)",
        "dependencies": ["farcaster-nexus", "concurseiro-grants", "cadcad-explorer"],
        "evidence": "Repositório Python completo com kit de grants públicos e simulação cadCAD",
        "next_milestone": "Submeter propostas qualificadas via GrantOS mantendo separação estrita de escopo (Grant Stacking)",
        "monetization": "Grants de Bens Públicos e Ecossistema (W3F, Polkadot, Nouns, Gitcoin)",
        "autonomy_level": "L2",
        "wip_active": False,
    },
    "farcaster-nexus": {
        "cluster": "GrantOS",
        "commercial_unit": "Distribution",
        "stage": "Construct",
        "asset_class": "D — Internal Tool",
        "asset_type": "Internal / OSS",
        "priority": "P2",
        "product_potential": "Alta como Canal de Distribuição e Reputação (Interaction -> Contribution -> Evidence -> Recognition -> Funding)",
        "dependencies": ["concurseiro-grants", "IPIT", "omni-dual-brain"],
        "evidence": "Integração TypeScript com Farcaster/Neynar e experimento de folksonomia/grafo social",
        "next_milestone": "Conectar ao módulo Reputation & Publishing OS para radar semanal assistido (Dias 76–90)",
        "monetization": "Aquisição orgânica de clientes, distribuição de bounties e Gitcoin Grants",
        "autonomy_level": "L2",
        "wip_active": False,
    },
    "IPIT": {
        "cluster": "GrantOS",
        "commercial_unit": "Intelligence",
        "stage": "Experiment",
        "asset_class": "E — Research",
        "asset_type": "Research",
        "priority": "P2",
        "product_potential": "Média/Alta (Experimento de inteligência coletiva e atribuição de contribuições verificáveis)",
        "dependencies": ["concurseiro-grants", "farcaster-nexus"],
        "evidence": "Implementação Python recente integrada ao experimento Concurseiro de Grants v2.0",
        "next_milestone": "Documentar evidências para rodadas de financiamento comunitário (Gitcoin)",
        "monetization": "Grants de pesquisa e bens públicos digitais",
        "autonomy_level": "L1",
        "wip_active": False,
    },
    # Cluster Capital Intelligence (P3)
    "invest-os": {
        "cluster": "Capital Intelligence",
        "commercial_unit": "Capital",
        "stage": "Construct",
        "asset_class": "A — Core IP",
        "asset_type": "Core IP",
        "priority": "P3",
        "product_potential": "Alta no longo prazo (Sistema adaptativo de suporte ao investidor Web3, KAIROS 8 capitais, econofísica)",
        "dependencies": ["sovereign-budget", "neurosimbolic-trader", "value-curator"],
        "evidence": "Destilação de 17 documentos em spec integrada Python + mockups InvestmentOS_v3.html",
        "next_milestone": "Manter estacionado comercialmente (WIP <= 2); reutilizar Policy Engine no ProofGate",
        "monetization": "Exploração comercial posterior (Fase P3)",
        "autonomy_level": "L2",
        "wip_active": False,
    },
    "neurosimbolic-trader": {
        "cluster": "Capital Intelligence",
        "commercial_unit": "Capital",
        "stage": "Experiment",
        "asset_class": "E — Research",
        "asset_type": "Research",
        "priority": "P3",
        "product_potential": "Média (Pesquisa neuro-simbólica aplicada a mercados)",
        "dependencies": ["invest-os", "value-curator"],
        "evidence": "Protótipo Python público de trading neuro-simbólico",
        "next_milestone": "Estacionado (P3) — usar apenas como caso de teste de mandatos restritivos no ProofGate",
        "monetization": "Pesquisa / Uso interno",
        "autonomy_level": "L1",
        "wip_active": False,
    },
    "sovereign-budget": {
        "cluster": "Capital Intelligence",
        "commercial_unit": "Capital",
        "stage": "Construct",
        "asset_class": "D — Internal Tool",
        "asset_type": "Internal",
        "priority": "P3",
        "product_potential": "Média/Alta (Controle orçamentário soberano Beancount, Buffer Fiduciário >= 1.20x e DeFi Health Factor >= 1.50)",
        "dependencies": ["invest-os"],
        "evidence": "Repositório local/remoto Python + painel termodinâmico sovereign_budget_thermo.html",
        "next_milestone": "Utilizar para contabilidade interna de receitas, custos variáveis e margem de contribuição da Eugência",
        "monetization": "Gestão financeira interna (Selfware)",
        "autonomy_level": "L2",
        "wip_active": False,
    },
    "jagannatha-hora-re": {
        "cluster": "Capital Intelligence",
        "commercial_unit": "Capital",
        "stage": "Experiment",
        "asset_class": "E — Research",
        "asset_type": "Research",
        "priority": "P3",
        "product_potential": "Nicho/Pesquisa (Engenharia reversa de efemérides e ciclos temporais em Python/C++)",
        "dependencies": [],
        "evidence": "Repositório público Python ativo com análise binária e algoritmos de precisão",
        "next_milestone": "Preservar no Laboratório de Exploração sem pressão de monetização imediata",
        "monetization": "Pesquisa aberta / Reputação técnica",
        "autonomy_level": "L1",
        "wip_active": False,
    },
    "claude-para-investidores": {
        "cluster": "Capital Intelligence",
        "commercial_unit": "Capital",
        "stage": "Experiment",
        "asset_class": "B — Open Core",
        "asset_type": "OSS / Research",
        "priority": "P3",
        "product_potential": "Média (Engenharia reversa e upgrade de prompts financeiros estruturados)",
        "dependencies": ["promptcraft", "invest-os"],
        "evidence": "Repositório público HTML/Markdown recém-atualizado",
        "next_milestone": "Catalogar templates no Promptcraft e manter como ativo de reputação",
        "monetization": "Adoção comunitária / Lead magnet para Capital Intelligence",
        "autonomy_level": "L1",
        "wip_active": False,
    },
    "pixelcoin": {
        "cluster": "Capital Intelligence",
        "commercial_unit": "Capital",
        "stage": "Experiment",
        "asset_class": "B — Open Core",
        "asset_type": "OSS / Internal",
        "priority": "P3",
        "product_potential": "Média (Interface generativa de inteligência econômica, vetores SVG e MCP)",
        "dependencies": ["storybook-genui"],
        "evidence": "Repositório local/remoto Python + pixelcoin_generative_ui.html",
        "next_milestone": "Reaproveitar componentes visuais no Portfolio OS",
        "monetization": "Design system interno e vitrine técnica",
        "autonomy_level": "L1",
        "wip_active": False,
    },
    # Infraestrutura de Dados
    "lakehouse": {
        "cluster": "ValueCurator",
        "commercial_unit": "Data Intelligence",
        "stage": "Construct",
        "asset_class": "D — Internal Tool",
        "asset_type": "Internal / OSS",
        "priority": "P2",
        "product_potential": "Alta (Lakehouse Multimodal com PostgreSQL + pgvector + pipelines ETL)",
        "dependencies": ["oracle", "valuecurator"],
        "evidence": "Repositório local e remoto Python com arquitetura PostgreSQL/pgAdmin4",
        "next_milestone": "Servir como camada de persistência e memória (Camada 5) do ValueCurator OS",
        "monetization": "Pacote Data Intelligence (Setup + mensalidade) + Grants Filecoin/The Graph",
        "autonomy_level": "L2",
        "wip_active": False,
    },
    # Cluster GeoIA (P3)
    "geoIA-UrbanFlow": {
        "cluster": "GeoIA",
        "commercial_unit": "Territorial Intelligence",
        "stage": "Seed",
        "asset_class": "E — Research",
        "asset_type": "Research / Commercial",
        "priority": "P3",
        "product_potential": "Média (Plataforma de navegação para micromobilidade urbana sustentável)",
        "dependencies": ["educacao-territorios", "EduAtlas"],
        "evidence": "Repositório no espaço compartilhado com Sandra",
        "next_milestone": "Estacionado (P3) — verificar titularidade e manter para editais de cidades inteligentes",
        "monetization": "Editais de inovação urbana / Grants",
        "autonomy_level": "L0",
        "wip_active": False,
    },
    "educacao-territorios": {
        "cluster": "GeoIA",
        "commercial_unit": "Territorial Intelligence",
        "stage": "Seed",
        "asset_class": "E — Research",
        "asset_type": "Research",
        "priority": "P3",
        "product_potential": "Média (Inteligência territorial aplicada à educação)",
        "dependencies": ["EduAtlas", "geoIA-UrbanFlow"],
        "evidence": "Protótipo TypeScript no espaço compartilhado com Sandra",
        "next_milestone": "Estacionado (P3) — aguardar janela de edital público específico",
        "monetization": "Grants educacionais / GovTech",
        "autonomy_level": "L0",
        "wip_active": False,
    },
    "EduAtlas": {
        "cluster": "GeoIA",
        "commercial_unit": "Territorial Intelligence",
        "stage": "Seed",
        "asset_class": "E — Research",
        "asset_type": "Research",
        "priority": "P3",
        "product_potential": "Média (Mapeamento e atlas educacional)",
        "dependencies": ["educacao-territorios"],
        "evidence": "Repositório no espaço compartilhado com Sandra",
        "next_milestone": "Estacionado (P3)",
        "monetization": "Grants de impacto social",
        "autonomy_level": "L0",
        "wip_active": False,
    },
    # Cluster AROS (P3)
    "aros-voice-kernel": {
        "cluster": "AROS",
        "commercial_unit": "Cognitive Interfaces",
        "stage": "Experiment",
        "asset_class": "A — Core IP",
        "asset_type": "Core IP / Research",
        "priority": "P3",
        "product_potential": "Média/Alta (Kernel mobile Kotlin de voz e biofeedback vocal)",
        "dependencies": ["prompt-audiofeedback", "omni-laboratory"],
        "evidence": "Repositório Kotlin no espaço compartilhado + especificações de biofeedback vocal",
        "next_milestone": "Estacionado (P3) — preservar IP e avaliar editais de pesquisa em saúde/biofeedback",
        "monetization": "Grants de pesquisa e inovação / App futuro",
        "autonomy_level": "L1",
        "wip_active": False,
    },
    "prompt-audiofeedback": {
        "cluster": "AROS",
        "commercial_unit": "Cognitive Interfaces",
        "stage": "Experiment",
        "asset_class": "E — Research",
        "asset_type": "Research",
        "priority": "P3",
        "product_potential": "Média (AROS Voice Kernel: Biofeedback Vocal Idiográfico para Google Play)",
        "dependencies": ["aros-voice-kernel"],
        "evidence": "Repositório local/remoto Python + PDF técnico detalhado",
        "next_milestone": "Estacionado (P3)",
        "monetization": "Grants de pesquisa aplicada",
        "autonomy_level": "L1",
        "wip_active": False,
    },
    "digital-twin": {
        "cluster": "AROS",
        "commercial_unit": "Cognitive Interfaces",
        "stage": "Seed",
        "asset_class": "E — Research",
        "asset_type": "Research",
        "priority": "P3",
        "product_potential": "Baixa/Média no curto prazo (Projeto Dados Sintéticos e gêmeo digital)",
        "dependencies": ["omni-laboratory"],
        "evidence": "Repositório no espaço compartilhado com Sandra",
        "next_milestone": "Estacionado (P3)",
        "monetization": "Pesquisa",
        "autonomy_level": "L0",
        "wip_active": False,
    },
    "omni-laboratory": {
        "cluster": "AROS",
        "commercial_unit": "Cognitive Interfaces",
        "stage": "Experiment",
        "asset_class": "E — Research",
        "asset_type": "Research",
        "priority": "P3",
        "product_potential": "Média (Symbolic Operating System for Assisted Imagination via Gemini Omni)",
        "dependencies": ["proterol", "omni-dual-brain"],
        "evidence": "Repositório Python privado no espaço Compilatorum",
        "next_milestone": "Manter no Laboratório de Exploração como fonte de insights para agentes",
        "monetization": "Pesquisa / Selfware",
        "autonomy_level": "L1",
        "wip_active": False,
    },
}


def classify_repo(raw: Dict[str, Any]) -> Dict[str, Any]:
    name = raw["name"]
    owner = raw["owner"]
    full_name = raw["full_name"]
    desc = raw.get("description") or ""
    lang = raw.get("language") or "Markdown/Spec"

    if name in CURATED_OVERRIDES:
        info = dict(CURATED_OVERRIDES[name])
    else:
        # Heuristic classification for the remaining repositories
        lower = (name + " " + desc).lower()
        if any(k in lower for k in ["dfk", "defi", "trader", "invest", "cadcad", "token", "nft", "web3", "pixelcoin"]):
            cluster = "Capital Intelligence"
            unit = "Capital"
            stage = "Experiment" if "eidos" in lower or "ip-nft" in lower or "nft-gen" in lower else "Archive"
            asset_class = "A — Core IP" if "eidos" in lower or "ip-nft" in lower or "nft-gen" in lower else "F — Archive"
            asset_type = "Core IP" if "A —" in asset_class else "Archive"
            priority = "P2" if "A —" in asset_class else "P3"
            potential = "Média (Tokenização de IP e ativos semânticos executáveis)" if "A —" in asset_class else "Baixa no curto prazo (Experimento Web3/DeFi estacionado)"
            monetization = "Licenciamento / Infraestrutura Web3 (Etapa 3)" if "A —" in asset_class else "Preservação / Arquivo"
        elif any(k in lower for k in ["grant", "dao", "govern", "farcaster", "coopetition"]):
            cluster = "GrantOS"
            unit = "Intelligence"
            stage = "Experiment"
            asset_class = "E — Research"
            asset_type = "Research"
            priority = "P2"
            potential = "Média (Componente de governança e jogos cooperativos)"
            monetization = "Grants e pesquisa"
        elif any(k in lower for k in ["neuro", "cognitive", "planner", "context", "uml", "storybook", "html", "compilat", "monorepo", "proterol", "knowledge", "slm", "molora"]):
            cluster = "NeuroCoder"
            unit = "Agent Engineering"
            is_active_tool = name in {"proterol", "knowledge-weaver", "storybook-genui", "sovereign-html-mockups", "compilatum", "NaturalLanguageCognitiveArchitecture"}
            stage = "Construct" if is_active_tool else "Archive"
            asset_class = "B — Open Core" if is_active_tool else "F — Archive"
            asset_type = "OSS / Internal" if is_active_tool else "Archive"
            priority = "P2" if is_active_tool else "P3"
            potential = "Média/Alta (Componente reutilizável de UI, ontologia ou engenharia cognitiva)" if is_active_tool else "Baixa (Protótipo anterior consolidado no Eugência OS)"
            monetization = "Reutilização interna (Selfware) e Open Core" if is_active_tool else "Preservação"
        else:
            cluster = "AROS" if owner == "smp-sandramariapereira" else "NeuroCoder"
            unit = "Research Lab"
            stage = "Archive"
            asset_class = "F — Archive"
            asset_type = "Archive"
            priority = "P3"
            potential = "Baixa no curto prazo (Material experimental sem prioridade comercial imediata)"
            monetization = "Preservação (Estacionado)"

        info = {
            "cluster": cluster,
            "commercial_unit": unit,
            "stage": stage,
            "asset_class": asset_class,
            "asset_type": asset_type,
            "priority": priority,
            "product_potential": potential,
            "dependencies": ["compilatum"],
            "evidence": f"Repositório GitHub ({lang}) atualizado em {raw['updated_at'][:10]}",
            "next_milestone": "Manter estacionado (Fase 0: Poda do Portfólio) até demanda específica" if stage == "Archive" else "Extrair componentes reutilizáveis para Selfware",
            "monetization": monetization,
            "autonomy_level": "L1" if stage != "Archive" else "L0",
            "wip_active": False,
        }

    ip_governance = (
        "Espaço compartilhado (smp-sandramariapereira): requer verificação formal de titularidade, coautoria e contrato antes de licenciamento exclusivo."
        if owner == "smp-sandramariapereira"
        else "Espaço próprio (compilatorum): titularidade direta da holding intelectual Compilatorum."
    )

    return {
        "id": f"repo:{full_name}",
        "name": name,
        "full_name": full_name,
        "owner": owner,
        "private": raw["private"],
        "language": lang,
        "description": desc or f"Ativo do ecossistema {owner}/{name}",
        "html_url": raw["html_url"],
        "updated_at": raw["updated_at"],
        "cluster": info["cluster"],
        "commercial_unit": info["commercial_unit"],
        "stage": info["stage"],
        "asset_class": info["asset_class"],
        "asset_type": info["asset_type"],
        "priority": info["priority"],
        "product_potential": info["product_potential"],
        "dependencies": info["dependencies"],
        "evidence": info["evidence"],
        "next_milestone": info["next_milestone"],
        "monetization": info["monetization"],
        "autonomy_level": info["autonomy_level"],
        "wip_active": info["wip_active"],
        "ip_governance": ip_governance,
    }


def generate_markdown(assets: List[Dict[str, Any]]) -> str:
    total = len(assets)
    comp_count = sum(1 for a in assets if a["owner"] == "compilatorum")
    sandra_count = sum(1 for a in assets if a["owner"] == "smp-sandramariapereira")
    wip_assets = [a for a in assets if a["wip_active"]]

    by_class: Dict[str, int] = {}
    by_cluster: Dict[str, int] = {}
    by_stage: Dict[str, int] = {}
    for a in assets:
        by_class[a["asset_class"]] = by_class.get(a["asset_class"], 0) + 1
        by_cluster[a["cluster"]] = by_cluster.get(a["cluster"], 0) + 1
        by_stage[a["stage"]] = by_stage.get(a["stage"], 0) + 1

    lines = [
        "# 🗂️ PORTFOLIO-ASSETS-REGISTER — Registro Geral de Ativos Digitais (Fase 0)",
        "",
        "> **Objetivo (Dias 1–7):** Transformar os repositórios do ecossistema Compilatorum + ValueCurator em um portfólio administrável, separando patrimônio intelectual (Core IP), infraestrutura interna (Selfware), bens públicos financiáveis (Open Core / Grants), produtos comerciais ativos ($WIP_{\\text{comercial}} \\le 2$) e arquivo estacionado.",
        "",
        "## 1. Sumário Executivo do Inventário",
        "",
        f"- **Total de Repositórios Auditados:** `{total}` repositórios (`{comp_count}` no espaço `compilatorum` e `{sandra_count}` no espaço compartilhado `smp-sandramariapereira`).",
        f"- **Produtos em WIP Comercial Ativo ($WIP_{{\\text{{comercial}}}} \\le 2$):** `{len(wip_assets)}` (`card-chat` como Motor 1 de Receita Curto Prazo; `value-curator` / **ProofGate** como Motor 2 de Ativo Estratégico Web3).",
        "- **Motor 3 de Produtividade Interna (P0):** `harness-engineering` + `emacs` + `omni-dual-brain`.",
        "- **Motor de Inteligência de Capital (P1):** `concurseiro-grants` + `governaut-os` + `maha-grid`.",
        "",
        "### 1.1. Distribuição por Classe Econômica (A–F)",
        "",
        "| Classe | Significado | Destino Estratégico | Qtd. Repos |",
        "| :--- | :--- | :--- | :---: |",
        f"| **A — Core IP** | Propriedade intelectual estratégica | Retenção e proteção contratual | {by_class.get('A — Core IP', 0)} |",
        f"| **B — Open Core** | Componentes abertos reutilizáveis | Adoção, reputação e Grants de Tooling | {by_class.get('B — Open Core', 0)} |",
        f"| **C — Commercial** | Software e serviços comercializáveis | Productized Services, Setup + Assinatura, Licenciamento | {by_class.get('C — Commercial', 0)} |",
        f"| **D — Internal Tool** | Ferramentas internas (Selfware) | Aumento da Alavancagem da Eugência ($L$) | {by_class.get('D — Internal Tool', 0)} |",
        f"| **E — Research** | Pesquisa experimental aplicada | Grants de pesquisa, papers e exploração | {by_class.get('E — Research', 0)} |",
        f"| **F — Archive** | Material experimental estacionado | Preservação sem custo operacional ativo | {by_class.get('F — Archive', 0)} |",
        "",
        "### 1.2. Distribuição por Cluster Econômico",
        "",
        "| Cluster | Repositórios | Papel na Arquitetura Arborescente ValueCurator |",
        "| :--- | :---: | :--- |",
    ]
    for cl, cnt in sorted(by_cluster.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| **{cl}** | {cnt} | Unidade econômica especializada sob o guarda-chuva ValueCurator |")

    lines.extend([
        "",
        "---",
        "",
        "## 2. Ativos Prioritários (P0 e P1 — Foco de Execução 90 Dias)",
        "",
        "| Repository | Owner | Cluster | Stage | Asset Type | Priority | WIP Comercial | Next Milestone | Monetization |",
        "| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- | :--- |",
    ])

    p0_p1 = [a for a in assets if a["priority"] in ("P0", "P1")]
    p0_p1.sort(key=lambda x: (x["priority"], not x["wip_active"], x["name"]))
    for a in p0_p1:
        wip_badge = "🟢 **ATIVO**" if a["wip_active"] else "⚪ Suporte/Infra"
        lines.append(
            f"| [`{a['name']}`]({a['html_url']}) | `{a['owner']}` | {a['cluster']} | `{a['stage']}` | `{a['asset_class']}` | **{a['priority']}** | {wip_badge} | {a['next_milestone']} | {a['monetization']} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 3. Registro Completo dos 72 Repositórios (Campos Padronizados Fase 0)",
        "",
        "Cada repositório é catalogado com os 9 campos exigidos na Seção 9 (Fase 0) do plano estratégico, acrescido da governança de titularidade jurídica (Seção 11):",
        "",
    ])

    # Group by cluster for clean navigation
    clusters_order = ["ValueCurator", "NeuroCoder", "GrantOS", "Capital Intelligence", "GeoIA", "AROS"]
    for cl in clusters_order:
        cl_assets = [a for a in assets if a["cluster"] == cl]
        cl_assets.sort(key=lambda x: (x["priority"], x["stage"], x["name"]))
        lines.append(f"### 3.{clusters_order.index(cl)+1}. Cluster: {cl} ({len(cl_assets)} repositórios)")
        lines.append("")
        lines.append("| Repository | Stage | Asset Type | Product Potential | Dependencies | Evidence | Next Milestone | Monetization |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for a in cl_assets:
            deps = ", ".join(a["dependencies"]) if a["dependencies"] else "—"
            lines.append(
                f"| **`{a['full_name']}`** ({a['priority']}) | `{a['stage']}` | `{a['asset_class']}` | {a['product_potential']} | {deps} | {a['evidence']} | {a['next_milestone']} | {a['monetization']} |"
            )
        lines.append("")

    lines.extend([
        "---",
        "",
        "## 4. Identificação de Duplicidades, Convergências e Governança Jurídica",
        "",
        "1. **`compilatorum/value-curator` vs `smp-sandramariapereira/valuecurator` vs `compilatorum/vc`:**",
        "   - **Decisão:** `compilatorum/vc` detém a ontologia e especificação do núcleo estratégico; `compilatorum/value-curator` concentra o motor Rust/Anchor e o SDK do **ProofGate**; `smp-sandramariapereira/valuecurator` integra o monorepo compartilhado com `KAIROS-Engine`. Antes do licenciamento comercial B2B do ProofGate (Fase 4), formalizar termo de titularidade e escopo de uso.",
        "2. **`smp-sandramariapereira/card-chat` (Node.js/TypeScript vs Refatoração Python/LangGraph):**",
        "   - **Decisão (Seção 3.1.A e 4.3):** Não manter duas implementações concorrentes. Manter a implementação Node.js/TypeScript/Express do `card-chat` para operação imediata no WhatsApp (Vespa TCG) e conectá-la via contrato HTTP/Webhook ao **AI Gateway** e **ProofGate** do ValueCurator OS (Python/FastAPI).",
        "3. **Planejadores e Mockups (`planner`, `context-planner-pwa`, `compilatum`, `monorepo`, `sovereign-html-mockups`, `lovable-command-center`):**",
        "   - **Decisão:** Consolidados conceitualmente neste **Eugência OS** (Cockpit Híbrido Web App + Cytoscape.js + Emacs Org-mode). Os repositórios anteriores permanecem em `Archive` / `Open Core` como patrimônio de design e componentes.",
        "4. **Voz e Biofeedback (`smp-sandramariapereira/aros-voice-kernel` e `compilatorum/prompt-audiofeedback`):**",
        "   - **Decisão:** Estacionados em `P3` (Cluster AROS) para evitar dispersão ($WIP_{\\text{comercial}} \\le 2$), preservando a documentação para editais de pesquisa aplicada.",
        "",
        "**Critério de Conclusão da Fase 0:** ✅ **CONCLUÍDO** — Todos os 72 repositórios estão inventariados, classificados de A a F, com dependências mapeadas e separação estrita entre os 2 motores comerciais ativos (`card-chat` e `value-curator`/ProofGate), a fábrica interna (`harness-engineering`/`emacs`) e os ativos estacionados.",
    ])

    return "\n".join(lines) + "\n"


def main() -> None:
    raw_repos = []
    with open(RAW_REPOS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                raw_repos.append(json.loads(line))

    assets = [classify_repo(r) for r in raw_repos]
    ASSETS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ASSETS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(assets, f, ensure_ascii=False, indent=2)

    REGISTER_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    md_content = generate_markdown(assets)
    with open(REGISTER_MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Generated {len(assets)} classified assets in {ASSETS_JSON_PATH}")
    print(f"Generated {REGISTER_MD_PATH} ({len(md_content)} bytes)")


if __name__ == "__main__":
    main()
