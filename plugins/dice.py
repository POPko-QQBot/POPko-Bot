import re
import random
from . import pc_status

def split_add_minus(msg,patterns):
    result_list = [msg]
    for p in patterns:
        string_temp = []
        list(
            map(
                lambda sub_string: string_temp.extend(sub_string.split(p)),
                result_list
                )
            )
        result_list = string_temp
    return result_list

def roll_attribute_match(msg):
    pattern = re.compile(
        r'(a)'
        r'(b|p)?'
        r'(\d*)'
        r'(\d+#)?'
        r'(b|p)?'
        r'(\d*)'
        r'( )?'
        r'(困难|极难)?'
        r'( )?'
        r'([\u4e00-\u9fa5a-zA-Z/]+)'
        )
    match = pattern.match(msg)
    results = []
    i = 6
    while i > 0:
        print(i)
        if match.group(i) and i != 4:
            results = [match.group(i)] + results
        i = i - 1
    times = int(match.group(4).strip('#')) if match.group(4) else 1
    if match.group(8):
        msg = ''.join(results) + ' ' + match.group(8) + match.group(10)
    else:
        msg = ''.join(results) + ' ' + match.group(10)
    if match.group(2) == 'b':
        bonus = 1
    else:
        bonus = 0
    return msg, times, bonus

def roll_attribute(msg,member_openid):
    from . import pc_status
    pc = pc_status.get_now_tag_pc(member_openid)
    pc_data = pc_status.get_st(pc, member_openid)
    results = []
    lose_dice = 99
    win_dice = 5
    hard_check = 0
    times = 1
    msg, times, bonus = roll_attribute_match(msg)
    if "困难" in msg:
        try:
            attribute = msg.split("困难")[1]
            attribute = pc_status.format_attribute(attribute)
            if attribute in pc_data:
                value = pc_data[attribute]
            else:
                value = pc_status.get_st_default(attribute)
            if value < 50:
                lose_dice = 95
                win_dice = 1
            if not value:
                return '你不输对技能我怎么roll'
            value = int(value/2)
            results.append(f'{pc}进行困难{attribute}检定:\n')
            hard_check = 1
        except:
            return '你不输入技能我怎么roll'
    elif "极难" in msg:
        try:
            attribute = msg.split("极难")[1]
            attribute = pc_status.format_attribute(attribute)
            if attribute in pc_data:
                value = pc_data[attribute]
            else:
                value = pc_status.get_st_default(attribute)
            if value < 50:
                lose_dice = 95
                win_dice = 1
            if not value:
                return '你不输对技能我怎么roll'
            value = int(value/5)
            results.append(f'{pc}进行极难{attribute}检定:\n')
            hard_check = 1
        except:
            return '你不输入技能我怎么roll'
    else:
        try:
            attribute = msg.split()[1]
        except:
            return '你不输入技能我怎么roll'
        attribute = pc_status.format_attribute(attribute)
        print(attribute)
        if attribute in pc_data:
            value = pc_data[attribute]
        else:
            value = pc_status.get_st_default(attribute)
        if value < 50:
            lose_dice = 95
            win_dice = 1
        if not value:
            return '你不输对技能我怎么roll'
        results.append(f'{pc}进行{attribute}检定:\n')
    for time in range(times):
        bonus = 0
        punish = 0
        unit_slot = 0
        ten_slot = 0
        check_list = []
        extra_dice_list = []
        check = random.randint(1,100)
        if "p" in msg:
            try:
                pattern = msg.split()[0]
                count = re.match(r'(a\d*p)(\d+)',msg).group(2)
                punish = int(count)
            except:
                punish = 1
            unit_slot = random.randint(1,10)
            for i in range(0,punish+1):
                ten_slot = random.randint(1,10)
                if unit_slot != 10 and ten_slot == 10:
                    check = unit_slot
                elif unit_slot == 10 and ten_slot != 10:
                    check = ten_slot * 10
                elif unit_slot == 10 and ten_slot == 10:
                    check = 100
                else:
                    check = ten_slot*10 + unit_slot
                check_list.append(check)
                if i == 0:
                    init_dice = check
                else:
                    extra_dice_list.append(str(ten_slot))
            for i in range(len(check_list)):
                for j in range(len(check_list) -1):
                    if check_list[j] > check_list[j+1]:
                        check_list[j],check_list[j+1] = check_list[j+1],check_list[j]
            check = check_list[-1]
        if "b" in msg:
            try:
                pattern = msg.split()[0]
                count = re.match(r'(a\d*b)(\d+)',msg).group(2)
                bonus = int(count)
            except:
                bonus = 1
            unit_slot = random.randint(1,10)
            for i in range(0,bonus+1):
                ten_slot = random.randint(1,10)
                if unit_slot != 10 and ten_slot == 10:
                    check = unit_slot
                elif unit_slot == 10 and ten_slot != 10:
                    check = ten_slot * 10
                elif unit_slot == 10 and ten_slot == 10:
                    check = 100
                else:
                    check = ten_slot*10 + unit_slot
                check_list.append(check)
                if i == 0:
                    init_dice = check
                else:
                    extra_dice_list.append(str(ten_slot))
            for i in range(len(check_list)):
                for j in range(len(check_list) -1):
                    if check_list[j] > check_list[j+1]:
                        check_list[j],check_list[j+1] = check_list[j+1],check_list[j]
            check = check_list[0]
        if len(extra_dice_list) > 1:
            extra_dice = ",".join(extra_dice_list)
        elif len(extra_dice_list) == 1:
            extra_dice = extra_dice_list[0]
        if bonus > 0:
            results.append(f'B={init_dice}  [奖励骰：{extra_dice}]  ')
        elif punish > 0:
            results.append(f'P={init_dice}  [惩罚骰：{extra_dice}]  ')
        if check > lose_dice:
            results.append(f'{check}/{value} 大失败\n')
        elif check <= win_dice:
            results.append(f'{check}/{value} 大成功\n')
        elif check <= int(value/5) and hard_check == 0:
            results.append(f'{check}/{value} 极难成功\n')
        elif check <= int(value/2) and hard_check == 0:
            results.append(f'{check}/{value} 困难成功\n')
        elif check <= value:
            results.append(f'{check}/{value} 成功\n')
        else:
            results.append(f'{check}/{value} 失败\n')
    return ''.join(results)

