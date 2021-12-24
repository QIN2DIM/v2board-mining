# v2board-mining

<span id="v2board-classify"></span>

## v2board Pattern

### 无阻碍（Normal）

> Definition：邮箱（无论是否限定域名 无需验证），密码，重述密码，邀请码（选填），点击注册

- [河豚](https://hetun.online/#/register) 3H 20GB
- [话啦啦](https://v2ssy.xyz/#/dashboard) not free
- [跨越长城](https://direct.gfwservice.xyz/#/dashboard) 2D 5GB
- [萌喵加速-Nirvana](https://portal.meomiao.xyz/#/dashboard) 1D 2GB
- [云上极速](https://yunshang.uk//#/dashboard) 1D 1GB

### 邮箱验证（Diy）

> Definition：自定义邮箱（需要验证），发送验证码，填写验证码，密码，重述密码，邀请码（选填），勾选服务条款，点击注册

- [SNOW](https://www.onsnow.net/#/dashboard) 1D 1GB
- [玛瑙云](https://manaocloud.xyz/#/register) 3D 2GB
- [TIGR](https://tigr.icu/s/#/register) 3D 10GB

### 邮箱验证（Limit）

> Definition：区别仅在限定了邮箱域名（仍需验证）。

- [VNStark-薇恩](https://vnstark.com/#/register)
- [sp-ss](https://dash.sp333.top/#/register) 永久 10G 下单
- [企鹅小屋](https://pengui.cloud/index.php#/dashboard) 1D 30GB 
- [麦当当](https://www.mdd.one/#/dashboard) 2D 10GB
- [爱探索](https://lovfree.com/#/dashboard) 1D 66GB 
- [Xstars](https://xstars.top/#/dashboard) 1D 5GB 
- [ExLink](https://dash.exl.ink/#/dashboard) 1D 5GB 
- [纵横加速](https://www.rerongtuliao.com/#/dashboard) 7D 2TB 
- [nanoPort](https://v3.nanoport.xyz/#/dashboard) 1D 5GB 
- [Zachary](https://zachary.pub/#/dashboard) 31D 1GB 
- [八·云 网络](https://bayun.me/#/dashboard) 1D 1GB 
- [遨游.pw](https://aoyou.pw/#/dashboard) 30D 5GB 

### 高级验证（Attention）

> Definition：点击发送邮箱验证码以及注册按钮后，弹出 Google reCAPTCHA

- [PandaCloud](https://www.xxm.buzz/#/register) 2H 3GB
  
  

## v2board Actions

### 实例注册，订阅缓存，订阅辐射

1. 实例注册
   沿用 selenium 设计方案，实现注册行为链。
2. 订阅缓存
   沿用 redis 设计方案，实现订阅缓存。
   Format：clash url-scheme
3. 订阅辐射
   沿用 redis 设计方案，实现订阅辐射。

### 实例发现，实例标注，实例筛选

1. 实例发现
   参照 [v2board-classify](#v2board-classify) 区分广义对象实例。
   - [√] 使用搜索引擎搜索 HTML/JavaScript 站源代码（暂行）
   - [×] 使用 Google 关联搜索（不可靠）
   - [×] 搜集 BBS 共享（过时风险，不可信）
   - [√] 搜集/监听 Channel 共享（可靠，需过滤）
     - 品云测速
     - 毒药测速

2. 实例标注
3. 实例筛选

### 订阅分发

沿用 easygui 设计方案，实现订阅分发（Clash 联动）。

- 用户点击「一键导入 Clash」，触发 「redis 原子取」指令，获取「Clash Url-Scheme」
- 使用默认浏览器访问「Clash Url-Scheme」实现 Clash-Yaml 的自动导入
