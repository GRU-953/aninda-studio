// Aninda Studio — the Figma plugin.
//
// Three commands:
//   build  make the library in this file
//   probe  report what this file and this plan allow, and make nothing
//   wipe   remove exactly what this plugin made, and nothing else
//
// Everything it creates carries setPluginData("as-built", "1"), so wipe can be
// exact. Every pass finds by name first and updates in place, so running build
// twice makes one library, not two.
//
// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader

import {
  buildPlan,
  PAGE_CARDS,
  PAGE_COMPONENTS,
  PAGE_MARKS,
  PLUGIN_DATA_KEY,
  PLUGIN_DATA_VALUE,
  THEME_MODES,
} from './plan';
import type { ComponentSpec, Plan, RawInput, TextStyleSpec, VarValue } from './plan';
import { BUNDLED, BUNDLE_SHA256, SOURCE_HASHES } from './tokens.generated';

// ---------------------------------------------------------------------------
// Receipt
// ---------------------------------------------------------------------------

interface Skip {
  what: string;
  why: string;
}

interface ProbeResult {
  fonts: { required: string[]; missing: string[]; ok: boolean };
  variables: { ok: boolean; reason: string };
  variableModes: { limit: number; reason: string };
  createNodeFromSvg: { ok: boolean; reason: string };
  combineAsVariants: { ok: boolean; reason: string };
}

interface Receipt {
  command: string;
  tokensSha256: string;
  tokensSource: string;
  sourceHashes: { [file: string]: string };
  mode: 'variables' | 'styles-only' | 'not run';
  probe: ProbeResult | null;
  created: { [key: string]: number };
  skipped: Skip[];
  decisions: Skip[];
  knownGaps: Skip[];
  stopped: string | null;
}

function emptyReceipt(command: string, sha: string, source: string): Receipt {
  return {
    command,
    tokensSha256: sha,
    tokensSource: source,
    sourceHashes: SOURCE_HASHES,
    mode: 'not run',
    probe: null,
    created: {},
    skipped: [],
    decisions: [],
    knownGaps: [],
    stopped: null,
  };
}

function count(receipt: Receipt, key: string, by: number): void {
  receipt.created[key] = (receipt.created[key] || 0) + by;
}

function reason(error: unknown): string {
  if (error instanceof Error) return error.message;
  return String(error);
}

function mark(target: { setPluginData(key: string, value: string): void }): void {
  target.setPluginData(PLUGIN_DATA_KEY, PLUGIN_DATA_VALUE);
}

function progress(message: string): void {
  figma.ui.postMessage({ type: 'progress', message });
}

// ---------------------------------------------------------------------------
// Colour helpers
// ---------------------------------------------------------------------------

interface Rgba {
  r: number;
  g: number;
  b: number;
  a: number;
}

function primitiveColours(plan: Plan): { [name: string]: Rgba } {
  const out: { [name: string]: Rgba } = {};
  for (const variable of plan.collections[0].variables) {
    const value = variable.values['Value'];
    if (value.kind === 'color') out[variable.name] = { r: value.r, g: value.g, b: value.b, a: value.a };
  }
  return out;
}

function resolveThemeColour(plan: Plan, modeLabel: string, variableName: string): Rgba {
  const primitives = primitiveColours(plan);
  const theme = plan.collections[1];
  for (const variable of theme.variables) {
    if (variable.name !== variableName) continue;
    const value = variable.values[modeLabel];
    if (!value) break;
    if (value.kind === 'color') return { r: value.r, g: value.g, b: value.b, a: value.a };
    if (value.kind === 'alias') {
      const target = primitives[value.variable];
      if (target) return target;
      throw new Error(`the alias ${variableName} points at ${value.variable}, which is not a primitive colour`);
    }
  }
  throw new Error(`no colour for ${variableName} in the ${modeLabel} mode`);
}

function solid(colour: Rgba): SolidPaint {
  return {
    type: 'SOLID',
    color: { r: colour.r, g: colour.g, b: colour.b },
    opacity: colour.a,
  };
}

function prettyRole(path: string): string {
  const parts = path.split('/').slice(1);
  const out: string[] = [];
  for (const part of parts) out.push(part.charAt(0).toUpperCase() + part.slice(1));
  return out.join('/');
}

// ---------------------------------------------------------------------------
// Pass 0 — the probe
// ---------------------------------------------------------------------------

