import os
import json
import re
import random
from . import dice
from . import st_name

def db_check():
    if not os.path.exists("./st_db.json"):
        os.system(r'touch {}'.format('./st_db.json'))
    if not os.path.exists("./tag_pc.json"):
        os.system(r'touch {}'.format('./tag_pc.json'))

def get_now_tag_pc(member_openid):
    with open('./tag_pc.json','r',encoding="utf-8") as tag_pc:
        pc_dic = tag_pc.read()
        if not pc_dic == '':
            pc_data = json.loads(pc_dic)
        else:
            pc_data = {}
        tag_pc.close()
    if member_openid in pc_data:
        return pc_data[member_openid]
    else:
        return None

def st_update(attribute, value, member_openid):
    pc = get_now_tag_pc(member_openid)
    with open('./st_db.json','r',encoding="utf-8") as st_db:
        st_data = json.loads(st_db.read())
    st_data[member_openid][pc][attribute] = value
    with open('./st_db.json','w',encoding="utf-8") as st_db:
        json.dump(st_data,st_db,ensure_ascii=False)

def get_st_modify(param):
    match = re.match(r'([\u4e00-\u9fa5a-zA-Z/]+)(.*)', param)
    attribute = match.group(1)
    modifier = match.group(2)
    dice_results = []
    operator_list = []
    if modifier.startswith('+') or modifier.startswith('-'):
        roll_list = dice.split_add_minus(modifier,"+-")
        for r in roll_list[1:]:
            res, expression = dice.dice_roll(r)
            dice_results.append(str(res))
        for a in modifier:
            if a == '+' or a == '-':
                operator_list.append(a)
        result_str = ''
        for i in range(0,len(dice_results)):
            result_str = result_str+operator_list[i]+dice_results[i]
        return attribute,result_str,'relative'
    else:
        return attribute,modifier,'direct'

def format_attribute(attribute):
    for key, value in st_name.STATUS_NAME.items():
        if attribute in value:
            return key
    return attribute

def pc_create(name, member_openid):
    st_data = {}
    try:
        with open('./st_db.json', 'r', encoding='utf-8') as st_db:
            st_data = json.load(st_db)
    except json.JSONDecodeError:
        st_data = {}
    if not member_openid in st_data:
        st_data[member_openid] = {}
    if name in st_data[member_openid]:
        return f'你已经有{name}这个角色了，不要重名'
    else:
        st_data[member_openid][name] = {}
    with open('./st_db.json','w',encoding="utf-8") as st_db:
        json.dump(st_data,st_db,ensure_ascii=False)
        st_db.close()
    return f'已为您创建空白角色{name}'

def get_pc_list(member_openid):
    st_data = {}
    try:
        with open('./st_db.json', 'r', encoding='utf-8') as st_db:
            st_data = json.load(st_db)
    except json.JSONDecodeError:
        st_data = {}
    results = []
    if not member_openid in st_data:
        return None
    for key in st_data[member_openid]:
        results.append(key)
    return results

def pc_tag(name, member_openid):
    st_data = {}
    try:
        with open('./st_db.json', 'r', encoding='utf-8') as st_db:
            st_data = json.load(st_db)
    except json.JSONDecodeError:
        st_data = {}
    if not member_openid in st_data:
        return f'你还没有角色{name},快输入/pc new 创建角色'
    if not name in get_pc_list(member_openid):
        return f"你还没有角色{name},你确定角色名字没错？"
    pc_data = {}
    try:
        with open('./tag_pc.json', 'r', encoding='utf-8') as tag_pc:
            pc_data = json.load(tag_pc)
    except json.JSONDecodeError:
        pc_data = {}
    pc_data[member_openid] = name
    with open('./tag_pc.json', 'w', encoding='utf-8') as tag_pc:
        json.dump(pc_data,tag_pc,ensure_ascii=False)
    return f'你的角色已绑定为{name}'

def get_st_default(attribute):
    attribute = format_attribute(attribute)
    default_data = st_name.SKILL_DEFAULT.items()
    for key, value in default_data:
        if key == attribute:
            return value
    return None 

def get_st(pc, member_openid):
    st_data = {}
    try:
        with open('./st_db.json', 'r', encoding='utf-8') as st_db:
            st_data = json.load(st_db)
    except json.JSONDecodeError:
        st_data = {}
    pc = get_now_tag_pc(member_openid)
    return st_data[member_openid][pc]

