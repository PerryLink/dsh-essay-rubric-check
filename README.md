# dsh-essay-rubric-check

**Boundary:** this plugin checks a **作文量表评分表** for arithmetic and evidence — that each criterion names
itself and its level description, that a score does not exceed the criterion's maximum, that the criteria total
the rubric's score, that **a scored criterion leaves a quoted excerpt from the writing**, that criterion numbers
are unique, and that the sheet names its student and rubric version. It does **not** decide whether the writing is
good, whether the score is right, whether the comment is apt, or whether a remark should be reviewed.

> ### ⚠️ What this plugin can and cannot do
>
> **It never sees the essay.** So it can check that a score *points at* a quotation — never that the quotation
> comes from that essay, and never that the score suits the writing. `ER-004`'s note says so, and the
> troubleshooting section repeats it: a plausible invented quotation passes this plugin.
>
> **`ER-003` ships deliberately unconfigured.** "Which rows sum to the total" depends on how your rubric divides
> its dimensions — content / structure / language / handwriting, or something else — so the expression points at
> a placeholder field and **computes nothing**. Change `expression.fields` to your rubric's dimension fields, or
> switch to a line-sum + header total, and the rule runs; otherwise it reports itself in `skipped`. **The plugin
> will not assume your total's composition.**
>
> Requiring a quotation for every scored criterion reflects one editorial rule — that marking be reviewable —
> rather than a quotation from a standard. That is why `ER-004` is `warn` and why its note explains how to relax
> it: if some dimensions in your rubric need no quotation, disable the rule or split those dimensions out.
>
> **Every `excerpt` in the rule pack says, in so many words, that the clause text was not obtained.** The regime
> lives in the Chinese language curriculum standards, national marking rules and each school's own rubric. The
> verification pass retrieved neither the clause text nor any rubric, so the pack states the gap in the `excerpt`
> field itself and keeps every rule at `warn` or `info`. **When the texts are in hand, replace each `excerpt`
> with the real clause and raise `kind` to `direct`.**

## Compatibility

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-alpha.1`. `engines.dsh` is deliberately not declared: it has no reader and cannot reject a host |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native`, `ptc` and `both`; for a marking batch use `ptc` |

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

## Install

```sh
pnpm pack
dsh plugin --profile <name> add ./dsh-essay-rubric-check-0.1.0.tgz
dsh --profile <name> --dump-config | grep 'dsh-essay-rubric-check'
```

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

## License

[Apache License 2.0](LICENSE) © 2026 dsh-essay-rubric-check contributors.