async function runProbe(plan: Plan): Promise<ProbeResult> {
  // Fonts first. If one is missing the run stops here, before anything is made.
  const available = await figma.listAvailableFontsAsync();
  const have: { [key: string]: boolean } = {};
  for (const font of available) have[`${font.fontName.family}|${font.fontName.style}`] = true;

  const required: string[] = [];
  const missing: string[] = [];
  for (const need of plan.fontsRequired) {
    const label = `${need.family} ${need.style}`;
    required.push(label);
    if (!have[`${need.family}|${need.style}`]) missing.push(label);
  }

  const result: ProbeResult = {
    fonts: { required, missing, ok: missing.length === 0 },
    variables: { ok: false, reason: '' },
    variableModes: { limit: 0, reason: '' },
    createNodeFromSvg: { ok: false, reason: '' },
    combineAsVariants: { ok: false, reason: '' },
  };

  // Variables. It is not documented whether the plugin Variables API is gated
  // by plan, so this asks rather than assumes.
  let probeCollection: VariableCollection | null = null;
  try {
    probeCollection = figma.variables.createVariableCollection('Aninda Studio probe');
    result.variables.ok = true;
  } catch (error) {
    result.variables.reason = reason(error);
  }

  // Modes are separately limited: a collection can hold more than one mode only
  // on some plans, and the message says how many.
  if (probeCollection) {
    let limit = 1;
    try {
      for (let i = 0; i < 3; i += 1) {
        probeCollection.addMode(`probe ${i}`);
        limit += 1;
      }
      result.variableModes.reason = 'four modes were accepted.';
    } catch (error) {
      result.variableModes.reason = reason(error);
    }
    result.variableModes.limit = limit;
    try {
      probeCollection.remove();
    } catch (error) {
      result.variables.reason = `created, but could not be removed again: ${reason(error)}`;
    }
  }

  try {
    const node = figma.createNodeFromSvg(
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2 2"><rect width="2" height="2"/></svg>'
    );
    node.remove();
    result.createNodeFromSvg.ok = true;
  } catch (error) {
    result.createNodeFromSvg.reason = reason(error);
  }

  let a: ComponentNode | null = null;
  let b: ComponentNode | null = null;
  try {
    a = figma.createComponent();
    a.name = 'Probe=A';
    b = figma.createComponent();
    b.name = 'Probe=B';
    const set = figma.combineAsVariants([a, b], figma.currentPage);
    set.remove();
    a = null;
    b = null;
    result.combineAsVariants.ok = true;
  } catch (error) {
    result.combineAsVariants.reason = reason(error);
  } finally {
    if (a && !a.removed) a.remove();
    if (b && !b.removed) b.remove();
  }

  return result;
}

// ---------------------------------------------------------------------------
// Pass 1 — variables
// ---------------------------------------------------------------------------

interface VariableIndex {
  byCollection: { [collection: string]: { [name: string]: Variable } };
  modeIds: { [collection: string]: { [modeLabel: string]: string } };
}

async function ensureCollections(
  plan: Plan,
  receipt: Receipt,
  modeLimit: number
): Promise<VariableIndex> {
  const index: VariableIndex = { byCollection: {}, modeIds: {} };
  const existing = await figma.variables.getLocalVariableCollectionsAsync();
  const allVariables = await figma.variables.getLocalVariablesAsync();

  for (const spec of plan.collections) {
    let collection: VariableCollection | null = null;
    for (const candidate of existing) {
      if (candidate.name === spec.name) {
        collection = candidate;
        break;
      }
    }
    if (!collection) {
      collection = figma.variables.createVariableCollection(spec.name);
      count(receipt, 'variableCollections', 1);
    }
    mark(collection);

    const wantedModes = spec.modes.slice(0, Math.max(1, modeLimit));
    if (wantedModes.length < spec.modes.length) {
      for (const dropped of spec.modes.slice(wantedModes.length)) {
        receipt.skipped.push({
          what: `The "${dropped}" mode of the ${spec.name} collection`,
          why:
            `this Figma file allows ${modeLimit} mode(s) per collection. The number of modes a collection may ` +
            'hold is set by the plan the file belongs to, and this plugin cannot change it.',
        });
      }
    }

    const modeIds: { [label: string]: string } = {};
    for (let i = 0; i < wantedModes.length; i += 1) {
      const label = wantedModes[i];
      let found = '';
      for (const mode of collection.modes) {
        if (mode.name === label) {
          found = mode.modeId;
          break;
        }
      }
      if (!found && i < collection.modes.length) {
        collection.renameMode(collection.modes[i].modeId, label);
        found = collection.modes[i].modeId;
      }
      if (!found) {
        try {
          found = collection.addMode(label);
        } catch (error) {
          receipt.skipped.push({
            what: `The "${label}" mode of the ${spec.name} collection`,
            why: reason(error),
          });
          continue;
        }
      }
      modeIds[label] = found;
    }
    index.modeIds[spec.name] = modeIds;

    const owned: { [name: string]: Variable } = {};
    for (const variable of allVariables) {
      if (variable.variableCollectionId === collection.id) owned[variable.name] = variable;
    }
    index.byCollection[spec.name] = owned;
  }

  return index;
}

function setVariableValue(
  variable: Variable,
  modeId: string,
  value: VarValue,
  index: VariableIndex
): void {
  if (value.kind === 'color') {
    variable.setValueForMode(modeId, { r: value.r, g: value.g, b: value.b, a: value.a });
  } else if (value.kind === 'float') {
    variable.setValueForMode(modeId, value.value);
  } else if (value.kind === 'string') {
    variable.setValueForMode(modeId, value.value);
  } else if (value.kind === 'easing') {
    variable.setValueForMode(modeId, {
      type: 'CUSTOM_CUBIC_BEZIER',
      easingFunctionCubicBezier: { x1: value.x1, y1: value.y1, x2: value.x2, y2: value.y2 },
    });
  } else {
    const target = index.byCollection[value.collection][value.variable];
    if (!target) throw new Error(`the alias target ${value.collection}/${value.variable} does not exist`);
    variable.setValueForMode(modeId, figma.variables.createVariableAlias(target));
  }
}

