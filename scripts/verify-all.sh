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
#   cd <the repository folder>
#   sh scripts/verify-all.sh
set -e
cd "$(dirname "$0")/.."
PY=./.venv/bin/python
export PLAYWRIGHT_BROWSERS_PATH=./00_sandbox/browsers
fail=0

# Does a rebuild change anything that is committed, or add anything that is not?
# The second half is the part `git diff` cannot answer: it compares tracked content,
# so a generator that begins writing a new output file produces no diff and the gate
# passes over output nobody committed. Prints ok or FAILED and sets `fail`.
drift() {
  what="$1"; shift
  if ! git diff --quiet -- "$@"; then
    echo "FAILED — $what differ from a fresh build"
    git diff --stat -- "$@" | sed 's/^/    /'
    fail=1
    return
  fi
  new_files=$(git status --porcelain --untracked-files=all -- "$@" | grep '^??' || true)
  if [ -n "$new_files" ]; then
    echo "FAILED — the build wrote files that are not committed"
    printf '%s\n' "$new_files" | sed 's/^/    /'
    fail=1
    return
  fi
  echo "ok"
}

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
# The count printed at the end is counted, not typed. It said 17 while the list
# held 18, in a project whose whole claim is that its numbers are measured.
n_prose=0
for path in README.md README.bn.md NOTICE TRADEMARKS.md LICENSE-DOCS.md \
            00_sandbox/TOOLCHAIN.md 01_research 02_strategy 09_guidebook/chapters \
            13_plugins/claude-code/README.md 13_plugins/claude-code/skills \
            13_plugins/figma/README.md 13_plugins/claude-design/PUSH-RECORD.md \
            06_type/BANGLA-STANDARD.md \
            06_type/BANGLA-STRINGS.md 06_type/SHORTLIST.md 06_type/RECOMMENDATION.md \
            06_type/MEASUREMENTS.md 06_type/pairings.md; do
  n_prose=$((n_prose + 1))
  $PY 13_plugins/claude-code/skills/aninda-review/scripts/check.py "$path" >/dev/null 2>&1 \
    || { echo "  english standard FAILED: $path"; fail=1; }
done
echo "  english standard: $n_prose paths"
run "no absolute paths in tracked files" $PY scripts/check_no_absolute_paths.py
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
# Two bugs lived here. The refusal was reported and then the diff ran anyway,
# found nothing (a refused build writes nothing) and printed `ok` on the line
# below the failure — so one gate said both things. And `git diff` sees TRACKED
# content only, so a build that started emitting a NEW file left this green.
# `drift()` below fixes the second for every gate that uses it.
if ! $PY 04_mark/build.py >/dev/null 2>&1; then
  echo "FAILED — the mark build refused"; fail=1
else
  drift "the committed marks" 04_mark/svg 04_mark/manifest.json 04_mark/proof.svg
fi
run "scripts/readme.py"       $PY scripts/readme.py --check
run "10_assets/build.py"      $PY 10_assets/build.py --check
run "guidebook PDF vs the book" $PY 09_guidebook/scripts/pdf.py --check
run "claude-design bundle"    $PY 13_plugins/claude-design/build.py --check
run "benchmark verdicts"      $PY scripts/benchmark.py --check
run "findings register"       $PY scripts/findings.py --check

echo "--- plugins ---"
run "claude-code plugin"      $PY 13_plugins/claude-code/scripts/check_plugin.py
printf '%-46s ' "figma plugin build is current"
# The refusal has to be reported, not swallowed. `|| true` here meant a build that
# died left dist/ exactly as committed, the diff below found nothing, and the gate
# printed ok — while the same failure fails the job in CI, which runs this build as
# a step of its own. A local gate weaker than the CI gate it mirrors is worse than
# no local gate: it teaches you to trust a pass that CI will not give you.
if ! ( cd 13_plugins/figma && node build.mjs --code-only ) >/dev/null 2>&1; then
  echo "FAILED — the figma build refused to run"; fail=1
else
  drift "the committed figma build" 13_plugins/figma/dist \
        13_plugins/figma/src/tokens.generated.ts 13_plugins/figma/RECEIPT-EXPECTED.json
fi
printf '%-46s ' "figma plugin typechecks"
if ( cd 13_plugins/figma && ../../00_sandbox/node_modules/.bin/tsc --noEmit -p tsconfig.json ) \
     >/dev/null 2>&1; then echo "ok"; else echo "FAILED"; fail=1; fi
printf '%-46s ' "the full figma build completes"
if out=$( cd 13_plugins/figma && node build.mjs 2>&1 ) \
     && printf '%s' "$out" | grep -q "manifest.json is adopted"; then
  echo "ok"
else
  echo "FAILED"; printf '%s\n' "$out" | tail -6 | sed 's/^/    /'; fail=1
fi
printf '%-46s ' "a placeholder manifest stops the figma build"
( cd 13_plugins/figma && cp manifest.json /tmp/manifest.committed.json \
  && printf '{"id":"x","api":"REPLACE_ME__FIGMA_GENERATES_THIS"}\n' > manifest.json )
if ( cd 13_plugins/figma && node build.mjs >/dev/null 2>&1 ); then
  echo "FAILED — the manifest gate let a placeholder through"; fail=1
else
  echo "ok"
fi
cp /tmp/manifest.committed.json 13_plugins/figma/manifest.json
# CI diffs the manifest after this test; so does this, for the same reason. The
# test overwrites a committed file on purpose, and a restore nobody checks is how
# a working tree quietly ends up holding a placeholder.
printf '%-46s ' "the placeholder test put the manifest back"
if git diff --quiet 13_plugins/figma/manifest.json; then echo "ok"; else
  echo "FAILED — manifest.json was not restored"; fail=1; fi
printf '%-46s ' "claude-code skill bundles are current"
if ! $PY 13_plugins/claude-code/scripts/build_skills.py >/dev/null 2>&1; then
  echo "FAILED — the skill bundle build refused to run"; fail=1
else
  drift "the committed .skill bundles" 13_plugins/claude-code/dist
fi
printf '%-46s ' "skill bundles are reproducible"
if $PY 13_plugins/claude-code/scripts/build_skills.py --prove >/dev/null 2>&1; then
  echo "ok"
else
  echo "FAILED"; fail=1
fi
# CI runs TWO node blocks here and this script ran only the second, so a package.json
# exports map naming a file that does not exist failed the job and passed locally.
# That asymmetry was invisible while check_gates.py could not see this step at all.
printf '%-46s ' "every npm export target exists"
if ( cd 12_packages/npm && node -e "
  const p = require('./package.json'), fs = require('fs');
  for (const [k, v] of Object.entries(p.exports)) {
    const f = typeof v === 'string' ? v : (v.import || v.types);
    if (!fs.existsSync(f)) { console.error('missing export target', k, f); process.exit(1); }
  }" ) >/dev/null 2>&1; then echo "ok"; else echo "FAILED"; fail=1; fi
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
