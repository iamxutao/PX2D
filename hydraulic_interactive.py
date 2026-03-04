#!/usr/bin/env python3
"""
交互式 ISO 1219 标准液压原理图
- 使用标准液压符号
- 点击升起/降落按钮后:
  - 换向阀位切换(高亮当前位)
  - 管路流向动画(蓝色压力油、橙色回油)
  - 液压缸活塞伸缩
  - 支撑臂角度联动
  - 状态面板实时更新
"""
import urllib.request, json

BASE_URL = 'http://localhost:1881'

svg = '''<svg width="1920" height="1080" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
 <defs>
  <marker id="arrB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
   <path d="M 0 0 L 10 5 L 0 10 z" fill="#1565C0"/>
  </marker>
  <marker id="arrO" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
   <path d="M 0 0 L 10 5 L 0 10 z" fill="#E65100"/>
  </marker>
 </defs>
 <g>
  <title>Layer 1</title>
  <rect id="svg_bg" fill="#FFFFFF" width="1920" height="1080"/>

  <!-- ========== 标题 ========== -->
  <text id="svg_title" x="700" y="32" text-anchor="middle" font-family="SimHei,Arial" font-size="22" fill="#1a237e" font-weight="bold">液压支撑臂系统原理图 (ISO 1219)</text>
  <line x1="50" y1="42" x2="1350" y2="42" stroke="#BDBDBD" stroke-width="1"/>

  <!-- =================================================================== -->
  <!--  布局: 左侧动力源(油箱+电机+泵) -> 中间控制(溢流阀+换向阀) -> 右侧执行(缸+臂) -->
  <!--  压力主管 y=200   回油主管 y=480                                      -->
  <!-- =================================================================== -->

  <!-- ========== 油箱 (ISO: 上开口梯形) x=130 y=490 ========== -->
  <line x1="90" y1="500" x2="170" y2="500" stroke="#333" stroke-width="2.5"/>
  <line x1="97" y1="500" x2="105" y2="530" stroke="#333" stroke-width="2.5"/>
  <line x1="105" y1="530" x2="155" y2="530" stroke="#333" stroke-width="2.5"/>
  <line x1="155" y1="530" x2="163" y2="500" stroke="#333" stroke-width="2.5"/>
  <text x="130" y="548" text-anchor="middle" font-family="SimHei,Arial" font-size="11" fill="#555">油箱 T</text>

  <!-- 油箱数据 -->
  <rect x="175" y="502" width="90" height="36" rx="3" fill="#FFF8E1" stroke="#FFB300" stroke-width="1"/>
  <text x="183" y="517" font-family="Arial" font-size="9" fill="#E65100">油温: 25.0C</text>
  <text x="183" y="531" font-family="Arial" font-size="9" fill="#E65100">液位: 85.0%</text>

  <!-- 吸油管 -->
  <line x1="130" y1="500" x2="130" y2="450" stroke="#1565C0" stroke-width="2.5"/>

  <!-- ========== 电动机 (ISO: 圆+M) x=130 y=420 ========== -->
  <circle cx="130" cy="420" r="22" fill="#E8EAF6" stroke="#333" stroke-width="2.5"/>
  <text x="130" y="426" text-anchor="middle" font-family="Arial" font-size="16" fill="#333" font-weight="bold">M</text>
  <text x="130" y="393" text-anchor="middle" font-family="SimHei,Arial" font-size="10" fill="#555">电动机</text>
  <!-- 电机状态 -->
  <rect id="motorStatus" x="157" y="408" width="70" height="22" rx="3" fill="#E8F5E9" stroke="#4CAF50" stroke-width="1"/>
  <text id="motorStatusTxt" x="192" y="423" text-anchor="middle" font-family="monospace" font-size="11" fill="#2E7D32" font-weight="bold">停止</text>

  <!-- 轴连接 -->
  <line x1="130" y1="398" x2="130" y2="352" stroke="#333" stroke-width="3"/>

  <!-- ========== 液压泵 (ISO: 圆+三角箭头) x=130 y=320 ========== -->
  <circle cx="130" cy="320" r="22" fill="#E8EAF6" stroke="#333" stroke-width="2.5"/>
  <polygon points="121,335 130,305 139,335" fill="#333"/>
  <text x="130" y="290" text-anchor="middle" font-family="SimHei,Arial" font-size="10" fill="#555">液压泵</text>

  <!-- 泵出口到压力主管 -->
  <line x1="130" y1="298" x2="130" y2="200" stroke="#1565C0" stroke-width="2.5"/>

  <!-- ========== 压力主管(水平 y=200) ========== -->
  <line id="pressMain" x1="130" y1="200" x2="650" y2="200" stroke="#1565C0" stroke-width="3"/>
  <!-- 流动指示(停止时不显示) -->
  <line id="flowP" x1="132" y1="200" x2="648" y2="200" stroke="#90CAF9" stroke-width="2" stroke-dasharray="12 8" opacity="0">
   <animate id="flowPanim" attributeName="stroke-dashoffset" from="0" to="-20" dur="0.6s" repeatCount="indefinite"/>
  </line>
  <text x="350" y="193" text-anchor="middle" font-family="Arial" font-size="9" fill="#1565C0" font-weight="bold">P (压力油路)</text>

  <!-- ========== 压力表 (ISO: 圆+指针) x=280 ========== -->
  <line x1="280" y1="200" x2="280" y2="170" stroke="#1565C0" stroke-width="2"/>
  <circle cx="280" cy="150" r="16" fill="#FFF" stroke="#333" stroke-width="2"/>
  <line id="gaugeNeedle" x1="280" y1="150" x2="271" y2="162" stroke="#D32F2F" stroke-width="1.5"/>
  <circle cx="280" cy="150" r="2.5" fill="#D32F2F"/>
  <text x="280" y="158" text-anchor="middle" font-family="Arial" font-size="6" fill="#999">MPa</text>
  <!-- 压力数值 -->
  <rect x="300" y="138" width="80" height="22" rx="3" fill="#FCE4EC" stroke="#E91E63" stroke-width="1"/>
  <text id="pressureVal" x="340" y="153" text-anchor="middle" font-family="monospace" font-size="13" fill="#C62828" font-weight="bold">0.0 MPa</text>

  <!-- ========== 溢流阀 (ISO: 方框+内部箭头+弹簧+调节) x=430 ========== -->
  <line x1="430" y1="200" x2="430" y2="230" stroke="#1565C0" stroke-width="2"/>
  <!-- 阀体方框 -->
  <rect x="413" y="230" width="34" height="40" fill="#FFF" stroke="#333" stroke-width="2.5"/>
  <!-- 内部箭头(向下) -->
  <line x1="430" y1="236" x2="430" y2="262" stroke="#333" stroke-width="1.5" marker-end="url(#arrO)"/>
  <!-- 弹簧(左侧) -->
  <polyline points="410,235 405,240 415,246 405,252 415,258 410,263" fill="none" stroke="#333" stroke-width="1.5"/>
  <!-- 调节箭头(右上) -->
  <line x1="450" y1="228" x2="462" y2="218" stroke="#333" stroke-width="1.5" marker-end="url(#arrB)"/>
  <!-- 阀出口到回油管 -->
  <line x1="430" y1="270" x2="430" y2="480" stroke="#E65100" stroke-width="2"/>
  <text x="430" y="290" text-anchor="middle" font-family="SimHei,Arial" font-size="10" fill="#555">溢流阀</text>

  <!-- ========== 回油主管(水平 y=480) ========== -->
  <line id="retMain" x1="130" y1="480" x2="750" y2="480" stroke="#E65100" stroke-width="2.5"/>
  <!-- 流动指示 -->
  <line id="flowR" x1="748" y1="480" x2="132" y2="480" stroke="#FFCC80" stroke-width="2" stroke-dasharray="12 8" opacity="0">
   <animate id="flowRanim" attributeName="stroke-dashoffset" from="0" to="-20" dur="0.6s" repeatCount="indefinite"/>
  </line>
  <!-- 回油到油箱 -->
  <line x1="130" y1="480" x2="130" y2="500" stroke="#E65100" stroke-width="2"/>
  <text x="450" y="497" text-anchor="middle" font-family="Arial" font-size="9" fill="#E65100" font-weight="bold">T (回油油路)</text>
  <!-- 回油箱符号(右端) -->
  <line x1="730" y1="480" x2="770" y2="480" stroke="#333" stroke-width="2.5"/>
  <line x1="735" y1="480" x2="740" y2="500" stroke="#333" stroke-width="2.5"/>
  <line x1="740" y1="500" x2="760" y2="500" stroke="#333" stroke-width="2.5"/>
  <line x1="760" y1="500" x2="765" y2="480" stroke="#333" stroke-width="2.5"/>

  <!-- ========== 三位四通电磁换向阀 (ISO标准: 3个方格+内部流道) ========== -->
  <!-- 位置: 中心 x=610 y=230~290 -->

  <!-- 三个位置方格(每格50x60) -->
  <!-- 左位 (P->A, B->T) 升起 -->
  <rect id="valveL" x="560" y="230" width="50" height="60" fill="#FFF" stroke="#333" stroke-width="2.5"/>
  <!-- 左位内部:交叉连接 P->A, B->T -->
  <line x1="573" y1="290" x2="587" y2="230" stroke="#333" stroke-width="1.5" marker-end="url(#arrB)"/>
  <line x1="587" y1="290" x2="573" y2="230" stroke="#333" stroke-width="1.5" marker-end="url(#arrB)"/>

  <!-- 中位 (全封闭 H型) -->
  <rect id="valveC" x="610" y="230" width="50" height="60" fill="#FFF" stroke="#333" stroke-width="2.5"/>
  <!-- 中位内部:H型封闭(4端口各封一小段) -->
  <line x1="623" y1="230" x2="623" y2="240" stroke="#333" stroke-width="1.5"/>
  <line x1="623" y1="240" x2="637" y2="240" stroke="#333" stroke-width="1.5"/>
  <line x1="637" y1="230" x2="637" y2="240" stroke="#333" stroke-width="1.5"/>
  <line x1="623" y1="290" x2="623" y2="280" stroke="#333" stroke-width="1.5"/>
  <line x1="623" y1="280" x2="637" y2="280" stroke="#333" stroke-width="1.5"/>
  <line x1="637" y1="290" x2="637" y2="280" stroke="#333" stroke-width="1.5"/>

  <!-- 右位 (P->B, A->T) 降落 -->
  <rect id="valveR" x="660" y="230" width="50" height="60" fill="#FFF" stroke="#333" stroke-width="2.5"/>
  <!-- 右位内部:平行连接 -->
  <line x1="673" y1="290" x2="673" y2="230" stroke="#333" stroke-width="1.5" marker-end="url(#arrB)"/>
  <line x1="697" y1="290" x2="697" y2="230" stroke="#333" stroke-width="1.5" marker-end="url(#arrB)"/>

  <!-- 高亮当前位(默认中位) -->
  <rect id="activeValve" x="610" y="230" width="50" height="60" fill="rgba(76,175,80,0.15)" stroke="#4CAF50" stroke-width="3" rx="2"/>

  <!-- 电磁铁 a (左侧) -->
  <rect x="535" y="242" width="25" height="36" fill="#FFF" stroke="#333" stroke-width="2"/>
  <line x1="548" y1="242" x2="560" y2="260" stroke="#333" stroke-width="1.5"/>
  <text x="548" y="273" text-anchor="middle" font-family="Arial" font-size="10" fill="#333" font-weight="bold">a</text>
  <!-- SOL-A 指示灯 -->
  <circle id="ledA" cx="548" cy="236" r="4" fill="#E0E0E0" stroke="#999" stroke-width="1"/>

  <!-- 电磁铁 b (右侧) -->
  <rect x="710" y="242" width="25" height="36" fill="#FFF" stroke="#333" stroke-width="2"/>
  <line x1="722" y1="278" x2="710" y2="260" stroke="#333" stroke-width="1.5"/>
  <text x="722" y="273" text-anchor="middle" font-family="Arial" font-size="10" fill="#333" font-weight="bold">b</text>
  <!-- SOL-B 指示灯 -->
  <circle id="ledB" cx="722" cy="236" r="4" fill="#E0E0E0" stroke="#999" stroke-width="1"/>

  <!-- 弹簧(左) -->
  <polyline points="560,250 556,254 564,258 556,262 560,266" fill="none" stroke="#333" stroke-width="1.2"/>
  <!-- 弹簧(右) -->
  <polyline points="710,250 714,254 706,258 714,262 710,266" fill="none" stroke="#333" stroke-width="1.2"/>

  <!-- 端口标注 P/T/A/B -->
  <text x="623" y="305" text-anchor="middle" font-family="Arial" font-size="10" fill="#1565C0" font-weight="bold">P</text>
  <text x="637" y="305" text-anchor="middle" font-family="Arial" font-size="10" fill="#E65100" font-weight="bold">T</text>
  <text x="623" y="224" text-anchor="middle" font-family="Arial" font-size="10" fill="#1565C0" font-weight="bold">A</text>
  <text x="637" y="224" text-anchor="middle" font-family="Arial" font-size="10" fill="#1565C0" font-weight="bold">B</text>

  <!-- P口连接到压力主管 -->
  <line x1="623" y1="290" x2="623" y2="310" stroke="#1565C0" stroke-width="2"/>
  <line x1="623" y1="310" x2="650" y2="310" stroke="#1565C0" stroke-width="2"/>
  <line x1="650" y1="200" x2="650" y2="310" stroke="#1565C0" stroke-width="2"/>
  <!-- T口连接到回油管 -->
  <line x1="637" y1="290" x2="637" y2="320" stroke="#E65100" stroke-width="2"/>
  <line x1="637" y1="320" x2="700" y2="320" stroke="#E65100" stroke-width="2"/>
  <line x1="700" y1="320" x2="700" y2="480" stroke="#E65100" stroke-width="2"/>

  <!-- A口管路: 向上拐到液压缸左端(无杆腔) -->
  <line id="pipeA1" x1="623" y1="230" x2="623" y2="140" stroke="#999" stroke-width="2.5"/>
  <line id="pipeA2" x1="623" y1="140" x2="920" y2="140" stroke="#999" stroke-width="2.5"/>
  <line id="pipeA3" x1="920" y1="140" x2="920" y2="195" stroke="#999" stroke-width="2.5"/>
  <!-- A管流动动画 -->
  <line id="flowA1" x1="623" y1="228" x2="623" y2="142" stroke="#90CAF9" stroke-width="2" stroke-dasharray="10 8" opacity="0">
   <animate attributeName="stroke-dashoffset" from="0" to="18" dur="0.5s" repeatCount="indefinite"/>
  </line>
  <line id="flowA2" x1="625" y1="140" x2="918" y2="140" stroke="#90CAF9" stroke-width="2" stroke-dasharray="10 8" opacity="0">
   <animate attributeName="stroke-dashoffset" from="0" to="-18" dur="0.5s" repeatCount="indefinite"/>
  </line>
  <line id="flowA3" x1="920" y1="142" x2="920" y2="193" stroke="#90CAF9" stroke-width="2" stroke-dasharray="10 8" opacity="0">
   <animate attributeName="stroke-dashoffset" from="0" to="-18" dur="0.5s" repeatCount="indefinite"/>
  </line>
  <text x="780" y="133" text-anchor="middle" font-family="Arial" font-size="9" fill="#1565C0">A口(无杆腔)</text>

  <!-- B口管路: 更高拐弯到液压缸右端(有杆腔) -->
  <line id="pipeB1" x1="637" y1="230" x2="637" y2="100" stroke="#999" stroke-width="2.5"/>
  <line id="pipeB2" x1="637" y1="100" x2="1080" y2="100" stroke="#999" stroke-width="2.5"/>
  <line id="pipeB3" x1="1080" y1="100" x2="1080" y2="195" stroke="#999" stroke-width="2.5"/>
  <!-- B管流动动画 -->
  <line id="flowB1" x1="637" y1="228" x2="637" y2="102" stroke="#90CAF9" stroke-width="2" stroke-dasharray="10 8" opacity="0">
   <animate attributeName="stroke-dashoffset" from="0" to="18" dur="0.5s" repeatCount="indefinite"/>
  </line>
  <line id="flowB2" x1="639" y1="100" x2="1078" y2="100" stroke="#90CAF9" stroke-width="2" stroke-dasharray="10 8" opacity="0">
   <animate attributeName="stroke-dashoffset" from="0" to="-18" dur="0.5s" repeatCount="indefinite"/>
  </line>
  <line id="flowB3" x1="1080" y1="102" x2="1080" y2="193" stroke="#90CAF9" stroke-width="2" stroke-dasharray="10 8" opacity="0">
   <animate attributeName="stroke-dashoffset" from="0" to="-18" dur="0.5s" repeatCount="indefinite"/>
  </line>
  <text x="870" y="93" text-anchor="middle" font-family="Arial" font-size="9" fill="#1565C0">B口(有杆腔)</text>

  <text x="635" y="218" text-anchor="middle" font-family="SimHei,Arial" font-size="10" fill="#333" font-weight="bold">三位四通电磁换向阀 (弹簧复位)</text>

  <!-- 阀位状态 -->
  <rect id="valveStatusBg" x="740" y="250" width="80" height="22" rx="3" fill="#E8F5E9" stroke="#4CAF50" stroke-width="1"/>
  <text id="valveStatusLbl" x="748" y="265" font-family="SimHei,Arial" font-size="9" fill="#2E7D32">阀位:</text>
  <text id="valveStatusVal" x="812" y="265" text-anchor="end" font-family="monospace" font-size="11" fill="#1B5E20" font-weight="bold">中位</text>

  <!-- ========== 液压缸 (ISO: 矩形+活塞+杆) ========== -->
  <!-- 缸筒外框 -->
  <rect id="cylBody" x="900" y="195" width="200" height="70" fill="#FFF" stroke="#333" stroke-width="2.5"/>
  <!-- 活塞(可移动) 初始位置 x=1000 -->
  <line id="piston" x1="1000" y1="195" x2="1000" y2="265" stroke="#333" stroke-width="4"/>
  <!-- 有杆腔端盖 -->
  <line x1="1075" y1="195" x2="1075" y2="265" stroke="#333" stroke-width="2.5"/>
  <!-- 活塞杆(可伸缩) -->
  <rect id="rod" x="1000" y="220" width="140" height="12" fill="#DDD" stroke="#333" stroke-width="1.5" rx="6"/>
  <!-- 杆端连接头 -->
  <circle id="rodEnd" cx="1140" cy="226" r="6" fill="#999" stroke="#333" stroke-width="2"/>

  <!-- 无杆腔填色(压力油) -->
  <rect id="chamberA" x="902" y="197" width="98" height="66" fill="rgba(21,101,192,0.08)" stroke="none"/>
  <!-- 有杆腔填色(压力油) -->
  <rect id="chamberB" x="1002" y="197" width="73" height="66" fill="rgba(21,101,192,0.05)" stroke="none"/>

  <text x="940" y="190" text-anchor="middle" font-family="SimHei,Arial" font-size="10" fill="#555">无杆腔</text>
  <text x="1040" y="190" text-anchor="middle" font-family="SimHei,Arial" font-size="10" fill="#555">有杆腔</text>
  <text x="1000" y="285" text-anchor="middle" font-family="SimHei,Arial" font-size="11" fill="#333" font-weight="bold">液压缸</text>

  <!-- 行程数据 -->
  <rect x="900" y="292" width="200" height="22" rx="3" fill="#E3F2FD" stroke="#64B5F6" stroke-width="1"/>
  <text x="908" y="307" font-family="SimHei,Arial" font-size="10" fill="#1565C0">行程:</text>
  <text id="strokeVal" x="1092" y="307" text-anchor="end" font-family="monospace" font-size="12" fill="#0D47A1" font-weight="bold">0 %</text>
  <!-- 行程条 -->
  <rect x="900" y="318" width="200" height="8" rx="4" fill="#E0E0E0"/>
  <rect id="strokeBar" x="900" y="318" width="0" height="8" rx="4" fill="#42A5F5"/>

  <!-- ========== 支撑臂 ========== -->
  <g id="armGroup" transform="rotate(0, 1146, 226)">
   <line id="arm" x1="1146" y1="226" x2="1280" y2="155" stroke="#795548" stroke-width="14" stroke-linecap="round"/>
   <line x1="1146" y1="226" x2="1280" y2="155" stroke="#8D6E63" stroke-width="8" stroke-linecap="round"/>
   <circle cx="1280" cy="155" r="5" fill="#A1887F" stroke="#5D4037" stroke-width="2"/>
   <text x="1260" y="145" font-family="SimHei,Arial" font-size="11" fill="#5D4037" font-weight="bold">支撑臂</text>
  </g>
  <!-- 铰接点 -->
  <circle cx="1146" cy="226" r="8" fill="#5D4037" stroke="#3E2723" stroke-width="2"/>
  <circle cx="1146" cy="226" r="3" fill="#A1887F"/>
  <!-- 基座 -->
  <rect x="1130" y="236" width="32" height="8" rx="2" fill="#5D4037"/>
  <rect x="1124" y="243" width="44" height="6" rx="2" fill="#8D6E63"/>

  <!-- ========== 图例 ========== -->
  <rect x="50" y="555" width="350" height="32" rx="4" fill="#FAFAFA" stroke="#E0E0E0"/>
  <text x="65" y="575" font-family="SimHei,Arial" font-size="10" fill="#555" font-weight="bold">图例:</text>
  <line x1="100" y1="571" x2="130" y2="571" stroke="#1565C0" stroke-width="3"/>
  <text x="135" y="575" font-family="SimHei,Arial" font-size="10" fill="#555">压力油路(P)</text>
  <line x1="210" y1="571" x2="240" y2="571" stroke="#E65100" stroke-width="3"/>
  <text x="245" y="575" font-family="SimHei,Arial" font-size="10" fill="#555">回油油路(T)</text>
  <line x1="320" y1="571" x2="350" y2="571" stroke="#999" stroke-width="2.5"/>
  <text x="355" y="575" font-family="SimHei,Arial" font-size="10" fill="#555">无流</text>

  <!-- ========== 控制面板 ========== -->
  <rect x="50" y="600" width="1300" height="230" rx="6" fill="#F5F5F5" stroke="#BDBDBD" stroke-width="1.5"/>
  <rect x="50" y="600" width="1300" height="32" rx="6" fill="#37474F"/>
  <rect x="50" y="626" width="1300" height="6" fill="#37474F"/>
  <text x="700" y="622" text-anchor="middle" font-family="SimHei,Arial" font-size="15" fill="#ECEFF1" font-weight="bold">操作控制面板</text>

  <!-- 原理说明 -->
  <text x="70" y="655" font-family="SimHei,Arial" font-size="12" fill="#333" font-weight="bold">工作原理:</text>
  <text x="70" y="675" font-family="SimHei,Arial" font-size="11" fill="#666">升起: 电磁铁a通电 -> 阀芯左移(左位) -> P口通A口 -> 压力油进无杆腔 -> 活塞伸出 -> 支撑臂上升</text>
  <text x="70" y="693" font-family="SimHei,Arial" font-size="11" fill="#666">降落: 电磁铁b通电 -> 阀芯右移(右位) -> P口通B口 -> 压力油进有杆腔 -> 活塞缩回 -> 支撑臂下降</text>
  <text x="70" y="711" font-family="SimHei,Arial" font-size="11" fill="#666">停止: 双弹簧复位 -> 阀芯回中位 -> 四口全封 -> 液压锁 -> 支撑臂保持</text>

  <!-- 升起按钮 -->
  <rect id="btnUp" x="800" y="645" width="200" height="55" rx="10" fill="#2E7D32" stroke="#1B5E20" stroke-width="2" cursor="pointer"/>
  <text id="btnUpTxt" x="900" y="680" text-anchor="middle" font-family="SimHei,Arial" font-size="24" fill="white" font-weight="bold" pointer-events="none">升 起</text>

  <!-- 降落按钮 -->
  <rect id="btnDown" x="1050" y="645" width="200" height="55" rx="10" fill="#C62828" stroke="#B71C1C" stroke-width="2" cursor="pointer"/>
  <text id="btnDownTxt" x="1150" y="680" text-anchor="middle" font-family="SimHei,Arial" font-size="24" fill="white" font-weight="bold" pointer-events="none">降 落</text>

  <!-- 停止按钮 -->
  <rect id="btnStop" x="800" y="710" width="450" height="40" rx="8" fill="#757575" stroke="#616161" stroke-width="2" cursor="pointer"/>
  <text id="btnStopTxt" x="1025" y="737" text-anchor="middle" font-family="SimHei,Arial" font-size="18" fill="white" font-weight="bold" pointer-events="none">停 止 (复位中位)</text>

  <!-- 系统综合状态 -->
  <rect x="70" y="762" width="660" height="55" rx="5" fill="#ECEFF1" stroke="#CFD8DC"/>
  <text x="85" y="782" font-family="SimHei,Arial" font-size="12" fill="#333" font-weight="bold">系统状态</text>
  <text x="165" y="782" font-family="SimHei,Arial" font-size="11" fill="#666">液压泵:</text>
  <text id="ssPump" x="220" y="782" font-family="monospace" font-size="12" fill="#2E7D32" font-weight="bold">停止</text>
  <text x="290" y="782" font-family="SimHei,Arial" font-size="11" fill="#666">换向阀:</text>
  <text id="ssValve" x="350" y="782" font-family="monospace" font-size="12" fill="#2E7D32" font-weight="bold">中位</text>
  <text x="420" y="782" font-family="SimHei,Arial" font-size="11" fill="#666">系统压力:</text>
  <text id="ssPress" x="500" y="782" font-family="monospace" font-size="12" fill="#C62828" font-weight="bold">0.0 MPa</text>
  <text x="580" y="782" font-family="SimHei,Arial" font-size="11" fill="#666">行程:</text>
  <text id="ssStroke" x="625" y="782" font-family="monospace" font-size="12" fill="#0D47A1" font-weight="bold">0%</text>
  <!-- 动作 -->
  <text x="85" y="805" font-family="SimHei,Arial" font-size="11" fill="#666">当前动作:</text>
  <text id="ssAction" x="165" y="805" font-family="monospace" font-size="12" fill="#757575" font-weight="bold">待机 - 系统停止</text>

  <!-- 状态指示灯 -->
  <rect x="740" y="762" width="280" height="55" rx="5" fill="#ECEFF1" stroke="#CFD8DC"/>
  <text x="755" y="782" font-family="SimHei,Arial" font-size="11" fill="#333" font-weight="bold">状态灯</text>
  <circle id="ledRun" cx="825" cy="778" r="8" fill="#E0E0E0" stroke="#BDBDBD" stroke-width="1.5"/>
  <text x="838" y="782" font-family="SimHei,Arial" font-size="10" fill="#555">运行</text>
  <circle id="ledUp" cx="885" cy="778" r="8" fill="#E0E0E0" stroke="#BDBDBD" stroke-width="1.5"/>
  <text x="898" y="782" font-family="SimHei,Arial" font-size="10" fill="#555">升起</text>
  <circle id="ledDn" cx="945" cy="778" r="8" fill="#E0E0E0" stroke="#BDBDBD" stroke-width="1.5"/>
  <text x="958" y="782" font-family="SimHei,Arial" font-size="10" fill="#555">降落</text>
  <circle id="ledStby" cx="1005" cy="778" r="8" fill="#FFC107" stroke="#F9A825" stroke-width="1.5"/>
  <text x="1018" y="782" font-family="SimHei,Arial" font-size="10" fill="#555">待机</text>
 </g>

 <script type="text/ecmascript"><![CDATA[
  var state = 'stop'; // stop, up, down
  var stroke = 0;     // 0-100
  var animTimer = null;
  var svgDoc = null;

  function init() {
   svgDoc = document.documentElement;
   var btnUp = svgDoc.getElementById('btnUp');
   var btnDown = svgDoc.getElementById('btnDown');
   var btnStop = svgDoc.getElementById('btnStop');
   if(btnUp) btnUp.addEventListener('click', function(){ doAction('up'); });
   if(btnDown) btnDown.addEventListener('click', function(){ doAction('down'); });
   if(btnStop) btnStop.addEventListener('click', function(){ doAction('stop'); });
  }

  function getEl(id){ return document.getElementById(id); }

  function doAction(act) {
   if(state === act) return;
   state = act;
   if(animTimer) { clearInterval(animTimer); animTimer = null; }

   if(act === 'up') {
    setValvePos('left');
    setMotor(true);
    setFlowUp();
    setSolenoids('a');
    animTimer = setInterval(function(){
     if(stroke < 100){ stroke += 2; updateCylinder(); }
     else { clearInterval(animTimer); animTimer = null; }
    }, 80);
    updateStatus('升起中', '运行', 15.0);
    setLeds('up');
   } else if(act === 'down') {
    setValvePos('right');
    setMotor(true);
    setFlowDown();
    setSolenoids('b');
    animTimer = setInterval(function(){
     if(stroke > 0){ stroke -= 2; updateCylinder(); }
     else { clearInterval(animTimer); animTimer = null; }
    }, 80);
    updateStatus('降落中', '运行', 12.0);
    setLeds('down');
   } else {
    setValvePos('center');
    setMotor(false);
    setFlowStop();
    setSolenoids('none');
    updateStatus('待机 - 系统停止', '停止', 0);
    setLeds('stop');
   }
  }

  function setValvePos(pos) {
   var av = getEl('activeValve');
   if(!av) return;
   if(pos === 'left')  { av.setAttribute('x','560'); }
   else if(pos === 'right') { av.setAttribute('x','660'); }
   else { av.setAttribute('x','610'); }
   var vt = getEl('valveStatusVal');
   if(vt) vt.textContent = pos==='left'?'左位(升)': pos==='right'?'右位(降)':'中位';
  }

  function setMotor(on) {
   var mt = getEl('motorStatusTxt');
   var mb = getEl('motorStatus');
   if(mt) mt.textContent = on ? '运行' : '停止';
   if(mb) { mb.setAttribute('fill', on?'#E8F5E9':'#ECEFF1'); mb.setAttribute('stroke', on?'#4CAF50':'#BDBDBD'); }
  }

  function setSolenoids(which) {
   var la = getEl('ledA');
   var lb = getEl('ledB');
   if(la) { la.setAttribute('fill', which==='a'?'#F44336':'#E0E0E0'); la.setAttribute('stroke', which==='a'?'#D32F2F':'#999'); }
   if(lb) { lb.setAttribute('fill', which==='b'?'#F44336':'#E0E0E0'); lb.setAttribute('stroke', which==='b'?'#D32F2F':'#999'); }
  }

  function setFlowUp() {
   // P主管流动
   setFlowLine('flowP', 1, '#90CAF9');
   setFlowLine('flowR', 1, '#FFCC80');
   // A管: 压力油(P->A) 蓝色
   setFlowLine('flowA1', 1, '#42A5F5');
   setFlowLine('flowA2', 1, '#42A5F5');
   setFlowLine('flowA3', 1, '#42A5F5');
   // B管: 回油(B->T) 橙色
   setFlowLine('flowB1', 1, '#FFB74D');
   setFlowLine('flowB2', 1, '#FFB74D');
   setFlowLine('flowB3', 1, '#FFB74D');
   // A管路变蓝(压力油)
   setPipeColor('pipeA1', '#1565C0');
   setPipeColor('pipeA2', '#1565C0');
   setPipeColor('pipeA3', '#1565C0');
   // B管路变橙(回油)
   setPipeColor('pipeB1', '#E65100');
   setPipeColor('pipeB2', '#E65100');
   setPipeColor('pipeB3', '#E65100');
   // 无杆腔充油
   var ca = getEl('chamberA');
   if(ca) ca.setAttribute('fill','rgba(21,101,192,0.2)');
   var cb = getEl('chamberB');
   if(cb) cb.setAttribute('fill','rgba(230,81,0,0.1)');
  }

  function setFlowDown() {
   setFlowLine('flowP', 1, '#90CAF9');
   setFlowLine('flowR', 1, '#FFCC80');
   // B管: 压力油(P->B) 蓝色
   setFlowLine('flowB1', 1, '#42A5F5');
   setFlowLine('flowB2', 1, '#42A5F5');
   setFlowLine('flowB3', 1, '#42A5F5');
   // A管: 回油(A->T) 橙色
   setFlowLine('flowA1', 1, '#FFB74D');
   setFlowLine('flowA2', 1, '#FFB74D');
   setFlowLine('flowA3', 1, '#FFB74D');
   // B管路变蓝
   setPipeColor('pipeB1', '#1565C0');
   setPipeColor('pipeB2', '#1565C0');
   setPipeColor('pipeB3', '#1565C0');
   // A管路变橙
   setPipeColor('pipeA1', '#E65100');
   setPipeColor('pipeA2', '#E65100');
   setPipeColor('pipeA3', '#E65100');
   var ca = getEl('chamberA');
   if(ca) ca.setAttribute('fill','rgba(230,81,0,0.1)');
   var cb = getEl('chamberB');
   if(cb) cb.setAttribute('fill','rgba(21,101,192,0.2)');
  }

  function setFlowStop() {
   var ids = ['flowP','flowR','flowA1','flowA2','flowA3','flowB1','flowB2','flowB3'];
   for(var i=0;i<ids.length;i++){ setFlowLine(ids[i], 0, null); }
   setPipeColor('pipeA1', '#999');
   setPipeColor('pipeA2', '#999');
   setPipeColor('pipeA3', '#999');
   setPipeColor('pipeB1', '#999');
   setPipeColor('pipeB2', '#999');
   setPipeColor('pipeB3', '#999');
   var ca = getEl('chamberA');
   if(ca) ca.setAttribute('fill','rgba(21,101,192,0.08)');
   var cb = getEl('chamberB');
   if(cb) cb.setAttribute('fill','rgba(21,101,192,0.05)');
  }

  function setFlowLine(id, opacity, color) {
   var el = getEl(id);
   if(!el) return;
   el.setAttribute('opacity', opacity);
   if(color) el.setAttribute('stroke', color);
  }

  function setPipeColor(id, color) {
   var el = getEl(id);
   if(el) el.setAttribute('stroke', color);
  }

  function updateCylinder() {
   var pistonX = 950 + stroke * 0.5;  // 950 ~ 1000
   var rodW = 90 + stroke * 0.5;      // 90 ~ 140
   var p = getEl('piston');
   var r = getEl('rod');
   var re = getEl('rodEnd');
   var cA = getEl('chamberA');
   if(p) { p.setAttribute('x1', pistonX); p.setAttribute('x2', pistonX); }
   if(r) { r.setAttribute('x', pistonX); r.setAttribute('width', rodW); }
   if(re) { re.setAttribute('cx', pistonX + rodW); }
   if(cA) { cA.setAttribute('width', pistonX - 902); }

   // 支撑臂角度: stroke 0->100 对应 0 -> -25度
   var angle = -stroke * 0.25;
   var ag = getEl('armGroup');
   if(ag) ag.setAttribute('transform', 'rotate('+angle+', 1146, 226)');

   // 更新行程数值
   var sv = getEl('strokeVal');
   if(sv) sv.textContent = stroke + ' %';
   var sb = getEl('strokeBar');
   if(sb) sb.setAttribute('width', stroke * 2);
   var ss = getEl('ssStroke');
   if(ss) ss.textContent = stroke + '%';
  }

  function updateStatus(action, pumpState, pressure) {
   var sa = getEl('ssAction');
   if(sa) sa.textContent = action;
   var sp = getEl('ssPump');
   if(sp) sp.textContent = pumpState;
   var sv = getEl('ssValve');
   if(sv) sv.textContent = state==='up'?'左位':state==='down'?'右位':'中位';
   var pp = getEl('ssPress');
   if(pp) pp.textContent = pressure.toFixed(1) + ' MPa';
   var pv = getEl('pressureVal');
   if(pv) pv.textContent = pressure.toFixed(1) + ' MPa';
   // 压力表指针角度
   var gn = getEl('gaugeNeedle');
   if(gn) {
    var angle = -45 + (pressure / 25) * 90;
    var rad = angle * Math.PI / 180;
    var nx = 280 + 14 * Math.cos(rad + Math.PI);
    var ny = 150 + 14 * Math.sin(rad + Math.PI);
    gn.setAttribute('x2', nx);
    gn.setAttribute('y2', ny);
   }
  }

  function setLeds(mode) {
   var run = getEl('ledRun');
   var up = getEl('ledUp');
   var dn = getEl('ledDn');
   var stby = getEl('ledStby');
   // reset all
   if(run) { run.setAttribute('fill','#E0E0E0'); run.setAttribute('stroke','#BDBDBD'); }
   if(up) { up.setAttribute('fill','#E0E0E0'); up.setAttribute('stroke','#BDBDBD'); }
   if(dn) { dn.setAttribute('fill','#E0E0E0'); dn.setAttribute('stroke','#BDBDBD'); }
   if(stby) { stby.setAttribute('fill','#E0E0E0'); stby.setAttribute('stroke','#BDBDBD'); }
   if(mode === 'up') {
    if(run) { run.setAttribute('fill','#4CAF50'); run.setAttribute('stroke','#388E3C'); }
    if(up) { up.setAttribute('fill','#4CAF50'); up.setAttribute('stroke','#388E3C'); }
   } else if(mode === 'down') {
    if(run) { run.setAttribute('fill','#4CAF50'); run.setAttribute('stroke','#388E3C'); }
    if(dn) { dn.setAttribute('fill','#F44336'); dn.setAttribute('stroke','#D32F2F'); }
   } else {
    if(stby) { stby.setAttribute('fill','#FFC107'); stby.setAttribute('stroke','#F9A825'); }
   }
  }

  // 初始化
  if(document.readyState === 'loading') {
   document.addEventListener('DOMContentLoaded', init);
  } else {
   setTimeout(init, 200);
  }
 ]]></script>
</svg>'''

