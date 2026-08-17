#!/usr/bin/env node
// Aninda Studio — build the Figma plugin.
//
//   node build.mjs              full build, then the manifest gate
//   node build.mjs --code-only  compile the artefacts and stop before the gate
//
// --code-only exists for one reason: continuous integration has to be able to
// rebuild dist/ and compare it against what is committed, and that check does
// not need a plugin id. It is not a way to ship an unadopted manifest — the
// output of --code-only will not load in Figma either.
//
// Nothing here writes a date or a timestamp into a generated file. Every
// artefact is a pure function of its inputs, so a rebuild that changes nothing
// produces a byte-identical file and the CI diff means something.
//
// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader

import { createHash } from 'node:crypto';
import { mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { inspectManifest, failLoudly } from './scripts/manifest-gate.mjs';

const PLUGIN_DIR = dirname(fileURLToPath(import.meta.url));
const PROJECT = resolve(PLUGIN_DIR, '..', '..');
const SANDBOX = join(PROJECT, '00_sandbox');
const SRC = join(PLUGIN_DIR, 'src');
const DIST = join(PLUGIN_DIR, 'dist');

const require = createRequire(join(SANDBOX, 'package.json'));
const esbuild = require('esbuild');

const codeOnly = process.argv.indexOf('--code-only') !== -1;

const sha256 = (buffer) => createHash('sha256').update(buffer).digest('hex');
const say = (line) => process.stdout.write(line + '\n');

// ---------------------------------------------------------------------------
// 1. Read every input and hash it
// ---------------------------------------------------------------------------

const TOKEN_FILES = [
  ['primitive', '07_tokens/build/primitive.tokens.json'],
  ['semantic.light', '07_tokens/build/semantic.light.tokens.json'],
  ['semantic.dark', '07_tokens/build/semantic.dark.tokens.json'],
  ['semantic.hc-light', '07_tokens/build/semantic.hc-light.tokens.json'],
  ['semantic.hc-dark', '07_tokens/build/semantic.hc-dark.tokens.json'],
  ['forced-colors.map', '07_tokens/build/forced-colors.map.json'],
];

const MARK_DIR = join(PROJECT, '04_mark', 'svg');

const sources = {};
const readInput = (relative) => {
  const bytes = readFileSync(join(PROJECT, relative));
  sources[relative] = sha256(bytes);
  return bytes.toString('utf8');
};

const tokenText = {};
for (const [key, relative] of TOKEN_FILES) tokenText[key] = readInput(relative);

const markFiles = readdirSync(MARK_DIR)
  .filter((f) => f.endsWith('.svg'))
  .sort();
const marks = markFiles.map((file) => ({
  name: file.replace(/\.svg$/, ''),
  file,
  svg: readInput(`04_mark/svg/${file}`),
}));

const markManifestText = readInput('04_mark/manifest.json');
const cardsText = readInput('08_components/_cards.json');

// One hash over every input, so a single number answers "are these the tokens
// I think they are". The order is the sorted file list, so it is reproducible.
const combined = Object.keys(sources)
  .sort()
  .map((k) => `${k}  ${sources[k]}`)
  .join('\n');
const bundleSha = sha256(Buffer.from(combined + '\n', 'utf8'));

say(`Read ${Object.keys(sources).length} input files. Bundle SHA-256 ${bundleSha}`);

// ---------------------------------------------------------------------------
// 2. Emit src/tokens.generated.ts
// ---------------------------------------------------------------------------

const generated = [
  '// GENERATED FILE. Do not hand-edit — run "node build.mjs" instead.',
  '//',
  '// Every token, mark and card in the Aninda Studio system, compiled in at build',
  '// time so the plugin works with no network connection at all. The manifest',
  '// declares networkAccess "none", and this is how that promise is kept.',
  '//',
  '// SPDX-License-Identifier: Apache-2.0',
  '// Copyright 2026 Aninda Sundar Howlader',
  '',
  "import type { RawInput } from './plan';",
  '',
  `export const BUNDLE_SHA256 = ${JSON.stringify(bundleSha)};`,
  '',
  `export const SOURCE_HASHES: { [file: string]: string } = ${JSON.stringify(sources, null, 2)};`,
  '',
  'export const BUNDLED: RawInput = {',
  `  primitive: ${tokenText['primitive'].trim()},`,
  '  semantic: {',
  `    light: ${tokenText['semantic.light'].trim()},`,
  `    dark: ${tokenText['semantic.dark'].trim()},`,
  `    'hc-light': ${tokenText['semantic.hc-light'].trim()},`,
  `    'hc-dark': ${tokenText['semantic.hc-dark'].trim()},`,
  '  },',
  `  forcedColors: ${tokenText['forced-colors.map'].trim()},`,
  `  marks: ${JSON.stringify(marks, null, 2)},`,
  `  markManifest: ${markManifestText.trim()},`,
  `  cards: ${cardsText.trim()},`,
  '};',
  '',
].join('\n');

writeFileSync(join(SRC, 'tokens.generated.ts'), generated, 'utf8');
say('Wrote src/tokens.generated.ts');

// ---------------------------------------------------------------------------
// 3. Run the same plan code Node-side, to write RECEIPT-EXPECTED.json
// ---------------------------------------------------------------------------

const temp = mkdtempSync(join(tmpdir(), 'aninda-plan-'));
let plan;
try {
  const planBundle = join(temp, 'plan.mjs');
  await esbuild.build({
    entryPoints: [join(SRC, 'plan.ts')],
    outfile: planBundle,
    bundle: true,
    format: 'esm',
    platform: 'node',
    target: 'node18',
    logLevel: 'warning',
  });
  const planModule = await import(pathToFileURL(planBundle).href);
  plan = planModule.buildPlan({
    primitive: JSON.parse(tokenText['primitive']),
    semantic: {
      light: JSON.parse(tokenText['semantic.light']),
      dark: JSON.parse(tokenText['semantic.dark']),
      'hc-light': JSON.parse(tokenText['semantic.hc-light']),
      'hc-dark': JSON.parse(tokenText['semantic.hc-dark']),
    },
    forcedColors: JSON.parse(tokenText['forced-colors.map']),
    marks,
    markManifest: JSON.parse(markManifestText),
    cards: JSON.parse(cardsText),
  });
} finally {
  rmSync(temp, { recursive: true, force: true });
}

const receiptExpected = {
  $comment:
    'What a clean run of the plugin should report. It is written by build.mjs from the same plan code the ' +
    'plugin runs, so comparing it against the receipt the plugin prints is a comparison of two numbers, not a ' +
    'reading of two documents. There is no date in this file on purpose: it is a pure function of the tokens, ' +
    'and the SHA-256 below changes only when they do.',
  generatedBy: '13_plugins/figma/build.mjs',
  tokensSha256: bundleSha,
  sources,
  fontsRequired: plan.fontsRequired,
  pages: plan.pages,
  expected: plan.totals,
  themeModes: plan.collections[1].modes,
  decisions: plan.decisions,
  knownGaps: plan.knownGaps,
};

writeFileSync(
  join(PLUGIN_DIR, 'RECEIPT-EXPECTED.json'),
  JSON.stringify(receiptExpected, null, 2) + '\n',
  'utf8'
);
say('Wrote RECEIPT-EXPECTED.json');
for (const key of Object.keys(plan.totals)) say(`  expected ${key}: ${plan.totals[key]}`);

// ---------------------------------------------------------------------------
// 4. Bundle the plugin
// ---------------------------------------------------------------------------

mkdirSync(DIST, { recursive: true });

await esbuild.build({
  entryPoints: [join(SRC, 'code.ts')],
  outfile: join(DIST, 'code.js'),
  bundle: true,
  format: 'iife',
  target: 'es2017',
  legalComments: 'none',
  logLevel: 'warning',
  banner: {
    js:
      '// Aninda Studio — Figma plugin. GENERATED by 13_plugins/figma/build.mjs.\n' +
      '// SPDX-License-Identifier: Apache-2.0\n' +
      '// Copyright 2026 Aninda Sundar Howlader\n' +
      `// tokens SHA-256 ${bundleSha}`,
  },
});
say('Wrote dist/code.js');

const ui = readFileSync(join(SRC, 'ui.html'), 'utf8').replace('__TOKENS_SHA256__', bundleSha);
writeFileSync(join(DIST, 'ui.html'), ui, 'utf8');
say('Wrote dist/ui.html');

// ---------------------------------------------------------------------------
// 5. The manifest gate
// ---------------------------------------------------------------------------

if (codeOnly) {
  say('');
  say('--code-only: the manifest was not checked. This build will not load in Figma');
  say('until "node scripts/adopt-scaffold.mjs" has been run.');
  process.exit(0);
}

const report = inspectManifest(PLUGIN_DIR);
if (!report.ok) failLoudly(report);

say('');
say(`manifest.json is adopted: id ${report.manifest.id}, api ${report.manifest.api}`);
say('Build finished.');
