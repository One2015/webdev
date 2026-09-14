#!/usr/bin/env python3
"""Read-only package validation. Does not validate webpages or run node gates."""
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parent.parent
errors=[]; checks=0
def check(ok,msg):
 global checks
 checks+=1
 if not ok: errors.append(msg)
for f in ROOT.rglob('*.json'):
 try: json.loads(f.read_text())
 except Exception as e: errors.append(f'{f.relative_to(ROOT)}: {e}')
 checks+=1
rules=json.loads((ROOT/'rubrics/rules.json').read_text())
ids=[r['id'] for r in rules['rules']]
check(len(ids)==len(set(ids)),'duplicate rule IDs')
for r in rules['rules']:
 for key in ['node','checker_kind','severity','applies_when','required_inputs','assertion','pass_condition','on_unknown','repair_target','exceptions']:
  check(key in r,f'{r["id"]}: missing {key}')
 check(r['severity'] in ['blocking','major','minor'],f'{r["id"]}: severity')
result=json.loads((ROOT/'examples/review-result.json').read_text())
check(result['rule_id'] in ids,'example references unknown rule')
check(result['status'] in rules['status_enum'],'example status invalid')
task=json.loads((ROOT/'examples/task-batch.json').read_text())
check(task['execution_end']=='query_only' and task['authorization']['build'] is False,'example default must not authorize build')
check(task['candidate_pool_target']>=task['delivery_target']>0,'candidate/delivery counts invalid')
check(task['preview_mode']=='reference_board' and not task['authorization']['preview_render'],'default preview authorization')
plan=json.loads((ROOT/'examples/evaluation-plan.json').read_text())
n=plan['delivery_target']
check(plan['required_pair_count']==n*(n-1)//2,'pair count mismatch')
check(plan['delivery_target']==task['delivery_target'],'task/evaluation target mismatch')
check(plan['minimum_ordinal'] in plan['ordinal_scale'],'ordinal threshold outside scale')
check(plan['fixed_weights'] is None,'uncalibrated weights must not be represented as standard')
stability=json.loads((ROOT/'examples/stability-contract.json').read_text())
check(stability['fonts']['font_ready_alone_is_proof'] is False,'font readiness must not be sole proof')
check(stability['reproduction']['llm_regeneration_byte_identical_guarantee'] is False,'false LLM determinism guarantee')
pair=json.loads((ROOT/'examples/pair-review.json').read_text())
check(pair['status']=='not_run' and not pair['screenshots'],'unexecuted pair example must not claim success')
check(all(i in ids for i in pair['rule_ids']),'unknown pair rubric references')
for f in ROOT.rglob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if target.startswith(('https://','http://','#')): continue
  check((f.parent/target.split('#')[0]).exists(),f'{f.relative_to(ROOT)} missing local link {target}')
for paper in json.loads((ROOT/'research/papers.json').read_text())['papers']:
 check(paper['url'].startswith('https://') and bool(paper['limitations']),'paper missing source or boundary')
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
for item in manifest['files']:
 f=ROOT/item['path']
 check(f.is_file(),f'missing {item["path"]}')
 if f.is_file(): check(hashlib.sha256(f.read_bytes()).hexdigest()==item['sha256'],f'hash mismatch {item["path"]}')
expected={r['path'] for r in manifest['files']}|{'MANIFEST.json','SHA256SUMS'}
actual={str(f.relative_to(ROOT)) for f in ROOT.rglob('*') if f.is_file() and '.git' not in f.parts and '__pycache__' not in f.parts}
check(expected==actual,'manifest file inventory mismatch')
for line in (ROOT/'SHA256SUMS').read_text().splitlines():
 digest,name=line.split('  ',1)
 check(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,f'SHA256SUMS mismatch {name}')
print(json.dumps({'scope':'documentation_package_only','checks':checks,'passed':checks-len(errors),'failed':len(errors),'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
