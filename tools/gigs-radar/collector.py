#!/usr/bin/env python3
"""Eugencia Web3 + AI opportunity collector (Python standard library only)."""
import argparse, datetime as dt, html, json, os, re, sqlite3, urllib.parse, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent
NOW=lambda: dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
S={
'remoteok':('Remote OK','https://remoteok.com/api',0,'Attribute Remote OK and link the original listing.'),
'himalayas':('Himalayas','https://himalayas.app/jobs/api',0,'Use nextCursor pagination; verify location/timezone restrictions.'),
'remotive':('Remotive','https://remotive.com/api/remote-jobs',0,'Attribute and link Remotive; recommended max four fetches/day.'),
'web3career':('Web3.career','https://web3.career/api/v1',1,'WEB3CAREER_API_TOKEN required; keep private; preserve apply_url; follow-link attribution.'),
'superteam_earn':('Superteam Earn','https://superteam.fun/api/agents/listings/live',1,'SUPERTEAM_EARN_API_KEY required; no agent registration or submission is performed.')}
TECH=('python','typescript','javascript','postgres','api','mcp','agent','llm','rag','evaluation','testing','qa','harness','solana','web3','blockchain','data','etl','automation','workflow','rust','dao','governance')
GIG=('bounty','freelance','contract','project','gig','task','challenge','hackathon')
def get(url,headers=None):
 r=urllib.request.Request(url,headers={'User-Agent':'Eugencia-Gigs-Radar/0.1','Accept':'application/json',**(headers or {})})
 with urllib.request.urlopen(r,timeout=25) as x:return json.loads(x.read().decode('utf-8','replace'))
def clean(v):return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',str(v or '')))).strip()
def init(c):
 c.executescript((ROOT/'schema.sql').read_text())
 for k,(name,url,auth,terms) in S.items():
  c.execute('''INSERT INTO sources(source_id,name,source_type,endpoint,auth_required,terms_notes,last_checked_at) VALUES(?,?,?,?,?,?,?) ON CONFLICT(source_id) DO UPDATE SET last_checked_at=excluded.last_checked_at''',(k,name,'authenticated_api' if auth else 'public_json_api',url,auth,terms,NOW()))
 weights={'technical_fit':.25,'contract_fit':.20,'geography_fit':.15,'payment_fit':.15,'selfware_leverage':.15,'ergonomics_fit':.10}
 evidence='Engenharia de Computação; atuação profissional em TI; projetos próprios com agentes IA, APIs, PostgreSQL, RAG, Web3, testes/harness e governança. Evidência de produção por stack deve ser verificada.'
 for k,w in weights.items():c.execute('INSERT OR IGNORE INTO profile_dimensions VALUES(?,?,?,?)',(k,w,evidence,'medium'))
 c.commit()
def fetch(src):
 if src=='remoteok':
  d=get(S[src][1]);return [x for x in d if isinstance(x,dict) and x.get('position')]
 if src=='himalayas':
  out=[];cursor=None
  for _ in range(5):
   u=S[src][1]+'?limit=100'+('&cursor='+urllib.parse.quote(cursor) if cursor else '')
   d=get(u);out+=d.get('jobs',[]);cursor=d.get('nextCursor')
   if not cursor:break
  return out
 if src=='remotive':return get(S[src][1]+'?category=software-dev&limit=100').get('jobs',[])
 if src=='web3career':
  t=os.getenv('WEB3CAREER_API_TOKEN')
  if not t:return []
  d=get(S[src][1]+'?'+urllib.parse.urlencode({'token':t,'remote':'true','limit':100}));return d if isinstance(d,list) else d.get('jobs',[])
 if src=='superteam_earn':
  t=os.getenv('SUPERTEAM_EARN_API_KEY')
  if not t:return []
  d=get(S[src][1]+'?take=100',{'Authorization':'Bearer '+t});return d if isinstance(d,list) else d.get('listings',[])
 return []
def norm(src,x):
 if src=='remoteok':
  url=x.get('url') or x.get('apply_url');tags=x.get('tags') or []
  return (x.get('id') or url,x.get('position'),x.get('company'),'full_time_or_contract',' / '.join(tags),clean(x.get('description')),x.get('location') or 'Remote (scope unspecified)',None,x.get('salary_min') or None,x.get('salary_max') or None,'USD' if x.get('salary_min') or x.get('salary_max') else None,x.get('date'),url,x.get('apply_url') or url,tags)
 if src=='himalayas':
  url=x.get('guid') or x.get('applicationLink');loc=x.get('locationRestrictions') or []
  pub=dt.datetime.fromtimestamp(x['pubDate'],dt.timezone.utc).isoformat().replace('+00:00','Z') if x.get('pubDate') else None
  return (url,x.get('title'),x.get('companyName'),(x.get('employmentType') or 'role').lower().replace(' ','_'),' / '.join(x.get('categories') or []),clean(x.get('description') or x.get('excerpt')),', '.join(loc) if loc else 'Remote (restrictions unspecified)',', '.join(loc) or None,x.get('minSalary'),x.get('maxSalary'),x.get('currency'),pub,url,x.get('applicationLink') or url,x.get('categories') or [])
 if src=='remotive':
  url=x.get('url');return (x.get('id') or url,x.get('title'),x.get('company_name'),x.get('job_type') or 'role',x.get('category'),clean(x.get('description')),x.get('candidate_required_location') or 'Remote (restrictions unspecified)',x.get('candidate_required_location'),None,None,None,x.get('publication_date'),url,url,[x.get('category')])
 if src=='web3career':
  url=x.get('apply_url') or x.get('url');tags=x.get('tags') or []
  return (x.get('id') or url,x.get('title') or x.get('position'),x.get('company'),'web3_role',' / '.join(tags) if isinstance(tags,list) else str(tags),clean(x.get('description')),x.get('location') or ('Remote' if x.get('remote') else 'Unspecified'),x.get('country'),None,None,None,x.get('date'),url,x.get('apply_url'),tags)
 if src=='superteam_earn':
  slug=x.get('slug') or x.get('url');url=slug if str(slug).startswith('http') else 'https://superteam.fun/earn/opportunities/'+str(slug or '')
  reward=x.get('reward') or {};tags=x.get('skills') or []
  return (x.get('id') or slug,x.get('title'),x.get('sponsor') or x.get('company'),x.get('type') or 'bounty',' / '.join(tags) if isinstance(tags,list) else str(tags),clean(x.get('description')),x.get('region') or 'Global (verify listing)',x.get('region'),reward.get('min'),reward.get('max'),reward.get('currency') or 'USDC',x.get('createdAt'),url,url,tags)
