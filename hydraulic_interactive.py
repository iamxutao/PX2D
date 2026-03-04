#!/usr/bin/env python3
"""
交互式 ISO 1219 标准液压原理图 (现代智控增强版)
- 保留标准液压符号(白底黑线为主, 结构清晰)
- 重构操作控制面板(深色科技工业风)
- 强化动作关联、发光状态指示和多维数字监测
"""
import urllib.request, json, time

BASE_URL = 'http://localhost:1881'

svg = '''<svg width="1920" height="1080" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
 <defs>
  <!-- 箭头定义 -->
  <marker id="arrB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
   <path d="M 0 0 L 10 5 L 0 10 z" fill="#1565C0"/>
  </marker>
  <marker id="arrO" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
   <path d="M 0 0 L 10 5 L 0 10 z" fill="#E65100"/>
  </marker>
  
  <!-- UI 阴影与发光效果 -->
  <filter id="panelShadow" x="-5%" y="-5%" width="110%" height="110%">
   <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000" flood-opacity="0.3"/>
  </filter>
  <filter id="glowGreen" x="-20%" y="-20%" width="140%" height="140%">
   <feGaussianBlur stdDeviation="3" result="blur"/>
   <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>
  <filter id="glowRed" x="-20%" y="-20%" width="140%" height="140%">
   <feGaussianBlur stdDeviation="3" result="blur"/>
   <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>
  <filter id="glowBlue" x="-20%" y="-20%" width="140%" height="140%">
   <feGaussianBlur stdDeviation="3" result="blur"/>
   <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>

  <!-- 面板渐变 -->
  <linearGradient id="panelBg" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#1E293B"/>
   <stop offset="100%" stop-color="#0F172A"/>
  </linearGradient>
  <linearGradient id="btnUpBg" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#10B981"/>
   <stop offset="100%" stop-color="#059669"/>
  </linearGradient>
  <linearGradient id="btnDnBg" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#EF4444"/>
   <stop offset="100%" stop-color="#DC2626"/>
  </linearGradient>
  <linearGradient id="btnStBg" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#64748B"/>
   <stop offset="100%" stop-color="#475569"/>
  </linearGradient>
 </defs>

 <g>
  <!-- 背景: 物理层浅灰色 -->
  <rect id="svg_bg" fill="#F8FAFC" width="1920" height="1080"/>

  <!-- ========== 标题栏 ========== -->
  <rect x="0" y="0" width="1920" height="60" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="2"/>
  <text x="960" y="38" text-anchor="middle" font-family="SimHei,Arial" font-size="24" fill="#1E293B" font-weight="bold" letter-spacing="2">智能液压系统 (HD-ISO-01)</text>
  <line x1="0" y1="60" x2="1920" y2="60" stroke="#CBD5E1" stroke-width="3"/>

  <!-- =================================================================== -->
  <!-- 物理原理图区 (ISO标准元件) -->
  <g transform="translate(150, 60)">
   
   <!-- == 流体管路层 (放置底层) == -->
   <!-- P主管 -->
   <line id="pressMain" x1="130" y1="180" x2="650" y2="180" stroke="#1565C0" stroke-width="4"/>
   <line id="flowP" x1="130" y1="180" x2="650" y2="180" stroke="#90CAF9" stroke-width="2.5" stroke-dasharray="15 10" opacity="0">
    <animate attributeName="stroke-dashoffset" from="0" to="-25" dur="0.6s" repeatCount="indefinite"/>
   </line>
   <text x="350" y="170" text-anchor="middle" font-family="Arial" font-size="11" fill="#1565C0" font-weight="bold">P (主压力油路 15MPa)</text>

   <!-- T主管 -->
   <line id="retMain" x1="130" y1="460" x2="750" y2="460" stroke="#E65100" stroke-width="4"/>
   <line id="flowR" x1="750" y1="460" x2="130" y2="460" stroke="#FFCC80" stroke-width="2.5" stroke-dasharray="15 10" opacity="0">
    <animate attributeName="stroke-dashoffset" from="0" to="-25" dur="0.6s" repeatCount="indefinite"/>
   </line>
   <text x="450" y="450" text-anchor="middle" font-family="Arial" font-size="11" fill="#E65100" font-weight="bold">T (主回油路)</text>

   <!-- == A/B 操作管路 == -->
   <line id="pipeA1" x1="623" y1="210" x2="623" y2="120" stroke="#94A3B8" stroke-width="4"/>
   <line id="pipeA2" x1="623" y1="120" x2="920" y2="120" stroke="#94A3B8" stroke-width="4"/>
   <line id="pipeA3" x1="920" y1="120" x2="920" y2="175" stroke="#94A3B8" stroke-width="4"/>
   <!-- A动画 -->
   <path id="flowA" d="M 623 210 L 623 120 L 920 120 L 920 175" fill="none" stroke="#FFF" stroke-width="2.5" stroke-dasharray="15 10" opacity="0">
    <animate id="animFlowA" attributeName="stroke-dashoffset" from="0" to="-25" dur="0.8s" repeatCount="indefinite"/>
   </path>
   <text x="770" y="110" text-anchor="middle" font-family="Arial" font-size="11" fill="#64748B" font-weight="bold">A 口联结</text>

   <line id="pipeB1" x1="637" y1="210" x2="637" y2="80" stroke="#94A3B8" stroke-width="4"/>
   <line id="pipeB2" x1="637" y1="80" x2="1080" y2="80" stroke="#94A3B8" stroke-width="4"/>
   <line id="pipeB3" x1="1080" y1="80" x2="1080" y2="175" stroke="#94A3B8" stroke-width="4"/>
   <!-- B动画 -->
   <path id="flowB" d="M 637 210 L 637 80 L 1080 80 L 1080 175" fill="none" stroke="#FFF" stroke-width="2.5" stroke-dasharray="15 10" opacity="0">
    <animate id="animFlowB" attributeName="stroke-dashoffset" from="0" to="-25" dur="0.8s" repeatCount="indefinite"/>
   </path>
   <text x="858" y="70" text-anchor="middle" font-family="Arial" font-size="11" fill="#64748B" font-weight="bold">B 口联结</text>

   <!-- == 动力源区 == -->
   <!-- 油箱 T -->
   <path d="M 90 480 L 170 480 M 97 480 L 105 510 M 105 510 L 155 510 M 155 510 L 163 480" stroke="#1E293B" stroke-width="3" fill="none"/>
   <text x="130" y="530" text-anchor="middle" font-family="SimHei,Arial" font-size="13" fill="#334155" font-weight="bold">系统油箱 T 200L</text>
   <line x1="130" y1="480" x2="130" y2="460" stroke="#E65100" stroke-width="4"/> <!-- 主机回油 -->
   <line x1="130" y1="460" x2="130" y2="410" stroke="#1565C0" stroke-width="4"/> <!-- 泵吸油 -->
   <!-- 吸油动画 -->
   <line id="flowS" x1="130" y1="480" x2="130" y2="410" stroke="#90CAF9" stroke-width="2.5" stroke-dasharray="10 8" opacity="0">
    <animate attributeName="stroke-dashoffset" from="0" to="18" dur="0.4s" repeatCount="indefinite"/>
   </line>

   <!-- 电动机 -->
   <circle cx="130" cy="380" r="26" fill="#F1F5F9" stroke="#1E293B" stroke-width="3"/>
   <text x="130" y="386" text-anchor="middle" font-family="Arial" font-size="18" fill="#1E293B" font-weight="bold">M</text>
   <text x="60" y="385" text-anchor="end" font-family="SimHei,Arial" font-size="12" fill="#334155" font-weight="bold">7.5kW 电机</text>
   <line x1="130" y1="354" x2="130" y2="306" stroke="#1E293B" stroke-width="4"/> <!-- 联轴器 -->
   <line x1="120" y1="330" x2="140" y2="330" stroke="#1E293B" stroke-width="3"/>

   <!-- 泵 -->
   <circle cx="130" cy="280" r="26" fill="#F1F5F9" stroke="#1E293B" stroke-width="3"/>
   <polygon points="120,298 130,262 140,298" fill="#1E293B"/> <!-- 恒定量黑三角 -->
   <text x="60" y="285" text-anchor="end" font-family="SimHei,Arial" font-size="12" fill="#334155" font-weight="bold">液压齿轮泵</text>
   <!-- 泵出油 -->
   <line x1="130" y1="254" x2="130" y2="180" stroke="#1565C0" stroke-width="4"/>
   <line id="flowPumpOut" x1="130" y1="254" x2="130" y2="180" stroke="#90CAF9" stroke-width="2.5" stroke-dasharray="10 8" opacity="0">
    <animate attributeName="stroke-dashoffset" from="0" to="18" dur="0.4s" repeatCount="indefinite"/>
   </line>

   <!-- 压力表 -->
   <line x1="280" y1="180" x2="280" y2="140" stroke="#1565C0" stroke-width="3"/>
   <circle cx="280" cy="116" r="20" fill="#FFF" stroke="#1E293B" stroke-width="3"/>
   <!-- 指针 -->
   <g id="gaugeNeedle" transform="rotate(-40, 280, 116)">
    <line x1="280" y1="116" x2="280" y2="98" stroke="#DC2626" stroke-width="2.5" stroke-linecap="round"/>
    <circle cx="280" cy="116" r="3" fill="#DC2626"/>
   </g>
   <text x="280" y="128" text-anchor="middle" font-family="Arial" font-size="9" fill="#64748B">MPa</text>

   <!-- == 控制控制阀 === -->
   <!-- 溢流阀 -->
   <line x1="430" y1="180" x2="430" y2="210" stroke="#1565C0" stroke-width="3"/>
   <rect x="410" y="210" width="40" height="46" fill="#FFF" stroke="#1E293B" stroke-width="3"/>
   <!-- 内部剪头与弹簧 -->
   <line x1="430" y1="218" x2="430" y2="248" stroke="#1E293B" stroke-width="2" marker-end="url(#arrO)"/>
   <polyline points="405,215 398,222 410,230 398,238 410,246 405,253" fill="none" stroke="#1E293B" stroke-width="2"/>
   <line x1="450" y1="208" x2="465" y2="195" stroke="#1E293B" stroke-width="2" marker-end="url(#arrB)"/>
   <text x="350" y="238" text-anchor="end" font-family="SimHei,Arial" font-size="12" fill="#334155" font-weight="bold">先导溢流阀 (设定16MPa)</text>
   
   <line x1="430" y1="256" x2="430" y2="460" stroke="#E65100" stroke-width="3"/>
   <line id="flowRV" x1="430" y1="256" x2="430" y2="460" stroke="#FFCC80" stroke-width="2" stroke-dasharray="10 8" opacity="0">
    <animate attributeName="stroke-dashoffset" from="0" to="-18" dur="0.6s" repeatCount="indefinite"/>
   </line>

   <!-- 换向阀 P,T 立管 -->
   <line x1="623" y1="270" x2="623" y2="290" stroke="#1565C0" stroke-width="3"/>
   <line x1="623" y1="290" x2="650" y2="290" stroke="#1565C0" stroke-width="3"/>
   <line x1="650" y1="180" x2="650" y2="290" stroke="#1565C0" stroke-width="3"/>

   <line x1="637" y1="270" x2="637" y2="300" stroke="#E65100" stroke-width="3"/>
   <line x1="637" y1="300" x2="700" y2="300" stroke="#E65100" stroke-width="3"/>
   <line x1="700" y1="300" x2="700" y2="460" stroke="#E65100" stroke-width="3"/>

   <!-- 三位四通阀 (主体) -->
   <!-- 底座与激活高亮 -->
   <rect id="activeValve" x="610" y="210" width="50" height="60" fill="rgba(16,185,129,0.2)" stroke="#10B981" stroke-width="4" rx="4"/>
   
   <!-- 左位 -->
   <rect x="560" y="210" width="50" height="60" fill="transparent" stroke="#1E293B" stroke-width="3"/>
   <line x1="573" y1="270" x2="587" y2="210" stroke="#1E293B" stroke-width="2" marker-end="url(#arrB)"/>
   <line x1="587" y1="270" x2="573" y2="210" stroke="#1E293B" stroke-width="2" marker-end="url(#arrB)"/>
   <!-- 中位 -->
   <rect x="610" y="210" width="50" height="60" fill="transparent" stroke="#1E293B" stroke-width="3"/>
   <line x1="623" y1="210" x2="623" y2="222" stroke="#1E293B" stroke-width="2"/>
   <line x1="623" y1="222" x2="637" y2="222" stroke="#1E293B" stroke-width="2"/>
   <line x1="637" y1="210" x2="637" y2="222" stroke="#1E293B" stroke-width="2"/>
   <line x1="623" y1="270" x2="623" y2="258" stroke="#1E293B" stroke-width="2"/>
   <line x1="623" y1="258" x2="637" y2="258" stroke="#1E293B" stroke-width="2"/>
   <line x1="637" y1="270" x2="637" y2="258" stroke="#1E293B" stroke-width="2"/>
   <!-- 右位 -->
   <rect x="660" y="210" width="50" height="60" fill="transparent" stroke="#1E293B" stroke-width="3"/>
   <line x1="673" y1="270" x2="673" y2="210" stroke="#1E293B" stroke-width="2" marker-end="url(#arrB)"/>
   <line x1="697" y1="270" x2="697" y2="210" stroke="#1E293B" stroke-width="2" marker-end="url(#arrB)"/>

   <!-- 电磁铁与弹簧 A端 -->
   <rect x="530" y="222" width="30" height="36" fill="#FFF" stroke="#1E293B" stroke-width="2"/>
   <line x1="545" y1="222" x2="560" y2="240" stroke="#1E293B" stroke-width="2"/>
   <text x="545" y="253" text-anchor="middle" font-family="Arial" font-size="12" fill="#1E293B" font-weight="bold">A</text>
   <circle id="isoLedA" cx="545" cy="216" r="5" fill="#E2E8F0" stroke="#94A3B8" stroke-width="1.5"/>
   <polyline points="560,230 555,235 565,240 555,245 560,250" fill="none" stroke="#1E293B" stroke-width="1.5"/>

   <!-- 电磁铁 B端 -->
   <rect x="710" y="222" width="30" height="36" fill="#FFF" stroke="#1E293B" stroke-width="2"/>
   <line x1="725" y1="258" x2="710" y2="240" stroke="#1E293B" stroke-width="2"/>
   <text x="725" y="253" text-anchor="middle" font-family="Arial" font-size="12" fill="#1E293B" font-weight="bold">B</text>
   <circle id="isoLedB" cx="725" cy="216" r="5" fill="#E2E8F0" stroke="#94A3B8" stroke-width="1.5"/>
   <polyline points="710,230 715,235 705,240 715,245 710,250" fill="none" stroke="#1E293B" stroke-width="1.5"/>
   
   <text x="635" y="325" text-anchor="middle" font-family="SimHei,Arial" font-size="12" fill="#334155" font-weight="bold">三位四通电磁换向阀 Y型</text>

   <!-- == 执行机构 = 液压缸 == -->
   <!-- 缸体 -->
   <rect x="900" y="175" width="200" height="70" fill="#FFF" stroke="#1E293B" stroke-width="4"/>
   <!-- 无杆腔油液区 -->
   <rect id="chamberA" x="902" y="177" width="98" height="66" fill="rgba(21,101,192,0.1)"/>
   <!-- 有杆腔油液区 -->
   <rect id="chamberB" x="1002" y="177" width="73" height="66" fill="rgba(230,81,0,0.05)"/>

   <!-- 活塞与杆 (可动组) -->
   <!-- 初始位置，伸出 0,活塞x=1000 -->
   <g id="isoPiston" transform="translate(0, 0)">
    <line x1="1000" y1="175" x2="1000" y2="245" stroke="#1E293B" stroke-width="6"/> <!-- 活塞 -->
    <rect x="1000" y="200" width="140" height="18" rx="8" fill="#E2E8F0" stroke="#1E293B" stroke-width="2.5"/> <!-- 杆 -->
    <circle cx="1140" cy="209" r="8" fill="#94A3B8" stroke="#1E293B" stroke-width="3"/> <!-- 关节头 -->
   </g>
   <!-- 缸端盖孔 -->
   <line x1="1075" y1="175" x2="1075" y2="245" stroke="#1E293B" stroke-width="4"/>

   <text x="940" y="165" text-anchor="middle" font-family="SimHei,Arial" font-size="12" fill="#64748B" font-weight="bold">无杆腔</text>
   <text x="1040" y="165" text-anchor="middle" font-family="SimHei,Arial" font-size="12" fill="#64748B" font-weight="bold">有杆腔</text>
   <text x="940" y="268" text-anchor="middle" font-family="SimHei,Arial" font-size="13" fill="#334155" font-weight="bold">液压支撑起升缸</text>

   <!-- 支撑臂结构 -->
   <!-- 旋转原点 x=1140, y=209 -->
   <g id="isoArm" transform="rotate(0, 1140, 209)">
    <line x1="1140" y1="209" x2="1320" y2="100" stroke="#475569" stroke-width="24" stroke-linecap="round"/>
    <line x1="1140" y1="209" x2="1320" y2="100" stroke="#64748B" stroke-width="14" stroke-linecap="round"/>
    <circle cx="1320" cy="100" r="10" fill="#CBD5E1" stroke="#334155" stroke-width="3"/>
    <text x="1320" y="80" text-anchor="middle" font-family="SimHei,Arial" font-size="14" fill="#1E293B" font-weight="bold">支 撑 位</text>
   </g>
   <!-- 固定基座支点 -->
   <circle cx="1140" cy="209" r="10" fill="#334155" stroke="#0F172A" stroke-width="2"/>
   <circle cx="1140" cy="209" r="4" fill="#94A3B8"/>
   <rect x="1120" y="222" width="40" height="12" rx="4" fill="#334155"/>
   <rect x="1110" y="234" width="60" height="8" rx="2" fill="#475569"/>

  </g> <!-- 物理图平移结束 -->

  <!-- =================================================================== -->
  <!-- 下方: 科幻/工业风 操作控制面板 -->
  
  <rect x="50" y="580" width="1820" height="460" rx="16" fill="url(#panelBg)" stroke="#334155" stroke-width="4" filter="url(#panelShadow)"/>
  
  <!-- 面板装饰线 -->
  <rect x="50" y="580" width="1820" height="60" rx="16" fill="#0F172A"/>
  <rect x="50" y="620" width="1820" height="20" fill="#0F172A"/>
  <line x1="50" y1="640" x2="1870" y2="640" stroke="#38BDF8" stroke-width="2" opacity="0.6"/>
  <text x="960" y="618" text-anchor="middle" font-family="Arial" font-size="20" fill="#38BDF8" font-weight="bold" letter-spacing="4">SYSTEM CONTROL CONSOLE // SYS-01</text>

  <!-- === 区域 1: 动作指令区 (Action Control) === -->
  <rect x="80" y="670" width="500" height="340" rx="12" fill="#1E293B" stroke="#475569" stroke-width="2"/>
  <text x="330" y="710" text-anchor="middle" font-family="SimHei,Arial" font-size="18" fill="#94A3B8" font-weight="bold">动作指令区</text>
  <line x1="100" y1="720" x2="560" y2="720" stroke="#475569" stroke-width="2"/>

  <!-- 大号发光按钮: 升起 -->
  <g id="btnUp" cursor="pointer" transform="translate(130, 750)">
   <rect x="0" y="0" width="400" height="70" rx="10" fill="url(#btnUpBg)" stroke="#059669" stroke-width="3"/>
   <rect id="btnUpHov" x="4" y="4" width="392" height="24" rx="6" fill="rgba(255,255,255,0.2)"/>
   <text x="200" y="45" text-anchor="middle" font-family="SimHei,Arial" font-size="32" fill="#FFF" font-weight="bold" letter-spacing="8" pointer-events="none">升 起</text>
  </g>

  <!-- 大号发光按钮: 降落 -->
  <g id="btnDown" cursor="pointer" transform="translate(130, 840)">
   <rect x="0" y="0" width="400" height="70" rx="10" fill="url(#btnDnBg)" stroke="#DC2626" stroke-width="3"/>
   <rect id="btnDnHov" x="4" y="4" width="392" height="24" rx="6" fill="rgba(255,255,255,0.2)"/>
   <text x="200" y="45" text-anchor="middle" font-family="SimHei,Arial" font-size="32" fill="#FFF" font-weight="bold" letter-spacing="8" pointer-events="none">降 落</text>
  </g>

  <!-- 大号中位按钮: 停止 -->
  <g id="btnStop" cursor="pointer" transform="translate(130, 930)">
   <rect x="0" y="0" width="400" height="50" rx="10" fill="url(#btnStBg)" stroke="#475569" stroke-width="3"/>
   <rect id="btnStHov" x="4" y="4" width="392" height="18" rx="6" fill="rgba(255,255,255,0.15)"/>
   <text x="200" y="34" text-anchor="middle" font-family="SimHei,Arial" font-size="24" fill="#E2E8F0" font-weight="bold" letter-spacing="8" pointer-events="none">停 止 (复位)</text>
  </g>

  <!-- === 区域 2: 系统遥测区 (Telemetry Data) === -->
  <rect x="610" y="670" width="700" height="340" rx="12" fill="#0F172A" stroke="#475569" stroke-width="2"/>
  <text x="960" y="708" text-anchor="middle" font-family="Arial" font-size="18" fill="#94A3B8" font-weight="bold">系统实时遥测 (Telemetry)</text>
  <line x1="630" y1="720" x2="1290" y2="720" stroke="#475569" stroke-width="2"/>

  <!-- 大型数字仪表板 -->
  <text x="650" y="770" font-family="SimHei,Arial" font-size="16" fill="#CBD5E1">主系统压力 (Sys Pressure):</text>
  <rect x="650" y="790" width="280" height="60" rx="6" fill="#1E293B" stroke="#334155" stroke-width="2"/>
  <text id="ssPress" x="910" y="835" text-anchor="end" font-family="monospace" font-size="44" fill="#38BDF8" font-weight="bold" filter="url(#glowBlue)">0.0</text>
  <text x="800" y="815" font-family="monospace" font-size="14" fill="#94A3B8">MPa</text>
  
  <text x="980" y="770" font-family="SimHei,Arial" font-size="16" fill="#CBD5E1">运行流量 (Flow Rate):</text>
  <rect x="980" y="790" width="280" height="60" rx="6" fill="#1E293B" stroke="#334155" stroke-width="2"/>
  <text id="ssFlow" x="1240" y="835" text-anchor="end" font-family="monospace" font-size="44" fill="#38BDF8" font-weight="bold" filter="url(#glowBlue)">0.0</text>
  <text x="1130" y="815" font-family="monospace" font-size="14" fill="#94A3B8">L/min</text>

  <!-- 行程进度光条 -->
  <text x="650" y="890" font-family="SimHei,Arial" font-size="16" fill="#CBD5E1">液压缸伸出行程 (Stroke Pos):</text>
  <text id="ssStrokeVal" x="1260" y="890" text-anchor="end" font-family="monospace" font-size="28" fill="#10B981" font-weight="bold" filter="url(#glowGreen)">0.0 %</text>
  
  <rect x="650" y="910" width="610" height="16" rx="8" fill="#334155"/>
  <rect id="ssStrokeBar" x="650" y="910" width="0" height="16" rx="8" fill="#10B981" filter="url(#glowGreen)"/>
  
  <!-- 刻度 -->
  <text x="650" y="945" font-family="Arial" font-size="12" fill="#64748B">0%</text>
  <text x="802" y="945" font-family="Arial" font-size="12" fill="#64748B">25%</text>
  <text x="955" y="945" font-family="Arial" font-size="12" fill="#64748B" text-anchor="middle">50%</text>
  <text x="1107" y="945" font-family="Arial" font-size="12" fill="#64748B">75%</text>
  <text x="1260" y="945" text-anchor="end" font-family="Arial" font-size="12" fill="#64748B">100%</text>

  <!-- === 区域 3: 连锁逻辑与状态指示区 (Logic & State) === -->
  <rect x="1340" y="670" width="500" height="340" rx="12" fill="#1E293B" stroke="#475569" stroke-width="2"/>
  <text x="1590" y="708" text-anchor="middle" font-family="SimHei,Arial" font-size="18" fill="#94A3B8" font-weight="bold">连锁逻辑指示</text>
  <line x1="1360" y1="720" x2="1820" y2="720" stroke="#475569" stroke-width="2"/>

  <!-- 大号状态文字 -->
  <text x="1370" y="760" font-family="SimHei,Arial" font-size="14" fill="#94A3B8">主动作模式 (Mode):</text>
  <text id="ssMode" x="1530" y="760" font-family="monospace" font-size="18" fill="#F59E0B" font-weight="bold">待机保护</text>

  <rect x="1370" y="790" width="440" height="180" rx="8" fill="#0F172A" stroke="#334155" stroke-width="2"/>
  
  <!-- 灯阵列逻辑 -->
  <circle id="ledPump" cx="1400" cy="820" r="12" fill="#475569" stroke="#64748B" stroke-width="2"/>
  <text x="1430" y="825" font-family="Arial" font-size="16" fill="#CBD5E1">主泵 M 运行</text>
  
  <circle id="ledSolA" cx="1400" cy="870" r="12" fill="#475569" stroke="#64748B" stroke-width="2"/>
  <text x="1430" y="875" font-family="Arial" font-size="16" fill="#CBD5E1">换向阀 SOL-A 激磁 (升起)</text>
  
  <circle id="ledSolB" cx="1400" cy="920" r="12" fill="#475569" stroke="#64748B" stroke-width="2"/>
  <text x="1430" y="925" font-family="Arial" font-size="16" fill="#CBD5E1">换向阀 SOL-B 激磁 (降落)</text>
  
  <circle id="ledLock" cx="1680" cy="820" r="12" fill="#F59E0B" stroke="#B45309" stroke-width="2" filter="url(#glowRed)"/>
  <text x="1710" y="825" font-family="Arial" font-size="16" fill="#FCD34D" font-weight="bold">中位锁止</text>
 </g>

 <!-- ================================================================ -->
 <!-- JavaScript 交互逻辑 -->
 <script type="text/ecmascript"><![CDATA[
  var state = 'stop';
  var stroke = 0; // 行程 0-100%
  var animTimer = null;
  var waveTimer = null;
  var svgDoc = null;

  function init() {
   svgDoc = document.documentElement;
   getEl('btnUp').addEventListener('click', function(){ doAction('up'); });
   getEl('btnDown').addEventListener('click', function(){ doAction('down'); });
   getEl('btnStop').addEventListener('click', function(){ doAction('stop'); });
   
   bindHover('btnUp', 'btnUpHov');
   bindHover('btnDown', 'btnDnHov');
   bindHover('btnStop', 'btnStHov');
  }

  function bindHover(gId, hovId) {
   var g = getEl(gId);
   var h = getEl(hovId);
   if(g && h) {
    g.addEventListener('mouseover', function(){ h.setAttribute('fill', 'rgba(255,255,255,0.4)'); });
    g.addEventListener('mouseout', function(){ h.setAttribute('fill', 'rgba(255,255,255,0.2)'); });
    g.addEventListener('mousedown', function(){ h.setAttribute('fill', 'rgba(0,0,0,0.2)'); });
    g.addEventListener('mouseup', function(){ h.setAttribute('fill', 'rgba(255,255,255,0.4)'); });
   }
  }

  function getEl(id) { return document.getElementById(id); }
  function setEl(id, attr, val) { var el = getEl(id); if(el) el.setAttribute(attr, val); }
  function setText(id, text) { var el = getEl(id); if(el) el.textContent = text; }

  function setFlowState(id, show) {
   var el = getEl(id);
   if(el) el.setAttribute('opacity', show ? '1' : '0');
  }

  function doAction(act) {
   if(state === act) return;
   state = act;
   if(animTimer) { clearInterval(animTimer); animTimer = null; }

   var flows = ['flowP','flowR','flowS','flowPumpOut','flowRV'];

   if(act === 'up') {
    // 换向阀移位 (左位) -> P向A油
    setEl('activeValve', 'x', '560');
    // 管路颜色与流动
    setEl('pipeA1', 'stroke', '#1565C0'); setEl('pipeA2', 'stroke', '#1565C0'); setEl('pipeA3', 'stroke', '#1565C0');
    setEl('pipeB1', 'stroke', '#E65100'); setEl('pipeB2', 'stroke', '#E65100'); setEl('pipeB3', 'stroke', '#E65100');
    
    for(var i=0;i<flows.length;i++) setFlowState(flows[i], true);
    setFlowState('flowA', true); setFlowState('flowB', true);
    
    // 设置A出B回的流动颜色
    setEl('flowA', 'stroke', '#90CAF9');
    setEl('flowB', 'stroke', '#FFCC80');

    // 面板指示
    setEl('isoLedA', 'fill', '#10B981'); setEl('isoLedB', 'fill', '#E2E8F0');
    setEl('ledSolA', 'fill', '#10B981'); setEl('ledSolA', 'filter', 'url(#glowGreen)');
    setEl('ledSolB', 'fill', '#475569'); setEl('ledSolB', 'filter', 'none');
    setEl('ledPump', 'fill', '#10B981'); setEl('ledPump', 'filter', 'url(#glowGreen)');
    setEl('ledLock', 'fill', '#475569'); setEl('ledLock', 'stroke', '#64748B'); setEl('ledLock', 'filter', 'none');
    
    updatePanel('正在升起...', 15.0, 35.0);

    animTimer = setInterval(function(){
     if(stroke < 100){ stroke += 1; updateOutputs(); }
     else { clearInterval(animTimer); animTimer = null; doAction('stop'); }
    }, 40);

   } else if(act === 'down') {
    // 换向阀移位 (右位) -> P向B油
    setEl('activeValve', 'x', '660');
    
    setEl('pipeB1', 'stroke', '#1565C0'); setEl('pipeB2', 'stroke', '#1565C0'); setEl('pipeB3', 'stroke', '#1565C0');
    setEl('pipeA1', 'stroke', '#E65100'); setEl('pipeA2', 'stroke', '#E65100'); setEl('pipeA3', 'stroke', '#E65100');
    
    for(var i=0;i<flows.length;i++) setFlowState(flows[i], true);
    setFlowState('flowA', true); setFlowState('flowB', true);
    
    setEl('flowB', 'stroke', '#90CAF9');
    setEl('flowA', 'stroke', '#FFCC80');

    // 面板指示
    setEl('isoLedB', 'fill', '#EF4444'); setEl('isoLedA', 'fill', '#E2E8F0');
    setEl('ledSolB', 'fill', '#EF4444'); setEl('ledSolB', 'filter', 'url(#glowRed)');
    setEl('ledSolA', 'fill', '#475569'); setEl('ledSolA', 'filter', 'none');
    setEl('ledPump', 'fill', '#10B981'); setEl('ledPump', 'filter', 'url(#glowGreen)');
    setEl('ledLock', 'fill', '#475569'); setEl('ledLock', 'stroke', '#64748B'); setEl('ledLock', 'filter', 'none');

    updatePanel('正在降落...', 12.5, 42.0);

    animTimer = setInterval(function(){
     if(stroke > 0){ stroke -= 1; updateOutputs(); }
     else { clearInterval(animTimer); animTimer = null; doAction('stop'); }
    }, 40);

   } else {
    // Stop (中位)
    setEl('activeValve', 'x', '610');
    
    setEl('pipeA1', 'stroke', '#94A3B8'); setEl('pipeA2', 'stroke', '#94A3B8'); setEl('pipeA3', 'stroke', '#94A3B8');
    setEl('pipeB1', 'stroke', '#94A3B8'); setEl('pipeB2', 'stroke', '#94A3B8'); setEl('pipeB3', 'stroke', '#94A3B8');
    
    for(var i=0;i<flows.length;i++) setFlowState(flows[i], false);
    setFlowState('flowA', false); setFlowState('flowB', false);

    setEl('isoLedA', 'fill', '#E2E8F0'); setEl('isoLedB', 'fill', '#E2E8F0');
    setEl('ledSolA', 'fill', '#475569'); setEl('ledSolA', 'filter', 'none');
    setEl('ledSolB', 'fill', '#475569'); setEl('ledSolB', 'filter', 'none');
    setEl('ledPump', 'fill', '#475569'); setEl('ledPump', 'filter', 'none');
    setEl('ledLock', 'fill', '#F59E0B'); setEl('ledLock', 'stroke', '#B45309'); setEl('ledLock', 'filter', 'url(#glowRed)');

    updatePanel('待机锁定', 0.0, 0.0);
   }
  }

  function updateOutputs() {
   // 原理图活塞移动
   var o = stroke * 1.5; // 最大150位移
   setEl('isoPiston', 'transform', 'translate(' + o + ', 0)');
   
   // 腔体动画
   var w = 98 + o;
   setEl('chamberA', 'width', w);
   
   // 原理图支撑臂旋转
   var angle = -stroke * 0.25; 
   setEl('isoArm', 'transform', 'rotate(' + angle + ', 1140, 209)');

   // 仪表板数值
   setText('ssStrokeVal', stroke.toFixed(1) + ' %');
   
   // 进度条宽度: 总宽610
   var bw = stroke * 6.1;
   setEl('ssStrokeBar', 'width', bw);
  }

  function updatePanel(modeRaw, press, flow) {
   setText('ssMode', modeRaw);
   setText('ssPress', press.toFixed(1));
   setText('ssFlow', flow.toFixed(1));

   if (modeRaw === '待机锁定') {
      setEl('ssMode', 'fill', '#F59E0B');
      setEl('ssPress', 'filter', 'none'); setEl('ssPress', 'fill', '#475569');
      setEl('ssFlow', 'filter', 'none'); setEl('ssFlow', 'fill', '#475569');
   } else {
      setEl('ssMode', 'fill', '#10B981');
      setEl('ssPress', 'filter', 'url(#glowBlue)'); setEl('ssPress', 'fill', '#38BDF8');
      setEl('ssFlow', 'filter', 'url(#glowBlue)'); setEl('ssFlow', 'fill', '#38BDF8');
   }

   // 压力表指针旋转 180度刻度
   var gnd = getEl('gaugeNeedle');
   if(gnd) {
    var ang = -40 + (press / 25) * 180;
    gnd.setAttribute('transform', 'rotate(' + ang + ', 280, 116)');
   }
  }

  if(document.readyState === 'loading') {
   document.addEventListener('DOMContentLoaded', init);
  } else {
   setTimeout(init, 200);
  }
 ]]></script>
</svg>'''

