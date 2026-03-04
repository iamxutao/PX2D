#!/usr/bin/env python3
"""
真实风格液压支撑臂原理图 (带完整动画与交互逻辑)
修复了布局、添加了流动动画脚本、技术参数、设备标牌和停止按钮
"""
import urllib.request, json, time

BASE_URL = 'http://localhost:1881'

svg = '''<svg width="1600" height="950" viewBox="0 0 1600 950" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
 <defs>
  <!-- 重金属质感渐变(水平/垂直) -->
  <linearGradient id="metalH" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#D0D0D0"/><stop offset="25%" stop-color="#B8B8B8"/>
   <stop offset="50%" stop-color="#A8A8A8"/><stop offset="75%" stop-color="#C0C0C0"/><stop offset="100%" stop-color="#989898"/>
  </linearGradient>
  <linearGradient id="metalV" x1="0" y1="0" x2="1" y2="0">
   <stop offset="0%" stop-color="#C8C8C8"/><stop offset="30%" stop-color="#A8A8A8"/>
   <stop offset="70%" stop-color="#B8B8B8"/><stop offset="100%" stop-color="#909090"/>
  </linearGradient>
  <!-- 外壳颜色梯队 -->
  <linearGradient id="tankBody" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#546E7A"/><stop offset="50%" stop-color="#37474F"/><stop offset="100%" stop-color="#263238"/>
  </linearGradient>
  <linearGradient id="motorShell" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#607D8B"/><stop offset="20%" stop-color="#455A64"/>
   <stop offset="80%" stop-color="#37474F"/><stop offset="100%" stop-color="#263238"/>
  </linearGradient>
  <linearGradient id="pumpShell" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#3F51B5"/><stop offset="50%" stop-color="#283593"/><stop offset="100%" stop-color="#1A237E"/>
  </linearGradient>
  <linearGradient id="valveBody" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#757575"/><stop offset="30%" stop-color="#616161"/><stop offset="100%" stop-color="#424242"/>
  </linearGradient>
  <linearGradient id="cylTube" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#B0BEC5"/><stop offset="25%" stop-color="#90A4AE"/>
   <stop offset="50%" stop-color="#78909C"/><stop offset="75%" stop-color="#90A4AE"/><stop offset="100%" stop-color="#607D8B"/>
  </linearGradient>
  
  <!-- 内部/细节特效 -->
  <linearGradient id="oilFill" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#FFCA28"/><stop offset="100%" stop-color="#EF6C00"/>
  </linearGradient>
  <linearGradient id="solenoid" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#1976D2"/><stop offset="100%" stop-color="#0D47A1"/>
  </linearGradient>
  <linearGradient id="rodGrad" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0%" stop-color="#F5F5F5"/><stop offset="40%" stop-color="#FFFFFF"/>
   <stop offset="60%" stop-color="#EEEEEE"/><stop offset="100%" stop-color="#BDBDBD"/>
  </linearGradient>

  <radialGradient id="gaugeface" cx="50%" cy="50%" r="50%">
   <stop offset="0%" stop-color="#FFFFFF"/><stop offset="85%" stop-color="#F5F5F5"/><stop offset="100%" stop-color="#E0E0E0"/>
  </radialGradient>

  <!-- 阴影特效 -->
  <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
   <feDropShadow dx="3" dy="4" stdDeviation="4" flood-color="rgba(0,0,0,0.3)"/>
  </filter>
  <filter id="shSm" x="-10%" y="-10%" width="120%" height="120%">
   <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="rgba(0,0,0,0.2)"/>
  </filter>
 </defs>

 <g>
  <!-- ========================================== -->
  <!-- 背景与标题 -->
  <rect id="svg_bg" fill="#E8EAED" width="1600" height="950"/>
  
  <rect x="450" y="15" width="700" height="46" rx="6" fill="#2C3E50" filter="url(#shadow)"/>
  <text x="800" y="45" text-anchor="middle" font-family="SimHei,Arial" font-size="22" fill="#ECEFF1" font-weight="bold">液压支撑臂真实控制系统 (FUXA SCADA)</text>

  <!-- ========================================== -->
  <!-- 下层: 管路系统 (先画,被设备盖住) -->
  
  <!-- 管路配色(支持脚本动态更改颜色): P/B=蓝色 T/A=橙色 初始静止=灰 -->
  <!-- P 压力主管 y=280-->
  <rect id="pipePm" x="210" y="272" width="600" height="16" rx="8" fill="#42A5F5" filter="url(#shSm)"/>
  <line id="flowP" x1="210" y1="280" x2="800" y2="280" stroke="#E3F2FD" stroke-width="4" stroke-dasharray="16 12" opacity="0">
   <animate attributeName="stroke-dashoffset" from="0" to="-28" dur="0.6s" repeatCount="indefinite"/>
  </line>

  <!-- T 回油主管 y=560 -->
  <rect id="pipeRm" x="210" y="552" width="600" height="16" rx="8" fill="#FFA726" filter="url(#shSm)"/>
  <line id="flowT" x1="800" y1="560" x2="210" y2="560" stroke="#FFF3E0" stroke-width="4" stroke-dasharray="16 12" opacity="0">
   <animate attributeName="stroke-dashoffset" from="0" to="-28" dur="0.6s" repeatCount="indefinite"/>
  </line>

  <!-- 吸油管 (油箱到泵) -->
  <rect id="pipeSp" x="210" y="460" width="16" height="100" rx="8" fill="#42A5F5" filter="url(#shSm)"/>
  <line id="flowS" x1="218" y1="550" x2="218" y2="460" stroke="#E3F2FD" stroke-width="4" stroke-dasharray="12 10" opacity="0">
   <animate attributeName="stroke-dashoffset" from="0" to="22" dur="0.7s" repeatCount="indefinite"/>
  </line>

  <!-- 出油管 (泵到P主管) -->
  <rect id="pipeDp" x="210" y="280" width="16" height="80" rx="8" fill="#42A5F5" filter="url(#shSm)"/>
  <line id="flowD" x1="218" y1="355" x2="218" y2="280" stroke="#E3F2FD" stroke-width="4" stroke-dasharray="12 10" opacity="0">
   <animate attributeName="stroke-dashoffset" from="0" to="22" dur="0.7s" repeatCount="indefinite"/>
  </line>

  <!-- 溢流阀管路 -->
  <rect id="pipeRVp" x="430" y="288" width="16" height="30" rx="8" fill="#42A5F5"/>
  <rect id="pipeRVt" x="430" y="378" width="16" height="182" rx="8" fill="#FFA726"/>
  <line id="flowRV" x1="438" y1="380" x2="438" y2="560" stroke="#FFF3E0" stroke-width="3" stroke-dasharray="10 8" opacity="0">
   <animate attributeName="stroke-dashoffset" from="0" to="-18" dur="0.8s" repeatCount="indefinite"/>
  </line>

  <!-- 换向阀P、T竖管 -->
  <rect id="pipeDVp" x="710" y="288" width="16" height="42" rx="8" fill="#42A5F5"/>
  <rect id="pipeDVt" x="760" y="408" width="16" height="152" rx="8" fill="#FFA726"/>
  <line id="flowDVt" x1="768" y1="410" x2="768" y2="560" stroke="#FFF3E0" stroke-width="3" stroke-dasharray="10 8" opacity="0">
   <animate attributeName="stroke-dashoffset" from="0" to="-18" dur="0.6s" repeatCount="indefinite"/>
  </line>

  <!-- A管路(换向阀→无杆腔) -->
  <rect id="pipeAv" x="710" y="180" width="16" height="110" rx="8" fill="#B0BEC5"/>
  <rect id="pipeAh" x="718" y="172" width="370" height="16" rx="8" fill="#B0BEC5" filter="url(#shSm)"/>
  <rect id="pipeAd" x="1072" y="180" width="16" height="60" rx="8" fill="#B0BEC5"/>
  
  <line id="flowAv" x1="718" y1="285" x2="718" y2="185" stroke="#FFF" stroke-width="3" stroke-dasharray="10 8" opacity="0">
   <animate id="animAv" attributeName="stroke-dashoffset" from="0" to="18" dur="0.5s" repeatCount="indefinite"/>
  </line>
  <line id="flowAh" x1="720" y1="180" x2="1080" y2="180" stroke="#FFF" stroke-width="3" stroke-dasharray="10 8" opacity="0">
   <animate id="animAh" attributeName="stroke-dashoffset" from="0" to="-18" dur="0.5s" repeatCount="indefinite"/>
  </line>

  <!-- B管路(换向阀→有杆腔) 更高位 -->
  <rect id="pipeBv" x="760" y="130" width="16" height="160" rx="8" fill="#B0BEC5"/>
  <rect id="pipeBh" x="768" y="122" width="480" height="16" rx="8" fill="#B0BEC5" filter="url(#shSm)"/>
  <rect id="pipeBd" x="1232" y="130" width="16" height="110" rx="8" fill="#B0BEC5"/>

  <line id="flowBh" x1="770" y1="130" x2="1240" y2="130" stroke="#FFF" stroke-width="3" stroke-dasharray="10 8" opacity="0">
  <animate id="animBh" attributeName="stroke-dashoffset" from="0" to="-18" dur="0.5s" repeatCount="indefinite"/>
  </line>

  <!-- 管系文字标签 -->
  <rect x="520" y="258" width="70" height="20" rx="3" fill="rgba(255,255,255,0.7)"/>
  <text x="555" y="272" text-anchor="middle" font-family="Arial" font-size="12" fill="#1565C0" font-weight="bold">P 压力油路</text>
  <rect x="520" y="538" width="70" height="20" rx="3" fill="rgba(255,255,255,0.7)"/>
  <text x="555" y="552" text-anchor="middle" font-family="Arial" font-size="12" fill="#E65100" font-weight="bold">T 回油油路</text>

  <!-- ========================================== -->
  <!-- 设备层 -->
  
  <!-- === 1. 油箱系统 === -->
  <g transform="translate(130, 550)">
   <!-- 箱体 -->
   <rect x="0" y="0" width="180" height="130" rx="6" fill="url(#tankBody)" stroke="#1A237E" stroke-width="2" filter="url(#shadow)"/>
   <!-- 顶盖 -->
   <rect x="0" y="0" width="180" height="15" rx="4" fill="#607D8B" stroke="#263238" stroke-width="1"/>
   <!-- 加油口 -->
   <path d="M 140 0 L 140 -10 L 160 -10 L 160 0 Z" fill="#455A64" stroke="#263238"/>
   <rect x="135" y="-14" width="30" height="4" rx="2" fill="#78909C"/>
   <!-- 视液窗 -->
   <rect x="20" y="30" width="24" height="80" rx="12" fill="#202020" stroke="#455A64" stroke-width="3"/>
   <rect x="24" y="34" width="16" height="72" rx="8" fill="#37474F"/>
   <clipPath id="tkLvl"><rect x="24" y="34" width="16" height="72" rx="8"/></clipPath>
   <rect id="oilLevel" x="24" y="45" width="16" height="61" fill="url(#oilFill)" clip-path="url(#tkLvl)"/>
   <!-- 波纹 -->
   <path id="oilWave" d="M 24 45 Q 28 42 32 45 Q 36 48 40 45" fill="none" stroke="#FFD54F" stroke-width="1" clip-path="url(#tkLvl)" opacity="0">
    <animate attributeName="d" values="M 24 45 Q 28 42 32 45 Q 36 48 40 45;M 24 45 Q 28 48 32 45 Q 36 42 40 45;M 24 45 Q 28 42 32 45 Q 36 48 40 45" dur="1.5s" repeatCount="indefinite"/>
   </path>
   <!-- 温度/液位表盘 -->
   <rect x="60" y="30" width="100" height="40" rx="4" fill="#FFF8E1" stroke="#FFB300" stroke-width="1"/>
   <text x="65" y="45" font-family="Arial" font-size="11" fill="#E65100">Temp:</text>
   <text x="155" y="45" text-anchor="end" font-family="monospace" font-size="13" fill="#BF360C" font-weight="bold">28.5 °C</text>
   <text x="65" y="62" font-family="Arial" font-size="11" fill="#E65100">Level:</text>
   <text x="155" y="62" text-anchor="end" font-family="monospace" font-size="13" fill="#BF360C" font-weight="bold">82.0 %</text>
   <!-- 标牌 -->
   <rect x="60" y="85" width="100" height="25" rx="2" fill="#37474F" stroke="#78909C" stroke-width="1"/>
   <text x="110" y="102" text-anchor="middle" font-family="Arial" font-size="12" fill="#B0BEC5" font-weight="bold">OIL TANK 200L</text>
  </g>

  <!-- === 2. 电动机 === -->
  <g transform="translate(130, 390)">
   <!-- 散热外壳 -->
   <rect x="0" y="15" width="130" height="70" rx="10" fill="url(#motorShell)" stroke="#263238" stroke-width="2" filter="url(#shadow)"/>
   <!-- 散热鳍片 -->
   <line x1="15" y1="25" x2="115" y2="25" stroke="#37474F" stroke-width="2"/>
   <line x1="15" y1="35" x2="115" y2="35" stroke="#37474F" stroke-width="2"/>
   <line x1="15" y1="45" x2="115" y2="45" stroke="#37474F" stroke-width="2"/>
   <line x1="15" y1="55" x2="115" y2="55" stroke="#37474F" stroke-width="2"/>
   <line x1="15" y1="65" x2="115" y2="65" stroke="#37474F" stroke-width="2"/>
   <line x1="15" y1="75" x2="115" y2="75" stroke="#37474F" stroke-width="2"/>
   <!-- 前后端盖 -->
   <rect x="0" y="15" width="18" height="70" rx="6" fill="#546E7A" stroke="#263238" stroke-width="1"/>
   <rect x="112" y="15" width="18" height="70" rx="6" fill="#546E7A" stroke="#263238" stroke-width="1"/>
   <!-- 接线盒 -->
   <rect x="40" y="0" width="50" height="18" rx="3" fill="#455A64" stroke="#263238" stroke-width="1"/>
   <path d="M 45 4 L 85 4 Z M 45 10 L 85 10 Z" stroke="#37474F" stroke-width="1.5"/>
   <!-- 轴 -->
   <rect x="60" y="-12" width="10" height="28" rx="2" fill="url(#metalV)"/>
   <!-- 标牌指示灯 -->
   <rect x="145" y="35" width="60" height="30" rx="4" fill="#ECEFF1" stroke="#CFD8DC" stroke-width="1"/>
   <circle id="motorLED" cx="158" cy="50" r="6" fill="#9E9E9E" stroke="#757575" stroke-width="1"/>
   <text id="motorTxt" x="185" y="54" text-anchor="middle" font-family="Arial" font-size="11" fill="#757575" font-weight="bold">STOP</text>
   <text x="65" y="105" text-anchor="middle" font-family="Arial" font-size="11" fill="#455A64" font-weight="bold">MOTOR 7.5kW</text>
  </g>

  <!-- === 3. 齿轮泵 === -->
  <g transform="translate(150, 270)">
   <!-- 泵壳体 -->
   <rect x="0" y="0" width="90" height="60" rx="12" fill="url(#pumpShell)" stroke="#1A237E" stroke-width="2" filter="url(#shadow)"/>
   <!-- 旋转动画(代表活塞/齿轮工作) -->
   <circle cx="28" cy="30" r="16" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2" stroke-dasharray="6 4"/>
   <circle cx="62" cy="30" r="16" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2" stroke-dasharray="6 4"/>
   <!-- 动画锚点 -->
   <g id="pumpGear1" transform="rotate(0, 28, 30)">
    <circle cx="28" cy="20" r="3" fill="rgba(255,255,255,0.4)"/>
    <circle cx="28" cy="40" r="3" fill="rgba(255,255,255,0.4)"/>
   </g>
   <g id="pumpGear2" transform="rotate(0, 62, 30)">
    <circle cx="62" cy="20" r="3" fill="rgba(255,255,255,0.4)"/>
    <circle cx="62" cy="40" r="3" fill="rgba(255,255,255,0.4)"/>
   </g>
   <!-- 标牌 -->
   <text x="45" y="34" text-anchor="middle" font-family="Arial" font-size="11" fill="#C5CAE9" font-weight="bold">PUMP</text>
   <text x="45" y="46" text-anchor="middle" font-family="Arial" font-size="9" fill="#9FA8DA">16mL/r</text>
  </g>

  <!-- === 4. 压力表 === -->
  <g transform="translate(320, 160)">
   <!-- 连接管 -->
   <rect x="25" y="80" width="10" height="35" rx="3" fill="url(#metalV)" stroke="#757575"/>
   <!-- 表壳 -->
   <circle cx="30" cy="40" r="38" fill="#424242" stroke="#212121" stroke-width="4" filter="url(#shadow)"/>
   <circle cx="30" cy="40" r="33" fill="url(#gaugeface)"/>
   <!-- 刻度弧 -->
   <path d="M 8 55 A 26 26 0 0 1 18 18" fill="none" stroke="#4CAF50" stroke-width="4" stroke-linecap="round"/>
   <path d="M 18 18 A 26 26 0 0 1 48 22" fill="none" stroke="#FFC107" stroke-width="4" stroke-linecap="round"/>
   <path d="M 48 22 A 26 26 0 0 1 54 53" fill="none" stroke="#F44336" stroke-width="4" stroke-linecap="round"/>
   <text x="4" y="65" font-family="Arial" font-size="8" fill="#666">0</text>
   <text x="48" y="16" font-family="Arial" font-size="8" fill="#666">16</text>
   <text x="60" y="65" font-family="Arial" font-size="8" fill="#666">25</text>
   <text x="30" y="58" text-anchor="middle" font-family="Arial" font-size="8" fill="#999">MPa</text>
   <!-- 指针 -->
   <g id="gaugeNeedleLRotate" transform="rotate(-40, 30, 40)">
    <polygon points="28,45 32,45 30,12" fill="#D32F2F"/>
    <circle cx="30" cy="40" r="4" fill="#D32F2F"/>
   </g>
   <!-- 数值板 -->
   <rect x="80" y="30" width="90" height="30" rx="4" fill="#FCE4EC" stroke="#E91E63" stroke-width="1"/>
   <text id="gaugePressTxt" x="125" y="51" text-anchor="middle" font-family="monospace" font-size="16" fill="#C62828" font-weight="bold">0.0 MPa</text>
  </g>

  <!-- === 5. 溢流阀 === -->
  <g transform="translate(410, 318)">
   <rect x="0" y="0" width="56" height="60" rx="8" fill="url(#valveBody)" stroke="#212121" stroke-width="2" filter="url(#shadow)"/>
   <!-- 阀芯六角端 -->
   <path d="M 0 10 L 10 0 L 46 0 L 56 10 Z" fill="#616161" stroke="#424242"/>
   <rect x="-6" y="25" width="68" height="15" rx="3" fill="#4D4D4D" stroke="#333" stroke-width="2"/>
   <!-- 调节手柄 -->
   <rect x="18" y="-12" width="20" height="12" rx="4" fill="#757575" stroke="#555" stroke-width="1.5"/>
   <line x1="28" y1="0" x2="28" y2="10" stroke="#999" stroke-width="2"/>
   <rect x="12" y="-16" width="32" height="6" rx="2" fill="#424242"/>
   <text x="28" y="55" text-anchor="middle" font-family="Arial" font-size="10" fill="#BDBDBD" font-weight="bold">RELIEF VAL</text>
   <text x="28" y="75" text-anchor="middle" font-family="Arial" font-size="10" fill="#EF5350" font-weight="bold">16.0 MPa</text>
  </g>

  <!-- === 6. 换向阀 (包括电磁铁) === -->
  <g transform="translate(560, 330)">
   <!-- 主阀体 -->
   <rect x="60" y="0" width="180" height="78" rx="6" fill="url(#valveBody)" stroke="#212121" stroke-width="2" filter="url(#shadow)"/>
   <circle cx="75" cy="15" r="4" fill="#555" stroke="#444"/>
   <circle cx="225" cy="15" r="4" fill="#555" stroke="#444"/>
   <circle cx="75" cy="63" r="4" fill="#555" stroke="#444"/>
   <circle cx="225" cy="63" r="4" fill="#555" stroke="#444"/>

   <!-- 状态指示屏 -->
   <rect x="90" y="16" width="120" height="46" rx="4" fill="#212121" stroke="#555" stroke-width="2"/>
   <!-- 左/中/右位块 -->
   <rect id="posLeft" x="96" y="22" width="30" height="34" rx="2" fill="#333"/>
   <text id="posLeftTxt" x="111" y="44" text-anchor="middle" font-family="Arial" font-size="10" fill="#4CAF50" opacity="0.3" font-weight="bold">升</text>
   <rect id="posCenter" x="135" y="22" width="30" height="34" rx="2" fill="#444" stroke="#4CAF50" stroke-width="2"/>
   <text id="posCenterTxt" x="150" y="44" text-anchor="middle" font-family="Arial" font-size="10" fill="#4CAF50" opacity="1.0" font-weight="bold">中</text>
   <rect id="posRight" x="174" y="22" width="30" height="34" rx="2" fill="#333"/>
   <text id="posRightTxt" x="189" y="44" text-anchor="middle" font-family="Arial" font-size="10" fill="#4CAF50" opacity="0.3" font-weight="bold">降</text>

   <!-- 电磁铁 A (左侧) -->
   <rect x="25" y="10" width="35" height="58" rx="6" fill="url(#solenoid)" stroke="#0D47A1" stroke-width="2" filter="url(#shSm)"/>
   <text x="42" y="32" text-anchor="middle" font-family="Arial" font-size="10" fill="#90CAF9" font-weight="bold">SOL</text>
   <text x="42" y="52" text-anchor="middle" font-family="Arial" font-size="20" fill="#BBDEFB" font-weight="bold">A</text>
   <circle id="ledA" cx="42" cy="60" r="4" fill="#4CAF50" opacity="0.2"/>
   <rect x="35" y="4" width="14" height="6" rx="2" fill="#263238"/> <!-- 端子 -->

   <!-- 电磁铁 B (右侧) -->
   <rect x="240" y="10" width="35" height="58" rx="6" fill="url(#solenoid)" stroke="#0D47A1" stroke-width="2" filter="url(#shSm)"/>
   <text x="257" y="32" text-anchor="middle" font-family="Arial" font-size="10" fill="#90CAF9" font-weight="bold">SOL</text>
   <text x="257" y="52" text-anchor="middle" font-family="Arial" font-size="20" fill="#BBDEFB" font-weight="bold">B</text>
   <circle id="ledB" cx="257" cy="60" r="4" fill="#4CAF50" opacity="0.2"/>
   <rect x="250" y="4" width="14" height="6" rx="2" fill="#263238"/>

   <text x="150" y="98" text-anchor="middle" font-family="Arial" font-size="13" fill="#616161" font-weight="bold">4/3 WAY VALVE</text>
  </g>

  <!-- === 7. 液压缸 === -->
  <g transform="translate(1080, 240)">
   <!-- 缸体外壳 -->
   <rect x="0" y="0" width="260" height="70" rx="8" fill="url(#cylTube)" stroke="#455A64" stroke-width="2" filter="url(#shadow)"/>
   <line x1="5" y1="12" x2="255" y2="12" stroke="rgba(255,255,255,0.4)" stroke-width="3"/>
   <line x1="5" y1="58" x2="255" y2="58" stroke="rgba(0,0,0,0.2)" stroke-width="2"/>
   <!-- 左端盖与安装耳环 -->
   <rect x="-16" y="-6" width="22" height="82" rx="4" fill="#546E7A" stroke="#37474F" stroke-width="2"/>
   <circle cx="-35" cy="35" r="16" fill="url(#metalH)" stroke="#546E7A" stroke-width="2"/>
   <circle cx="-35" cy="35" r="8" fill="#ECEFF1" stroke="#9E9E9E"/>

   <!-- 右端盖与导向套 -->
   <rect x="254" y="-6" width="26" height="82" rx="4" fill="#546E7A" stroke="#37474F" stroke-width="2"/>
   <rect x="280" y="10" width="14" height="50" rx="2" fill="#78909C" stroke="#455A64" stroke-width="2"/>
   
   <!-- A/B 口管接座 -->
   <rect x="0" y="-12" width="16" height="12" rx="2" fill="#78909C" stroke="#455A64" stroke-width="2"/>
   <text x="8" y="-15" text-anchor="middle" font-family="Arial" font-size="12" fill="#1565C0" font-weight="bold">A</text>
   <rect x="220" y="-12" width="16" height="12" rx="2" fill="#78909C" stroke="#455A64" stroke-width="2"/>
   <text x="228" y="-15" text-anchor="middle" font-family="Arial" font-size="12" fill="#1565C0" font-weight="bold">B</text>
   
   <text x="130" y="40" text-anchor="middle" font-family="Arial" font-size="14" fill="#37474F" font-weight="bold">CYLINDER D63/d35</text>

   <!-- 活塞与活塞杆 (动态组) -->
   <!-- 初始态: offset=0 极限=120 -->
   <g id="pistonGroup" transform="translate(0, 0)">
    <!-- 杆 -->
    <rect x="120" y="21" width="180" height="28" fill="url(#rodGrad)" stroke="#BDBDBD" stroke-width="1.5"/>
    <line x1="120" y1="26" x2="300" y2="26" stroke="rgba(255,255,255,0.7)" stroke-width="2"/>
    <!-- 内部活塞块表示(半透明透过缸壁) -->
    <rect x="110" y="6" width="10" height="58" rx="2" fill="#2E3030" opacity="0.6"/>
    <!-- 杆端耳环(带动支撑臂) -->
    <circle cx="300" cy="35" r="16" fill="url(#metalH)" stroke="#757575" stroke-width="2"/>
    <circle cx="300" cy="35" r="8" fill="#ECEFF1" stroke="#9E9E9E"/>
   </g>
  </g>

  <!-- 行程状态板 -->
  <rect x="1060" y="340" width="300" height="40" rx="6" fill="#E3F2FD" stroke="#64B5F6" stroke-width="1" filter="url(#shSm)"/>
  <text x="1080" y="365" font-family="Arial" font-size="14" fill="#1565C0" font-weight="bold">行 程:</text>
  <text id="strokeTxt" x="1330" y="365" text-anchor="end" font-family="monospace" font-size="18" fill="#0D47A1" font-weight="bold">0 %</text>
  <rect x="1080" y="385" width="250" height="8" rx="4" fill="#CFD8DC"/>
  <rect id="strokeBar" x="1080" y="385" width="0" height="8" rx="4" fill="#2196F3"/>

  <!-- === 8. 支撑臂 === -->
  <!-- 左枢轴 cx=1380 cy=275 ; 杆端枢轴位于piston.x+300. 当stroke=0, cx=1380. (距离0)
       这里为了演示，枢轴设置得符合动画联动
       支撑臂固定旋转点 cx=1280, cy=275
       stroke=0 时，旋转0度.
  -->
  <g id="armGroup" transform="rotate(0, 1280, 275)">
   <!-- 工字钢臂主体 -->
   <line x1="1280" y1="275" x2="1480" y2="120" stroke="#5D4037" stroke-width="28" stroke-linecap="round" filter="url(#shadow)"/>
   <line x1="1280" y1="275" x2="1480" y2="120" stroke="#8D6E63" stroke-width="18" stroke-linecap="round"/>
   <line x1="1280" y1="275" x2="1480" y2="120" stroke="#795548" stroke-width="6" stroke-linecap="round"/>
   <!-- 末端负载点 -->
   <circle cx="1480" cy="120" r="12" fill="#A1887F" stroke="#5D4037" stroke-width="3"/>
   <circle cx="1280" cy="275" r="12" fill="#5D4037" stroke="#3E2723" stroke-width="3"/>
   <circle cx="1280" cy="275" r="5" fill="#A1887F"/>
   <text x="1440" y="105" text-anchor="middle" font-family="SimHei,Arial" font-size="16" fill="#4E342E" font-weight="bold">负 载</text>
  </g>
  <!-- 支撑臂基座 -->
  <rect x="1255" y="287" width="50" height="15" rx="4" fill="#4E342E" stroke="#3E2723" stroke-width="2"/>
  <rect x="1240" y="302" width="80" height="12" rx="4" fill="#795548" stroke="#5D4037" stroke-width="2"/>

  <!-- === 9. 底部控制面板 === -->
  <rect x="50" y="650" width="1500" height="280" rx="10" fill="#FFFFFF" stroke="#B0BEC5" stroke-width="2" filter="url(#shadow)"/>
  <rect x="50" y="650" width="1500" height="40" rx="10" fill="#37474F"/>
  <rect x="50" y="680" width="1500" height="10" fill="#37474F"/>
  <text x="800" y="678" text-anchor="middle" font-family="Arial" font-size="18" fill="#ECEFF1" font-weight="bold">控制台面板</text>

  <!-- 动作说明 -->
  <rect x="70" y="705" width="600" height="100" rx="6" fill="#F5F5F5" stroke="#E0E0E0"/>
  <text x="85" y="725" font-family="Arial" font-size="13" fill="#333" font-weight="bold">动作逻辑:</text>
  <text x="85" y="745" font-family="Arial" font-size="12" fill="#666">升起: 电磁铁A得电 → 左位接入 → 压力油进无杆腔 → 液压缸伸出 → 支撑臂上升</text>
  <text x="85" y="765" font-family="Arial" font-size="12" fill="#666">降落: 电磁铁B得电 → 右位接入 → 压力油进有杆腔 → 液压缸缩回 → 支撑臂下降</text>
  <text x="85" y="785" font-family="Arial" font-size="12" fill="#666">停止: 双电磁铁失电 → 弹簧回中位 → 四口全封持压锁定 → 系统待机</text>

  <!-- 操作按钮 -->
  <g id="btnUp" cursor="pointer" transform="translate(690, 705)">
   <rect x="0" y="0" width="230" height="60" rx="12" fill="#2E7D32" stroke="#1B5E20" stroke-width="2" filter="url(#shadow)"/>
   <rect id="btnUpHov" x="4" y="4" width="222" height="20" rx="8" fill="rgba(255,255,255,0.15)"/>
   <text x="115" y="38" text-anchor="middle" font-family="SimHei,Arial" font-size="28" fill="#FFF" font-weight="bold" pointer-events="none">升 起</text>
  </g>

  <g id="btnDown" cursor="pointer" transform="translate(940, 705)">
   <rect x="0" y="0" width="230" height="60" rx="12" fill="#C62828" stroke="#B71C1C" stroke-width="2" filter="url(#shadow)"/>
   <rect id="btnDownHov" x="4" y="4" width="222" height="20" rx="8" fill="rgba(255,255,255,0.15)"/>
   <text x="115" y="38" text-anchor="middle" font-family="SimHei,Arial" font-size="28" fill="#FFF" font-weight="bold" pointer-events="none">降 落</text>
  </g>

  <g id="btnStop" cursor="pointer" transform="translate(1190, 705)">
   <rect x="0" y="0" width="230" height="60" rx="12" fill="#616161" stroke="#424242" stroke-width="2" filter="url(#shadow)"/>
   <rect id="btnStopHov" x="4" y="4" width="222" height="20" rx="8" fill="rgba(255,255,255,0.15)"/>
   <text x="115" y="38" text-anchor="middle" font-family="SimHei,Arial" font-size="28" fill="#FFF" font-weight="bold" pointer-events="none">停 止</text>
  </g>

  <!-- 系统运行状态综合栏 -->
  <rect x="70" y="820" width="1350" height="90" rx="8" fill="#ECEFF1" stroke="#CFD8DC" stroke-width="2"/>
  <text x="90" y="850" font-family="Arial" font-size="14" fill="#333" font-weight="bold">系统监控值:</text>
  
  <text x="210" y="850" font-family="Arial" font-size="13" fill="#666">电机/泵:</text>
  <text id="ssPump" x="280" y="850" font-family="monospace" font-size="14" fill="#4CAF50" font-weight="bold">停止</text>
  
  <text x="360" y="850" font-family="Arial" font-size="13" fill="#666">换向阀向:</text>
  <text id="ssValve" x="430" y="850" font-family="monospace" font-size="14" fill="#616161" font-weight="bold">中位</text>
  
  <text x="510" y="850" font-family="Arial" font-size="13" fill="#666">主油路压力:</text>
  <text id="ssPress" x="590" y="850" font-family="monospace" font-size="14" fill="#C62828" font-weight="bold">0.0 MPa</text>
  
  <text x="700" y="850" font-family="Arial" font-size="13" fill="#666">液压缸行程:</text>
  <text id="ssStroke" x="780" y="850" font-family="monospace" font-size="14" fill="#0D47A1" font-weight="bold">0 %</text>
  
  <text x="860" y="850" font-family="Arial" font-size="13" fill="#666">流量 Q:</text>
  <text id="ssFlow" x="910" y="850" font-family="monospace" font-size="14" fill="#1565C0" font-weight="bold">0.0 L/min</text>

  <text x="90" y="885" font-family="Arial" font-size="14" fill="#333" font-weight="bold">当前状态码:</text>
  <text id="ssAction" x="210" y="885" font-family="monospace" font-size="15" fill="#424242" font-weight="bold">[00] 系统待机</text>

  <!-- 指示灯组 -->
  <g transform="translate(1050, 840)">
   <circle id="ledRun" cx="0" cy="0" r="10" fill="#BDBDBD" stroke="#9E9E9E" stroke-width="2"/>
   <text x="20" y="5" font-family="Arial" font-size="13" fill="#555">运行</text>
   
   <circle id="ledUp" cx="80" cy="0" r="10" fill="#BDBDBD" stroke="#9E9E9E" stroke-width="2"/>
   <text x="100" y="5" font-family="Arial" font-size="13" fill="#555">升起</text>
   
   <circle id="ledDn" cx="160" cy="0" r="10" fill="#BDBDBD" stroke="#9E9E9E" stroke-width="2"/>
   <text x="180" y="5" font-family="Arial" font-size="13" fill="#555">降落</text>
   
   <circle id="ledErr" cx="240" cy="0" r="10" fill="#BDBDBD" stroke="#9E9E9E" stroke-width="2"/>
   <text x="260" y="5" font-family="Arial" font-size="13" fill="#555">故障</text>
  </g>
 </g>

 <!-- ================================================================ -->
 <!-- JavaScript 交互动画与逻辑 -->
 <script type="text/ecmascript"><![CDATA[
  var state = 'stop';
  var stroke = 0; // 行程 0-100%
  var animTimer = null;
  var waveTimer = null;
  var svgDoc = null;

  function init() {
   svgDoc = document.documentElement;
   var btnUp = document.getElementById('btnUp');
   var btnDown = document.getElementById('btnDown');
   var btnStop = document.getElementById('btnStop');
   if(btnUp) btnUp.addEventListener('click', function(){ doAction('up'); });
   if(btnDown) btnDown.addEventListener('click', function(){ doAction('down'); });
   if(btnStop) btnStop.addEventListener('click', function(){ doAction('stop'); });
   
   // Hover effects
   bindHover('btnUp', 'btnUpHov');
   bindHover('btnDown', 'btnDownHov');
   bindHover('btnStop', 'btnStopHov');
  }

  function bindHover(gId, hovId) {
   var g = document.getElementById(gId);
   var h = document.getElementById(hovId);
   if(g && h) {
    g.addEventListener('mouseover', function(){ h.setAttribute('fill', 'rgba(255,255,255,0.3)'); });
    g.addEventListener('mouseout', function(){ h.setAttribute('fill', 'rgba(255,255,255,0.15)'); });
   }
  }

  function getEl(id) { return document.getElementById(id); }

  function setEl(id, attr, val) {
   var el = getEl(id);
   if(el) el.setAttribute(attr, val);
  }

  function setText(id, text) {
   var el = getEl(id);
   if(el) el.textContent = text;
  }

  function setAnimState(id, mode) {
   var el = getEl(id);
   if(!el) return;
   var opacity = (mode === 'stop') ? '0' : '0.8';
   el.setAttribute('opacity', opacity);
   if (mode === 'up') {
       if(id === 'flowP' || id === 'flowD' || id === 'flowS' || id === 'flowAv' || id === 'flowAh') el.setAttribute('stroke', '#E3F2FD');
       if(id === 'flowT' || id === 'flowRV' || id === 'flowDVt' || id === 'flowBh') el.setAttribute('stroke', '#FFF3E0');
   } else if (mode === 'down') {
       if(id === 'flowP' || id === 'flowD' || id === 'flowS' || id === 'flowBh') el.setAttribute('stroke', '#E3F2FD');
       if(id === 'flowT' || id === 'flowRV' || id === 'flowDVt' || id === 'flowAv' || id === 'flowAh') el.setAttribute('stroke', '#FFF3E0');
   }
  }

  function doAction(act) {
   if(state === act) return;
   state = act;
   if(animTimer) { clearInterval(animTimer); animTimer = null; }

   var flows = ['flowP','flowT','flowS','flowD','flowRV','flowDVt','flowAv','flowAh','flowBh'];

   if(act === 'up') {
    // 阀门切换左位
    setEl('posLeft', 'fill', '#444'); setEl('posLeft', 'stroke', '#4CAF50'); setEl('posLeft', 'stroke-width', '2');
    setEl('posCenter', 'fill', '#333'); setEl('posCenter', 'stroke', 'none'); 
    setEl('posRight', 'fill', '#333'); setEl('posRight', 'stroke', 'none');
    setEl('posLeftTxt', 'opacity', '1'); setEl('posCenterTxt', 'opacity', '0.3'); setEl('posRightTxt', 'opacity', '0.3');
    
    // 管路颜色
    setEl('pipeAv', 'fill', '#42A5F5'); setEl('pipeAh', 'fill', '#42A5F5'); setEl('pipeAd', 'fill', '#42A5F5');
    setEl('pipeBv', 'fill', '#FFA726'); setEl('pipeBh', 'fill', '#FFA726'); setEl('pipeBd', 'fill', '#FFA726');

    // 流动动画开启
    for(var i=0;i<flows.length;i++) setAnimState(flows[i], 'up');
    setEl('oilWave', 'opacity', '0.8');

    // 电磁铁A亮
    setEl('ledA', 'fill', '#4CAF50'); setEl('ledA', 'opacity', '1');
    setEl('ledB', 'fill', '#4CAF50'); setEl('ledB', 'opacity', '0.2');

    // 其他状态
    setEl('motorLED', 'fill', '#4CAF50');
    setText('motorTxt', 'RUN');
    updateStatus('[01] 升起运行中', '运行', '左位', 15.0, 25.5);
    setLeds('up');

    animTimer = setInterval(function(){
     if(stroke < 100){ stroke += 1.5; updateOutputs(); }
     else { clearInterval(animTimer); animTimer = null; doAction('stop'); }
    }, 50);

   } else if(act === 'down') {
    setEl('posRight', 'fill', '#444'); setEl('posRight', 'stroke', '#4CAF50'); setEl('posRight', 'stroke-width', '2');
    setEl('posCenter', 'fill', '#333'); setEl('posCenter', 'stroke', 'none'); 
    setEl('posLeft', 'fill', '#333'); setEl('posLeft', 'stroke', 'none');
    setEl('posRightTxt', 'opacity', '1'); setEl('posCenterTxt', 'opacity', '0.3'); setEl('posLeftTxt', 'opacity', '0.3');

    setEl('pipeAv', 'fill', '#FFA726'); setEl('pipeAh', 'fill', '#FFA726'); setEl('pipeAd', 'fill', '#FFA726');
    setEl('pipeBv', 'fill', '#42A5F5'); setEl('pipeBh', 'fill', '#42A5F5'); setEl('pipeBd', 'fill', '#42A5F5');

    for(var i=0;i<flows.length;i++) setAnimState(flows[i], 'down');
    setEl('oilWave', 'opacity', '0.8');

    setEl('ledB', 'fill', '#4CAF50'); setEl('ledB', 'opacity', '1');
    setEl('ledA', 'fill', '#4CAF50'); setEl('ledA', 'opacity', '0.2');

    setEl('motorLED', 'fill', '#4CAF50');
    setText('motorTxt', 'RUN');
    updateStatus('[02] 降落运行中', '运行', '右位', 12.0, 32.0);
    setLeds('down');

    animTimer = setInterval(function(){
     if(stroke > 0){ stroke -= 1.5; updateOutputs(); }
     else { clearInterval(animTimer); animTimer = null; doAction('stop'); }
    }, 50);

   } else {
    // Stop
    setEl('posCenter', 'fill', '#444'); setEl('posCenter', 'stroke', '#4CAF50'); setEl('posCenter', 'stroke-width', '2');
    setEl('posLeft', 'fill', '#333'); setEl('posLeft', 'stroke', 'none'); 
    setEl('posRight', 'fill', '#333'); setEl('posRight', 'stroke', 'none');
    setEl('posCenterTxt', 'opacity', '1'); setEl('posLeftTxt', 'opacity', '0.3'); setEl('posRightTxt', 'opacity', '0.3');

    setEl('pipeAv', 'fill', '#B0BEC5'); setEl('pipeAh', 'fill', '#B0BEC5'); setEl('pipeAd', 'fill', '#B0BEC5');
    setEl('pipeBv', 'fill', '#B0BEC5'); setEl('pipeBh', 'fill', '#B0BEC5'); setEl('pipeBd', 'fill', '#B0BEC5');

    for(var i=0;i<flows.length;i++) setAnimState(flows[i], 'stop');
    setEl('oilWave', 'opacity', '0');

    setEl('ledA', 'opacity', '0.2');
    setEl('ledB', 'opacity', '0.2');
    
    setEl('motorLED', 'fill', '#9E9E9E');
    setText('motorTxt', 'STOP');
    updateStatus('[00] 系统待机锁定', '停止', '中位', 0.0, 0.0);
    setLeds('stop');
   }
  }

  function updateOutputs() {
   // 缸行程 (120到300 是180宽. svg里偏移等比计算)
   var offset = stroke * 1.8; 
   var pg = getEl('pistonGroup');
   if(pg) {
    pg.setAttribute('transform', 'translate(' + offset + ', 0)');
   }

   // 支撑臂旋转 (-25 度 max. 1280, 275 是支点)
   var angle = -stroke * 0.25;
   var ag = getEl('armGroup');
   if(ag) {
    ag.setAttribute('transform', 'rotate(' + angle + ', 1280, 275)');
   }

   // 进度条
   setText('strokeTxt', stroke.toFixed(1) + ' %');
   setText('ssStroke', stroke.toFixed(1) + ' %');
   setEl('strokeBar', 'width', (stroke * 2.5)); // 250宽 -> *2.5

   // 液位降低模拟 (油被吸走) 
   // 正常 82% 随行程改变.  61px高度是满(100%), 偏移
   var oilH = 61 - (stroke * 0.08); // 最大降低8px
   var yOffset = 45 + (stroke * 0.08);
   setEl('oilLevel', 'height', oilH);
   setEl('oilLevel', 'y', yOffset);
  }

  function updateStatus(action, pumpSt, valveSt, press, flow) {
   setText('ssAction', action);
   setText('ssPump', pumpSt);
   setText('ssValve', valveSt);
   setText('ssPress', press.toFixed(1) + ' MPa');
   setText('ssFlow', flow.toFixed(1) + ' L/min');
   setText('gaugePressTxt', press.toFixed(1) + ' MPa');

   // 指针旋转: -40度 是 0 MPa, 140度 是 30MPa. 范围180度. (press/30)*180
   var gnd = getEl('gaugeNeedleLRotate');
   if(gnd) {
    var ang = -40 + (press / 30) * 180;
    gnd.setAttribute('transform', 'rotate(' + ang + ', 30, 40)');
   }
  }

  function setLeds(mode) {
   var cRun = getEl('ledRun'), cUp = getEl('ledUp'), cDn = getEl('ledDn');
   if(mode === 'up') {
    cRun.setAttribute('fill', '#4CAF50'); cUp.setAttribute('fill', '#4CAF50'); cDn.setAttribute('fill', '#BDBDBD');
   } else if (mode === 'down') {
    cRun.setAttribute('fill', '#4CAF50'); cUp.setAttribute('fill', '#BDBDBD'); cDn.setAttribute('fill', '#C62828');
   } else {
    cRun.setAttribute('fill', '#BDBDBD'); cUp.setAttribute('fill', '#BDBDBD'); cDn.setAttribute('fill', '#BDBDBD');
   }
  }

  if(document.readyState === 'loading') {
   document.addEventListener('DOMContentLoaded', init);
  } else {
   setTimeout(init, 200);
  }
 ]]></script>
</svg>'''


