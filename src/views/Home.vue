<template>
  <base-page
    ref="basePage"
    :color-list="colorList"
    :color-selected="colorSelected"
    :self-router="selfRouter"
    :land-show="landShow"
    @selectColor="retrieveColorAndSelect($event)">
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
      // provide: {
      //   send: 'hello',
      // },
      lastEls: null,
      colorSeries: [],
      isColorDisabled: false,
      loadSentSuccess: false,
    }
  },
  mounted () {
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
      // console.log(this.colorList, '------11----')
      // if (this.colorList.length === 0) { // 从子组件传过来list为空
      //   this.colorList = this.getColorList(colorData)
      // }
      this.colorSelected = this.common.retrieveColorAndSelect(colorId, this.colorList)
      // console.log(this.colorSelected, '--do it--------')
      // eslint-disable-next-line handle-callback-err
      // this.$refs.basePage.changeColor(this.colorSelected)
    },
  },
}
</script>
