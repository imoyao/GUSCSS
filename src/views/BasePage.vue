<template>
  <div class="base">
    <div
      :style="`background-color:${colorSelected.hex};`"
      :class="{'color-bright':!colorSelected.is_bright}"
      class="display">
      <!-- 添加到喜爱颜色 -->
      <!-- 随机 -->
      <CopyButton
        :is-bright="colorSelected.is_bright"
        :copied="isCopied"
        class="copy"
        @click.native="copy(colorSelected.hex)" />
      <RandomButton
        :is-bright="colorSelected.is_bright"
        class="random"
        @click.native="random" />

      <slot> 此处插入切换色系内容 </slot>

      <div class="kanji">
        {{ bigTitle() }}
      </div>
      <div class="romaji">
        {{ colorSelected.pinyin||landShow.eng }}
      </div>
      <div class="color-decs">
        {{ colorDesc() }}
      </div>
      <div class="color-rgb-progress">
        <e-progress
          v-for="(rgb,index) in colorSelected.rgb"
          :key="index"
          :is-bright="colorSelected.is_bright"
          :text-inside="true"
          :stroke-width="12"
          :format="formatPercent"
          :color="RGBList[index]"
          :percentage="rgbPercent(`${rgb}`)"/>
      </div>
      <div
        v-if="colorSelected.cmyk"
        class="cmyk-number">
        <e-progress
          v-for="(cmykVal,index) in colorSelected.cmyk"
          :is-bright="colorSelected.is_bright"
          :key="index"
          :width="50"
          :format="formatCMYKPercent"
          :color="cymkList[index]"
          :class="cymkStr[index]"
          :percentage="parseInt(`${cmykVal}`)"
          class="n"
          type="circle"/>
      </div>
      <ColorFooter
        :href="selfRouter"
        :is-bright="colorSelected.is_bright"/>
    </div>
    <div class="tab-wrapper">
      <div class="tab">
        <ColorTab
          v-for="color in colorList"
          :key="color.id"
          :kanji="color.name"
          :hex="color.hex"
          :disabled="isColorDisabled"
          class="js-tab-item tab-item"
          @click.native="changeColor(color)" />
      </div>
    </div>
  </div>
</template>

<script>
import anime from 'animejs'
import ColorTab from '@/components/ColorTab.vue'
import ShareButton from '@/components/ShareButton.vue'
import CopyButton from '@/components/CopyButton.vue'
import RandomButton from '@/components/RandomButton.vue'
import ColorFooter from '@/components/ColorFooter.vue'
import EProgress from '@/plugins/Progress.vue'
import {
  checkInSight,
  checkInSightInit,
  throttle,
  clipboardCopy,
} from '@/util.js'

