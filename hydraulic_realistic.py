#!/usr/bin/env python3
"""
真实简易风格液压支撑臂原理图
元器件使用接近真实外观的2D简化绘制
"""
import urllib.request, json

BASE_URL = 'http://localhost:1881'

svg = '''<svg width="1400" height="900" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
 <defs>
  <!-- 金属质感渐变(水平) -->
  <linearGradient id="metalH" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#D0D0D0"/>
   <stop offset="25%" stop-color="#B8B8B8"/>
   <stop offset="50%" stop-color="#A8A8A8"/>
   <stop offset="75%" stop-color="#C0C0C0"/>
   <stop offset="100%" stop-color="#989898"/>
  </linearGradient>
  <!-- 金属质感(垂直) -->
  <linearGradient id="metalV" x1="0" y1="0" x2="1" y2="0">
   <stop offset="0%" stop-color="#C8C8C8"/>
   <stop offset="30%" stop-color="#A8A8A8"/>
   <stop offset="70%" stop-color="#B8B8B8"/>
   <stop offset="100%" stop-color="#909090"/>
  </linearGradient>
  <!-- 油箱钢板 -->
  <linearGradient id="tankBody" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#607D8B"/>
   <stop offset="50%" stop-color="#455A64"/>
   <stop offset="100%" stop-color="#37474F"/>
  </linearGradient>
  <!-- 油液 -->
  <linearGradient id="oilFill" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#FFB300"/>
   <stop offset="100%" stop-color="#E65100"/>
  </linearGradient>
  <!-- 电机壳体 -->
  <linearGradient id="motorShell" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#78909C"/>
   <stop offset="20%" stop-color="#546E7A"/>
   <stop offset="80%" stop-color="#455A64"/>
   <stop offset="100%" stop-color="#37474F"/>
  </linearGradient>
  <!-- 泵壳体(深蓝灰) -->
  <linearGradient id="pumpShell" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#5C6BC0"/>
   <stop offset="50%" stop-color="#3949AB"/>
   <stop offset="100%" stop-color="#283593"/>
  </linearGradient>
  <!-- 阀体(深灰) -->
  <linearGradient id="valveBody" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#6D6D6D"/>
   <stop offset="30%" stop-color="#555555"/>
   <stop offset="100%" stop-color="#3D3D3D"/>
  </linearGradient>
  <!-- 电磁铁 -->
  <linearGradient id="solenoid" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#1565C0"/>
   <stop offset="100%" stop-color="#0D47A1"/>
  </linearGradient>
  <!-- 液压缸缸筒 -->
  <linearGradient id="cylTube" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#B0BEC5"/>
   <stop offset="25%" stop-color="#90A4AE"/>
   <stop offset="50%" stop-color="#78909C"/>
   <stop offset="75%" stop-color="#90A4AE"/>
   <stop offset="100%" stop-color="#607D8B"/>
  </linearGradient>
  <!-- 活塞杆(亮银) -->
  <linearGradient id="rodGrad" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#E0E0E0"/>
   <stop offset="40%" stop-color="#F5F5F5"/>
   <stop offset="60%" stop-color="#E8E8E8"/>
   <stop offset="100%" stop-color="#BDBDBD"/>
  </linearGradient>
  <!-- 压力管(蓝) -->
  <linearGradient id="pipeBlue" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#42A5F5"/>
   <stop offset="50%" stop-color="#1E88E5"/>
   <stop offset="100%" stop-color="#1565C0"/>
  </linearGradient>
  <linearGradient id="pipeBlueH" x1="0" y1="0" x2="1" y2="0">
   <stop offset="0%" stop-color="#42A5F5"/>
   <stop offset="50%" stop-color="#1E88E5"/>
   <stop offset="100%" stop-color="#1565C0"/>
  </linearGradient>
  <!-- 回油管(橙) -->
  <linearGradient id="pipeOrange" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#FFA726"/>
   <stop offset="50%" stop-color="#FB8C00"/>
   <stop offset="100%" stop-color="#E65100"/>
  </linearGradient>
  <linearGradient id="pipeOrangeH" x1="0" y1="0" x2="1" y2="0">
   <stop offset="0%" stop-color="#FFA726"/>
   <stop offset="50%" stop-color="#FB8C00"/>
   <stop offset="100%" stop-color="#E65100"/>
  </linearGradient>
  <!-- 表盘 -->
  <radialGradient id="gaugeface" cx="50%" cy="50%" r="50%">
   <stop offset="0%" stop-color="#FAFAFA"/>
   <stop offset="85%" stop-color="#F0F0F0"/>
   <stop offset="100%" stop-color="#BDBDBD"/>
  </radialGradient>
  <!-- 阴影 -->
  <filter id="shadow">
   <feDropShadow dx="2" dy="3" stdDeviation="3" flood-color="rgba(0,0,0,0.25)"/>
  </filter>
  <filter id="shSm">
   <feDropShadow dx="1" dy="1" stdDeviation="1.5" flood-color="rgba(0,0,0,0.2)"/>
  </filter>
  <!-- 流动箭头 -->
  <marker id="arB" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="4" markerHeight="4" orient="auto">
   <path d="M 0 1 L 6 4 L 0 7 z" fill="#1E88E5"/>
  </marker>
  <marker id="arO" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="4" markerHeight="4" orient="auto">
   <path d="M 0 1 L 6 4 L 0 7 z" fill="#FB8C00"/>
  </marker>
 </defs>
 <g>
  <title>Layer 1</title>
  <!-- 浅灰工业背景 -->
  <rect id="svg_bg" fill="#ECEFF1" height="900" width="1400"/>

  <!-- ============ 标题 ============ -->
  <rect id="svg_hd0" x="350" y="8" width="700" height="42" rx="6" fill="#37474F" filter="url(#shadow)"/>
  <text id="svg_hd1" x="700" y="36" text-anchor="middle" font-family="Arial" font-size="20" fill="#ECEFF1" font-weight="bold">液压支撑臂控制系统原理图</text>

  <!-- ================================================================ -->
  <!--                     管路层 (先画，设备覆盖)                       -->
  <!-- 压力主管 y=255  蓝色管                                            -->
  <!-- 回油主管 y=510  橙色管                                            -->
  <!-- ================================================================ -->

  <!-- == 压力主管 (水平 y=255) == -->
  <rect id="svg_pm" x="168" y="248" width="530" height="14" rx="7" fill="url(#pipeBlueH)" filter="url(#shSm)"/>
  <!-- 流动指示(虚线动画) -->
  <line id="svg_pmf" x1="170" y1="255" x2="696" y2="255" stroke="#90CAF9" stroke-width="3" stroke-dasharray="14 10" opacity="0.7">
   <animate attributeName="stroke-dashoffset" from="0" to="-24" dur="0.7s" repeatCount="indefinite"/>
  </line>

  <!-- == 泵吸油管 (油箱→泵 垂直) == -->
  <rect id="svg_sm" x="168" y="420" width="14" height="80" rx="7" fill="url(#pipeBlue)" filter="url(#shSm)"/>
  <line id="svg_smf" x1="175" y1="498" x2="175" y2="420" stroke="#90CAF9" stroke-width="3" stroke-dasharray="10 8" opacity="0.5">
   <animate attributeName="stroke-dashoffset" from="0" to="18" dur="0.8s" repeatCount="indefinite"/>
  </line>

  <!-- == 泵出口管 (泵→压力主管 垂直) == -->
  <rect id="svg_po" x="168" y="255" width="14" height="76" rx="7" fill="url(#pipeBlue)" filter="url(#shSm)"/>
  <line id="svg_pof" x1="175" y1="330" x2="175" y2="256" stroke="#90CAF9" stroke-width="3" stroke-dasharray="10 8" opacity="0.7">
   <animate attributeName="stroke-dashoffset" from="0" to="18" dur="0.8s" repeatCount="indefinite"/>
  </line>

  <!-- == 溢流阀分支管(压力管→溢流阀) == -->
  <rect id="svg_rvp0" x="398" y="262" width="14" height="30" rx="7" fill="url(#pipeBlue)"/>
  <!-- == 溢流阀出口→回油管 == -->
  <rect id="svg_rvp1" x="398" y="344" width="14" height="173" rx="7" fill="url(#pipeOrange)"/>
  <line id="svg_rvpf" x1="405" y1="346" x2="405" y2="515" stroke="#FFE0B2" stroke-width="2" stroke-dasharray="8 8" opacity="0.4">
   <animate attributeName="stroke-dashoffset" from="0" to="-16" dur="1s" repeatCount="indefinite"/>
  </line>

  <!-- == 换向阀P口连接(压力管→阀) == -->
  <rect id="svg_dvpc" x="618" y="262" width="14" height="38" rx="7" fill="url(#pipeBlue)"/>
  <!-- == 换向阀T口→回油管 == -->
  <rect id="svg_dvtc" x="668" y="370" width="14" height="147" rx="7" fill="url(#pipeOrange)"/>
  <line id="svg_dvtf" x1="675" y1="372" x2="675" y2="515" stroke="#FFE0B2" stroke-width="2" stroke-dasharray="8 8" opacity="0.5">
   <animate attributeName="stroke-dashoffset" from="0" to="-16" dur="0.8s" repeatCount="indefinite"/>
  </line>

  <!-- == A管(换向阀→液压缸无杆腔) 向上再右拐 == -->
  <rect id="svg_aV" x="618" y="170" width="14" height="92" rx="7" fill="url(#pipeBlue)"/>
  <rect id="svg_aH" x="625" y="163" width="315" height="14" rx="7" fill="url(#pipeBlueH)" filter="url(#shSm)"/>
  <rect id="svg_aD" x="933" y="170" width="14" height="62" rx="7" fill="url(#pipeBlue)"/>
  <!-- A管流动 -->
  <line id="svg_aVf" x1="625" y1="260" x2="625" y2="175" stroke="#90CAF9" stroke-width="2" stroke-dasharray="8 8" opacity="0.5">
   <animate attributeName="stroke-dashoffset" from="0" to="16" dur="0.6s" repeatCount="indefinite"/>
  </line>
  <line id="svg_aHf" x1="630" y1="170" x2="938" y2="170" stroke="#90CAF9" stroke-width="2" stroke-dasharray="8 8" opacity="0.5">
   <animate attributeName="stroke-dashoffset" from="0" to="-16" dur="0.6s" repeatCount="indefinite"/>
  </line>

  <!-- == B管(换向阀→液压缸有杆腔) 更高拐弯 == -->
  <rect id="svg_bV" x="668" y="120" width="14" height="180" rx="7" fill="url(#pipeBlue)"/>
  <rect id="svg_bH" x="675" y="113" width="420" height="14" rx="7" fill="url(#pipeBlueH)" filter="url(#shSm)"/>
  <rect id="svg_bD" x="1088" y="120" width="14" height="112" rx="7" fill="url(#pipeBlue)"/>
  <!-- B管流动 -->
  <line id="svg_bHf" x1="680" y1="120" x2="1093" y2="120" stroke="#BBDEFB" stroke-width="2" stroke-dasharray="8 8" opacity="0.4">
   <animate attributeName="stroke-dashoffset" from="0" to="-16" dur="0.6s" repeatCount="indefinite"/>
  </line>

  <!-- == 回油主管 (水平 y=510) == -->
  <rect id="svg_rm" x="168" y="503" width="530" height="14" rx="7" fill="url(#pipeOrangeH)" filter="url(#shSm)"/>
  <line id="svg_rmf" x1="696" y1="510" x2="170" y2="510" stroke="#FFE0B2" stroke-width="3" stroke-dasharray="14 10" opacity="0.5">
   <animate attributeName="stroke-dashoffset" from="0" to="-24" dur="0.7s" repeatCount="indefinite"/>
  </line>

  <!-- 管路标签 -->
  <text id="svg_pml" x="370" y="244" text-anchor="middle" font-family="Arial" font-size="10" fill="#1565C0" font-weight="bold">P 压力油路</text>
  <text id="svg_rml" x="370" y="530" text-anchor="middle" font-family="Arial" font-size="10" fill="#E65100" font-weight="bold">T 回油油路</text>
  <text id="svg_aml" x="780" y="160" text-anchor="middle" font-family="Arial" font-size="9" fill="#1976D2">A管路(无杆腔)</text>
  <text id="svg_bml" x="860" y="110" text-anchor="middle" font-family="Arial" font-size="9" fill="#1976D2">B管路(有杆腔)</text>

  <!-- ================================================================ -->
  <!--                          设备层                                   -->
  <!-- ================================================================ -->

  <!-- ===== 油箱 (真实钢制方箱, 带视液窗, 管接头) ===== -->
  <!-- 箱体 -->
  <rect id="svg_tk1" x="95" y="505" width="170" height="110" rx="5" fill="url(#tankBody)" stroke="#263238" stroke-width="2" filter="url(#shadow)"/>
  <!-- 顶板(略浅) -->
  <rect id="svg_tk2" x="95" y="505" width="170" height="12" rx="5" fill="#546E7A" stroke="#263238" stroke-width="1"/>
  <!-- 加油口 -->
  <circle id="svg_tk3" cx="240" cy="511" r="8" fill="#455A64" stroke="#37474F" stroke-width="2"/>
  <circle id="svg_tk4" cx="240" cy="511" r="4" fill="#546E7A"/>
  <!-- 视液窗(圆形, 能看到油位) -->
  <circle id="svg_tk5" cx="180" cy="565" r="20" fill="#263238" stroke="#455A64" stroke-width="3"/>
  <circle id="svg_tk6" cx="180" cy="565" r="16" fill="#37474F"/>
  <!-- 油液(半满状态) -->
  <clipPath id="tkClip"><circle cx="180" cy="565" r="15"/></clipPath>
  <rect id="svg_tk7" x="164" y="558" width="32" height="24" fill="url(#oilFill)" clip-path="url(#tkClip)"/>
  <!-- 油面波纹 -->
  <path id="svg_tk8" d="M 164 558 Q 172 554 180 558 Q 188 562 196 558" fill="none" stroke="#FFD54F" stroke-width="1" clip-path="url(#tkClip)" opacity="0.8">
   <animate attributeName="d" values="M 164 558 Q 172 554 180 558 Q 188 562 196 558;M 164 558 Q 172 562 180 558 Q 188 554 196 558;M 164 558 Q 172 554 180 558 Q 188 562 196 558" dur="2s" repeatCount="indefinite"/>
  </path>
  <!-- 排油口 -->
  <rect id="svg_tk9" x="110" y="605" width="20" height="10" rx="3" fill="#455A64" stroke="#37474F" stroke-width="1"/>
  <!-- 吸油管接头(顶部,连接到泵) -->
  <rect id="svg_tka" x="170" y="497" width="20" height="12" rx="3" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <!-- 回油管接头(顶部) -->
  <rect id="svg_tkb" x="130" y="497" width="20" height="12" rx="3" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <!-- 标签 -->
  <text id="svg_tkn" x="180" y="600" text-anchor="middle" font-family="Arial" font-size="11" fill="#90A4AE" font-weight="bold">OIL TANK</text>
  <!-- 温度/液位数据 -->
  <rect id="svg_tkd" x="95" y="620" width="170" height="38" rx="5" fill="#FFF8E1" stroke="#FFB300" stroke-width="1" filter="url(#shSm)"/>
  <text id="svg_tkd1" x="105" y="637" font-family="Arial" font-size="10" fill="#E65100">油温:</text>
  <text id="svg_tkv1" x="195" y="637" text-anchor="end" font-family="monospace" font-size="12" fill="#BF360C" font-weight="bold">25.0 C</text>
  <text id="svg_tkd2" x="105" y="652" font-family="Arial" font-size="10" fill="#E65100">液位:</text>
  <text id="svg_tkv2" x="195" y="652" text-anchor="end" font-family="monospace" font-size="12" fill="#BF360C" font-weight="bold">85.0 %</text>
  <!-- 液位条 -->
  <rect id="svg_tklb" x="200" y="625" width="60" height="28" rx="3" fill="#ECEFF1" stroke="#FFB300" stroke-width="1"/>
  <rect id="svg_tklv" x="202" y="629" width="56" height="20" rx="2" fill="#E8F5E9"/>
  <rect id="svg_tklf" x="202" y="633" width="48" height="16" rx="2" fill="#FFB300" opacity="0.6"/>

  <!-- ===== 电动机 (真实感: 圆柱壳体+散热片+接线盒+轴) ===== -->
  <!-- 电机壳体(主体圆角矩形) -->
  <rect id="svg_mo1" x="115" y="380" width="120" height="55" rx="10" fill="url(#motorShell)" stroke="#263238" stroke-width="2" filter="url(#shadow)"/>
  <!-- 散热片(横纹) -->
  <line id="svg_mo2a" x1="125" y1="390" x2="225" y2="390" stroke="#37474F" stroke-width="1.5"/>
  <line id="svg_mo2b" x1="125" y1="398" x2="225" y2="398" stroke="#37474F" stroke-width="1.5"/>
  <line id="svg_mo2c" x1="125" y1="406" x2="225" y2="406" stroke="#37474F" stroke-width="1.5"/>
  <line id="svg_mo2d" x1="125" y1="414" x2="225" y2="414" stroke="#37474F" stroke-width="1.5"/>
  <line id="svg_mo2e" x1="125" y1="422" x2="225" y2="422" stroke="#37474F" stroke-width="1.5"/>
  <!-- 前端盖 -->
  <rect id="svg_mo3" x="115" y="380" width="16" height="55" rx="5" fill="#546E7A" stroke="#263238" stroke-width="1.5"/>
  <!-- 后端盖 -->
  <rect id="svg_mo4" x="219" y="380" width="16" height="55" rx="5" fill="#546E7A" stroke="#263238" stroke-width="1.5"/>
  <!-- 接线盒(顶部) -->
  <rect id="svg_mo5" x="155" y="370" width="40" height="14" rx="3" fill="#455A64" stroke="#263238" stroke-width="1"/>
  <circle id="svg_mo6" cx="165" cy="377" r="3" fill="#37474F" stroke="#263238" stroke-width="0.5"/>
  <circle id="svg_mo7" cx="175" cy="377" r="3" fill="#37474F" stroke="#263238" stroke-width="0.5"/>
  <circle id="svg_mo8" cx="185" cy="377" r="3" fill="#37474F" stroke="#263238" stroke-width="0.5"/>
  <!-- 电机铭牌 -->
  <rect id="svg_mo9" x="140" y="400" width="50" height="18" rx="2" fill="#37474F" stroke="#546E7A" stroke-width="0.5"/>
  <text id="svg_mo10" x="165" y="413" text-anchor="middle" font-family="Arial" font-size="9" fill="#B0BEC5" font-weight="bold">MOTOR</text>
  <!-- 轴(连接到泵) -->
  <rect id="svg_mox" x="170" y="333" width="10" height="48" rx="5" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>

  <!-- 电机状态 -->
  <rect id="svg_mos" x="240" y="393" width="75" height="25" rx="5" fill="#E8F5E9" stroke="#4CAF50" stroke-width="1" filter="url(#shSm)"/>
  <circle id="svg_moi" cx="254" cy="406" r="5" fill="#4CAF50">
   <animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <text id="svg_mov" x="277" y="410" text-anchor="middle" font-family="monospace" font-size="11" fill="#2E7D32" font-weight="bold">停止</text>

  <!-- ===== 液压泵 (真实齿轮泵: 壳体+进出油口+齿轮示意) ===== -->
  <rect id="svg_pu0" x="130" y="290" width="90" height="46" rx="8" fill="url(#pumpShell)" stroke="#1A237E" stroke-width="2" filter="url(#shadow)"/>
  <!-- 内部齿轮示意(两个啮合齿轮轮廓) -->
  <circle id="svg_pu1" cx="158" cy="313" r="13" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="1.5" stroke-dasharray="4 3"/>
  <circle id="svg_pu2" cx="182" cy="313" r="13" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="1.5" stroke-dasharray="4 3"/>
  <!-- 旋转动画 -->
  <circle id="svg_pu3" cx="158" cy="313" r="4" fill="rgba(255,255,255,0.3)">
   <animateTransform attributeName="transform" type="rotate" from="0 158 313" to="360 158 313" dur="2s" repeatCount="indefinite"/>
  </circle>
  <circle id="svg_pu4" cx="182" cy="313" r="4" fill="rgba(255,255,255,0.3)">
   <animateTransform attributeName="transform" type="rotate" from="360 182 313" to="0 182 313" dur="2s" repeatCount="indefinite"/>
  </circle>
  <!-- 方向箭头 -->
  <polygon id="svg_pu5" points="170,296 175,302 165,302" fill="rgba(255,255,255,0.5)"/>
  <!-- 进油口(底部) -->
  <rect id="svg_pu6" x="170" y="334" width="14" height="10" rx="3" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <!-- 出油口(顶部) -->
  <rect id="svg_pu7" x="170" y="282" width="14" height="10" rx="3" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <!-- 铭牌 -->
  <text id="svg_pun" x="175" y="280" text-anchor="middle" font-family="Arial" font-size="9" fill="#9FA8DA" font-weight="bold">PUMP</text>

  <!-- ===== 压力表 (真实感: 圆形表盘+表壳+刻度+指针) ===== -->
  <!-- 表壳 -->
  <circle id="svg_pg0" cx="320" cy="210" r="28" fill="#424242" stroke="#212121" stroke-width="3" filter="url(#shadow)"/>
  <!-- 表盘 -->
  <circle id="svg_pg1" cx="320" cy="210" r="23" fill="url(#gaugeface)"/>
  <!-- 刻度(弧段) -->
  <path id="svg_pg2a" d="M 302 225 A 20 20 0 0 1 312 193" fill="none" stroke="#4CAF50" stroke-width="3" stroke-linecap="round"/>
  <path id="svg_pg2b" d="M 312 193 A 20 20 0 0 1 335 200" fill="none" stroke="#FFC107" stroke-width="3" stroke-linecap="round"/>
  <path id="svg_pg2c" d="M 335 200 A 20 20 0 0 1 338 225" fill="none" stroke="#F44336" stroke-width="3" stroke-linecap="round"/>
  <!-- 刻度数字 -->
  <text id="svg_pgn0" x="300" y="228" text-anchor="middle" font-family="Arial" font-size="6" fill="#666">0</text>
  <text id="svg_pgn1" x="306" y="198" text-anchor="middle" font-family="Arial" font-size="6" fill="#666">10</text>
  <text id="svg_pgn2" x="330" y="195" text-anchor="middle" font-family="Arial" font-size="6" fill="#666">20</text>
  <text id="svg_pgn3" x="340" y="228" text-anchor="middle" font-family="Arial" font-size="6" fill="#666">30</text>
  <!-- 指针 -->
  <line id="svg_pg3" x1="320" y1="210" x2="305" y2="223" stroke="#D32F2F" stroke-width="1.5"/>
  <circle id="svg_pg4" cx="320" cy="210" r="3" fill="#D32F2F"/>
  <!-- 单位 -->
  <text id="svg_pg5" x="320" y="222" text-anchor="middle" font-family="Arial" font-size="6" fill="#999">MPa</text>
  <!-- 连接管 -->
  <rect id="svg_pgp" x="316" y="236" width="8" height="22" rx="4" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <!-- 压力数值 -->
  <rect id="svg_pgd" x="355" y="198" width="85" height="24" rx="5" fill="#FCE4EC" stroke="#E91E63" stroke-width="1" filter="url(#shSm)"/>
  <text id="svg_pgv" x="397" y="215" text-anchor="middle" font-family="monospace" font-size="14" fill="#C62828" font-weight="bold">0.0 MPa</text>

  <!-- ===== 溢流阀 (真实感: 六角阀体+弹簧调节帽+管接头) ===== -->
  <!-- 阀体(主体) -->
  <rect id="svg_rv1" x="385" y="288" width="40" height="60" rx="4" fill="url(#valveBody)" stroke="#212121" stroke-width="2" filter="url(#shadow)"/>
  <!-- 六角螺纹外观 -->
  <rect id="svg_rv2" x="382" y="300" width="46" height="16" rx="2" fill="#4D4D4D" stroke="#333" stroke-width="1"/>
  <!-- 调节手柄(顶部旋钮) -->
  <rect id="svg_rv3" x="394" y="278" width="22" height="14" rx="4" fill="#757575" stroke="#555" stroke-width="1.5"/>
  <line id="svg_rv4" x1="405" y1="280" x2="405" y2="290" stroke="#999" stroke-width="1.5"/>
  <!-- 弹簧 -->
  <polyline id="svg_rv5" points="396,330 400,335 410,328 400,340 410,333 396,348" fill="none" stroke="#90A4AE" stroke-width="1.5"/>
  <!-- 进出口接头 -->
  <rect id="svg_rv6" x="398" y="258" width="14" height="32" rx="4" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <rect id="svg_rv7" x="398" y="346" width="14" height="8" rx="3" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <!-- 标签 -->
  <text id="svg_rvn" x="405" y="365" text-anchor="middle" font-family="Arial" font-size="9" fill="#757575">溢流阀</text>

  <!-- ===== 三位四通电磁换向阀 (真实感: 阀体块+两端电磁铁+位置指示) ===== -->
  <!-- 中央阀体(铝块) -->
  <rect id="svg_dv0" x="580" y="300" width="130" height="72" rx="4" fill="url(#valveBody)" stroke="#212121" stroke-width="2" filter="url(#shadow)"/>
  <!-- 阀体表面螺栓 -->
  <circle id="svg_dvb1" cx="595" cy="315" r="4" fill="#555" stroke="#444" stroke-width="1"/>
  <circle id="svg_dvb2" cx="695" cy="315" r="4" fill="#555" stroke="#444" stroke-width="1"/>
  <circle id="svg_dvb3" cx="595" cy="357" r="4" fill="#555" stroke="#444" stroke-width="1"/>
  <circle id="svg_dvb4" cx="695" cy="357" r="4" fill="#555" stroke="#444" stroke-width="1"/>

  <!-- 三个位置方格(中央指示面板) -->
  <rect id="svg_dvp0" x="610" y="318" width="70" height="36" rx="3" fill="#333" stroke="#555" stroke-width="1"/>
  <!-- 左位 -->
  <rect id="svg_dvp1" x="613" y="321" width="20" height="30" rx="2" fill="#2E3030"/>
  <text id="svg_dvp1t" x="623" y="340" text-anchor="middle" font-family="Arial" font-size="8" fill="#81C784">升</text>
  <!-- 中位(激活) -->
  <rect id="svg_dvp2" x="636" y="321" width="20" height="30" rx="2" fill="#444" stroke="#81C784" stroke-width="1"/>
  <text id="svg_dvp2t" x="646" y="340" text-anchor="middle" font-family="Arial" font-size="8" fill="#81C784" font-weight="bold">中</text>
  <!-- 右位 -->
  <rect id="svg_dvp3" x="659" y="321" width="20" height="30" rx="2" fill="#2E3030"/>
  <text id="svg_dvp3t" x="669" y="340" text-anchor="middle" font-family="Arial" font-size="8" fill="#81C784">降</text>

  <!-- P口(上, 进油) -->
  <rect id="svg_dvPc" x="618" y="293" width="14" height="10" rx="3" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <text id="svg_dvPt" x="625" y="292" text-anchor="middle" font-family="Arial" font-size="8" fill="#1976D2" font-weight="bold">P</text>
  <!-- T口(下, 回油) -->
  <rect id="svg_dvTc" x="668" y="370" width="14" height="10" rx="3" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <text id="svg_dvTt" x="675" y="388" text-anchor="middle" font-family="Arial" font-size="8" fill="#E65100" font-weight="bold">T</text>
  <!-- A口(左上) -->
  <rect id="svg_dvAc" x="618" y="260" width="14" height="10" rx="3" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <text id="svg_dvAt" x="611" y="268" text-anchor="end" font-family="Arial" font-size="8" fill="#1976D2" font-weight="bold">A</text>
  <!-- B口(右上) -->
  <rect id="svg_dvBc" x="668" y="260" width="14" height="10" rx="3" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <text id="svg_dvBt" x="690" y="268" font-family="Arial" font-size="8" fill="#1976D2" font-weight="bold">B</text>

  <!-- 左侧电磁铁(SOL-A) -->
  <rect id="svg_ea0" x="555" y="310" width="28" height="52" rx="4" fill="url(#solenoid)" stroke="#0D47A1" stroke-width="1.5" filter="url(#shSm)"/>
  <text id="svg_ea1" x="569" y="322" text-anchor="middle" font-family="Arial" font-size="6" fill="#90CAF9">SOL</text>
  <text id="svg_ea2" x="569" y="342" text-anchor="middle" font-family="Arial" font-size="14" fill="#BBDEFB" font-weight="bold">A</text>
  <!-- LED指示灯 -->
  <circle id="svg_ea3" cx="569" cy="355" r="4" fill="#4CAF50" opacity="0.3"/>
  <!-- 接线端子 -->
  <rect id="svg_ea4" x="562" y="305" width="14" height="7" rx="2" fill="#263238"/>

  <!-- 右侧电磁铁(SOL-B) -->
  <rect id="svg_eb0" x="707" y="310" width="28" height="52" rx="4" fill="url(#solenoid)" stroke="#0D47A1" stroke-width="1.5" filter="url(#shSm)"/>
  <text id="svg_eb1" x="721" y="322" text-anchor="middle" font-family="Arial" font-size="6" fill="#90CAF9">SOL</text>
  <text id="svg_eb2" x="721" y="342" text-anchor="middle" font-family="Arial" font-size="14" fill="#BBDEFB" font-weight="bold">B</text>
  <circle id="svg_eb3" cx="721" cy="355" r="4" fill="#4CAF50" opacity="0.3"/>
  <rect id="svg_eb4" x="714" y="305" width="14" height="7" rx="2" fill="#263238"/>

  <!-- 阀铭牌 -->
  <text id="svg_dvn" x="645" y="390" text-anchor="middle" font-family="Arial" font-size="10" fill="#757575" font-weight="bold">三位四通电磁换向阀</text>
  <!-- 阀状态 -->
  <rect id="svg_dvsd" x="740" y="322" width="80" height="24" rx="5" fill="#E8F5E9" stroke="#4CAF50" stroke-width="1" filter="url(#shSm)"/>
  <text id="svg_dvsl" x="750" y="338" font-family="Arial" font-size="9" fill="#2E7D32">阀位:</text>
  <text id="svg_dvsv" x="810" y="338" text-anchor="end" font-family="monospace" font-size="11" fill="#1B5E20" font-weight="bold">中位</text>

  <!-- ===== 液压缸 (真实感: 缸筒+端盖+活塞+杆+密封+耳环) ===== -->
  <!-- 尾端耳环(安装座) -->
  <circle id="svg_cye0" cx="915" cy="258" r="12" fill="url(#metalH)" stroke="#757575" stroke-width="2"/>
  <circle id="svg_cye1" cx="915" cy="258" r="5" fill="#ECEFF1" stroke="#9E9E9E" stroke-width="1"/>
  <!-- 缸筒(主体圆柱) -->
  <rect id="svg_cy0" x="920" y="228" width="200" height="60" rx="6" fill="url(#cylTube)" stroke="#546E7A" stroke-width="2" filter="url(#shadow)"/>
  <!-- 缸筒高光线 -->
  <line id="svg_cyhl" x1="925" y1="238" x2="1115" y2="238" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
  <line id="svg_cyhl2" x1="925" y1="278" x2="1115" y2="278" stroke="rgba(0,0,0,0.15)" stroke-width="1"/>
  <!-- 后端盖 -->
  <rect id="svg_cy1" x="916" y="224" width="14" height="68" rx="4" fill="#78909C" stroke="#546E7A" stroke-width="2"/>
  <!-- 前端盖(导向套) -->
  <rect id="svg_cy2" x="1105" y="230" width="20" height="56" rx="4" fill="#78909C" stroke="#546E7A" stroke-width="2"/>
  <!-- 活塞杆(亮银色, 从前端盖伸出) -->
  <rect id="svg_cy3" x="1110" y="247" width="100" height="22" rx="11" fill="url(#rodGrad)" stroke="#9E9E9E" stroke-width="1.5"/>
  <!-- 杆端关节轴承(耳环) -->
  <circle id="svg_cye2" cx="1210" cy="258" r="14" fill="url(#metalH)" stroke="#757575" stroke-width="2"/>
  <circle id="svg_cye3" cx="1210" cy="258" r="6" fill="#ECEFF1" stroke="#9E9E9E" stroke-width="1"/>
  <!-- 活塞位置指示(内部) -->
  <rect id="svg_cy4" x="1000" y="234" width="8" height="48" rx="2" fill="#546E7A" stroke="#455A64" stroke-width="1" opacity="0.6"/>
  <!-- 油口标记 -->
  <rect id="svg_cyAp" x="933" y="220" width="14" height="10" rx="3" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <rect id="svg_cyBp" x="1088" y="220" width="14" height="10" rx="3" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <text id="svg_cya" x="940" y="218" font-family="Arial" font-size="8" fill="#1976D2" font-weight="bold">A</text>
  <text id="svg_cyb" x="1095" y="218" font-family="Arial" font-size="8" fill="#1976D2" font-weight="bold">B</text>

  <!-- 缸铭牌 -->
  <text id="svg_cyn" x="1020" y="266" text-anchor="middle" font-family="Arial" font-size="10" fill="#455A64" font-weight="bold">HYDRAULIC CYLINDER</text>

  <!-- 行程数据 -->
  <rect id="svg_cyd" x="920" y="298" width="200" height="24" rx="5" fill="#E3F2FD" stroke="#64B5F6" stroke-width="1" filter="url(#shSm)"/>
  <text id="svg_cdl" x="930" y="314" font-family="Arial" font-size="10" fill="#1565C0">行程:</text>
  <text id="svg_cdv" x="1110" y="314" text-anchor="end" font-family="monospace" font-size="13" fill="#0D47A1" font-weight="bold">0.0 %</text>
  <!-- 行程进度条 -->
  <rect id="svg_cpb0" x="920" y="326" width="200" height="8" rx="4" fill="#CFD8DC"/>
  <rect id="svg_cpb1" x="920" y="326" width="0" height="8" rx="4" fill="#42A5F5"/>

  <!-- ===== 支撑臂 (机械结构) ===== -->
  <!-- 臂体(工字钢截面) -->
  <line id="svg_ar1" x1="1216" y1="258" x2="1330" y2="175" stroke="#6D4C41" stroke-width="18" stroke-linecap="round" filter="url(#shadow)"/>
  <line id="svg_ar2" x1="1216" y1="258" x2="1330" y2="175" stroke="#8D6E63" stroke-width="12" stroke-linecap="round"/>
  <!-- 工字钢中心线 -->
  <line id="svg_ar3" x1="1216" y1="258" x2="1330" y2="175" stroke="#795548" stroke-width="4" stroke-linecap="round"/>
  <!-- 铰接点(关节轴承) -->
  <circle id="svg_ar4" cx="1216" cy="258" r="8" fill="#5D4037" stroke="#3E2723" stroke-width="2"/>
  <circle id="svg_ar5" cx="1216" cy="258" r="3" fill="#8D6E63"/>
  <!-- 末端(被支撑物) -->
  <circle id="svg_ar6" cx="1330" cy="175" r="6" fill="#A1887F" stroke="#5D4037" stroke-width="2"/>
  <!-- 基座 -->
  <rect id="svg_ar7" x="1200" y="268" width="32" height="10" rx="3" fill="#5D4037" stroke="#3E2723" stroke-width="1"/>
  <rect id="svg_ar8" x="1192" y="277" width="48" height="8" rx="3" fill="#8D6E63" stroke="#5D4037" stroke-width="1"/>
  <text id="svg_arn" x="1290" y="165" text-anchor="middle" font-family="Arial" font-size="12" fill="#5D4037" font-weight="bold">支撑臂</text>

  <!-- ================================================================ -->
  <!--                        图例                                       -->
  <!-- ================================================================ -->
  <rect id="svg_lg0" x="50" y="670" width="400" height="36" rx="6" fill="white" stroke="#BDBDBD" stroke-width="1" filter="url(#shSm)"/>
  <text id="svg_lg1" x="65" y="693" font-family="Arial" font-size="10" fill="#555" font-weight="bold">图例:</text>
  <rect id="svg_lg2" x="100" y="683" width="30" height="10" rx="5" fill="url(#pipeBlueH)"/>
  <text id="svg_lg3" x="135" y="693" font-family="Arial" font-size="10" fill="#555">压力油路</text>
  <rect id="svg_lg4" x="195" y="683" width="30" height="10" rx="5" fill="url(#pipeOrangeH)"/>
  <text id="svg_lg5" x="230" y="693" font-family="Arial" font-size="10" fill="#555">回油油路</text>
  <line id="svg_lg6" x1="290" y1="688" x2="320" y2="688" stroke="#90CAF9" stroke-width="2" stroke-dasharray="6 4"/>
  <text id="svg_lg7" x="325" y="693" font-family="Arial" font-size="10" fill="#555">油液流动</text>
  <circle id="svg_lg8" cx="395" cy="688" r="5" fill="url(#metalH)" stroke="#757575" stroke-width="1"/>
  <text id="svg_lg9" x="405" y="693" font-family="Arial" font-size="10" fill="#555">管接头</text>

  <!-- ================================================================ -->
  <!--                     底部操作控制面板                               -->
  <!-- ================================================================ -->
  <rect id="svg_cp" x="50" y="720" width="1300" height="165" rx="8" fill="white" stroke="#BDBDBD" stroke-width="1" filter="url(#shadow)"/>
  <rect id="svg_cph" x="50" y="720" width="1300" height="30" rx="8" fill="#37474F"/>
  <rect id="svg_cph2" x="50" y="740" width="1300" height="10" fill="#37474F"/>
  <text id="svg_cpt" x="700" y="741" text-anchor="middle" font-family="Arial" font-size="14" fill="#ECEFF1" font-weight="bold">操作控制面板</text>

  <!-- 操作说明 -->
  <text id="svg_od1" x="70" y="773" font-family="Arial" font-size="11" fill="#666">升起: 电磁铁A得电, 换向阀左位, P->A进油, 液压缸伸出, 支撑臂升起</text>
  <text id="svg_od2" x="70" y="791" font-family="Arial" font-size="11" fill="#666">降落: 电磁铁B得电, 换向阀右位, P->B进油, 液压缸缩回, 支撑臂降落</text>
  <text id="svg_od3" x="70" y="809" font-family="Arial" font-size="11" fill="#666">停止: 双弹簧复位中位, 所有油口封闭, 液压目锁定</text>

  <!-- 升起按钮 -->
  <rect id="svg_bu1" x="780" y="762" width="180" height="50" rx="10" fill="#2E7D32" stroke="#1B5E20" stroke-width="2" filter="url(#shadow)"/>
  <rect id="svg_bu1h" x="784" y="766" width="172" height="18" rx="8" fill="rgba(255,255,255,0.15)"/>
  <text id="svg_bu1t" x="870" y="795" text-anchor="middle" font-family="Arial" font-size="22" fill="white" font-weight="bold">升 起</text>

  <!-- 降落按钮 -->
  <rect id="svg_bd1" x="990" y="762" width="180" height="50" rx="10" fill="#C62828" stroke="#B71C1C" stroke-width="2" filter="url(#shadow)"/>
  <rect id="svg_bd1h" x="994" y="766" width="172" height="18" rx="8" fill="rgba(255,255,255,0.15)"/>
  <text id="svg_bd1t" x="1080" y="795" text-anchor="middle" font-family="Arial" font-size="22" fill="white" font-weight="bold">降 落</text>

  <!-- 系统综合状态 -->
  <rect id="svg_ss0" x="70" y="825" width="580" height="45" rx="6" fill="#F5F5F5" stroke="#E0E0E0"/>
  <text id="svg_ss1" x="85" y="845" font-family="Arial" font-size="11" fill="#333" font-weight="bold">系统状态</text>
  <line id="svg_ssl" x1="155" y1="832" x2="155" y2="858" stroke="#E0E0E0"/>
  <text id="svg_ss2" x="170" y="845" font-family="Arial" font-size="10" fill="#666">液压泵:</text>
  <text id="svg_ssv1" x="220" y="845" font-family="monospace" font-size="11" fill="#2E7D32" font-weight="bold">停止</text>
  <text id="svg_ss3" x="285" y="845" font-family="Arial" font-size="10" fill="#666">换向阀:</text>
  <text id="svg_ssv2" x="340" y="845" font-family="monospace" font-size="11" fill="#2E7D32" font-weight="bold">中位</text>
  <text id="svg_ss4" x="400" y="845" font-family="Arial" font-size="10" fill="#666">系统压力:</text>
  <text id="svg_ssv3" x="465" y="845" font-family="monospace" font-size="11" fill="#C62828" font-weight="bold">0.0 MPa</text>
  <text id="svg_ss5" x="550" y="845" font-family="Arial" font-size="10" fill="#666">行程:</text>
  <text id="svg_ssv4" x="590" y="845" font-family="monospace" font-size="11" fill="#0D47A1" font-weight="bold">0%</text>
  <text id="svg_ss6" x="85" y="863" font-family="Arial" font-size="10" fill="#E65100">报警:</text>
  <circle id="svg_ss7" cx="125" cy="859" r="5" fill="#4CAF50"/>
  <text id="svg_ssv5" x="135" y="863" font-family="monospace" font-size="11" fill="#4CAF50" font-weight="bold">无报警 - 系统正常</text>

  <!-- 状态指示灯 -->
  <rect id="svg_si0" x="780" y="825" width="390" height="45" rx="6" fill="#F5F5F5" stroke="#E0E0E0"/>
  <text id="svg_si1" x="800" y="845" font-family="Arial" font-size="11" fill="#333" font-weight="bold">指示灯</text>
  <circle id="svg_si2" cx="870" cy="843" r="8" fill="#4CAF50" stroke="#388E3C" stroke-width="1.5"/>
  <text id="svg_si3" x="883" y="847" font-family="Arial" font-size="10" fill="#555">运行</text>
  <circle id="svg_si4" cx="930" cy="843" r="8" fill="#E0E0E0" stroke="#BDBDBD" stroke-width="1.5"/>
  <text id="svg_si5" x="943" y="847" font-family="Arial" font-size="10" fill="#999">报警</text>
  <circle id="svg_si6" cx="990" cy="843" r="8" fill="#E0E0E0" stroke="#BDBDBD" stroke-width="1.5"/>
  <text id="svg_si7" x="1003" y="847" font-family="Arial" font-size="10" fill="#999">故障</text>
  <circle id="svg_si8" cx="1050" cy="843" r="8" fill="#BDBDBD" stroke="#9E9E9E" stroke-width="1.5"/>
  <text id="svg_si9" x="1063" y="847" font-family="Arial" font-size="10" fill="#999">待机</text>
  <text id="svg_sil" x="1110" y="847" font-family="Arial" font-size="10" fill="#666">当前:</text>
  <text id="svg_siv" x="1150" y="847" font-family="monospace" font-size="12" fill="#757575" font-weight="bold">待机中</text>
 </g>
</svg>'''

