#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader
#
# WHY THIS FILE EXISTS
# ====================
# Every gate CI runs, in one command, so a local pass means the same thing as a
# green run. Two commits went out red because the loop being typed by hand at the
# time happened to omit the Figma plugin's drift guard — the gate that catches a
# generated bundle left stale by a change to its inputs. A verification set that
# lives in someone's head is not a verification set.
#
# Ordered cheapest-failure-first, the same as .github/workflows/ci.yml.
#
#   cd /Users/gru953/Claude/Cowork/Aninda_Studio
#   sh scripts/verify-all.sh
set -e
cd "$(dirname "$0")/.."
PY=./.venv/bin/python
export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
fail=0

run() {
  name="$1"; shift
  printf '%-46s ' "$name"
  if out=$("$@" 2>&1); then
    echo "ok"
  else
    echo "FAILED"
    echo "$out" | tail -12 | sed 's/^/    /'
    fail=1
  fi
}

# One sequencing trap, learned the hard way. scripts/readme.py discovers the
# repository's generators with `git ls-files`, so a NEW generator is invisible to
# its rebuild-chain guard until it is tracked. Running this script before staging
# therefore cannot see an unregistered new generator, and CI — which checks out a
# commit — can. So stage first: `git add -A`, then run this. The check below makes
# the trap visible rather than leaving it to be discovered by a red run.
printf '%-46s ' "new files are staged, so guards can see them"
if [ -z "$(git ls-files --others --exclude-standard)" ]; then
  echo "ok"
else
  echo "WARNING — untracked files present; git ls-files based guards cannot see them:"
  git ls-files --others --exclude-standard | sed 's/^/    /'
fi

echo "--- lint ---"
# TRACKED files only, for both of these. CI checks out a commit, so it only ever
# sees what git holds; sweeping the working tree instead made the first version of
# these two gates fail on ten gitignored macOS .DS_Store files and on JSON inside
# .claude/, neither of which CI can see. A local gate stricter than the CI gate it
# mirrors is its own kind of wrong: it trains you to ignore the output.
printf '%-46s ' "every tracked JSON parses"
if $PY - <<'PYJSON' >/dev/null 2>&1
import json, subprocess, sys
files = subprocess.run(["git", "ls-files", "-z", "*.json"], capture_output=True,
                       text=True).stdout.split("\0")
bad = []
for f in files:
    if not f or f.startswith("00_sandbox/node_modules/"):
        continue
    try:
        json.load(open(f, encoding="utf-8"))
    except Exception as exc:
        bad.append(f"{f}: {exc}")
if bad:
    print("\n".join(bad)); sys.exit(1)
PYJSON
then echo "ok"; else
  echo "FAILED"; fail=1
fi
printf '%-46s ' "no .DS_Store tracked"
if git ls-files | grep -q '\.DS_Store'; then
  echo "FAILED"; git ls-files | grep '\.DS_Store' | sed 's/^/    /'; fail=1
else echo "ok"; fi
printf '%-46s ' "generated files say they are generated"
if grep -q "GENERATED" 07_tokens/css/tokens.css; then echo "ok"; else echo "FAILED"; fail=1; fi

echo "--- prose and licences ---"
for path in README.md README.bn.md NOTICE TRADEMARKS.md LICENSE-DOCS.md \
            00_sandbox/TOOLCHAIN.md 01_research 02_strategy 09_guidebook/chapters \
            13_plugins/claude-code/README.md 13_plugins/claude-code/skills \
            13_plugins/figma/README.md 06_type/BANGLA-STANDARD.md \
            06_type/BANGLA-STRINGS.md 06_type/SHORTLIST.md 06_type/RECOMMENDATION.md \
            06_type/MEASUREMENTS.md 06_type/pairings.md; do
  $PY 13_plugins/claude-code/skills/aninda-review/scripts/check.py "$path" >/dev/null 2>&1 \
    || { echo "  english standard FAILED: $path"; fail=1; }
done
echo "  english standard: 17 paths"
run "CI and this script agree" $PY scripts/check_gates.py
run "licence claims"          $PY scripts/check_licence_claims.py
run "MEASUREMENTS.md figures" $PY scripts/check_measurements.py

