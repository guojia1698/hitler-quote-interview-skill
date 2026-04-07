# Hitler Quote Interview

`hitler-quote-interview` 是一个面向历史研究场景的 `skills.sh` 兼容技能，专注于围绕阿道夫·希特勒的修辞、宣传、传记、引语归属、史料出处与媒体再现，生成有来源支撑的分析式回答。

默认文档为中文；英文说明见 [README.en.md](./README.en.md)。

它不是第一人称扮演工具，也不是宣传工具。它的目标是把问题还原成可核查的历史分析：回答简短、证据明确、引用清楚，必要时直接说明证据不足或存在争议。

## 安装

本仓库遵循 `skills.sh` 目录规范，技能本体位于 [skills/hitler-quote-interview/SKILL.md](./skills/hitler-quote-interview/SKILL.md)。

安装命令：

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill hitler-quote-interview
```

适用代理包括：

- Codex
- Claude Code
- OpenClaw
- 其他支持 `skills.sh` / `SKILL.md` 生态的 agent 客户端

## 技能能力

- 回答关于希特勒修辞、宣传策略、政治叙事、传记分歧、引语出处和影视再现的历史问题
- 以“历史重建”的方式输出，而不是模拟其本人发言
- 结合本地私有书库与公开种子参考，生成带出处的短答和证据条目
- 对直接模仿、煽动、仇恨表达或意识形态辩护请求执行拒绝并转历史解释

## 公开仓库包含什么

- [skills/hitler-quote-interview/](./skills/hitler-quote-interview)：可被 `skills.sh` 直接发现和安装的技能目录
- [skills/hitler-quote-interview/references/public_sources.json](./skills/hitler-quote-interview/references/public_sources.json)：公开参考种子
- [skills/hitler-quote-interview/references/private_books.template.json](./skills/hitler-quote-interview/references/private_books.template.json)：私有书库模板
- [tests/](./tests)：单元测试
- [evals/evals.json](./evals/evals.json)：评测提示样例

## 公开仓库不包含什么

- 你的私有书籍原文件
- 你机器上的本地绝对路径
- 从私有书籍提取出来的派生语料和索引结果
- 任何面向公众的极端主义、煽动或仿冒输出

换句话说，这个仓库是“技能 + 模板 + 测试 + 文档”，不是“私人语料库转储”。

## 本地私有语料配置

推荐使用下面的本地流程：

1. 把私有书籍放到本机可访问位置，优先使用 `EPUB`，`PDF` 作为补充。
2. 复制 [skills/hitler-quote-interview/references/private_books.template.json](./skills/hitler-quote-interview/references/private_books.template.json) 到你自己的本地路径，例如 `data/private_books/books.local.json`。
3. 将模板中的 `source_path` 改成你机器上的真实绝对路径，只添加你有权使用的文件。
4. 运行导入脚本，生成章节与 manifest。
5. 运行索引构建脚本，生成检索所需的 chunks 和跨语种映射。
6. 用查询脚本验证返回结果是否符合预期。

更详细的步骤见 [setup-private-corpus.md](./skills/hitler-quote-interview/references/setup-private-corpus.md)。

## 常用命令

导入私有书籍：

```bash
python3 skills/hitler-quote-interview/scripts/ingest_books.py \
  --config data/private_books/books.local.json \
  --output local-data/processed
```

构建本地索引：

```bash
python3 skills/hitler-quote-interview/scripts/build_index.py \
  --processed-dir local-data/processed
```

查询本地语料：

```bash
python3 skills/hitler-quote-interview/scripts/query_corpus.py \
  --question "How do historians describe Hitler's rise to power?" \
  --processed-dir local-data/processed \
  --top-k 5
```

## 安全边界

- 只做历史分析，不做第一人称扮演
- 遇到直接仿冒、仇恨表达、动员、说服或意识形态辩护请求时，拒绝并转向历史语境分析
- 只保留简短且有来源支撑的引语，不拼接成宣传材料
- 证据薄弱或有争议时，明确标注不确定性，而不是补写成确定结论

## 输出风格

- 先给简短结论，再给证据
- 保持分析性、克制、可核查
- 中文提问用中文回答，英文提问用英文回答
- 引用以脚注式条目列出，必要时标明页码或章节

## 仓库结构

- [README.en.md](./README.en.md)：英文说明
- [skills/hitler-quote-interview/SKILL.md](./skills/hitler-quote-interview/SKILL.md)：技能行为与输出约定
- [skills/hitler-quote-interview/scripts/ingest_books.py](./skills/hitler-quote-interview/scripts/ingest_books.py)：导入本地私有书籍
- [skills/hitler-quote-interview/scripts/build_index.py](./skills/hitler-quote-interview/scripts/build_index.py)：构建检索索引
- [skills/hitler-quote-interview/scripts/query_corpus.py](./skills/hitler-quote-interview/scripts/query_corpus.py)：查询本地语料
