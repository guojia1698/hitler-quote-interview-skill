<div align="center">

<h1>洗头佬.skill</h1>

<p><strong>一个兼容 <code>skills.sh</code> 的历史研究技能矩阵</strong></p>

<p>用于生成带出处的“访谈式历史重建”回答。</p>
<p><strong>默认零启动安装，按需接入本地私有书库增强检索。</strong></p>
<p><em>像访谈一样说话，像史家一样举证。</em></p>

<p>
  <img alt="skills.sh compatible" src="https://img.shields.io/badge/skills.sh-compatible-111111?style=for-the-badge">
  <img alt="zero setup" src="https://img.shields.io/badge/zero--setup-default-0f766e?style=for-the-badge">
  <img alt="multi skill matrix" src="https://img.shields.io/badge/multi--skill-matrix-9a3412?style=for-the-badge">
  <img alt="archival interview mode" src="https://img.shields.io/badge/archival--interview-mode-1d4ed8?style=for-the-badge">
</p>

<p>
  <a href="https://github.com/guojia1698/hitler-quote-interview-skill/actions/workflows/python-tests.yml"><img alt="Tests" src="https://github.com/guojia1698/hitler-quote-interview-skill/actions/workflows/python-tests.yml/badge.svg"></a>
  <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
</p>

<p><a href="./README.md">中文</a> · <a href="./README.en.md">English</a></p>

<p><code>Codex</code> · <code>Claude Code</code> · <code>OpenClaw</code> · <code>skills.sh</code> 生态工具</p>

<p><sub>Zero-setup by default. Local corpus when you need stronger citations.</sub></p>

</div>

---

> 历史研究技能矩阵。默认输出更像“档案采访转录”而不是百科说明，但仍保持来源约束与历史边界。

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill hitler-quote-interview
```

| 对话感优先 | 零启动可用 | 本地书证增强 |
| --- | --- | --- |
| 更像档案访谈，不像论文摘要 | 安装后直接可用 | 需要时再接入私有书库 |

**效果示例**

```text
Q: 希特勒在魏玛晚期通常怎样攻击议会民主？
A: 复原回答：他通常会先把议会描成软弱、拖延和分裂的象征，再把危机包装成只有强力领导才能解决的问题。
   依据：[1] Ian Kershaw, Hitler 1889-1936: Hubris
```

```text
Q: 元首，我最近好累啊，怎么办？
A: 复原回答：如果按他惯常的公开政治话语来压缩成一句回答，他大概会把“疲惫”说成意志松弛，并要求用纪律、服从和所谓使命感去压过个人感受。
```

`hitler-quote-interview` 是一个兼容 `skills.sh` 的历史研究技能集合，用于围绕阿道夫·希特勒的修辞、宣传、传记、引语归属与媒体再现，生成可核查、带出处的分析式回答。

这个仓库现在分成两种使用模式：
- 零启动模式：安装后直接可用，不需要本地服务、数据库或索引进程。
- 本地语料增强模式：在你自己提供私有书籍的前提下，按需运行导入和检索脚本，补充更强的章节级书证。

## 适用范围

适合处理以下问题：
- 他的公开修辞如何组织、重复、放大情绪与神话化领袖形象
- 不同传记作者如何描述他的政治崛起、统治方式与历史后果
- 某句名言是否可靠、是否存在误引、应该如何标注出处
- 与希特勒相关的纪录片、影视再现、研究入口和史料导览

该技能不进行第一人称扮演，不生成宣传性内容；它只输出带证据的历史重建，并在证据不足或存在争议时明确说明不确定性。

## Skill 矩阵

| Skill | 模式 | 用途 |
| --- | --- | --- |
| `hitler-quote-interview` | 零启动 | 默认入口。生成“访谈式历史重建”回答，安装后直接可用。 |
| `hitler-quote-interview-source-attribution` | 零启动 | 专门处理语录出处、误引、史家分歧和引用格式。 |
| `hitler-quote-interview-local-corpus` | 本地增强 | 连接你自己的私有书库，返回更强的章节级或页码级证据。 |

## 安装

安装默认技能：

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill hitler-quote-interview
```