def pc_modify(command,member_openid):
    pc = get_now_tag_pc(member_openid)
    if not pc:
        return f'你绑定角色之后再说吧'
    if command == 'show':
        results = []
        results.append(f'{pc}当前属性如下：\n')
        st_data = get_st(pc,member_openid)
        base_list = ['体力','理智','魔法','幸运','力量','体质','体型','敏捷','外貌','智力','意志','教育','初始幸运']
        try:
            max_hp = int((st_data['体型'] + st_data['体质']) / 10)
            max_mp = int(st_data['意志']/5)
        except:
            return f'{pc}的基础属性不完整，请补充完整'
        if '体力' in st_data:
            hp_value = st_data['体力']
        else:
            hp_value = max_hp
            st_data['体力'] = hp_value
        if '魔法' in st_data:
            mp_value = st_data['魔法']
        else:
            mp_value = max_mp
            st_data['魔法'] = hp_value
        if '克苏鲁神话' in st_data:
            max_san = 99 - st_data['克苏鲁神话']
        else:
            max_san = 99
        if not '闪避' in st_data:
            st_data['闪避'] = int(st_data['敏捷']/2)

        if '初始幸运' in st_data:
            results.append(f'HP:{hp_value}/{max_hp}    MP:{mp_value}/{max_mp}\nSAN:{st_data["理智"]}/{max_san}       幸运:{st_data["幸运"]}/{st_data["初始幸运"]}(初始)\n\n基础属性:\n')
        else:
            results.append(f'HP:{hp_value}/{max_hp}    MP:{mp_value}/{max_mp}\nSAN:{st_data["理智"]}/{max_san}       幸运:{st_data["幸运"]}(未设置初始值)\n\n基础属性:\n')
        results.append(f'力量:{st_data["力量"]}    外貌:{st_data["外貌"]}\n体质:{st_data["体质"]}    智力:{st_data["智力"]}\n体型:{st_data["体型"]}    意志:{st_data["意志"]}\n敏捷:{st_data["敏捷"]}    教育:{st_data["教育"]}\n\n技能:\n')
        for key in st_data:
            value = st_data[key]
            if not key in base_list:
                output = f'{key}:{value}'
                results.append(f'{output}\n')
        # con = st_data['体型']
        # siz = st_data['体质']
        # max_hp = int((con + siz) / 10)
        # value = st_data['生命']        
        # if value <= 0:
        #     value = max_hp
        # results.append(f'生命:{value}/{max_hp}')
        # for key in st_data:
        #     value = st_data[key]
        #     if key in line_list:
        #         results.append(f'{key}：{value}\0')
        #     else:
        #         results.append(f'{key}：{value}\n')
        # print("".join(results))
        return "".join(results)
    if command == 'list':
        pc_list = get_pc_list(member_openid)
        return "\n".join(pc_list)

def pc_remove(name, member_openid):
    pc_list = get_pc_list(member_openid)
    if not name in pc_list:
        return f'你没有名为{name}的角色，别乱删！'
    st_data = {}
    try:
        with open('./st_db.json', 'r', encoding='utf-8') as st_db:
            st_data = json.load(st_db)
        with open('./tag_pc.json', 'r', encoding='utf-8') as tag_pc:
            pc_data = json.load(tag_pc)
    except json.JSONDecodeError:
        st_data = {}
        pc_data = {}
    del st_data[member_openid][name]
    if name == pc_data[member_openid]:
        del pc_data[member_openid]
        with open('./tag_pc.json', 'w', encoding='utf-8') as tag_pc:
            json.dump(pc_data,tag_pc,ensure_ascii=False)
    with open('./st_db.json','w',encoding="utf-8") as st_db:
        json.dump(st_data,st_db,ensure_ascii=False)
    return f'已经删除角色卡{name}'

def pc_main(msg, member_openid):
    db_check()
    parts = msg.split()
    if len(parts) < 2:
        command = 'show'
    else:
        command = parts[1]
    if command == 'new':
        if len(parts) < 3:
            return '没有名字我可没办法创建'
        name = parts[2]
        return pc_create(name, member_openid)
    elif command == 'tag':
        if len(parts) < 3:
            return '没有名字我可没办法绑定'
        name = parts[2]
        return pc_tag(name, member_openid)
    elif command == 'del':
        if len(parts) < 3:
            return '没有名字我可没办法删除'
        name = parts[2]
        return pc_remove(name, member_openid)
    return pc_modify(command, member_openid)


