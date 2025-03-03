import random
from . import dice

def pcCreate(pcType):
    if pcType == "/DND5" or pcType == "/dnd5":
        pc_list = []
        result = f"的英雄作成如下："
        sets = 0
        while sets < 5:
            status_list = []
            status_sum = 0
            for st in range(0,6):
                status_temp_list = []
                for x in range(0,4):
                    status_temp = random.randint(1,6)
                    status_temp_list.append(status_temp)
                for a in range(0,len(status_temp_list)):
                    for b in range(0,len(status_temp_list)-a-1):
                        if status_temp_list[b] <= status_temp_list[b+1]:
                            status_temp_list[b], status_temp_list[b+1] = status_temp_list[b+1], status_temp_list[b]
                #print(status_temp_list)
                status = status_temp_list[0] + status_temp_list[1] + status_temp_list[2]
                status_list.append(status)
                status_sum = status_sum + status
            result = f"{result}\n力量:{status_list[0]} 体质:{status_list[1]} 敏捷:{status_list[2]} 智力:{status_list[3]} 感知:{status_list[4]} 魅力:{status_list[5]} 共计:{status_sum}"
            sets = sets + 1
        return(result)
    else:
        pc_list = []
        result = f"的调查员作成如下："
        sets = 0
        while sets < 3:
            sets = sets + 1
            status_list = []
            STR = int(dice.dice_roll("3d6")[0])*5
            CON = int(dice.dice_roll("3d6")[0])*5
            SIZ = (int(dice.dice_roll("2d6")[0]+6))*5
            DEX = int(dice.dice_roll("3d6")[0])*5
            APP = int(dice.dice_roll("3d6")[0])*5
            INT = (int(dice.dice_roll("2d6")[0]+6))*5
            POW = int(dice.dice_roll("3d6")[0])*5
            EDU = (int(dice.dice_roll("2d6")[0]+6))*5
            LUC = int(dice.dice_roll("3d6")[0])*5
            SUM1 = STR+CON+SIZ+DEX+APP+INT+POW+EDU+LUC
            SUM2 = STR+CON+SIZ+DEX+APP+INT+POW+EDU
            result = f"{result}\n力量:{STR} 体质:{CON} 体型:{SIZ} 敏捷:{DEX} 外貌:{APP} 智力:{INT} 意志:{POW} 教育:{EDU} 幸运:{LUC} 共计:{SUM2}/{SUM1}"
        return(result)
