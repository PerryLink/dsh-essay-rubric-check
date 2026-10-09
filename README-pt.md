# dsh-essay-rubric-check — Verificação da folha de rubrica de redação sobre pontuações, citações de localização e aritmética

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-essay-rubric-check` lê uma folha de pontuação —o cabeçalho do aluno mais uma linha por critério— e verifica a completude, a aritmética e o rasto de evidência dessa própria folha: se cada critério regista um nome ou uma descrição de nível, se uma pontuação não excede o máximo desse critério, se as pontuações dos critérios somam a pontuação da rubrica, se cada critério pontuado deixa uma citação textual, se os números de critério não se repetem e se a folha declara o seu aluno e a sua versão de rubrica.

## Como é a saída

![Terminal demo of dsh-essay-rubric-check: real output over its ER-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-essay-rubric-check/main/docs/assets/dsh-essay-rubric-check-demo.png)

Saída real deste plugin sobre o seu próprio fixture de teste `ER-001` — não é uma simulação. O pacote de regras não inventa citações, por isso cada achado nomeia a cláusula aplicada e avisa que o seu texto não foi obtido.

## O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Um critério tem uma pontuação acima do máximo escrito para ele. O que acontece? | `ER-002` compara `score` com `maxScore` e assinala a linha em que a pontuação excede o máximo. Compara apenas esses dois números e não julga se essa pontuação é adequada a esta redação: o plugin nunca vê o texto. |
| Porque é que a regra do total aparece em `skipped` em vez de reportar algo? | `ER-003` é entregue deliberadamente por configurar. A sua expressão aponta para um campo de preenchimento, `dimensionRef`, pelo que nada é somado e a regra reporta-se a si mesma em `skipped`. Indique os campos de dimensão da sua própria rubrica em `expression.fields`, ou mude para somar as linhas de detalhe contra o total do cabeçalho, e ela é executada. O plugin não assume como o seu total é composto. |
| O mesmo número de critério aparece em duas linhas da rubrica. | `ER-005` reporta um valor repetido em `criterionNo`, porque uma duplicação faz um critério parecer registado duas vezes. Ao comparar, ignora os espaços em branco. Pontuar uma dimensão por escalões é uma forma legítima: dê a cada escalão o seu próprio número, ou desative a regra. |
| Um critério tem pontuação mas nenhuma citação textual do texto. | `ER-004` reporta essa linha: só quando `score` está preenchido é que exige `evidenceQuote`. Verifica que a célula de localização está preenchida, não que a citação venha realmente dessa redação: uma citação inventada mas verosímil passa neste plugin. |
| Estão vazios tanto o nome do critério como a sua descrição de nível. | `ER-001` exige pelo menos um de `criterion` e `levelDesc` numa linha e reporta a linha em que ambos estão vazios. Apenas verifica que um deles está preenchido e não julga se os critérios da rubrica são sólidos nem se as suas descrições de nível são adequadas. |
| O cabeçalho da folha não diz a que aluno pertence nem que versão da rubrica foi usada. | `ER-006` exige que o cabeçalho declare `student` e `rubricVersion`, e reporta o que faltar, porque as pontuações não podem ser atribuídas e as versões da rubrica não são diretamente comparáveis. Ambos são campos de cabeçalho, verificados uma vez para a folha e não linha a linha. Se o seu formulário também registar no cabeçalho uma data de correção, acrescente `markedAt` aos `fields` da regra. |

## Normas que segue

| Documento | Número | Regras que o citam |
|---|---|---|
| 《普通高中语文课程标准》 | 现行版本与条号本次未核实 | ER-001, ER-002, ER-003, ER-005, ER-006 |
| 《普通高等学校招生全国统一考试评卷工作规定》 | 现行版本与条号本次未核实 | ER-004 |

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

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-alpha.1`. **`engines.dsh` não é declarado**: não tem leitor e não pode recusar nenhum host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native`, `ptc` e `both`; para um diretório inteiro use `ptc` |

## What it does

A tabela de regras, os campos e o comportamento detalhado estão em [README.md](README.md#what-it-does) (versão principal em inglês). O plugin apenas lista divergências literais frente às cláusulas citadas e indica em `skipped` cada verificação que não pôde ser executada.

## Install

```sh
dsh plugin --profile <name> add dsh-essay-rubric-check
dsh --profile <name> --dump-config | grep 'dsh-essay-rubric-check'
```

## Configuration

Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem editar código; os limites por regra ficam no pacote de regras sob `rules/`.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/essay-rubric-check.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta |

## Material format

Aceita JSON ou YAML. O exemplo completo de campos está em [README.md](README.md#material-format) (versão principal em inglês). Os campos são opcionais na camada de leitura e validados pelo motor, de modo que uma exportação parcial gera achados sobre o que falta em vez de falhar.

## Rule sources

Os dados das regras ficam separados do código: cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e URL de origem. O carregador impõe que o trecho seja citação real de pelo menos oito caracteres e que uma verificação baseada apenas em princípio geral (`kind: derived-from-principle`, teto `warn`) ou em política local (`kind: institutional-configuration`, teto `info`) nunca seja declarada `error`.

Os limites verificados e as conclusões deliberadamente **não** afirmadas estão em [README.md](README.md#rule-sources) (versão principal em inglês) e em `rules/evidence/`.

## Troubleshooting

- **O plugin instala mas a ferramenta não aparece**: confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou.
- **`dsh plugin add` recusa o pacote**: a faixa de peers cobre `0.1.x` e `0.2.x`; fora dela, conceda isenção explícita com `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Uma regra não executou**: leia o arranjo `skipped`.
- **`check` informa `manifest-peers` como falha**: problema conhecido do `dsh-plugin-dev`; o runtime aplica a compatibilidade na instalação.
- **Os horários parecem deslocados**: toda a aritmética é de hora local sobre as cadeias fornecidas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-essay-rubric-check
```

O último comando copia o kit compartilhado de `../_shared` para `src/shared/`; execute-o novamente após cada alteração compartilhada.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-essay-rubric-check contributors.