def roll_bonus(msg):
    match = re.match(r'[bp](\d+)?', msg)
    try:
        extra_dice_num = int(match.group(1))
    except:
        extra_dice_num = 1
    bonus = 0
    if 'b' in msg:
        bonus = 1
    unit_slot = random.randint(1,10)
    check_list = []
    extra_dice_list = []
    results = []
    for i in range(0,extra_dice_num+1):
        ten_slot = random.randint(1,10)
        if unit_slot == 10 and ten_slot != 10:
            check = ten_slot * 10
        elif unit_slot != 10 and ten_slot == 10:
            check = unit_slot
        elif unit_slot != 10 and ten_slot != 10:
            check = ten_slot * 10 + unit_slot
        else:
            check = 100
        check_list.append(check)
        if i == 0:
            init_dice = check
        else:
            extra_dice_list.append(str(ten_slot))
    for i in range(0,len(check_list)):
        for j in range(0,len(check_list)-1):
            if check_list[j] > check_list[j+1]:
                check_list[j],check_list[j+1] = check_list[j+1],check_list[j]
    if bonus > 0:
        check = check_list[0]
        bonus_type = '奖励骰'
    else:
        check = check_list[-1]
        bonus_type = '惩罚骰'
    return check, init_dice, extra_dice_list, bonus_type

def dice_roll(msg):
    try:
        return int(msg), msg
    except:
        match = re.match(r'(\d+)?d(\d+)',msg)
    try:
        dice_num = int(match.group(1))
    except:
        dice_num = 1
    dice_face = int(match.group(2))
    expression_list = []
    result = 0
    for i in range(0,dice_num):
        dice = random.randint(1,dice_face)
        expression_list.append(str(dice))
    for r in expression_list:
        result = result + int(r)
    expression = '+'.join(expression_list)
    return result, expression
    
