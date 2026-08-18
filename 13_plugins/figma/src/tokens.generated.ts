// GENERATED FILE. Do not hand-edit — run "node build.mjs" instead.
//
// Every token, mark and card in the Aninda Studio system, compiled in at build
// time so the plugin works with no network connection at all. The manifest
// declares networkAccess "none", and this is how that promise is kept.
//
// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader

import type { RawInput } from './plan';

export const BUNDLE_SHA256 = "f210bd649b4e2af31378d8f61ed403907469b6e286e896566e32e7500415417b";

export const SOURCE_HASHES: { [file: string]: string } = {
  "07_tokens/build/primitive.tokens.json": "359b6b214801145054bd3154b51247b2cc3fbf1983f54664b959b30802aaf43f",
  "07_tokens/build/semantic.light.tokens.json": "bcf15346d37fa2566444a2e104355b8d63193219083be5e248e42c62ecddd3f7",
  "07_tokens/build/semantic.dark.tokens.json": "2e76f39e6583772b465e4e346a4fc4682d60f91014bfd22e5bc88179e383159f",
  "07_tokens/build/semantic.hc-light.tokens.json": "46ccb577f108f8d2e4d50e05325ae669ea0fdd2da8304ae11c1b11a1ab6022a2",
  "07_tokens/build/semantic.hc-dark.tokens.json": "92c7347bb61a429b47786e652d0b3e4582fa56ad26dc740d2cd6c00042037ad2",
  "07_tokens/build/forced-colors.map.json": "58560c18bc09567071160cfea947402ab7f1ad44a9eb128c0ce6d6ae0e10f641",
  "04_mark/svg/icon-1024.svg": "9ff31c7bfa022fdd1cfbcf6782320b84d83422ddd617f97a8ab41248409407bd",
  "04_mark/svg/icon-1088-watch.svg": "f0dd4c249a78419af2855f90344cb05d1335444194c1ac9059e1b81c5b6bd6cb",
  "04_mark/svg/icon-192.svg": "58b7f359ff0841f399214b16ec5790932106dc66854b6c87c7dee88dc20eadb7",
  "04_mark/svg/icon-512.svg": "3b00945f46b41e8017622d73e3eafb49c63209f2a2e8ac9342b91fd0de5caac1",
  "04_mark/svg/icon-appstore-square-1024.svg": "a7d60253c14a9f9b7e494fa9aa4182a732bd507f3800e1677afea829a5e93a3c",
  "04_mark/svg/mark-heavy.svg": "43544b56cd14e0d65fdb63a68d0e2113ae4428f1bdf73cdc4b4016d0f7423fbc",
  "04_mark/svg/mark-regular.svg": "dae564226af690e7dd0a00d14a4a56c80535ec2a8284b7c8b9cd181082220787",
  "04_mark/svg/tile-web.svg": "b631c922ebb4287e9d227fd4303864e7373dbf38467ca086fbde9cbee573600b",
  "04_mark/svg/wordmark-bangla.svg": "6b42edde179882a29c3147a78e333ef3e341fbd16913ec8fd70519599d8b464d",
  "04_mark/svg/wordmark-latin.svg": "975775a95ca4d09341cd38a165006ab092581cffdeaab533f61934a4206893af",
  "04_mark/manifest.json": "440d2eafd5c5ebb6d66d3a5aae0a5e170dc2b9a88ebacc697ced0bc8a877f4ad",
  "08_components/_cards.json": "bd177c1e4882eaa9df2c6a6bc1d3807563914b0c7c463c9fdd3fd8915ee08421"
};

