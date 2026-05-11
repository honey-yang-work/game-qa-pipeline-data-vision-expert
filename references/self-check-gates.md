# 多遍自检门禁

在声明 skill 更新、QA 资产生成或白盒审计任务完成之前，必须执行以下检查。

## 第 1 遍：结构保真

确认所有核心阶段仍然存在：

- Phase 0: 需求分块与知识加载
- Phase 1: 三位一体审计与坑点扫描
- Phase 2: 逻辑全景建模与 RTM
- Phase 3: 资深设计与红蓝对抗
- Phase 4: 全自动化资产交付
- Phase 5: 后端工程 + 配置表联合逆向审计与动态渗透策略

失败处理：先恢复缺失阶段或门禁，再继续。

## 第 2 遍：能力覆盖

确认以下能力仍然存在：

- 图文表三位一体审计
- 项目术语和历史坑点扫描
- 项目专属知识库建立、更新与命中使用
- 能力边界库
- 规则承载域识别
- 全文证据合并门禁
- `R` / `T` 双追踪 RTM
- 数据驱动测试
- 红蓝对抗
- Python / Airtest 自动化伪代码
- Excel / JSON / XMind 交付
- Windows 中文资产编码保护
- 默认后端工程 `C:\NuoYaIdle\Server\` 需求驱动源码定位
- 默认配置表目录 `C:\NuoYaIdle\Tools\表格配置及转换\excel\` 字段和值读取
- 源码拓扑树
- 调用链源码图
- 闭环证据链
- 代码与配置追踪矩阵
- 命中置信度分级
- 代码缺陷 / 配置缺陷 / 代码配置不一致 / 配置证据不足定性
- Phase 5 只读审计优先
- 源码业务释义注释落地
- 修复后 Diff 复审模式
- 默认工程根或配置根不可用时的降级询问策略
- 守方证明与攻方破坏
- 《白盒审视结论单》
- 收尾规则增量与避坑点学习

失败处理：把缺失能力补回 `SKILL.md` 或正确的 reference 文件。

## 第 3 遍：契约一致性

检查文档和脚本在以下内容上保持一致：

- `SKILL.md`、`output-contracts.md`、脚本三者的口径
- 工作簿工作表名称
- 测试用例列
- RTM 列
- 可选的代码与配置追踪矩阵列
- 优先级取值
- 追踪 ID 格式
- 输出文件命名
- JSON 载荷结构

预期工作表名称：

- `测试用例库`
- `需求跟踪矩阵`

可选 Phase 5 工作表：

- `代码追踪矩阵`

失败处理：更新文档或脚本，使两者保持一致。

## 第 4 遍：工具验证

运行：

```powershell
$env:PYTHONUTF8='1'; python "C:\Users\yangfeng\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "C:\Users\yangfeng\.codex\skills\game-qa-pipeline-data-vision-expert"
python -m py_compile "C:\Users\yangfeng\.codex\skills\game-qa-pipeline-data-vision-expert\scripts\build_game_qa_data_vision_workbook.py"
python -m py_compile "C:\Users\yangfeng\.codex\skills\game-qa-pipeline-data-vision-expert\scripts\validate_game_qa_payload.py"
```

同时做一遍最小载荷冒烟验证：

- 如果仓库内已提供样例载荷，直接用样例载荷运行：
  - `validate_game_qa_payload.py`
  - `build_game_qa_data_vision_workbook.py`
- 如果仓库内没有样例载荷，按 `references/output-contracts.md` 中的 JSON 结构临时构造一份最小合法载荷，至少验证：
  - `test_cases`
  - `rtm`
  - 可选 `code_traceability`
  - 输出工作表名为 `测试用例库` / `需求跟踪矩阵`，并在提供 `code_traceability` 时生成 `代码追踪矩阵`

失败处理：修复失败脚本或契约后，才能声明完成。

## 第 5 遍：场景压测

用心智模拟或实际方式测试以下触发场景：

| 场景 | 必须表现 |
|---|---|
| 长文本 + UI 图片 + 表格 | 先执行 Phase 0，确认后再进入 Phase 1 |
| 表驱动概率或权重规则 | 生成字段级 `T` ID 和数据驱动测试用例 |
| 用户直接要求测试用例 | 仍先执行必要反问与门禁，再进入设计 |
| 用户粘贴源码 | 立即触发 Phase 5 |
| 本地文件夹或压缩包 | 安全分流，跳过无关文件，先输出拓扑 |
| 完整后端工程 | 未给其他根目录时默认使用 `C:\NuoYaIdle\Server\` |
| 默认工程根不可读 | 只询问新的后端工程路径，不要求用户贴代码 |
| 默认配置根不可读 | 标记配置证据不足，只询问新的配置表目录 |
| 用户要求基于上一轮修复重新复审 | 触发 Phase 5 的 Diff 复审模式 |
| Phase 5 Step 2 | 只新增 `[新增业务释义注释]`，不得新增可执行插桩 |

失败处理：强化强制门禁或快速参考规则。

## 第 6 遍：防丢 diff 复查

重构 skill 结构时，对比旧能力清单和新能力清单。每个旧能力都必须属于以下状态之一：

- 保留在 `SKILL.md` 中
- 移动到某个 reference 文件中
- 由脚本承载

不得静默删除任何能力。

失败处理：恢复缺失内容，并重新执行所有检查。