def score(r):
 blob=' '.join(str(v or '') for v in (r[1],r[4],r[5],r[13])).lower();typ=str(r[3]).lower();loc=str(r[6]).lower()
 t=min(95,35+4*sum(k in blob for k in TECH));c=95 if any(k in typ for k in GIG) else (35 if 'contract' in typ else 20)
 g=100 if ('global' in loc or 'worldwide' in loc) else (65 if 'remote' in loc else 20)
 p=80 if r[8] or r[9] else 45;reuse=min(95,40+7*sum(k in blob for k in ('mcp','agent','api','postgres','solana','evaluation','harness','automation')));e=70 if c>=90 else 45
 vals=(t,c,g,p,reuse,e);total=round(sum(a*b for a,b in zip(vals,(.25,.2,.15,.15,.15,.1))),1)
 return (*vals,55 if r[5] else 30,total,'shortlist' if total>=75 else ('qualify' if total>=60 else 'watchlist'))
def collect(c,sources):
 init(c)
 for src in sources:
  start=NOW();seen=inserted=0;err=None
  try:
   rows=fetch(src);seen=len(rows)
   for x in rows:
    r=norm(src,x)
    if not r or not r[1] or not r[12]:continue
    ext=str(r[0]);oid=(src+'-'+ext)[:240];ts=NOW()
    cols='external_id,title,organization,opportunity_type,category,description,location,eligible_regions,compensation_min,compensation_max,compensation_currency,published_at,source_url,apply_url,raw_tags'
    vals=[ext,*r[1:14],json.dumps(r[14])]
    c.execute(f'''INSERT INTO opportunities(opportunity_id,source_id,{cols},remote_scope,compensation_type,status,first_seen_at,last_seen_at)
    VALUES({','.join('?' for _ in range(22))}) ON CONFLICT(source_id,external_id) DO UPDATE SET title=excluded.title,description=excluded.description,location=excluded.location,status=excluded.status,last_seen_at=excluded.last_seen_at''',[oid,src,*vals,'remote_unspecified','not_disclosed','open_at_collection',ts,ts])
    sc=score(r);c.execute('''INSERT INTO opportunity_scores VALUES(?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(opportunity_id) DO UPDATE SET technical_fit=excluded.technical_fit,contract_fit=excluded.contract_fit,geography_fit=excluded.geography_fit,payment_fit=excluded.payment_fit,selfware_leverage=excluded.selfware_leverage,ergonomics_fit=excluded.ergonomics_fit,confidence=excluded.confidence,score_total=excluded.score_total,disposition=excluded.disposition,rationale=excluded.rationale,scoring_version=excluded.scoring_version''',(oid,*sc,'Heurística lexical; confirmar requisitos e escopo manualmente.','heuristic-v0.1'))
    c.execute('INSERT INTO funnel_events(opportunity_id,stage,event_at,notes) VALUES(?,?,?,?)',(oid,'DISCOVER',ts,'Coleta automática; ainda não qualificada.'));inserted+=1
  except Exception as e:err=str(e)
  c.execute('UPDATE sources SET last_checked_at=? WHERE source_id=?',(NOW(),src));c.execute('INSERT INTO collection_runs(started_at,finished_at,source_id,records_seen,records_inserted,errors) VALUES(?,?,?,?,?,?)',(start,NOW(),src,seen,inserted,err));c.commit();print(src,seen,inserted,err or '')
def main():
 p=argparse.ArgumentParser();p.add_argument('--db',default=str(ROOT/'eugencia_crypto_ai_gigs.sqlite'));p.add_argument('--sources',default=','.join(S));p.add_argument('--init-only',action='store_true');a=p.parse_args();c=sqlite3.connect(a.db);c.execute('PRAGMA foreign_keys=ON');init(c)
 if not a.init_only:collect(c,[x.strip() for x in a.sources.split(',') if x.strip()])
 print('DB',a.db,'opportunities',c.execute('select count(*) from opportunities').fetchone()[0]);c.close()
if __name__=='__main__':main()
