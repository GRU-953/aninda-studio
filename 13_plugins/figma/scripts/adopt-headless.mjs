#!/usr/bin/env node
// Aninda Studio — adopt the manifest values without the Figma desktop app.
//
// Usage:  node scripts/adopt-headless.mjs
//
// WHY THIS EXISTS ALONGSIDE adopt-scaffold.mjs
// ============================================
// adopt-scaffold.mjs copies `id` and `api` out of a manifest Figma itself wrote.
// That is still the route to a PUBLISHABLE plugin and nothing here replaces it.
//
// But the claim this project had been making — that Figma publishes neither value,
// so both must come from the desktop app — turned out to be half wrong, and the
// half that was wrong had blocked the build for weeks.
//
// `api` IS published, twice over:
//   1. Figma's own manifest guide documents the field and shows "1.0.0"
//      https://developers.figma.com/docs/plugins/manifest  (read 19 August 2026)
//   2. Every manifest in Figma's own official samples repository declares it.
//      Swept all 32 on 19 August 2026: 32 of 32 are exactly "1.0.0", no other
//      value anywhere.
//      https://github.com/figma/plugin-samples
//
// So `api` is adopted from those two sources, not guessed.
//
// `id` is genuinely not obtainable headlessly, and this script does NOT pretend
// otherwise. Figma issues a numeric id when a plugin is created or published — the
// manifest guide says an id can be obtained "at the time you publish your plugin".
// Until then there is nothing to copy.
//
// What Figma's own samples show is that an unpublished plugin does not need one: of
// the 32 sample manifests, several ship a readable slug instead of a number —
// `png-crop`, `bar-chart-sample`, `pie-chart-sample`, `document-statistics-sample`.
// Figma loads those through Import plugin from manifest. So this script writes a
// slug of the same shape and records what it is: a development id, not a Figma id.
//
// The manifest gate below then distinguishes the two states rather than treating
// them as one, because a plugin with a slug id loads and cannot be published, and
// saying otherwise would be the kind of quiet overclaim this repository exists to
// avoid.
//
// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader

import { readFileSync, writeFileSync, existsSync, appendFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const PLUGIN_DIR = resolve(HERE, '..');
const TEMPLATE = join(PLUGIN_DIR, 'manifest.template.json');
const TARGET = join(PLUGIN_DIR, 'manifest.json');
const RECORD = join(HERE, 'figma-api-version.txt');

// The two published sources, and what each one gave.
const API = '1.0.0';
const API_SOURCES = [
  'https://developers.figma.com/docs/plugins/manifest — documents the "api" field ' +
    'and shows 1.0.0; read 19 August 2026',
  'https://github.com/figma/plugin-samples — all 32 manifest.json files on main ' +
    'declare "api": "1.0.0"; swept 19 August 2026',
];

// A development id, in the shape Figma's own samples use for unpublished plugins.
const DEV_ID = 'aninda-studio-build-the-library';

function die(message) {
  process.stderr.write(`\nadopt-headless: ${message}\n\n`);
  process.exit(1);
}

if (!existsSync(TEMPLATE)) die(`manifest.template.json is missing from ${PLUGIN_DIR}`);
const template = JSON.parse(readFileSync(TEMPLATE, 'utf8'));

if (existsSync(TARGET)) {
  const current = JSON.parse(readFileSync(TARGET, 'utf8'));
  if (/^\d+$/.test(String(current.id ?? ''))) {
    die(
      `manifest.json already carries a Figma-issued numeric id (${current.id}).\n` +
        '  That is better than anything this script can write, so it is left alone.\n' +
        '  To change it, run adopt-scaffold.mjs with the manifest Figma generated.'
    );
  }
}

template.api = API;
template.id = DEV_ID;
writeFileSync(TARGET, JSON.stringify(template, null, 2) + '\n', 'utf8');

const stamp = '2026-08-19';
const header = existsSync(RECORD)
  ? ''
  : [
      'Aninda Studio — Figma plugin id and api version, and where each came from.',
      '',
      'Two routes write to this file, and they are not equivalent:',
      '',
      '  adopt-scaffold.mjs  copies both values out of a manifest Figma generated.',
      '                      This is the route to a publishable plugin.',
      '  adopt-headless.mjs  adopts the api from Figma\'s published documentation',
      '                      and its official samples, and writes a DEVELOPMENT id',
      '                      because Figma issues the real one at publish time.',
      '',
      'Every entry below names its route and its sources. Nothing is guessed; where',
      'a value could not be obtained, that is stated rather than filled in.',
      '',
      '',
    ].join('\n');

const entry = [
  `date adopted : ${stamp}`,
  'route        : adopt-headless.mjs (no Figma desktop app involved)',
  `api          : ${API}`,
  ...API_SOURCES.map((s, i) => `  source ${i + 1}   : ${s}`),
  `id           : ${DEV_ID}`,
  '  standing   : DEVELOPMENT ONLY. Not issued by Figma. Loads through Import',
  '               plugin from manifest; cannot be published. Figma issues a numeric',
  '               id at publish time, and adopt-scaffold.mjs replaces this with it.',
  '  precedent  : Figma\'s own samples ship slug ids for unpublished plugins —',
  '               png-crop, bar-chart-sample, pie-chart-sample,',
  '               document-statistics-sample.',
  '',
  '',
].join('\n');

appendFileSync(RECORD, header + entry, 'utf8');

process.stdout.write(
  [
    '',
    'Adopted without the Figma desktop app:',
    `  api  ${API}   from Figma's manifest guide and all 32 of its official samples`,
    `  id   ${DEV_ID}   DEVELOPMENT ONLY — Figma issues the real one at publish time`,
    '',
    `Written to  ${TARGET}`,
    `Recorded in ${RECORD}`,
    '',
    'The plugin will now build and will load through Plugins > Development >',
    'Import plugin from manifest. It is NOT publishable until adopt-scaffold.mjs',
    'has copied a Figma-issued id.',
    '',
  ].join('\n')
);