def roll(msg, member_openid):
    pc = pc_status.get_now_tag_pc(member_openid)
    if 'h' in msg:
        command = msg.split('h')
        msg = ''.join(command)
    if "r" in msg:
        try:
            msg = msg.split("r")[1].strip()
        except:
            msg = "1d100"
    results = []
    dice_list = []
    expression_list = []
    operator_list = []
    if "a" in msg:
        return roll_attribute(msg, member_openid)
    print(msg)
    if "p" in msg or "b" in msg:
        result, init_dice, extra_dice_list, bonus = roll_bonus(msg)
        if len(extra_dice_list) > 1:
            extra_dice = ", ".join(extra_dice_list)
        elif len(extra_dice_list) == 1:
            extra_dice = extra_dice_list[0]
        return f'{pc}进行D100掷骰,P={init_dice}  [{bonus}：{extra_dice}]={result}'
    if len(msg) == 0:
        msg = "1d100"
    results.append(f'{pc}掷骰：{msg}=')
    roll_list = split_add_minus(msg,"+-")
    for pattern in roll_list:
        dice, expression = dice_roll(pattern)
        dice_list.append(dice)
        expression_list.append(expression)
    for a in msg:
        if a == '+' or a == '-':
            operator_list.append(a)
    ex = ''
    di = ''
    for i in range(0,len(roll_list)):
        if i == len(roll_list) - 1:
            ex = ex + f'{expression_list[i]}'
            di = di + f'{dice_list[i]}'
        else:
            ex = ex + f'{expression_list[i]}'+f'{operator_list[i]}'
            di = di + f'{dice_list[i]}'+f'{operator_list[i]}'
    di = eval(di)
    results.append(ex)
    result = ''.join(results)
    return f'{result}={di}'


def dnd_roll(msg):
    try:
        msg = msg.split('dr')[1].strip()
    except:
        result = dice_roll('1d20')[0]
        return f'进行D20掷骰={result}'
    match = re.match(r'(\d+#)?([bp])?',msg)
    results = []
    try:
        times = int(match.group(1).strip('#')[0])
    except:
        times = 1
    for i in range(0,times):
        if times == 1:
            time = ''
        else:
            time = f'第{i+1}次'
        bonus = match.group(2)
        if bonus == 'b' or bonus == 'p':
            roll_1 = dice_roll('1d20')[0]
            roll_2 = dice_roll('1d20')[0]
            if bonus == 'b':
                bonus = '优势'
                if roll_1 < roll_2:
                    roll_1,roll_2 = roll_2,roll_1
            else:
                bonus = '劣势'
                if roll_1 > roll_2:
                    roll_1,roll_2 = roll_2,roll_1
            results.append(f'{time}进行D20{bonus}掷骰[{roll_1}，{roll_2}]={roll_1}\n')
        else:
            result = dice_roll('1d20')[0]
            results.append(f'{time}进行D20掷骰={result}\n')
    return ''.join(results)

def dnd_check(msg):
    match = re.match(r'dc([bp])?(\d+)?( )?([+-])?(.*)?',msg)
    dice_list = []
    results = []
    expression_list=[]
    operator_list=[]
    try:
        check_value = int(match.group(2))
    except:
        return '请设置DC值'
    try:
        operator = match.group(4)
    except:
        operator = ''
    try:
        roll_list = split_add_minus(match.group(5),'+-')
        for r in roll_list:
            dice, expression = dice_roll(r)
            dice_list.append(dice)
            expression_list.append(expression)
        for a in msg:
            if a == '+' or a == '-':
                operator_list.append(a)
        ex = ''
        di = ''
        for i in range(0,len(roll_list)):
            if i == len(roll_list) - 1:
                ex = ex + f'{expression_list[i]}'
                di = di + f'{dice_list[i]}'
            else:
                ex = ex + f'{expression_list[i]}'+f'{operator_list[i]}'
                di = di + f'{dice_list[i]}'+f'{operator_list[i]}'
    except:
        ex = ''
        di = ''
        operator = ''
    bonus = match.group(1)
    if bonus == 'b' or bonus == 'p':
        roll_1 = dice_roll('1d20')[0]
        roll_2 = dice_roll('1d20')[0]
        if bonus == 'b':
            bonus = '优势'
            if roll_1 < roll_2:
                roll_1,roll_2 = roll_2,roll_1
        else:
            bonus = '劣势'
            if roll_1 > roll_2:
                roll_1,roll_2 = roll_2,roll_1
        result = roll_1
        results.append(f'进行DC为{check_value}的D20{bonus}检定[{roll_1}，{roll_2}]=')
    else:
        result = dice_roll('1d20')[0]
        results.append(f'进行DC为{check_value}的D20检定=')
    init_dice = result
    if di == '':
        results.append(f'{result},')
    elif operator != '':
        expression = str(result)+operator+ex
        result = eval(str(result)+operator+di)
        results.append(f'{expression}={result},')
    else:
        operator='+'
        expression = str(result)+operator+ex
        result = eval(str(result)+operator+di)
        results.append(f'{expression}={result},')
    if result >= check_value and init_dice != 20:
        check = '成功'
    elif init_dice == 20:
        check = 'N20大成功'
    elif init_dice == 1:
        check = 'N1大失败'
    else:
        check = '失败'
    results.append(f'{check}')
    return ''.join(results)