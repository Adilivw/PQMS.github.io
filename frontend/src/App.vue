<template>
  <div id="app">
    <el-container>
      <el-header>
        <nav-header></nav-header>
      </el-header>
      
      <el-container>
        <el-aside width="200px">
          <nav-menu></nav-menu>
        </el-aside>
        
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import NavHeader from '@/components/NavHeader.vue'
import NavMenu from '@/components/NavMenu.vue'

export default {
  name: 'App',
  components: {
    NavHeader,
    NavMenu
  }
}
</script>

<style>
#app {
  font-family: 'Microsoft YaHei', sans-serif;
  -webkit-font-smoothing: antialiased;
  height: 100vh;
}

.el-header {
  background-color: #409EFF;
  color: white;
  line-height: 60px;
}

.el-aside {
  background-color: #545c64;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style> 