def st_main(msg, member_openid):
    db_check()
    try:
        msg = 'st '+ msg[2:].strip()
    except:
        pass
    parts = msg.split()
    pc = get_now_tag_pc(member_openid)
    if not pc:
        return f'你不绑定角色我怎么知道你要给谁加属性？'
    st_data = {}
    try:
        with open('./st_db.json', 'r', encoding='utf-8') as st_db:
            st_data = json.load(st_db)
    except json.JSONDecodeError:
        st_data = {}
    pc_data = st_data[member_openid][pc]
    if len(parts) < 2:
        return "你咩都唔讲，叫我估咩也？"
    if parts[1] == 'show':
        try:
            attribute = format_attribute(parts[2])
            if attribute in pc_data:
                return f'{pc}的{attribute}属性值为：{pc_data[attribute]}'
            else:
                value = get_st_default(attribute)
                return f'{pc}的{attribute}属性值为：{value}'
        except:
            return pc_main(msg, member_openid)
    if '初始幸运' in parts[1]:
        value = re.match(r'(\D+)(\d+)',msg).group(2)
        try:
            value = int(value)
            if value >= 15 and value <= 90:
                st_data[member_openid][pc]['初始幸运'] = value
                with open('./st_db.json','w',encoding="utf-8") as st_db:
                    json.dump(st_data,st_db,ensure_ascii=False)
                return f'已记录{pc}初始幸运值'
            else:
                return f'{value}不是一个可用的数字'
        except:
            return f'{value}不是一个可用的数字'
    if not parts[1] == 'del':
        params = parts[1:]
    else:
        if len(parts) < 3:
            return '你不说哪个属性我删哪个？'
        attribute = parts[2]
        attribute = format_attribute(attribute)
        del pc_data[attribute]
        st_data[member_openid][pc] = pc_data
        with open('./st_db.json','w',encoding="utf-8") as st_db:
            json.dump(st_data,st_db,ensure_ascii=False)
        return f'已为{pc}删除{attribute}'
    results = []
    results.append(f"{pc}的属性值发生了变化")
    for param in params:
        parsed = get_st_modify(param)
        if not parsed:
            return f"好心你讲些我听的明的东西好不好"
        attribute, modifier, mod_type = parsed
        attribute = format_attribute(attribute)
        try:
            max_hp = int((pc_data['体质'] + pc_data['体型'])/10)
            max_mp = int((pc_data['意志'])/5)
        except:
            max_hp, max_mp = 0, 0
        if '克苏鲁神话' in pc_data:
            max_san = 99 - pc_data['克苏鲁神话']
        else:
            max_san = 99
        if mod_type == 'direct':
            try:
                value = int(modifier)
            except:
                return f'你填个{modifier}，就不怕你的角色坏掉吗？'
            if attribute == '体力':
                if value > max_hp:
                    value = max_hp
                elif value < 0:
                    value = 0
            elif attribute == '魔法':
                if value > max_mp:
                    value = max_mp
                elif value < 0:
                    value = 0
            elif attribute == '理智':
                if value > max_san:
                    value = max_san
                elif value < 0:
                    value = 0
            elif attribute == '克苏鲁神话':
                max_san = 99 - end_value
                if pc_data['理智'] > max_san:
                    pc_data['理智'] = max_san
            pc_data[attribute] = value
            results.append(f'{pc}的{attribute}已设置为{value}点')
        elif mod_type == 'relative':
            if attribute in pc_data:
                value = pc_data[attribute]
            else:
                value = get_st_default(attribute)
                if not value:
                    value = 0
            cal = eval('0' + modifier)
            end_value = value + cal
            results.append(f'{attribute}:{value}{modifier}={end_value}')
            if attribute == '体力':
                if end_value > max_hp:
                    end_value = max_hp
                    results.append(f'超出上限，{pc}的{attribute}调整为{end_value}')
            elif attribute == '魔法':
                if end_value > max_mp:
                    end_value = max_mp
                    results.append(f'超出上限，{pc}的{attribute}调整为{end_value}')
            elif attribute == '理智':
                if end_value > max_san:
                    end_value = max_san
                    results.append(f'超出上限，{pc}的{attribute}调整为{end_value}')
            elif attribute == '克苏鲁神话':
                max_san = 99 - end_value
                if pc_data['理智'] > max_san:
                    pc_data['理智'] = max_san
            if end_value < 0:
                end_value = 0
                results.append(f'不能为负，{pc}的{attribute}调整为{end_value}')
            pc_data[attribute] = end_value
            

        # if mod_type == 'dice':
        #     if attribute not in pc_data:
        #         return f'{pc}是不会这个能力的，麻烦你check清楚'
        #     sign = modifier[0]
        #     dice_result = dice.roll(modifier[1:])
        #     if sign == '+':
        #         if attribute == '体力':
        #             max_hp = int((pc_data['体质'] + pc_data['体型'])/10)
        #             if pc_data[attribute] + dice_result > max_hp :
        #                 pc_data[attribute] = max_hp
        #                 results.append(f'{attribute}增加超出上限，现在是{pc_data[attribute]}')
        #                 continue
        #         elif attribute == '魔法':
        #             max_mp = int(pc_data['意志']/5)
        #             if pc_data[attribute] + dice_result > max_mp :
        #                 pc_data[attribute] = max_mp
        #                 results.append(f'{attribute}增加超出上限，现在是{pc_data[attribute]}')
        #                 continue
        #         elif attribute == '理智':
        #             if '克苏鲁神话' in pc_data:
        #                 max_san = 99 - pc_data['克苏鲁神话']
        #             else:
        #                 max_san = 99
        #             if pc_data[attribute] + dice_result > max_san :
        #                 pc_data[attribute] = max_san
        #                 results.append(f'{attribute}增加超出上限，现在是{pc_data[attribute]}')
        #                 continue
        #         pc_data[attribute] = pc_data[attribute] + dice_result
        #         results.append(f'{attribute}增加了{dice_result}点，现在是{pc_data[attribute]}')
        #     else:
        #         if attribute == '体力':
        #             max_hp = int((pc_data['体质'] + pc_data['体型'])/10)
        #             if pc_data[attribute] - dice_result < 0 :
        #                 pc_data[attribute] = 0
        #                 results.append(f'{attribute}不能为负值，现在是{pc_data[attribute]}')
        #                 continue
        #         elif attribute == '魔法':
        #             max_mp = int(pc_data['意志']/5)
        #             if pc_data[attribute] - dice_result < 0 :
        #                 pc_data[attribute] = 0
        #                 results.append(f'{attribute}不能为负值，现在是{pc_data[attribute]}')
        #                 continue
        #         elif attribute == '理智':
        #             if '克苏鲁神话' in pc_data:
        #                 max_san = 99 - pc_data['克苏鲁神话']
        #             else:
        #                 max_san = 99
        #             if pc_data[attribute] - dice_result < 0 :
        #                 pc_data[attribute] = 0
        #                 results.append(f'{attribute}归0了，你陷入了永久疯狂')
        #                 continue
        #         pc_data[attribute] = pc_data[attribute] - dice_result
        #         results.append(f'{attribute}减少了{dice_result}点，现在是{pc_data[attribute]}')
        # elif mod_type == 'direct':
        #     try:
        #         value = int(modifier)
        #     except:
        #         return f'你填个{modifier}，就不怕你的角色坏掉吗？'
        #     if attribute == '体力':
        #         max_hp = int((pc_data['体质'] + pc_data['体型'])/10)
        #         if value > max_hp:
        #             value = max_hp
        #         elif value < 0:
        #             value = 0
        #     pc_data[attribute] = value
        #     results.append(f'{pc}的{attribute}已设置为{value}点')
        # elif mod_type == 'relative':
        #     if attribute not in pc_data:
        #         return f'{pc}是不会这个能力的，麻烦你check清楚'
        #     sign = modifier[0]
        #     try:
        #         value = int(modifier[1:])
        #     except:
        #         return f'你填个{modifier[1:]}，就不怕你的角色坏掉吗？'
        #     if sign == '+':
        #         if attribute == '体力':
        #             max_hp = int((pc_data['体质'] + pc_data['体型'])/10)
        #             if pc_data[attribute] + value > max_hp :
        #                 pc_data[attribute] = max_hp
        #                 results.append(f'{attribute}增加超出上限，现在是{pc_data[attribute]}')
        #                 continue
        #         pc_data[attribute] = pc_data[attribute] + value
        #         results.append(f'{attribute}增加了{value}点，现在是{pc_data[attribute]}')
        #     else:
        #         if attribute == '体力':
        #             max_hp = int((pc_data['体质'] + pc_data['体型'])/10)
        #             if pc_data[attribute] - value < 0 :
        #                 pc_data[attribute] = 0
        #                 results.append(f'{attribute}不能为负值，现在是{pc_data[attribute]}')
        #                 continue
        #         pc_data[attribute] = pc_data[attribute] - value
        #         results.append(f'{attribute}减少了{value}点，现在是{pc_data[attribute]}')
    if not '体力' in pc_data:
        try:
            pc_data['体力'] = int((pc_data['体质'] + pc_data['体型'])/10)
        except:
            results.append(f'{pc}的体质或体型没有设置，无法计算体力上限，请设置体质/体型')
    elif not '魔法' in pc_data:
        try:
            pc_data['魔法'] = int(pc_data['意志']/5)
        except:
            results.append(f'{pc}的意志没有设置，无法计算魔法上限，请设置意志')
    elif not '理智' in pc_data:
        try:
            pc_data['理智'] = int(pc_data['意志'])
        except:
            results.append(f'{pc}的意志没有设置，无法计算理智，请设置意志')
    elif not '闪避' in pc_data or pc_data['闪避'] < int(pc_data['敏捷']/2):
        try:
            pc_data['闪避'] = int(pc_data['敏捷']/2)
        except:
            results.append(f'{pc}的敏捷没有设置，无法计算闪避，请设置敏捷')
    st_data[member_openid][pc] = pc_data
    with open('./st_db.json','w',encoding="utf-8") as st_db:
        json.dump(st_data,st_db,ensure_ascii=False)
    return "\n".join(results)


