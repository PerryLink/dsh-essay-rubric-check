# dsh-essay-rubric-check — Verificación de la hoja de rúbrica de ensayo sobre puntuaciones, citas de localización y aritmética

`dsh-essay-rubric-check` lee una hoja de puntuación —la cabecera del estudiante más una fila por criterio— y comprueba la completitud, la aritmética y el rastro de evidencia de esa propia hoja: que cada criterio registre un nombre o una descripción de nivel, que una puntuación no supere el máximo de ese criterio, que las puntuaciones de los criterios sumen la puntuación de la rúbrica, que todo criterio puntuado deje una cita textual, que los números de criterio no se repitan y que la hoja declare su estudiante y su versión de rúbrica.

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| Un criterio lleva una puntuación superior al máximo escrito para él. ¿Qué ocurre? | `ER-002` compara `score` con `maxScore` e informa de la fila en la que la puntuación supera el máximo. Solo compara esos dos números y no juzga si esa puntuación corresponde a este ensayo: el plugin nunca ve el texto. |
| ¿Por qué la regla del total aparece en `skipped` en lugar de informar de algo? | `ER-003` se entrega deliberadamente sin configurar. Su expresión apunta a un campo de relleno, `dimensionRef`, así que no suma nada y la regla se informa a sí misma en `skipped`. Indique los campos de dimensión de su propia rúbrica en `expression.fields`, o cambie a sumar las filas de detalle contra el total de la cabecera, y se ejecuta. El plugin no supone cómo se compone su total. |
| El mismo número de criterio aparece en dos filas de la rúbrica. | `ER-005` informa de un valor repetido en `criterionNo`, porque un duplicado hace que un criterio parezca registrado dos veces. Al comparar ignora los espacios en blanco. Puntuar una dimensión por bandas es una forma legítima: dé a cada banda su propio número, o desactive la regla. |
| Un criterio tiene puntuación pero ninguna cita textual del escrito. | `ER-004` informa de esa fila: solo cuando `score` está relleno exige `evidenceQuote`. Comprueba que la celda de localización esté rellena, no que la cita provenga realmente de ese ensayo: una cita inventada pero verosímil pasa este plugin. |
| Están vacíos tanto el nombre del criterio como su descripción de nivel. | `ER-001` exige al menos uno de `criterion` y `levelDesc` en una fila e informa de la fila en la que ambos están vacíos. Solo comprueba que uno de los dos esté relleno y no juzga si los criterios de la rúbrica son sólidos ni si sus descripciones de nivel son adecuadas. |
| La cabecera de la hoja no dice a qué estudiante pertenece ni qué versión de rúbrica se usó. | `ER-006` exige que la cabecera declare `student` y `rubricVersion`, e informa del que falte, porque las puntuaciones no se pueden atribuir y las versiones de rúbrica no son directamente comparables. Ambos son campos de cabecera, comprobados una vez para la hoja y no fila por fila. Si su formulario también registra en la cabecera una fecha de corrección, añada `markedAt` a los `fields` de la regla. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
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

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-essay-rubric-check
dsh --profile <name> --dump-config | grep 'dsh-essay-rubric-check'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/essay-rubric-check.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-essay-rubric-check
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-essay-rubric-check contributors.
