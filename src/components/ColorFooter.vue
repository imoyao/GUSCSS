<template>
  <div
    :class="{'fill-bright':!isBright}"
    class="footer-info">
    <footer class="foot-link">
      <p>
        <router-link
          v-for="(site,index) in showAbleSites"
          :class="{'fill-bright':!isBright}"
          :key="index"
          :to="`${ site.href }`"><el-divider direction="vertical"/><span>{{ site.title }}</span>
        </router-link >
      </p>
      <p
        :class="{'fill-bright':!isBright}"
        class="footer-deco">© {{ nowYear }}
        <el-link
          :class="{'fill-bright':!isBright}"
          :href="`${ copyInfo.href }`"
          target="_blank">
          {{ copyInfo.title }}
        </el-link> 作品<el-divider direction="vertical"/>
        <el-link
          :class="{'fill-bright':!isBright}"
          :href="`${ repoInfo.href }`"
          target="_blank">
          {{ repoInfo.title }}
        </el-link><el-divider direction="vertical"/>保留删库跑路、域名过期等权利
      </p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'ColorFooter',
  props: {
    href: {
      type: String,
      default: '/',
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
      repoInfo: {
        title: '源码',
        href: 'https://github.com/imoyao/GUSCSS/',
      },
      footerLinks:
        [{ title: '中国传统色', href: '/' }, { title: '日本の伝統色', href: '/nippon' }, { title: '不问色号', href: '/lipsticks' },
        ],
    }
  },
  computed: {
    showAbleSites: function () {
      let that = this
      return this.footerLinks.filter(function (site) {
        return site.href !== that.href
      })
    },
    nowYear: function () {
      let nowDate = new Date()
      return nowDate.getFullYear()
    },
  },
}
</script>

<style lang="scss" scoped>
@import '../mixin.scss';
.footer-info{
  position: fixed;
  bottom: 0.5rem;
  left: 1.2rem;
  font-size: .5rem;
  p{
    margin: 0;
    line-height: 0.8rem;
    /*font-size: .5rem;*/
    @include for-phone {
      width:275px;
      white-space: normal;
    }
    .footer-deco{
     margin-bottom: 3px;
    }
    a{
      /*font-size: .6rem;*/
      color:#0c0c0c;
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
  .fill-bright {
    fill: #fffffb !important;
  }
}
</style>
