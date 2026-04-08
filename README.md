<div align="center">

<h1>洗头佬.skill</h1>

<p><strong>一个兼容 <code>skills.sh</code> 的强势人格与历史分析双轨技能仓库</strong></p>

<p>主打一个虚构强势人格：短、狠、直接、第一人称。</p>
<p><strong>默认零启动安装；需要历史材料时，再切换到历史分析与本地书库增强技能。</strong></p>
<p><em>像指挥官一样说话。像产品一样即装即用。</em></p>

<p>
  <img alt="skills.sh compatible" src="https://img.shields.io/badge/skills.sh-compatible-111111?style=for-the-badge">
  <img alt="zero setup" src="https://img.shields.io/badge/zero--setup-default-0f766e?style=for-the-badge">
  <img alt="multi skill matrix" src="https://img.shields.io/badge/multi--skill-matrix-9a3412?style=for-the-badge">
  <img alt="first person persona" src="https://img.shields.io/badge/first--person-persona-1d4ed8?style=for-the-badge">
</p>

<p>
  <a href="https://github.com/guojia1698/hitler-quote-interview-skill/actions/workflows/python-tests.yml"><img alt="Tests" src="https://github.com/guojia1698/hitler-quote-interview-skill/actions/workflows/python-tests.yml/badge.svg"></a>
  <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
</p>

<p><a href="./README.md">中文</a> · <a href="./README.en.md">English</a></p>

<p><code>Codex</code> · <code>Claude Code</code> · <code>OpenClaw</code> · <code>skills.sh</code> 生态工具</p>

<p><sub>Zero-setup by default. First-person persona first. Historical depth on demand.</sub></p>

</div>

---

> 这是一个双轨 skill 仓库：主轨是虚构强势人格，副轨是历史分析。默认首页推荐的是前者。

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill iron-will-commander
```

| 第一人称 | 零启动可用 | 历史副轨 |
| --- | --- | --- |
| 更像虚构指挥官人格，不像解释器 | 安装后直接可用 | 需要时再切换到历史分析 skill |

**为什么它更像成品**

- 首屏安装即可用，不需要先启动本地服务
- 默认回答是单段第一人称人格回复，不是说明书体
- 虚构人格和历史分析分轨，减少风格串味
- 要出处时再装历史副轨，不强迫每轮都带解释
- 需要更深书证时，再切到本地语料增强 skill

**效果示例**

```text
Q: 生活太累了，指挥官。你在生活累的时候怎么办？
A: 我不和疲惫谈判。我先砍掉噪音，只留下最重要的一件事，然后把它做完。累不是命令，目标才是命令。
```

```text
Q: 如果遇到工作上的难题，你会怎么想？
A: 我先砍掉模糊。我不问它难不难，我问它卡在哪一步。把问题切开，先拿下第一段，后面的路自然会露出来。
```

这个仓库现在提供两类能力：
- `iron-will-commander`：虚构第一人称强势人格，适合短、狠、直接的对话体验
- `hitler-quote-interview` 及其扩展：历史分析、副轨出处核验、本地书证增强

默认推荐前者；如果你需要历史问题、出处问题或私有书籍检索，再装后两类。

## 适用问题

适合处理以下问题：
- 想要一个强势、冷硬、第一人称、命令式的虚构 persona 跟你对话
- 想要短句、高压、执行导向、低解释密度的回复
- 需要另装历史分析 skill 来处理传记、出处、影视与史料问题

主技能不绑定任何真实政治人物或意识形态；它只是一个虚构强势人格工具。

## Skill 矩阵

| Skill | 模式 | 用途 |
| --- | --- | --- |
| `iron-will-commander` | 零启动 | 默认入口。生成虚构强势人格的第一人称短回复。 |
| `hitler-quote-interview` | 零启动 | 历史分析副轨。生成“访谈式历史重建”回答。 |
| `hitler-quote-interview-source-attribution` | 零启动 | 专门处理语录出处、误引、史家分歧和引用格式。 |
| `hitler-quote-interview-local-corpus` | 本地增强 | 连接你自己的私有书库，返回更强的章节级或页码级证据。 |

## 安装

安装默认技能：

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill iron-will-commander
```

安装历史分析技能：

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

安装 `iron-will-commander` 后即可直接使用。默认行为是：
- 跟随用户输入语言作答
- 直接进入第一人称 persona
- 默认只给一段短回复
- 口吻强势、冷硬、执行导向
- 用户连续追问时保持人格连续性

示例问题：

```text
生活太累了，指挥官。你在生活累的时候怎么办？
```

```text
If I hit a hard problem at work, what do you do first?
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

两条能力轨的输出边界不同：
- `iron-will-commander`：允许第一人称，但只能是虚构 persona，不绑定真实政治人物或意识形态。
- `hitler-quote-interview` 及其扩展：保持历史分析口径，不做第一人称人物代言。
- 所有 skill 都必须跟随用户语言。
- 所有 skill 都拒绝仇恨、暴力、犯罪、自残鼓励和极端主义动员。

## 仓库结构

```text
.
├── README.md
├── README.en.md
├── skills/
│   ├── iron-will-commander/
│   ├── hitler-quote-interview/
│   ├── hitler-quote-interview-source-attribution/
│   └── hitler-quote-interview-local-corpus/
├── tests/
├── evals/
└── .github/workflows/
```

说明：
- `skills/iron-will-commander/` 是默认安装入口，走虚构第一人称 persona 模式。
- `skills/hitler-quote-interview/` 是历史分析副轨。
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
- 虚构 persona skill 的第一人称与触发约束
- `EPUB` / `PDF` 导入
- 索引构建与跨语种链接
- biography / rhetoric / media / unsafe_roleplay 路由
- skill 矩阵结构与零启动说明

## License

本项目采用 [MIT License](./LICENSE)。
