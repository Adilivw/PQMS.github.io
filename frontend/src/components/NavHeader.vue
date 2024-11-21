<template>
  <div class="nav-header">
    <div class="logo">涂装工艺自动检测与智能评价系统</div>
    <div class="user-info">
      <el-dropdown>
        <span class="el-dropdown-link">
          管理员<i class="el-icon-arrow-down"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>个人信息</el-dropdown-item>
          <el-dropdown-item>退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavHeader'
}
</script>

<style scoped>
.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
}

.user-info {
  color: white;
  cursor: pointer;
}
</style> 