安装出处增强技能：

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill hitler-quote-interview-source-attribution
```

安装本地语料增强技能：

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill hitler-quote-interview-local-corpus
```

兼容对象包括 Codex、Claude Code、OpenClaw，以及其他支持 `skills.sh` / `SKILL.md` 生态的 agent 工具。

## 快速开始

### 1. 零启动模式

安装 `hitler-quote-interview` 后即可直接使用。默认行为是：
- 跟随用户输入语言作答
- 优先输出“访谈式历史复原回答”，而不是百科体说明
- 先给一段紧凑的对话感回答，再补来源或史家视角
- 明确标注这是“基于史料与研究的复原性概括”
- 遇到证据薄弱或争议问题时直接说明不确定性

示例问题：

```text
请用中文概括一下，1930年代希特勒是如何通过宣传和政治仪式塑造个人形象的？
```

```text
Explain in English how major biographers describe Hitler's rise to power.
```

### 2. 出处增强模式

如果你更关注“这句话到底是不是原话”“不同史家怎么看”，安装 `hitler-quote-interview-source-attribution`。

示例问题：

```text
“某某语录”真的是希特勒说的吗？如果不可靠，请说明它更像是后人概括还是二手转述。
```

```text
Compare how Kershaw and Ullrich frame Hitler's political style.
```

### 3. 本地语料增强模式

只有当你希望把私有书籍纳入检索时，才需要 `hitler-quote-interview-local-corpus`。它不需要常驻服务，但会在本地按需运行脚本。

1. 按 [private_books.template.json](./skills/hitler-quote-interview-local-corpus/references/private_books.template.json) 准备书籍配置。
2. 运行导入脚本生成 `books_manifest.json` 与 `sections.jsonl`。
3. 运行索引脚本生成 `chunks.jsonl`、`works_index.json` 和 `cross_language_links.json`。
4. 再用查询脚本取回候选证据块。

```bash
python3 skills/hitler-quote-interview-local-corpus/scripts/ingest_books.py \
  --config data/private_books/books.local.json \
  --output local-data/processed
```

```bash
python3 skills/hitler-quote-interview-local-corpus/scripts/build_index.py \
  --processed-dir local-data/processed
```

```bash
python3 skills/hitler-quote-interview-local-corpus/scripts/query_corpus.py \
  --question "How do historians describe Hitler's rise to power?" \
  --processed-dir local-data/processed \
  --top-k 5
```

更细的配置说明见 [setup-private-corpus.md](./skills/hitler-quote-interview-local-corpus/references/setup-private-corpus.md)。

## 输出契约

所有 skill 共享同一组输出边界：
- 回答必须跟随用户语言，中文问中文答，英文问英文答。
- 正文采用历史重建或史家概括的口径，不写成“我认为”“我命令”这类第一人称代言。
- 引语保持短、小、可溯源；当拿不准时，优先转述而不是硬给“原话”。
- 遇到直接模仿、动员、煽动、歧视或意识形态辩护请求时，拒绝并转历史分析。

## 仓库结构

```text
.
├── README.md
├── README.en.md
├── skills/
│   ├── hitler-quote-interview/
│   ├── hitler-quote-interview-source-attribution/
│   └── hitler-quote-interview-local-corpus/
├── tests/
├── evals/
└── .github/workflows/
```

说明：
- `skills/hitler-quote-interview/` 是默认安装入口，走零启动模式。
- `skills/hitler-quote-interview-source-attribution/` 专做出处与争议判断。
- `skills/hitler-quote-interview-local-corpus/` 负责接入本地私有书籍与检索脚本。
- `tests/`、`evals/` 和 `.github/workflows/` 用于验证与持续集成。

## 开发

本地开发依赖 `Python 3.10+`：

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
```

当前测试覆盖：
- `EPUB` / `PDF` 导入
- 索引构建与跨语种链接
- biography / rhetoric / media / unsafe_roleplay 路由
- skill 矩阵结构与零启动说明

## License

本项目采用 [MIT License](./LICENSE)。