async function passVariables(plan: Plan, receipt: Receipt, modeLimit: number): Promise<VariableIndex> {
  const index = await ensureCollections(plan, receipt, modeLimit);

  for (const spec of plan.collections) {
    const collections = await figma.variables.getLocalVariableCollectionsAsync();
    let collection: VariableCollection | null = null;
    for (const candidate of collections) {
      if (candidate.name === spec.name) collection = candidate;
    }
    if (!collection) {
      receipt.skipped.push({
        what: `Every variable in the ${spec.name} collection`,
        why: 'the collection itself could not be found after it was made.',
      });
      continue;
    }

    for (const variableSpec of spec.variables) {
      let variable = index.byCollection[spec.name][variableSpec.name] || null;
      if (!variable) {
        try {
          variable = figma.variables.createVariable(
            variableSpec.name,
            collection,
            variableSpec.resolvedType as VariableResolvedDataType
          );
          count(receipt, 'variables', 1);
        } catch (error) {
          receipt.skipped.push({
            what: `Variable ${spec.name}/${variableSpec.name}`,
            why: reason(error),
          });
          continue;
        }
        index.byCollection[spec.name][variableSpec.name] = variable;
      } else {
        count(receipt, 'variablesUpdated', 1);
      }
      mark(variable);
      if (variableSpec.description) variable.description = variableSpec.description;

      for (const modeLabel of Object.keys(index.modeIds[spec.name])) {
        const value = variableSpec.values[modeLabel];
        if (!value) continue;
        const modeId = index.modeIds[spec.name][modeLabel];
        try {
          setVariableValue(variable, modeId, value, index);
          if (value.kind === 'alias') count(receipt, 'variableAliases', 1);
        } catch (error) {
          receipt.skipped.push({
            what: `The ${modeLabel} value of ${spec.name}/${variableSpec.name}`,
            why: reason(error),
          });
        }
      }
    }
  }

  return index;
}

// ---------------------------------------------------------------------------
// Pass 2 — styles
// ---------------------------------------------------------------------------

interface StyleIndex {
  paint: { [name: string]: PaintStyle };
  text: { [name: string]: TextStyle };
  effect: { [name: string]: EffectStyle };
  grid: { [name: string]: GridStyle };
  /** Given a semantic role path, the paint style a node should use. */
  paintForRole: (role: string) => PaintStyle | null;
}

async function passPaintStyles(
  plan: Plan,
  receipt: Receipt,
  index: VariableIndex | null
): Promise<{ [name: string]: PaintStyle }> {
  const existing = await figma.getLocalPaintStylesAsync();
  const byName: { [name: string]: PaintStyle } = {};
  for (const style of existing) byName[style.name] = style;

  const make = (name: string, description: string): PaintStyle => {
    let style = byName[name];
    if (!style) {
      style = figma.createPaintStyle();
      style.name = name;
      byName[name] = style;
      count(receipt, 'paintStyles', 1);
    } else {
      count(receipt, 'paintStylesUpdated', 1);
    }
    style.description = description;
    mark(style);
    return style;
  };

  if (index) {
    for (const spec of plan.paintStyles) {
      const style = make(spec.name, spec.description);
      const variable = index.byCollection[spec.bindTo.collection][spec.bindTo.variable];
      const base = solid(resolveThemeColour(plan, 'Light', spec.bindTo.variable));
      if (!variable) {
        style.paints = [base];
        receipt.skipped.push({
          what: `The variable binding on paint style ${spec.name}`,
          why: 'the Theme variable it should follow was not made, so the style holds the Light value instead.',
        });
        continue;
      }
      try {
        style.paints = [figma.variables.setBoundVariableForPaint(base, 'color', variable)];
      } catch (error) {
        style.paints = [base];
        receipt.skipped.push({
          what: `The variable binding on paint style ${spec.name}`,
          why: reason(error),
        });
      }
    }
    return byName;
  }

  // Styles-only mode. Without variables Figma has no idea of a mode, so each of
  // the four themes becomes its own set of plain paint styles.
  for (const mode of THEME_MODES) {
    for (const spec of plan.paintStyles) {
      const role = spec.bindTo.variable;
      const name = `${mode.label}/${prettyRole(role)}`;
      const style = make(
        name,
        `${spec.description} Variables were not available in this file, so this style holds the ${mode.label} value directly and does not follow a mode.`
      );
      style.paints = [solid(resolveThemeColour(plan, mode.label, role))];
    }
  }
  return byName;
}

async function passTextStyles(
  plan: Plan,
  receipt: Receipt,
  index: VariableIndex | null
): Promise<{ [name: string]: TextStyle }> {
  const existing = await figma.getLocalTextStylesAsync();
  const byName: { [name: string]: TextStyle } = {};
  for (const style of existing) byName[style.name] = style;

  for (const spec of plan.textStyles) {
    let style = byName[spec.name];
    if (!style) {
      style = figma.createTextStyle();
      style.name = spec.name;
      byName[spec.name] = style;
      count(receipt, 'textStyles', 1);
    } else {
      count(receipt, 'textStylesUpdated', 1);
    }
    mark(style);
    style.description = spec.description;
    style.fontName = { family: spec.family, style: spec.style };
    style.fontSize = spec.fontSize;
    style.lineHeight =
      spec.lineHeightPercent === null
        ? { unit: 'AUTO' }
        : { unit: 'PERCENT', value: spec.lineHeightPercent };
    style.letterSpacing = { unit: 'PERCENT', value: 0 };

    bindTextField(style, spec, receipt, index);
  }
  return byName;
}

function bindTextField(
  style: TextStyle,
  spec: TextStyleSpec,
  receipt: Receipt,
  index: VariableIndex | null
): void {
  if (!index) {
    if (spec.bindFontSize || spec.bindFontFamily) {
      receipt.skipped.push({
        what: `The variable bindings on text style ${spec.name}`,
        why: 'variables were not available in this file, so the size and family are held as plain numbers.',
      });
    }
    return;
  }
  const bindings: { field: 'fontSize' | 'fontFamily'; variable: string | null }[] = [
    { field: 'fontSize', variable: spec.bindFontSize },
    { field: 'fontFamily', variable: spec.bindFontFamily },
  ];
  for (const binding of bindings) {
    if (!binding.variable) continue;
    const variable = index.byCollection['Primitives'][binding.variable];
    if (!variable) {
      receipt.skipped.push({
        what: `The ${binding.field} binding on text style ${spec.name}`,
        why: `the primitive variable ${binding.variable} was not made.`,
      });
      continue;
    }
    try {
      style.setBoundVariable(binding.field, variable);
    } catch (error) {
      receipt.skipped.push({
        what: `The ${binding.field} binding on text style ${spec.name}`,
        why: reason(error),
      });
    }
  }
}

