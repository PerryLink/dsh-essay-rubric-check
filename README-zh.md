# dsh-essay-rubric-check — 作文量表评分核对（按评分项、原文定位与分值算术核对评分自洽）

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

<!-- topblock:v1 -->
> **这是什么**　作文量表评分核对。输出一份「哪一行、哪一栏、差什么」的清单。
> **给谁用**　教研员、语文教师、阅卷组；不用懂命令行。
> **你交什么**　这项核对用到的原始材料（表格、清单或文书）；不改原件。Excel 可先转成 JSON/YAML，对话里也能代转。
> **它不做什么**　不判合规、不认定责任、不替代审核人；只列材料内部能逐条指认的差异。
> **怎么开始**　在 WorkBuddy / 扣子搜「教学与点评核对包」（本检查是其中一项；上架以商城为准）；或命令行：
> `dsh plugin --profile <name> add dsh-essay-rubric-check`
<!-- /topblock:v1 -->

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-essay-rubric-check?metric=downloads)](https://dshfind.com/en/plugins/PerryLink/dsh-essay-rubric-check?ref=badge)

`dsh-essay-rubric-check` 读取一份作文量表评分表——学生表头加每个评分项一行——核对这张评分表自身的齐备、算术与依据：每个评分项是否填写了名称或等级描述、得分是否不超过该项分值、各评分项得分合计是否等于量表总分、给出得分的评分项是否留下原文定位、评分项序号是否唯一、表头是否声明学生与量表版本。

## Install

```sh
dsh plugin --profile <name> add dsh-essay-rubric-check
dsh --profile <name> --dump-config | grep 'dsh-essay-rubric-check'
```

## 实际输出长什么样

![dsh-essay-rubric-check 工作流图：文档 → 规则包 → 核对结果。](docs/assets/dsh-essay-rubric-check-flow.svg)

*工作流概览：文档 → 规则包 → 核对结果。下面的示例使用实际命令面。*


本插件对自己 `ER-001` 测试夹具的**真实输出**，不是示意图。规则库不伪造引文，因此每条发现都会同时写明所引条款，以及该条款原文本次未取得。

## 它回答什么问题

### 示例

下表是示例集：第一行是详细走查，其余行是简短案例。


#### 详细输出

**工具** `essay_rubric_check`

**输入**

~~~json
{"rows":[{"序号":"1","评分项":"","维度":"内容","等级描述":"","得分":"18", ...}]}
~~~
 
**输出**

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

*来源 `dsh-essay-rubric-check/tests/fixtures/ER-001/ER-001-unsafe.json; dsh-essay-rubric-check/tests/fixtures/ER-001/cases.json; dsh-essay-rubric-check/rules/essay-rubric-check.yaml; dsh-essay-rubric-check/tests/index.test.ts`*

| 你会问 | 它怎么答 |
|---|---|
| 某一项的得分超过了该项写明的分值，会怎样？ | `ER-002` 比较 `score` 与 `maxScore`，得分超过该项分值的行会被报出。它只比较这两个数，不判断这个分数与这篇作文是否相称：本插件看不到作文本身。 |
| 为什么合计那条规则出现在 `skipped` 里，什么都不报？ | `ER-003` 出厂即有意留白：算式指向占位字段 `dimensionRef`，因此不加总任何数，本条报告自己进了 `skipped`。把本机构量表的维度字段填进 `expression.fields`，或改为按明细行求和并与表头总分核对，它就会执行。本插件不替使用方假定总分的构成。 |
| 量表里两行用了同一个评分项序号。 | `ER-005` 会报出 `criterionNo` 的重复值，因为重复会让一个评分项看起来登记了两次。比较时忽略空白字符。同一维度分档打分是正常情形：请给每一档不同的序号，或停用本条。 |
| 某一项打了分，却没有摘录学生原句作为定位。 | `ER-004` 会报出该行：只有在 `score` 已填写时，它才要求 `evidenceQuote`。它核对定位栏是否填写，不核对所引原文是否真的出自该作文——编得像样的引文能通过本插件。 |
| 评分项名称与等级描述两栏都是空的。 | `ER-001` 要求一行至少填写 `criterion` 与 `levelDesc` 之一，两栏皆空的行会被报出。它只核对是否填了其中之一，不判断量表的分项设置是否科学、等级描述是否恰当。 |
| 评分表表头没有写明是哪个学生，也没写用的是哪一版量表。 | `ER-006` 要求表头声明 `student` 与 `rubricVersion`，缺哪个报哪个，因为分数无法归属，而量表换版时分数不可直接比较。这两项都是表头字段，按整张评分表核对一次，不逐行核对。若本机构表式还在表头记录评阅日期，把 `markedAt` 加进本条的 `fields` 即可。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
|---|---|---|
| 《普通高中语文课程标准》 | 现行版本与条号本次未核实 | ER-001, ER-002, ER-003, ER-005, ER-006 |
| 《普通高等学校招生全国统一考试评卷工作规定》 | 现行版本与条号本次未核实 | ER-004 |

**边界（中文译文，以英文原文为准）：** 本插件核对一份 **作文量表评分表** 的算术与证据——每个评分项是否写明名称与等级描述，得分是否不超过该项分值，各评分项得分合计是否等于量表总分，**给出得分的评分项是否留有摘自作文的引文**，评分项序号是否唯一，以及表格是否写明学生与量表版本。它**不**判定作文是否写得好、分数是否正确、评语是否恰当，也不判定某条评语是否应当复核。

> ### ⚠️ 本插件能做什么、不能做什么（以英文原文为准）
>
> **它从不看作文本身。** 因此它能核对一个分数是否*指向*一条引文——但从不能核对这条引文是否出自那篇作文，也从不能核对这个分数是否与那篇作文相称。`ER-004` 的说明写明了这一点，故障排查一节也重申：编得像样的虚构引文能通过本插件。
>
> **`ER-003` 出厂即有意留白。** “哪些行加总等于总分”取决于你的量表如何划分维度——内容 / 结构 / 语言 / 书写，或者别的划分方式——因此算式只指向一个占位字段，**不计算任何数**。把 `expression.fields` 改为你量表的维度字段，或改为按明细行求和并与表头总分核对，这条规则就会执行；否则它报告自己进了 `skipped`。**本插件不会假定你的总分如何构成。**
>
> 要求每个已评分的评分项都附一条引文，反映的是一条编辑规则——评分应可复核——而不是标准中的某条引文。正因如此，`ER-004` 是 `warn`，其说明也解释了如何放宽它：如果你量表中的某些维度不需要引文，就停用该规则，或把这些维度拆分出去。
>
> **规则库中的每一条 `excerpt` 都明确写着：本次未取得条款原文。** 该制度见于语文课程标准、国家评卷规则和各校自己的评分量表。核验过程既未取得条款原文，也未取得任何评分量表，因此规则库把这一缺口写在 `excerpt` 字段本身，并把每条规则保持在 `warn` 或 `info`。**拿到原文后，请把每条 `excerpt` 替换为真实条款，并把 `kind` 提升为 `direct`。**

## Compatibility

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-rc.2`。**已声明 `engines.dsh`**：0.2.1 起由宿主单独裁决，范围为 `>=0.2.1-0 <0.3.0` |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/essay-rubric-check.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-essay-rubric-check
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## PerryLink DSH Plugin Family

完整清单（62 个核查器 + 通用插件）见 [按材料选核查器](https://perrylink.github.io/zh/checkers/choose/)；本仓只是其中一个。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-essay-rubric-check contributors.
