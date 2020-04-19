<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h2>Essential Links</h2>
    <ul>
      <li>
        <a
          href="/"
          target="_blank"
        >
          首页
        </a>
      </li>
      <li>
        <a
          href="https://github.com/imoyao/Traditional-Chinese-Colors"
          target="_blank"
        >
          源码
        </a>
      </li>
      <li>
        由<a
          href="https://www.masantu.com/"
          target="_blank"
        >
          别院牧志
        </a>开发维护
      </li>
    </ul>
    <h2>Ecosystem</h2>
    <ul>
      <li>
        <a
          href="http://router.vuejs.org/"
          target="_blank"
        >
          vue-router
        </a>
      </li>
      <li>
        <a
          href="http://vuex.vuejs.org/"
          target="_blank"
        >
          vuex
        </a>
      </li>
      <li>
        <a
          href="http://vue-loader.vuejs.org/"
          target="_blank"
        >
          vue-loader
        </a>
      </li>
      <li>
        <a
          href="https://github.com/vuejs/awesome-vue"
          target="_blank"
        >
          awesome-vue
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'About',
  data () {
    return {
      msg: 'Welcome to Traditional Chinese Colors'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.hello{
  text-align:center
}
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>


<!--<template>-->
<!--    <div class="markdown-body">-->
<!--        关于页面参见 <a target="_blank" href="https://github.com/imoyao/Traditional-Chinese-Colors">源码</a>-->
<!--    </div>-->
<!--</template>-->

<!--&lt;!&ndash;<script>&ndash;&gt;-->
<!--&lt;!&ndash;    // import readme from '../readme.md'&ndash;&gt;-->
<!--&lt;!&ndash;    // import 'highlight.js/styles/github.css'&ndash;&gt;-->
<!--&lt;!&ndash;    // import 'github-markdown-css'&ndash;&gt;-->
<!--&lt;!&ndash;    //&ndash;&gt;-->
<!--&lt;!&ndash;    // export default {&ndash;&gt;-->
<!--&lt;!&ndash;    //     components: {&ndash;&gt;-->
<!--&lt;!&ndash;    //         readme&ndash;&gt;-->
<!--&lt;!&ndash;    //     },&ndash;&gt;-->
<!--&lt;!&ndash;    // }&ndash;&gt;-->
<!--&lt;!&ndash;</script>&ndash;&gt;-->
<!--&lt;!&ndash; Add "scoped" attribute to limit CSS to this component only &ndash;&gt;-->
<!--<style scoped>-->
<!--    .main {-->
<!--        padding: 10px 30px;-->
<!--    }-->

<!--    blockquote {-->
<!--        border-left: #eee solid 5px;-->
<!--        padding-left: 15px;-->
<!--        color: #8e8e8e;-->
<!--        margin-inline-start: 0px;-->
<!--        margin-inline-end: 0px;-->
<!--    }-->

<!--    ul li {-->
<!--        line-height: 25px;-->
<!--    }-->

<!--    pre code {-->
<!--        background: #F6F6F6;-->
<!--    }-->

<!--    p code {-->
<!--        color: #D34B62;-->
<!--        background: #F6F6F6;-->
<!--        margin: 0 2px;-->
<!--    }-->

<!--    @keyframes squeezeBody {-->
<!--        from {-->
<!--            width: 100%;-->
<!--        }-->
<!--        to {-->
<!--            width: calc(100% - 300px);-->
<!--        }-->
<!--    }-->

<!--    @-webkit-keyframes squeezeBody {-->
<!--        from {-->
<!--            width: 100%;-->
<!--        }-->
<!--        to {-->
<!--            width: calc(100% - 300px);-->
<!--        }-->
<!--    }-->

<!--    @keyframes stretchBody {-->
<!--        from {-->
<!--            width: calc(100% - 300px);-->
<!--        }-->
<!--        to {-->
<!--            width: 100%;-->
<!--        }-->
<!--    }-->

<!--    @-webkit-keyframes stretchBody {-->
<!--        from {-->
<!--            width: calc(100% - 300px);-->
<!--        }-->
<!--        to {-->
<!--            width: 100%;-->
<!--        }-->
<!--    }-->

<!--    .squeezed-body {-->
<!--        animation: squeezeBody 0.5s ease;-->
<!--        -webkit-animation: squeezeBody 0.5s ease;-->
<!--        width: calc(100% - 300px);-->
<!--    }-->

<!--    .full-body {-->
<!--        animation: stretchBody 0.5s ease;-->
<!--        -webkit-animation: stretchBody 0.5s ease;-->
<!--        width: 100%;-->
<!--    }-->

<!--    h1,-->
<!--    h2,-->
<!--    h3,-->
<!--    h4,-->
<!--    h5,-->
<!--    h6 {-->
<!--        font-family: 'Old Standard TT', serif;-->
<!--        font-weight: bold;-->
<!--    }-->

<!--    h1 {-->
<!--        border-bottom: 1px solid #ddd;-->
<!--    }-->

<!--    .serif {-->
<!--        font-family: 'Old Standard TT', serif;-->
<!--    }-->

<!--    .top-bar {-->
<!--        height: 45px;-->
<!--        min-height: 45px;-->
<!--        position: absolute;-->
<!--        top: 0;-->
<!--        right: 0;-->
<!--        left: 0;-->
<!--    }-->

<!--    .bars-lnk {-->
<!--        color: #fff;-->
<!--    }-->

<!--    .bars-lnk i {-->
<!--        display: inline-block;-->
<!--        margin-left: 10px;-->
<!--        margin-top: 7px;-->
<!--    }-->

<!--    .bars-lnk img {-->
<!--        display: inline-block;-->
<!--        margin-left: 10px;-->
<!--        margin-top: -15px;-->
<!--        margin-right: 15px;-->
<!--        height: 35px;-->
<!--    }-->

<!--    .lateral-menu {-->
<!--        background-color: #333;-->
<!--        color: rgb(144, 144, 144);-->
<!--        width: 300px;-->
<!--        font-family: 'Open Sans', 'Myriad Pro', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Geneva, Verdana, sans-serif;-->
<!--    }-->

<!--    .lateral-menu label {-->
<!--        color: rgb(144, 144, 144);-->
<!--    }-->

<!--    .lateral-menu-content {-->
<!--        padding-left: 10px;-->
<!--        height: 100%;-->
<!--        font-size: 12px;-->
<!--        font-style: normal;-->
<!--        font-variant: normal;-->
<!--        font-weight: bold;-->
<!--        line-height: 16px;-->
<!--    }-->

<!--    .lateral-menu-content .title {-->
<!--        padding-top: 15px;-->
<!--        font-size: 2em;-->
<!--        height: 45px;-->
<!--    }-->

<!--    .lateral-menu-content-inner {-->
<!--        overflow-y: auto;-->
<!--        height: 100%;-->
<!--        padding-top: 10px;-->
<!--        padding-bottom: 50px;-->
<!--        padding-right: 10px;-->
<!--        font-size: 0.9em;-->
<!--    }-->

<!--    .container {-->
<!--        display: flex;-->
<!--        flex-direction: row;-->
<!--        flex-wrap: nowrap;-->
<!--        justify-content: center;-->
<!--        align-items: stretch;-->
<!--        width: 100%;-->
<!--        height: 100%;-->
<!--        padding-top: 65px;-->
<!--    }-->

<!--    .container > * {-->
<!--        display: block;-->
<!--        width: 50%;-->
<!--        margin-left: 10px;-->
<!--        margin-right: 10px;-->
<!--        max-height: 100%;-->
<!--    }-->

<!--    .container textarea {-->
<!--        resize: none;-->
<!--        font-family: Consolas, "Liberation Mono", Courier, monospace;-->
<!--        height: 97%;-->
<!--        max-height: 97%;-->
<!--        width: 45%;-->
<!--    }-->

<!--    #preview {-->
<!--        height: 97%;-->
<!--        max-height: 97%;-->
<!--        border: 1px solid #eee;-->
<!--        overflow-y: scroll;-->
<!--        width: 55%;-->
<!--        padding: 10px;-->
<!--    }-->

<!--    pre {-->
<!--        white-space: pre-wrap;-->
<!--        /* css-3 */-->
<!--        white-space: -moz-pre-wrap;-->
<!--        /* Mozilla, since 1999 */-->
<!--        white-space: -pre-wrap;-->
<!--        /* Opera 4-6 */-->
<!--        white-space: -o-pre-wrap;-->
<!--        /* Opera 7 */-->
<!--        word-wrap: break-word;-->
<!--        /* Internet Explorer 5.5+ */-->
<!--        background-color: #f8f8f8;-->
<!--        border: 1px solid #dfdfdf;-->
<!--        margin-top: 1.5em;-->
<!--        margin-bottom: 1.5em;-->
<!--        padding: 0.125rem 0.3125rem 0.0625rem;-->
<!--    }-->

<!--    pre {-->
<!--        padding: 16px;-->
<!--        overflow: auto;-->
<!--        font-size: 85%;-->
<!--        line-height: 1.45;-->
<!--        background-color: #f6f8fa;-->
<!--        border-radius: 3px;-->
<!--    }-->

<!--    .modal-wrapper {-->
<!--        position: absolute;-->
<!--        width: 100%;-->
<!--        height: 100%;-->
<!--        top: 0;-->
<!--        left: 0;-->
<!--        z-index: 999;-->
<!--        background-color: rgba(51, 51, 51, 0.5);-->
<!--    }-->

<!--    .modal-inner {-->
<!--        margin-top: 200px;-->
<!--        margin-left: auto;-->
<!--        margin-right: auto;-->
<!--        width: 600px;-->
<!--        height: 225px;-->
<!--        background-color: #fff;-->
<!--        opacity: 1;-->
<!--        z-index: 1000;-->
<!--    }-->

<!--    .modal-close-btn {-->
<!--        float: right;-->
<!--        display: inline-block;-->
<!--        margin-right: 5px;-->
<!--        color: #ff4336;-->
<!--    }-->

<!--    .modal-close-btn:hover {-->
<!--        float: right;-->
<!--        display: inline-block;-->
<!--        margin-right: 5px;-->
<!--        color: #8d0002;-->
<!--    }-->

<!--    .modal-topbar {-->
<!--        clear: both;-->
<!--        height: 25px;-->
<!--    }-->

<!--    .modal-inner .link-area {-->
<!--        margin: 10px;-->
<!--        height: 170px;-->
<!--    }-->

<!--    .modal-inner textarea {-->
<!--        width: 100%;-->
<!--        height: 100%;-->
<!--        margin: 0;-->
<!--        padding: 0;-->
<!--    }-->

<!--    .version {-->
<!--        color: white;-->
<!--        font-size: 0.8em !important;-->
<!--    }-->
<!--</style>-->
