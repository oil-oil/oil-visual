<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="oil-visual：漫画墨线、半调网点、小人和黄色边牧组成的配图风格">
</p>

`oil-visual` 是一套给 Codex 使用的配图规范。它把角色、线条、网点、颜色、场景和图片文字统一在一套规则里，让不同主题的图保持同一种视觉语言。

适合用来画概念解释、机制流程、对比关系和角色场景。

## 配图风格

- 用粗细分明的黑色墨线画轮廓和细节。
- 用圆形半调网点表现灰面和阴影，不使用柔和渐变。
- 主角是戴圆框眼镜的极简小人，旁边保留一只胖胖的暖黄色边牧。
- 场景使用米白色纸张质感，只保留少量真正帮助理解的环境物件。
- 暖黄色是固定颜色；每张图最多再使用两种语义色。
- 图片需要文字时，使用短而准确的无衬线标签，并直接放在对应物体上。

## 示例

<p align="center">
  <img src="./examples/explainer-agent-workflow.png" width="48%" alt="小人和黄色边牧风格的子 Agent 机制图">
  <img src="./examples/explainer-cost-comparison.png" width="48%" alt="小人和黄色边牧风格的成本对照图">
</p>

左图用任务单、工作桌和结果文件夹说明任务怎样分配与汇总。右图用资料数量和消耗表对比分工与重复处理。两张图的文字都直接画在图片里。

## 安装

```bash
git clone https://github.com/oil-oil/oil-visual.git ~/.codex/skills/oil-visual
```

重启 Codex，然后在对话里点名使用：

```text
Use $oil-visual to explain how the main Agent assigns work to subagents.
Use short, exact Chinese labels inside the image.
```

```text
Use $oil-visual to draw the glasses stick figure reviewing a blueprint,
with the warm-yellow Border Collie sitting beside the desk.
```

完整规则、提示词结构和交付检查都写在 [`SKILL.md`](./SKILL.md) 里。

## License

[MIT](./LICENSE)
