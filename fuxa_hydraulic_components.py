#!/usr/bin/env python3
"""
FUXA 液压支撑臂 - 使用内置组件(proc-eng/pipe/value/button)
修复版: 正确的事件格式 + 美化视觉 + 参数显示在元器件旁边
"""
import json, urllib.request, uuid

BASE_URL = 'http://localhost:1881'
DEVICE_ID = '0'

def sid():
    return uuid.uuid4().hex[:8]

def mk(prefix):
    return f'{prefix}{sid()}-{sid()}'

def tref(tag_id):
    """生成变量全路径引用"""
    return f's:{DEVICE_ID};{tag_id}'

# ============================================================
# Tags
# ============================================================
TAGS = {
    't_pump_running':      {'name':'pump_running',      'type':'boolean', 'init':'false',  'description':'泵运行'},
    't_valve_position':    {'name':'valve_position',    'type':'number',  'init':'0',      'description':'阀位 0中1左2右'},
    't_system_pressure':   {'name':'system_pressure',   'type':'number',  'init':'0',      'description':'压力MPa'},
    't_cylinder_position': {'name':'cylinder_position', 'type':'number',  'init':'0',      'description':'行程%'},
    't_oil_temperature':   {'name':'oil_temperature',   'type':'number',  'init':'25',     'description':'油温C'},
    't_oil_level':         {'name':'oil_level',         'type':'number',  'init':'85',     'description':'油位%'},
    't_cmd_action':        {'name':'cmd_action',        'type':'number',  'init':'0',      'description':'指令 0停1升2降'},
    't_flow_rate':         {'name':'flow_rate',         'type':'number',  'init':'0',      'description':'流量L/min'},
    't_motor_speed':       {'name':'motor_speed',       'type':'number',  'init':'0',      'description':'转速rpm'},
    't_alarm_status':      {'name':'alarm_status',      'type':'number',  'init':'0',      'description':'报警'},
}

# ============================================================
# 正确的 FUXA GaugeEvent 格式
# ============================================================
def make_set_value_event(variable_id, value):
    """创建正确的 FUXA 按钮点击设值事件"""
    return {
        'type': 'shapes.event-click',        # GaugeEventType.click
        'action': 'onSetValue',              # GaugeEventActionType key
        'actparam': str(value),              # 要设置的值
        'actoptions': {
            'variable': {
                'variableId': variable_id    # 目标变量
            }
        }
    }

