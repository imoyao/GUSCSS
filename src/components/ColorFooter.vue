<template>
  <div class="footer-info">
    <footer>
      <p :class="{'fill-bright':!isBright}">© 2020
        <el-link
          :class="{'fill-bright':!isBright}"
          :href="`${ copyInfo.href }`"
          target="_blank">
          {{ copyInfo.title }}
        </el-link> 作品
        <router-link
          v-for="(site,index) in showAbleSites"
          :class="{'fill-bright':!isBright}"
          :key="index"
          :to="`${ site.href }`"><el-divider direction="vertical"/><span>{{ site.title }}</span></router-link >
        <br>保留删库跑路、域名过期等权利
    </p></footer>
  </div>
</template>

<script>
export default {
  name: 'ColorFooter',
  props: {
    fillColor: {
      type: String,
      default: 'dark',
    },
    isBright: {
      type: Boolean,
      default: true,
    },
    copied: {
      type: Boolean,
      default: false,
    },
  },
  data () {
    return {
      copyInfo: {
        title: '别院牧志',
        href: 'https://masantu.com',
      },
      footerLinks:
        [{ title: 'nippon', href: '/nippon' }, { title: '中国传统色', href: '/' }, { title: 'lipsticks', href: '/lipsticks' },
        ],
    }
  },

  computed: {
    showAbleSites: function () {
      return this.footerLinks.filter(function (site) {
        return site.href !== '/'
      })
    },
  },
  methods: {
    goNippon (urlHref) {
      // eslint-disable-next-line handle-callback-err
      this.$router.push({ path: urlHref }).catch(err => {})
    },
  },
}
</script>

<style lang="scss" scoped>
.footer-info{
  position: fixed;
  bottom: 0.5rem;
  left: 1.2rem;
  p{
    margin: 0;
    line-height: 0.8rem;
    font-size: .5rem;
    a{
      font-size: .6rem;
      color:#fffffb;
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
}
</style>
