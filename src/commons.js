// 提取公用方法到 common [vue--提取公共方法 - 帅到要去报警 - 博客园](https://www.cnblogs.com/e0yu/p/9844842.html)
const jinrishici = require('jinrishici')

export default{
  retrieveColorAndSelect: function (colorId, colorList) {
    let colorSelected
    if (colorId) {
      colorSelected = colorList.find(val => val.id === colorId)
    } else {
      colorSelected = {
        hex: '#ffffff',
        is_bright: true,
      }
    }
    return colorSelected
  },
  loadSentence: function () {
    jinrishici.load(result => {
      this.msg = result.data.content
      this.loadSentSuccess = true
      // eslint-disable-next-line handle-callback-err
    }, err => {
    })
    return { 'msg': this.msg, 'success': this.loadSentSuccess }
  },
  getColorList (colorData) {
    let realColorData = colorData.data
    let colorLists = []
    // TODO:大数组赋值性能问题，导致选择所有颜色时会卡顿
    let allColorSeries = []
    for (let [key, value] of Object.entries(realColorData)) {
      allColorSeries.push({ color: key, hex: value.hex })
      const copyArr = Object.assign([], value.colors)
      Array.prototype.push.apply(colorLists, copyArr)
    }
    this.colorSeries = Array.from(new Set(allColorSeries))
    return { 'colorLists': colorLists, 'series': this.colorSeries }
  },
  // 切换颜色分组
  changeColorSeries (color, colorData) {
    document.querySelector('.tab-wrapper').scrollTop = 0
    if (color === 'all') this.colorList = this.getColorList(colorData).colorLists
    else this.colorList = colorData.data[color].colors
    return {
      'cl': this.colorList,
      'cSelected': this.colorList[0], // TODO: 随机取
    }
  },
}
