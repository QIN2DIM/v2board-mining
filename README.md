# v2board-mining

<span id="v2board-classify"></span>
## v2board 站点搜集

### 无阻碍（normal）

> Definition：邮箱（无论是否限定域名 无需验证），密码，重述密码，邀请码（选填），点击注册

- [河豚](https://hetun.online/#/register) 3小时 20G
- [话啦啦-网络加速优质服务商](https://v2ssy.xyz/#/dashboard) 无免费节点
- [跨越长城](https://direct.gfwservice.xyz/#/dashboard) 2day 5G 
- [萌喵加速-Nirvana](https://portal.meomiao.xyz/#/dashboard) 1day 2G
- [云上极速](https://yunshang.uk//#/dashboard) 1day 1G

### 邮箱验证（diy）

> Definition：自定义邮箱（需要验证），发送验证码，填写验证码，密码，重述密码，邀请码（选填），勾选服务条款，点击注册
- [SNOW](https://www.onsnow.net/#/dashboard) 1G 每16日重置

### 邮箱验证（limit）

> Definition：区别仅在限定了邮箱域名（仍需验证）。

- [VNStark-薇恩](https://vnstark.com/#/register)
- [sp-ss](https://dash.sp333.top/#/register) 永久 10G 下单
- [企鹅小屋](https://pengui.cloud/index.php#/dashboard) 1day 30G gmail
- [麦当当](https://www.mdd.one/#/dashboard) 2day 10G gmail
- [爱探索](https://lovfree.com/#/dashboard) 1day 66G gmail
- [Xstars](https://xstars.top/#/dashboard) 1day 5G gmail
- [ExLink](https://dash.exl.ink/#/dashboard) 1day 5G gmail tos
- [纵横加速](https://www.rerongtuliao.com/#/dashboard) 7day 2T gmail 
- [nanoPort](https://v3.nanoport.xyz/#/dashboard) 1day 5G gmail
- [Zachary](https://zachary.pub/#/dashboard) 31day 1g gmail
- [八·云 网络](https://bayun.me/#/dashboard) 1day 1G gmail
- [遨游.pw](https://aoyou.pw/#/dashboard) 30day 5G gmail

### 高级验证（Attention）

> Definition：额外捆绑其他人机验证方案，如 GeeTest滑动验证，Google RECAPTCHA
> 点击发送验证码/注册，弹出人机验证

- [PandaCloud！ (xxm.buzz)](https://www.xxm.buzz/#/register)
  点击发送邮箱验证码后，弹出 Google RECAPTCHA

## v2board-action 定义

**方法论1：**实例注册，订阅缓存，订阅辐射
**方法论2：**实例发现，实例标注，实例筛选
**方法论3：**订阅分发（Clash 联动）

### 方法论1

1. 实例注册
    沿用 selenium 设计方案，实现注册行为链。
2. 订阅缓存
    沿用 redis 设计方案，实现订阅缓存。
    Format：clash url-scheme
3. 订阅辐射
    沿用 redis 设计方案，实现订阅辐射。

### 方法论2

1. 实例发现
    参照 [v2board-classify](#v2board-classify) 区分广义对象实例。
    - [√] 使用搜索引擎搜索 HTML/JavaScript 站源代码（暂行）
    - [×] 使用 Google 关联搜索（不可靠）
    - [×] 搜集 BBS 共享（过时风险，不可信）
    - [√] 搜集/监听 Channel 共享（可靠，需过滤）
      - 品云测速
      - 毒药测速

2. 实例标注
3. 实力筛选

### 方法论3

沿用 easygui 设计方案，实现订阅分发。

- 用户点击「一键导入 Clash」，触发 「redis 原子取」指令，获取「Clash Url-Scheme」
- 使用默认浏览器访问「Clash Url-Scheme」实现 Clash-Yaml 的自动导入