# 获取并更新项目
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
        project['hmi']['views'][i]['profile']['width'] = 1600
        project['hmi']['views'][i]['profile']['height'] = 950
        project['hmi']['views'][i]['profile']['bkcolor'] = '#E8EAED'
        print(f'更新视图 SVG: {len(svg)} chars')
        found = True
        break

if not found:
    new_view = {
        'id': 'v_hydraulic_arm_01',
        'name': '液压支撑臂真实控制',
        'profile': {
            'width': 1600,
            'height': 950,
            'bkcolor': '#E8EAED'
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
try:
    resp = urllib.request.urlopen(req, timeout=30)
    print(f'项目更新: HTTP {resp.status}')
except Exception as e:
    print(f"推送 FUXA 失败: {e}")
    exit(1)

# 验证
time.sleep(1)
req = urllib.request.Request(f'{BASE_URL}/api/project')
resp = urllib.request.urlopen(req, timeout=10)
data = json.loads(resp.read().decode())
for v in data.get('hmi', {}).get('views', []):
    if v.get('id') == 'v_hydraulic_arm_01':
        s = v.get('svgcontent', '')
        print(f'SVG 长度: {len(s)} chars')
        checks = ['btnUp', 'btnDown', 'btnStop', 'metalH', 'oilFill', 'solenoid', 'pistonGroup', 'doAction', 'strokeBase']
        
        ok = sum(1 for kw in checks if kw in s)
        print(f'通过检查点 {ok}/{len(checks)}')
        break

print('完成! 请刷新浏览器 http://localhost:1881 查看效果')
