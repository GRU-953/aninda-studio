// Aninda Studio — the manifest gate.
//
// Two manifest values do not come from this repository: the plugin `id` and the
// `api` version. This gate refuses to let either be a placeholder.
//
// The header here used to say neither was published anywhere readable. Half of that
// was wrong, and the wrong half blocked the build for weeks. `api` IS published: it
// is documented in Figma's manifest guide, and all 32 manifests in Figma's own
// official samples repository declare exactly "1.0.0" — swept 19 August 2026. So it
// is adopted from those, not guessed. See scripts/adopt-headless.mjs.
//
// The `id` genuinely is not obtainable without Figma: it is issued when a plugin is
// created or published. So there are two legitimate states, and this gate now tells
// them apart rather than calling both "adopted":
//
//   a numeric id   issued by Figma. The plugin can be published.
//   a slug id      a development id, the shape Figma's own samples use for
//                  unpublished plugins. It loads through Import plugin from
//                  manifest and cannot be published.
//
// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

export const PLACEHOLDER = 'REPLACE_ME__FIGMA_GENERATES_THIS';

/** Fields that must be adopted from Figma before the plugin can be loaded. */
export const ADOPTED_FIELDS = ['id', 'api'];

/**
 * The one api version this repository has a source for.
 * Recorded, with both sources and the date each was read, in
 * scripts/figma-api-version.txt. adopt-headless.mjs writes the same value.
 */
export const KNOWN_API = '1.0.0';

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
  // Each field must be a non-empty string. This used to accept anything that was
  // not undefined, null or '' — so a number, an object, an array, a boolean and a
  // whitespace-only string all passed, and the build then printed
  // "adopted for DEVELOPMENT: id [object Object], api [object Object]" and exited
  // 0. adopt-scaffold.mjs was already this strict; the two disagreed about what a
  // valid manifest is, and the looser one was the one that ships.
  for (const field of ADOPTED_FIELDS) {
    const value = manifest[field];
    if (value === undefined || value === null || value === '') {
      problems.push(`"${field}" is missing.`);
    } else if (typeof value !== 'string') {
      problems.push(
        `"${field}" is ${Array.isArray(value) ? 'an array' : typeof value}, ` +
        `not a string: ${JSON.stringify(value)}.`);
    } else if (value.trim() === '') {
      problems.push(`"${field}" is only whitespace.`);
    } else if (value.includes('REPLACE_ME')) {
      problems.push(`"${field}" is still the placeholder ${JSON.stringify(value)}.`);
    }
  }
  // And the api is checked against the one value this repository records, rather
  // than merely being non-empty. The gate's own failure text says "a wrong id or
  // api version makes Figma refuse the plugin with an error that does not say why"
  // — it could not act on that, because it never compared. scripts/figma-api-version.txt
  // holds the value and both of its sources.
  if (typeof manifest.api === 'string' && manifest.api.trim() !== ''
      && !manifest.api.includes('REPLACE_ME') && manifest.api !== KNOWN_API) {
    problems.push(
      `"api" is ${JSON.stringify(manifest.api)}. The only value this repository ` +
      `has a source for is ${JSON.stringify(KNOWN_API)} — Figma's manifest guide ` +
      `and all 32 of its official sample manifests. See ` +
      `scripts/figma-api-version.txt. If Figma has published a new version, adopt ` +
      `it there first, with its source and the date it was read.`);
  }
  // Loadable and publishable are different states, and the gate used to know only
  // one of them. A slug id — the shape Figma's own samples use for unpublished
  // plugins — loads perfectly through Import plugin from manifest and can never be
  // published, because publishing needs an id Figma issued. Reporting that as simply
  // "adopted" would let the build imply the plugin is ready to ship when it is not.
  const publishable = /^\d+$/.test(String(manifest.id ?? ''));
  return {
    ok: problems.length === 0,
    missingFile: false,
    problems,
    manifest,
    path,
    publishable,
  };
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
  out.push('  The plugin "id" is issued by Figma when you create or publish a');
  out.push('  plugin, so there is nothing here to copy it from. The "api" version');
  out.push('  IS published — see adopt-headless.mjs, which reads it from Figma\'s own');
  out.push('  manifest guide and from all 32 of its official sample manifests.');
  out.push('  A wrong id or api version makes Figma refuse the plugin with an error');
  out.push('  that does not say why, which is why neither is ever invented here.');
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
  out.push('  OR, with no Figma app to hand:');
  out.push('');
  out.push('        node scripts/adopt-headless.mjs');
  out.push('');
  out.push('  That adopts the api version from Figma\'s published manifest guide and');
  out.push('  from all 32 of its official sample manifests, and writes a development');
  out.push('  id of the shape Figma\'s own samples use. The plugin then builds and');
  out.push('  loads. It cannot be published until a Figma-issued id replaces that.');
  out.push('');
  out.push(line);
  out.push('');
  process.stderr.write(out.join('\n'));
  process.exit(1);
}
