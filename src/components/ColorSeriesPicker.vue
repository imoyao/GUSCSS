<template>

  <div
    class="picker"
    @click="toggle">
    <div
      v-for="item in colorSeries"
      :key="item.hex"
      :data-color="item.color"
      :style="`border:0.1rem solid #${!isBright?'fffffb':'0c0c0c'};background-color:${item.hex};z-index:${item.color === currentColor?999:1};`"
      class="circle" />
    <div
      :style="`border:0.1rem solid #${!isBright?'fffffb':'0c0c0c'};z-index:${'all' === currentColor?999:1};`"
      class="circle linear-gradient"
      data-color="all" />
  </div>
</template>

<script>
import anime from 'animejs'
export default {
  props: {
    isBright: {
      type: Boolean,
      default: true,
    },
    borderColor: {
      type: String,
      default: 'dark',
    },
    colorSeries: {
      type: Array,
      default: () => [],
    },
  },
  data () {
    return {
      isOpen: false,
      anime: null,
      currentColor: null,
    }
  },
  mounted () {},
  methods: {
    open () {
      anime({
        targets: document.querySelectorAll('.circle'),
        translateY: [
          '0rem',
          function (el, i, l) {
            return i * -2 + 'rem'
          },
        ],
        duration: 100,
        easing: 'easeInSine',
      })
    },
    close () {
      anime({
        targets: document.querySelectorAll('.circle'),
        translateY: [
          function (el, i, l) {
            return i * -2 + 'rem'
          },
          '0rem',
        ],
        duration: 100,
        easing: 'easeInSine',
      })
    },
    toggle (e) {
      if (this.isOpen === false) {
        this.open()
        this.isOpen = true
      } else {
        this.close()
        this.$emit('colorChange', (this.currentColor = e.target.dataset.color))
        this.isOpen = false
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.picker {
  position: relative;
  height: 100%;
  width: 100%;
  .circle {
    box-sizing: border-box; // 待定
    transition: all 1s;
    position: absolute;
    height: 100%;
    width: 100%;
    border-radius: 50%;
  }
  .linear-gradient {
    z-index: 998;
    background: linear-gradient(
      to top right,
      #fffffb,
      #cb1b45,
      #f7c242,
      #7db9de,
      #00aa90,
      #8a6bbe,
      #fffffb
    );
  }
}
</style>
