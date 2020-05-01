<template>
  <base-page
    :color-list="colorList"
    :color-selected="colorSelected"
    :self-router="selfRouter"
    :land-show="landShow">
    <div class="lip-select">
      <el-cascader
        v-model="selectedOptions"
        :options="lipData"
        :props="{ expandTrigger: 'hover' }"
        class="select-brand"
        @change="handleChange"/>
    </div>
    <div class="lip-img">
      <div
        v-for="fit in fits"
        :key="fit"
        class="block">
        <el-image
          :src="url"
          :fit="fit"
          :preview-src-list="srcList"/>
      </div>

    </div>
  </base-page>

</template>

<script>
import BasePage from './BasePage'
import colorData from '@/data/lipsticks.json'
export default {
  name: 'Lipsticks',
  components: {
    BasePage,
  },
  data () {
    return {
      // for 循环写进base
      landShow: {
        title: '不问色号',
        desc: '小山重迭金明灭，鬓云欲度香腮雪。懒起画蛾眉，弄妆梳洗迟。\n' + '照花前后镜，花面交相映。新帖绣罗襦，双双金鹧鸪。',
        eng: 'six colors six life',
      },
      colorList: [],
      colorData: colorData,
      selfRouter: '/lipsticks',
      colorSelected: {
        is_bright: true,
      },
      isCopied: false,
      lastEls: null,
      isColorDisabled: false,
      selectedOptions: [],
      lipData: [],
      selectedLipstrik: [],
      colorSet: new Set(),
      fits: ['cover'],
      url: '//img4.xiji.com/images/19/01/6efcdf3646ab405e003d3feefa2d463ac20b9d3a.jpg',
      srcList: [
        '//ci.xiaohongshu.com/26cd24f8-1440-5c74-a82a-fcbee522bade?imageView2/2/w/1080/format/jpg',
        '//ci.xiaohongshu.com/7d62a4a7-2006-4aeb-a3f7-050f6152e1f5@r_1280w_1280h.jpg',
      ],
    }
  },
  created () {
    this.lipData = this.formatTree(colorData.brands)
  },
  methods: {
    // 先对取到的数据进行一个递归转化
    formatTree (treeData) {
      let result = []
      treeData.forEach((item) => {
        if (item.hasOwnProperty('id')) {
          this.colorSet.add(item)
        }
        let value = item.letter
        let label = item.name
        let children = item.series || item.lipsticks
        let lipsticks = item.lipsticks
        if (children && children.length > 0) {
          children = this.formatTree(children)
        }
        if (children && children.length > 0) {
          result.push({
            value, label, children,
          })
        }
        if (children && children.length === 0) {
          result.push({
            value, label, lipsticks,
          })
        }
      })
      this.colorList = Array.from(this.colorSet)
      return result
    },
    // see also:[elementUI Cascader 级联选择器获取数据信息_JavaScript_Dreamer_xr的博客-CSDN博客](https://blog.csdn.net/xr510002594/article/details/86245903)
    selectBrandSeries (val, opt) {
      // see also:[VUE.JS 使用axios数据请求时数据绑定时 报错 TypeError: Cannot set property 'xxxx' of undefined 的解决办法 - 254980080 - 博客园](https://www.cnblogs.com/qq254980080/p/10441848.html)
      let that = this
      return val.map(function (value, index, array) {
        let selectColors
        if (opt) {
          for (let item of opt) {
            if (item.value === value) {
              if (item.hasOwnProperty('lipsticks')) {
                // let selectColors = item.lipsticks // 选择品牌下面的一个系列
                that.colorList = item.lipsticks
              }
              opt = item.children
              return opt
            }
          }
        }
        return selectColors
      })
    },
    handleChange (value) {
      this.selectBrandSeries(value, this.lipData)
    },
  },
}
</script>

<style lang="scss" scoped>
@import '@/mixin.scss';
/*https://www.helloweba.net/javascript/295.html*/
.select-brand{
  width: 20px;
}
.base .display .select-brand {
    position: absolute;
    height: 1.2rem;
    right: 6.2rem;
}
.lip-select/deep/.el-input.el-input--suffix{
  bottom: .35rem;
  @include for-phone {
    bottom: .7rem;
  }
}
.lip-select/deep/.el-input{
  width:auto;
}
.lip-select/deep/.el-input__icon{
    margin-right: -3px;
}
.lip-select/deep/.el-input__inner{
  padding-right: 10px!important;
  height: 1.3rem;
  background-color: transparent!important;
}
</style>
