<template>
  <div class="card">
    <div
      :style="`background-color:${hex};`"
      class="color-block"/>
    <div class="monji-block">
      <div class="kanji">{{ kanji }}</div>
      <div class="rgb">{{ hex }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ColorTab',
  props: {
    kanji: {
      type: String,
      default: '-',
    },
    hex: {
      type: String,
      default: '-',
    },
  },
  methods: {},
}
</script>

<style scoped lang="scss">
.card {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  color: #3a3226;
  height: 2.5rem;
  .color-block {
    height: 100%;
    width: 0.618rem;
    margin-right: 0.5rem;
  }
  .monji-block {
    flex-grow: 0;
    flex-shrink: 1;
    width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    .kanji {
      font-family: 'FZQKBYSJT',serif;
      width: 100%;
      text-align: left;
      overflow: hidden;
      text-overflow: ellipsis;
      font-size: 1.2rem;
    }
    .rgb {
      font-size: 0.8rem;
    }
  }
}
</style>
