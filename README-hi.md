# dsh-essay-rubric-check — निबंध रूब्रिक अंकन-पत्र की जाँच, अंकों, उद्धरण-प्रमाण और अंकगणित पर

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-essay-rubric-check` एक अंकन-पत्र पढ़ता है — छात्र का हेडर और प्रत्येक कसौटी की एक पंक्ति — और उसी पत्र की पूर्णता, अंकगणित तथा प्रमाण-श्रृंखला जाँचता है: क्या प्रत्येक कसौटी में नाम या स्तर-विवरण दर्ज है, क्या कोई अंक उस कसौटी के अधिकतम से अधिक नहीं है, क्या कसौटियों के अंकों का जोड़ रूब्रिक के कुल अंक के बराबर है, क्या हर अंकित कसौटी कोई उद्धृत अंश छोड़ती है, क्या कसौटी-क्रमांक दोहराए नहीं गए हैं, और क्या पत्र में छात्र तथा रूब्रिक संस्करण घोषित हैं।

## आउटपुट कैसा दिखता है

![Terminal demo of dsh-essay-rubric-check: real output over its ER-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-essay-rubric-check/main/docs/assets/dsh-essay-rubric-check-demo.png)

इस प्लगइन का अपने ही `ER-001` टेस्ट फ़िक्स्चर पर वास्तविक आउटपुट — कोई नकली चित्र नहीं। नियम-पैक उद्धरण नहीं गढ़ता, इसलिए हर निष्कर्ष लागू किए गए खंड का नाम और यह भी बताता है कि उसका मूल पाठ इस बार प्राप्त नहीं हुआ।

## यह किन सवालों का जवाब देता है

| आपका सवाल | इसका जवाब |
|---|---|
| किसी कसौटी में उसके लिए लिखे अधिकतम से अधिक अंक दर्ज है। क्या होता है? | `ER-002` `score` की तुलना `maxScore` से करता है और जिस पंक्ति में अंक अधिकतम से अधिक है उसे दर्ज करता है। यह केवल उन दोनों संख्याओं की तुलना करता है और यह नहीं आँकता कि वह अंक इस निबंध के अनुरूप है या नहीं: यह प्लगइन निबंध को कभी नहीं देखता। |
| कुल-अंक वाला नियम कुछ बताने के बजाय `skipped` में क्यों आता है? | `ER-003` जानबूझकर बिना कॉन्फ़िगर भेजा गया है। उसका व्यंजक एक प्लेसहोल्डर फ़ील्ड `dimensionRef` की ओर संकेत करता है, इसलिए कुछ भी जोड़ा नहीं जाता और नियम स्वयं को `skipped` में दर्ज करता है। अपने रूब्रिक के आयाम-फ़ील्ड `expression.fields` में लिखें, या विवरण-पंक्तियों का जोड़ हेडर के कुल अंक से मिलाने का तरीका चुनें, तब यह चलता है। यह प्लगइन यह नहीं मान लेता कि आपका कुल अंक किन चीज़ों से बनता है। |
| रूब्रिक की दो पंक्तियों में एक ही कसौटी-क्रमांक है। | `ER-005` `criterionNo` में दोहराया गया मान दर्ज करता है, क्योंकि दोहराव से एक कसौटी दो बार दर्ज दिखती है। तुलना करते समय यह श्वेत-स्थान छोड़ देता है। एक ही आयाम को श्रेणियों में अंकित करना सामान्य है: हर श्रेणी को अलग क्रमांक दें, या इस नियम को बंद कर दें। |
| किसी कसौटी में अंक है, पर लेख से कोई उद्धृत अंश नहीं। | `ER-004` उस पंक्ति को दर्ज करता है: केवल जब `score` भरा हो, तब वह `evidenceQuote` की अपेक्षा करता है। यह देखता है कि स्थान-निर्देश वाला खाना भरा है, यह नहीं कि उद्धरण वास्तव में उसी निबंध से है — मनगढ़ंत पर विश्वसनीय लगता उद्धरण इस प्लगइन से पास हो जाता है। |
| कसौटी का नाम और उसका स्तर-विवरण, दोनों खाली हैं। | `ER-001` एक पंक्ति में `criterion` और `levelDesc` में से कम से कम एक की अपेक्षा करता है और जिस पंक्ति में दोनों खाली हैं उसे दर्ज करता है। यह केवल देखता है कि इनमें से एक भरा है, और यह नहीं आँकता कि रूब्रिक की कसौटियाँ ठोस हैं या उनके स्तर-विवरण उपयुक्त हैं। |
| पत्र के हेडर में न यह लिखा है कि यह किस छात्र का है, न यह कि कौन-सा रूब्रिक संस्करण प्रयुक्त हुआ। | `ER-006` हेडर में `student` और `rubricVersion` दोनों घोषित होने की अपेक्षा करता है और जो छूटा हो उसे दर्ज करता है, क्योंकि अंकों का श्रेय नहीं दिया जा सकता और रूब्रिक संस्करण सीधे तुलनीय नहीं होते। ये दोनों हेडर-फ़ील्ड हैं, जो पूरे पत्र के लिए एक बार जाँचे जाते हैं, पंक्ति-दर-पंक्ति नहीं। यदि आपके प्रपत्र में हेडर में जाँच-तिथि भी दर्ज होती है, तो नियम के `fields` में `markedAt` जोड़ दें। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
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

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-alpha.1` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` जानबूझकर घोषित नहीं**: इसका कोई पाठक नहीं और यह किसी होस्ट को अस्वीकार नहीं कर सकता |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native`, `ptc` और `both` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Install

```sh
dsh plugin --profile <name> add dsh-essay-rubric-check
dsh --profile <name> --dump-config | grep 'dsh-essay-rubric-check'
```

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/essay-rubric-check.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-essay-rubric-check
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## License

[Apache License 2.0](LICENSE) © 2026 dsh-essay-rubric-check contributors.
