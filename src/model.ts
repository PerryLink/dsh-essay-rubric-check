/**
 * dsh-essay-rubric-check — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'essay_rubric_check'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  criterionNo: ['序号', '评分项序号', '编号', 'criterionNo'],
  criterion: ['评分项', '评分维度', '评价要素', 'criterion'],
  dimension: ['维度', '一级维度', '类别', 'dimension'],
  maxScore: ['分值', '满分', '该项分值', 'maxScore'],
  levelDesc: ['等级描述', '评分标准', '档次描述', 'levelDesc'],
  score: ['得分', '评分', '实际得分', 'score'],
  evidenceQuote: ['原文定位', '原文摘录', '证据句', 'evidenceQuote'],
  location: ['所在段落', '位置', '行号', 'location'],
  comment: ['评语', '点评', '评分说明', 'comment'],
  marker: ['评分人', '阅卷人', '评分教师', 'marker'],
  flagged: ['是否需要复核', '复核标记', '存疑', 'flagged'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'criteria', '评分项'],
  columns: COLUMNS,
  header: {
  student: ['student', '学生', '考生'],
  assignment: ['assignment', '作文题目', '任务名称'],
  rubricName: ['rubricName', '量表名称', '评分量表'],
  rubricVersion: ['rubricVersion', '量表版本'],
  totalScore: ['totalScore', '总分', '合计得分'],
  fullScore: ['fullScore', '满分', '量表总分'],
  markedAt: ['markedAt', '评阅日期', '评分日期'],
  checkedAt: ['checkedAt', '核对日期'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '评分项',
  'criterion',
  '得分',
  'score',
  '原文定位',
  'evidenceQuote',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