# 获取并更新项目
req = urllib.request.Request(f'{BASE_URL}/api/project')
resp = urllib.request.urlopen(req, timeout=10)
project = json.loads(resp.read().decode())

found = False
for i, v in enumerate(project['hmi']['views']):
    if v['id'] == 'v_hydraulic_arm_01':
        project['hmi']['views'][i]['svgcontent'] = svg
        # 更新视图尺寸
        project['hmi']['views'][i]['profile']['width'] = 1400
        project['hmi']['views'][i]['profile']['height'] = 900
        project['hmi']['views'][i]['profile']['bkcolor'] = '#ECEFF1'
        print(f'更新视图 SVG: {len(svg)} chars')
        found = True
        break

if not found:
    # 创建新视图
    new_view = {
        'id': 'v_hydraulic_arm_01',
        'name': '液压支撑臂',
        'profile': {
            'width': 1400,
            'height': 900,
            'bkcolor': '#ECEFF1'
        },
        'svgcontent': svg,
        'items': {}
    }
    project['hmi']['views'].append(new_view)
    print(f'创建新视图: {len(svg)} chars')

body = json.dumps(project).encode('utf-8')
req = urllib.request.Request(
    f'{BASE_URL}/api/project',
    data=body,
    headers={'Content-Type': 'application/json'},
    method='POST'
)
resp = urllib.request.urlopen(req, timeout=30)
print(f'项目更新: HTTP {resp.status}')

# 验证
import time; time.sleep(1)
req = urllib.request.Request(f'{BASE_URL}/api/project')
resp = urllib.request.urlopen(req, timeout=10)
data = json.loads(resp.read().decode())
for v in data.get('hmi', {}).get('views', []):
    if v.get('id') == 'v_hydraulic_arm_01':
        s = v.get('svgcontent', '')
        print(f'SVG 长度: {len(s)} chars')
        checks = ['PUMP', 'MOTOR', 'OIL TANK', 'CYLINDER', 'SOL', 'animate', 'metalH', 'shadow']
        for kw in checks:
            print(f'  包含 "{kw}": {"Yes" if kw in s else "No"}')
        break

print('完成! 请刷新浏览器 http://localhost:1881 查看效果')