export default {
  name: 'BasePage',
  components: {
    ColorTab,
    ShareButton,
    CopyButton,
    RandomButton,
    ColorFooter,
    EProgress,
  },
  props: {
    landShow: {
      type: Object,
      default: () => {},
    },
    selfRouter: {
      type: String,
      default: '',
    },
    copied: {
      type: Boolean,
      default: false,
    },
    colorList: {
      type: Array,
      default: () => [],
    },
  },
  data () {
    return {
      msg: String,
      colorSelected: {
        is_bright: true,
        tra_name: '',
      },
      isCopied: false,
      lastEls: null,
      cymkList: [
        '#00FFFF',
        '#800080',
        '#FFFF00',
        '#000000',
      ],
      cymkStr: ['c', 'y', 'm', 'k'],
      RGBList: [
        '#ff4949',
        '#13ce66',
        '#20a0ff',
      ],
      isColorDisabled: false,
      loadSentSuccess: false,
    }
  },
  watch: {
    colorList () {
      this.$nextTick(() => {
        checkInSightInit(this.listAnime)()
      })
    },
    colorSelected () {
      this.$nextTick(() => {
        this.displayAnime()
      })
    },
    $route (r) {
      this.retrieveColorAndSelect(r.query.colorId)
    },
  },
  mounted () {
    // trigger watch colorList
    // route to specific color
    this.retrieveColorAndSelect(this.$route.query.colorId)
    document
      .querySelector('.tab-wrapper')
      .addEventListener('scroll', throttle(checkInSight(this.listAnime)))
    window.addEventListener('pageshow', throttle(checkInSight(this.listAnime)))
    window.addEventListener('click', throttle(checkInSight(this.listAnime), 1000)) // 页面跳转（不太友好）
    window.addEventListener(
      'resize',
      throttle(checkInSight(this.listAnime), 1000)
    )
  },
  methods: {
    rgbPercent (rgbNum) {
      return parseInt(rgbNum) / 255 * 100
    },
    // TODO: 切换之后保持 keep-alive
    retrieveColorAndSelect (colorId) {
      this.colorSelected = this.common.retrieveColorAndSelect(colorId, this.colorList)
    },
    changeColor (color) {
      this.isColorDisabled = true
      // watch $route and change color
      // see also:https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      // eslint-disable-next-line handle-callback-err
      this.$router.push({ path: this.selfRouter, query: { colorId: color.id } }).catch(err => {})
      let loadObj = this.common.loadSentence()
      this.msg = loadObj.msg
      this.loadSentSuccess = loadObj.success
      setTimeout(() => {
        this.isColorDisabled = false
      }, 1000)
    },
    share () {
      window.open(
        `https://github.com/imoyao/Traditional-Chinese-Colors`
      )
    },
    // 复制按钮
    copy (hex) {
      if (!this.isCopied) {
        clipboardCopy(`${hex}`)
        this.isCopied = true
        setTimeout(() => {
          this.isCopied = false
        }, 1000)
      }
    },
    // 随机选择
    random () {
      let colorLength = this.colorList.length
      let random = this.colorList[Math.floor(Math.random() * colorLength)]
      this.changeColor(random)
    },
    listAnime (el, isInit) {
      if (this.lastEls && isInit) {
        anime.remove(this.lastEls)
      }
      this.lastEls = el
      anime({
        targets: el,
        translateY: [250, 0],
        opacity: [0, 1],
        easing: 'easeOutSine',
        delay: function (el, i, l) {
          return i * 80
        },
      })
    },
    displayAnime () {
      let monji = document.querySelectorAll('.display .kanji,.romaji,.color-decs')
      let rgb = document.querySelectorAll('.display .rgb-number .cymk')
      let cmyk = document.querySelectorAll('.display .cmyk-number .cymk')
      anime.remove([monji, rgb, cmyk])
      anime({
        targets: monji,
        translateX: [150, 0],
        opacity: [0, 1],
        easing: 'easeOutSine',
      })
      anime({
        targets: rgb,
        innerHTML: (el, i, l) => {
          return this.colorSelected.rgb[i]
        },
        round: 1,
        easing: 'easeOutSine',
      })
      anime({
        targets: cmyk,
        innerHTML: (el, i, l) => {
          return this.colorSelected.cmyk[i]
        },
        round: 1,
        easing: 'easeOutSine',
      })
    },

    loadSentence: function () {
      let loadObj = this.common.loadSentence()
      this.msg = loadObj.msg
      this.loadSentSuccess = loadObj.success
    },
    formatPercent (percentage) {
      return Math.round(percentage / 100 * 255) // 四舍五入
    },
    formatCMYKPercent (percentage) {
      return parseInt(percentage)
    },
    bigTitle () {
      if (this.selfRouter === '/nippon') {
        return this.colorSelected.tra_name || this.landShow.title
      } else {
        return this.colorSelected.name || this.landShow.title
      }
    },
    colorDesc () {
      let firstDesc = this.colorSelected.desc
      if (firstDesc) {
        return firstDesc
      } else {
        return this.loadSentSuccess ? '📢' + this.msg : this.landShow.desc
      }
    },

  },
}
</script>

