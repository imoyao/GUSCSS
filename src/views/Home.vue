<template>
  <div class="home">
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
      <ShareButton
        :is-bright="colorSelected.is_bright"
        class="share"
        @click.native="share(colorSelected.name)" />
      <RandomButton
        :is-bright="colorSelected.is_bright"
        class="random"
        @click.native="random" />
      <ColorSeriesPicker
        :is-bright="colorSelected.is_bright"
        class="series"
        @colorChange="changeColorSeries" />
      <div class="color-remark">
        {{ colorSelected.pinyin||'zhōng guó chuán tǒng sè' }}
      </div>
      <div class="kanji">
        {{ colorSelected.name||'中国传统色' }}
      </div>
      <div class="romaji">
        {{ colorSelected.color||'The Traditional Colors of China' }}
      </div>
      <div class="color-decs">
        {{ colorSelected.desc|| '📢'+this.msg ||'梅子金黄杏子肥，麦花雪白菜花稀。' }}
      </div>
      <div class="rgb-block">
        <div
          v-for="(el,i) in ['r','g','b']"
          :key="el"
          :style="`width:${colorSelected.rgb?(colorSelected.rgb[i]/255*100):0}%`"
          :class="{[el]:true,'bg-bright':!colorSelected.is_bright}" />
      </div>
      <div
        v-if="colorSelected.rgb"
        class="rgb-number">
        <template v-for="el in ['R','G','B']">
          <div :key="el">{{ el }}</div>
          <div
            :key="el + 'n'"
            class="n">0</div>
        </template>
      </div>
      <div
        v-if="colorSelected.cmyk"
        class="cmyk-number">
        <div
          v-for="(el,index) in ['c','m','y','k']"
          :class="{[el]:true}">
          <CircleProgress
            :is-bright="colorSelected.is_bright"
            :id="index"
            :radius="5"
            :barColor="cymkList[index]"
            :progress="colorSelected.cmyk[index]"
            :backgroundColor="'rgba(255,255,255,0.7)'"
            :widthPresent="1/colorSelected.cmyk.length"
            :isAnimation="true"
          > </CircleProgress>
        </div>
      </div>
    </div>
    <div class="tab-wrapper">
      <div class="tab">
        <ColorTab
          v-for="color in colorList"
          :key="color.id"
          :kanji="color.name"
          :hex="color.hex"
          class="js-tab-item tab-item"
          @click.native="changeColor(color)" />
      </div>
    </div>
  </div>
</template>

<script>
import anime from 'animejs'
const jinrishici=require('jinrishici')
import ColorTab from '@/components/ColorTab.vue'
import ColorSeriesPicker from '@/components/ColorSeriesPicker.vue'
import ShareButton from '@/components/ShareButton.vue'
import CopyButton from '@/components/CopyButton.vue'
import RandomButton from '@/components/RandomButton.vue'
import CircleProgress  from '@/plugins/CircleProgress.vue';
// import colorList from '@/data/color'
// TODO: 打包之后验证
// import colorList from '@/data/zhColors.json'
import colorData from '@/data/zhColors.json'

import {
  checkInSight,
  checkInSightInit,
  throttle,
  clipboardCopy,
} from '@/util.js'

export default {
  name: 'Home',
  components: {
    ColorTab,
    ColorSeriesPicker,
    ShareButton,
    CopyButton,
    RandomButton,
    CircleProgress,
  },
  data () {
    return {
      msg: String,
      colorList: [],
      colorSelected: {},
      isCopied: false,
      lastEls: null,
      cymkList:[
        '#00FFFF',
        '#800080',
        '#FFFF00',
        '#000000',
      ]
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
    this.colorList = colorData.data
    // route to specific color
    this.retrieveColorAndSelect(this.$route.query.colorId)
    document
      .querySelector('.tab-wrapper')
      .addEventListener('scroll', throttle(checkInSight(this.listAnime)))
    window.addEventListener(
      'resize',
      throttle(checkInSight(this.listAnime), 1000)
    )
    this.loadSentence()
  },
  methods: {
    retrieveColorAndSelect (colorId) {
      if (colorId) {
        this.colorSelected = this.colorList.find(val => val.id === colorId)
      } else {
        this.colorSelected = {
          hex: '#ffffff',
          is_bright: true,
        }
      }
    },
    // 切换颜色分组
    changeColorSeries (color) {
      document.querySelector('.tab-wrapper').scrollTop = 0
      if (color === 'all') this.colorList = colorData.data
      else this.colorList = colorData.data.filter(val => val.color_series === color)
      this.colorSelected = this.colorList[0]
    },
    changeColor (color) {
      // watch $route and change color
      this.$router.push({ path: '/', query: { colorId: color.id } })
      this.loadSentence()
    },
    // TODO 修改为访问仓库
    share (name) {
      // let location = window.location.href
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
      let random = colorList[Math.floor(Math.random() * colorData.data.length)]
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
      let monji = document.querySelectorAll('.display .kanji,.romaji,.color-decs,color-remark')
      let rgb = document.querySelectorAll('.display .rgb-number .n')
      let cmyk = document.querySelectorAll('.display .cmyk-number .n')
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
      // anime({
      //   targets: cmyk,
      //   innerHTML: (el, i, l) => {
      //     return this.colorSelected.cmyk[i]
      //   },
      //   round: 1,
      //   easing: 'easeOutSine',
      // })
    },

    loadSentence: function() {
      jinrishici.load(result => {
        this.msg = result.data.content
      }, err => {
        console.log("test");
      })
    }
},
}
</script>

<style lang="scss" scoped>
@import '@/mixin.scss';
.home {
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
      bottom: 1.5rem;
    }
    .share,
    .copy,
    .random {
      transition: all 1s;
      fill: #0c0c0c;
    }
    .series {
      right: 1+1.6 * 0rem;
    }
    .share {
      right: 1+1.6 * 1rem;
    }
    .copy {
      right: 1+1.6 * 2rem;
    }
    .random {
      right: 1+1.6 * 3rem;
    }
    .romaji {
      position: absolute;
      bottom: 1.5rem;
      left: 6.5rem;
      writing-mode: vertical-lr;
      letter-spacing: 0.2rem;
    }
    .color-remark {
      position: absolute;
      bottom: 1.5rem;
      left: 1.5rem;
      writing-mode: vertical-lr;
      letter-spacing: 0.2rem;
    }
    .kanji {
      font-family: 'FZQKBYSJT',serif;
      position: absolute;
      bottom: 1rem;
      left: 3rem;
      writing-mode: vertical-lr;
      letter-spacing: 0.5rem;
      font-size: 3rem;
    }
    .color-decs {
      font-family: 'FZQKBYSJT',serif;
      position: absolute;
      bottom: 1.5rem;
      left: 8rem;
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
      font-family: 'MONO';
      font-size: 1.3rem;
      display: flex;
      justify-content: space-around;
    }
    // mononspace needed
    .cmyk-number {
      font-family: 'MONO';
      font-size: 1.3rem;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      margin: 2rem 1rem;
      .n {
        &::after {
          margin-bottom: 0.5rem;
          margin-left: -0.5rem;
          display: inline-block;
          font-size: 1rem;
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
        background: url(../assets/64253519_p9.png);
        background-attachment: local;
        background-repeat: repeat;
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
</style>