# ============================================================
# 视图1: 液压原理图 (优化视觉)
# ============================================================
def build_schematic():
    items = {}
    s = []

    # 配色
    C_BG = '#FAFAFA'         # 背景
    C_PIPE = '#37474F'       # 管道边框
    C_PRESSURE = '#E65100'   # 压力管
    C_RETURN = '#607D8B'     # 回油管
    C_A = '#1E88E5'          # A管路
    C_B = '#FB8C00'          # B管路
    C_COMP = '#1565C0'       # 组件轮廓
    C_LABEL = '#37474F'      # 标签文字

    s.append(f'''<svg width="1400" height="800" viewBox="0 0 1400 800" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
<defs>
  <marker id="af" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">
    <path d="M0 0L10 5L0 10z" fill="{C_COMP}"/>
  </marker>
  <linearGradient id="gTank" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#E3F2FD"/>
    <stop offset="100%" stop-color="#BBDEFB"/>
  </linearGradient>
  <linearGradient id="gCyl" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#CFD8DC"/>
    <stop offset="100%" stop-color="#B0BEC5"/>
  </linearGradient>
</defs>
<g>
<title>Layer 1</title>
<rect fill="{C_BG}" width="1400" height="800" id="svg_bg"/>
''')

    # 标题
    s.append(f'<text x="700" y="38" text-anchor="middle" font-family="SimHei,Arial" font-size="22" fill="#0D47A1" font-weight="bold">液压支撑臂系统原理图</text>')

    # ====== 坐标系 ======
    # 油箱 (100,280)  电机 (260,340)  泵 (370,340)  溢流阀 (460,460)
    # 换向阀 (600,310)  液压缸 (900,200)  支撑臂 (1120,100)
    # 核心管线 y=280(高压)  y=520(回油)

    # ===== 管道先画(在底层) =====

    # 吸油管: 油箱底部 -> 泵入口
    p1 = mk('PIE_')
    s.append(f'''<g id="{p1}" type="svg-ext-pipe">
  <path d="M200,380 L310,380 L310,360 L360,360" fill="none" stroke="{C_PIPE}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M200,380 L310,380 L310,360 L360,360" fill="none" stroke="#90A4AE" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
</g>''')
    items[p1] = {'id':p1,'type':'svg-ext-pipe','name':'吸油管',
        'property':{'variableId':tref('t_pump_running'),
            'options':{'border':C_PIPE,'borderWidth':12,'pipe':'#90A4AE','pipeWidth':7,'content':'#64B5F6','contentWidth':4,'contentSpace':18}},
        'label':'Pipe','hide':False,'lock':False}

    # 压力管: 泵出口 -> T形分流 -> 换向阀P口
    p2 = mk('PIE_')
    s.append(f'''<g id="{p2}" type="svg-ext-pipe">
  <path d="M440,340 L470,340 L470,280 L640,280 L640,310" fill="none" stroke="{C_PIPE}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M440,340 L470,340 L470,280 L640,280 L640,310" fill="none" stroke="{C_PRESSURE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
</g>''')
    items[p2] = {'id':p2,'type':'svg-ext-pipe','name':'压力管',
        'property':{'variableId':tref('t_system_pressure'),
            'options':{'border':C_PIPE,'borderWidth':12,'pipe':C_PRESSURE,'pipeWidth':7,'content':'#FF5722','contentWidth':4,'contentSpace':18},
            'ranges':[{'min':5,'max':25,'color':'#FF5722','stroke':'#D84315'}]},
        'label':'Pipe','hide':False,'lock':False}

    # 溢流阀回油支路: 从压力管分出 -> 溢流阀 -> 油箱
    s.append(f'<path d="M470,340 L470,460 L380,460" fill="none" stroke="{C_PIPE}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>')
    s.append(f'<path d="M380,460 L200,460 L200,420" fill="none" stroke="{C_PIPE}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity="0.4"/>')

    # A管路: 换向阀A口 -> 液压缸A口(左)
    p3 = mk('PIE_')
    s.append(f'''<g id="{p3}" type="svg-ext-pipe">
  <path d="M620,310 L620,210 L900,210" fill="none" stroke="{C_PIPE}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M620,310 L620,210 L900,210" fill="none" stroke="{C_A}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
</g>''')
    items[p3] = {'id':p3,'type':'svg-ext-pipe','name':'A管路',
        'property':{'variableId':tref('t_valve_position'),
            'options':{'border':C_PIPE,'borderWidth':12,'pipe':C_A,'pipeWidth':7,'content':'#2196F3','contentWidth':4,'contentSpace':18},
            'ranges':[{'min':1,'max':1,'color':'#2196F3','stroke':'#1565C0'},{'min':2,'max':2,'color':'#FFB300','stroke':'#FF8F00'}]},
        'label':'Pipe','hide':False,'lock':False}

    # B管路: 换向阀B口 -> 液压缸B口(右)
    p4 = mk('PIE_')
    s.append(f'''<g id="{p4}" type="svg-ext-pipe">
  <path d="M660,310 L660,170 L1060,170 L1060,210" fill="none" stroke="{C_PIPE}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M660,310 L660,170 L1060,170 L1060,210" fill="none" stroke="{C_B}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
</g>''')
    items[p4] = {'id':p4,'type':'svg-ext-pipe','name':'B管路',
        'property':{'variableId':tref('t_valve_position'),
            'options':{'border':C_PIPE,'borderWidth':12,'pipe':C_B,'pipeWidth':7,'content':'#FF8F00','contentWidth':4,'contentSpace':18},
            'ranges':[{'min':1,'max':1,'color':'#FFB300','stroke':'#FF8F00'},{'min':2,'max':2,'color':'#2196F3','stroke':'#1565C0'}]},
        'label':'Pipe','hide':False,'lock':False}

    # 回油管: 换向阀T口 -> 油箱
    p5 = mk('PIE_')
    s.append(f'''<g id="{p5}" type="svg-ext-pipe">
  <path d="M640,370 L640,520 L200,520 L200,420" fill="none" stroke="{C_PIPE}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M640,370 L640,520 L200,520 L200,420" fill="none" stroke="{C_RETURN}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
</g>''')
    items[p5] = {'id':p5,'type':'svg-ext-pipe','name':'回油管',
        'property':{'variableId':tref('t_pump_running'),
            'options':{'border':C_PIPE,'borderWidth':12,'pipe':C_RETURN,'pipeWidth':7,'content':'#90A4AE','contentWidth':4,'contentSpace':18}},
        'label':'Pipe','hide':False,'lock':False}

    # ===== 油箱 =====
    tank_id = mk('proceng-')
    s.append(f'''<g id="{tank_id}" type="svg-ext-proceng-tank5">
  <rect x="80" y="280" width="120" height="160" rx="6" fill="url(#gTank)" stroke="{C_COMP}" stroke-width="2.5"/>
  <line x1="80" y1="310" x2="200" y2="310" stroke="{C_COMP}" stroke-width="1.5"/>
  <line x1="80" y1="410" x2="200" y2="410" stroke="{C_COMP}" stroke-width="1.5"/>
  <rect x="90" y="340" width="100" height="65" fill="#FFB300" opacity="0.35" rx="3"/>
</g>''')
    items[tank_id] = {'id':tank_id,'type':'svg-ext-proceng','name':'油箱',
        'property':{'variableId':tref('t_oil_level'),
            'ranges':[{'min':0,'max':30,'color':'#FFCDD2','stroke':'#E53935'},
                      {'min':30,'max':60,'color':'#FFF9C4','stroke':'#F9A825'},
                      {'min':60,'max':100,'color':'#C8E6C9','stroke':'#43A047'}]},
        'label':'ProcEng','hide':False,'lock':False}
    s.append(f'<text x="140" y="275" text-anchor="middle" font-family="SimHei" font-size="14" fill="{C_LABEL}" font-weight="bold">油箱</text>')

    # 油箱旁数据: 油位 + 油温
    vOL = mk('VAL_')
    s.append(f'<g id="{vOL}"><text x="140" y="395" text-anchor="middle" font-family="Consolas" font-size="13" fill="#E65100"><tspan>85</tspan></text></g>')
    items[vOL] = {'id':vOL,'type':'svg-ext-value','name':'油位',
        'property':{'variableId':tref('t_oil_level'),'unit':' %','digits':0}, 'label':'Value','hide':False,'lock':False}
    vOT = mk('VAL_')
    s.append(f'<g id="{vOT}"><text x="140" y="455" text-anchor="middle" font-family="Consolas" font-size="12" fill="#455A64"><tspan>25</tspan></text></g>')
    items[vOT] = {'id':vOT,'type':'svg-ext-value','name':'油温',
        'property':{'variableId':tref('t_oil_temperature'),'unit':' °C','digits':0}, 'label':'Value','hide':False,'lock':False}
    s.append('<text x="140" y="470" text-anchor="middle" font-family="SimHei" font-size="10" fill="#999">油温</text>')

    # ===== 电机 =====
    motor_id = mk('proceng-')
    mx, my = 280, 320
    s.append(f'''<g id="{motor_id}" type="svg-ext-proceng-motor">
  <circle cx="{mx}" cy="{my+20}" r="28" fill="#E3F2FD" stroke="{C_COMP}" stroke-width="2.5"/>
  <path d="M{mx} {my-6} L{mx+24} {my+20} L{mx} {my+46}Z" fill="{C_COMP}" opacity="0.6"/>
  <text x="{mx}" y="{my+25}" text-anchor="middle" font-family="Arial" font-size="16" fill="{C_COMP}" font-weight="bold">M</text>
</g>''')
    items[motor_id] = {'id':motor_id,'type':'svg-ext-proceng','name':'电机',
        'property':{'variableId':tref('t_pump_running'),
            'ranges':[{'min':0,'max':0,'color':'#ECEFF1','stroke':'#90A4AE'},
                      {'min':1,'max':1,'color':'#C8E6C9','stroke':'#2E7D32'}],
            'actions':[{'variableId':tref('t_pump_running'),'type':'clockwise','range':{'min':1,'max':1}}]},
        'label':'ProcEng','hide':False,'lock':False}
    s.append(f'<text x="{mx}" y="{my-14}" text-anchor="middle" font-family="SimHei" font-size="13" fill="{C_LABEL}">电机</text>')

    # 电机旁数据: 转速
    vMS = mk('VAL_')
    s.append(f'<g id="{vMS}"><text x="{mx}" y="{my+62}" text-anchor="middle" font-family="Consolas" font-size="11" fill="#1565C0"><tspan>0</tspan></text></g>')
    items[vMS] = {'id':vMS,'type':'svg-ext-value','name':'转速',
        'property':{'variableId':tref('t_motor_speed'),'unit':' rpm','digits':0}, 'label':'Value','hide':False,'lock':False}

    # 电机-泵连线
    s.append(f'<line x1="{mx+28}" y1="{my+20}" x2="360" y2="{my+20}" stroke="#455A64" stroke-width="5" stroke-dasharray="10,5"/>')

    # ===== 液压泵 =====
    pump_id = mk('proceng-')
    px, py = 400, 320
    s.append(f'''<g id="{pump_id}" type="svg-ext-proceng-pumphidra">
  <circle cx="{px}" cy="{py+20}" r="28" fill="#E3F2FD" stroke="{C_COMP}" stroke-width="2.5"/>
  <path d="M{px-24} {py+20} L{px} {py-6} L{px+24} {py+20}" fill="none" stroke="{C_COMP}" stroke-width="2.5"/>
</g>''')
    items[pump_id] = {'id':pump_id,'type':'svg-ext-proceng','name':'液压泵',
        'property':{'variableId':tref('t_pump_running'),
            'ranges':[{'min':0,'max':0,'color':'#ECEFF1','stroke':'#90A4AE'},
                      {'min':1,'max':1,'color':'#BBDEFB','stroke':'#1565C0'}],
            'actions':[{'variableId':tref('t_pump_running'),'type':'clockwise','range':{'min':1,'max':1}}]},
        'label':'ProcEng','hide':False,'lock':False}
    s.append(f'<text x="{px}" y="{py-14}" text-anchor="middle" font-family="SimHei" font-size="13" fill="{C_LABEL}">液压泵</text>')

    # 泵旁数据: 流量
    vFR = mk('VAL_')
    s.append(f'<g id="{vFR}"><text x="{px}" y="{py+62}" text-anchor="middle" font-family="Consolas" font-size="11" fill="#E65100"><tspan>0</tspan></text></g>')
    items[vFR] = {'id':vFR,'type':'svg-ext-value','name':'流量',
        'property':{'variableId':tref('t_flow_rate'),'unit':' L/min','digits':1}, 'label':'Value','hide':False,'lock':False}

    # ===== 压力表 =====
    vP = mk('VAL_')
    gx, gy = 500, 250
    s.append(f'''<circle cx="{gx}" cy="{gy}" r="24" fill="#fff" stroke="{C_COMP}" stroke-width="2.5"/>
<text x="{gx}" y="{gy+28}" text-anchor="middle" font-family="SimHei" font-size="10" fill="#888">P (MPa)</text>
<g id="{vP}"><text x="{gx}" y="{gy+5}" text-anchor="middle" font-family="Consolas" font-size="16" fill="#D84315" font-weight="bold"><tspan>0</tspan></text></g>''')
    items[vP] = {'id':vP,'type':'svg-ext-value','name':'压力',
        'property':{'variableId':tref('t_system_pressure'),'unit':'','digits':1}, 'label':'Value','hide':False,'lock':False}

    # ===== 溢流阀 =====
    rv_id = mk('proceng-')
    rvx, rvy = 465, 430
    s.append(f'''<g id="{rv_id}" type="svg-ext-proceng-valveax" transform="translate({rvx},{rvy}) rotate(90,20,12) scale(1.5)">
  <path d="M0 0L20 12L0 24Z M40 0L20 12L40 24Z" fill="none" stroke="#BF360C" stroke-width="1.5"/>
</g>''')
    items[rv_id] = {'id':rv_id,'type':'svg-ext-proceng','name':'溢流阀',
        'property':{'variableId':tref('t_system_pressure'),
            'ranges':[{'min':0,'max':15,'color':'#E8F5E9','stroke':'#43A047'},
                      {'min':15,'max':25,'color':'#FFCDD2','stroke':'#E53935'}]},
        'label':'ProcEng','hide':False,'lock':False}
    s.append(f'<text x="{rvx+18}" y="{rvy+55}" text-anchor="middle" font-family="SimHei" font-size="12" fill="{C_LABEL}">溢流阀</text>')

    # ===== 三位四通换向阀 =====
    valve_id = mk('proceng-')
    vvx, vvy = 590, 310
    bw = 50 # 单格宽度
    s.append(f'''<g id="{valve_id}" type="svg-ext-proceng-valvecx">
  <!-- 左位 升起 -->
  <rect x="{vvx}" y="{vvy}" width="{bw}" height="{bw}" fill="#E8F5E9" stroke="{C_COMP}" stroke-width="1.5" rx="2"/>
  <line x1="{vvx+5}" y1="{vvy+12}" x2="{vvx+bw-5}" y2="{vvy+bw-12}" stroke="{C_COMP}" stroke-width="1.2" marker-end="url(#af)"/>
  <line x1="{vvx+5}" y1="{vvy+bw-12}" x2="{vvx+bw-5}" y2="{vvy+12}" stroke="{C_COMP}" stroke-width="1.2" marker-end="url(#af)"/>
  <!-- 中位 停止 -->
  <rect x="{vvx+bw}" y="{vvy}" width="{bw}" height="{bw}" fill="#ECEFF1" stroke="{C_COMP}" stroke-width="1.5" rx="2"/>
  <line x1="{vvx+bw+15}" y1="{vvy+12}" x2="{vvx+bw+15}" y2="{vvy+18}" stroke="{C_COMP}" stroke-width="1.2"/>
  <line x1="{vvx+bw+35}" y1="{vvy+12}" x2="{vvx+bw+35}" y2="{vvy+18}" stroke="{C_COMP}" stroke-width="1.2"/>
  <line x1="{vvx+bw+15}" y1="{vvy+32}" x2="{vvx+bw+15}" y2="{vvy+38}" stroke="{C_COMP}" stroke-width="1.2"/>
  <line x1="{vvx+bw+35}" y1="{vvy+32}" x2="{vvx+bw+35}" y2="{vvy+38}" stroke="{C_COMP}" stroke-width="1.2"/>
  <!-- 右位 降落 -->
  <rect x="{vvx+2*bw}" y="{vvy}" width="{bw}" height="{bw}" fill="#FFF3E0" stroke="{C_COMP}" stroke-width="1.5" rx="2"/>
  <line x1="{vvx+2*bw+5}" y1="{vvy+12}" x2="{vvx+3*bw-5}" y2="{vvy+12}" stroke="{C_COMP}" stroke-width="1.2" marker-end="url(#af)"/>
  <line x1="{vvx+3*bw-5}" y1="{vvy+bw-12}" x2="{vvx+2*bw+5}" y2="{vvy+bw-12}" stroke="{C_COMP}" stroke-width="1.2" marker-end="url(#af)"/>
  <!-- 端口标注 -->
  <text x="{vvx+15}" y="{vvy-6}" font-family="Arial" font-size="11" fill="{C_A}" font-weight="bold">A</text>
  <text x="{vvx+bw+28}" y="{vvy-6}" font-family="Arial" font-size="11" fill="{C_B}" font-weight="bold">B</text>
  <text x="{vvx+bw+22}" y="{vvy+bw+15}" font-family="Arial" font-size="11" fill="{C_PRESSURE}" font-weight="bold">P</text>
  <text x="{vvx+bw+22}" y="{vvy+bw+30}" font-family="Arial" font-size="11" fill="{C_RETURN}" font-weight="bold">T</text>
</g>''')
    items[valve_id] = {'id':valve_id,'type':'svg-ext-proceng','name':'换向阀',
        'property':{'variableId':tref('t_valve_position'),
            'ranges':[{'min':0,'max':0,'color':'#ECEFF1','stroke':C_COMP},
                      {'min':1,'max':1,'color':'#A5D6A7','stroke':'#2E7D32'},
                      {'min':2,'max':2,'color':'#FFE0B2','stroke':'#E65100'}],
            'actions':[{'variableId':tref('t_valve_position'),'type':'blink','range':{'min':1,'max':2},
                        'options':{'fillA':'#C8E6C9','fillB':'#FFF9C4','interval':800}}]},
        'label':'ProcEng','hide':False,'lock':False}
    s.append(f'<text x="{vvx+75}" y="{vvy+bw+44}" text-anchor="middle" font-family="SimHei" font-size="13" fill="{C_LABEL}" font-weight="bold">三位四通换向阀</text>')

    # ===== 液压缸 =====
    cyl_id = mk('proceng-')
    ccx, ccy = 900, 190
    cw, ch = 160, 60
    s.append(f'''<g id="{cyl_id}" type="svg-ext-proceng">
  <rect x="{ccx}" y="{ccy}" width="{cw}" height="{ch}" fill="url(#gCyl)" stroke="{C_COMP}" stroke-width="2.5" rx="4"/>
  <rect x="{ccx+cw-25}" y="{ccy+5}" width="12" height="{ch-10}" fill="#78909C" stroke="#455A64" stroke-width="1"/>
  <rect x="{ccx+cw-15}" y="{ccy+18}" width="100" height="{ch-36}" fill="#B0BEC5" stroke="#78909C" stroke-width="1.5" rx="2"/>
  <text x="{ccx-12}" y="{ccy+ch//2+5}" text-anchor="end" font-family="Arial" font-size="12" fill="{C_A}" font-weight="bold">A</text>
  <text x="{ccx+cw+115}" y="{ccy+ch//2+5}" font-family="Arial" font-size="12" fill="{C_B}" font-weight="bold">B</text>
</g>''')
    items[cyl_id] = {'id':cyl_id,'type':'svg-ext-proceng','name':'液压缸',
        'property':{'variableId':tref('t_cylinder_position'),
            'ranges':[{'min':0,'max':30,'color':'#E3F2FD','stroke':C_COMP},
                      {'min':30,'max':70,'color':'#BBDEFB','stroke':C_COMP},
                      {'min':70,'max':100,'color':'#90CAF9','stroke':'#0D47A1'}]},
        'label':'ProcEng','hide':False,'lock':False}
    s.append(f'<text x="{ccx+cw//2}" y="{ccy-10}" text-anchor="middle" font-family="SimHei" font-size="14" fill="{C_LABEL}" font-weight="bold">液压缸</text>')

    # 缸旁数据: 行程
    vCP = mk('VAL_')
    s.append(f'<g id="{vCP}"><text x="{ccx+cw//2}" y="{ccy+ch+22}" text-anchor="middle" font-family="Consolas" font-size="14" fill="{C_COMP}" font-weight="bold"><tspan>0</tspan></text></g>')
    items[vCP] = {'id':vCP,'type':'svg-ext-value','name':'行程',
        'property':{'variableId':tref('t_cylinder_position'),'unit':' %','digits':0}, 'label':'Value','hide':False,'lock':False}

    # ===== 支撑臂简图 =====
    ax, ay = 1150, 100
    s.append(f'''<g>
  <rect x="{ax-30}" y="{ay+150}" width="80" height="25" fill="#78909C" stroke="#455A64" stroke-width="1.5" rx="4"/>
  <text x="{ax+10}" y="{ay+167}" text-anchor="middle" font-family="SimHei" font-size="10" fill="#fff">底座</text>
  <line x1="{ax+10}" y1="{ay+150}" x2="{ax+10}" y2="{ay+110}" stroke="#455A64" stroke-width="4" stroke-linecap="round"/>
  <line x1="{ax+10}" y1="{ay+110}" x2="{ax+100}" y2="{ay+60}" stroke="#455A64" stroke-width="3" stroke-linecap="round"/>
  <circle cx="{ax+10}" cy="{ay+110}" r="6" fill="#FFB300" stroke="#FF8F00" stroke-width="1.5"/>
  <circle cx="{ax+100}" cy="{ay+60}" r="4" fill="#E53935" stroke="#B71C1C" stroke-width="1"/>
  <text x="{ax+108}" y="{ay+58}" font-family="SimHei" font-size="10" fill="#333">臂端</text>
  <text x="{ax+35}" y="{ay+200}" text-anchor="middle" font-family="SimHei" font-size="13" fill="{C_LABEL}">支撑臂</text>
</g>''')

    # ===== 图例 =====
    lx, ly = 60, 620
    s.append(f'''<rect x="{lx}" y="{ly}" width="300" height="110" fill="#fff" stroke="#E0E0E0" stroke-width="1" rx="6"/>
<text x="{lx+150}" y="{ly+20}" text-anchor="middle" font-family="SimHei" font-size="13" fill="#333" font-weight="bold">管路图例</text>
<line x1="{lx+20}" y1="{ly+40}" x2="{lx+80}" y2="{ly+40}" stroke="{C_PRESSURE}" stroke-width="4"/>
<text x="{lx+90}" y="{ly+44}" font-family="SimHei" font-size="11" fill="#666">压力管路 (P)</text>
<line x1="{lx+20}" y1="{ly+60}" x2="{lx+80}" y2="{ly+60}" stroke="{C_A}" stroke-width="4"/>
<text x="{lx+90}" y="{ly+64}" font-family="SimHei" font-size="11" fill="#666">A管路 (工作口A)</text>
<line x1="{lx+20}" y1="{ly+80}" x2="{lx+80}" y2="{ly+80}" stroke="{C_B}" stroke-width="4"/>
<text x="{lx+90}" y="{ly+84}" font-family="SimHei" font-size="11" fill="#666">B管路 (工作口B)</text>
<line x1="{lx+20}" y1="{ly+100}" x2="{lx+80}" y2="{ly+100}" stroke="{C_RETURN}" stroke-width="4"/>
<text x="{lx+90}" y="{ly+104}" font-family="SimHei" font-size="11" fill="#666">回油管路 (T)</text>
''')

    s.append('</g>\n</svg>')
    return '\n'.join(s), items


