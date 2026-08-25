#!/usr/bin/env node
// Aninda Studio — adopt the two values only Figma can supply.
//
// Usage:  node scripts/adopt-scaffold.mjs /path/to/figma/manifest.json
//
// Reads the `id` and `api` from a manifest Figma generated, writes them into
// this plugin's manifest.json (built from manifest.template.json), and records
// what was adopted and when in scripts/figma-api-version.txt.
//
// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader

import { readFileSync, writeFileSync, existsSync, appendFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ADOPTED_FIELDS } from './manifest-gate.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const PLUGIN_DIR = resolve(HERE, '..');
const TEMPLATE = join(PLUGIN_DIR, 'manifest.template.json');
const TARGET = join(PLUGIN_DIR, 'manifest.json');
const RECORD = join(HERE, 'figma-api-version.txt');

function die(message) {
  process.stderr.write(`\nadopt-scaffold: ${message}\n\n`);
  process.exit(1);
}

const sourcePath = process.argv[2];
if (!sourcePath) {
  die(
    'I need the path to a manifest.json that Figma generated.\n' +
      '  Create one with Plugins > Development > New plugin... in the Figma\n' +
      '  desktop app, then run:\n' +
      '    node scripts/adopt-scaffold.mjs /path/to/that/manifest.json'
  );
}

const source = resolve(sourcePath);
if (!existsSync(source)) die(`there is no file at ${source}`);
if (!existsSync(TEMPLATE)) die(`manifest.template.json is missing from ${PLUGIN_DIR}`);

let generated;
try {
  generated = JSON.parse(readFileSync(source, 'utf8'));
} catch (error) {
  die(`${source} is not valid JSON: ${error.message}`);
}

const template = JSON.parse(readFileSync(TEMPLATE, 'utf8'));
const adopted = {};
for (const field of ADOPTED_FIELDS) {
  const value = generated[field];
  if (typeof value !== 'string' || value === '') {
    die(
      `the manifest at ${source} has no usable "${field}".\n` +
        '  That file may not be the one Figma generated. Look for the manifest.json\n' +
        '  sitting next to the code.js Figma created for you.'
    );
  }
  if (value.includes('REPLACE_ME')) {
    die(`the manifest at ${source} still has a placeholder in "${field}".`);
  }
  adopted[field] = value;
  template[field] = value;
}

writeFileSync(TARGET, JSON.stringify(template, null, 2) + '\n', 'utf8');

const stamp = new Date().toISOString().slice(0, 10);
const header = existsSync(RECORD)
  ? ''
  : [
      'Aninda Studio — Figma plugin id and api version, as adopted.',
      '',
      'Each line below records what was copied out of a manifest Figma wrote,',
      'out of a manifest Figma itself generated, and on what date. Nothing here',
      'was chosen by me or by any script.',
      '',
      'Written by scripts/adopt-scaffold.mjs.',
      '',
      '',
    ].join('\n');

const entry = [
  `date adopted : ${stamp}`,
  `id           : ${adopted.id}`,
  `api          : ${adopted.api}`,
  `copied from  : ${source}`,
  '',
  '',
].join('\n');

appendFileSync(RECORD, header + entry, 'utf8');

process.stdout.write(
  [
    '',
    'Adopted from the manifest Figma generated:',
    `  id   ${adopted.id}`,
    `  api  ${adopted.api}`,
    '',
    `Written to  ${TARGET}`,
    `Recorded in ${RECORD}`,
    '',
    'Next: run "node build.mjs".',
    '',
  ].join('\n')
);