async function passEffectStyles(
  plan: Plan,
  receipt: Receipt,
  index: VariableIndex | null
): Promise<{ [name: string]: EffectStyle }> {
  const existing = await figma.getLocalEffectStylesAsync();
  const byName: { [name: string]: EffectStyle } = {};
  for (const style of existing) byName[style.name] = style;

  for (const spec of plan.effectStyles) {
    let style = byName[spec.name];
    if (!style) {
      style = figma.createEffectStyle();
      style.name = spec.name;
      byName[spec.name] = style;
      count(receipt, 'effectStyles', 1);
    } else {
      count(receipt, 'effectStylesUpdated', 1);
    }
    mark(style);
    style.description = spec.description;

    const colour = spec.bindColor
      ? resolveThemeColour(plan, 'Light', spec.bindColor.variable)
      : { r: 0, g: 0, b: 0, a: 1 };
    let effect: Effect = {
      type: 'DROP_SHADOW',
      color: { r: colour.r, g: colour.g, b: colour.b, a: colour.a },
      offset: { x: 0, y: 0 },
      radius: spec.radius,
      spread: spec.spread,
      visible: true,
      blendMode: 'NORMAL',
    };

    if (index) {
      if (spec.bindColor) {
        const variable = index.byCollection[spec.bindColor.collection][spec.bindColor.variable];
        if (variable) {
          try {
            effect = figma.variables.setBoundVariableForEffect(effect, 'color', variable);
          } catch (error) {
            receipt.skipped.push({ what: `The colour binding on ${spec.name}`, why: reason(error) });
          }
        }
      }
      if (spec.bindSpread) {
        const variable = index.byCollection['Primitives'][spec.bindSpread];
        if (variable) {
          try {
            effect = figma.variables.setBoundVariableForEffect(effect, 'spread', variable);
          } catch (error) {
            receipt.skipped.push({ what: `The spread binding on ${spec.name}`, why: reason(error) });
          }
        }
      }
    } else {
      receipt.skipped.push({
        what: `The variable bindings on effect style ${spec.name}`,
        why: 'variables were not available in this file, so the ring holds the Light colour directly.',
      });
    }

    style.effects = [effect];
  }
  return byName;
}

async function passGridStyles(
  plan: Plan,
  receipt: Receipt,
  index: VariableIndex | null
): Promise<{ [name: string]: GridStyle }> {
  const existing = await figma.getLocalGridStylesAsync();
  const byName: { [name: string]: GridStyle } = {};
  for (const style of existing) byName[style.name] = style;

  for (const spec of plan.gridStyles) {
    let style = byName[spec.name];
    if (!style) {
      style = figma.createGridStyle();
      style.name = spec.name;
      byName[spec.name] = style;
      count(receipt, 'gridStyles', 1);
    } else {
      count(receipt, 'gridStylesUpdated', 1);
    }
    mark(style);
    style.description = spec.description;

    const grids: LayoutGrid[] = [];
    for (const grid of spec.grids) {
      let made: LayoutGrid =
        grid.pattern === 'GRID'
          ? { pattern: 'GRID', sectionSize: grid.sectionSize || 8, visible: true }
          : {
              pattern: grid.pattern,
              alignment: grid.alignment || 'STRETCH',
              gutterSize: grid.gutterSize || 0,
              count: grid.count || 1,
              offset: grid.offset || 0,
              visible: true,
            };
      if (index) {
        if (spec.bindGutter) {
          const variable = index.byCollection['Primitives'][spec.bindGutter];
          if (variable) {
            try {
              made = figma.variables.setBoundVariableForLayoutGrid(made, 'gutterSize', variable);
            } catch (error) {
              receipt.skipped.push({ what: `The gutter binding on ${spec.name}`, why: reason(error) });
            }
          }
        }
        if (spec.bindOffset) {
          const variable = index.byCollection['Primitives'][spec.bindOffset];
          if (variable) {
            try {
              made = figma.variables.setBoundVariableForLayoutGrid(made, 'offset', variable);
            } catch (error) {
              receipt.skipped.push({ what: `The margin binding on ${spec.name}`, why: reason(error) });
            }
          }
        }
      }
      grids.push(made);
    }
    style.layoutGrids = grids;
  }
  return byName;
}

// ---------------------------------------------------------------------------
// Pages and nodes
// ---------------------------------------------------------------------------

async function ensurePage(name: string, receipt: Receipt): Promise<PageNode> {
  for (const page of figma.root.children) {
    if (page.name === name) {
      await page.loadAsync();
      mark(page);
      return page;
    }
  }
  const page = figma.createPage();
  page.name = name;
  mark(page);
  count(receipt, 'pages', 1);
  await page.loadAsync();
  return page;
}

function removeNamed(parent: BaseNode & ChildrenMixin, name: string): boolean {
  let removed = false;
  for (const child of parent.children.slice()) {
    if (child.name === name) {
      child.remove();
      removed = true;
    }
  }
  return removed;
}

function findNamed(parent: BaseNode & ChildrenMixin, name: string): SceneNode | null {
  for (const child of parent.children) if (child.name === name) return child;
  return null;
}

