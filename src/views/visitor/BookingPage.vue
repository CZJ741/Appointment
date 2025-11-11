<template>
  <div class="max-w-4xl mx-auto bg-white rounded-xl shadow-md overflow-hidden">
    <!-- 页面标题 -->
    <div class="bg-primary p-6">
      <h1 class="text-2xl font-bold text-white">预约探访</h1>
      <p class="text-white/80 mt-1">请按步骤完成预约信息填写</p>
    </div>

    <!-- 步骤指示器 -->
    <div class="px-6 py-8">
      <div class="flex items-center justify-between mb-10">
        <div 
          class="flex flex-col items-center" 
          :class="{ 'text-primary': currentStep >= 1 }"
        >
          <div 
            class="w-10 h-10 rounded-full flex items-center justify-center mb-2 text-white font-bold"
            :class="{ 'bg-primary': currentStep >= 1, 'bg-gray-300': currentStep < 1 }"
          >
            1
          </div>
          <span class="text-sm font-medium">基本信息</span>
        </div>
        
        <div class="flex-1 h-1 mx-4 bg-gray-300">
          <div 
            class="h-full bg-primary transition-all duration-500" 
            :style="{ width: currentStep >= 2 ? '100%' : '0%' }"
          ></div>
        </div>
        
        <div 
          class="flex flex-col items-center" 
          :class="{ 'text-primary': currentStep >= 2 }"
        >
          <div 
            class="w-10 h-10 rounded-full flex items-center justify-center mb-2 text-white font-bold"
            :class="{ 'bg-primary': currentStep >= 2, 'bg-gray-300': currentStep < 2 }"
          >
            2
          </div>
          <span class="text-sm font-medium">亲属信息</span>
        </div>
        
        <div class="flex-1 h-1 mx-4 bg-gray-300">
          <div 
            class="h-full bg-primary transition-all duration-500" 
            :style="{ width: currentStep >= 3 ? '100%' : '0%' }"
          ></div>
        </div>
        
        <div 
          class="flex flex-col items-center" 
          :class="{ 'text-primary': currentStep >= 3 }"
        >
          <div 
            class="w-10 h-10 rounded-full flex items-center justify-center mb-2 text-white font-bold"
            :class="{ 'bg-primary': currentStep >= 3, 'bg-gray-300': currentStep < 3 }"
          >
            3
          </div>
          <span class="text-sm font-medium">确认提交</span>
        </div>
      </div>

      <!-- 第一步：基本信息 -->
      <div v-if="currentStep === 1" class="space-y-6 animate-fade-in">
        <h2 class="text-xl font-bold text-gray-800">基本信息</h2>
        <p class="text-gray-600">请填写探访人的基本信息</p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">探访人姓名 <span class="text-red-500">*</span></label>
            <input
              type="text"
              v-model="formData.visitorName"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors"
              placeholder="请输入您的姓名"
              required
            />
            <span v-if="errors.visitorName" class="text-red-500 text-xs mt-1 block">{{ errors.visitorName }}</span>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">性别 <span class="text-red-500">*</span></label>
            <div class="flex space-x-4">
              <label class="inline-flex items-center">
                <input 
                  type="radio" 
                  v-model="formData.gender" 
                  value="男"
                  class="form-radio text-primary focus:ring-primary"
                >
                <span class="ml-2">男</span>
              </label>
              <label class="inline-flex items-center">
                <input 
                  type="radio" 
                  v-model="formData.gender" 
                  value="女"
                  class="form-radio text-primary focus:ring-primary"
                >
                <span class="ml-2">女</span>
              </label>
            </div>
            <span v-if="errors.gender" class="text-red-500 text-xs mt-1 block">{{ errors.gender }}</span>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">身份证号码 <span class="text-red-500">*</span></label>
            <input
              type="text"
              v-model="formData.idCard"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors"
              placeholder="请输入18位身份证号码"
              maxlength="18"
              required
            />
            <span v-if="errors.idCard" class="text-red-500 text-xs mt-1 block">{{ errors.idCard }}</span>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">联系电话 <span class="text-red-500">*</span></label>
            <input
              type="tel"
              v-model="formData.phone"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors"
              placeholder="请输入手机号码"
              maxlength="11"
              required
            />
            <span v-if="errors.phone" class="text-red-500 text-xs mt-1 block">{{ errors.phone }}</span>
          </div>

          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">联系地址 <span class="text-red-500">*</span></label>
            <input
              type="text"
              v-model="formData.address"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors"
              placeholder="请输入详细联系地址"
              required
            />
            <span v-if="errors.address" class="text-red-500 text-xs mt-1 block">{{ errors.address }}</span>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">戒毒人员姓名 <span class="text-red-500">*</span></label>
            <input
              type="text"
              v-model="formData.patientName"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors"
              placeholder="请输入戒毒人员姓名"
              required
            />
            <span v-if="errors.patientName" class="text-red-500 text-xs mt-1 block">{{ errors.patientName }}</span>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">与戒毒人员关系 <span class="text-red-500">*</span></label>
            <select
              v-model="formData.relationship"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors"
              required
            >
              <option value="">请选择关系</option>
              <option value="配偶">配偶</option>
              <option value="父母">父母</option>
              <option value="子女">子女</option>
              <option value="兄弟姐妹">兄弟姐妹</option>
              <option value="其他亲属">其他亲属</option>
            </select>
            <span v-if="errors.relationship" class="text-red-500 text-xs mt-1 block">{{ errors.relationship }}</span>
          </div>
        </div>

        <div class="mt-8 flex justify-end">
          <button 
            @click="nextStep"
            class="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors duration-200 shadow-md hover:shadow-lg"
          >
            下一步
          </button>
        </div>
      </div>

      <!-- 第二步：亲属信息 -->
      <div v-if="currentStep === 2" class="space-y-6 animate-fade-in">
        <div class="flex justify-between items-center">
          <div>
            <h2 class="text-xl font-bold text-gray-800">亲属信息</h2>
            <p class="text-gray-600">每批次最多可添加3名亲属</p>
          </div>
          <button 
            @click="addVisitor"
            :disabled="formData.visitors.length >= 3"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            添加亲属
          </button>
        </div>

        <div v-for="(visitor, index) in formData.visitors" :key="index" class="border border-gray-200 rounded-lg p-5 mb-4">
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-medium text-gray-800">亲属 {{ index + 1 }}</h3>
            <button 
              @click="removeVisitor(index)"
              class="text-red-500 hover:text-red-700 transition-colors"
              :disabled="formData.visitors.length <= 1"
            >
              删除
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">姓名 <span class="text-red-500">*</span></label>
              <input
                type="text"
                v-model="visitor.name"
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors"
                placeholder="请输入亲属姓名"
                required
              />
              <span v-if="errors[`visitor_${index}_name`]" class="text-red-500 text-xs mt-1 block">{{ errors[`visitor_${index}_name`] }}</span>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">性别 <span class="text-red-500">*</span></label>
              <div class="flex space-x-4">
                <label class="inline-flex items-center">
                  <input 
                    type="radio" 
                    :name="`gender_${index}`"
                    v-model="visitor.gender" 
                    value="男"
                    class="form-radio text-primary focus:ring-primary"
                  >
                  <span class="ml-2">男</span>
                </label>
                <label class="inline-flex items-center">
                  <input 
                    type="radio" 
                    :name="`gender_${index}`"
                    v-model="visitor.gender" 
                    value="女"
                    class="form-radio text-primary focus:ring-primary"
                  >
                  <span class="ml-2">女</span>
                </label>
              </div>
              <span v-if="errors[`visitor_${index}_gender`]" class="text-red-500 text-xs mt-1 block">{{ errors[`visitor_${index}_gender`] }}</span>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">身份证号码 <span class="text-red-500">*</span></label>
              <input
                type="text"
                v-model="visitor.idCard"
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors"
                placeholder="请输入18位身份证号码"
                maxlength="18"
                required
              />
              <span v-if="errors[`visitor_${index}_idCard`]" class="text-red-500 text-xs mt-1 block">{{ errors[`visitor_${index}_idCard`] }}</span>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">联系电话 <span class="text-red-500">*</span></label>
              <input
                type="tel"
                v-model="visitor.phone"
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors"
                placeholder="请输入手机号码"
                maxlength="11"
                required
              />
              <span v-if="errors[`visitor_${index}_phone`]" class="text-red-500 text-xs mt-1 block">{{ errors[`visitor_${index}_phone`] }}</span>
            </div>

            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">与戒毒人员关系 <span class="text-red-500">*</span></label>
              <select
                v-model="visitor.relationship"
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors"
                required
              >
                <option value="">请选择关系</option>
                <option value="配偶">配偶</option>
                <option value="父母">父母</option>
                <option value="子女">子女</option>
                <option value="兄弟姐妹">兄弟姐妹</option>
                <option value="其他亲属">其他亲属</option>
              </select>
              <span v-if="errors[`visitor_${index}_relationship`]" class="text-red-500 text-xs mt-1 block">{{ errors[`visitor_${index}_relationship`] }}</span>
            </div>
          </div>
        </div>

        <div class="mt-8 flex justify-between">
          <button 
            @click="prevStep"
            class="px-6 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors duration-200"
          >
            上一步
          </button>
          <button 
            @click="nextStep"
            class="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors duration-200 shadow-md hover:shadow-lg"
          >
            下一步
          </button>
        </div>
      </div>

      <!-- 第三步：确认提交 -->
      <div v-if="currentStep === 3" class="space-y-6 animate-fade-in">
        <h2 class="text-xl font-bold text-gray-800">确认信息</h2>
        <p class="text-gray-600">请确认以下信息无误后提交</p>

        <div class="bg-gray-50 rounded-lg p-6">
          <h3 class="text-lg font-medium text-gray-800 mb-4">探访人信息</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><span class="text-gray-600">姓名：</span><span class="font-medium">{{ formData.visitorName }}</span></div>
            <div><span class="text-gray-600">性别：</span><span class="font-medium">{{ formData.gender }}</span></div>
            <div><span class="text-gray-600">身份证号：</span><span class="font-medium">{{ formData.idCard }}</span></div>
            <div><span class="text-gray-600">联系电话：</span><span class="font-medium">{{ formData.phone }}</span></div>
            <div class="md:col-span-2"><span class="text-gray-600">联系地址：</span><span class="font-medium">{{ formData.address }}</span></div>
            <div><span class="text-gray-600">戒毒人员姓名：</span><span class="font-medium">{{ formData.patientName }}</span></div>
            <div><span class="text-gray-600">与戒毒人员关系：</span><span class="font-medium">{{ formData.relationship }}</span></div>
          </div>
        </div>

        <div class="bg-gray-50 rounded-lg p-6">
          <h3 class="text-lg font-medium text-gray-800 mb-4">探访亲属信息</h3>
          <div v-for="(visitor, index) in formData.visitors" :key="index" class="mb-4 pb-4 border-b border-gray-200 last:border-0">
            <h4 class="font-medium mb-2">亲属 {{ index + 1 }}</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div><span class="text-gray-600">姓名：</span><span class="font-medium">{{ visitor.name }}</span></div>
              <div><span class="text-gray-600">性别：</span><span class="font-medium">{{ visitor.gender }}</span></div>
              <div><span class="text-gray-600">身份证号：</span><span class="font-medium">{{ visitor.idCard }}</span></div>
              <div><span class="text-gray-600">联系电话：</span><span class="font-medium">{{ visitor.phone }}</span></div>
              <div class="md:col-span-2"><span class="text-gray-600">与戒毒人员关系：</span><span class="font-medium">{{ visitor.relationship }}</span></div>
            </div>
          </div>
        </div>

        <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-blue-700">
                提交后，工作人员将在3个工作日内完成审核，请保持电话畅通，及时查收审核结果。
              </p>
            </div>
          </div>
        </div>

        <div class="mt-8 flex justify-between">
          <button 
            @click="prevStep"
            class="px-6 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors duration-200"
          >
            上一步
          </button>
          <button 
            @click="submitForm"
            :disabled="isSubmitting"
            class="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isSubmitting" class="inline-block mr-2 spinner"></span>
            提交预约
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'BookingPage',
  setup() {
    const store = useStore()
    const router = useRouter()
    const currentStep = ref(1)
    const isSubmitting = ref(false)
    const errors = reactive({})

    // 表单数据
    const formData = reactive({
      visitorName: '',
      gender: '',
      idCard: '',
      phone: '',
      address: '',
      patientName: '',
      relationship: '',
      visitors: []
    })

    // 添加亲属
    const addVisitor = () => {
      if (formData.visitors.length < 3) {
        formData.visitors.push({
          name: '',
          gender: '',
          idCard: '',
          phone: '',
          relationship: ''
        })
      }
    }

    // 删除亲属
    const removeVisitor = (index) => {
      formData.visitors.splice(index, 1)
    }

    // 验证身份证号码
    const validateIdCard = (idCard) => {
      const reg = /^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/
      return reg.test(idCard)
    }

    // 验证手机号码
    const validatePhone = (phone) => {
      const reg = /^1[3-9]\d{9}$/
      return reg.test(phone)
    }

    // 验证第一步表单
    const validateStep1 = () => {
      let isValid = true
      errors.visitorName = ''
      errors.gender = ''
      errors.idCard = ''
      errors.phone = ''
      errors.address = ''
      errors.patientName = ''
      errors.relationship = ''

      if (!formData.visitorName.trim()) {
        errors.visitorName = '请输入姓名'
        isValid = false
      }

      if (!formData.gender) {
        errors.gender = '请选择性别'
        isValid = false
      }

      if (!formData.idCard.trim()) {
        errors.idCard = '请输入身份证号码'
        isValid = false
      } else if (!validateIdCard(formData.idCard)) {
        errors.idCard = '请输入有效的身份证号码'
        isValid = false
      }

      if (!formData.phone.trim()) {
        errors.phone = '请输入联系电话'
        isValid = false
      } else if (!validatePhone(formData.phone)) {
        errors.phone = '请输入有效的手机号码'
        isValid = false
      }

      if (!formData.address.trim()) {
        errors.address = '请输入联系地址'
        isValid = false
      }

      if (!formData.patientName.trim()) {
        errors.patientName = '请输入戒毒人员姓名'
        isValid = false
      }

      if (!formData.relationship) {
        errors.relationship = '请选择与戒毒人员关系'
        isValid = false
      }

      return isValid
    }

    // 验证第二步表单
    const validateStep2 = () => {
      // 如果没有添加亲属，则验证通过
      if (formData.visitors.length === 0) {
        return true
      }
      
      let isValid = true
      
      // 清除之前的错误信息
      formData.visitors.forEach((_, index) => {
        errors[`visitor_${index}_name`] = ''
        errors[`visitor_${index}_gender`] = ''
        errors[`visitor_${index}_idCard`] = ''
        errors[`visitor_${index}_phone`] = ''
        errors[`visitor_${index}_relationship`] = ''
      })

      // 验证每个亲属信息
      formData.visitors.forEach((visitor, index) => {
        if (!visitor.name.trim()) {
          errors[`visitor_${index}_name`] = '请输入姓名'
          isValid = false
        }

        if (!visitor.gender) {
          errors[`visitor_${index}_gender`] = '请选择性别'
          isValid = false
        }

        if (!visitor.idCard.trim()) {
          errors[`visitor_${index}_idCard`] = '请输入身份证号码'
          isValid = false
        } else if (!validateIdCard(visitor.idCard)) {
          errors[`visitor_${index}_idCard`] = '请输入有效的身份证号码'
          isValid = false
        }

        if (!visitor.phone.trim()) {
          errors[`visitor_${index}_phone`] = '请输入联系电话'
          isValid = false
        } else if (!validatePhone(visitor.phone)) {
          errors[`visitor_${index}_phone`] = '请输入有效的手机号码'
          isValid = false
        }

        if (!visitor.relationship) {
          errors[`visitor_${index}_relationship`] = '请选择与戒毒人员关系'
          isValid = false
        }
      })

      return isValid
    }

    // 下一步
    const nextStep = () => {
      if (currentStep.value === 1 && validateStep1()) {
        currentStep.value = 2
        scrollToTop()
      } else if (currentStep.value === 2 && validateStep2()) {
        currentStep.value = 3
        scrollToTop()
      }
    }

    // 上一步
    const prevStep = () => {
      if (currentStep.value > 1) {
        currentStep.value--
        scrollToTop()
      }
    }

    // 滚动到顶部
    const scrollToTop = () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    }

    // 提交表单
    const submitForm = async () => {
      if (!validateStep1() || !validateStep2()) {
        return
      }

      isSubmitting.value = true

      try {
        // 检查用户是否已登录
        if (!store.state.userWxid) {
          // 实际项目中应该调用微信API获取wxid
          // 这里模拟一个wxid用于演示
          const mockWxid = `wxid_${Date.now()}`
          await store.dispatch('userLogin', mockWxid)
        }
        
        // 准备探访人（申请人）信息
        const applicantVisitor = {
          name: formData.visitorName,
          gender: formData.gender,
          idCard: formData.idCard,
          phone: formData.phone,
          relationship: formData.relationship,
          id: `visitor-${Date.now()}-applicant`
        }
        
        // 准备提交数据：包含申请人和亲属信息
        const appointmentData = {
          visitors: [
            // 首先添加申请人信息
            applicantVisitor,
            // 然后添加其他亲属信息（现在没有默认的第一个亲属）
            ...formData.visitors.map((visitor, index) => ({
              ...visitor,
              id: `visitor-${Date.now()}-${index}`
            }))
          ],
          // 添加戒毒人员信息
          patientName: formData.patientName,
          applicantAddress: formData.address
        }

        // 提交预约，包含wxid参数
        const newAppointment = await store.dispatch('createAppointment', {
          appointmentData,
          wxid: store.state.userWxid
        })
        
        // 显示成功消息
        window.showNotification('success', '预约成功', `您的预约申请已提交，将安排在${newAppointment.month}进行，请耐心等待审核结果`)
        
        // 跳转到预约列表页
        setTimeout(() => {
          router.push('/appointments')
        }, 1500)
      } catch (error) {
        console.error('提交预约失败:', error)
        window.showNotification('error', '提交失败', '请稍后重试')
      } finally {
        isSubmitting.value = false
      }
    }

    return {
      currentStep,
      formData,
      errors,
      isSubmitting,
      addVisitor,
      removeVisitor,
      nextStep,
      prevStep,
      submitForm
    }
  }
}
</script>

<style scoped>
/* 自定义样式 */
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 输入框聚焦效果增强 */
input:focus, select:focus {
  outline: none;
  ring: 2px solid #4361ee;
  border-color: #4361ee;
}

/* 表单验证错误样式 */
input.error, select.error {
  border-color: #f56565;
}
</style>