<template>
  <base-page
    ref="basePage"
    :color-list="colorList"
    :color-selected="colorSelected"
    :self-router="selfRouter"
    :land-show="landShow">
    <div>
      <ColorSeriesPicker
        :color-series="colorSeries"
        :is-bright="colorSelected.is_bright"
        class="series"
        @colorChange="changeColorSeries" />
    </div>

  </base-page>
</template>

<script>
import BasePage from './BasePage'
import ColorSeriesPicker from '@/components/ColorSeriesPicker.vue'
import colorData from '@/data/zhColors.json'

export default {
  name: 'Home',
  components: {
    BasePage,
    ColorSeriesPicker,
  },
  data () {
    return {
      landShow: {
        title: '中国传统色',
        desc: '梅子金黄杏子肥，麦花雪白菜花稀。',
        eng: 'The Traditional Colors of China',
      },
      colorList: [],
      colorData: colorData,
      colorSelected: {
        is_bright: true,
      },
      selfRouter: '/',
      isCopied: false,
      lastEls: null,
      colorSeries: [],
      isColorDisabled: false,
      loadSentSuccess: false,
    }
  },
  created () {
    this.colorList = this.getColorList(colorData)
  },
  methods: {
    // 从父组件调用
    changeColorSeries (color) {
      let obj = this.common.changeColorSeries(color, colorData)
      this.colorList = obj.cl
      this.colorSelected = obj.cSelected
    },
    getColorList () {
      let colorObj = this.common.getColorList(this.colorData)
      this.colorSeries = colorObj.series
      return colorObj.colorLists
    },
    retrieveColorAndSelect (colorId) {
      this.colorSelected = this.common.retrieveColorAndSelect(colorId, this.colorList)
    },
  },
}
</script>