async function makeText(
  characters: string,
  styleName: string,
  colourRole: string,
  styles: StyleIndex,
  receipt: Receipt
): Promise<TextNode> {
  const node = figma.createText();
  const style = styles.text[styleName];
  if (style) {
    await figma.loadFontAsync(style.fontName as FontName);
    node.fontName = style.fontName as FontName;
    node.characters = characters;
    await node.setTextStyleIdAsync(style.id);
  } else {
    await figma.loadFontAsync({ family: 'Literata', style: 'Regular' });
    node.characters = characters;
    receipt.skipped.push({
      what: `The text style ${styleName} on a piece of text`,
      why: 'that style was not made, so the text carries no style.',
    });
  }
  const paint = styles.paintForRole(colourRole);
  if (paint) {
    await node.setFillStyleIdAsync(paint.id);
  } else {
    receipt.skipped.push({
      what: `The colour ${colourRole} on a piece of text`,
      why: 'no paint style was made for that role.',
    });
  }
  mark(node);
  return node;
}

// ---------------------------------------------------------------------------
// Pass 3 — the marks
// ---------------------------------------------------------------------------

async function passMarks(plan: Plan, receipt: Receipt, probe: ProbeResult): Promise<void> {
  const page = await ensurePage(PAGE_MARKS, receipt);

  if (!probe.createNodeFromSvg.ok) {
    receipt.skipped.push({
      what: `All ${plan.marks.length} marks, and the Mark component set`,
      why: `createNodeFromSvg is not available in this file: ${probe.createNodeFromSvg.reason}`,
    });
    return;
  }

  let x = 0;
  for (const spec of plan.marks) {
    const name = `Mark/${spec.name}`;
    removeNamed(page, name);
    let node: FrameNode;
    try {
      node = figma.createNodeFromSvg(spec.svg);
    } catch (error) {
      receipt.skipped.push({ what: `The mark ${spec.file}`, why: reason(error) });
      continue;
    }
    node.name = name;
    page.appendChild(node);
    node.x = x;
    node.y = 0;
    x += node.width + 64;
    markTree(node);
    count(receipt, 'marks', 1);
  }

  // The two mark weights as one component set, so a designer swaps weight
  // rather than hunting for a second file.
  const setName = plan.markSet.name;
  const existingSet = findNamed(page, setName);
  const madeComponents: ComponentNode[] = [];
  if (existingSet && existingSet.type === 'COMPONENT_SET') {
    for (const variant of plan.markSet.variants) {
      const variantName = `${plan.markSet.property}=${variant.value}`;
      let component = findNamed(existingSet, variantName);
      if (!component || component.type !== 'COMPONENT') {
        component = figma.createComponent();
        component.name = variantName;
        existingSet.appendChild(component);
      }
      fillMarkComponent(component as ComponentNode, variant.svg, receipt);
      count(receipt, 'markSetVariantsUpdated', 1);
    }
    mark(existingSet);
    return;
  }

  if (existingSet) existingSet.remove();
  for (const variant of plan.markSet.variants) {
    const component = figma.createComponent();
    component.name = `${plan.markSet.property}=${variant.value}`;
    page.appendChild(component);
    fillMarkComponent(component, variant.svg, receipt);
    madeComponents.push(component);
  }

  if (!probe.combineAsVariants.ok) {
    for (const component of madeComponents) {
      component.name = `${setName} — ${component.name}`;
      count(receipt, 'markSetVariants', 1);
    }
    receipt.skipped.push({
      what: `The Mark component set`,
      why:
        `combineAsVariants is not available in this file (${probe.combineAsVariants.reason}), so the two ` +
        'weights were left as two separate components instead of one set.',
    });
    return;
  }

  try {
    const set = figma.combineAsVariants(madeComponents, page);
    set.name = setName;
    set.description = 'The mark in its two stroke weights. Stroke 9 at 24 px and above, stroke 15 below.';
    mark(set);
    for (const child of set.children) mark(child);
    count(receipt, 'markSetVariants', madeComponents.length);
  } catch (error) {
    receipt.skipped.push({ what: 'The Mark component set', why: reason(error) });
  }
}

function fillMarkComponent(component: ComponentNode, svg: string, receipt: Receipt): void {
  for (const child of component.children.slice()) child.remove();
  let node: FrameNode;
  try {
    node = figma.createNodeFromSvg(svg);
  } catch (error) {
    receipt.skipped.push({ what: `A mark variant`, why: reason(error) });
    return;
  }
  component.resizeWithoutConstraints(node.width, node.height);
  component.appendChild(node);
  node.x = 0;
  node.y = 0;
  markTree(component);
}

function markTree(node: SceneNode): void {
  mark(node);
  const withChildren = node as SceneNode & Partial<ChildrenMixin>;
  if (withChildren.children) {
    for (const child of withChildren.children) markTree(child);
  }
}

// ---------------------------------------------------------------------------
// Pass 4 — components
// ---------------------------------------------------------------------------