# ============================================================
# 视图2: 操作控制面板
# ============================================================
def build_control():
    items = {}
    s = []

    s.append('''<svg width="900" height="500" viewBox="0 0 900 500" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
<g>
<title>Layer 1</title>
<rect fill="#1a237e" width="900" height="500" rx="0"/>
<rect x="10" y="10" width="880" height="480" fill="#263238" rx="12"/>
''')

    s.append('<text x="450" y="50" text-anchor="middle" font-family="SimHei" font-size="22" fill="#ECEFF1" font-weight="bold">液压支撑臂 - 操作控制台</text>')
    s.append('<line x1="60" y1="65" x2="840" y2="65" stroke="#37474F" stroke-width="1"/>')

    # ===== 按钮 =====
    btns = [
        ('升起', '#2E7D32', '#1B5E20', '1', 130),
        ('停止', '#E65100', '#BF360C', '0', 380),
        ('降落', '#C62828', '#B71C1C', '2', 630),
    ]

    for label, bg, border, val, bx in btns:
        bid = mk('HXB_')
        bhx = sid()
        s.append(f'''<g id="{bid}">
  <rect id="svg_{sid()}" x="{bx}" y="85" width="160" height="65" fill="{bg}" stroke="{border}" stroke-width="2" rx="10"/>
  <foreignObject x="{bx}" y="85" width="160" height="65">
    <div id="B-HXB_{bhx}" xmlns="http://www.w3.org/1999/xhtml"
         style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;
                color:#fff;font-family:SimHei,Arial;font-size:20px;font-weight:bold;cursor:pointer;
                background-color:{bg};border-radius:10px;user-select:none;">{label}</div>
  </foreignObject>
</g>''')
        items[bid] = {
            'id': bid, 'type': 'svg-ext-html_button', 'name': f'{label}按钮',
            'property': {
                'text': label,
                'events': [make_set_value_event(tref('t_cmd_action'), val)]
            },
            'label': 'HtmlButton', 'hide': False, 'lock': False
        }

    # ===== 指示灯 =====
    indicators = [
        ('泵运行', 't_pump_running', 180, [{'min':0,'max':0,'color':'#424242','stroke':'#212121'},{'min':1,'max':1,'color':'#4CAF50','stroke':'#2E7D32'}]),
        ('报警', 't_alarm_status', 450, [{'min':0,'max':0,'color':'#424242','stroke':'#212121'},{'min':1,'max':99,'color':'#F44336','stroke':'#C62828'}]),
        ('阀动作', 't_valve_position', 720, [{'min':0,'max':0,'color':'#424242','stroke':'#212121'},{'min':1,'max':1,'color':'#4CAF50','stroke':'#2E7D32'},{'min':2,'max':2,'color':'#FFB300','stroke':'#F57F17'}]),
    ]

    s.append('<text x="450" y="195" text-anchor="middle" font-family="SimHei" font-size="15" fill="#78909C">系统状态</text>')
    for label, tag, ix, ranges in indicators:
        sem_id = mk('SEM_')
        s.append(f'''<g id="{sem_id}">
  <circle cx="{ix}" cy="230" r="18" fill="#424242" stroke="#333" stroke-width="2.5"/>
</g>
<text x="{ix}" y="262" text-anchor="middle" font-family="SimHei" font-size="11" fill="#90A4AE">{label}</text>''')
        items[sem_id] = {'id':sem_id,'type':'svg-ext-gauge_semaphore','name':f'{label}灯',
            'property':{'variableId':tref(tag),'ranges':ranges},
            'label':'GaugeSemaphore','hide':False,'lock':False}

    # ===== 数据卡片 =====
    s.append('<text x="450" y="300" text-anchor="middle" font-family="SimHei" font-size="15" fill="#78909C">运行数据</text>')

    cards = [
        ('系统压力','t_system_pressure','MPa',1),
        ('油温','t_oil_temperature','°C',0),
        ('油位','t_oil_level','%',0),
        ('流量','t_flow_rate','L/min',1),
        ('电机转速','t_motor_speed','rpm',0),
        ('缸行程','t_cylinder_position','%',0),
    ]
    for i, (label, tag, unit, digits) in enumerate(cards):
        col, row = i % 3, i // 3
        cx = 65 + col * 270
        cy = 315 + row * 88

        vid = mk('VAL_')
        s.append(f'''<rect x="{cx}" y="{cy}" width="230" height="75" fill="#37474F" stroke="#455A64" stroke-width="1" rx="8"/>
<text x="{cx+115}" y="{cy+20}" text-anchor="middle" font-family="SimHei" font-size="12" fill="#78909C">{label}</text>
<g id="{vid}"><text x="{cx+95}" y="{cy+50}" text-anchor="middle" font-family="Consolas" font-size="26" fill="#4FC3F7" font-weight="bold"><tspan>--</tspan></text></g>
<text x="{cx+180}" y="{cy+50}" font-family="Arial" font-size="13" fill="#607D8B">{unit}</text>''')
        items[vid] = {'id':vid,'type':'svg-ext-value','name':label,
            'property':{'variableId':tref(tag),'unit':'','digits':digits},
            'label':'Value','hide':False,'lock':False}

    s.append('</g>\n</svg>')
    return '\n'.join(s), items


