<!--https://github.com/cgd199158/vue-circleProgress-->
<template>
  <div
    ref="box"
    class="content">
    <svg
      :id="idStr"
      :width="width"
      :height="width"
      style="transform: rotate(-90deg)"
      xmlns="http://www.w3.org/2000/svg"
    >
      <linearGradient
        :id="`gradient-${id}`"
        gradientUnits="userSpaceOnUse">
        <stop
          v-for="(item, index) in gradientsColor"
          :key="index"
          :offset="item.offset"
          :stop-color="item.color"
        />
      </linearGradient>
      <circle
        :r="(width-radius)/2"
        :cy="width/2"
        :cx="width/2"
        :stroke-width="radius"
        :stroke="backgroundColor"
        fill="none"
      />
      <circle
        v-if="gradientsColorShow"
        ref="$bar"
        :r="(width-radius)/2"
        :cy="width/2"
        :cx="width/2"
        :stroke="gradientsColor ? `url(#gradient-${id})` : barColor"
        :stroke-width="radius"
        :stroke-linecap="isRound ? 'round':'square'"
        :stroke-dasharray="(width-radius)*3.14"
        :stroke-dashoffset="dashoffsetValue"
        fill="none"
      />
    </svg>
    <div class="center-text">
      <p
        v-if="!$slots.default"
        :class="{'fill-bright':isBright}"
        class="title">{{ progress }}</p>
      <slot/>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    widthPresent: {
      type: Number,
      default: 1,
    },
    gradientsColor: {
      type: [Boolean, Array],
      default: false,
    },
    radius: {
      type: [Number, String],
      default: 20,
    }, // 进度条厚度
    progress: {
      type: [Number, String],
      default: 20,
    }, // 进度条百分比
    barColor: {
      type: String,
      default: '#1890ff',
    }, // 进度条颜色
    backgroundColor: {
      type: String,
      default: 'rgba(0,0,0,0.3)',
    }, // 背景颜色
    isAnimation: {
      // 是否是动画效果
      type: Boolean,
      default: true,
    },
    isRound: {
      // 是否是圆形画笔
      type: Boolean,
      default: true,
    },
    id: {
      // 组件的id，多组件共存时使用
      type: [String, Number],
      default: 1,
    },
    duration: {
      // 整个动画时长
      type: [String, Number],
      default: 1000,
    },
    delay: {
      // 延迟多久执行
      type: [String, Number],
      default: 200,
    },
    timeFunction: {
      // 动画缓动函数
      type: String,
      default: 'cubic-bezier(0.99, 0.01, 0.22, 0.94)',
    },
    isBright: {
      type: Boolean,
      default: true,
    },
  },
  data () {
    return {
      width: 200,
      idStr: '',
      oldValue: 0,
    }
  },
  computed: {
    gradientsColorShow: function () {
      return true
    },
    dashoffsetValue: function () {
      const { isAnimation, width, radius, progress, oldValue } = this
      return isAnimation
        ? ((width - radius) * 3.14 * (100 - oldValue)) / 100
        : ((width - radius) * 3.14 * (100 - progress)) / 100
    },
  },
  watch: {
    id: function () {
      this.idStr = `circle_progress_keyframes_${this.id || 1}`
    },
    progress: function (newData, oldData) {
      if (newData !== oldData) {
        this.oldValue = oldData
        this.setAnimation()
      }
    },
  },
  mounted () {
    this.idStr = `circle_progress_keyframes_${this.id || 1}`
    let self = this
    this.setCircleWidth()
    this.setAnimation()
    // 此处不能使用window.onresize
    window.addEventListener('resize', function () {
      self.setCircleWidth()
      self.setAnimation(self)
    })
  },
  methods: {
    setCircleWidth () {
      // const { widthPresent } = this;
      // let box = this.$refs.box;
      // let width = box.clientWidth * widthPresent;
      // let height = box.clientHeight * widthPresent;
      // this.width = width > height ? height : width;
      this.width = 50
    },
    setAnimation () {
      let self = this
      if (self.isAnimation) {
        // 重复定义判断
        if (document.getElementById(self.idStr)) {
          self.$refs.$bar.classList.remove(`circle_progress_bar${self.id}`)
        }
        this.$nextTick(() => {
          this.startAnimation()
        })
      }
    },
    startAnimation () {
      // 生成动画样式文件
      let style = document.createElement('style')
      style.id = this.idStr
      style.type = 'text/css'
      style.innerHTML = `
      @keyframes circle_progress_keyframes_name_${this.id} {
      from {stroke-dashoffset: ${((this.width - this.radius) *
        3.14 *
        (100 - this.oldValue)) /
        100}px;}
      to {stroke-dashoffset: ${((this.width - this.radius) *
        3.14 *
        (100 - this.progress)) /
        100}px;}}
      .circle_progress_bar${
  this.id
} {animation: circle_progress_keyframes_name_${this.id} ${
  this.duration
}ms ${this.delay}ms ${this.timeFunction} forwards;}`
      // 添加新样式文件
      document.getElementsByTagName('head')[0].appendChild(style)
      // 往svg元素中添加动画class
      this.$refs.$bar.classList.add(`circle_progress_bar${this.id}`)
    },
  },
}
</script>
<style  scoped>
.content {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.center-text {
  position: absolute;
  font-size: 22px;
  font-weight: bold;
}
/*占比文字和其他文字保持统一*/
.fill-bright {
  fill: #fffffb !important;
}
</style>