# 获取并更新项目
req = urllib.request.Request(f'{BASE_URL}/api/project')
resp = urllib.request.urlopen(req, timeout=10)
project = json.loads(resp.read().decode())

found = False
for i, v in enumerate(project['hmi']['views']):
    if v['id'] == 'v_hydraulic_arm_01':
        project['hmi']['views'][i]['svgcontent'] = svg
        project['hmi']['views'][i]['profile']['width'] = 1920
        project['hmi']['views'][i]['profile']['height'] = 1080
        project['hmi']['views'][i]['profile']['bkcolor'] = '#FFFFFF'
        print(f'更新视图 SVG: {len(svg)} chars')
        found = True
        break

if not found:
    new_view = {
        'id': 'v_hydraulic_arm_01',
        'name': '液压支撑臂',
        'profile': {'width': 1920, 'height': 1080, 'bkcolor': '#FFFFFF'},
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
        checks = ['script', 'doAction', 'activeValve', 'flowA1', 'piston', 'armGroup',
                  'btnUp', 'btnDown', 'btnStop', 'stroke-dasharray', 'animate']
        for kw in checks:
            print(f'  {kw}: {"Yes" if kw in s else "No"}')
        break

print('完成! 请刷新浏览器 http://localhost:1881 查看交互效果')
print('点击 升起/降落/停止 按钮观察:')
print('  - 阀位高亮框移动')
print('  - 管路颜色和流向变化')
print('  - 液压缸活塞伸缩')
print('  - 支撑臂角度变化')
print('  - 状态面板实时更新')