# ============================================================
# Mock 脚本
# ============================================================
MOCK_SCRIPT = {
    'id': 'script_hydraulic_mock',
    'name': '液压模拟',
    'mode': 'server',
    'scheduling': 'interval',
    'interval': 1,
    'code': '''
var cmd = Number($getTag('cmd_action')) || 0;
var cylPos = Number($getTag('cylinder_position')) || 0;
var oilTemp = Number($getTag('oil_temperature')) || 25;
var pump = false, valvePos = 0, pressure = 0, flow = 0, rpm = 0;

if (cmd === 1) {
    pump = true; valvePos = 1;
    pressure = 12 + Math.random() * 2;
    flow = 18 + Math.random() * 4;
    rpm = 1450 + Math.floor(Math.random() * 50);
    if (cylPos < 100) cylPos = Math.min(100, cylPos + 2);
} else if (cmd === 2) {
    pump = true; valvePos = 2;
    pressure = 8 + Math.random() * 2;
    flow = 15 + Math.random() * 3;
    rpm = 1450 + Math.floor(Math.random() * 50);
    if (cylPos > 0) cylPos = Math.max(0, cylPos - 2);
} else {
    pump = false; valvePos = 0;
    pressure = 0; flow = 0; rpm = 0;
}

oilTemp = pump ? Math.min(65, oilTemp + 0.1) : Math.max(25, oilTemp - 0.05);

$setTag('pump_running', pump);
$setTag('valve_position', valvePos);
$setTag('system_pressure', Math.round(pressure * 10) / 10);
$setTag('cylinder_position', Math.round(cylPos));
$setTag('flow_rate', Math.round(flow * 10) / 10);
$setTag('motor_speed', Math.round(rpm));
$setTag('oil_temperature', Math.round(oilTemp * 10) / 10);
$setTag('oil_level', Math.max(60, 85 - cylPos * 0.15));
$setTag('alarm_status', pressure > 20 ? 1 : (oilTemp > 60 ? 2 : 0));
'''
}


