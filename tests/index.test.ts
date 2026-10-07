import { describeTablePlugin } from './table-plugin-suite.ts'
import { Config } from '../src/config.ts'
import { parseMaterial, runCheck, SPEC } from '../src/model.ts'
import { buildView } from '../src/view.ts'
import { inject, name, resolvePackageFile, TOOL_NAME } from '../src/index.ts'

describeTablePlugin({
  name,
  inject,
  TOOL_NAME,
  resolvePackageFile,
  Config,
  rulesFile: 'rules/essay-rubric-check.yaml',
  parseMaterial,
  runCheck,
  buildView,
  columnNames: SPEC.columns,
  samples: {
    good: {
          "student": "某某考生",
          "assignment": "某某作文题",
          "rubricName": "某某作文评分量表",
          "rubricVersion": "2026 版",
          "totalScore": "18",
          "fullScore": "20",
          "markedAt": "2026-04-10",
          "rows": [
                {
                      "序号": "1",
                      "评分项": "内容",
                      "维度": "内容",
                      "分值": "20",
                      "等级描述": "切合题意，中心突出，内容充实，感情真挚（一类卷 17—20 分）",
                      "得分": "18",
                      "原文定位": "\"他把那盏灯擦了三遍，直到玻璃上映出自己的影子。\"",
                      "所在段落": "第 4 段",
                      "评语": "以细节支撑情感，内容充实，符合一类卷标准。",
                      "评分人": "王老师",
                      "是否需要复核": "否"
                }
          ]
    },
    unknownColumn: { rows: [{ 备注: '甲' }] },
  },
})
