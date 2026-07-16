# Vox Director for Codex

一个面向 Codex 的视频导演 Skill：把一句主题、一个产品、一段脚本或一个观点，制作成完整的 **Vox 风格纸张剪贴 / 编辑部拼贴视频**。

它负责的不只是生成图片，而是串起整条制作流程：脚本拆解、分镜设计、统一视觉、图片生成、剪纸动画、中文旁白、字幕、配乐、音画同步、质量检查与最终渲染。

本版本基于 [Alisa0808/vox-director](https://github.com/Alisa0808/vox-director) 改造，更适合在本地 Codex 工作流中使用。

## 主要特点

- 默认使用 Codex 内置 **ImageGen** 生成图片，也可按需指定 API 路径使用 `gpt-image-2`
- 使用 **HyperFrames** 制作确定性的剪纸、拼贴、推拉、遮罩和转场动画
- 用户明确指定时，也可以切换到 **Remotion**
- 使用 **MiniMax** 生成中文旁白和音乐，支持女性声线、语速与情绪起伏
- 标题、字幕、时间和数字由后期实时排版，不让图片模型生成文字，减少乱码和错字
- 不依赖 Atlas Cloud
- 支持横屏、竖屏以及不同时长，不限制画面中只能出现少量物体
- 输出完整 MP4，并检查关键帧、字幕可读性、音画同步和最终时长

## 工作流程

1. 根据主题编写并充实旁白脚本
2. 把内容拆成场景、节奏与镜头
3. 设计统一的 Vox 纸张剪贴视觉系统
4. 用 ImageGen 生成不含文字和数字的画面素材
5. 用 MiniMax 生成带情绪变化的旁白和可选配乐
6. 用 HyperFrames 编排动画、字幕与转场
7. 检查关键帧、文字、声音和节奏
8. 渲染高清成片，并按需要输出适合社交平台发送的版本

## 安装

把下面这段话发给 Codex：

```text
安装这个 skill：

https://github.com/kakaxi12/vox-director-codex/tree/main/vox-director
```

也可以手动安装：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/kakaxi12/vox-director-codex.git
cp -R vox-director-codex/vox-director ~/.codex/skills/vox-director
```

安装完成后，新建一个 Codex 任务即可使用。

## 使用示例

```text
使用 $vox-director，以 Vox 剪纸拼贴风制作一个关于“人工智能如何改变普通人一天”的视频，中文女性旁白，约 60 秒，9:16 竖屏。
```

也可以直接说：

```text
用 Vox 剪纸风做一个关于“为什么年轻人越来越喜欢独处”的中文视频，画面丰富一些，旁白自然、有情绪起伏。
```

如果没有指定时长、比例或图片风格，Skill 会根据内容自行选择适合的方案。

## 运行环境

- Codex 内置 `imagegen` Skill
- HyperFrames 插件或相关 Skills
- Node.js 22+
- FFmpeg
- 使用 MiniMax 旁白或音乐时，需要安装 `mmx-cli` 并配置使用者自己的 MiniMax 凭据

Codex 内置 ImageGen 路径不要求使用者额外提供 OpenAI API Key。仓库中不包含任何 API Key、生成视频或私人素材。

## 说明

这是一个制作工作流 Skill，不是单独的视频生成模型。实际生成时间、声音额度和音乐额度取决于所使用的服务与本地设备性能。

## 许可与来源

本仓库保留了上游许可证，见 [vox-director/LICENSE](vox-director/LICENSE)。工作流改编自 [Alisa0808/vox-director](https://github.com/Alisa0808/vox-director)。