async function passComponents(plan: Plan, receipt: Receipt, styles: StyleIndex, probe: ProbeResult): Promise<void> {
  const page = await ensurePage(PAGE_COMPONENTS, receipt);
  let y = 0;

  for (const setName of plan.componentSets) {
    const specs = plan.components.filter((c) => c.set === setName);
    const existing = findNamed(page, setName);
    const components: ComponentNode[] = [];

    if (existing && existing.type === 'COMPONENT_SET') {
      for (const spec of specs) {
        let node = findNamed(existing, spec.name);
        if (!node || node.type !== 'COMPONENT') {
          node = figma.createComponent();
          node.name = spec.name;
          existing.appendChild(node);
        }
        await paintComponent(node as ComponentNode, spec, styles, receipt);
        count(receipt, 'componentsUpdated', 1);
      }
      mark(existing);
      existing.y = y;
      y += existing.height + 96;
      continue;
    }
    if (existing) existing.remove();

    for (const spec of specs) {
      const node = figma.createComponent();
      node.name = spec.name;
      page.appendChild(node);
      await paintComponent(node, spec, styles, receipt);
      components.push(node);
    }

    if (!probe.combineAsVariants.ok) {
      for (const node of components) {
        node.name = `${setName} — ${node.name}`;
        count(receipt, 'components', 1);
      }
      receipt.skipped.push({
        what: `The ${setName} component set`,
        why:
          `combineAsVariants is not available in this file (${probe.combineAsVariants.reason}), so its ` +
          `${components.length} variants were left as separate components.`,
      });
      continue;
    }

    try {
      const set = figma.combineAsVariants(components, page);
      set.name = setName;
      mark(set);
      set.y = y;
      y += set.height + 96;
      count(receipt, 'components', components.length);
      count(receipt, 'componentSets', 1);
    } catch (error) {
      receipt.skipped.push({ what: `The ${setName} component set`, why: reason(error) });
    }
  }

  for (const spec of plan.components) {
    if (spec.set !== null) continue;
    let node = findNamed(page, spec.name);
    if (node && node.type !== 'COMPONENT') {
      node.remove();
      node = null;
    }
    if (!node) {
      node = figma.createComponent();
      node.name = spec.name;
      page.appendChild(node);
      count(receipt, 'components', 1);
    } else {
      count(receipt, 'componentsUpdated', 1);
    }
    await paintComponent(node as ComponentNode, spec, styles, receipt);
    (node as ComponentNode).y = y;
    y += (node as ComponentNode).height + 96;
  }
}

async function paintComponent(
  component: ComponentNode,
  spec: ComponentSpec,
  styles: StyleIndex,
  receipt: Receipt
): Promise<void> {
  for (const child of component.children.slice()) child.remove();
  mark(component);

  if (spec.kind === 'input') {
    component.layoutMode = 'VERTICAL';
    component.primaryAxisSizingMode = 'AUTO';
    component.counterAxisSizingMode = 'FIXED';
    component.itemSpacing = 8;
    component.fills = [];
    component.resizeWithoutConstraints(spec.width, component.height);

    const label = await makeText(spec.lines[0].text, spec.lines[0].textStyle, spec.lines[0].colourRole, styles, receipt);
    component.appendChild(label);

    const field = figma.createFrame();
    field.name = 'Field';
    field.layoutMode = 'HORIZONTAL';
    field.primaryAxisSizingMode = 'FIXED';
    field.counterAxisSizingMode = 'AUTO';
    field.counterAxisAlignItems = 'CENTER';
    field.paddingLeft = spec.paddingX;
    field.paddingRight = spec.paddingX;
    field.paddingTop = spec.paddingY;
    field.paddingBottom = spec.paddingY;
    field.cornerRadius = spec.cornerRadius;
    field.minHeight = spec.height;
    field.layoutAlign = 'STRETCH';
    mark(field);
    component.appendChild(field);
    await applySurface(field, spec, styles, receipt);
    const placeholder = await makeText(
      spec.lines[1].text,
      spec.lines[1].textStyle,
      spec.lines[1].colourRole,
      styles,
      receipt
    );
    field.appendChild(placeholder);
    if (spec.focusRing && styles.effect['Focus/Ring']) {
      await field.setEffectStyleIdAsync(styles.effect['Focus/Ring'].id);
    }
    return;
  }

  component.layoutMode = spec.kind === 'card' ? 'VERTICAL' : 'HORIZONTAL';
  component.primaryAxisSizingMode = spec.kind === 'card' ? 'AUTO' : 'AUTO';
  component.counterAxisSizingMode = spec.kind === 'card' ? 'FIXED' : 'AUTO';
  component.counterAxisAlignItems = 'CENTER';
  component.primaryAxisAlignItems = 'CENTER';
  component.paddingLeft = spec.paddingX;
  component.paddingRight = spec.paddingX;
  component.paddingTop = spec.paddingY;
  component.paddingBottom = spec.paddingY;
  component.cornerRadius = spec.cornerRadius;
  component.itemSpacing = 16;
  if (spec.height > 0) component.minHeight = spec.height;
  if (spec.width > 0) component.resizeWithoutConstraints(spec.width, component.height);
  if (spec.kind === 'card') {
    component.counterAxisAlignItems = 'MIN';
    component.primaryAxisAlignItems = 'MIN';
  }
  await applySurface(component, spec, styles, receipt);

  for (const line of spec.lines) {
    const text = await makeText(line.text, line.textStyle, line.colourRole, styles, receipt);
    component.appendChild(text);
    if (spec.kind === 'card') text.layoutAlign = 'STRETCH';
  }
}

async function applySurface(
  node: FrameNode | ComponentNode,
  spec: ComponentSpec,
  styles: StyleIndex,
  receipt: Receipt
): Promise<void> {
  const fill = styles.paintForRole(spec.fillRole);
  if (fill) {
    await node.setFillStyleIdAsync(fill.id);
  } else {
    receipt.skipped.push({ what: `The fill ${spec.fillRole} on ${spec.name}`, why: 'no paint style for that role.' });
  }
  if (spec.strokeRole) {
    const stroke = styles.paintForRole(spec.strokeRole);
    if (stroke) {
      await node.setStrokeStyleIdAsync(stroke.id);
      node.strokeWeight = spec.strokeWeight;
      node.strokeAlign = 'INSIDE';
    } else {
      receipt.skipped.push({
        what: `The border ${spec.strokeRole} on ${spec.name}`,
        why: 'no paint style for that role.',
      });
    }
  }
}

