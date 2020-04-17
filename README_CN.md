# 中国传统色
> 梅子金黄杏子肥，麦花雪白菜花稀。
  <right><br>——范成大 ·《四时田园杂兴·其二》</right>
## 预览
- [Traditional-Chinese-Colors | 中国传统色](https://colors.masantu.com/)
- 源码：[imoyao/Traditional-Chinese-Colors](https://github.com/imoyao/Traditional-Chinese-Colors)
## 说明
前端参考了[nippon-color:PWA build with vue-cli 3](https://github.com/ssshooter/nippon-color)，后端使用Python对各种采集的数据进行了风格统一。

## PWA
<!-- https://www.flaticon.com/packs/japan-21 -->
<div>Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>        

[Background image from pixiv](https://www.pixiv.net/member_illust.php?mode=medium&illust_id=64253519)

### v1.0.0 
v1.0.0 release :tada:

:sparkles: Add random color button

:lipstick: Design adjustment 

:zap: Compress background image

:bug: Scroll to top while color sort is changed

## TODO
- favor color
- how to use pwa
- better scroll experience
- hover & active
- optimise font color base on background color manually
- optimise sort of color manually

## 安装
### 前端
```
npm install
```
### 出现错误

```
npm rebuild node-sass
```
### 开发热重载
```
npm run serve
```

### 生产
```
npm run build
```
出现文字乱码执行`CHCP 65001`

### 部署
~~run deploy.sh~~
现在我们直接把其导出到docs目录，github支持部署docs目录为项目文档。  
参见[Simpler GitHub Pages publishing - The GitHub Blog](https://github.blog/2016-08-17-simpler-github-pages-publishing/)

### 代码Lint
```
npm run lint
```
### TODO
- [ ] cmky数据返回为列表，而代码中使用的是字符串；
- [ ] 添加cmky环；
- [ ] 添加颜色描述，没有的时候使用API显示古诗（？）
- [ ] 将原页面修改为日本色页面；

### 问题定位
1. **必须**执行npm install安装依赖包；
2. 如果run或者build出错，请检查vue版本或者是否正常安装；否则，删除node_modules重装；

### 更改日志
还没有呢~~[wiki](https://github.com/ssshooter/nippon-color/wiki/Changelog)~~

