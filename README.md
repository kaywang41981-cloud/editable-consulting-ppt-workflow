# Editable Consulting PPT Workflow

A Codex skill for creating evidence-backed, template-faithful, native-editable PowerPoint presentations through a structured clarification, SVG approval, PPTX build, and QA workflow.

中文说明：这是一个用于制作专业咨询型 PowerPoint 的 Codex Skill。它强调保留用户提供的母版和版式，先通过 SVG 确认视觉方案，再使用原生文本、形状、表格和图表生成可编辑 PPTX，并完成结构与视觉 QA。

## Key principles

- Ask one clarification question at a time before production.
- Require a user-provided PPTX template for production work.
- Use SVG previews as visual specifications, not as flattened final slides.
- Preserve the source deck's masters, layouts, theme, headers, footers, logos, page numbers, and dimensions.
- Build slides with native-editable PowerPoint objects and embedded chart workbooks.
- Separate verified facts, third-party estimates, and hypotheses requiring validation.
- Treat Microsoft PowerPoint for macOS as the final acceptance environment.

## Installation

Clone this repository into your Codex skills directory:

```bash
git clone https://github.com/kaywang41981-cloud/editable-consulting-ppt-workflow.git ~/.codex/skills/editable-consulting-ppt-workflow
```

Restart Codex or begin a new task after installation so the skill can be discovered.

## Usage

Invoke the skill by name:

```text
Use $editable-consulting-ppt-workflow to redesign this slide using my PPTX template. Ask one question at a time, show me an SVG preview first, and generate a native-editable PPTX after approval.
```

中文示例：

```text
使用 $editable-consulting-ppt-workflow，根据我提供的 PPT 母版和页面截图，一次只问一个问题。先生成 SVG 预览供我确认，确认后再制作完全可编辑的 PPTX。
```

See [`references/user-guide.zh-CN.md`](references/user-guide.zh-CN.md) for more Chinese usage examples.

## Repository structure

```text
.
├── SKILL.md                         # Main skill instructions
├── agents/openai.yaml               # Skill display metadata
├── references/                      # Workflow, research, build, and QA guidance
├── scripts/                         # SVG and PPTX inspection/QA utilities
└── assets/
    ├── examples/                    # Neutral demonstration assets
    └── templates/                   # Reusable ledgers and QA templates
```

The bundled neutral PPTX is for testing and demonstration only. It must not be used as the default production template.

## Verification utilities

The repository includes utilities for:

- SVG validation
- PPTX structural inspection
- font checks
- source-template comparison
- combined PPTX QA reporting
- preliminary rendering
- public-release sanitization

Most Python utilities use the standard library. The test-template generator requires Node.js and its referenced presentation package. Preliminary rendering may use LibreOffice when available, but final acceptance still requires Microsoft PowerPoint for macOS.

## License

Released under the [MIT License](LICENSE).
