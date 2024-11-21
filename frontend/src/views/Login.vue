<template>
  <div class="login-container">
    <div class="login-box">
      <div class="title-container">
        <h2 class="title">涂装工艺智能管理平台</h2>
        <div class="subtitle">Intelligent Coating Process Management</div>
      </div>
      
      <el-form ref="loginForm" :model="loginForm" :rules="loginRules">
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            prefix-icon="el-icon-user"
            placeholder="用户名">
          </el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            prefix-icon="el-icon-lock"
            type="password"
            placeholder="密码">
          </el-input>
        </el-form-item>
        
        <el-button type="primary" class="login-button" @click="handleLogin">
          登录系统
        </el-button>
      </el-form>
    </div>
    
    <!-- 动态背景效果 -->
    <div class="particles-container" ref="particles"></div>
  </div>
</template>

<script>
import particles from 'particles.js'

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
    }
  },
  mounted() {
    if (window.particlesJS) {
      window.particlesJS.load('particles-js', '/particles.json')
    }
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          // 登录逻辑
          this.$router.push('/dashboard')
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  height: 100vh;
  background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.login-box {
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  z-index: 1;
}

.title-container {
  text-align: center;
  margin-bottom: 40px;
  
  .title {
    font-size: 28px;
    color: #303133;
    margin-bottom: 10px;
    font-weight: bold;
  }
  
  .subtitle {
    font-size: 16px;
    color: #909399;
  }
}

.login-button {
  width: 100%;
  margin-top: 20px;
  padding: 12px 0;
  font-size: 16px;
}

.particles-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style> 