# ============================================================
# 部署
# ============================================================
def deploy():
    print('=== 部署液压系统 v2 (优化版) ===')

    req = urllib.request.Request(f'{BASE_URL}/api/project')
    resp = urllib.request.urlopen(req, timeout=10)
    project = json.loads(resp.read())

    # 更新 Tags
    device = project.get('devices',{}).get(DEVICE_ID,{})
    for tid, td in TAGS.items():
        device['tags'][tid] = {
            'id':tid,'name':td['name'],'type':td['type'],'address':td['name'],
            'init':td['init'],'description':td['description'],
            'daq':{'enabled':False,'changed':False,'interval':60,'restored':False}
        }
    print(f'Tags: {len(TAGS)}')

    sch_svg, sch_items = build_schematic()
    ctl_svg, ctl_items = build_control()
    print(f'原理图: {len(sch_items)} items, {len(sch_svg)} chars')
    print(f'控制面板: {len(ctl_items)} items, {len(ctl_svg)} chars')

    views = [v for v in project['hmi']['views']
             if v['id'] not in ['v_hydraulic_schematic','v_hydraulic_control','v_hydraulic_arm_01']]

    views.append({'id':'v_hydraulic_schematic','name':'液压原理图',
        'profile':{'width':1400,'height':800,'bkcolor':'#FAFAFA'},
        'svgcontent':sch_svg,'items':sch_items})
    views.append({'id':'v_hydraulic_control','name':'操作控制面板',
        'profile':{'width':900,'height':500,'bkcolor':'#263238'},
        'svgcontent':ctl_svg,'items':ctl_items})

    project['hmi']['views'] = views
    project['hmi']['layout'] = {
        'start': 'v_hydraulic_schematic',
        'navigation': {
            'bkcolor':'#0D47A1','fgcolor':'#FFFFFF',
            'items':[{'text':'液压原理图','view':'v_hydraulic_schematic','icon':'schema'},
                     {'text':'操作面板','view':'v_hydraulic_control','icon':'gamepad'}],
            'mode':'over'},
        'header':{'bkcolor':'#0D47A1','fgcolor':'#FFFFFF','title':'液压支撑臂控制系统','alarms':'fix'},
        'showDev':True,'zoom':'autoresize'
    }

    # Mock脚本
    if isinstance(project.get('scripts'), list):
        project['scripts'] = [s for s in project['scripts'] if s.get('id') != MOCK_SCRIPT['id']]
        project['scripts'].append(MOCK_SCRIPT)
    else:
        project['scripts'] = [MOCK_SCRIPT]

    body = json.dumps(project).encode('utf-8')
    print(f'POST: {len(body)} bytes')
    req = urllib.request.Request(f'{BASE_URL}/api/project', data=body,
        headers={'Content-Type':'application/json'}, method='POST')
    resp = urllib.request.urlopen(req, timeout=60)
    print(f'HTTP {resp.status}')

    # 验证
    req = urllib.request.Request(f'{BASE_URL}/api/project')
    resp = urllib.request.urlopen(req, timeout=10)
    proj = json.loads(resp.read())
    for v in proj['hmi']['views']:
        ic = len(v.get('items',{}))
        print(f'  {v["id"]} ({v["name"]}) - {ic} 组件')

    print(f'\n完成! 请刷新 {BASE_URL}')

if __name__ == '__main__':
    deploy()
