<template>
  <div id="app">
    <div>
        <router-view></router-view>
    </div>
  </div>
</template>

<script>

export default {
    name: 'app',
    components: {

    },
}
</script>

<style>
    @import "./assets/css/main.css";
    @import "./assets/css/color-dark.css";
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
}
</style>
