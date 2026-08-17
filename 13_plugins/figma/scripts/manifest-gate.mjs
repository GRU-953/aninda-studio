// Aninda Studio — the manifest gate.
//
// Figma generates two values that cannot be guessed: the plugin `id`, and the
// `api` version it currently accepts. Neither is published anywhere I can read,
// so this project never invents them. It copies them from a manifest Figma
// itself wrote, and refuses to go further until that has happened.
//
// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

export const PLACEHOLDER = 'REPLACE_ME__FIGMA_GENERATES_THIS';

/** Fields that must be adopted from Figma before the plugin can be loaded. */
export const ADOPTED_FIELDS = ['id', 'api'];

/**
 * Read manifest.json and report what is still a placeholder.
 * Returns { ok, missingFile, problems, manifest }.
 */
export function inspectManifest(pluginDir) {
  const path = join(pluginDir, 'manifest.json');
  if (!existsSync(path)) {
    return { ok: false, missingFile: true, problems: [], manifest: null, path };
  }
  let manifest;
  try {
    manifest = JSON.parse(readFileSync(path, 'utf8'));
  } catch (error) {
    return {
      ok: false,
      missingFile: false,
      problems: [`manifest.json is not valid JSON: ${error.message}`],
      manifest: null,
      path,
    };
  }
  const problems = [];
  for (const field of ADOPTED_FIELDS) {
    const value = manifest[field];
    if (value === undefined || value === null || value === '') {
      problems.push(`"${field}" is missing.`);
    } else if (typeof value === 'string' && value.includes('REPLACE_ME')) {
      problems.push(`"${field}" is still the placeholder ${JSON.stringify(value)}.`);
    }
  }
  return { ok: problems.length === 0, missingFile: false, problems, manifest, path };
}

/** The loud failure. Prints what to do, then exits with a non-zero status. */
export function failLoudly(report) {
  const line = '='.repeat(72);
  const out = [];
  out.push('');
  out.push(line);
  out.push('  BUILD STOPPED — the Figma manifest has not been adopted yet.');
  out.push(line);
  out.push('');
  if (report.missingFile) {
    out.push('  There is no manifest.json in the plugin folder.');
  } else {
    for (const problem of report.problems) out.push(`  ${problem}`);
  }
  out.push('');
  out.push('  I will not guess these two values.');
  out.push('');
  out.push('  The plugin "id" is issued by Figma when you create a plugin, and the');
  out.push('  "api" version is whatever your Figma build currently accepts. Figma');
  out.push('  does not publish either one, so a guess would be a number I made up.');
  out.push('  A wrong id or api version makes Figma refuse the plugin with an error');
  out.push('  that does not say why.');
  out.push('');
  out.push('  What to do, one step at a time:');
  out.push('');
  out.push('   1. Open the Figma desktop app.');
  out.push('   2. Open any design file.');
  out.push('   3. In the top-left menu, choose Plugins, then Development,');
  out.push('      then "New plugin...".');
  out.push('   4. Name it "Aninda Studio", choose "Figma design", and pick');
  out.push('      "Empty" as the template.');
  out.push('   5. Save it into a scratch folder — anywhere, it is thrown away.');
  out.push('   6. Come back here and run:');
  out.push('');
  out.push('        node scripts/adopt-scaffold.mjs /path/to/that/manifest.json');
  out.push('');
  out.push('   7. Run "node build.mjs" again.');
  out.push('');
  out.push(line);
  out.push('');
  process.stderr.write(out.join('\n'));
  process.exit(1);
}
