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
run "scripts/readme.py"       $PY scripts/readme.py --check

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
run "11_site/check.py"        $PY 11_site/check.py
run "08_components/check.py"  $PY 08_components/check.py

echo
[ "$fail" -eq 0 ] && echo "ALL GATES PASSED" || { echo "SOMETHING FAILED — see above"; exit 1; }
