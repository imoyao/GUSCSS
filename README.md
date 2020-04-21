# 中国传统色
> 梅子金黄杏子肥，麦花雪白菜花稀。
  <right><br>——范成大 ·《四时田园杂兴·其二》</right>

这是一个基于 Vue2 和 Python3 写的展示中国传统色的单页面静态网页。
## 预览
- [Traditional-Chinese-Colors | 中国传统色](https://colors.masantu.com/)
- 源码：[imoyao/Traditional-Chinese-Colors](https://github.com/imoyao/Traditional-Chinese-Colors)
## 说明
本项目主要用于 Python 代码的练习，同时对 Vue2 更加深入地了解。实现一个**伪**前后端分离的小项目。前端参考了[nippon-color:PWA build with vue-cli 3](https://github.com/ssshooter/nippon-color)，后端使用 Python 对各种采集的数据进行了风格统一。

## PWA
<!-- https://www.flaticon.com/packs/japan-21 -->
<div>Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>        

[Background image from pixiv](https://www.pixiv.net/member_illust.php?mode=medium&illust_id=64253519)

## 更新日志
#### V1.0.0
1. 使用 Python 解析所有获取到的数据
2. 色系和亮度全部自动识别（待改进）

## 安装
### 版本信息

#### Python
```plain
python --version
Python 3.7.3
```
#### Vue
```plain
G:\Traditional-Chinese-Colors>vue --version
2.9.6
```
### 前端

#### 安装依赖
```shell
npm install
```
#### 开发模式（热重载）
```shell
npm run serve
```

#### 生产模式
```shell
npm run build
```
如果提示找不到命令`ERROR  Error: The system cannot find the path specified.`，执行：
```
npm install -g @vue/cli-service
```
报错，如果出现文字乱码执行`CHCP 65001`，然后截图发上来大家一起看看。

### 后端（伪）

#### 安装依赖
```shell
pip install pipenv
pipenv shell
pipenv install
cd backend
python main.py
cd ..
```

### 部署
~~执行 run deploy.sh ~~

现在我们直接把其导出到 docs 目录，github 支持部署 docs 目录为项目文档。  
参见[Simpler GitHub Pages publishing - The GitHub Blog](https://github.blog/2016-08-17-simpler-github-pages-publishing/)

### 代码 Lint
```shell
npm run lint
```
### BUG
- [ ] 颜色描述返回的字典中很多desc都为空，导致只能加载每日诗词
- [x] 线上访问由于使用自定义字体导致访问很慢（使用CDN之后好多了）。
    将Vue和router改为线上使用CDN之后chunk-vendors大幅度减小
### TODO
#### 高优先级
- [ ] 接受数据修订（色系、亮色/暗色、颜色描述）
- [x] 数据返回时按照色系分组返回
- [ ] 添加日本色页面；
- [ ] 添加口红页面；
- [ ] 点击弹框页面（参照[此处](https://colors.ichuantong.cn/)关于实现）；
#### 次优先级
- [ ] favorite 颜色本地记录
- [ ] 卡顿改进（有吗？😐）
- [ ] hover & active 视觉改进
- [ ] 添加关于页面（解析 readme 为 about），参考[Creating a Simple Blog using Vue with Markdown - DEV Community 👩‍💻👨‍💻](https://dev.to/vycoder/creating-a-simple-blog-using-vue-with-markdown-2omd)
#### 已完成
- [x] 使用 Python 解析各种数据并返回给 Vue；
- [x] cmky 数据返回为列表，而代码中使用的是字符串；
- [x] 添加 cmky 环；
- [x] 添加颜色描述，没有的时候使用 API 显示古诗。（基于[今日诗词](https://www.jinrishici.com/doc/)）
- [x] 使用自定义字体；参考[此处](https://blog.csdn.net/lanseguhui/article/details/94629601)
- [x] 直接保存到目的（data）目录，不用手动复制数据；
- [x] 前端加载太慢（CDN）；
    参考[Github+jsDelivr搭建自己的免费cdn](https://blog.csdn.net/cungudafa/article/details/104274949)

### 贡献/帮助我

### 我是开发人员
你可以 fork 此仓库之后修改[amend 文件](_data/amend.json) 中的 data 字段，修改是以 id 为准，只提交修改新值，不修改值直接不写。之后提交 pr 即可。当然，也欢迎提交代码逻辑及实现中不合理的地方及 bug 修复。
```json
{
  "id": "1847572",
  "name": "朱砂",
  "tra_name": "硃砂",
  "color_series": "red",
  "pinyin": "zhū shā",
  "font_color": "dark",
  "is_bright": true,
  "rgb": [
    184,
    75,
    72
  ],
  "hex": "#B84B48",
  "cmyk": [
    0,
    59,
    61,
    28
  ],
  "desc": "",
  "figure": ""
}
```

### 我是普通用户
如果你不会写代码，但是有 github 账号，可以 [去 issue](https://github.com/imoyao/Traditional-Chinese-Colors/issues) 提交反馈；如果你没有账号或者不会使用 Github，可以直接发邮件[给我](mailto:immoyao@gmail.com)，邮箱地址：immoyao@gmail.com。

### 我除了钱啥都没
请使用微信（WeChat）扫描下方二维码与我一起做**公益**吧！  
![腾讯公益](https://www.masantu.com/img/PublicWelfare-for-Children.jpg)
当然还可以去我的博客找赞赏码给我打钱。（慢慢找去吧）😊

### 故障排查
1. **必须**执行 npm install 安装依赖包；
2. 如果 run 或者 build 出错，请检查 vue 版本或者是否正常安装；否则，删除 node_modules 重装 node 环境；
3. `× Error: pngquant failed to build, make sure that libpng-dev is installed`  
针对win10，以管理员身份执行`npm install -g windows-build-tools`
参见：[Error: pngquant failed to build, make sure that libpng-dev is installed_运维_logocool的专栏-CSDN博客](https://blog.csdn.net/logocool/article/details/104653530)


### 更改日志
还没有呢~

