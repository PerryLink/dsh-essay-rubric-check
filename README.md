# dsh-essay-rubric-check — Essay rubric scoring sheet check on criterion scores, quotation evidence and score arithmetic

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

<!-- topblock:v1 -->
> **What it is** — Essay rubric scoring sheet check on criterion scores, quotation evidence and score arithmetic. It returns a list of what is inconsistent, where, and what to fix.
> **Who it is for** — teaching researchers and graders; no command line required.
> **What you give it** — the source material the check works on (a table, register or document); the original is never modified. Excel can be converted to JSON/YAML first, in chat if the platform supports it.
> **What it does not do** — no compliance verdict, no liability finding, no replacement for the reviewer; differences only.
> **How to start** — search "Teaching and Review Suite" in WorkBuddy / Coze (this check is one part of it; availability as listed); or:
> `dsh plugin --profile <name> add dsh-essay-rubric-check`
<!-- /topblock:v1 -->

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-essay-rubric-check?metric=downloads)](https://dshfind.com/en/plugins/PerryLink/dsh-essay-rubric-check?ref=badge)

`dsh-essay-rubric-check` reads one scoring sheet — the student header plus one row per criterion — and checks that sheet's own completeness, arithmetic and evidence trail: whether each criterion records a name or a level description, whether a score stays within that criterion's maximum, whether the criterion scores total the rubric's score, whether every scored criterion leaves a quoted excerpt, whether criterion numbers are unique, and whether the sheet names its student and rubric version.

## Install

```sh
dsh plugin --profile <name> add dsh-essay-rubric-check
dsh --profile <name> --dump-config | grep 'dsh-essay-rubric-check'
```

## What it looks like

![Workflow diagram for dsh-essay-rubric-check: document → rule pack → findings.](docs/assets/dsh-essay-rubric-check-flow.svg)

*Workflow overview: document → rule pack → findings. The examples below use the real command surface.*



## What it answers

### Examples

The table below is the example set: the first row is the detailed walkthrough, the remaining rows are short cases.

#### Detailed output

**Tool** `essay_rubric_check`

**Input**

~~~json
{"rows":[{"序号":"1","评分项":"","维度":"内容","等级描述":"","得分":"18", ...}]}
~~~
 
**Output**

~~~json
{
  "id": "dsh-essay-rubric-check.ER-001.de09b5a6",
  "ruleId": "ER-001",
  "severity": "warn",
  "locator": {
    "row": 1,
    "field": "criterion"
  },
  "found": "第 1 行 criterion、levelDesc 都为空",
  "expected": "criterion、levelDesc 至少应填写一项",
  "fix": "补填评分项与等级描述；本条只核对是否填写，不判断量表是否合理"
}
~~~

*Observed from `dsh-essay-rubric-check/tests/fixtures/ER-001/ER-001-unsafe.json; dsh-essay-rubric-check/tests/fixtures/ER-001/cases.json; dsh-essay-rubric-check/rules/essay-rubric-check.yaml; dsh-essay-rubric-check/tests/index.test.ts`*

| You ask | What it answers |
|---|---|
| One criterion carries a score above the maximum written for it. What happens? | `ER-002` compares `score` with `maxScore` and reports the row where the score exceeds the maximum. It only compares the two numbers, and it does not judge whether that score suits this essay: the plugin never sees the writing. |
| Why does the total rule appear in `skipped` instead of reporting anything? | `ER-003` ships deliberately unconfigured. Its expression points at a placeholder field, `dimensionRef`, so nothing is added up and the rule reports itself in `skipped`. Name your rubric's own dimension fields in `expression.fields`, or switch to summing the detail rows against the header total, and it runs. The plugin will not assume how your total is composed. |
| The same criterion number is used on two rows of the rubric. | `ER-005` reports a repeated value in `criterionNo`, because a duplicate makes a criterion look registered twice. It ignores whitespace when comparing. Scoring one dimension in bands is a legitimate shape: give each band its own number, or disable the rule. |
| A criterion has a score but no quoted excerpt from the writing. | `ER-004` reports that row: only where `score` is filled does it require `evidenceQuote`. It checks that the locating cell is filled, not that the quotation really comes from that essay — a plausible invented quotation passes this plugin. |
| Both the criterion name and its level description are blank. | `ER-001` requires at least one of `criterion` and `levelDesc` on a row and reports the row where both are empty. It only checks that one of them is filled, and does not judge whether the rubric's criteria are sound or its level descriptions apt. |
| The sheet header does not say which student it belongs to, or which rubric version was used. | `ER-006` requires the header to declare both `student` and `rubricVersion`, and reports the missing one, because scores cannot be attributed and rubric versions are not directly comparable. Both are header fields, checked once for the sheet rather than per row. If your form also records a marking date in the header, add `markedAt` to the rule's `fields`. |

## Standards it follows

| Document | Number | Cited by rules |
|---|---|---|
| 《普通高中语文课程标准》 | 现行版本与条号本次未核实 | ER-001, ER-002, ER-003, ER-005, ER-006 |
| 《普通高等学校招生全国统一考试评卷工作规定》 | 现行版本与条号本次未核实 | ER-004 |

**Boundary:** this plugin checks a **作文量表评分表** for arithmetic and evidence — that each criterion names
itself and its level description, that a score does not exceed the criterion's maximum, that the criteria total
the rubric's score, that **a scored criterion leaves a quoted excerpt from the writing**, that criterion numbers
are unique, and that the sheet names its student and rubric version. It does **not** decide whether the writing is
good, whether the score is right, whether the comment is apt, or whether a remark should be reviewed.

> ### ⚠️ Read this before trusting a citation in the report
>
> **`excerpt` status is per rule, not uniform.** Some rules quote the clause verbatim (`kind: direct`), some are derived from the principle of the cited articles (`kind: derived-from-principle`, capped at `warn`), and some use thresholds your institution configures (`kind: institutional-configuration`, capped at `info`). The pack never paraphrases a quotation: when the text was not obtained, the `excerpt` field says so and the reasoning lives in `note`; a test asserts that no rule claims a quotation it does not have. **For any rule still marked as not obtained, replace the `excerpt` with the real clause and raise `kind` to `direct` once the text is in hand.**
>
> The conclusion is the reviewer's: this plugin lists differences it can point to in the material and does not decide facts or compliance.

## Compatibility

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-rc.2`. `engines.dsh` is declared as `>=0.2.1-0 <0.3.0` and is enforced by the host since 0.2.1 |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native` and `ptc`; for a marking batch use `ptc` |

## What it does

Registers the `essay_rubric_check` tool. It reads one scoring sheet — the student header plus one row per
criterion — applies a versioned rule pack, and returns a report.

| Rule | Check | Severity | Basis kind |
|---|---|---|---|
| `ER-001` | the criterion and its level description are recorded | warn | principle |
| `ER-002` | a score does not exceed the criterion's maximum | warn | principle |
| `ER-003` | the criteria total the rubric score (unconfigured by default) | warn | principle |
| `ER-004` | a scored criterion leaves a quoted excerpt | warn | principle |
| `ER-005` | criterion numbers are unique | warn | principle |
| `ER-006` | the sheet names its student and rubric version | warn | principle |

## Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `rulesFile` | string | `rules/essay-rubric-check.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

Rule-level parameters worth knowing:

- `ER-003` `expression` — **must be configured before it does anything.** Either name your dimension fields
  (`{ "op": "sum", "fields": ["contentScore", "languageScore"] }`) or sum the detail lines against a header
  total; the shipped expression points at a placeholder and computes nothing.
- `ER-002` `leftField` / `rightField` / `relation` — the comparison, `score <= maxScore` by default.
- `ER-004` `conditionField` / `requiredFields` — what triggers the quotation requirement.

## Material format

The tool accepts JSON or YAML:

```yaml
student: 某某考生
assignment: 某某作文题
rubricName: 某某作文评分量表
rubricVersion: 2026 版
totalScore: '18'
fullScore: '20'
markedAt: 2026-04-10
rows:
  - { 序号: '1', 评分项: 内容, 分值: '20',
      等级描述: 切合题意，中心突出，内容充实，感情真挚（一类卷 17—20 分）,
      得分: '18', 原文定位: '"他把那盏灯擦了三遍，直到玻璃上映出自己的影子。"',
      所在段落: 第 4 段, 评语: 以细节支撑情感，内容充实，符合一类卷标准。, 评分人: 王老师 }
```

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the sheet's own column
names are kept, so a finding names the column it read.

## Rule sources

Rule data lives in `rules/essay-rubric-check.yaml`. The pack's header states the citation gap in full, and each
rule's `note` repeats the part that matters for that rule. The load-time guard that normally enforces "an excerpt
must be a real quotation of at least eight characters" cannot tell a quotation from a description — so this pack
leans on the header, the per-rule notes and a test that asserts every `excerpt` admits the gap.

## Troubleshooting

- **`ER-003` reports itself as skipped.** Its expression still points at the placeholder field. Configure the
  dimension fields or the line-sum form — the plugin will not assume your total's composition.
- **`ER-004` passed an invented quotation.** It checks that a quotation is *present*, never that it appears in the
  essay. Comparing needs the essay, which the plugin does not see.
- **`ER-004` fires on a criterion that needs no quotation.** Disable the rule, or split that criterion into a
  rubric of its own.
- **`ER-002` fires on a score equal to the maximum.** Equality is allowed; a finding means the score is larger.
- **`ER-005` fires on two rows for one dimension.** Band rows within a dimension are legitimate — number them
  apart.
- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and
  that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if
  your runtime sits outside it, grant an explicit exemption:
  `dsh plugin --profile <name> allow-version dsh-essay-rubric-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer
  range that predates the 0.2 line. The runtime enforces peer compatibility at install time, so the
  declared range is the correct one; this is a known upstream issue in `dsh-plugin-dev`.

## Development

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, the shared table-plugin suite plus paired fixtures
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
node ../scripts/sync-shared.mjs dsh-essay-rubric-check   # refresh src/shared from ../_shared
```

The plugin is **data-only**: `src/model.ts` declares the table shape, the shared kit supplies the reader and the
check engine, and the rule pack declares every check.

## PerryLink DSH Plugin Family

Full family index: [choose a checker by material](https://perrylink.github.io/zh/checkers/choose/) and [all plugins](https://github.com/PerryLink). This repository is one of them.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-essay-rubric-check contributors.
