// Aninda Studio — the build plan.
//
// This file turns the DTCG token files, the marks and the card registry into a
// flat list of everything the plugin will make. It touches no Figma API, so the
// same code runs twice: once in Node, to write RECEIPT-EXPECTED.json, and once
// inside Figma, to do the work. "Did it work" is then a comparison of two
// numbers produced by one piece of code, not two.
//
// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader

/* eslint-disable @typescript-eslint/no-explicit-any */

export const ROOT_FONT_PX = 16;

export type Json = any;

export interface RawInput {
  primitive: Json;
  semantic: { light: Json; dark: Json; 'hc-light': Json; 'hc-dark': Json };
  forcedColors: Json;
  marks: { name: string; file: string; svg: string }[];
  markManifest: Json;
  cards: Json;
}

export type VarValue =
  | { kind: 'color'; r: number; g: number; b: number; a: number }
  | { kind: 'float'; value: number }
  | { kind: 'string'; value: string }
  | { kind: 'easing'; x1: number; y1: number; x2: number; y2: number }
  | { kind: 'alias'; collection: string; variable: string };

export type FigmaVarType = 'COLOR' | 'FLOAT' | 'STRING' | 'BOOLEAN' | 'EASING';

export interface VarSpec {
  name: string;
  resolvedType: FigmaVarType;
  description: string;
  values: { [modeLabel: string]: VarValue };
}

export interface CollectionSpec {
  name: string;
  modes: string[];
  variables: VarSpec[];
}

export interface PaintStyleSpec {
  name: string;
  description: string;
  bindTo: { collection: string; variable: string };
}

export interface TextStyleSpec {
  name: string;
  description: string;
  family: string;
  style: string;
  fontSize: number;
  lineHeightPercent: number | null; // null means Figma's automatic line height
  bindFontSize: string | null; // a Primitives variable name
  bindFontFamily: string | null;
}

export interface EffectStyleSpec {
  name: string;
  description: string;
  radius: number;
  spread: number;
  bindColor: { collection: string; variable: string } | null;
  bindSpread: string | null;
}

export interface GridStyleSpec {
  name: string;
  description: string;
  grids: {
    pattern: 'COLUMNS' | 'ROWS' | 'GRID';
    alignment?: 'MIN' | 'MAX' | 'STRETCH' | 'CENTER';
    count?: number;
    gutterSize?: number;
    offset?: number;
    sectionSize?: number;
  }[];
  bindGutter: string | null;
  bindOffset: string | null;
}

export interface MarkSpec {
  name: string;
  file: string;
  svg: string;
}

export interface MarkSetSpec {
  name: string;
  property: string;
  variants: { value: string; file: string; svg: string }[];
}

export interface ComponentLine {
  text: string;
  textStyle: string;
  colourRole: string;
  source: string;
}

export interface ComponentSpec {
  set: string | null;
  name: string;
  kind: 'button' | 'input' | 'badge' | 'card';
  variantProps: { [property: string]: string };
  width: number;
  height: number;
  paddingX: number;
  paddingY: number;
  cornerRadius: number;
  fillRole: string;
  strokeRole: string | null;
  strokeWeight: number;
  focusRing: boolean;
  lines: ComponentLine[];
}

export interface CardFrameSpec {
  name: string;
  nameBangla: string;
  group: string;
  subtitle: string;
  subtitleBangla: string;
  width: number;
  height: number;
  path: string;
}

export interface Gap {
  what: string;
  why: string;
}

export interface Plan {
  fontsRequired: { family: string; style: string; usedFor: string }[];
  collections: CollectionSpec[];
  paintStyles: PaintStyleSpec[];
  textStyles: TextStyleSpec[];
  effectStyles: EffectStyleSpec[];
  gridStyles: GridStyleSpec[];
  marks: MarkSpec[];
  markSet: MarkSetSpec;
  components: ComponentSpec[];
  componentSets: string[];
  cardFrames: CardFrameSpec[];
  pages: string[];
  decisions: Gap[];
  knownGaps: Gap[];
  totals: { [key: string]: number };
}

