<template>
  <div class="footer-info">
    <footer :url-href="urlHref"><p>© 2020 别院牧志 | <button @click="goNippon(urlHref)">友链</button>
    </p></footer>
  </div>
</template>

<script>
export default {
  name: 'ColorFooter',
  props: {
    urlHref: {
      type: String,
      default: '/',
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
  }
}
</style>
