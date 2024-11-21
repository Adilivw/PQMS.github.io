<template>
  <el-menu
    :default-active="activeIndex"
    class="nav-menu"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b"
    router>
    <el-menu-item index="/dashboard">
      <i class="el-icon-menu"></i>
      <span>实时监控</span>
    </el-menu-item>
    
    <el-menu-item index="/spc">
      <i class="el-icon-s-data"></i>
      <span>SPC分析</span>
    </el-menu-item>
    
    <el-menu-item index="/analysis">
      <i class="el-icon-s-marketing"></i>
      <span>智能分析</span>
    </el-menu-item>
    
    <el-menu-item index="/data">
      <i class="el-icon-document"></i>
      <span>数据管理</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  name: 'NavMenu',
  data() {
    return {
      activeIndex: '/dashboard'
    }
  }
}
</script>

<style scoped>
.nav-menu {
  height: 100%;
  border-right: none;
}
</style> 