export const THEME_MODES: { key: 'light' | 'dark' | 'hc-light' | 'hc-dark'; label: string }[] = [
  { key: 'light', label: 'Light' },
  { key: 'dark', label: 'Dark' },
  { key: 'hc-light', label: 'High contrast light' },
  { key: 'hc-dark', label: 'High contrast dark' },
];

export const PAGE_MARKS = 'Aninda Studio · Marks';
export const PAGE_COMPONENTS = 'Aninda Studio · Components';
export const PAGE_CARDS = 'Aninda Studio · Cards';

export const PLUGIN_DATA_KEY = 'as-built';
export const PLUGIN_DATA_VALUE = '1';

// ---------------------------------------------------------------------------
// DTCG walking
// ---------------------------------------------------------------------------

interface Leaf {
  path: string[];
  type: string;
  value: Json;
  description: string;
}

/** Walk a DTCG document, carrying group-level $type down to each leaf. */
export function walkTokens(doc: Json): Leaf[] {
  const out: Leaf[] = [];
  const visit = (node: Json, path: string[], inheritedType: string): void => {
    if (node === null || typeof node !== 'object' || Array.isArray(node)) return;
    const type: string = typeof node.$type === 'string' ? node.$type : inheritedType;
    if (Object.prototype.hasOwnProperty.call(node, '$value')) {
      out.push({
        path,
        type,
        value: node.$value,
        description: typeof node.$description === 'string' ? node.$description : '',
      });
      return;
    }
    for (const key of Object.keys(node)) {
      if (key.charAt(0) === '$') continue;
      visit(node[key], path.concat([key]), type);
    }
  };
  visit(doc, [], '');
  return out;
}

/** "{color.ramp.ground.950}" -> "color/ramp/ground/950". Returns null if not an alias. */
export function aliasTarget(value: Json): string | null {
  if (typeof value !== 'string') return null;
  const trimmed = value.trim();
  if (trimmed.length < 3 || trimmed.charAt(0) !== '{' || trimmed.charAt(trimmed.length - 1) !== '}') {
    return null;
  }
  return trimmed.slice(1, -1).split('.').join('/');
}

function toRgb(value: Json): { r: number; g: number; b: number; a: number } {
  const c = value && value.components;
  if (!Array.isArray(c) || c.length < 3) {
    throw new Error('a colour token has no three-part components array');
  }
  const alpha = typeof value.alpha === 'number' ? value.alpha : 1;
  return { r: Number(c[0]), g: Number(c[1]), b: Number(c[2]), a: alpha };
}

function round(n: number, places: number): number {
  const f = Math.pow(10, places);
  return Math.round(n * f) / f;
}

/** A dimension token in px. rem is converted at a 16 px root and the note says so. */
function dimensionPx(value: Json): { px: number; note: string } {
  const raw = Number(value.value);
  const unit = String(value.unit);
  if (unit === 'rem') {
    const px = round(raw * ROOT_FONT_PX, 4);
    return { px, note: `${raw} rem, which is ${px} px at a ${ROOT_FONT_PX} px root` };
  }
  return { px: raw, note: `${raw} ${unit}` };
}

// ---------------------------------------------------------------------------
// The plan
// ---------------------------------------------------------------------------