// ---------------------------------------------------------------------------
// Pass 5 — card frames
// ---------------------------------------------------------------------------

async function passCardFrames(plan: Plan, receipt: Receipt, styles: StyleIndex): Promise<void> {
  const page = await ensurePage(PAGE_CARDS, receipt);
  const groups: string[] = [];
  for (const card of plan.cardFrames) if (groups.indexOf(card.group) === -1) groups.push(card.group);

  const nextY: { [group: string]: number } = {};
  for (const group of groups) nextY[group] = 0;

  for (const card of plan.cardFrames) {
    const name = `Card/${card.group}/${card.name}`;
    removeNamed(page, name);

    const frame = figma.createFrame();
    frame.name = name;
    page.appendChild(frame);
    frame.layoutMode = 'VERTICAL';
    frame.primaryAxisSizingMode = 'FIXED';
    frame.counterAxisSizingMode = 'FIXED';
    frame.resizeWithoutConstraints(card.width, card.height);
    frame.paddingLeft = 48;
    frame.paddingRight = 48;
    frame.paddingTop = 48;
    frame.paddingBottom = 48;
    frame.itemSpacing = 12;
    frame.cornerRadius = 14;
    mark(frame);

    const surface = styles.paintForRole('color/surface/base');
    if (surface) await frame.setFillStyleIdAsync(surface.id);
    const edge = styles.paintForRole('color/line/default');
    if (edge) {
      await frame.setStrokeStyleIdAsync(edge.id);
      frame.strokeWeight = 1;
      frame.strokeAlign = 'INSIDE';
    }

    const lines: { text: string; style: string; role: string }[] = [
      { text: card.group, style: 'Latin/Caption', role: 'color/ink/muted' },
      { text: card.name, style: 'Latin/H2', role: 'color/ink/default' },
    ];
    if (card.subtitle) lines.push({ text: card.subtitle, style: 'Latin/Lead', role: 'color/ink/muted' });
    lines.push({ text: card.path, style: 'Mono/Caption', role: 'color/ink/muted' });

    // A card frame carried its Bangla name and subtitle here, and reported in the
    // receipt when the string register held none — so a gap was visible in Figma
    // rather than silently absent. Both went with the Bangla on 27 August 2026.

    for (const line of lines) {
      const text = await makeText(line.text, line.style, line.role, styles, receipt);
      text.layoutAlign = 'STRETCH';
      text.textAutoResize = 'HEIGHT';
      frame.appendChild(text);
    }

    const column = groups.indexOf(card.group);
    frame.x = column * (1280 + 200);
    frame.y = nextY[card.group];
    nextY[card.group] += card.height + 120;
    count(receipt, 'cardFrames', 1);
  }
}

// ---------------------------------------------------------------------------
// Wipe
// ---------------------------------------------------------------------------

async function runWipe(receipt: Receipt): Promise<void> {
  await figma.loadAllPagesAsync();

  for (const page of figma.root.children) {
    const marked = page.findAll(
      (node) => node.getPluginData(PLUGIN_DATA_KEY) === PLUGIN_DATA_VALUE
    );
    // Remove the outermost matches only; removing a parent takes its children.
    for (const node of marked) {
      if (node.removed) continue;
      let ancestorMarked = false;
      let parent = node.parent;
      while (parent && parent.type !== 'PAGE' && parent.type !== 'DOCUMENT') {
        if (parent.getPluginData(PLUGIN_DATA_KEY) === PLUGIN_DATA_VALUE) {
          ancestorMarked = true;
          break;
        }
        parent = parent.parent;
      }
      if (ancestorMarked) continue;
      node.remove();
      count(receipt, 'nodesRemoved', 1);
    }
  }

  const styleGroups: BaseStyle[][] = [
    await figma.getLocalPaintStylesAsync(),
    await figma.getLocalTextStylesAsync(),
    await figma.getLocalEffectStylesAsync(),
    await figma.getLocalGridStylesAsync(),
  ];
  for (const group of styleGroups) {
    for (const style of group) {
      if (style.getPluginData(PLUGIN_DATA_KEY) !== PLUGIN_DATA_VALUE) continue;
      style.remove();
      count(receipt, 'stylesRemoved', 1);
    }
  }

  try {
    for (const variable of await figma.variables.getLocalVariablesAsync()) {
      if (variable.getPluginData(PLUGIN_DATA_KEY) !== PLUGIN_DATA_VALUE) continue;
      variable.remove();
      count(receipt, 'variablesRemoved', 1);
    }
    for (const collection of await figma.variables.getLocalVariableCollectionsAsync()) {
      if (collection.getPluginData(PLUGIN_DATA_KEY) !== PLUGIN_DATA_VALUE) continue;
      collection.remove();
      count(receipt, 'variableCollectionsRemoved', 1);
    }
  } catch (error) {
    receipt.skipped.push({ what: 'Removing variables', why: reason(error) });
  }

  // Pages last, and only if this plugin made them and they are now empty.
  for (const page of figma.root.children.slice()) {
    if (page.getPluginData(PLUGIN_DATA_KEY) !== PLUGIN_DATA_VALUE) continue;
    if (page.children.length > 0) {
      receipt.skipped.push({
        what: `The page "${page.name}"`,
        why: `it still holds ${page.children.length} item(s) this plugin did not make, so it was left alone.`,
      });
      continue;
    }
    if (figma.root.children.length === 1) {
      receipt.skipped.push({
        what: `The page "${page.name}"`,
        why: 'it is the only page in the file, and Figma will not let a file have none.',
      });
      continue;
    }
    page.remove();
    count(receipt, 'pagesRemoved', 1);
  }
}

