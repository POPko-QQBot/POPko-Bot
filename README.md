# POPko-Bot
本机器人基于QQ官方pythonSDK制作

## 部署步骤
1. pip install -r requirements.txt
2. pip install qq-botpy
3. python client.py

## 聊天指令
| 指令      | 参数                | 效果                                    | 备注                                  |
|-----------|---------------------|---------------------------------------|---------------------------------------|
| /jrrp     |                     | 取1-100随机数模拟今日人品（点数越小越欧） |                                       |
| /coc或/dnd | {次数}              | 根据coc或dnd车卡规则，创造对应个数的数据 |                                       |
| r         | {dice_num}d{dice_face} | 掷骰                                  | 例：r1d6+1d4+1                        |
| ra        | （b/p）(困难/极难){attribute} | 技能检定                            | 例如：rap2 困难力量，带有2个惩罚骰的困难力量检定 |
| pc        | new {name}          | 创建名为{name}的空白角色卡            |                                       |
| pc        | tag {name}          | 绑定当前QQ号下名为{name}的角色         |                                       |
| pc        | show                | 展示当前绑定角色                      |                                       |
| pc        | del {name}          | 删除当前QQ号名为{name}的角色           |                                       |
| st        | {attribute}{value}  | 录入{attribute}数据                   | 可以一次录入多个数据                   |
| st        | {attribute}+/-{value} | 改变{attribute}属性值                | 例如st 力量+1d6+2d8                   |
| st        | show                | 展示当前绑定角色                      | 可以使用show {attribute}展示某个技能的属性 |
| st        | del {attribute}     | 删除当前绑定角色的{attribute}         |                                       |
| dr        | b/p                 | D20掷骰                               | b为优势、p为劣势                      |
| dc        | (b/p){num}{dice}    | DC为{num}的优势/劣势豁免检定，加值为{dice} | 例如 dc15+1d6+1d4+2，dc为15的豁免检定，加值为1d6+1d4+2 |