export function buildPlan(input: RawInput): Plan {
  const decisions: Gap[] = [];
  const knownGaps: Gap[] = [];

  // --- Primitives -----------------------------------------------------------
  const primitiveLeaves = walkTokens(input.primitive);
  const primitiveVars: VarSpec[] = [];
  const primitivePx: { [name: string]: number } = {};
  const primitiveNumber: { [name: string]: number } = {};

  for (const leaf of primitiveLeaves) {
    const name = leaf.path.join('/');
    const description = leaf.description;
    if (leaf.type === 'color') {
      const rgb = toRgb(leaf.value);
      primitiveVars.push({
        name,
        resolvedType: 'COLOR',
        description: description || `${leaf.value.hex} in sRGB.`,
        values: { Value: { kind: 'color', ...rgb } },
      });
    } else if (leaf.type === 'dimension') {
      const { px, note } = dimensionPx(leaf.value);
      primitivePx[name] = px;
      primitiveVars.push({
        name,
        resolvedType: 'FLOAT',
        description: description ? `${description} Source value: ${note}.` : `Source value: ${note}.`,
        values: { Value: { kind: 'float', value: px } },
      });
    } else if (leaf.type === 'number') {
      primitiveNumber[name] = Number(leaf.value);
      primitiveVars.push({
        name,
        resolvedType: 'FLOAT',
        description,
        values: { Value: { kind: 'float', value: Number(leaf.value) } },
      });
    } else if (leaf.type === 'fontFamily') {
      const stack: string[] = Array.isArray(leaf.value) ? leaf.value.map(String) : [String(leaf.value)];
      primitiveVars.push({
        name,
        resolvedType: 'STRING',
        description:
          (description ? description + ' ' : '') +
          `Figma holds one family name, so this is the first in the stack. The full stack is: ${stack.join(', ')}.`,
        values: { Value: { kind: 'string', value: stack[0] } },
      });
    } else if (leaf.type === 'duration') {
      primitiveVars.push({
        name,
        resolvedType: 'FLOAT',
        description: (description ? description + ' ' : '') + `Milliseconds.`,
        values: { Value: { kind: 'float', value: Number(leaf.value.value) } },
      });
    } else if (leaf.type === 'cubicBezier') {
      const b: number[] = leaf.value.map(Number);
      primitiveVars.push({
        name,
        resolvedType: 'EASING',
        description:
          (description ? description + ' ' : '') +
          `cubic-bezier(${b[0]}, ${b[1]}, ${b[2]}, ${b[3]}).`,
        values: { Value: { kind: 'easing', x1: b[0], y1: b[1], x2: b[2], y2: b[3] } },
      });
    } else {
      knownGaps.push({
        what: `Primitive token ${name}`,
        why: `its DTCG $type is "${leaf.type}", and Figma has no variable type that carries it.`,
      });
    }
  }

  // --- Theme ----------------------------------------------------------------
  const themeVars: VarSpec[] = [];
  const semanticPaths: string[] = walkTokens(input.semantic.light).map((leaf) => leaf.path.join('/'));

  for (const path of semanticPaths) {
    const values: { [mode: string]: VarValue } = {};
    let description = '';
    for (const mode of THEME_MODES) {
      const doc = input.semantic[mode.key];
      const leaf = walkTokens(doc).filter((l) => l.path.join('/') === path)[0];
      if (!leaf) {
        throw new Error(
          `the ${mode.key} theme has no token at ${path}. The four themes must hold identical token paths.`
        );
      }
      if (!description) description = leaf.description;
      const target = aliasTarget(leaf.value);
      if (target !== null) {
        values[mode.label] = { kind: 'alias', collection: 'Primitives', variable: target };
      } else {
        values[mode.label] = { kind: 'color', ...toRgb(leaf.value) };
      }
    }
    themeVars.push({
      name: path,
      resolvedType: 'COLOR',
      description:
        description ||
        'One of the semantic colour roles. Each mode holds the value measured for that theme.',
      values,
    });
  }

  const collections: CollectionSpec[] = [
    { name: 'Primitives', modes: ['Value'], variables: primitiveVars },
    { name: 'Theme', modes: THEME_MODES.map((m) => m.label), variables: themeVars },
  ];

  // --- Paint styles ---------------------------------------------------------
  const paintStyles: PaintStyleSpec[] = semanticPaths.map((path) => {
    const parts = path.split('/');
    const pretty = parts
      .slice(1)
      .map((p) => p.charAt(0).toUpperCase() + p.slice(1))
      .join('/');
    return {
      name: `Theme/${pretty}`,
      description: `Bound to the Theme variable ${path}, so it follows whichever of the four modes the frame is set to.`,
      bindTo: { collection: 'Theme', variable: path },
    };
  });

  decisions.push({
    what: 'No paint style was made for the 66 primitive ramp steps.',
    why:
      'They exist as variables in the Primitives collection. A designer should reach for a role such as ' +
      'Theme/Ink/Default, which follows the theme, rather than for a fixed ramp step, which does not.',
  });

  // --- Text styles ----------------------------------------------------------
  const banglaMin = primitivePx['dimension/type/bangla-min'];
  const banglaBumpBelow = primitivePx['dimension/type/bangla-weight-bump-below'];
  const banglaLineHeight = primitiveNumber['number/lineHeight/bangla'];

  const steps: { key: string; label: string; banglaScaleKey: string }[] = [
    { key: 'display', label: 'Display', banglaScaleKey: 'display' },
    { key: 'h1', label: 'H1', banglaScaleKey: 'title' },
    { key: 'h2', label: 'H2', banglaScaleKey: 'title' },
    { key: 'h3', label: 'H3', banglaScaleKey: 'heading' },
    { key: 'lead', label: 'Lead', banglaScaleKey: 'heading' },
    { key: 'body', label: 'Body', banglaScaleKey: 'body' },
    { key: 'caption', label: 'Caption', banglaScaleKey: 'caption' },
  ];

  const textStyles: TextStyleSpec[] = [];
  const fontsRequired: { family: string; style: string; usedFor: string }[] = [];
  const needFont = (family: string, style: string, usedFor: string): void => {
    for (const f of fontsRequired) if (f.family === family && f.style === style) return;
    fontsRequired.push({ family, style, usedFor });
  };

  for (const step of steps) {
    const varName = `dimension/type/${step.key}`;
    const px = primitivePx[varName];
    if (typeof px !== 'number') {
      knownGaps.push({
        what: `Text style Latin/${step.label}`,
        why: `there is no primitive dimension token at ${varName}.`,
      });
      continue;
    }
    needFont('Literata', 'Regular', 'every Latin text style');
    textStyles.push({
      name: `Latin/${step.label}`,
      description: `${px} px, from ${varName}. Line height is left on Figma's automatic setting, because the token set defines a line height for Bangla only.`,
      family: 'Literata',
      style: 'Regular',
      fontSize: px,
      lineHeightPercent: null,
      bindFontSize: varName,
      bindFontFamily: 'fontFamily/latin',
    });
  }

  for (const step of steps) {
    const latinPx = primitivePx[`dimension/type/${step.key}`];
    if (typeof latinPx !== 'number') continue;
    const scale = primitiveNumber[`number/scale/bangla/${step.banglaScaleKey}`];
    const raw = round(latinPx * scale, 4);
    const clamped = raw < banglaMin;
    const size = clamped ? banglaMin : raw;
    const heavier = size < banglaBumpBelow;
    const style = heavier ? 'Medium' : 'Regular';
    needFont('Noto Serif Bengali', style, 'Bangla text styles');
    const notes: string[] = [
      `${latinPx} px Latin times the measured Bangla multiplier ${scale} gives ${raw} px.`,
    ];
    if (clamped) notes.push(`That is below the ${banglaMin} px Bangla floor, so it is held at ${banglaMin} px.`);
    if (heavier) {
      notes.push(
        `Below ${banglaBumpBelow} px the Bangla is set one weight heavier, so this style is Medium rather than Regular.`
      );
    }
    notes.push(`Line height ${banglaLineHeight}, from number/lineHeight/bangla.`);
    textStyles.push({
      name: `Bangla/${step.label}`,
      description: notes.join(' '),
      family: 'Noto Serif Bengali',
      style,
      fontSize: size,
      lineHeightPercent: round(banglaLineHeight * 100, 2),
      bindFontSize: clamped ? 'dimension/type/bangla-min' : null,
      bindFontFamily: 'fontFamily/bangla',
    });
  }

  for (const step of [
    { key: 'body', label: 'Body' },
    { key: 'caption', label: 'Caption' },
  ]) {
    const varName = `dimension/type/${step.key}`;
    const px = primitivePx[varName];
    if (typeof px !== 'number') continue;
    needFont('Aninda Mono', 'Regular', 'the two monospaced text styles');
    textStyles.push({
      name: `Mono/${step.label}`,
      description: `${px} px, from ${varName}. Aninda Mono is the renamed IBM Plex Mono subset; Plex is a Reserved Font Name under the SIL Open Font License 1.1, so a subset has to be renamed.`,
      family: 'Aninda Mono',
      style: 'Regular',
      fontSize: px,
      lineHeightPercent: null,
      bindFontSize: varName,
      bindFontFamily: 'fontFamily/mono',
    });
  }

  knownGaps.push({
    what: 'Latin and monospaced text styles carry no line height.',
    why:
      'The token set defines number/lineHeight/bangla and nothing for Latin. Figma’s automatic line height ' +
      'is used rather than a number I would have had to invent.',
  });

  // --- Effect styles --------------------------------------------------------
  const ringWidth = primitivePx['dimension/focus/ring-width'];
  const effectStyles: EffectStyleSpec[] = [
    {
      name: 'Focus/Ring',
      description: `A ${ringWidth} px ring drawn as a shadow with no blur and no offset, spread ${ringWidth} px, coloured by the Theme variable color/focus/ring. Figma has no outline effect, so a zero-blur shadow is how a ring is expressed.`,
      radius: 0,
      spread: ringWidth,
      bindColor: { collection: 'Theme', variable: 'color/focus/ring' },
      bindSpread: 'dimension/focus/ring-width',
    },
  ];

  decisions.push({
    what: 'No elevation or shadow effect styles were made.',
    why:
      'The token set has no shadow or elevation token. Inventing blur radii and opacities here would put ' +
      'numbers in the library that the system never agreed to.',
  });

  // --- Grid styles ----------------------------------------------------------
  const gridStyles: GridStyleSpec[] = [
    {
      name: 'Layout/12 column',
      description: `Twelve stretched columns, gutter ${primitivePx['dimension/space/4']} px from dimension/space/4, margin ${primitivePx['dimension/space/5']} px from dimension/space/5.`,
      grids: [
        {
          pattern: 'COLUMNS',
          alignment: 'STRETCH',
          count: 12,
          gutterSize: primitivePx['dimension/space/4'],
          offset: primitivePx['dimension/space/5'],
        },
      ],
      bindGutter: 'dimension/space/4',
      bindOffset: 'dimension/space/5',
    },
    {
      name: 'Layout/8 px baseline',
      description: `An ${primitivePx['dimension/space/1']} px square grid, from dimension/space/1. Every spacing step in the system is a multiple of it.`,
      grids: [{ pattern: 'GRID', sectionSize: primitivePx['dimension/space/1'] }],
      bindGutter: null,
      bindOffset: null,
    },
  ];

  // --- Marks ----------------------------------------------------------------
  const marks: MarkSpec[] = input.marks.map((m) => ({ name: m.name, file: m.file, svg: m.svg }));
  const byFile = (file: string): string => {
    for (const m of input.marks) if (m.file === file) return m.svg;
    throw new Error(`the mark ${file} is missing from the bundled set`);
  };
  const markSet: MarkSetSpec = {
    name: 'Mark',
    property: 'Weight',
    variants: [
      { value: 'Regular', file: 'mark-regular.svg', svg: byFile('mark-regular.svg') },
      { value: 'Heavy', file: 'mark-heavy.svg', svg: byFile('mark-heavy.svg') },
    ],
  };

  // --- Components -----------------------------------------------------------
  const controlRadius = primitivePx['dimension/radius/control'];
  const badgeRadius = primitivePx['dimension/radius/badge'];
  const cardRadius = primitivePx['dimension/radius/card'];
  const comfortable = primitivePx['dimension/target/comfortable'];
  const space2 = primitivePx['dimension/space/2'];
  const space3 = primitivePx['dimension/space/3'];
  const space4 = primitivePx['dimension/space/4'];
  const space5 = primitivePx['dimension/space/5'];

  const components: ComponentSpec[] = [];

  const buttonVariants: { tone: string; script: string; label: string; role: string; source: string }[] = [
    {
      tone: 'Accent',
      script: 'Latin',
      label: 'Save the entry',
      role: 'color/accent/default',
      source: 'ENGLISH-STANDARD.md, the interface-text rule that a button is a verb with its object',
    },
    {
      tone: 'Accent',
      script: 'Bangla',
      label: 'লেখাটি সংরক্ষণ করুন',
      role: 'color/accent/default',
      source: 'BANGLA-STANDARD.md, verified string bt-1',
    },
    {
      tone: 'Danger',
      script: 'Latin',
      label: 'Delete the file',
      role: 'color/status/danger',
      source: 'the plain-English pair of the verified Bangla string bt-3',
    },
    {
      tone: 'Danger',
      script: 'Bangla',
      label:
        'ফাইলটি মুছে ফেলুন',
      role: 'color/status/danger',
      source: 'BANGLA-STANDARD.md, verified string bt-3',
    },
  ];

  for (const v of buttonVariants) {
    components.push({
      set: 'Button',
      name: `Tone=${v.tone}, Script=${v.script}`,
      kind: 'button',
      variantProps: { Tone: v.tone, Script: v.script },
      width: 0,
      height: comfortable,
      paddingX: space4,
      paddingY: space2,
      cornerRadius: controlRadius,
      fillRole: v.role,
      strokeRole: v.role,
      strokeWeight: 1,
      focusRing: false,
      lines: [
        {
          text: v.label,
          textStyle: v.script === 'Bangla' ? 'Bangla/Body' : 'Latin/Body',
          colourRole: 'color/accent/on',
          source: v.source,
        },
      ],
    });
  }

  decisions.push({
    what: 'Buttons are filled, and were outlined until 26 August 2026.',
    why:
      'The reason they were outlined was that the semantic roles included no "on accent" text colour, so the ' +
      'label on a filled button was not defined anywhere in the system. That role now exists. color/accent/on is ' +
      'surface.lowest, measured as ink against every fill that carries it — accent, accent-hover and danger — with ' +
      'the worst of those published rather than the flattering one. So a filled button now uses only roles that ' +
      'were measured, which is what the outlined one was standing in for, and it matches what components.css ships.',
  });
  decisions.push({
    what: 'Component borders are 1 px.',
    why: 'The token set has no border-width token. 1 px is stated here rather than hidden in the drawing code.',
  });

  for (const state of ['Default', 'Focus']) {
    components.push({
      set: 'Input',
      name: `State=${state}`,
      kind: 'input',
      variantProps: { State: state },
      width: 320,
      height: comfortable,
      paddingX: space3,
      paddingY: space2,
      cornerRadius: controlRadius,
      fillRole: 'color/surface/bright',
      strokeRole: state === 'Focus' ? 'color/focus/ring' : 'color/line/default',
      strokeWeight: 1,
      focusRing: state === 'Focus',
      lines: [
        {
          text: 'Name',
          textStyle: 'Latin/Caption',
          colourRole: 'color/ink/muted',
          source: 'BANGLA-STANDARD.md verified string gb-2 (নাম), in its English pair',
        },
        {
          text: 'নাম',
          textStyle: 'Bangla/Body',
          colourRole: 'color/ink/default',
          source: 'BANGLA-STANDARD.md, verified string gb-2',
        },
      ],
    });
  }

  const badgeStatuses: { name: string; role: string }[] = [
    { name: 'Success', role: 'color/status/success' },
    { name: 'Warning', role: 'color/status/warning' },
    { name: 'Danger', role: 'color/status/danger' },
    { name: 'Information', role: 'color/status/info' },
  ];
  for (const s of badgeStatuses) {
    components.push({
      set: 'Badge',
      name: `Status=${s.name}`,
      kind: 'badge',
      variantProps: { Status: s.name },
      width: 0,
      height: 0,
      paddingX: space2,
      paddingY: primitivePx['dimension/space/0'],
      cornerRadius: badgeRadius,
      fillRole: 'color/surface/high',
      strokeRole: s.role,
      strokeWeight: 1,
      focusRing: false,
      lines: [
        {
          text: s.name,
          textStyle: 'Latin/Caption',
          colourRole: s.role,
          source: 'the name of the semantic role itself, not interface copy',
        },
      ],
    });
  }

  decisions.push({
    what: 'Every badge carries a word, never colour alone.',
    why:
      'In forced-colors mode all four status colours resolve to CanvasText, so a badge that carried only a ' +
      'colour would carry nothing. forced-colors.map.json states this as a rule.',
  });

  components.push({
    set: null,
    name: 'Card',
    kind: 'card',
    variantProps: {},
    width: 480,
    height: 0,
    paddingX: space5,
    paddingY: space5,
    cornerRadius: cardRadius,
    fillRole: 'color/surface/high',
    strokeRole: 'color/line/default',
    strokeWeight: 1,
    focusRing: false,
    lines: [
      {
        text: 'Card',
        textStyle: 'Latin/H3',
        colourRole: 'color/ink/default',
        source: 'the component name',
      },
      {
        text: 'A surface one step above the page, with the card radius and a hairline edge.',
        textStyle: 'Latin/Body',
        colourRole: 'color/ink/muted',
        source: 'written for this library, to the English standard',
      },
    ],
  });

  const componentSets: string[] = [];
  for (const c of components) {
    if (c.set !== null && componentSets.indexOf(c.set) === -1) componentSets.push(c.set);
  }

  // --- Card frames ----------------------------------------------------------
  const cardsRegistry: Json[] = input.cards && Array.isArray(input.cards.cards) ? input.cards.cards : [];
  const cardFrames: CardFrameSpec[] = cardsRegistry.map((c: Json) => ({
    name: String(c.name),
    nameBangla: typeof c.name_bn === 'string' ? c.name_bn : '',
    group: String(c.group),
    subtitle: typeof c.subtitle === 'string' ? c.subtitle : '',
    subtitleBangla: typeof c.subtitle_bn === 'string' ? c.subtitle_bn : '',
    width: Number(c.width),
    height: Number(c.height),
    path: String(c.path),
  }));

  const missingBanglaName = cardFrames.filter((c) => c.nameBangla === '').length;
  const missingBanglaSubtitle = cardFrames.filter((c) => c.subtitleBangla === '').length;
  if (missingBanglaName > 0 || missingBanglaSubtitle > 0) {
    knownGaps.push({
      what: `${missingBanglaName} card frames carry no Bangla name and ${missingBanglaSubtitle} carry no Bangla subtitle.`,
      why:
        'BANGLA-STANDARD.md holds a verified string for each of the others and none for these. Writing new Bangla ' +
        'to fill the space is not allowed, so those frames stay English-only and are counted here instead.',
    });
  }

  const totals = {
    collections: collections.length,
    variables: primitiveVars.length + themeVars.length,
    primitiveVariables: primitiveVars.length,
    themeVariables: themeVars.length,
    themeModes: THEME_MODES.length,
    variableAliases: themeVars.reduce(
      (sum, v) =>
        sum +
        Object.keys(v.values).filter((mode) => v.values[mode].kind === 'alias').length,
      0
    ),
    paintStyles: paintStyles.length,
    textStyles: textStyles.length,
    effectStyles: effectStyles.length,
    gridStyles: gridStyles.length,
    marks: marks.length,
    markSetVariants: markSet.variants.length,
    components: components.length,
    componentSets: componentSets.length,
    cardFrames: cardFrames.length,
    pages: 3,
  };

  return {
    fontsRequired,
    collections,
    paintStyles,
    textStyles,
    effectStyles,
    gridStyles,
    marks,
    markSet,
    components,
    componentSets,
    cardFrames,
    pages: [PAGE_MARKS, PAGE_COMPONENTS, PAGE_CARDS],
    decisions,
    knownGaps,
    totals,
  };
}