# 推送服务到 FUXA
req = urllib.request.Request(f'{BASE_URL}/api/project')
try:
    resp = urllib.request.urlopen(req, timeout=10)
    project = json.loads(resp.read().decode())
except Exception as e:
    print(f"无法连接到 FUXA 服务 {BASE_URL}: {e}")
    exit(1)

found = False
for i, v in enumerate(project['hmi']['views']):
    if v['id'] == 'v_hydraulic_arm_01':
        project['hmi']['views'][i]['svgcontent'] = svg
        project['hmi']['views'][i]['profile']['width'] = 1920
        project['hmi']['views'][i]['profile']['height'] = 1080
        project['hmi']['views'][i]['profile']['bkcolor'] = '#F8FAFC'
        print(f'更新视图 SVG: {len(svg)} chars')
        found = True
        break

if not found:
    new_view = {
        'id': 'v_hydraulic_arm_01',
        'name': '标准原理图与控制台',
        'profile': {'width': 1920, 'height': 1080, 'bkcolor': '#F8FAFC'},
        'svgcontent': svg,
        'items': {}
    }
    project['hmi']['views'].append(new_view)
    print(f'创建新视图: {len(svg)} chars')

body = json.dumps(project).encode('utf-8')
req = urllib.request.Request(f'{BASE_URL}/api/project', data=body, headers={'Content-Type': 'application/json'}, method='POST')
try:
    resp = urllib.request.urlopen(req, timeout=30)
    print(f'项目更新: HTTP {resp.status}')
except Exception as e:
    print(f"推送 FUXA 失败: {e}")
    exit(1)

print('完成! 请刷新浏览器 http://localhost:1881 查看现代智控增强版 ISO 原理图')