<style lang="scss">
@import '@/mixin.scss';
.base {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  .display {
    position: relative;
    height: 100%;
    width: 100px;
    flex-grow: 1;
    transition: all 1s;
    .series,
    .share,
    .copy,
    .random {
      position: absolute;
      height: 1.2rem;
      width: 1.2rem;
      bottom: 3rem;
    }
    .share,
    .copy,
    .select-brand
    .random {
      transition: all 1s;
      fill: #0c0c0c;
    }
    .series {
      right: 1+1.6 * 0rem;
    }
    .copy {
      right: 1+1.6 * 1rem;
    }
    .random {
      right: 1+1.6 * 2rem;
    }
    .select-brand {
      position: absolute;
      bottom: 3rem;
      height: 1.2rem;
      right: 1+1.6 * 3rem;
    }
    .romaji {
      position: absolute;
      bottom: 3rem;
      left: 5rem;
      writing-mode: vertical-lr;
      letter-spacing: 0.2rem;
    }
    .kanji {
      font-family: 'FZQKBYSJT',serif;
      position: absolute;
      bottom: 3rem;
      left: 1rem;
      writing-mode: vertical-lr;
      letter-spacing: 0.5rem;
      font-size: 3rem;
    }
    .color-decs {
      font-family: 'FZQKBYSJT',serif;
      position: absolute;
      bottom: 3rem;
      left: 7rem;
      letter-spacing: 0.2rem;
      line-height: 1rem;
      width: 50%;
      font-size: 0.8rem;
      white-space:normal;
      word-break:break-all;
      overflow:hidden;
      @include for-phone {
        writing-mode: vertical-lr;
        text-align: end;
        height: 68%;
      }
      @include for-tablet {
        writing-mode: vertical-lr;
        text-align: end;
        height: 68%;
      }
    }
    .rgb-block {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      margin-bottom: 2px;
      .r,
      .g,
      .b {
        transition: all 1s;
        background-color: #0c0c0c;
        height: 2px;
        width: 0%;
        margin-top: 2px;
      }
    }
    .rgb-number {
      font-family: 'MONO',sans-serif;
      font-size: 1.3rem;
      display: flex;
      justify-content: space-around;
    }
    // mononspace needed
    .cmyk-number {
      font-family: 'MONO',sans-serif;
      /*font-size: 1.3rem;*/
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      margin: 1rem 1rem;
      .n {
        &::after {
          /*margin-bottom: 0.5rem;*/
          margin-left: -0.5rem;
          display: inline-block;
          font-size: 0.5rem;
          position: relative;
          top: -0.8rem;
        }
      }
      .c {
        &::before {
          content: 'C';
        }
      }
      .m {
        &::before {
          content: 'M';
        }
      }
      .y {
        &::before {
          content: 'Y';
        }
      }
      .k {
        &::before {
          content: 'K';
        }
      }
    }
  }
  .tab-wrapper {
    flex-shrink: 0;
    height: 100%;
    overflow-y: scroll;
    @include for-phone {
      flex-basis: 100px;
    }

    @include for-tablet {
      flex-basis: 400px;
    }
    @include for-desktop {
      flex-basis: 800px;
    }
    @include for-desktop-plus {
      flex-basis: 1200px;
    }
    .tab {
      min-height: 100%;
      width: 100%;
      position: relative;
      &:before {
        content: '';
        display: block;
        width: 100%;
        height: 100%;
        position: absolute;
        background: url(https://raw.githubusercontent.com/masantu/statics/master/images/16163833_p9.jpg) repeat local;
        opacity: 0.3;
      }
      @include for-tablet-up {
        display: flex;
        justify-content: flex-start;
        align-content: flex-start;
        flex-wrap: wrap;
      }
      .tab-item {
        margin-bottom: 1rem;
        @include for-phone {
          width: 100%;
        }
        @include for-tablet {
          width: 33%;
        }
        @include for-desktop {
          width: 25%;
        }
        @include for-desktop-plus {
          width: 20%;
        }
      }
    }
  }
}
.color-bright {
  color: #fffffb !important;
}
.bg-bright {
  background-color: #fffffb !important;
}
.js-tab-item {
  // for animate initial state
  opacity: 0;
}
.el-progress-bar__inner {
  background-image: linear-gradient(45deg,rgba(255,255,255,.15) 25%,transparent 25%,transparent 50%,rgba(255,255,255,.15) 50%,rgba(255,255,255,.15) 75%,transparent 75%,transparent);
  background-size: 1rem 1rem;
}
/*去除背景色*/
.color-rgb-progress/deep/.el-progress-bar__outer{
  background-color: transparent;
}
.el-progress.el-progress--circle{
  margin-bottom: 0.5rem;
}
.color-rgb-progress/deep/.el-progress-bar__innerText{
  margin-top: -0.56rem;
}
.el-progress--circle .el-progress__text, .el-progress--dashboard .el-progress__text{
  top: 65% !important;
}
.el-progress-bar__innerText{
   padding-bottom: 1rem;
}
</style>