export const BUNDLED: RawInput = {
  primitive: {
  "$schema": "https://tr.designtokens.org/format/",
  "$description": "Aninda Studio primitive tokens. Generated — do not hand-edit. Colour ramps are computed in OKLCH and gamut-mapped into sRGB; every value is the rounded 8-bit hex a browser will actually produce.",
  "$extensions": {
    "studio.aninda": {
      "direction": "estuary",
      "generatedBy": "07_tokens/build.py",
      "spec": "DTCG 2025.10 (Final Community Group Report, 28 October 2025) — a W3C Community Group specification, NOT a W3C Standard"
    }
  },
  "color": {
    "$type": "color",
    "ramp": {
      "ground": {
        "50": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.94902,
              0.976471,
              0.968627
            ],
            "hex": "#F2F9F7"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 50,
              "luminance": 0.933438,
              "isAnchor": false
            }
          }
        },
        "100": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.890196,
              0.941176,
              0.92549
            ],
            "hex": "#E3F0EC"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 100,
              "luminance": 0.847068,
              "isAnchor": false
            }
          }
        },
        "200": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.784314,
              0.882353,
              0.854902
            ],
            "hex": "#C8E1DA"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 200,
              "luminance": 0.711911,
              "isAnchor": false
            }
          }
        },
        "300": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.666667,
              0.807843,
              0.768627
            ],
            "hex": "#AACEC4"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 300,
              "luminance": 0.566734,
              "isAnchor": false
            }
          }
        },
        "400": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.545098,
              0.709804,
              0.666667
            ],
            "hex": "#8BB5AA"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 400,
              "luminance": 0.414382,
              "isAnchor": false
            }
          }
        },
        "500": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.435294,
              0.607843,
              0.564706
            ],
            "hex": "#6F9B90"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 500,
              "luminance": 0.288352,
              "isAnchor": false
            }
          }
        },
        "600": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.341176,
              0.501961,
              0.462745
            ],
            "hex": "#578076"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 600,
              "luminance": 0.187721,
              "isAnchor": false
            }
          }
        },
        "700": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.254902,
              0.396078,
              0.360784
            ],
            "hex": "#41655C"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 700,
              "luminance": 0.112036,
              "isAnchor": false
            }
          }
        },
        "800": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.180392,
              0.294118,
              0.262745
            ],
            "hex": "#2E4B43"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 800,
              "luminance": 0.060181,
              "isAnchor": false
            }
          }
        },
        "900": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.105882,
              0.184314,
              0.164706
            ],
            "hex": "#1B2F2A"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 900,
              "luminance": 0.024331,
              "isAnchor": true
            }
          }
        },
        "950": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.05098,
              0.101961,
              0.090196
            ],
            "hex": "#0D1A17"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 950,
              "luminance": 0.008862,
              "isAnchor": false
            }
          }
        },
        "$description": "Estuary (মোহনা) — The ground, and the source of every surface tint and every text role.",
        "$extensions": {
          "studio.aninda": {
            "hueOklch": 176.896,
            "chromaCeiling": 0.05127,
            "anchor": "#0C3A31",
            "anchorStep": 900
          }
        }
      },
      "accent": {
        "50": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.929412,
              0.980392,
              0.992157
            ],
            "hex": "#EDFAFD"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 50,
              "luminance": 0.934671,
              "isAnchor": false
            }
          }
        },
        "100": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.85098,
              0.94902,
              0.968627
            ],
            "hex": "#D9F2F7"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 100,
              "luminance": 0.849706,
              "isAnchor": false
            }
          }
        },
        "200": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.709804,
              0.894118,
              0.92549
            ],
            "hex": "#B5E4EC"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 200,
              "luminance": 0.713654,
              "isAnchor": false
            }
          }
        },
        "300": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.556863,
              0.823529,
              0.866667
            ],
            "hex": "#8ED2DD"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 300,
              "luminance": 0.570629,
              "isAnchor": false
            }
          }
        },
        "400": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.396078,
              0.729412,
              0.780392
            ],
            "hex": "#65BAC7"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 400,
              "luminance": 0.420066,
              "isAnchor": false
            }
          }
        },
        "500": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.258824,
              0.627451,
              0.682353
            ],
            "hex": "#42A0AE"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 500,
              "luminance": 0.293546,
              "isAnchor": false
            }
          }
        },
        "600": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.152941,
              0.517647,
              0.572549
            ],
            "hex": "#278492"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 600,
              "luminance": 0.190083,
              "isAnchor": true
            }
          }
        },
        "700": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.070588,
              0.411765,
              0.454902
            ],
            "hex": "#126974"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 700,
              "luminance": 0.114921,
              "isAnchor": false
            }
          }
        },
        "800": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.019608,
              0.301961,
              0.337255
            ],
            "hex": "#054D56"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 800,
              "luminance": 0.060116,
              "isAnchor": false
            }
          }
        },
        "900": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.003922,
              0.192157,
              0.215686
            ],
            "hex": "#013137"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 900,
              "luminance": 0.024788,
              "isAnchor": false
            }
          }
        },
        "950": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.0,
              0.105882,
              0.12549
            ],
            "hex": "#001B20"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 950,
              "luminance": 0.008881,
              "isAnchor": false
            }
          }
        },
        "$description": "Tidewater (জোয়ার) — A cyan-teal one hue-step off the ground. Carries links, focus and the primary action.",
        "$extensions": {
          "studio.aninda": {
            "hueOklch": 208.996,
            "chromaCeiling": 0.0899,
            "anchor": "#0E7C8A",
            "anchorStep": 600
          }
        }
      },
      "success": {
        "50": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.937255,
              0.984314,
              0.94902
            ],
            "hex": "#EFFBF2"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 50,
              "luminance": 0.937556,
              "isAnchor": false
            }
          }
        },
        "100": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.870588,
              0.956863,
              0.886275
            ],
            "hex": "#DEF4E2"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 100,
              "luminance": 0.857214,
              "isAnchor": false
            }
          }
        },
        "200": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.745098,
              0.901961,
              0.780392
            ],
            "hex": "#BEE6C7"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 200,
              "luminance": 0.716634,
              "isAnchor": false
            }
          }
        },
        "300": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.607843,
              0.835294,
              0.666667
            ],
            "hex": "#9BD5AA"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 300,
              "luminance": 0.574582,
              "isAnchor": false
            }
          }
        },
        "400": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.466667,
              0.745098,
              0.545098
            ],
            "hex": "#77BE8B"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 400,
              "luminance": 0.426118,
              "isAnchor": false
            }
          }
        },
        "500": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.34902,
              0.643137,
              0.435294
            ],
            "hex": "#59A46F"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 500,
              "luminance": 0.298216,
              "isAnchor": false
            }
          }
        },
        "600": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.25098,
              0.533333,
              0.341176
            ],
            "hex": "#408857"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 600,
              "luminance": 0.193858,
              "isAnchor": false
            }
          }
        },
        "700": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.176471,
              0.423529,
              0.258824
            ],
            "hex": "#2D6C42"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 700,
              "luminance": 0.11676,
              "isAnchor": true
            }
          }
        },
        "800": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.113725,
              0.313725,
              0.180392
            ],
            "hex": "#1D502E"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 800,
              "luminance": 0.061956,
              "isAnchor": false
            }
          }
        },
        "900": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.058824,
              0.196078,
              0.105882
            ],
            "hex": "#0F321B"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 900,
              "luminance": 0.024618,
              "isAnchor": false
            }
          }
        },
        "950": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.019608,
              0.113725,
              0.05098
            ],
            "hex": "#051D0D"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 950,
              "luminance": 0.0094,
              "isAnchor": false
            }
          }
        },
        "$description": "Silt (পলি) — semantic",
        "$extensions": {
          "studio.aninda": {
            "hueOklch": 152.008,
            "chromaCeiling": 0.10913,
            "anchor": "#1B6B3A",
            "anchorStep": 700
          }
        }
      },
      "warning": {
        "50": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              1.0,
              0.964706,
              0.921569
            ],
            "hex": "#FFF6EB"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 50,
              "luminance": 0.931701,
              "isAnchor": false
            }
          }
        },
        "100": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.984314,
              0.917647,
              0.839216
            ],
            "hex": "#FBEAD6"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 100,
              "luminance": 0.842106,
              "isAnchor": false
            }
          }
        },
        "200": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.952941,
              0.835294,
              0.686275
            ],
            "hex": "#F3D5AF"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 200,
              "luminance": 0.697394,
              "isAnchor": false
            }
          }
        },
        "300": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.901961,
              0.741176,
              0.529412
            ],
            "hex": "#E6BD87"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 300,
              "luminance": 0.549688,
              "isAnchor": false
            }
          }
        },
        "400": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.823529,
              0.631373,
              0.372549
            ],
            "hex": "#D2A15F"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 400,
              "luminance": 0.400189,
              "isAnchor": false
            }
          }
        },
        "500": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.721569,
              0.52549,
              0.243137
            ],
            "hex": "#B8863E"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 500,
              "luminance": 0.275894,
              "isAnchor": false
            }
          }
        },
        "600": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.607843,
              0.423529,
              0.145098
            ],
            "hex": "#9B6C25"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 600,
              "luminance": 0.178281,
              "isAnchor": false
            }
          }
        },
        "700": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.486275,
              0.329412,
              0.078431
            ],
            "hex": "#7C5414"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 700,
              "luminance": 0.106767,
              "isAnchor": true
            }
          }
        },
        "800": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.364706,
              0.235294,
              0.027451
            ],
            "hex": "#5D3C07"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 800,
              "luminance": 0.055745,
              "isAnchor": false
            }
          }
        },
        "900": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.231373,
              0.145098,
              0.007843
            ],
            "hex": "#3B2502"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 900,
              "luminance": 0.022574,
              "isAnchor": false
            }
          }
        },
        "950": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.137255,
              0.07451,
              0.0
            ],
            "hex": "#231300"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 950,
              "luminance": 0.008231,
              "isAnchor": false
            }
          }
        },
        "$description": "Kans (কাশ) — semantic",
        "$extensions": {
          "studio.aninda": {
            "hueOklch": 73.298,
            "chromaCeiling": 0.108,
            "anchor": "#8A5A00",
            "anchorStep": 700
          }
        }
      },
      "danger": {
        "50": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              1.0,
              0.94902,
              0.929412
            ],
            "hex": "#FFF2ED"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 50,
              "luminance": 0.908792,
              "isAnchor": false
            }
          }
        },
        "100": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              1.0,
              0.886275,
              0.854902
            ],
            "hex": "#FFE2DA"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 100,
              "luminance": 0.807156,
              "isAnchor": false
            }
          }
        },
        "200": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              1.0,
              0.780392,
              0.72549
            ],
            "hex": "#FFC7B9"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 200,
              "luminance": 0.656114,
              "isAnchor": false
            }
          }
        },
        "300": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              1.0,
              0.65098,
              0.576471
            ],
            "hex": "#FFA693"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 300,
              "luminance": 0.506415,
              "isAnchor": false
            }
          }
        },
        "400": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.984314,
              0.513725,
              0.435294
            ],
            "hex": "#FB836F"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 400,
              "luminance": 0.378925,
              "isAnchor": false
            }
          }
        },
        "500": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.882353,
              0.396078,
              0.317647
            ],
            "hex": "#E16551"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 500,
              "luminance": 0.259115,
              "isAnchor": false
            }
          }
        },
        "600": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.752941,
              0.298039,
              0.227451
            ],
            "hex": "#C04C3A"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 600,
              "luminance": 0.166826,
              "isAnchor": false
            }
          }
        },
        "700": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.607843,
              0.215686,
              0.156863
            ],
            "hex": "#9B3728"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 700,
              "luminance": 0.098553,
              "isAnchor": true
            }
          }
        },
        "800": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.458824,
              0.145098,
              0.098039
            ],
            "hex": "#752519"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 800,
              "luminance": 0.051759,
              "isAnchor": false
            }
          }
        },
        "900": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.298039,
              0.082353,
              0.047059
            ],
            "hex": "#4C150C"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 900,
              "luminance": 0.020996,
              "isAnchor": false
            }
          }
        },
        "950": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.180392,
              0.031373,
              0.015686
            ],
            "hex": "#2E0804"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 950,
              "luminance": 0.007634,
              "isAnchor": false
            }
          }
        },
        "$description": "Laterite (লাল মাটি) — semantic",
        "$extensions": {
          "studio.aninda": {
            "hueOklch": 31.189,
            "chromaCeiling": 0.15914,
            "anchor": "#A8301F",
            "anchorStep": 700
          }
        }
      },
      "info": {
        "50": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.937255,
              0.976471,
              1.0
            ],
            "hex": "#EFF9FF"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 50,
              "luminance": 0.933217,
              "isAnchor": false
            }
          }
        },
        "100": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.870588,
              0.937255,
              1.0
            ],
            "hex": "#DEEFFF"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 100,
              "luminance": 0.84482,
              "isAnchor": false
            }
          }
        },
        "200": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.745098,
              0.870588,
              0.988235
            ],
            "hex": "#BEDEFC"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 200,
              "luminance": 0.702169,
              "isAnchor": false
            }
          }
        },
        "300": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.615686,
              0.792157,
              0.952941
            ],
            "hex": "#9DCAF3"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 300,
              "luminance": 0.55879,
              "isAnchor": false
            }
          }
        },
        "400": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.478431,
              0.694118,
              0.882353
            ],
            "hex": "#7AB1E1"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 400,
              "luminance": 0.410169,
              "isAnchor": false
            }
          }
        },
        "500": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.360784,
              0.588235,
              0.784314
            ],
            "hex": "#5C96C8"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 500,
              "luminance": 0.282572,
              "isAnchor": false
            }
          }
        },
        "600": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.270588,
              0.486275,
              0.666667
            ],
            "hex": "#457CAA"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 600,
              "luminance": 0.185821,
              "isAnchor": false
            }
          }
        },
        "700": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.192157,
              0.380392,
              0.537255
            ],
            "hex": "#316189"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 700,
              "luminance": 0.110081,
              "isAnchor": true
            }
          }
        },
        "800": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.129412,
              0.278431,
              0.403922
            ],
            "hex": "#214767"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 800,
              "luminance": 0.058088,
              "isAnchor": false
            }
          }
        },
        "900": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.070588,
              0.176471,
              0.258824
            ],
            "hex": "#122D42"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 900,
              "luminance": 0.023986,
              "isAnchor": false
            }
          }
        },
        "950": {
          "$value": {
            "colorSpace": "srgb",
            "components": [
              0.027451,
              0.098039,
              0.156863
            ],
            "hex": "#071928"
          },
          "$extensions": {
            "studio.aninda": {
              "step": 950,
              "luminance": 0.008936,
              "isAnchor": false
            }
          }
        },
        "$description": "Monsoon (বর্ষা) — semantic",
        "$extensions": {
          "studio.aninda": {
            "hueOklch": 245.674,
            "chromaCeiling": 0.0962,
            "anchor": "#235E8C",
            "anchorStep": 700
          }
        }
      }
    }
  },
  "dimension": {
    "$type": "dimension",
    "space": {
      "0": {
        "$value": {
          "value": 4,
          "unit": "px"
        },
        "$description": "Step 0 of the 4px spacing scale"
      },
      "1": {
        "$value": {
          "value": 8,
          "unit": "px"
        },
        "$description": "Step 1 of the 4px spacing scale"
      },
      "2": {
        "$value": {
          "value": 12,
          "unit": "px"
        },
        "$description": "Step 2 of the 4px spacing scale"
      },
      "3": {
        "$value": {
          "value": 16,
          "unit": "px"
        },
        "$description": "Step 3 of the 4px spacing scale"
      },
      "4": {
        "$value": {
          "value": 24,
          "unit": "px"
        },
        "$description": "Step 4 of the 4px spacing scale"
      },
      "5": {
        "$value": {
          "value": 32,
          "unit": "px"
        },
        "$description": "Step 5 of the 4px spacing scale"
      },
      "6": {
        "$value": {
          "value": 48,
          "unit": "px"
        },
        "$description": "Step 6 of the 4px spacing scale"
      },
      "7": {
        "$value": {
          "value": 64,
          "unit": "px"
        },
        "$description": "Step 7 of the 4px spacing scale"
      },
      "8": {
        "$value": {
          "value": 96,
          "unit": "px"
        },
        "$description": "Step 8 of the 4px spacing scale"
      },
      "9": {
        "$value": {
          "value": 128,
          "unit": "px"
        },
        "$description": "Step 9 of the 4px spacing scale"
      }
    },
    "radius": {
      "badge": {
        "$value": {
          "value": 4,
          "unit": "px"
        },
        "$description": "Corner radius for a badge"
      },
      "control": {
        "$value": {
          "value": 8,
          "unit": "px"
        },
        "$description": "Corner radius for a control"
      },
      "card": {
        "$value": {
          "value": 14,
          "unit": "px"
        },
        "$description": "Corner radius for a card"
      },
      "hero": {
        "$value": {
          "value": 24,
          "unit": "px"
        },
        "$description": "Corner radius for a hero"
      }
    },
    "target": {
      "min": {
        "$value": {
          "value": 24,
          "unit": "px"
        },
        "$description": "WCAG 2.2 SC 2.5.8 Target Size (Minimum), Level AA",
        "$extensions": {
          "studio.aninda": {
            "source": "WCAG 2.2 SC 2.5.8 Target Size (Minimum), Level AA"
          }
        }
      },
      "apple-min": {
        "$value": {
          "value": 28,
          "unit": "px"
        },
        "$description": "Apple HIG minimum control size, iOS and iPadOS",
        "$extensions": {
          "studio.aninda": {
            "source": "Apple HIG minimum control size, iOS and iPadOS"
          }
        }
      },
      "comfortable": {
        "$value": {
          "value": 44,
          "unit": "px"
        },
        "$description": "Apple HIG default control size, iOS and iPadOS",
        "$extensions": {
          "studio.aninda": {
            "source": "Apple HIG default control size, iOS and iPadOS"
          }
        }
      },
      "android-min": {
        "$value": {
          "value": 48,
          "unit": "px"
        },
        "$description": "Android accessibility guidance minimum touch target, in dp",
        "$extensions": {
          "studio.aninda": {
            "source": "Android accessibility guidance minimum touch target, in dp"
          }
        }
      }
    },
    "focus": {
      "ring-width": {
        "$value": {
          "value": 3,
          "unit": "px"
        },
        "$description": "Focus indicator geometry. WCAG 2.2 SC 2.4.13 Focus Appearance is Level AAA, adopted here by choice; Level AA requires only SC 2.4.11."
      },
      "ring-offset": {
        "$value": {
          "value": 2,
          "unit": "px"
        },
        "$description": "Focus indicator geometry. WCAG 2.2 SC 2.4.13 Focus Appearance is Level AAA, adopted here by choice; Level AA requires only SC 2.4.11."
      }
    },
    "type": {
      "caption": {
        "$value": {
          "value": 0.7502,
          "unit": "rem"
        },
        "$description": "12.0px at a 16px root — step -1 of a 1.333 scale"
      },
      "body": {
        "$value": {
          "value": 1.0,
          "unit": "rem"
        },
        "$description": "16.0px at a 16px root — step +0 of a 1.333 scale"
      },
      "lead": {
        "$value": {
          "value": 1.333,
          "unit": "rem"
        },
        "$description": "21.33px at a 16px root — step +1 of a 1.333 scale"
      },
      "h3": {
        "$value": {
          "value": 1.7769,
          "unit": "rem"
        },
        "$description": "28.43px at a 16px root — step +2 of a 1.333 scale"
      },
      "h2": {
        "$value": {
          "value": 2.3686,
          "unit": "rem"
        },
        "$description": "37.9px at a 16px root — step +3 of a 1.333 scale"
      },
      "h1": {
        "$value": {
          "value": 3.1573,
          "unit": "rem"
        },
        "$description": "50.52px at a 16px root — step +4 of a 1.333 scale"
      },
      "display": {
        "$value": {
          "value": 4.2087,
          "unit": "rem"
        },
        "$description": "67.34px at a 16px root — step +5 of a 1.333 scale"
      },
      "bangla-min": {
        "$value": {
          "value": 12,
          "unit": "px"
        },
        "$description": "Hard floor for Bangla — never apply the multiplier past it. At 12px the মাত্রা renders at luminance 123 on white at weight 400, which reads as grey rather than ink; at weight 500 it is 108 and holds. So this floor is only safe together with the weight bump.",
        "$extensions": {
          "studio.aninda": {
            "measuredAt": "device_scale_factor=1",
            "luminanceByWeight": {
              "400": 123,
              "500": 108,
              "600": 90
            }
          }
        }
      },
      "bangla-weight-bump-below": {
        "$value": {
          "value": 14,
          "unit": "px"
        },
        "$description": "Below this size, step Bangla up one weight. Measured: 12px/400 fails at luminance 123, 12px/500 holds at 108, 13px/400 already holds at 94. The threshold is set at 14 rather than 13 because the relationship is not monotonic — it depends on how the stroke lands on the pixel grid — and one size of margin is cheap."
      }
    }
  },
  "number": {
    "$type": "number",
    "scale": {
      "ratio": {
        "$value": 1.333,
        "$description": "A perfect fourth. The jumps are large on purpose: hierarchy is unmistakable and fewer levels are needed to express it."
      },
      "bangla": {
        "$description": "How much to shrink Bangla so it looks the same size as Latin. Measured on rendered specimens, not estimated. Bangla's reading height is about 0.62 em against Latin's 0.51, so equal nominal sizes do not look equal. These barely move across the scale because Literata's x-height is nearly flat across its optical range — a face without that property would need a wider spread.",
        "caption": {
          "$value": 0.815,
          "$description": "Bangla multiplier at caption size"
        },
        "body": {
          "$value": 0.816,
          "$description": "Bangla multiplier at body size"
        },
        "heading": {
          "$value": 0.817,
          "$description": "Bangla multiplier at heading size"
        },
        "title": {
          "$value": 0.822,
          "$description": "Bangla multiplier at title size"
        },
        "display": {
          "$value": 0.825,
          "$description": "Bangla multiplier at display size"
        }
      }
    },
    "lineHeight": {
      "bangla": {
        "$value": 1.6,
        "$description": "Bangla needs more leading than Latin: the মাত্রা sits above the letters and the vowel signs hang below, so lines collide sooner. Collision measured at 1.25."
      }
    }
  },
  "fontFamily": {
    "$type": "fontFamily",
    "latin": {
      "$value": [
        "Literata",
        "Georgia",
        "serif"
      ],
      "$description": "Literata, by Veronika Burian and José Scaglione (TypeTogether). An optical-size axis from 7 to 72, so the letterforms are redrawn for the size rather than merely scaled. Its x-height is almost flat across that range (0.5166 to 0.5130 em), which is why the Bangla multiplier below barely moves.",
      "$extensions": {
        "studio.aninda": {
          "licence": "SIL OFL 1.1"
        }
      }
    },
    "bangla": {
      "$value": [
        "Noto Serif Bengali",
        "serif"
      ],
      "$description": "Never uppercased, never letter-spaced, never synthetically emboldened. A serif Bangla answers Bengali's own letterpress tradition rather than importing a Latin UI convention.",
      "$extensions": {
        "studio.aninda": {
          "licence": "SIL OFL 1.1"
        }
      }
    },
    "mono": {
      "$value": [
        "Aninda Mono",
        "IBM Plex Mono",
        "ui-monospace",
        "monospace"
      ],
      "$description": "IBM Plex Mono, by Mike Abbink and Bold Monday. It carries the Reserved Font Name 'Plex', and subsetting a font counts as modifying it under OFL 1.1 clause 3 — so the subset shipped here is renamed 'Aninda Mono'. The unmodified family name is kept as the next fallback, so anyone who already has IBM Plex Mono installed gets the real thing.",
      "$extensions": {
        "studio.aninda": {
          "licence": "SIL OFL 1.1"
        }
      }
    }
  },
  "duration": {
    "$type": "duration",
    "motion": {
      "colour": {
        "$value": {
          "value": 120,
          "unit": "ms"
        }
      },
      "move": {
        "$value": {
          "value": 220,
          "unit": "ms"
        }
      }
    }
  },
  "cubicBezier": {
    "$type": "cubicBezier",
    "motion": {
      "standard": {
        "$value": [
          0.2,
          0.0,
          0.0,
          1.0
        ],
        "$description": "Things that move may overshoot; things that only change colour or opacity never do."
      },
      "enter": {
        "$value": [
          0.05,
          0.7,
          0.1,
          1.0
        ],
        "$description": "Things that move may overshoot; things that only change colour or opacity never do."
      },
      "exit": {
        "$value": [
          0.3,
          0.0,
          0.8,
          0.15
        ],
        "$description": "Things that move may overshoot; things that only change colour or opacity never do."
      }
    }
  }
},
  semantic: {
    light: {
  "$schema": "https://tr.designtokens.org/format/",
  "$description": "Aninda Studio semantic tokens — Light theme. Generated; do not hand-edit. Every text pairing in this file was measured against every surface it can land on, at a target of 4.5:1, on the rounded 8-bit hex and again with every channel of both colours nudged by ±1. The published figure is the worst of those.",
  "$extensions": {
    "studio.aninda": {
      "direction": "estuary",
      "theme": "light",
      "polarity": "light",
      "highContrast": false,
      "textTarget": 4.5,
      "nonTextTarget": 3.0,
      "generatedBy": "07_tokens/build.py",
      "note": "DTCG 2025.10 has no theming concept. Themes are separate files with identical token paths, because a tool is permitted to ignore $extensions and would then render one theme's values for all four without erroring."
    }
  },
  "color": {
    "$type": "color",
    "surface": {
      "lowest": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.992157,
            1.0,
            0.996078
          ],
          "hex": "#FDFFFE"
        },
        "$description": "Tonal surface 'lowest' for the Light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.995583,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "low": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.984314,
            0.988235,
            0.988235
          ],
          "hex": "#FBFCFC"
        },
        "$description": "Tonal surface 'low' for the Light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.971583,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "base": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.972549,
            0.980392,
            0.976471
          ],
          "hex": "#F8FAF9"
        },
        "$description": "Tonal surface 'base' for the Light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.951672,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "high": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.964706,
            0.968627,
            0.968627
          ],
          "hex": "#F6F7F7"
        },
        "$description": "Tonal surface 'high' for the Light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.928297,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "highest": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.952941,
            0.960784,
            0.956863
          ],
          "hex": "#F3F5F4"
        },
        "$description": "Tonal surface 'highest' for the Light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.908911,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "dim": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.945098,
            0.94902,
            0.94902
          ],
          "hex": "#F1F2F2"
        },
        "$description": "Tonal surface 'dim' for the Light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.886158,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "bright": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            1.0,
            1.0,
            1.0
          ],
          "hex": "#FFFFFF"
        },
        "$description": "Tonal surface 'bright' for the Light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 1.0,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      }
    },
    "ink": {
      "default": {
        "$description": "lightest ground step clearing 4.5:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "ground",
            "step": 950,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 15.9043,
              "worstCaseLsb": 15.6124,
              "hardestGround": "dim",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 17.7633,
                "low": 17.3556,
                "base": 17.0173,
                "high": 16.6202,
                "highest": 16.2909,
                "dim": 15.9043,
                "bright": 17.8384
              }
            }
          }
        },
        "$value": "{color.ramp.ground.950}"
      },
      "muted": {
        "$description": "lightest ground step clearing 4.5:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "ground",
            "step": 700,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 5.7775,
              "worstCaseLsb": 5.6402,
              "hardestGround": "dim",
              "level": "AA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 6.4528,
                "low": 6.3047,
                "base": 6.1818,
                "high": 6.0375,
                "highest": 5.9179,
                "dim": 5.7775,
                "bright": 6.48
              }
            }
          }
        },
        "$value": "{color.ramp.ground.700}"
      }
    },
    "line": {
      "default": {
        "$description": "lightest ground step clearing 3.0:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "ground",
            "step": 600,
            "kind": "nontext",
            "proof": {
              "required": 3.0,
              "measured": 3.938,
              "worstCaseLsb": 3.849,
              "hardestGround": "dim",
              "level": "meets 1.4.11",
              "criterion": "WCAG 2.2 1.4.11",
              "againstEverySurface": {
                "lowest": 4.3984,
                "low": 4.2974,
                "base": 4.2136,
                "high": 4.1153,
                "highest": 4.0338,
                "dim": 3.938,
                "bright": 4.4169
              }
            }
          }
        },
        "$value": "{color.ramp.ground.600}"
      }
    },
    "accent": {
      "default": {
        "$description": "lightest accent step clearing 4.5:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 700,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 5.6764,
              "worstCaseLsb": 5.546,
              "hardestGround": "dim",
              "level": "AA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 6.3399,
                "low": 6.1944,
                "base": 6.0736,
                "high": 5.9319,
                "highest": 5.8143,
                "dim": 5.6764,
                "bright": 6.3667
              }
            }
          }
        },
        "$value": "{color.ramp.accent.700}"
      },
      "edge": {
        "$description": "lightest accent step clearing 3.0:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 600,
            "kind": "nontext",
            "proof": {
              "required": 3.0,
              "measured": 3.8993,
              "worstCaseLsb": 3.8134,
              "hardestGround": "dim",
              "level": "meets 1.4.11",
              "criterion": "WCAG 2.2 1.4.11",
              "againstEverySurface": {
                "lowest": 4.3551,
                "low": 4.2551,
                "base": 4.1722,
                "high": 4.0748,
                "highest": 3.9941,
                "dim": 3.8993,
                "bright": 4.3735
              }
            }
          }
        },
        "$value": "{color.ramp.accent.600}"
      },
      "hover": {
        "$description": "nearest accent step beyond 700, away from the label #FDFFFE, clearing 4.5:1 as a ground under that label and staying ΔE 9.28 from the resting fill",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 800,
            "kind": "fill",
            "proof": {
              "required": 4.5,
              "measured": 9.4953,
              "worstCaseLsb": 9.2768,
              "hardestGround": "label (surface.lowest)",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "label (surface.lowest)": 9.4953
              }
            }
          }
        },
        "$value": "{color.ramp.accent.800}"
      }
    },
    "focus": {
      "ring": {
        "$description": "lightest accent step clearing 3.0:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 600,
            "kind": "nontext",
            "proof": {
              "required": 3.0,
              "measured": 3.8993,
              "worstCaseLsb": 3.8134,
              "hardestGround": "dim",
              "level": "meets 1.4.11",
              "criterion": "WCAG 2.2 1.4.11",
              "againstEverySurface": {
                "lowest": 4.3551,
                "low": 4.2551,
                "base": 4.1722,
                "high": 4.0748,
                "highest": 3.9941,
                "dim": 3.8993,
                "bright": 4.3735
              }
            }
          }
        },
        "$value": "{color.ramp.accent.600}"
      }
    },
    "status": {
      "success": {
        "$description": "lightest success step clearing 4.5:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "success",
            "step": 700,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 5.6138,
              "worstCaseLsb": 5.4829,
              "hardestGround": "dim",
              "level": "AA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 6.27,
                "low": 6.1261,
                "base": 6.0067,
                "high": 5.8665,
                "highest": 5.7503,
                "dim": 5.6138,
                "bright": 6.2965
              }
            }
          }
        },
        "$value": "{color.ramp.success.700}"
      },
      "warning": {
        "$description": "lightest warning step clearing 4.5:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "warning",
            "step": 700,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 5.9716,
              "worstCaseLsb": 5.8314,
              "hardestGround": "dim",
              "level": "AA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 6.6696,
                "low": 6.5165,
                "base": 6.3895,
                "high": 6.2404,
                "highest": 6.1168,
                "dim": 5.9716,
                "bright": 6.6978
              }
            }
          }
        },
        "$value": "{color.ramp.warning.700}"
      },
      "danger": {
        "$description": "lightest danger step clearing 4.5:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "danger",
            "step": 700,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 6.3019,
              "worstCaseLsb": 6.1622,
              "hardestGround": "dim",
              "level": "AA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 7.0385,
                "low": 6.8769,
                "base": 6.7429,
                "high": 6.5855,
                "highest": 6.455,
                "dim": 6.3019,
                "bright": 7.0682
              }
            }
          }
        },
        "$value": "{color.ramp.danger.700}"
      },
      "info": {
        "$description": "lightest info step clearing 4.5:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "info",
            "step": 700,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 5.848,
              "worstCaseLsb": 5.7107,
              "hardestGround": "dim",
              "level": "AA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 6.5316,
                "low": 6.3817,
                "base": 6.2573,
                "high": 6.1113,
                "highest": 5.9902,
                "dim": 5.848,
                "bright": 6.5592
              }
            }
          }
        },
        "$value": "{color.ramp.info.700}"
      }
    }
  }
},
    dark: {
  "$schema": "https://tr.designtokens.org/format/",
  "$description": "Aninda Studio semantic tokens — Dark theme. Generated; do not hand-edit. Every text pairing in this file was measured against every surface it can land on, at a target of 4.5:1, on the rounded 8-bit hex and again with every channel of both colours nudged by ±1. The published figure is the worst of those.",
  "$extensions": {
    "studio.aninda": {
      "direction": "estuary",
      "theme": "dark",
      "polarity": "dark",
      "highContrast": false,
      "textTarget": 4.5,
      "nonTextTarget": 3.0,
      "generatedBy": "07_tokens/build.py",
      "note": "DTCG 2025.10 has no theming concept. Themes are separate files with identical token paths, because a tool is permitted to ignore $extensions and would then render one theme's values for all four without erroring."
    }
  },
  "color": {
    "$type": "color",
    "surface": {
      "lowest": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.043137,
            0.047059,
            0.043137
          ],
          "hex": "#0B0C0B"
        },
        "$description": "Tonal surface 'lowest' for the Dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.003583,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "low": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.054902,
            0.062745,
            0.058824
          ],
          "hex": "#0E100F"
        },
        "$description": "Tonal surface 'low' for the Dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.004984,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "base": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.066667,
            0.070588,
            0.070588
          ],
          "hex": "#111212"
        },
        "$description": "Tonal surface 'base' for the Dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.005955,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "high": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.066667,
            0.07451,
            0.070588
          ],
          "hex": "#111312"
        },
        "$description": "Tonal surface 'high' for the Dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.006286,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "highest": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.070588,
            0.07451,
            0.07451
          ],
          "hex": "#121313"
        },
        "$description": "Tonal surface 'highest' for the Dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.006414,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "dim": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.023529,
            0.027451,
            0.027451
          ],
          "hex": "#060707"
        },
        "$description": "Tonal surface 'dim' for the Dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.00206,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "bright": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.070588,
            0.078431,
            0.07451
          ],
          "hex": "#121413"
        },
        "$description": "Tonal surface 'bright' for the Dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.006759,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      }
    },
    "ink": {
      "default": {
        "$description": "darkest ground step clearing 4.5:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "ground",
            "step": 50,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 17.3265,
              "worstCaseLsb": 17.0278,
              "hardestGround": "bright",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 18.3537,
                "low": 17.8858,
                "base": 17.5757,
                "high": 17.4722,
                "highest": 17.4326,
                "dim": 18.8904,
                "bright": 17.3265
              }
            }
          }
        },
        "$value": "{color.ramp.ground.50}"
      },
      "muted": {
        "$description": "darkest ground step clearing 4.5:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "ground",
            "step": 500,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 5.9612,
              "worstCaseLsb": 5.8353,
              "hardestGround": "bright",
              "level": "AA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 6.3146,
                "low": 6.1536,
                "base": 6.0469,
                "high": 6.0113,
                "highest": 5.9977,
                "dim": 6.4993,
                "bright": 5.9612
              }
            }
          }
        },
        "$value": "{color.ramp.ground.500}"
      }
    },
    "line": {
      "default": {
        "$description": "darkest ground step clearing 3.0:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "ground",
            "step": 600,
            "kind": "nontext",
            "proof": {
              "required": 3.0,
              "measured": 4.1882,
              "worstCaseLsb": 4.0943,
              "hardestGround": "bright",
              "level": "meets 1.4.11",
              "criterion": "WCAG 2.2 1.4.11",
              "againstEverySurface": {
                "lowest": 4.4365,
                "low": 4.3234,
                "base": 4.2485,
                "high": 4.2235,
                "highest": 4.2139,
                "dim": 4.5663,
                "bright": 4.1882
              }
            }
          }
        },
        "$value": "{color.ramp.ground.600}"
      }
    },
    "accent": {
      "default": {
        "$description": "darkest accent step clearing 4.5:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 500,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 6.0527,
              "worstCaseLsb": 5.9274,
              "hardestGround": "bright",
              "level": "AA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 6.4115,
                "low": 6.2481,
                "base": 6.1397,
                "high": 6.1036,
                "highest": 6.0898,
                "dim": 6.599,
                "bright": 6.0527
              }
            }
          }
        },
        "$value": "{color.ramp.accent.500}"
      },
      "edge": {
        "$description": "darkest accent step clearing 3.0:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 600,
            "kind": "nontext",
            "proof": {
              "required": 3.0,
              "measured": 4.2299,
              "worstCaseLsb": 4.1375,
              "hardestGround": "bright",
              "level": "meets 1.4.11",
              "criterion": "WCAG 2.2 1.4.11",
              "againstEverySurface": {
                "lowest": 4.4806,
                "low": 4.3664,
                "base": 4.2907,
                "high": 4.2654,
                "highest": 4.2558,
                "dim": 4.6117,
                "bright": 4.2299
              }
            }
          }
        },
        "$value": "{color.ramp.accent.600}"
      },
      "hover": {
        "$description": "nearest accent step beyond 500, away from the label #0B0C0B, clearing 4.5:1 as a ground under that label and staying ΔE 7.97 from the resting fill",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 400,
            "kind": "fill",
            "proof": {
              "required": 4.5,
              "measured": 8.7727,
              "worstCaseLsb": 8.6199,
              "hardestGround": "label (surface.lowest)",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "label (surface.lowest)": 8.7727
              }
            }
          }
        },
        "$value": "{color.ramp.accent.400}"
      }
    },
    "focus": {
      "ring": {
        "$description": "darkest accent step clearing 3.0:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 600,
            "kind": "nontext",
            "proof": {
              "required": 3.0,
              "measured": 4.2299,
              "worstCaseLsb": 4.1375,
              "hardestGround": "bright",
              "level": "meets 1.4.11",
              "criterion": "WCAG 2.2 1.4.11",
              "againstEverySurface": {
                "lowest": 4.4806,
                "low": 4.3664,
                "base": 4.2907,
                "high": 4.2654,
                "highest": 4.2558,
                "dim": 4.6117,
                "bright": 4.2299
              }
            }
          }
        },
        "$value": "{color.ramp.accent.600}"
      }
    },
    "status": {
      "success": {
        "$description": "darkest success step clearing 4.5:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "success",
            "step": 500,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 6.135,
              "worstCaseLsb": 6.0074,
              "hardestGround": "bright",
              "level": "AA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 6.4987,
                "low": 6.333,
                "base": 6.2232,
                "high": 6.1866,
                "highest": 6.1726,
                "dim": 6.6887,
                "bright": 6.135
              }
            }
          }
        },
        "$value": "{color.ramp.success.500}"
      },
      "warning": {
        "$description": "darkest warning step clearing 4.5:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "warning",
            "step": 500,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 5.7417,
              "worstCaseLsb": 5.6207,
              "hardestGround": "bright",
              "level": "AA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 6.0821,
                "low": 5.927,
                "base": 5.8243,
                "high": 5.79,
                "highest": 5.7769,
                "dim": 6.26,
                "bright": 5.7417
              }
            }
          }
        },
        "$value": "{color.ramp.warning.500}"
      },
      "danger": {
        "$description": "darkest danger step clearing 4.5:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "danger",
            "step": 500,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 5.4461,
              "worstCaseLsb": 5.3348,
              "hardestGround": "bright",
              "level": "AA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 5.7689,
                "low": 5.6219,
                "base": 5.5244,
                "high": 5.4919,
                "highest": 5.4794,
                "dim": 5.9376,
                "bright": 5.4461
              }
            }
          }
        },
        "$value": "{color.ramp.danger.500}"
      },
      "info": {
        "$description": "darkest info step clearing 4.5:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "info",
            "step": 500,
            "kind": "text",
            "proof": {
              "required": 4.5,
              "measured": 5.8593,
              "worstCaseLsb": 5.7362,
              "hardestGround": "bright",
              "level": "AA",
              "criterion": "WCAG 2.2 1.4.3",
              "againstEverySurface": {
                "lowest": 6.2067,
                "low": 6.0485,
                "base": 5.9436,
                "high": 5.9086,
                "highest": 5.8952,
                "dim": 6.3882,
                "bright": 5.8593
              }
            }
          }
        },
        "$value": "{color.ramp.info.500}"
      }
    }
  }
},
    'hc-light': {
  "$schema": "https://tr.designtokens.org/format/",
  "$description": "Aninda Studio semantic tokens — High contrast, light theme. Generated; do not hand-edit. Every text pairing in this file was measured against every surface it can land on, at a target of 7.0:1, on the rounded 8-bit hex and again with every channel of both colours nudged by ±1. The published figure is the worst of those.",
  "$extensions": {
    "studio.aninda": {
      "direction": "estuary",
      "theme": "hc-light",
      "polarity": "light",
      "highContrast": true,
      "textTarget": 7.0,
      "nonTextTarget": 4.5,
      "generatedBy": "07_tokens/build.py",
      "note": "DTCG 2025.10 has no theming concept. Themes are separate files with identical token paths, because a tool is permitted to ignore $extensions and would then render one theme's values for all four without erroring."
    }
  },
  "color": {
    "$type": "color",
    "surface": {
      "lowest": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.988235,
            0.992157,
            0.988235
          ],
          "hex": "#FCFDFC"
        },
        "$description": "Tonal surface 'lowest' for the High contrast, light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.979743,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "low": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.980392,
            0.980392,
            0.980392
          ],
          "hex": "#FAFAFA"
        },
        "$description": "Tonal surface 'low' for the High contrast, light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.955973,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "base": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.968627,
            0.972549,
            0.968627
          ],
          "hex": "#F7F8F7"
        },
        "$description": "Tonal surface 'base' for the High contrast, light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.936243,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "high": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.960784,
            0.960784,
            0.960784
          ],
          "hex": "#F5F5F5"
        },
        "$description": "Tonal surface 'high' for the High contrast, light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.913099,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "highest": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.94902,
            0.952941,
            0.94902
          ],
          "hex": "#F2F3F2"
        },
        "$description": "Tonal surface 'highest' for the High contrast, light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.893892,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "dim": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.945098,
            0.945098,
            0.945098
          ],
          "hex": "#F1F1F1"
        },
        "$description": "Tonal surface 'dim' for the High contrast, light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.879622,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "bright": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            1.0,
            1.0,
            1.0
          ],
          "hex": "#FFFFFF"
        },
        "$description": "Tonal surface 'bright' for the High contrast, light theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 1.0,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      }
    },
    "ink": {
      "default": {
        "$description": "lightest ground step clearing 7.0:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "ground",
            "step": 950,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 15.7933,
              "worstCaseLsb": 15.503,
              "hardestGround": "dim",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 17.4942,
                "low": 17.0904,
                "base": 16.7552,
                "high": 16.362,
                "highest": 16.0357,
                "dim": 15.7933,
                "bright": 17.8384
              }
            }
          }
        },
        "$value": "{color.ramp.ground.950}"
      },
      "muted": {
        "$description": "lightest ground step clearing 7.0:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "ground",
            "step": 800,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 8.4372,
              "worstCaseLsb": 8.2335,
              "hardestGround": "dim",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 9.3459,
                "low": 9.1302,
                "base": 8.9511,
                "high": 8.7411,
                "highest": 8.5668,
                "dim": 8.4372,
                "bright": 9.5298
              }
            }
          }
        },
        "$value": "{color.ramp.ground.800}"
      }
    },
    "line": {
      "default": {
        "$description": "lightest ground step clearing 4.5:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "ground",
            "step": 700,
            "kind": "nontext",
            "proof": {
              "required": 4.5,
              "measured": 5.7371,
              "worstCaseLsb": 5.6007,
              "hardestGround": "dim",
              "level": "meets policy",
              "criterion": "policy, above WCAG 2.2 1.4.11 — WCAG defines no AAA level for non-text contrast",
              "againstEverySurface": {
                "lowest": 6.355,
                "low": 6.2083,
                "base": 6.0866,
                "high": 5.9437,
                "highest": 5.8252,
                "dim": 5.7371,
                "bright": 6.48
              }
            }
          }
        },
        "$value": "{color.ramp.ground.700}"
      }
    },
    "accent": {
      "default": {
        "$description": "lightest accent step clearing 7.0:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 800,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 8.4422,
              "worstCaseLsb": 8.2447,
              "hardestGround": "dim",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 9.3514,
                "low": 9.1356,
                "base": 8.9564,
                "high": 8.7462,
                "highest": 8.5718,
                "dim": 8.4422,
                "bright": 9.5354
              }
            }
          }
        },
        "$value": "{color.ramp.accent.800}"
      },
      "edge": {
        "$description": "lightest accent step clearing 4.5:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 700,
            "kind": "nontext",
            "proof": {
              "required": 4.5,
              "measured": 5.6368,
              "worstCaseLsb": 5.5072,
              "hardestGround": "dim",
              "level": "meets policy",
              "criterion": "policy, above WCAG 2.2 1.4.11 — WCAG defines no AAA level for non-text contrast",
              "againstEverySurface": {
                "lowest": 6.2438,
                "low": 6.0997,
                "base": 5.9801,
                "high": 5.8397,
                "highest": 5.7233,
                "dim": 5.6368,
                "bright": 6.3667
              }
            }
          }
        },
        "$value": "{color.ramp.accent.700}"
      },
      "hover": {
        "$description": "nearest accent step beyond 800, away from the label #FCFDFC, clearing 7.0:1 as a ground under that label and staying ΔE 8.90 from the resting fill",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 900,
            "kind": "fill",
            "proof": {
              "required": 7.0,
              "measured": 13.7688,
              "worstCaseLsb": 13.4699,
              "hardestGround": "label (surface.lowest)",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "label (surface.lowest)": 13.7688
              }
            }
          }
        },
        "$value": "{color.ramp.accent.900}"
      }
    },
    "focus": {
      "ring": {
        "$description": "lightest accent step clearing 4.5:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 700,
            "kind": "nontext",
            "proof": {
              "required": 4.5,
              "measured": 5.6368,
              "worstCaseLsb": 5.5072,
              "hardestGround": "dim",
              "level": "meets policy",
              "criterion": "policy, above WCAG 2.2 1.4.11 — WCAG defines no AAA level for non-text contrast",
              "againstEverySurface": {
                "lowest": 6.2438,
                "low": 6.0997,
                "base": 5.9801,
                "high": 5.8397,
                "highest": 5.7233,
                "dim": 5.6368,
                "bright": 6.3667
              }
            }
          }
        },
        "$value": "{color.ramp.accent.700}"
      }
    },
    "status": {
      "success": {
        "$description": "lightest success step clearing 7.0:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "success",
            "step": 800,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 8.3035,
              "worstCaseLsb": 8.1064,
              "hardestGround": "dim",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 9.1978,
                "low": 8.9855,
                "base": 8.8092,
                "high": 8.6025,
                "highest": 8.4309,
                "dim": 8.3035,
                "bright": 9.3787
              }
            }
          }
        },
        "$value": "{color.ramp.success.800}"
      },
      "warning": {
        "$description": "lightest warning step clearing 7.0:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "warning",
            "step": 800,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 8.7912,
              "worstCaseLsb": 8.5828,
              "hardestGround": "dim",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 9.738,
                "low": 9.5132,
                "base": 9.3266,
                "high": 9.1077,
                "highest": 8.9261,
                "dim": 8.7912,
                "bright": 9.9295
              }
            }
          }
        },
        "$value": "{color.ramp.warning.800}"
      },
      "danger": {
        "$description": "lightest danger step clearing 7.0:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "danger",
            "step": 800,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 9.1356,
              "worstCaseLsb": 8.934,
              "hardestGround": "dim",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 10.1195,
                "low": 9.8859,
                "base": 9.692,
                "high": 9.4645,
                "highest": 9.2758,
                "dim": 9.1356,
                "bright": 10.3185
              }
            }
          }
        },
        "$value": "{color.ramp.danger.800}"
      },
      "info": {
        "$description": "lightest info step clearing 7.0:1 against all 7 surfaces, hardest being dim",
        "$extensions": {
          "studio.aninda": {
            "family": "info",
            "step": 800,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 8.6006,
              "worstCaseLsb": 8.3959,
              "hardestGround": "dim",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 9.5269,
                "low": 9.307,
                "base": 9.1244,
                "high": 8.9103,
                "highest": 8.7326,
                "dim": 8.6006,
                "bright": 9.7143
              }
            }
          }
        },
        "$value": "{color.ramp.info.800}"
      }
    }
  }
},
    'hc-dark': {
  "$schema": "https://tr.designtokens.org/format/",
  "$description": "Aninda Studio semantic tokens — High contrast, dark theme. Generated; do not hand-edit. Every text pairing in this file was measured against every surface it can land on, at a target of 7.0:1, on the rounded 8-bit hex and again with every channel of both colours nudged by ±1. The published figure is the worst of those.",
  "$extensions": {
    "studio.aninda": {
      "direction": "estuary",
      "theme": "hc-dark",
      "polarity": "dark",
      "highContrast": true,
      "textTarget": 7.0,
      "nonTextTarget": 4.5,
      "generatedBy": "07_tokens/build.py",
      "note": "DTCG 2025.10 has no theming concept. Themes are separate files with identical token paths, because a tool is permitted to ignore $extensions and would then render one theme's values for all four without erroring."
    }
  },
  "color": {
    "$type": "color",
    "surface": {
      "lowest": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.027451,
            0.031373,
            0.027451
          ],
          "hex": "#070807"
        },
        "$description": "Tonal surface 'lowest' for the High contrast, dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.002342,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "low": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.047059,
            0.047059,
            0.047059
          ],
          "hex": "#0C0C0C"
        },
        "$description": "Tonal surface 'low' for the High contrast, dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.003677,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "base": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.054902,
            0.058824,
            0.054902
          ],
          "hex": "#0E0F0E"
        },
        "$description": "Tonal surface 'base' for the High contrast, dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.004667,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "high": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.066667,
            0.066667,
            0.066667
          ],
          "hex": "#111111"
        },
        "$description": "Tonal surface 'high' for the High contrast, dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.005605,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "highest": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.066667,
            0.070588,
            0.066667
          ],
          "hex": "#111211"
        },
        "$description": "Tonal surface 'highest' for the High contrast, dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.005923,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "dim": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.011765,
            0.011765,
            0.011765
          ],
          "hex": "#030303"
        },
        "$description": "Tonal surface 'dim' for the High contrast, dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.000911,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      },
      "bright": {
        "$value": {
          "colorSpace": "srgb",
          "components": [
            0.070588,
            0.070588,
            0.070588
          ],
          "hex": "#121212"
        },
        "$description": "Tonal surface 'bright' for the High contrast, dark theme",
        "$extensions": {
          "studio.aninda": {
            "luminance": 0.006049,
            "derivation": "swept along the lightness axis until each rung was at least ΔE2000 0.9 from the one before it"
          }
        }
      }
    },
    "ink": {
      "default": {
        "$description": "darkest ground step clearing 7.0:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "ground",
            "step": 50,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 17.5461,
              "worstCaseLsb": 17.251,
              "hardestGround": "bright",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 18.7888,
                "low": 18.3216,
                "base": 17.9896,
                "high": 17.686,
                "highest": 17.5857,
                "dim": 19.317,
                "bright": 17.5461
              }
            }
          }
        },
        "$value": "{color.ramp.ground.50}"
      },
      "muted": {
        "$description": "darkest ground step clearing 7.0:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "ground",
            "step": 400,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 8.2853,
              "worstCaseLsb": 8.1239,
              "hardestGround": "bright",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 8.8721,
                "low": 8.6515,
                "base": 8.4947,
                "high": 8.3514,
                "highest": 8.304,
                "dim": 9.1215,
                "bright": 8.2853
              }
            }
          }
        },
        "$value": "{color.ramp.ground.400}"
      }
    },
    "line": {
      "default": {
        "$description": "darkest ground step clearing 4.5:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "ground",
            "step": 500,
            "kind": "nontext",
            "proof": {
              "required": 4.5,
              "measured": 6.0367,
              "worstCaseLsb": 5.9118,
              "hardestGround": "bright",
              "level": "meets policy",
              "criterion": "policy, above WCAG 2.2 1.4.11 — WCAG defines no AAA level for non-text contrast",
              "againstEverySurface": {
                "lowest": 6.4643,
                "low": 6.3035,
                "base": 6.1893,
                "high": 6.0849,
                "highest": 6.0504,
                "dim": 6.646,
                "bright": 6.0367
              }
            }
          }
        },
        "$value": "{color.ramp.ground.500}"
      }
    },
    "accent": {
      "default": {
        "$description": "darkest accent step clearing 7.0:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 400,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 8.3867,
              "worstCaseLsb": 8.2253,
              "hardestGround": "bright",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 8.9807,
                "low": 8.7574,
                "base": 8.5987,
                "high": 8.4536,
                "highest": 8.4057,
                "dim": 9.2332,
                "bright": 8.3867
              }
            }
          }
        },
        "$value": "{color.ramp.accent.400}"
      },
      "edge": {
        "$description": "darkest accent step clearing 4.5:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 500,
            "kind": "nontext",
            "proof": {
              "required": 4.5,
              "measured": 6.1294,
              "worstCaseLsb": 6.0051,
              "hardestGround": "bright",
              "level": "meets policy",
              "criterion": "policy, above WCAG 2.2 1.4.11 — WCAG defines no AAA level for non-text contrast",
              "againstEverySurface": {
                "lowest": 6.5635,
                "low": 6.4003,
                "base": 6.2843,
                "high": 6.1783,
                "highest": 6.1433,
                "dim": 6.748,
                "bright": 6.1294
              }
            }
          }
        },
        "$value": "{color.ramp.accent.500}"
      },
      "hover": {
        "$description": "nearest accent step beyond 400, away from the label #070807, clearing 7.0:1 as a ground under that label and staying ΔE 7.11 from the resting fill",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 300,
            "kind": "fill",
            "proof": {
              "required": 7.0,
              "measured": 11.8572,
              "worstCaseLsb": 11.6686,
              "hardestGround": "label (surface.lowest)",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "label (surface.lowest)": 11.8572
              }
            }
          }
        },
        "$value": "{color.ramp.accent.300}"
      }
    },
    "focus": {
      "ring": {
        "$description": "darkest accent step clearing 4.5:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "accent",
            "step": 500,
            "kind": "nontext",
            "proof": {
              "required": 4.5,
              "measured": 6.1294,
              "worstCaseLsb": 6.0051,
              "hardestGround": "bright",
              "level": "meets policy",
              "criterion": "policy, above WCAG 2.2 1.4.11 — WCAG defines no AAA level for non-text contrast",
              "againstEverySurface": {
                "lowest": 6.5635,
                "low": 6.4003,
                "base": 6.2843,
                "high": 6.1783,
                "highest": 6.1433,
                "dim": 6.748,
                "bright": 6.1294
              }
            }
          }
        },
        "$value": "{color.ramp.accent.500}"
      }
    },
    "status": {
      "success": {
        "$description": "darkest success step clearing 7.0:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "success",
            "step": 400,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 8.4947,
              "worstCaseLsb": 8.3311,
              "hardestGround": "bright",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 9.0963,
                "low": 8.8701,
                "base": 8.7094,
                "high": 8.5624,
                "highest": 8.5139,
                "dim": 9.3521,
                "bright": 8.4947
              }
            }
          }
        },
        "$value": "{color.ramp.success.400}"
      },
      "warning": {
        "$description": "darkest warning step clearing 7.0:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "warning",
            "step": 400,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 8.0321,
              "worstCaseLsb": 7.8755,
              "hardestGround": "bright",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 8.601,
                "low": 8.3871,
                "base": 8.2351,
                "high": 8.0961,
                "highest": 8.0502,
                "dim": 8.8427,
                "bright": 8.0321
              }
            }
          }
        },
        "$value": "{color.ramp.warning.400}"
      },
      "danger": {
        "$description": "darkest danger step clearing 7.0:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "danger",
            "step": 400,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 7.6527,
              "worstCaseLsb": 7.506,
              "hardestGround": "bright",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 8.1947,
                "low": 7.9909,
                "base": 7.8461,
                "high": 7.7137,
                "highest": 7.67,
                "dim": 8.4251,
                "bright": 7.6527
              }
            }
          }
        },
        "$value": "{color.ramp.danger.400}"
      },
      "info": {
        "$description": "darkest info step clearing 7.0:1 against all 7 surfaces, hardest being bright",
        "$extensions": {
          "studio.aninda": {
            "family": "info",
            "step": 400,
            "kind": "text",
            "proof": {
              "required": 7.0,
              "measured": 8.2101,
              "worstCaseLsb": 8.0507,
              "hardestGround": "bright",
              "level": "AAA",
              "criterion": "WCAG 2.2 1.4.6",
              "againstEverySurface": {
                "lowest": 8.7916,
                "low": 8.573,
                "base": 8.4177,
                "high": 8.2756,
                "highest": 8.2287,
                "dim": 9.0388,
                "bright": 8.2101
              }
            }
          }
        },
        "$value": "{color.ramp.info.400}"
      }
    }
  }
},
  },
  forcedColors: {
  "format": "non-dtcg",
  "$description": "Forced-colors mode cannot be expressed in DTCG. Its values are CSS system colour keywords supplied by the operating system — they have no colour space, no components and no hex, and DTCG's thirteen types include nothing that fits. Bending them into a colour token would be a lie about what they are, so this file sits deliberately outside the DTCG tree.",
  "generatedBy": "07_tokens/build.py",
  "map": {
    "color.surface.base": "Canvas",
    "color.surface.lowest": "Canvas",
    "color.surface.low": "Canvas",
    "color.surface.high": "Canvas",
    "color.surface.highest": "Canvas",
    "color.surface.dim": "Canvas",
    "color.surface.bright": "Canvas",
    "color.ink.default": "CanvasText",
    "color.ink.muted": "CanvasText",
    "color.line.default": "CanvasText",
    "color.accent.default": "LinkText",
    "color.accent.edge": "CanvasText",
    "color.accent.hover": "ButtonFace",
    "color.focus.ring": "Highlight",
    "color.status.success": "CanvasText",
    "color.status.warning": "CanvasText",
    "color.status.danger": "CanvasText",
    "color.status.info": "CanvasText"
  },
  "rules": [
    "Every brand colour must be overridden. A hex that survives forced-colors mode defeats the whole point of it.",
    "forced-color-adjust: none is forbidden except where explicitly allow-listed with a stated reason.",
    "Because status colours all resolve to CanvasText, nothing may rely on colour alone — every state carries a glyph and a word regardless.",
    "GrayText is reserved for roles that are genuinely disabled, and this map assigns it to none. CSS Color 4 defines it normatively as disabled text, so using it for a live role teaches a high-contrast reader that live content is inactive — and WCAG exempts inactive components from contrast requirements, which would hand away a measured guarantee for nothing. color.ink.muted was mapped to it and paints subtitles, toast bodies and empty-state messages."
  ]
},
  marks: [
  {
    "name": "icon-1024",
    "file": "icon-1024.svg",
    "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\" width=\"1024\" height=\"1024\" role=\"img\" fill=\"none\" style=\"color:#FFFFFF\"><title>Aninda Studio — the icon, 1024px — rounded, used everywhere</title><rect width=\"100\" height=\"100\" rx=\"24\" ry=\"24\" fill=\"#0D1A17\"/><g style=\"color:#FFFFFF\" transform=\"translate(9.4862,-7.0876) scale(0.920767)\"><circle cx=\"44\" cy=\"58\" r=\"28\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"9\"/><path d=\"M72 30V94\" stroke=\"currentColor\" stroke-width=\"9\" stroke-linecap=\"round\"/></g></svg>\n"
  },
  {
    "name": "icon-1088-watch",
    "file": "icon-1088-watch.svg",
    "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\" width=\"1088\" height=\"1088\" role=\"img\" fill=\"none\" style=\"color:#FFFFFF\"><title>Aninda Studio — the icon, 1088px for watchOS — rounded</title><rect width=\"100\" height=\"100\" rx=\"24\" ry=\"24\" fill=\"#0D1A17\"/><g style=\"color:#FFFFFF\" transform=\"translate(9.4862,-7.0876) scale(0.920767)\"><circle cx=\"44\" cy=\"58\" r=\"28\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"9\"/><path d=\"M72 30V94\" stroke=\"currentColor\" stroke-width=\"9\" stroke-linecap=\"round\"/></g></svg>\n"
  },
  {
    "name": "icon-192",
    "file": "icon-192.svg",
    "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\" width=\"192\" height=\"192\" role=\"img\" fill=\"none\" style=\"color:#FFFFFF\"><title>Aninda Studio — the icon, 192px — PWA</title><rect width=\"100\" height=\"100\" rx=\"24\" ry=\"24\" fill=\"#0D1A17\"/><g style=\"color:#FFFFFF\" transform=\"translate(9.4862,-7.0876) scale(0.920767)\"><circle cx=\"44\" cy=\"58\" r=\"28\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"9\"/><path d=\"M72 30V94\" stroke=\"currentColor\" stroke-width=\"9\" stroke-linecap=\"round\"/></g></svg>\n"
  },
  {
    "name": "icon-512",
    "file": "icon-512.svg",
    "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\" width=\"512\" height=\"512\" role=\"img\" fill=\"none\" style=\"color:#FFFFFF\"><title>Aninda Studio — the icon, 512px — avatars and PWA</title><rect width=\"100\" height=\"100\" rx=\"24\" ry=\"24\" fill=\"#0D1A17\"/><g style=\"color:#FFFFFF\" transform=\"translate(9.4862,-7.0876) scale(0.920767)\"><circle cx=\"44\" cy=\"58\" r=\"28\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"9\"/><path d=\"M72 30V94\" stroke=\"currentColor\" stroke-width=\"9\" stroke-linecap=\"round\"/></g></svg>\n"
  },
  {
    "name": "icon-appstore-square-1024",
    "file": "icon-appstore-square-1024.svg",
    "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\" width=\"1024\" height=\"1024\" role=\"img\" fill=\"none\" style=\"color:#FFFFFF\"><title>Aninda Studio — square unmasked master, for Icon Composer and App Store submission only</title><rect width=\"100\" height=\"100\" fill=\"#0D1A17\"/><g style=\"color:#FFFFFF\" transform=\"translate(9.4862,-7.0876) scale(0.920767)\"><circle cx=\"44\" cy=\"58\" r=\"28\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"9\"/><path d=\"M72 30V94\" stroke=\"currentColor\" stroke-width=\"9\" stroke-linecap=\"round\"/></g></svg>\n"
  },
  {
    "name": "mark-heavy",
    "file": "mark-heavy.svg",
    "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\" width=\"100\" height=\"100\" role=\"img\" fill=\"none\"><title>Aninda Studio — the mark, heavy weight</title><!-- Recolourable: drawn in currentColor, with no colour on the root. Set `color` on this element or an ancestor. --><circle cx=\"44\" cy=\"58\" r=\"28\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"15\"/><path d=\"M72 30V94\" stroke=\"currentColor\" stroke-width=\"15\" stroke-linecap=\"round\"/></svg>\n"
  },
  {
    "name": "mark-regular",
    "file": "mark-regular.svg",
    "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\" width=\"100\" height=\"100\" role=\"img\" fill=\"none\"><title>Aninda Studio — the mark, regular weight</title><!-- Recolourable: drawn in currentColor, with no colour on the root. Set `color` on this element or an ancestor. --><circle cx=\"44\" cy=\"58\" r=\"28\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"9\"/><path d=\"M72 30V94\" stroke=\"currentColor\" stroke-width=\"9\" stroke-linecap=\"round\"/></svg>\n"
  },
  {
    "name": "tile-web",
    "file": "tile-web.svg",
    "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\" width=\"100\" height=\"100\" role=\"img\" fill=\"none\" style=\"color:#FFFFFF\"><title>Aninda Studio — web tile</title><rect width=\"100\" height=\"100\" rx=\"24\" ry=\"24\" fill=\"#0D1A17\"/><g style=\"color:#FFFFFF\" transform=\"translate(12.7177,-2.5341) scale(0.847324)\"><circle cx=\"44\" cy=\"58\" r=\"28\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"15\"/><path d=\"M72 30V94\" stroke=\"currentColor\" stroke-width=\"15\" stroke-linecap=\"round\"/></g></svg>\n"
  },
  {
    "name": "wordmark-bangla",
    "file": "wordmark-bangla.svg",
    "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 -100 530.7 140\" width=\"530.7\" height=\"140\" role=\"img\" fill=\"none\"><title>Aninda Studio — wordmark, অনিন্দ্য স্টুডিও</title><!-- Recolourable: drawn in currentColor, with no colour on the root. Set `color` on this element or an ancestor. --><g fill=\"currentColor\"><g transform=\"translate(0.000,0.000) scale(0.100000,-0.100000)\"><path d=\"M687.5575561523438 -16.03948974609375 634.318603515625 22.4002685546875Q602.6385498046875 76.64056396484375 563.098388671875 114.7008056640625Q523.5582275390625 152.76104736328125 475.1981201171875 178.961181640625L498.59771728515625 246.080322265625Q536.5582275390625 222.84002685546875 572.2784423828125 186.55990600585938Q607.9986572265625 150.27978515625 638.6787109375 88.5997314453125L629.759033203125 72.43975830078125V564.5609130859375H4.639892578125L-30.5997314453125 622H767.8775024414062L804.1171264648438 564.5609130859375H693.5173950195312V-14.71954345703125ZM341.87884521484375 80.04217529296875Q292.8795166015625 80.04217529296875 246.79986572265625 99.22189331054688Q200.72021484375 118.401611328125 159.50033569335938 163.06124877929688Q118.28045654296875 207.72088623046875 82.02041625976562 284.4206848144531Q45.7603759765625 361.1204833984375 15.56024169921875 475.16064453125L61.07965087890625 488.4805908203125Q96.39959716796875 374.64056396484375 137.699462890625 307.7004699707031Q178.99932861328125 240.7603759765625 227.619140625 212.16030883789062Q276.23895263671875 183.56024169921875 333.19879150390625 183.56024169921875Q401.91900634765625 183.56024169921875 441.4789123535156 215.46051025390625Q481.038818359375 247.36077880859375 477.6787109375 309.08099365234375Q475.9986572265625 346.80120849609375 462.4186706542969 370.4213562011719Q448.83868408203125 394.04150390625 429.4387512207031 405.4815979003906Q410.038818359375 416.92169189453125 390.23895263671875 416.92169189453125Q376.27911376953125 416.92169189453125 365.1593017578125 413.621826171875Q354.03948974609375 410.32196044921875 340.1593017578125 403.64190673828125Q335.1593017578125 445.28179931640625 319.89959716796875 477.20147705078125Q304.639892578125 509.12115478515625 273.5404968261719 532.7208862304688Q242.44110107421875 556.3206176757812 188.842041015625 571.3206176757812L312.2396240234375 573.16064453125Q332.03948974609375 557.16064453125 351.2991943359375 531.2607116699219Q370.55889892578125 505.36077880859375 383.15863037109375 473.08099365234375Q395.75836181640625 440.80120849609375 395.75836181640625 403.56158447265625Q395.75836181640625 359.4417724609375 371.3785095214844 329.7218933105469Q346.9986572265625 300.00201416015625 301.91900634765625 300.00201416015625Q259.03948974609375 300.00201416015625 229.65963745117188 326.76171875Q200.27978515625 353.52142333984375 200.27978515625 399.48126220703125Q200.27978515625 452.60107421875 236.99966430664062 479.9407653808594Q273.71954345703125 507.28045654296875 329.91900634765625 507.28045654296875Q396.9986572265625 507.28045654296875 442.93841552734375 477.5404968261719Q488.878173828125 447.800537109375 512.1780395507812 399.8406982421875Q535.4779052734375 351.880859375 535.4779052734375 295.80120849609375Q535.4779052734375 250.64190673828125 524.0381469726562 211.62216186523438Q512.598388671875 172.6024169921875 488.9986572265625 142.76239013671875Q465.39892578125 112.92236328125 428.759033203125 96.48226928710938Q392.119140625 80.04217529296875 341.87884521484375 80.04217529296875Z\"/></g><g transform=\"translate(77.400,0.000) scale(0.100000,-0.100000)\"><path d=\"M139.47857666015625 -27.8795166015625 80 2.360107421875V564.5609130859375H4.79986572265625L-30.5997314453125 622H74.11981201171875Q52.27978515625 642.3199462890625 30.239959716796875 664.6198120117188Q8.20013427734375 686.919677734375 -12.27978515625 709.8795166015625Q15.0401611328125 775.9598388671875 57.699798583984375 823.0599060058594Q100.35943603515625 870.1599731445312 154.65896606445312 895.4799194335938Q208.95849609375 920.7998657226562 269.51806640625 920.7998657226562Q319.91766357421875 920.7998657226562 370.2774353027344 903.7399597167969Q420.63720703125 886.6800537109375 468.3570861816406 856.7001342773438Q516.0769653320312 826.72021484375 560.1770324707031 787.5401611328125Q604.277099609375 748.360107421875 641.997314453125 704.1198120117188L613.6780395507812 678.2804565429688Q550.5977172851562 739.9210205078125 494.8975830078125 775.0411682128906Q439.19744873046875 810.1613159179688 389.6174621582031 825.3212890625Q340.0374755859375 840.4812622070312 294.07763671875 840.4812622070312Q244.3975830078125 840.4812622070312 201.07763671875 818.3410339355469Q157.7576904296875 796.2008056640625 127.7978515625 761.4605102539062Q97.8380126953125 726.72021484375 86.5582275390625 689.1599731445312Q95.07830810546875 677.3199462890625 101.99832153320312 665.8999328613281Q108.9183349609375 654.4799194335938 116.4183349609375 643.3999328613281Q123.9183349609375 632.3199462890625 131.9183349609375 622H217.2784423828125L254.51806640625 564.5609130859375H143.75836181640625V-26.5595703125Z\"/></g><g transform=\"translate(99.800,0.000) scale(0.100000,-0.100000)\"><path d=\"M449.71820068359375 -16.67938232421875 401.27911376953125 20.84002685546875Q399.479248046875 58.7603759765625 390.479248046875 100.16064453125Q381.479248046875 141.5609130859375 366.2192077636719 180.44110107421875Q350.95916748046875 219.3212890625 330.3591003417969 250.60140991210938Q309.759033203125 281.88153076171875 283.5789794921875 300.4815979003906Q257.39892578125 319.0816650390625 227.23895263671875 319.0816650390625Q216.759033203125 319.0816650390625 206.55923461914062 317.10174560546875Q196.35943603515625 315.121826171875 189.199462890625 310.96185302734375L215.27911376953125 351.4002685546875Q229.39892578125 341.7603759765625 235.11880493164062 324.10040283203125Q240.83868408203125 306.4404296875 240.83868408203125 289.4805908203125Q240.83868408203125 262.68072509765625 229.8587646484375 241.48092651367188Q218.87884521484375 220.2811279296875 197.67904663085938 208.3212890625Q176.479248046875 196.3614501953125 144.71954345703125 196.3614501953125Q89.9598388671875 196.3614501953125 62.38018798828125 228.88119506835938Q34.800537109375 261.40093994140625 34.800537109375 309.1204833984375Q34.800537109375 362.79986572265625 69.82028198242188 393.4996643066406Q104.84002685546875 424.199462890625 161.5997314453125 424.199462890625Q205.75970458984375 424.199462890625 242.919677734375 408.35943603515625Q280.07965087890625 392.5194091796875 309.2396240234375 364.4193420410156Q338.39959716796875 336.31927490234375 359.7995300292969 300.2991943359375Q381.199462890625 264.27911376953125 394.2593688964844 223.99899291992188Q407.31927490234375 183.7188720703125 411.27911376953125 143.6787109375L400.8795166015625 149.2396240234375Q399.5595703125 168.03948974609375 397.39959716796875 199.2991943359375Q395.2396240234375 230.55889892578125 393.57965087890625 266.5786437988281Q391.919677734375 302.598388671875 391.919677734375 334.43841552734375V564.5609130859375H5.47991943359375L-30.5997314453125 622H530.1981201171875L566.2777709960938 564.5609130859375H455.67803955078125V-15.35943603515625Z\"/></g><g transform=\"translate(153.400,0.000) scale(0.100000,-0.100000)\"><path d=\"M680.51806640625 -26.7978515625Q653.878173828125 31.08233642578125 638.3584289550781 90.92202758789062Q622.8386840820312 150.76171875 622.8386840820312 212.44110107421875Q622.8386840820312 246.60107421875 627.2586975097656 280.26104736328125Q631.6787109375 313.9210205078125 640.9387512207031 347.1609802246094Q650.1987915039062 380.40093994140625 663.8788452148438 412.04083251953125L687.3179321289062 399.24163818359375Q636.6378784179688 368.92169189453125 589.7178649902344 331.5217590332031Q542.7978515625 294.121826171875 496.7178649902344 251.38186645507812Q450.63787841796875 208.64190673828125 403.157958984375 159.96185302734375L346.07965087890625 196.44110107421875Q329.39959716796875 265.961181640625 307.4795837402344 313.1014099121094Q285.5595703125 360.24163818359375 260.89959716796875 384.46185302734375Q236.2396240234375 408.68206787109375 209.43975830078125 408.68206787109375Q200.27978515625 408.68206787109375 191.69979858398438 407.1020812988281Q183.11981201171875 405.5220947265625 176.79986572265625 402.36212158203125L199.43975830078125 436.76104736328125Q212.2396240234375 429.12115478515625 217.3795166015625 413.2811279296875Q222.5194091796875 397.44110107421875 222.5194091796875 379.44110107421875Q222.5194091796875 343.2811279296875 199.13955688476562 318.5813293457031Q175.75970458984375 293.88153076171875 133.3199462890625 293.88153076171875Q83.52008056640625 293.88153076171875 59.92034912109375 321.9213562011719Q36.32061767578125 349.961181640625 36.32061767578125 393.240966796875Q36.32061767578125 443.00067138671875 69.800537109375 471.2205505371094Q103.28045654296875 499.4404296875 153.88018798828125 499.4404296875Q195.72021484375 499.4404296875 230.62014770507812 479.74029541015625Q265.52008056640625 460.0401611328125 292.2399597167969 425.7399597167969Q318.9598388671875 391.43975830078125 336.3396911621094 346.2995300292969Q353.71954345703125 301.1593017578125 361.03948974609375 250.119140625L343.43975830078125 239.6787109375V564.5609130859375H5.639892578125L-30.5997314453125 622H784.2376098632812L820.3172607421875 564.5609130859375H407.1981201171875V258.60040283203125L385.23828125 282.35943603515625Q410.07830810546875 309.199462890625 440.9983215332031 337.4595031738281Q471.9183349609375 365.71954345703125 507.75836181640625 394.07965087890625Q543.598388671875 422.43975830078125 582.1984558105469 448.79986572265625Q620.7985229492188 475.15997314453125 661.6787109375 497.52008056640625L757.357421875 412.40093994140625Q723.357421875 357.240966796875 705.7774353027344 295.8811950683594Q688.1974487304688 234.52142333984375 688.1974487304688 172.84136962890625Q688.1974487304688 142.20147705078125 691.7975158691406 112.62149047851562Q695.3975830078125 83.04150390625 703.07763671875 53.401611328125Q710.7576904296875 23.76171875 722.2376098632812 -8.157958984375Z\"/></g><g transform=\"translate(232.400,0.000) scale(0.100000,-0.100000)\"><path d=\"M83.47991943359375 -50.318603515625 56.4002685546875 -13.91900634765625Q101.0401611328125 14.240966796875 121.360107421875 51.820953369140625Q141.6800537109375 89.40093994140625 141.6800537109375 133.5609130859375Q141.6800537109375 165.9210205078125 129.44009399414062 197.60107421875Q117.20013427734375 229.2811279296875 100.38018798828125 261.7011413574219Q83.56024169921875 294.12115478515625 71.32028198242188 328.2811279296875Q59.080322265625 362.44110107421875 59.080322265625 398.9210205078125Q59.080322265625 438.5609130859375 75.44009399414062 470.86077880859375Q91.79986572265625 503.16064453125 117.15963745117188 529.5605773925781Q142.5194091796875 555.9605102539062 167.83935546875 574.9605102539062L177.9598388671875 564.5609130859375H5.47991943359375L-30.5997314453125 622H286.0789794921875L322.15863037109375 564.5609130859375H207.1593017578125L231.83868408203125 571.9605102539062Q213.51873779296875 558.800537109375 194.33868408203125 536.0605773925781Q175.15863037109375 513.3206176757812 162.05856323242188 483.32061767578125Q148.95849609375 453.32061767578125 148.95849609375 417.800537109375Q148.95849609375 383.60040283203125 161.03848266601562 353.3403625488281Q173.11846923828125 323.080322265625 189.2784423828125 292.8403625488281Q205.43841552734375 262.60040283203125 217.51840209960938 229.20046997070312Q229.598388671875 195.800537109375 229.598388671875 156.32061767578125Q229.598388671875 91.36077880859375 188.19879150390625 37.480926513671875Q146.7991943359375 -16.39892578125 83.47991943359375 -50.318603515625Z\"/></g><g transform=\"translate(287.400,0.000) scale(0.100000,-0.100000)\"><path d=\"M596.277099609375 28.3212890625Q559.1572875976562 28.3212890625 528.57763671875 44.7811279296875Q497.99798583984375 61.240966796875 479.89825439453125 90.68072509765625Q461.79852294921875 120.1204833984375 461.79852294921875 158.56024169921875V322.48260498046875L466.598388671875 275.92303466796875Q451.878173828125 308.60308837890625 439.35809326171875 326.92303466796875Q426.8380126953125 345.24298095703125 415.7580261230469 352.722900390625Q404.67803955078125 360.20281982421875 393.878173828125 360.20281982421875Q382.5582275390625 360.20281982421875 371.21820068359375 352.4628601074219Q359.878173828125 344.722900390625 346.378173828125 322.20281982421875Q332.878173828125 299.6827392578125 312.5582275390625 255.6024169921875Q292.23828125 209.842041015625 272.4983215332031 183.14190673828125Q252.75836181640625 156.4417724609375 230.598388671875 145.4417724609375Q208.43841552734375 134.4417724609375 178.43841552734375 134.4417724609375Q150.91900634765625 134.4417724609375 125.1593017578125 150.16131591796875Q99.39959716796875 165.880859375 76.0997314453125 199.02041625976562Q52.79986572265625 232.15997314453125 30.79986572265625 284L70.31927490234375 303.39959716796875Q86.31927490234375 274.199462890625 99.73928833007812 259.199462890625Q113.1593017578125 244.199462890625 125.81927490234375 238.95950317382812Q138.479248046875 233.71954345703125 151.95916748046875 233.71954345703125Q173.27911376953125 233.71954345703125 190.69912719726562 246.53948974609375Q208.119140625 259.35943603515625 226.55923461914062 290.07965087890625Q244.99932861328125 320.79986572265625 266.8795166015625 374.16064453125Q283.67938232421875 414.36077880859375 300.33935546875 432.2607116699219Q316.99932861328125 450.16064453125 332.31927490234375 455.2205505371094Q347.63922119140625 460.28045654296875 359.759033203125 460.28045654296875Q393.6787109375 460.28045654296875 421.8785095214844 428.1208190917969Q450.07830810546875 395.961181640625 478.31793212890625 329.282470703125L469.43841552734375 337.52276611328125Q467.2784423828125 357.72222900390625 465.2784423828125 384.4421081542969Q463.2784423828125 411.1619873046875 462.6984558105469 437.8818664550781Q462.11846923828125 464.60174560546875 462.11846923828125 483.80120849609375V564.5609130859375H114.47991943359375L109.16064453125 578.72021484375Q154.43975830078125 569.72021484375 187.41934204101562 554.0602416992188Q220.39892578125 538.4002685546875 241.61880493164062 513.0003356933594Q262.83868408203125 487.60040283203125 272.9986572265625 450.5404968261719Q283.15863037109375 413.4805908203125 282.95849609375 361.68072509765625L252.6787109375 307.68072509765625Q251.3587646484375 359.240966796875 241.55889892578125 394.2212219238281Q231.759033203125 429.20147705078125 213.69912719726562 450.42169189453125Q195.63922119140625 471.64190673828125 168.45916748046875 481.342041015625Q141.27911376953125 491.04217529296875 105.19879150390625 491.04217529296875Q90.39892578125 491.04217529296875 77.41900634765625 489.9621887207031Q64.4390869140625 488.8822021484375 54.59906005859375 486.8822021484375L-30.5997314453125 622H888.9163208007812L924.8359985351562 564.5609130859375H525.556884765625V160.080322265625Q525.556884765625 133.52008056640625 541.6770324707031 118.139892578125Q557.7971801757812 102.75970458984375 584.717529296875 102.75970458984375Q615.7978515625 102.75970458984375 645.5779724121094 124.15997314453125Q675.3580932617188 145.56024169921875 699.6981201171875 180.46051025390625Q724.0381469726562 215.36077880859375 739.1181335449219 257.8008728027344Q754.1981201171875 300.240966796875 756.1981201171875 342.16064453125L788.3567504882812 311.40093994140625Q778.2369384765625 299.12115478515625 766.5371398925781 290.461181640625Q754.8373413085938 281.80120849609375 731.1171264648438 281.80120849609375Q690.5173950195312 281.80120849609375 668.1375427246094 306.0010070800781Q645.7576904296875 330.2008056640625 645.7576904296875 368.64056396484375Q645.7576904296875 403.88018798828125 670.4374084472656 430.9200134277344Q695.1171264648438 457.9598388671875 740.8768310546875 457.9598388671875Q770.9966430664062 457.9598388671875 796.0364685058594 444.8199462890625Q821.0762939453125 431.6800537109375 836.2161865234375 403.4802551269531Q851.3560791015625 375.28045654296875 851.3560791015625 328.16064453125Q851.3560791015625 280.240966796875 830.6961059570312 227.86111450195312Q810.0361328125 175.48126220703125 774.4762268066406 130.24130249023438Q738.9163208007812 85.0013427734375 693.1365356445312 56.66131591796875Q647.3567504882812 28.3212890625 596.277099609375 28.3212890625ZM737.0756225585938 608.16064453125Q733.87548828125 647.1204833984375 711.6552734375 671.0404968261719Q689.43505859375 694.9605102539062 658.9748840332031 706.4006042480469Q628.5147094726562 717.8406982421875 597.6746826171875 717.8406982421875Q563.7944946289062 717.8406982421875 533.4745483398438 714.3406982421875Q503.15460205078125 710.8406982421875 471.854736328125 707.3406982421875Q440.55487060546875 703.8406982421875 402.55487060546875 703.8406982421875Q345.8353271484375 703.8406982421875 308.3155822753906 724.3206176757812Q270.79583740234375 744.800537109375 252.65594482421875 780.6004028320312Q234.51605224609375 816.4002685546875 234.51605224609375 861.5200805664062Q234.51605224609375 875.9598388671875 235.83599853515625 890.8995971679688Q237.15594482421875 905.83935546875 239.47589111328125 919.7991943359375L283.1954345703125 915.3192749023438Q282.1954345703125 907.1593017578125 281.6154479980469 898.6793823242188Q281.03546142578125 890.199462890625 281.03546142578125 882.7195434570312Q281.03546142578125 835.6392211914062 312.735595703125 816.2192077636719Q344.43572998046875 796.7991943359375 396.63519287109375 796.7991943359375Q446.43505859375 796.7991943359375 491.43505859375 802.7192077636719Q536.43505859375 808.6392211914062 586.43505859375 808.6392211914062Q634.354736328125 808.6392211914062 677.8346557617188 785.7794494628906Q721.3145751953125 762.919677734375 750.8346557617188 718.4200134277344Q780.354736328125 673.9203491210938 785.5548706054688 608.16064453125Z\"/></g><g transform=\"translate(358.100,-2.200) scale(0.100000,-0.100000)\"><path d=\"M178.60040283203125 -291.35943603515625Q140.96051025390625 -233.03948974609375 94.24063110351562 -189.17938232421875Q47.520751953125 -145.31927490234375 -9.699127197265625 -120.619140625Q-66.91900634765625 -95.91900634765625 -135.39892578125 -95.91900634765625Q-172.99932861328125 -95.91900634765625 -189.61947631835938 -107.85910034179688Q-206.2396240234375 -119.7991943359375 -206.2396240234375 -140.99932861328125Q-206.2396240234375 -162.8795166015625 -190.03948974609375 -176.419677734375Q-173.83935546875 -189.9598388671875 -144.27911376953125 -189.9598388671875Q-115.55889892578125 -189.9598388671875 -94.29885864257812 -176.67971801757812Q-73.038818359375 -163.39959716796875 -61.2188720703125 -134.199462890625Q-49.39892578125 -104.99932861328125 -49.39892578125 -57.99932861328125Q-49.39892578125 -43.35943603515625 -52.318939208984375 -22.579315185546875Q-55.23895263671875 -1.7991943359375 -60.0789794921875 18.160980224609375Q-64.91900634765625 38.12115478515625 -70.759033203125 49.44110107421875L-16.15997314453125 63.520751953125Q-2.47991943359375 35.04083251953125 3.65997314453125 -6.399261474609375Q9.79986572265625 -47.83935546875 9.79986572265625 -88.759033203125Q9.79986572265625 -136.7991943359375 -7.0 -175.03915405273438Q-23.79986572265625 -213.27911376953125 -57.419677734375 -235.41900634765625Q-91.03948974609375 -257.55889892578125 -141.1593017578125 -257.55889892578125Q-193.038818359375 -257.55889892578125 -228.75869750976562 -226.09906005859375Q-264.47857666015625 -194.63922119140625 -264.47857666015625 -144.199462890625Q-264.47857666015625 -94.5997314453125 -228.3587646484375 -63.559906005859375Q-192.23895263671875 -32.52008056640625 -124.119140625 -32.52008056640625Q-69.83935546875 -32.52008056640625 -20.39959716796875 -52.0Q29.0401611328125 -71.47991943359375 72.5 -104.9598388671875Q115.9598388671875 -138.43975830078125 151.35977172851562 -180.33969116210938Q186.75970458984375 -222.2396240234375 212.11981201171875 -268.07965087890625Z\"/></g><g transform=\"translate(376.800,0.000) scale(0.100000,-0.100000)\"><path d=\"M139.47857666015625 -27.8795166015625 80 2.360107421875V564.5609130859375H4.79986572265625L-30.5997314453125 622H74.11981201171875Q52.27978515625 642.3199462890625 30.239959716796875 664.6198120117188Q8.20013427734375 686.919677734375 -12.27978515625 709.8795166015625Q15.0401611328125 775.9598388671875 57.699798583984375 823.0599060058594Q100.35943603515625 870.1599731445312 154.65896606445312 895.4799194335938Q208.95849609375 920.7998657226562 269.51806640625 920.7998657226562Q319.91766357421875 920.7998657226562 370.2774353027344 903.7399597167969Q420.63720703125 886.6800537109375 468.3570861816406 856.7001342773438Q516.0769653320312 826.72021484375 560.1770324707031 787.5401611328125Q604.277099609375 748.360107421875 641.997314453125 704.1198120117188L613.6780395507812 678.2804565429688Q550.5977172851562 739.9210205078125 494.8975830078125 775.0411682128906Q439.19744873046875 810.1613159179688 389.6174621582031 825.3212890625Q340.0374755859375 840.4812622070312 294.07763671875 840.4812622070312Q244.3975830078125 840.4812622070312 201.07763671875 818.3410339355469Q157.7576904296875 796.2008056640625 127.7978515625 761.4605102539062Q97.8380126953125 726.72021484375 86.5582275390625 689.1599731445312Q95.07830810546875 677.3199462890625 101.99832153320312 665.8999328613281Q108.9183349609375 654.4799194335938 116.4183349609375 643.3999328613281Q123.9183349609375 632.3199462890625 131.9183349609375 622H217.2784423828125L254.51806640625 564.5609130859375H143.75836181640625V-26.5595703125Z\"/></g><g transform=\"translate(399.200,0.000) scale(0.100000,-0.100000)\"><path d=\"M369.2396240234375 37.68206787109375Q283.60040283203125 37.68206787109375 217.50067138671875 86.02175903320312Q151.40093994140625 134.3614501953125 103.54083251953125 232.10107421875Q55.68072509765625 329.8406982421875 24.7603759765625 477.1204833984375L71.2396240234375 488.60040283203125Q94.639892578125 399.52008056640625 122.60006713867188 333.4200134277344Q150.56024169921875 267.3199462890625 185.82028198242188 224.34002685546875Q221.080322265625 181.360107421875 266.38018798828125 160.30020141601562Q311.6800537109375 139.24029541015625 369.75970458984375 139.24029541015625Q444.35943603515625 139.24029541015625 485.9193420410156 178.42034912109375Q527.479248046875 217.60040283203125 527.479248046875 279.36077880859375Q527.479248046875 317.3212890625 517.3192749023438 339.5013427734375Q507.1593017578125 361.681396484375 487.63922119140625 375.16131591796875L530.5582275390625 380.52142333984375Q508.07830810546875 346.7215576171875 478.6984558105469 320.24163818359375Q449.318603515625 293.76171875 417.5987243652344 279.0217590332031Q385.87884521484375 264.28179931640625 355.7188720703125 264.28179931640625Q330.7991943359375 264.28179931640625 309.9394226074219 273.3417053222656Q289.07965087890625 282.401611328125 273.639892578125 296.84136962890625Q256.6800537109375 312.80120849609375 247.80020141601562 333.8410339355469Q238.92034912109375 354.880859375 238.92034912109375 382.60040283203125V564.5609130859375H5.79986572265625L-30.5997314453125 622H617.6392211914062L654.038818359375 564.5609130859375H302.6787109375V385.03948974609375Q302.6787109375 371.07965087890625 311.15863037109375 363.7396240234375Q319.6385498046875 356.39959716796875 335.15863037109375 356.39959716796875Q362.91900634765625 356.39959716796875 390.0391540527344 373.43975830078125Q417.1593017578125 390.47991943359375 442.63922119140625 418.15997314453125Q468.119140625 445.84002685546875 488.87884521484375 478.43975830078125Q533.038818359375 440.11981201171875 558.318603515625 386.2801208496094Q583.598388671875 332.4404296875 583.598388671875 257.520751953125Q583.598388671875 194.80120849609375 559.0384826660156 145.04150390625Q534.4785766601562 95.28179931640625 486.87884521484375 66.48193359375Q439.27911376953125 37.68206787109375 369.2396240234375 37.68206787109375Z\"/></g><g transform=\"translate(461.500,0.000) scale(0.100000,-0.100000)\"><path d=\"M427.59906005859375 48.44110107421875Q342.15997314453125 48.44110107421875 262.1201477050781 99.08099365234375Q182.080322265625 149.72088623046875 118.30020141601562 257.04083251953125Q54.52008056640625 364.36077880859375 14.6800537109375 532.5609130859375L59.5194091796875 545.2008056640625Q92.1593017578125 433.64056396484375 133.09939575195312 357.42034912109375Q174.03948974609375 281.20013427734375 221.89959716796875 235.23995971679688Q269.75970458984375 189.27978515625 321.9996643066406 168.919677734375Q374.2396240234375 148.5595703125 430.1593017578125 148.5595703125Q483.8795166015625 148.5595703125 519.1194763183594 164.0997314453125Q554.3594360351562 179.639892578125 571.9993286132812 205.76004028320312Q589.6392211914062 231.88018798828125 589.6392211914062 263.360107421875Q589.6392211914062 294.56024169921875 574.8192749023438 314.0003356933594Q559.9993286132812 333.4404296875 539.3594360351562 342.7004699707031Q518.7195434570312 351.96051025390625 500.5997314453125 351.800537109375L484.3199462890625 393.35943603515625Q517.27978515625 413.27978515625 538.7998657226562 440.25970458984375Q560.3199462890625 467.2396240234375 560.3199462890625 503.15997314453125Q560.3199462890625 535.1204833984375 539.5796508789062 553.2607116699219Q518.83935546875 571.4009399414062 475.39892578125 571.4009399414062Q441.9986572265625 571.4009399414062 411.0384826660156 560.0609130859375Q380.07830810546875 548.7208862304688 355.378173828125 528.9608459472656Q330.67803955078125 509.2008056640625 315.31793212890625 483.020751953125Q299.95782470703125 456.8406982421875 295.91766357421875 426.16064453125L241.27911376953125 441.6800537109375Q251.1593017578125 455.360107421875 266.99932861328125 461.0599060058594Q282.83935546875 466.75970458984375 296.39892578125 466.75970458984375Q325.87884521484375 466.75970458984375 342.9387512207031 447.4996643066406Q359.9986572265625 428.2396240234375 359.9986572265625 396.47991943359375Q359.9986572265625 358.52008056640625 338.038818359375 338.5003356933594Q316.0789794921875 318.4805908203125 278.5194091796875 318.4805908203125Q242.27978515625 318.4805908203125 214.89993286132812 343.9404296875Q187.52008056640625 369.4002685546875 187.52008056640625 419.52008056640625Q187.52008056640625 461.15997314453125 208.60006713867188 499.2399597167969Q229.6800537109375 537.3199462890625 266.84002685546875 566.7399597167969Q304 596.1599731445312 352.8199462890625 613.4200134277344Q401.639892578125 630.6800537109375 456.43975830078125 630.6800537109375Q511.67938232421875 630.6800537109375 549.4390869140625 611.8801879882812Q587.1987915039062 593.080322265625 606.6586303710938 559.5404968261719Q626.1184692382812 526.0006713867188 626.1184692382812 481.04083251953125Q626.1184692382812 444.9210205078125 614.7185363769531 408.26104736328125Q603.318603515625 371.60107421875 583.1787109375 340.8410339355469Q563.038818359375 310.08099365234375 536.7389526367188 291.4809265136719Q510.4390869140625 272.880859375 480.63922119140625 272.880859375Q443.5194091796875 272.880859375 423.3196105957031 293.4206848144531Q403.11981201171875 313.96051025390625 403.11981201171875 346.56024169921875Q403.11981201171875 368.84002685546875 412.5197448730469 385.3798522949219Q421.919677734375 401.919677734375 439.0595703125 410.5595703125Q456.199462890625 419.199462890625 479.67938232421875 419.199462890625Q512.919677734375 419.199462890625 543.2195434570312 405.7995300292969Q573.5194091796875 392.39959716796875 597.4390869140625 368.0197448730469Q621.3587646484375 343.639892578125 635.0384826660156 311.1201477050781Q648.7182006835938 278.60040283203125 648.7182006835938 240.2008056640625Q648.7182006835938 188.2811279296875 624.2784423828125 144.54116821289062Q599.8386840820312 100.80120849609375 551.0588989257812 74.62115478515625Q502.27911376953125 48.44110107421875 427.59906005859375 48.44110107421875Z\"/></g></g></svg>\n"
  },
  {
    "name": "wordmark-latin",
    "file": "wordmark-latin.svg",
    "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 -100 654.6 140\" width=\"654.6\" height=\"140\" role=\"img\" fill=\"none\"><title>Aninda Studio — wordmark, aninda studio</title><!-- Recolourable: drawn in currentColor, with no colour on the root. Set `color` on this element or an ancestor. --><g fill=\"currentColor\"><g transform=\"translate(0.000,0.000) scale(0.100000,-0.100000)\"><path d=\"M191.1204833984375 -14Q124.4805908203125 -14 87.50067138671875 21.420013427734375Q50.520751953125 56.84002685546875 50.520751953125 121.3199462890625Q50.520751953125 172.11981201171875 76.8406982421875 204.4598388671875Q103.16064453125 236.79986572265625 164.9805908203125 254.47991943359375Q226.800537109375 272.15997314453125 333.1204833984375 276.639892578125V400.8795166015625Q333.1204833984375 441.2396240234375 323.10040283203125 465.75970458984375Q313.080322265625 490.27978515625 291.8002014160156 501.5398254394531Q270.52008056640625 512.7998657226562 236.47991943359375 512.7998657226562Q204.39959716796875 512.7998657226562 172.0595703125 502.3798522949219Q139.71954345703125 491.9598388671875 123.03948974609375 475.27978515625Q143.4390869140625 452.56024169921875 154.23895263671875 436.10040283203125Q165.038818359375 419.64056396484375 169.45883178710938 408.4006042480469Q173.87884521484375 397.16064453125 173.87884521484375 388.00067138671875Q173.87884521484375 369.72088623046875 158.33901977539062 355.5010070800781Q142.7991943359375 341.2811279296875 114.5595703125 341.2811279296875Q84.360107421875 341.2811279296875 69.24029541015625 356.5609130859375Q54.1204833984375 371.8406982421875 54.1204833984375 398.1204833984375Q54.1204833984375 430.1204833984375 80.28045654296875 460.24029541015625Q106.4404296875 490.360107421875 151.44009399414062 509.47991943359375Q196.43975830078125 528.5997314453125 251.19879150390625 528.5997314453125Q316.11846923828125 528.5997314453125 359.67803955078125 509.3396911621094Q403.23760986328125 490.07965087890625 425.15728759765625 449.0398254394531Q447.07696533203125 408 447.07696533203125 343.00067138671875V79.8795166015625Q447.07696533203125 52.5194091796875 458.777099609375 41.0194091796875Q470.47723388671875 29.5194091796875 488.83734130859375 29.5194091796875Q500.6773681640625 29.5194091796875 512.7975158691406 32.779449462890625Q524.9176635742188 36.03948974609375 537.437744140625 42.5595703125L542.437744140625 35.39959716796875Q518.157958984375 6.79986572265625 491.598388671875 -3.600067138671875Q465.038818359375 -14 439.4390869140625 -14Q391.71954345703125 -14 368.11981201171875 10.739959716796875Q344.52008056640625 35.47991943359375 339.080322265625 83.20013427734375Q323.0401611328125 47.3199462890625 301.9400939941406 25.899932861328125Q280.84002685546875 4.47991943359375 253.78012084960938 -4.760040283203125Q226.72021484375 -14 191.1204833984375 -14ZM243.038818359375 30.119140625Q270.479248046875 30.119140625 290.6596374511719 43.49932861328125Q310.84002685546875 56.8795166015625 321.9802551269531 80.53982543945312Q333.1204833984375 104.20013427734375 333.1204833984375 134.800537109375V262.3199462890625Q272.199462890625 261.15997314453125 235.538818359375 249.23995971679688Q198.878173828125 237.3199462890625 182.7978515625 209.87985229492188Q166.717529296875 182.43975830078125 166.717529296875 134.39959716796875Q166.717529296875 83.2396240234375 186.13787841796875 56.67938232421875Q205.5582275390625 30.119140625 243.038818359375 30.119140625Z\"/></g><g transform=\"translate(53.500,0.000) scale(0.100000,-0.100000)\"><path d=\"M39.96051025390625 0V12L85.240966796875 17.360107421875Q100.9210205078125 19.20013427734375 105.84103393554688 28.960174560546875Q110.76104736328125 38.72021484375 110.76104736328125 64.56024169921875V435.2396240234375Q110.76104736328125 469.27978515625 104.68106079101562 482.27978515625Q98.60107421875 495.27978515625 76.44110107421875 496.43975830078125L30.1204833984375 500.27978515625L31.1204833984375 510.5997314453125L216.437744140625 520.0796508789062L221.7576904296875 514.5997314453125L220.7576904296875 415.47991943359375H221.7576904296875Q244.27777099609375 472.11981201171875 290.2178649902344 500.3597717285156Q336.157958984375 528.5997314453125 390.59771728515625 528.5997314453125Q442.717529296875 528.5997314453125 477.5973815917969 508.77978515625Q512.4772338867188 488.9598388671875 530.5371398925781 450.15997314453125Q548.5970458984375 411.360107421875 548.5970458984375 353.60040283203125V58Q548.5970458984375 35.360107421875 554.5970458984375 26.940093994140625Q560.5970458984375 18.52008056640625 579.4370727539062 16.52008056640625L622.7576904296875 12V0H365.5997314453125V11.15997314453125L405.92034912109375 15.6800537109375Q424.1204833984375 17.6800537109375 429.46051025390625 26.600067138671875Q434.800537109375 35.52008056640625 434.800537109375 58V360.47991943359375Q434.800537109375 408.11981201171875 427.0204162597656 435.97991943359375Q419.24029541015625 463.84002685546875 400.0 475.6201477050781Q380.75970458984375 487.4002685546875 346.119140625 487.4002685546875Q311.9986572265625 487.4002685546875 284.1582946777344 470.4802551269531Q256.31793212890625 453.56024169921875 240.437744140625 423.2801208496094Q224.55755615234375 393 224.55755615234375 352.75970458984375V61.360107421875Q224.55755615234375 38.72021484375 229.31759643554688 29.460174560546875Q234.07763671875 20.20013427734375 248.7576904296875 18.20013427734375L296.6385498046875 11.15997314453125V0Z\"/></g><g transform=\"translate(118.000,0.000) scale(0.100000,-0.100000)\"><path d=\"M38.080322265625 0V12L87.5609130859375 17.360107421875Q104.08099365234375 19.20013427734375 108.58099365234375 29.38018798828125Q113.08099365234375 39.56024169921875 113.08099365234375 64.56024169921875V435.2396240234375Q113.08099365234375 469.27978515625 107.00100708007812 482.27978515625Q100.9210205078125 495.27978515625 78.76104736328125 496.43975830078125L32.4404296875 500.27978515625L33.4404296875 510.5997314453125L220.0374755859375 520.0796508789062L227.0374755859375 514.5997314453125V61.360107421875Q227.0374755859375 37.88018798828125 232.19744873046875 29.0401611328125Q237.357421875 20.20013427734375 252.83734130859375 18.20013427734375L305.39825439453125 11.15997314453125V0ZM157.4390869140625 617.520751953125Q123.84002685546875 617.520751953125 103.02041625976562 637.0404968261719Q82.2008056640625 656.5602416992188 82.2008056640625 688.0796508789062Q82.2008056640625 719.2791137695312 102.86044311523438 739.2188720703125Q123.52008056640625 759.1586303710938 157.4390869140625 759.1586303710938Q192.51806640625 759.1586303710938 212.937744140625 739.7188720703125Q233.357421875 720.2791137695312 233.357421875 688.7597045898438Q233.357421875 657.4002685546875 212.53781127929688 637.4605102539062Q191.71820068359375 617.520751953125 157.4390869140625 617.520751953125Z\"/></g><g transform=\"translate(151.300,0.000) scale(0.100000,-0.100000)\"><path d=\"M39.96051025390625 0V12L85.240966796875 17.360107421875Q100.9210205078125 19.20013427734375 105.84103393554688 28.960174560546875Q110.76104736328125 38.72021484375 110.76104736328125 64.56024169921875V435.2396240234375Q110.76104736328125 469.27978515625 104.68106079101562 482.27978515625Q98.60107421875 495.27978515625 76.44110107421875 496.43975830078125L30.1204833984375 500.27978515625L31.1204833984375 510.5997314453125L216.437744140625 520.0796508789062L221.7576904296875 514.5997314453125L220.7576904296875 415.47991943359375H221.7576904296875Q244.27777099609375 472.11981201171875 290.2178649902344 500.3597717285156Q336.157958984375 528.5997314453125 390.59771728515625 528.5997314453125Q442.717529296875 528.5997314453125 477.5973815917969 508.77978515625Q512.4772338867188 488.9598388671875 530.5371398925781 450.15997314453125Q548.5970458984375 411.360107421875 548.5970458984375 353.60040283203125V58Q548.5970458984375 35.360107421875 554.5970458984375 26.940093994140625Q560.5970458984375 18.52008056640625 579.4370727539062 16.52008056640625L622.7576904296875 12V0H365.5997314453125V11.15997314453125L405.92034912109375 15.6800537109375Q424.1204833984375 17.6800537109375 429.46051025390625 26.600067138671875Q434.800537109375 35.52008056640625 434.800537109375 58V360.47991943359375Q434.800537109375 408.11981201171875 427.0204162597656 435.97991943359375Q419.24029541015625 463.84002685546875 400.0 475.6201477050781Q380.75970458984375 487.4002685546875 346.119140625 487.4002685546875Q311.9986572265625 487.4002685546875 284.1582946777344 470.4802551269531Q256.31793212890625 453.56024169921875 240.437744140625 423.2801208496094Q224.55755615234375 393 224.55755615234375 352.75970458984375V61.360107421875Q224.55755615234375 38.72021484375 229.31759643554688 29.460174560546875Q234.07763671875 20.20013427734375 248.7576904296875 18.20013427734375L296.6385498046875 11.15997314453125V0Z\"/></g><g transform=\"translate(215.300,0.000) scale(0.100000,-0.100000)\"><path d=\"M256.15997314453125 -14Q190.84002685546875 -14 144.30020141601562 13.920013427734375Q97.7603759765625 41.84002685546875 72.88052368164062 98.92001342773438Q48.00067138671875 156 48.00067138671875 241.79986572265625Q48.00067138671875 331.639892578125 77.56057739257812 395.79986572265625Q107.1204833984375 459.9598388671875 162.32028198242188 494.27978515625Q217.52008056640625 528.5997314453125 294.27978515625 528.5997314453125Q328.3199462890625 528.5997314453125 360.6201477050781 519.919677734375Q392.92034912109375 511.2396240234375 416.080322265625 496.71954345703125V691.7998657226562Q416.080322265625 724.0401611328125 408.5003356933594 734.9601745605469Q400.92034912109375 745.8801879882812 374.360107421875 747.0401611328125L327.03948974609375 750.0401611328125L328.03948974609375 760.360107421875L523.0368041992188 766.4799194335938L530.0368041992188 761V60Q530.0368041992188 36 536.2968444824219 26.420013427734375Q542.556884765625 16.84002685546875 562.2369384765625 14.84002685546875L607.5575561523438 12V0L429.5997314453125 -9L419.52008056640625 80.47991943359375H417.20013427734375Q401.84002685546875 48.5997314453125 378.3999328613281 27.43975830078125Q354.9598388671875 6.27978515625 324.5398254394531 -3.860107421875Q294.11981201171875 -14 256.15997314453125 -14ZM294.2784423828125 26.4390869140625Q330.119140625 26.4390869140625 357.21954345703125 40.1593017578125Q384.3199462890625 53.8795166015625 400.20013427734375 82.27978515625Q416.080322265625 110.6800537109375 416.080322265625 154.56024169921875V464.1593017578125Q392.360107421875 484.8795166015625 361.1797180175781 497.75970458984375Q329.99932861328125 510.639892578125 296.3587646484375 510.639892578125Q252.03814697265625 510.639892578125 223.77777099609375 485.9598388671875Q195.51739501953125 461.27978515625 182.13720703125 405.919677734375Q168.75701904296875 350.5595703125 168.75701904296875 258.199462890625Q168.75701904296875 174.5194091796875 183.37716674804688 123.49932861328125Q197.997314453125 72.479248046875 226.07763671875 49.45916748046875Q254.157958984375 26.4390869140625 294.2784423828125 26.4390869140625Z\"/></g><g transform=\"translate(278.300,0.000) scale(0.100000,-0.100000)\"><path d=\"M191.1204833984375 -14Q124.4805908203125 -14 87.50067138671875 21.420013427734375Q50.520751953125 56.84002685546875 50.520751953125 121.3199462890625Q50.520751953125 172.11981201171875 76.8406982421875 204.4598388671875Q103.16064453125 236.79986572265625 164.9805908203125 254.47991943359375Q226.800537109375 272.15997314453125 333.1204833984375 276.639892578125V400.8795166015625Q333.1204833984375 441.2396240234375 323.10040283203125 465.75970458984375Q313.080322265625 490.27978515625 291.8002014160156 501.5398254394531Q270.52008056640625 512.7998657226562 236.47991943359375 512.7998657226562Q204.39959716796875 512.7998657226562 172.0595703125 502.3798522949219Q139.71954345703125 491.9598388671875 123.03948974609375 475.27978515625Q143.4390869140625 452.56024169921875 154.23895263671875 436.10040283203125Q165.038818359375 419.64056396484375 169.45883178710938 408.4006042480469Q173.87884521484375 397.16064453125 173.87884521484375 388.00067138671875Q173.87884521484375 369.72088623046875 158.33901977539062 355.5010070800781Q142.7991943359375 341.2811279296875 114.5595703125 341.2811279296875Q84.360107421875 341.2811279296875 69.24029541015625 356.5609130859375Q54.1204833984375 371.8406982421875 54.1204833984375 398.1204833984375Q54.1204833984375 430.1204833984375 80.28045654296875 460.24029541015625Q106.4404296875 490.360107421875 151.44009399414062 509.47991943359375Q196.43975830078125 528.5997314453125 251.19879150390625 528.5997314453125Q316.11846923828125 528.5997314453125 359.67803955078125 509.3396911621094Q403.23760986328125 490.07965087890625 425.15728759765625 449.0398254394531Q447.07696533203125 408 447.07696533203125 343.00067138671875V79.8795166015625Q447.07696533203125 52.5194091796875 458.777099609375 41.0194091796875Q470.47723388671875 29.5194091796875 488.83734130859375 29.5194091796875Q500.6773681640625 29.5194091796875 512.7975158691406 32.779449462890625Q524.9176635742188 36.03948974609375 537.437744140625 42.5595703125L542.437744140625 35.39959716796875Q518.157958984375 6.79986572265625 491.598388671875 -3.600067138671875Q465.038818359375 -14 439.4390869140625 -14Q391.71954345703125 -14 368.11981201171875 10.739959716796875Q344.52008056640625 35.47991943359375 339.080322265625 83.20013427734375Q323.0401611328125 47.3199462890625 301.9400939941406 25.899932861328125Q280.84002685546875 4.47991943359375 253.78012084960938 -4.760040283203125Q226.72021484375 -14 191.1204833984375 -14ZM243.038818359375 30.119140625Q270.479248046875 30.119140625 290.6596374511719 43.49932861328125Q310.84002685546875 56.8795166015625 321.9802551269531 80.53982543945312Q333.1204833984375 104.20013427734375 333.1204833984375 134.800537109375V262.3199462890625Q272.199462890625 261.15997314453125 235.538818359375 249.23995971679688Q198.878173828125 237.3199462890625 182.7978515625 209.87985229492188Q166.717529296875 182.43975830078125 166.717529296875 134.39959716796875Q166.717529296875 83.2396240234375 186.13787841796875 56.67938232421875Q205.5582275390625 30.119140625 243.038818359375 30.119140625Z\"/></g><g transform=\"translate(352.900,0.000) scale(0.100000,-0.100000)\"><path d=\"M62.20013427734375 -14.79986572265625 48.4002685546875 170.479248046875 62.72021484375 171.7991943359375Q78.20013427734375 109.199462890625 102.20013427734375 73.07965087890625Q126.20013427734375 36.9598388671875 157.84002685546875 21.399932861328125Q189.47991943359375 5.84002685546875 228.39959716796875 5.84002685546875Q280.3199462890625 5.84002685546875 310.15997314453125 33.9002685546875Q340 61.96051025390625 340 110.32061767578125Q340 144.36077880859375 323.34002685546875 163.22088623046875Q306.6800537109375 182.08099365234375 277.7399597167969 193.02108764648438Q248.79986572265625 203.961181640625 211.199462890625 214.48126220703125Q182.88018798828125 222.9210205078125 154.9404296875 233.54083251953125Q127.00067138671875 244.16064453125 104.16064453125 261.2205505371094Q81.32061767578125 278.28045654296875 67.96051025390625 305.4404296875Q54.60040283203125 332.60040283203125 54.60040283203125 373.28045654296875Q54.60040283203125 417.52008056640625 75.30020141601562 452.8199462890625Q96 488.11981201171875 135.07965087890625 508.3597717285156Q174.1593017578125 528.5997314453125 229.55889892578125 528.5997314453125Q274.119140625 528.5997314453125 304.3390197753906 516.0595703125Q334.55889892578125 503.5194091796875 355.75836181640625 488.2396240234375L370.11846923828125 528.5997314453125H380.598388671875L392.5582275390625 367.20013427734375L376.9183349609375 368.360107421875Q356.6385498046875 437.199462890625 322.9186706542969 473.5595703125Q289.19879150390625 509.919677734375 230.83868408203125 509.919677734375Q184.6385498046875 509.919677734375 157.85842895507812 487.6194763183594Q131.07830810546875 465.31927490234375 131.07830810546875 423.55889892578125Q131.07830810546875 389.15863037109375 148.57830810546875 369.8785095214844Q166.07830810546875 350.598388671875 194.65829467773438 340.098388671875Q223.23828125 329.598388671875 256.39825439453125 319.2784423828125Q287.4779052734375 310.318603515625 316.0378112792969 298.2586975097656Q344.59771728515625 286.19879150390625 368.27777099609375 268.2988586425781Q391.95782470703125 250.39892578125 405.4779052734375 222.65896606445312Q418.99798583984375 194.91900634765625 418.99798583984375 154.59906005859375Q418.99798583984375 102.35943603515625 395.0582275390625 64.65963745117188Q371.11846923828125 26.9598388671875 328.038818359375 6.47991943359375Q284.95916748046875 -14 227.199462890625 -14Q188.71954345703125 -14 153.19979858398438 -3.260040283203125Q117.6800537109375 7.47991943359375 87 31.52008056640625L74.52008056640625 -14.79986572265625Z\"/></g><g transform=\"translate(398.600,0.000) scale(0.100000,-0.100000)\"><path d=\"M227.5997314453125 -14Q188.15997314453125 -14 159.56024169921875 0.420013427734375Q130.96051025390625 14.84002685546875 115.92068481445312 47.5Q100.880859375 80.15997314453125 100.880859375 133.79986572265625V498.5997314453125H31.00067138671875V509.43975830078125Q70.52008056640625 512.919677734375 94.29986572265625 528.1395568847656Q118.07965087890625 543.3594360351562 130.97958374023438 576.2593688964844Q143.8795166015625 609.1593017578125 149.83935546875 664.3594360351562L207.59771728515625 672.6392211914062L214.6773681640625 667.5194091796875V514.5997314453125H358.35809326171875V498.5997314453125H214.6773681640625V145.27911376953125Q214.6773681640625 98.55889892578125 228.93740844726562 75.05889892578125Q243.19744873046875 51.55889892578125 279.7576904296875 51.55889892578125Q304.437744140625 51.55889892578125 329.3979187011719 61.978912353515625Q354.35809326171875 72.39892578125 373.35809326171875 93.91900634765625L382.878173828125 86.759033203125Q352.43841552734375 38.35943603515625 316.7787780761719 12.179718017578125Q281.119140625 -14 227.5997314453125 -14Z\"/></g><g transform=\"translate(436.700,0.000) scale(0.100000,-0.100000)\"><path d=\"M253.92034912109375 -14Q177.16064453125 -14 136.12081909179688 30.219879150390625Q95.08099365234375 74.43975830078125 95.08099365234375 160.99932861328125V437.27911376953125Q95.08099365234375 470.83935546875 89.08099365234375 483.1194763183594Q83.08099365234375 495.39959716796875 61.72088623046875 496.39959716796875L26.800537109375 499.2396240234375L27.64056396484375 509.5595703125L202.3975830078125 520.0796508789062L208.87750244140625 514.5997314453125V154.9598388671875Q208.87750244140625 109.15997314453125 217.07763671875 80.79986572265625Q225.27777099609375 52.43975830078125 244.51806640625 39.39959716796875Q263.75836181640625 26.35943603515625 295.87884521484375 26.35943603515625Q330.67938232421875 26.35943603515625 357.0197448730469 41.599395751953125Q383.360107421875 56.83935546875 397.8202819824219 85.5194091796875Q412.28045654296875 114.199462890625 412.28045654296875 154.27978515625V436.95916748046875Q412.28045654296875 469.5595703125 406.5204162597656 482.4795837402344Q400.7603759765625 495.39959716796875 379.56024169921875 496.39959716796875L344.639892578125 499.2396240234375L345.47991943359375 509.5595703125L519.5970458984375 520.0796508789062L526.0769653320312 514.5997314453125V62.5595703125Q526.0769653320312 37.919677734375 532.5769653320312 27.77978515625Q539.0769653320312 17.639892578125 558.7168579101562 15.639892578125L605.0374755859375 12.639892578125L604.8775024414062 0.639892578125L426.43975830078125 -8.84002685546875L415.080322265625 82.5595703125H413.080322265625Q395.0401611328125 47.07965087890625 371.860107421875 25.93975830078125Q348.6800537109375 4.79986572265625 319.4400939941406 -4.600067138671875Q290.20013427734375 -14 253.92034912109375 -14Z\"/></g><g transform=\"translate(499.100,0.000) scale(0.100000,-0.100000)\"><path d=\"M256.15997314453125 -14Q190.84002685546875 -14 144.30020141601562 13.920013427734375Q97.7603759765625 41.84002685546875 72.88052368164062 98.92001342773438Q48.00067138671875 156 48.00067138671875 241.79986572265625Q48.00067138671875 331.639892578125 77.56057739257812 395.79986572265625Q107.1204833984375 459.9598388671875 162.32028198242188 494.27978515625Q217.52008056640625 528.5997314453125 294.27978515625 528.5997314453125Q328.3199462890625 528.5997314453125 360.6201477050781 519.919677734375Q392.92034912109375 511.2396240234375 416.080322265625 496.71954345703125V691.7998657226562Q416.080322265625 724.0401611328125 408.5003356933594 734.9601745605469Q400.92034912109375 745.8801879882812 374.360107421875 747.0401611328125L327.03948974609375 750.0401611328125L328.03948974609375 760.360107421875L523.0368041992188 766.4799194335938L530.0368041992188 761V60Q530.0368041992188 36 536.2968444824219 26.420013427734375Q542.556884765625 16.84002685546875 562.2369384765625 14.84002685546875L607.5575561523438 12V0L429.5997314453125 -9L419.52008056640625 80.47991943359375H417.20013427734375Q401.84002685546875 48.5997314453125 378.3999328613281 27.43975830078125Q354.9598388671875 6.27978515625 324.5398254394531 -3.860107421875Q294.11981201171875 -14 256.15997314453125 -14ZM294.2784423828125 26.4390869140625Q330.119140625 26.4390869140625 357.21954345703125 40.1593017578125Q384.3199462890625 53.8795166015625 400.20013427734375 82.27978515625Q416.080322265625 110.6800537109375 416.080322265625 154.56024169921875V464.1593017578125Q392.360107421875 484.8795166015625 361.1797180175781 497.75970458984375Q329.99932861328125 510.639892578125 296.3587646484375 510.639892578125Q252.03814697265625 510.639892578125 223.77777099609375 485.9598388671875Q195.51739501953125 461.27978515625 182.13720703125 405.919677734375Q168.75701904296875 350.5595703125 168.75701904296875 258.199462890625Q168.75701904296875 174.5194091796875 183.37716674804688 123.49932861328125Q197.997314453125 72.479248046875 226.07763671875 49.45916748046875Q254.157958984375 26.4390869140625 294.2784423828125 26.4390869140625Z\"/></g><g transform=\"translate(562.600,0.000) scale(0.100000,-0.100000)\"><path d=\"M38.080322265625 0V12L87.5609130859375 17.360107421875Q104.08099365234375 19.20013427734375 108.58099365234375 29.38018798828125Q113.08099365234375 39.56024169921875 113.08099365234375 64.56024169921875V435.2396240234375Q113.08099365234375 469.27978515625 107.00100708007812 482.27978515625Q100.9210205078125 495.27978515625 78.76104736328125 496.43975830078125L32.4404296875 500.27978515625L33.4404296875 510.5997314453125L220.0374755859375 520.0796508789062L227.0374755859375 514.5997314453125V61.360107421875Q227.0374755859375 37.88018798828125 232.19744873046875 29.0401611328125Q237.357421875 20.20013427734375 252.83734130859375 18.20013427734375L305.39825439453125 11.15997314453125V0ZM157.4390869140625 617.520751953125Q123.84002685546875 617.520751953125 103.02041625976562 637.0404968261719Q82.2008056640625 656.5602416992188 82.2008056640625 688.0796508789062Q82.2008056640625 719.2791137695312 102.86044311523438 739.2188720703125Q123.52008056640625 759.1586303710938 157.4390869140625 759.1586303710938Q192.51806640625 759.1586303710938 212.937744140625 739.7188720703125Q233.357421875 720.2791137695312 233.357421875 688.7597045898438Q233.357421875 657.4002685546875 212.53781127929688 637.4605102539062Q191.71820068359375 617.520751953125 157.4390869140625 617.520751953125Z\"/></g><g transform=\"translate(595.100,0.000) scale(0.100000,-0.100000)\"><path d=\"M292.55889892578125 -14Q217.67938232421875 -14 161.93975830078125 17.260040283203125Q106.20013427734375 48.52008056640625 75.42034912109375 106.6800537109375Q44.64056396484375 164.84002685546875 44.64056396484375 245.639892578125Q44.64056396484375 334.75970458984375 77.00033569335938 397.919677734375Q109.360107421875 461.07965087890625 168.33969116210938 494.8396911621094Q227.31927490234375 528.5997314453125 307.51873779296875 528.5997314453125Q380.5582275390625 528.5997314453125 434.95782470703125 497.6596374511719Q489.357421875 466.71954345703125 519.63720703125 409.0595703125Q549.9169921875 351.39959716796875 549.9169921875 270.47991943359375Q549.9169921875 183.15997314453125 518.13720703125 119.5Q486.357421875 55.84002685546875 428.3778381347656 20.920013427734375Q370.39825439453125 -14 292.55889892578125 -14ZM309.23895263671875 3.84002685546875Q347.83935546875 3.84002685546875 374.0997314453125 27.360107421875Q400.360107421875 50.88018798828125 413.5003356933594 104.20013427734375Q426.64056396484375 157.52008056640625 426.64056396484375 246.75970458984375Q426.64056396484375 318.1593017578125 417.4404296875 368.479248046875Q408.24029541015625 418.7991943359375 390.2600402832031 450.1593017578125Q372.27978515625 481.5194091796875 347.0194091796875 496.1395568847656Q321.759033203125 510.75970458984375 289.6385498046875 510.75970458984375Q250.1981201171875 510.75970458984375 222.77777099609375 488.1596374511719Q195.357421875 465.5595703125 181.21719360351562 413.9795837402344Q167.07696533203125 362.39959716796875 167.07696533203125 274.9598388671875Q167.07696533203125 177.92034912109375 185.05722045898438 117.92034912109375Q203.0374755859375 57.92034912109375 234.89791870117188 30.88018798828125Q266.75836181640625 3.84002685546875 309.23895263671875 3.84002685546875Z\"/></g></g></svg>\n"
  }
],
  markManifest: {
  "generated_by": "04_mark/build.py",
  "warning": "Generated. Do not hand-edit \u2014 change the script and re-run.",
  "grid": 100.0,
  "geometry": {
    "circle": {
      "cx": 44.0,
      "cy": 58.0,
      "r": 28.0
    },
    "stem_x": 72.0,
    "stem_top": 30.0,
    "stem_bottom": 94.0
  },
  "strokes": {
    "regular": 9.0,
    "heavy": 15.0,
    "switch_px": 24,
    "rule": "stroke 9 at 24 px and above; stroke 15 below",
    "stroke_by_file": {
      "mark-regular.svg": 9.0,
      "mark-heavy.svg": 15.0,
      "tile-web.svg": 15.0,
      "icon-1024.svg": 9.0,
      "icon-1088-watch.svg": 9.0,
      "icon-512.svg": 9.0,
      "icon-192.svg": 9.0,
      "icon-appstore-square-1024.svg": 9.0
    }
  },
  "clear_space": "half the mark's own height on all four sides",
  "safe_field": 90.0,
  "tile_radius_percent": 24.0,
  "tile_radius_grid_units_per_100": 24.0,
  "tile_radius_px_at_1024": 245.8,
  "tile_radius_source": "read at build time from dimension.radius.hero. That token is 24 px; this is 24 units per 100 on the icon grid, which is 245.8 px of rounding on the 1024 px icon. The numeral is reused deliberately, so the icon corner belongs to the same family as every other rounded corner in the kit \u2014 it is an echo, not a unit conversion. Apple publishes no corner radius; this number is ours and is not claimed to be theirs.",
  "icon_policy": {
    "decision": "One rounded icon is used on every surface, Apple included. Owner's decision, 14 August 2026.",
    "everyday": [
      "icon-1024.svg",
      "icon-1088-watch.svg",
      "icon-512.svg",
      "icon-192.svg",
      "tile-web.svg"
    ],
    "app_store_only": "icon-appstore-square-1024.svg",
    "trade_off": "Apple's current guidance asks for square, unmasked artwork: the system applies the mask and derives Liquid Glass specular highlights from the layer edges, so a pre-rounded edge sits inside the mask and the highlight follows the wrong geometry. Apple's own wording is that pre-masked artwork 'negatively impacts specular highlight effects' and makes edges 'look jagged'. Measured here: under the circle watchOS and visionOS mask to, the rounded icon and the square master are the same image in every pixel \u2014 see the difference recorded in 'checks' below. Judged rather than measured: in a static render under Apple's rounded-rectangle mask the difference looks slight. That one is not a measurement, because Apple publishes no corner radius, so there is no mask to composite against without substituting our own radius for theirs. The dynamic cost \u2014 the moving specular highlight \u2014 could not be measured outside Apple's own renderer and is not known.",
    "if_you_ever_submit_to_the_app_store": "Use icon-appstore-square-1024.svg, not the rounded icon. Icon Composer expects unmasked layers.",
    "verified_against": "Apple Human Interface Guidelines, checked 14 August 2026"
  },
  "files": [
    "mark-regular.svg",
    "mark-heavy.svg",
    "wordmark-latin.svg",
    "wordmark-bangla.svg",
    "tile-web.svg",
    "icon-1024.svg",
    "icon-1088-watch.svg",
    "icon-512.svg",
    "icon-192.svg",
    "icon-appstore-square-1024.svg"
  ],
  "contact_sheet": "proof.svg \u2014 generated from the same strings written to 04_mark/svg, with every caption read out of the artwork",
  "checks": [
    "uharfbuzz present, HarfBuzz 14.3.0",
    "Bangla wordmark: 16 code points \u2192 11 glyphs, advance 520.1",
    "Latin wordmark: 13 code points \u2192 13 glyphs, advance 653.2",
    "conjuncts formed: 15 code points \u2192 11 glyphs",
    "negative control passed: naive 16 glyphs \u2260 shaped 11 glyphs",
    "icon at stroke 9: mark 65.0\u00d773.0 scaled \u00d70.9208, worst corner exactly on the 45-unit inscribed circle \u2014 the scale is derived from the mark's own diagonal, so this is a fit by construction; what is tested is that all four corners also land inside the 90-unit field",
    "icon at stroke 15: mark 71.0\u00d779.0 scaled \u00d70.8473, worst corner exactly on the 45-unit inscribed circle \u2014 the scale is derived from the mark's own diagonal, so this is a fit by construction; what is tested is that all four corners also land inside the 90-unit field",
    "4 recolourable files carry no root colour and draw in currentColor",
    "tile-web.svg: 4.7% background showing \u2014 rounded",
    "icon-1024.svg: 4.7% background showing \u2014 rounded \u2014 the everyday icon, all platforms",
    "icon-1088-watch.svg: 4.7% background showing \u2014 rounded",
    "icon-512.svg: 4.7% background showing \u2014 rounded",
    "icon-192.svg: 4.7% background showing \u2014 rounded",
    "icon-appstore-square-1024.svg: 0.0% background showing \u2014 square and fully opaque \u2014 App Store only",
    "under a circle inscribed in the frame, icon-1024.svg and icon-appstore-square-1024.svg are the same image in all 65536 pixels \u2014 the corner rounding lies entirely outside the circle watchOS and visionOS mask to, and the artwork inside it has not drifted between the two files",
    "contact sheet: 10 artefacts nested from the same strings written to 04_mark/svg, every caption read out of the artwork"
  ]
},
  cards: {
  "_generator": "08_components/build.py",
  "_warning": "GENERATED FILE. Do not hand-edit — the next build overwrites it.",
  "_note": "width and height are the declared design canvas for a card, not a measured render height. The cards are fluid; check.py measures them at 360, 768 and 1280 CSS px.",
  "_bangla_gaps": {
    "note": "Bangla appears only where an approved string exists. Two files, and they are not interchangeable: 06_type/BANGLA-STANDARD.md governs — it holds the Bangla Academy spelling rules with their primary sources, and the 31 strings reviewed against them — while 06_type/bangla-strings.json is the register of 94 approved keys written under those rules, each carrying the rule number or dictionary page it rests on, and it is the file these cards actually read. The fields listed here are empty because neither holds an entry for them. Writing new Bangla to fill them is not allowed, so they stay in English and are named here instead, for review.",
    "name_bn": [],
    "subtitle_bn": []
  },
  "_fonts": [
    {
      "file": "fonts/literata-subset.woff2",
      "family": "Literata",
      "source": "06_type/candidates/latin/literata/Literata[opsz,wght].ttf",
      "licence": "SIL OFL 1.1",
      "licence_file": "fonts/literata-OFL.txt",
      "bytes": 82024,
      "renamed": false
    },
    {
      "file": "fonts/notoserifbengali-subset.woff2",
      "family": "Noto Serif Bengali",
      "source": "06_type/candidates/bangla/notoserifbengali/NotoSerifBengali[wdth,wght].ttf",
      "licence": "SIL OFL 1.1",
      "licence_file": "fonts/notoserifbengali-OFL.txt",
      "bytes": 110712,
      "renamed": false
    },
    {
      "file": "fonts/anindamono-subset.woff2",
      "family": "Aninda Mono",
      "source": "06_type/candidates/mono/ibmplexmono/IBMPlexMono-Regular.ttf",
      "licence": "SIL OFL 1.1",
      "licence_file": "fonts/anindamono-OFL.txt",
      "bytes": 10464,
      "renamed": true
    },
    {
      "file": "fonts/AnindaMono-Regular.ttf",
      "family": "Aninda Mono (desktop)",
      "source": "06_type/candidates/mono/ibmplexmono/IBMPlexMono-Regular.ttf",
      "licence": "SIL OFL 1.1",
      "licence_file": "fonts/anindamono-OFL.txt",
      "bytes": 136228,
      "renamed": true,
      "subset": false
    }
  ],
  "counts": {
    "Foundations": 6,
    "Components": 16,
    "Patterns": 8
  },
  "cards": [
    {
      "path": "cards/foundations/colour.html",
      "name": "Colour",
      "name_bn": "রং",
      "group": "Foundations",
      "subtitle": "Every colour role across four themes, each with the contrast ratio it was measured at and the criterion it was measured against, over the seven surfaces they are measured against.",
      "subtitle_bn": "চার থিমে প্রতিটি রঙের ভূমিকা — প্রতিটির মাপা কনট্রাস্ট অনুপাত আর কোন মানদণ্ডে মাপা হয়েছে",
      "width": 1280,
      "height": 2400
    },
    {
      "path": "cards/foundations/typography.html",
      "name": "Typography",
      "name_bn": "হরফ",
      "group": "Foundations",
      "subtitle": "One scale of a perfect fourth, two scripts, a measured multiplier for Bangla and a floor it never goes below.",
      "subtitle_bn": "পারফেক্ট ফোর্থ অনুপাতে একটি স্কেল, দুই লিপি, বাংলার জন্য মেপে নেওয়া গুণক আর যে মাপের নিচে হরফ কখনো নামে না",
      "width": 1280,
      "height": 1900
    },
    {
      "path": "cards/foundations/space-and-shape.html",
      "name": "Space and shape",
      "name_bn": "ফাঁক ও আকার",
      "group": "Foundations",
      "subtitle": "A 4 px scale in ten steps, and four radii. Everything in the system sits on one of them.",
      "subtitle_bn": "দশ ধাপে ৪ পিক্সেলের একটি স্কেল আর চার রকম কোণের বাঁক — পদ্ধতির সবকিছু এর কোনো একটির উপর বসে",
      "width": 1280,
      "height": 1500
    },
    {
      "path": "cards/foundations/motion.html",
      "name": "Motion",
      "name_bn": "গতি",
      "group": "Foundations",
      "subtitle": "Two durations and three easing curves. Things that move may overshoot; things that only change colour never do.",
      "subtitle_bn": "দুটি সময়কাল আর তিনটি ইজিং বাঁক — যা নড়ে তা একটু বেশি এগিয়ে ফিরে আসতে পারে, যার শুধু রং বদলায় তা কখনো নয়",
      "width": 1280,
      "height": 1500
    },
    {
      "path": "cards/foundations/the-marks.html",
      "name": "The marks",
      "name_bn": "চিহ্ন",
      "group": "Foundations",
      "subtitle": "The mark in two weights, drawn in currentColor so it takes whatever theme it lands in.",
      "subtitle_bn": "চিহ্ন দুই ওজনে — currentColor দিয়ে আঁকা, তাই যে থিমে বসে সেই থিমের রং নিয়ে নেয়",
      "width": 1280,
      "height": 1400
    },
    {
      "path": "cards/foundations/accessibility.html",
      "name": "Accessibility",
      "name_bn": "অভিগম্যতা",
      "group": "Foundations",
      "subtitle": "Target sizes with the guidance each one comes from, the anatomy of the focus ring, and what happens in forced colours &mdash; the mode where the operating system replaces every colour with its own.",
      "subtitle_bn": "ছোঁয়ার জায়গার মাপ আর তার নির্দেশনার উৎস, ফোকাস রিঙের গড়ন, আর ফোর্সড কালার্স মোডে কী হয় — যেখানে অপারেটিং সিস্টেম নিজের রং বসিয়ে সব রং বদলে দেয়",
      "width": 1280,
      "height": 1700
    },
    {
      "path": "cards/components/button.html",
      "name": "Button",
      "name_bn": "বাটন",
      "group": "Components",
      "subtitle": "Four kinds, two sizes and an icon-only form, each with a label that says what will happen.",
      "subtitle_bn": "চার রকম, দুই মাপ আর শুধু আইকনের একটি রূপ — প্রতিটির লেখা বলে দেয় কী ঘটবে",
      "width": 1280,
      "height": 1500
    },
    {
      "path": "cards/components/input.html",
      "name": "Input",
      "name_bn": "ইনপুট",
      "group": "Components",
      "subtitle": "A label, an optional hint, and an error that says what happened and then what to do next.",
      "subtitle_bn": "ঘরের নাম, দরকারে একটি ইঙ্গিত, আর ভুল হলে যে বার্তা বলে কী হয়েছে আর তারপর কী করতে হবে",
      "width": 1280,
      "height": 1500
    },
    {
      "path": "cards/components/select.html",
      "name": "Select",
      "name_bn": "বাছাই তালিকা",
      "group": "Components",
      "subtitle": "A native select with a drawn arrow, so the arrow follows the theme instead of the operating system.",
      "subtitle_bn": "ব্রাউজারের নিজের সিলেক্ট, তিরটি আঁকা — তাই তির অপারেটিং সিস্টেমের নয়, থিমের রং নেয়",
      "width": 1280,
      "height": 1300
    },
    {
      "path": "cards/components/checkbox-radio.html",
      "name": "Checkbox and radio",
      "name_bn": "চেকবক্স ও রেডিও",
      "group": "Components",
      "subtitle": "Native controls at 24 px, wrapped in a label so the words are part of the target.",
      "subtitle_bn": "ব্রাউজারের নিজের চেকবক্স ও রেডিও, ২৪ পিক্সেল মাপে — লেখাটিও সঙ্গে জোড়া, তাই লেখায় ছুঁলেও কাজ হয়",
      "width": 1280,
      "height": 1500
    },
    {
      "path": "cards/components/textarea.html",
      "name": "Textarea",
      "name_bn": "লেখার ঘর",
      "group": "Components",
      "subtitle": "You can drag it taller but never wider, so the line length stays comfortable to read.",
      "subtitle_bn": "টেনে লম্বা করা যায়, চওড়া নয় — তাই লাইনের মাপ পড়ার মতো আরামেই থাকে",
      "width": 1280,
      "height": 1300
    },
    {
      "path": "cards/components/badge.html",
      "name": "Badge",
      "name_bn": "ব্যাজ",
      "group": "Components",
      "subtitle": "Five meanings, each carrying a glyph and a word so the colour is the third signal and never the only one.",
      "subtitle_bn": "পাঁচটি অর্থ, প্রতিটির সঙ্গে একটি প্রতীক ও একটি শব্দ — রং এখানে তৃতীয় সংকেত, কখনো একমাত্র নয়",
      "width": 1280,
      "height": 1200
    },
    {
      "path": "cards/components/card.html",
      "name": "Card",
      "name_bn": "কার্ড",
      "group": "Components",
      "subtitle": "A surface a step brighter than the page, with a shadow in the light theme and none in the dark ones.",
      "subtitle_bn": "পাতার চেয়ে এক ধাপ উজ্জ্বল একটি তল — আলো থিমে ছায়া পড়ে, অন্ধকার থিমে পড়ে না",
      "width": 1280,
      "height": 1200
    },
    {
      "path": "cards/components/alert.html",
      "name": "Alert",
      "name_bn": "বার্তা",
      "group": "Components",
      "subtitle": "Four kinds. Each says what happened, then what happens next, and never blames the reader.",
      "subtitle_bn": "চার রকম — প্রতিটি বলে কী হয়েছে, তারপর কী হবে, আর কখনো পাঠককে দোষ দেয় না",
      "width": 1280,
      "height": 1600
    },
    {
      "path": "cards/components/dialog.html",
      "name": "Dialog",
      "name_bn": "ডায়ালগ",
      "group": "Components",
      "subtitle": "A real dialog element over a dimmed backdrop, with the destructive action named rather than called OK.",
      "subtitle_bn": "ব্রাউজারের নিজের ডায়ালগ উপাদান, পিছনে আবছা পর্দা — যে কাজ আর ফেরানো যায় না তার নাম লেখা থাকে, শুধু OK নয়",
      "width": 1280,
      "height": 1200
    },
    {
      "path": "cards/components/table.html",
      "name": "Table",
      "name_bn": "টেবিল",
      "group": "Components",
      "subtitle": "Row headers, a caption saying what the numbers are, and a sideways scroll when the table is wider than the space.",
      "subtitle_bn": "সারির শিরোনাম, সংখ্যাগুলো কীসের তা বলা এক লাইনের পরিচয়, আর জায়গার চেয়ে চওড়া হলে পাশে সরিয়ে দেখা",
      "width": 1280,
      "height": 1200
    },
    {
      "path": "cards/components/tabs.html",
      "name": "Tabs",
      "name_bn": "ট্যাব",
      "group": "Components",
      "subtitle": "The selected tab is bold, underlined and marked with aria-selected. Three signals, one of which is a colour.",
      "subtitle_bn": "বাছাই করা ট্যাব মোটা হরফে, নিচে দাগ, আর aria-selected দিয়ে চিহ্নিত — তিনটি সংকেত, তার একটি রং",
      "width": 1280,
      "height": 1200
    },
    {
      "path": "cards/components/nav.html",
      "name": "Nav",
      "name_bn": "নেভিগেশন",
      "group": "Components",
      "subtitle": "Vertical and horizontal. The current item carries a bar, a heavier weight and aria-current.",
      "subtitle_bn": "খাড়া আর আড়াআড়ি — এখন যেখানে আছেন সেই অংশে একটি দাগ, ভারী হরফ আর aria-current",
      "width": 1280,
      "height": 1200
    },
    {
      "path": "cards/components/breadcrumb.html",
      "name": "Breadcrumb",
      "name_bn": "পথরেখা",
      "group": "Components",
      "subtitle": "The last item is not a link, because you are already on it.",
      "subtitle_bn": "শেষ ধাপটি লিংক নয়, কারণ আপনি এখন সেখানেই আছেন",
      "width": 1280,
      "height": 1000
    },
    {
      "path": "cards/components/toast.html",
      "name": "Toast",
      "name_bn": "টোস্ট",
      "group": "Components",
      "subtitle": "A short message with a dismiss button that has a name of its own, not only a cross.",
      "subtitle_bn": "ছোটো একটি বার্তা, সরানোর বাটনটির নিজের নাম আছে — শুধু একটি ক্রস নয়",
      "width": 1280,
      "height": 1200
    },
    {
      "path": "cards/components/empty-state.html",
      "name": "Empty state",
      "name_bn": "যখন কিছু নেই",
      "group": "Components",
      "subtitle": "Says what is missing, and then exactly what to do about it.",
      "subtitle_bn": "কী নেই তা বলে, তারপর ঠিক কী করতে হবে সেটাও বলে",
      "width": 1280,
      "height": 1300
    },
    {
      "path": "cards/components/code-block.html",
      "name": "Code block",
      "name_bn": "কোড ব্লক",
      "group": "Components",
      "subtitle": "Aninda Mono, a horizontal scroll rather than a wrap, and a copy button that says what it copies.",
      "subtitle_bn": "Aninda Mono হরফে, লাইন ভাঙে না — পাশে সরে যায়, আর কপি বাটনটি বলে কী কপি হবে",
      "width": 1280,
      "height": 1100
    },
    {
      "path": "cards/patterns/sign-in.html",
      "name": "Sign in",
      "name_bn": "প্রবেশ",
      "group": "Patterns",
      "subtitle": "One card, two fields, and an option for someone who has no password.",
      "subtitle_bn": "একটি কার্ড, দুটি ঘর, আর যার পাসওয়ার্ড নেই তার জন্যও একটি উপায়",
      "width": 1280,
      "height": 1500
    },
    {
      "path": "cards/patterns/settings.html",
      "name": "Settings",
      "name_bn": "সেটিংস",
      "group": "Patterns",
      "subtitle": "Grouped in fieldsets, with the destructive action kept apart and named.",
      "subtitle_bn": "ঘরগুলো দলে সাজানো, আর যে কাজ আর ফেরানো যায় না সেটি আলাদা রাখা, নাম ধরে লেখা",
      "width": 1280,
      "height": 1900
    },
    {
      "path": "cards/patterns/dashboard.html",
      "name": "Dashboard",
      "name_bn": "ড্যাশবোর্ড",
      "group": "Patterns",
      "subtitle": "Four figures, one table, and a note saying where the numbers came from.",
      "subtitle_bn": "চারটি সংখ্যা, একটি টেবিল, আর সংখ্যাগুলো কোথা থেকে এসেছে তা বলা একটি লাইন",
      "width": 1280,
      "height": 1900
    },
    {
      "path": "cards/patterns/docs-page.html",
      "name": "Docs page",
      "name_bn": "নির্দেশিকার পাতা",
      "group": "Patterns",
      "subtitle": "Breadcrumb, page navigation and prose held to a readable line length.",
      "subtitle_bn": "পথরেখা, পাতার ভিতরের নেভিগেশন, আর পড়ার মতো মাপে ধরে রাখা লেখা",
      "width": 1280,
      "height": 1900
    },
    {
      "path": "cards/patterns/landing.html",
      "name": "Landing",
      "name_bn": "প্রথম পাতা",
      "group": "Patterns",
      "subtitle": "A claim, the reason to believe it, and two ways forward.",
      "subtitle_bn": "একটি দাবি, সেটি বিশ্বাস করার কারণ, আর এগিয়ে যাওয়ার দুটি পথ",
      "width": 1280,
      "height": 1900
    },
    {
      "path": "cards/patterns/pricing.html",
      "name": "Pricing",
      "name_bn": "দাম",
      "group": "Patterns",
      "subtitle": "Three plans, with the recommended one marked by a badge and a word.",
      "subtitle_bn": "তিনটি প্যাকেজ, সুপারিশ করা প্যাকেজটির গায়ে একটি ব্যাজ আর একটি শব্দ",
      "width": 1280,
      "height": 1600
    },
    {
      "path": "cards/patterns/not-found.html",
      "name": "Not found",
      "name_bn": "পাতা পাওয়া যায়নি",
      "group": "Patterns",
      "subtitle": "Says the page is missing, then offers the pages most people were looking for.",
      "subtitle_bn": "পাতাটি নেই তা জানায়, তারপর মানুষ যেসব পাতা সবচেয়ে বেশি খোঁজেন সেগুলো দেখায়",
      "width": 1280,
      "height": 1300
    },
    {
      "path": "cards/patterns/form-with-validation.html",
      "name": "Form with validation",
      "name_bn": "যাচাইসহ ফর্ম",
      "group": "Patterns",
      "subtitle": "A summary at the top, an error under each field, and nothing lost.",
      "subtitle_bn": "উপরে এক জায়গায় সব ভুলের তালিকা, প্রতিটি ঘরের নিচে তার নিজের ভুল, আর কিছুই হারায় না",
      "width": 1280,
      "height": 1700
    }
  ]
},
};
