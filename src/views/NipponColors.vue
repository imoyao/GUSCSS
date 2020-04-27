<template>
  <base-page
    :color-list="colorList"
    :color-selected="colorSelected"
    :self-router="selfRouter"
    :land-show="landShow"
    @selectColor="retrieveColorAndSelect">
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
import colorData from '@/data/nipponColors.json'

export default {
  name: 'NipponColors',
  components: {
    BasePage,
    ColorSeriesPicker,
  },
  data () {
    return {
      landShow: {
        title: '日本の伝統色',
        desc: '我庭の小草萌えいでぬ限りなき天地今やよみがへるらし.',
        eng: 'The Traditional Colors of Japan',
      },
      colorList: [],
      selfRouter: '/nippon',
      colorData: colorData,
      colorSelected: {
        is_bright: true,
      },
      isCopied: false,
      lastEls: null,
      colorSeries: [],
      isColorDisabled: false,
      loadSentSuccess: false,
    }
  },
  mounted () {
    this.colorList = this.getColorList(colorData)
    this.retrieveColorAndSelect(this.$route.query.colorId) // 刷新时根据路由初始化颜色
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
      console.log('do this in parent------')
      this.colorSelected = this.common.retrieveColorAndSelect(colorId, this.colorList)
    },
  },
}
</script>