def san_check(msg, member_openid):
    pc = get_now_tag_pc(member_openid)
    pc_data = get_st(pc, member_openid)
    parts = msg.split('sc')
    param = parts[1].strip()
    dices = param.split('/')
    san = format_attribute('san')
    value = pc_data[san]
    check = random.randint(1,100)
    pass_dice = dices[0]
    fail_dice = dices[1]
    try:
        pass_value = int(pass_dice)
    except:
        pass_value, expression = dice.dice_roll(pass_dice)
    try:
        fail_value = int(fail_dice)
    except:
        fail_value, expression = dice.dice_roll(fail_dice)
    if check <= value:
        value = pc_data[san] - pass_value
        st_update(san, value, member_openid)
        return f'{pc}的San Check：\n1D100={check}/{pc_data[san]}成功\n理智减少{pass_dice}={pass_value} -> 剩余{value}'
    else:
        value = pc_data[san] - fail_value
        st_update(san, value, member_openid)
        return f'{pc}的San Check：\n1D100={check}/{pc_data[san]}失败\n理智减少{fail_dice}={fail_value} -> 剩余{value}'


def en(msg, member_openid):
    pc = get_now_tag_pc(member_openid)
    pc_data = get_st(pc, member_openid)
    part = msg[2:].strip()
    attribute = format_attribute(part)
    illegal_list = ['力量','体力','敏捷','理智','魔法','外貌','体型','克苏鲁神话']
    if not attribute or attribute in illegal_list:
        return f'{part} 不是一个有效的技能名'
    check = random.randint(1,100)
    if not attribute in pc_data:
        value_o = get_st_default(attribute)
    else:
        value_o = pc_data[attribute]
    if value_o < check or check > 95:
        en_count = random.randint(1,10)
        value = value_o + en_count
        st_update(attribute,value,member_openid)
        return f'{pc}的{attribute}增强或成长检定:\n1D100={check}/{value_o}  成功\n{pc}的{attribute}增加1D10={en_count}点，当前为{value}点'
    else:
        return f'{pc}的{attribute}增强或成长检定:\n1D100={check}/{value_o}  失败\n{pc}的{attribute}没有变化'