// ---------------------------------------------------------------------------
// Build
// ---------------------------------------------------------------------------

async function runBuild(plan: Plan, receipt: Receipt): Promise<void> {
  progress('Probing what this file allows…');
  const probe = await runProbe(plan);
  receipt.probe = probe;

  if (!probe.fonts.ok) {
    receipt.stopped =
      `Stopped before making anything. These fonts are not installed: ${probe.fonts.missing.join(', ')}. ` +
      'Install them, restart Figma, and run this again.';
    return;
  }

  for (const font of plan.fontsRequired) {
    await figma.loadFontAsync({ family: font.family, style: font.style });
  }

  receipt.mode = probe.variables.ok ? 'variables' : 'styles-only';
  if (!probe.variables.ok) {
    receipt.skipped.push({
      what: 'The Primitives and Theme variable collections, and every variable in them',
      why:
        `createVariableCollection failed in this file: ${probe.variables.reason}. The plugin carried on in ` +
        'styles-only mode, where each of the four themes becomes its own set of plain paint styles.',
    });
  }

  let index: VariableIndex | null = null;
  if (probe.variables.ok) {
    progress('Making variable collections…');
    index = await passVariables(plan, receipt, probe.variableModes.limit);
  }

  progress('Making paint styles…');
  const paint = await passPaintStyles(plan, receipt, index);
  progress('Making text styles…');
  const text = await passTextStyles(plan, receipt, index);
  progress('Making effect styles…');
  const effect = await passEffectStyles(plan, receipt, index);
  progress('Making grid styles…');
  const grid = await passGridStyles(plan, receipt, index);

  const styles: StyleIndex = {
    paint,
    text,
    effect,
    grid,
    paintForRole: (role: string): PaintStyle | null => {
      const direct = paint[`Theme/${prettyRole(role)}`];
      if (direct) return direct;
      const light = paint[`Light/${prettyRole(role)}`];
      return light || null;
    },
  };

  progress('Drawing the marks…');
  await passMarks(plan, receipt, probe);
  progress('Building the components…');
  await passComponents(plan, receipt, styles, probe);
  progress('Laying out the 30 card frames…');
  await passCardFrames(plan, receipt, styles);
}

// ---------------------------------------------------------------------------
// Entry
// ---------------------------------------------------------------------------

function parseOverride(text: string): { input: RawInput; label: string } {
  const parsed = JSON.parse(text);
  const need = ['primitive', 'semantic'];
  for (const key of need) {
    if (!parsed[key]) throw new Error(`the pasted JSON has no "${key}" key`);
  }
  for (const mode of THEME_MODES) {
    if (!parsed.semantic[mode.key]) {
      throw new Error(`the pasted JSON has no semantic."${mode.key}" theme`);
    }
  }
  const input: RawInput = {
    primitive: parsed.primitive,
    semantic: parsed.semantic,
    forcedColors: parsed.forcedColors || BUNDLED.forcedColors,
    marks: parsed.marks || BUNDLED.marks,
    markManifest: parsed.markManifest || BUNDLED.markManifest,
    cards: parsed.cards || BUNDLED.cards,
  };
  return { input, label: 'pasted into the plugin by hand' };
}

async function main(): Promise<void> {
  figma.showUI(__html__, { width: 560, height: 680, themeColors: true });

  const command = figma.command || 'build';
  let plan: Plan;
  try {
    plan = buildPlan(BUNDLED);
  } catch (error) {
    figma.ui.postMessage({ type: 'fatal', message: reason(error) });
    return;
  }

  figma.ui.postMessage({
    type: 'ready',
    command,
    sha: BUNDLE_SHA256,
    expected: plan.totals,
    fonts: plan.fontsRequired.map((f) => `${f.family} ${f.style}`),
  });

  figma.ui.onmessage = async (message: { type: string; command?: string; tokens?: string }) => {
    if (message.type === 'close') {
      figma.closePlugin();
      return;
    }
    if (message.type !== 'run') return;

    const chosen = message.command || command;
    let activePlan = plan;
    let source = 'compiled into the plugin at build time';

    if (message.tokens && message.tokens.trim().length > 0) {
      try {
        const override = parseOverride(message.tokens);
        activePlan = buildPlan(override.input);
        source = override.label;
      } catch (error) {
        figma.ui.postMessage({
          type: 'fatal',
          message: `The pasted tokens could not be used: ${reason(error)}`,
        });
        return;
      }
    }

    const receipt = emptyReceipt(chosen, BUNDLE_SHA256, source);
    receipt.decisions = activePlan.decisions;
    receipt.knownGaps = activePlan.knownGaps;

    try {
      if (chosen === 'probe') {
        progress('Probing…');
        receipt.probe = await runProbe(activePlan);
        receipt.mode = receipt.probe.variables.ok ? 'variables' : 'styles-only';
        receipt.stopped = 'Probe only. Nothing was made and nothing was changed.';
      } else if (chosen === 'wipe') {
        progress('Removing everything this plugin made…');
        await runWipe(receipt);
        receipt.mode = 'not run';
      } else {
        await runBuild(activePlan, receipt);
      }
    } catch (error) {
      receipt.stopped = `The run stopped with an error: ${reason(error)}`;
    }

    figma.ui.postMessage({
      type: 'receipt',
      receipt,
      expected: activePlan.totals,
    });
  };
}

void main();
