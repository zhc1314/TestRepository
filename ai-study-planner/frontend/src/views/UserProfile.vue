<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>用户信息采集 - 考研画像</h2>
          <p class="subtitle">请填写您的考研基本信息，帮助AI为您定制学习规划</p>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="140px"
        class="profile-form"
      >
        <!-- 基本信息 -->
        <el-divider content-position="left">基本信息</el-divider>
        <el-form-item label="用户ID" prop="user_id">
          <el-input v-model="formData.user_id" placeholder="请输入用户ID" />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="formData.nickname" placeholder="请输入昵称" />
        </el-form-item>

        <!-- 目标院校/专业 -->
        <el-divider content-position="left">目标设定</el-divider>
        <el-form-item label="目标院校" prop="target_university">
          <el-input v-model="formData.target_university" placeholder="如：北京大学" />
        </el-form-item>
        <el-form-item label="目标专业" prop="target_major">
          <el-input v-model="formData.target_major" placeholder="如：计算机科学与技术" />
        </el-form-item>
        <el-form-item label="是否跨考">
          <el-switch v-model="formData.is_cross_major" />
        </el-form-item>
        <el-form-item label="专业课科目">
          <el-select
            v-model="formData.major_subjects"
            multiple
            placeholder="请选择专业课科目"
            style="width: 100%"
          >
            <el-option label="数据结构" value="数据结构" />
            <el-option label="计算机组成原理" value="计算机组成原理" />
            <el-option label="操作系统" value="操作系统" />
            <el-option label="计算机网络" value="计算机网络" />
          </el-select>
        </el-form-item>

        <!-- 目标分数 -->
        <el-divider content-position="left">目标分数</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="目标总分" prop="target_total_score">
              <el-input-number v-model="formData.target_total_score" :min="0" :max="500" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="政治目标分">
              <el-input-number v-model="formData.target_politics_score" :min="0" :max="100" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="英语目标分">
              <el-input-number v-model="formData.target_english_score" :min="0" :max="100" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="数学目标分">
              <el-input-number v-model="formData.target_math_score" :min="0" :max="150" />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 备考时间规划 -->
        <el-divider content-position="left">备考时间规划</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="备考开始时间" prop="study_start_date">
              <el-date-picker
                v-model="formData.study_start_date"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="考试日期" prop="exam_date">
              <el-date-picker
                v-model="formData.exam_date"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="工作日学习时长">
              <el-input-number v-model="formData.weekday_study_hours" :min="0" :max="24" :precision="1" />
              <span class="input-suffix">小时/天</span>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="周末学习时长">
              <el-input-number v-model="formData.weekend_study_hours" :min="0" :max="24" :precision="1" />
              <span class="input-suffix">小时/天</span>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 现有基础评估 -->
        <el-divider content-position="left">现有基础评估</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="政治基础">
              <el-select v-model="formData.politics_level" placeholder="请选择">
                <el-option label="优秀" value="优秀" />
                <el-option label="良好" value="良好" />
                <el-option label="一般" value="一般" />
                <el-option label="较差" value="较差" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="英语基础">
              <el-select v-model="formData.english_level" placeholder="请选择">
                <el-option label="优秀" value="优秀" />
                <el-option label="良好" value="良好" />
                <el-option label="一般" value="一般" />
                <el-option label="较差" value="较差" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="数学基础">
              <el-select v-model="formData.math_level" placeholder="请选择">
                <el-option label="优秀" value="优秀" />
                <el-option label="良好" value="良好" />
                <el-option label="一般" value="一般" />
                <el-option label="较差" value="较差" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 学习偏好 -->
        <el-divider content-position="left">学习偏好</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学习时间偏好">
              <el-select v-model="formData.study_time_preference" placeholder="请选择">
                <el-option label="早起" value="早起" />
                <el-option label="熬夜" value="熬夜" />
                <el-option label="正常作息" value="正常" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学习方法偏好">
              <el-select v-model="formData.study_method_preference" placeholder="请选择">
                <el-option label="视频课为主" value="视频课" />
                <el-option label="刷题为主" value="刷题" />
                <el-option label="看书为主" value="看书" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="其他偏好">
          <el-input
            v-model="formData.other_preferences"
            type="textarea"
            :rows="3"
            placeholder="请输入其他学习偏好或说明"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading" size="large">
            提交并进入系统
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { createUserProfile, type UserProfile } from '@/api/userProfile'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const formData = reactive<UserProfile>({
  user_id: '',
  nickname: '',
  target_university: '',
  target_major: '',
  is_cross_major: false,
  major_subjects: [],
  target_total_score: undefined,
  target_politics_score: undefined,
  target_english_score: undefined,
  target_math_score: undefined,
  study_start_date: '',
  exam_date: '',
  weekday_study_hours: undefined,
  weekend_study_hours: undefined,
  politics_level: '',
  english_level: '',
  math_level: '',
  study_time_preference: '',
  study_method_preference: '',
  other_preferences: ''
})

const rules: FormRules = {
  user_id: [{ required: true, message: '请输入用户ID', trigger: 'blur' }],
  target_university: [{ required: true, message: '请输入目标院校', trigger: 'blur' }],
  target_major: [{ required: true, message: '请输入目标专业', trigger: 'blur' }],
  target_total_score: [{ required: true, message: '请输入目标总分', trigger: 'blur' }]
}

const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        loading.value = true
        const response = await createUserProfile(formData)
        
        userStore.setUserId(formData.user_id)
        userStore.setUserProfile(response as UserProfile)
        
        ElMessage.success('信息提交成功！')
        router.push('/home')
      } catch (error) {
        console.error('提交失败:', error)
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.profile-card {
  max-width: 900px;
  width: 100%;
}

.card-header h2 {
  margin: 0 0 10px 0;
  color: #303133;
}

.subtitle {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.profile-form {
  margin-top: 20px;
}

.input-suffix {
  margin-left: 10px;
  color: #909399;
}
</style>