echo "--- generated output must match its source ---"
run "05_colour/engine.py"     $PY 05_colour/engine.py --check
run "07_tokens/build.py"      $PY 07_tokens/build.py --check
run "07_tokens/emit_css.py"   $PY 07_tokens/emit_css.py --check
run "12_packages/build.py"    $PY 12_packages/build.py --check
run "08_components/build.py"  $PY 08_components/build.py --check
run "11_site/build.py"        $PY 11_site/build.py --check
run "09_guidebook/build.py"   $PY 09_guidebook/build.py --check
printf '%-46s ' "marks are current (shaping gates inside)"
$PY 04_mark/build.py >/dev/null 2>&1 || { echo "FAILED — the mark build refused"; fail=1; }
if git diff --quiet 04_mark/svg 04_mark/manifest.json 04_mark/proof.svg; then
  echo "ok"
else
  echo "FAILED — the committed marks differ from a fresh build"
  git diff --stat 04_mark/svg 04_mark/manifest.json 04_mark/proof.svg | sed 's/^/    /'
  fail=1
fi
run "scripts/readme.py"       $PY scripts/readme.py --check
run "claude-design bundle"    $PY 13_plugins/claude-design/build.py --check
run "findings register"       $PY scripts/findings.py --check

echo "--- plugins ---"
run "claude-code plugin"      $PY 13_plugins/claude-code/scripts/check_plugin.py
printf '%-46s ' "figma plugin build is current"
( cd 13_plugins/figma && node build.mjs --code-only >/dev/null 2>&1 || true )
if git diff --quiet 13_plugins/figma/dist 13_plugins/figma/src/tokens.generated.ts \
                    13_plugins/figma/RECEIPT-EXPECTED.json; then
  echo "ok"
else
  echo "FAILED — the committed build differs from a fresh one"
  git diff --stat 13_plugins/figma/dist 13_plugins/figma/src/tokens.generated.ts \
                  13_plugins/figma/RECEIPT-EXPECTED.json | sed 's/^/    /'
  fail=1
fi
printf '%-46s ' "figma plugin typechecks"
if ( cd 13_plugins/figma && ../../00_sandbox/node_modules/.bin/tsc --noEmit -p tsconfig.json ) \
     >/dev/null 2>&1; then echo "ok"; else echo "FAILED"; fail=1; fi
printf '%-46s ' "a placeholder manifest stops the figma build"
if ( cd 13_plugins/figma && node build.mjs >/dev/null 2>&1 ); then
  echo "FAILED — the manifest gate let a placeholder through"; fail=1
else
  echo "ok"
fi
printf '%-46s ' "claude-code skill bundles are current"
$PY 13_plugins/claude-code/scripts/build_skills.py >/dev/null 2>&1 || true
if git diff --quiet 13_plugins/claude-code/dist; then
  echo "ok"
else
  echo "FAILED — the committed .skill bundles differ from a fresh build"
  git diff --stat 13_plugins/claude-code/dist | sed 's/^/    /'
  fail=1
fi
printf '%-46s ' "skill bundles are reproducible"
if $PY 13_plugins/claude-code/scripts/build_skills.py --prove >/dev/null 2>&1; then
  echo "ok"
else
  echo "FAILED"; fail=1
fi
printf '%-46s ' "npm entry points import and agree"
if ( cd 12_packages/npm && node --input-type=module -e "
  import a from 'node:assert';
  import { createRequire } from 'node:module';
  import esm, { tokens, themes } from './dist/index.mjs';
  const cjs = createRequire(import.meta.url)('./dist/index.cjs');
  a.ok(esm && typeof esm === 'object');
  a.strictEqual(tokens, esm);
  a.ok(Array.isArray(themes) && themes.length === 4);
  a.deepStrictEqual(Object.keys(cjs.tokens), Object.keys(esm));" >/dev/null 2>&1 ); then
  echo "ok"
else
  echo "FAILED"; fail=1
fi

echo "--- rendered and measured (slow) ---"
run "00_sandbox/measure.py"   $PY 00_sandbox/measure.py
run "11_site/check.py"        $PY 11_site/check.py
run "08_components/check.py"  $PY 08_components/check.py

echo
[ "$fail" -eq 0 ] && echo "ALL GATES PASSED" || { echo "SOMETHING FAILED — see above"; exit 1; }
