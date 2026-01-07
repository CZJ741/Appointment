<template>
  <!-- 用户须知弹窗 -->
  <div v-if="showNoticeDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75 p-4 notice-dialog">
    <div class="bg-white rounded-xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-hidden">
      <!-- 弹窗标题 -->
      <div class="bg-primary text-white px-6 py-4 flex justify-between items-center">
        <h2 class="text-xl font-bold">探访须知</h2>
      </div>
      
      <!-- 弹窗内容 -->
      <div class="px-6 py-4 max-h-[60vh] overflow-y-auto">
        <h3 class="text-lg font-medium text-gray-800 mb-4">探访须知</h3>
        
        <p class="text-gray-700 mb-4">尊敬的戒毒人员家属：</p>
        <p class="text-gray-700 mb-4">为保障戒毒人员的合法权益，维护戒毒所正常管理秩序，营造安全、规范、有序的探访环境，确保探访活动顺利进行，请您在预约探访前仔细阅读并遵守以下须知：</p>
        
        <h4 class="text-md font-medium text-gray-800 mt-6 mb-3">一、探访资格与手续</h4>
        <ul class="list-disc list-inside space-y-2 text-gray-700 mb-4">
          <li>探访对象：原则上仅限于戒毒人员的直系亲属（配偶、父母、子女、同胞兄弟姐妹）及监护人。其他关系人申请探访，需经所政管理科严格审核批准。</li>
          <li>身份证明：探访时，请携带本人有效身份证件（身份证、户口簿等）以及能证明与戒毒人员亲属关系的材料（如户口簿、结婚证、出生医学证明、派出所出具的亲属关系证明等）。</li>
          <li>申请流程：请按照戒毒所通知或规定的预约方式（如现场预约、线上平台预约等）提前办理探访申请。</li>
        </ul>
        
        <h4 class="text-md font-medium text-gray-800 mt-6 mb-3">二、探访时间与安排</h4>
        <ul class="list-disc list-inside space-y-2 text-gray-700 mb-4">
          <li>探访时间：我所探访时间为每月第三周的周三（具体请查询我所公众号发布的时间安排信息），上午8:30至11:30，下午14:30至16:00。</li>
          <li>时长与频率：每次探访时间原则上不超过20分钟。每月探访次数不超过1次。具体安排可能根据管理需要、场所实际情况或特殊时期要求进行调整，请予以理解配合。</li>
          <li>服从安排：请严格按照预约时间到达，听从民警指引，在指定区域等候和进行探访。探访结束时间到，请自觉离开。</li>
        </ul>
        
        <h4 class="text-md font-medium text-gray-800 mt-6 mb-3">三、探访纪律与要求</h4>
        <ul class="list-disc list-inside space-y-2 text-gray-700 mb-4">
          <li>遵守法规：探访期间，请自觉遵守国家法律法规及戒毒所的各项管理规定。</li>
          <li>接受安检：所有探访人员及携带物品必须接受安全检查。严禁携带任何违禁品、危险品（如刀具、绳索、火种、玻璃制品等）、通讯工具（手机、智能手表等）、录音录像设备、现金、贵重物品以及其他未经许可的物品进入探访区域。</li>
          <li>交谈规范：探访交谈内容应健康、积极，有利于戒毒人员思想稳定和戒治康复。严禁谈论有碍戒治管理、涉及案件或其他不当内容；严禁使用暗语、隐语或外语（必要翻译除外）交流；严禁大声喧哗、争吵或有其他影响秩序的行为。</li>
          <li>传递物品：不允许私自传递任何物品。确需为戒毒人员转交必要的生活、学习用品（限于书籍、照片、书信，且需符合规定），必须经民警检查、登记并统一转交。食品、药品、衣物等严格禁止。</li>
          <li>行为举止：请保持探访区域整洁，爱护公物。探访时请注意言行举止，着装得体。未经许可，不得在探访区内拍照、摄像。不得携带宠物进入探访区域。</li>
          <li>特殊情况：如遇戒毒人员正在接受治疗、参加重要戒治活动或处于隔离审查等特殊情况，探访可能被暂停或取消，敬请谅解。</li>
        </ul>
        
        <h4 class="text-md font-medium text-gray-800 mt-6 mb-3">四、其他注意事项</h4>
        <ul class="list-disc list-inside space-y-2 text-gray-700 mb-4">
          <li>健康告知：如您本人有传染病或身体不适，请暂缓探访，或主动向民警说明情况。</li>
          <li>配合管理：请尊重并配合值班民警的管理和指挥。如有疑问或需要帮助，可向现场民警咨询。</li>
          <li>责任自负：违反本须知规定者，民警有权立即中止探访，情节严重者将依法追究责任，并可能影响后续探访资格。</li>
          <li>信息变更：探访政策如有调整，将以戒毒所官方通知为准。</li>
        </ul>
        
        <h4 class="text-md font-medium text-gray-800 mt-6 mb-3">五、沟通与联系</h4>
        <p class="text-gray-700 mb-4">家属的支持与配合是戒毒工作的重要力量。我们鼓励家属通过正规渠道，积极配合戒毒所开展帮教工作。如需了解戒毒人员的戒治表现、政策咨询等，请在通过0713-8880121在工作时间与我所所政管理科联系。</p>
        <p class="text-gray-700 mb-6">感谢各位家属的理解、支持与配合！让我们共同努力，帮助戒毒人员坚定信心，早日戒除毒瘾，回归家庭和社会！</p>
        
        <div class="text-right text-gray-600 mt-8">
          <p>黄冈市强制隔离戒毒所</p>
          <p>所政管理科</p>
          <p>2026年1月7日</p>
        </div>
      </div>
      
      <!-- 弹窗底部 -->
      <div class="bg-gray-50 px-6 py-4 flex justify-between items-center border-t border-gray-200">
        <div v-if="!isCountdownComplete" class="text-gray-600">
          请仔细阅读以上内容（{{ countdown }}秒）
        </div>
        <div v-else class="text-green-600 font-medium">
          阅读完成
        </div>
        <button 
          @click="closeNoticeDialog"
          :disabled="!isCountdownComplete"
          class="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          我已阅读并同意
        </button>
      </div>
    </div>
  </div>
  
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
          <span class="text-sm font-medium">预约信息</span>
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
          <span class="text-sm font-medium">确认提交</span>
        </div>
      </div>

      <!-- 第一步：预约信息 -->
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
          <option value="朋友">朋友</option>
        </select>
        <span v-if="errors.relationship" class="text-red-500 text-xs mt-1 block">{{ errors.relationship }}</span>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">探访日 <span class="text-red-500">*</span></label>
        <select
          v-model="formData.visitDate"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors"
          required
        >
          <option value="">请选择探访日</option>
          <option v-for="date in filteredVisitDates" :key="date.value" :value="date.value">
            {{ date.label }} (已有{{ getBatchCount(date.value) }}次预约)
            
          </option>
        </select>
        <span v-if="errors.visitDate" class="text-red-500 text-xs mt-1 block">{{ errors.visitDate }}</span>
      </div>

      <div class="md:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">预约原因及期望探访时间备注 <span class="text-red-500">*</span></label>
          <textarea
            v-model="formData.appointmentReason"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors"
            placeholder="请写明探访原因和抵达戒毒所时间 如：关心近况，2025-12-01 10:00 抵达戒毒所 期望10：00进行探访 (实际探访时间段以管理员分配为准,请及时登录系统查看分配结果） "
            rows="3"
            required
          ></textarea>
          <span v-if="errors.appointmentReason" class="text-red-500 text-xs mt-1 block">{{ errors.appointmentReason }}</span>
        </div>
        </div>

        <!-- 分割线 -->
        <div class="border-t border-gray-200 my-8"></div>

        <!-- 随行人员信息 -->
        <div class="mt-6">
          <div class="flex justify-between items-center mb-4">
            <div>
              <h2 class="text-xl font-bold text-gray-800">随行人员信息</h2>
              <p class="text-gray-600">每批次最多可添加2名随行人员</p>
            </div>
            <button 
              @click="addVisitor"
              :disabled="formData.visitors.length >= 2"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              添加随行人员
            </button>
          </div>

          <div v-for="(visitor, index) in formData.visitors" :key="index" class="border border-gray-200 rounded-lg p-6 mb-5 shadow-sm hover:shadow-md transition-shadow duration-200 bg-white">
            <div class="flex justify-between items-center mb-4">
              <h3 class="font-medium text-gray-800">随行人员 {{ index + 1 }}</h3>
              <button 
                @click="removeVisitor(index)"
                class="px-3 py-1 text-sm bg-red-50 text-red-600 rounded-md hover:bg-red-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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
                  placeholder="请输入随行人员姓名"
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
                  <option value="朋友">朋友</option>
                </select>
                <span v-if="errors[`visitor_${index}_relationship`]" class="text-red-500 text-xs mt-1 block">{{ errors[`visitor_${index}_relationship`] }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-12 flex justify-end">
          <button 
            @click="nextStep"
            class="px-6 py-3 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors duration-200 shadow-md hover:shadow-lg font-medium"
          >
            下一步
          </button>
        </div>
      </div>

      <!-- 第二步：确认提交 -->
      <div v-if="currentStep === 2" class="space-y-6 animate-fade-in">
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
            <div><span class="text-gray-600">探访日：</span><span class="font-medium">{{ formData.visitDate }}</span></div>
            <div class="md:col-span-2"><span class="text-gray-600">预约原因及备注：</span><span class="font-medium">{{ formData.appointmentReason }}</span></div>
          </div>
        </div>

        <div class="bg-gray-50 rounded-lg p-6">
          <h3 class="text-lg font-medium text-gray-800 mb-4">探访随行人员信息</h3>
          <div v-for="(visitor, index) in formData.visitors" :key="index" class="mb-4 pb-4 border-b border-gray-200 last:border-0">
            <h4 class="font-medium mb-2">随行人员 {{ index + 1 }}</h4>
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
                提交后，工作人员将在5个工作日内完成审核，请保持电话畅通，并请在临近探访日前及时登录系统，查看审核结果。
              </p>
            </div>
          </div>
        </div>

        <div class="mt-12 flex justify-between">
          <button 
            @click="prevStep"
            class="px-6 py-3 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors duration-200 font-medium"
          >
            上一步
          </button>
          <button 
            @click="submitForm"
            :disabled="isSubmitting"
            class="px-6 py-3 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed font-medium"
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'BookingPage',
  setup() {
    const store = useStore()
    const router = useRouter()
    const currentStep = ref(1)
    const isSubmitting = ref(false)
    const errors = reactive({
      appointmentReason: '' 
    })

    // 用户须知弹窗状态
    const showNoticeDialog = ref(true)
    const countdown = ref(5)
    const isCountdownComplete = ref(false)
    let countdownTimer = null

    // 探访日批次数统计
    const visitDateStats = ref({})

    // 页面加载时初始化数据
    onMounted(async () => {
      await loadVisitDateStats()
      
      // 启动用户须知倒计时
      startCountdown()
    })

    // 启动倒计时
    const startCountdown = () => {
      countdownTimer = setInterval(() => {
        if (countdown.value > 0) {
          countdown.value--
        } else {
          clearInterval(countdownTimer)
          isCountdownComplete.value = true
        }
      }, 1000)
    }

    // 关闭用户须知弹窗
    const closeNoticeDialog = () => {
      if (isCountdownComplete.value) {
        showNoticeDialog.value = false
      }
    }

    // 加载探访日批次数统计
    const loadVisitDateStats = async () => {
      try {
        const response = await axios.get('/appointment/visit-date-stats/')
        visitDateStats.value = response.data
      } catch (error) {
        console.error('加载探访日统计失败:', error)
      }
    }

    // 探访日列表（2026年）
    const visitDates = [
      { value: '2026-01-14', label: '2026年1月14日' },
      { value: '2026-02-10', label: '2026年2月10日' },
      { value: '2026-03-18', label: '2026年3月18日' },
      { value: '2026-04-15', label: '2026年4月15日' },
      { value: '2026-05-13', label: '2026年5月13日' },
      { value: '2026-06-17', label: '2026年6月17日' },
      { value: '2026-07-15', label: '2026年7月15日' },
      { value: '2026-08-12', label: '2026年8月12日' },
      { value: '2026-09-16', label: '2026年9月16日' },
      { value: '2026-10-14', label: '2026年10月14日' },
      { value: '2026-11-18', label: '2026年11月18日' },
      { value: '2026-12-16', label: '2026年12月16日' }
    ]

    // 过滤掉已过期的探访日
    const filteredVisitDates = computed(() => {
      const today = new Date()
      // 将今天的时间设置为00:00:00，确保只比较日期部分
      today.setHours(0, 0, 0, 0)
      
      return visitDates.filter(date => {
        const visitDate = new Date(date.value)
        // 设置探访日时间为00:00:00，确保只比较日期部分
        visitDate.setHours(0, 0, 0, 0)
        return visitDate >= today
      })
    })

    // 计算每个探访日已预约的批次数
    const getBatchCount = (visitDate) => {
      return visitDateStats.value[visitDate] || 0
    }

    // 表单数据
    const formData = reactive({
      visitorName: '',
      gender: '',
      idCard: '',
      phone: '',
      address: '',
      patientName: '',
      relationship: '',
      visitDate: '', // 添加探访日字段
      appointmentReason: '', // 添加预约原因字段
      visitors: []
    })

    // 添加随行人员
    const addVisitor = () => {
      if (formData.visitors.length < 2) {
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
      errors.visitDate = ''
      errors.appointmentReason = ''

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
      
      if (!formData.appointmentReason.trim()) {
        errors.appointmentReason = '请输入预约原因'
        isValid = false
      }

      if (!formData.visitDate) {
        errors.visitDate = '请选择探访日'
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
      if (currentStep.value === 1 && validateStep1() && validateStep2()) {
        currentStep.value = 2
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
        // 确保用户已登录（使用用户名密码系统）
        if (!store.getters.isUserLoggedInByUsername) {
          window.showNotification('error', '登录失败', '请先登录后再预约')
          router.push('/login')
          isSubmitting.value = false
          return
        }
        
        // 准备提交数据：转换为后端期望的格式和字段名
        const appointmentData = {
          // 主访客人信息（使用下划线命名）
          visitor_name: formData.visitorName,
          visitor_gender: formData.gender,
          visitor_id_card: formData.idCard,
          visitor_phone: formData.phone,
          visitor_address: formData.address,
          
          // 戒毒人员信息
          prisoner_name: formData.patientName,
          relationship: formData.relationship,
          
          // 探访日
          visit_date: formData.visitDate,
          
          // 使用用户输入的预约原因
        appointment_reason: formData.appointmentReason,
          
          // 转换亲属信息（如果有）
          relatives: formData.visitors.map(visitor => ({
            name: visitor.name,
            gender: visitor.gender,
            id_card: visitor.idCard, // 转换为下划线命名
            phone: visitor.phone,
            relationship: visitor.relationship
          }))
        }

        // 提交预约
        const newAppointment = await store.dispatch('createAppointment', appointmentData)
        
        // 显示成功消息
        window.showNotification('success', '预约成功', `您的预约申请已提交，请耐心等待审核结果`)
        
        // 跳转到预约列表页
        setTimeout(() => {
          router.push('/appointments')
        }, 1500)
      } catch (error) {
        console.error('提交预约失败:', error)
        // 显示API返回的具体错误信息，如果有的话
        const errorMessage = error.response?.data?.detail || error || '请稍后重试'
        window.showNotification('error', '提交失败', errorMessage)
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
      submitForm,
      filteredVisitDates,
      getBatchCount,
      // 用户须知相关
      showNoticeDialog,
      countdown,
      isCountdownComplete,
      closeNoticeDialog
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
  box-shadow: 0 0 0 2px #4361ee;
  border-color: #4361ee;
}

/* 表单验证错误样式 */
input.error, select.error {
  border-color: #f56565;
}

/* 用户须知弹窗样式优化 */
.notice-dialog-enter-active {
  animation: noticeFadeIn 0.3s ease-out;
}

.notice-dialog-leave-active {
  animation: noticeFadeOut 0.3s ease-in;
}

@keyframes noticeFadeIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes noticeFadeOut {
  from { opacity: 1; transform: scale(1); }
  to { opacity: 0; transform: scale(0.9); }
}

/* 弹窗内容滚动条美化 */
.max-h\[60vh\]::-webkit-scrollbar {
  width: 8px;
}

.max-h\[60vh\]::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.max-h\[60vh\]::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.max-h\[60vh\]::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* 弹窗内容段落间距优化 */
.max-h\[60vh\] h3 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #2d3748;
  font-size: 1.125rem;
  font-weight: 600;
}

.max-h\[60vh\] ol {
  margin-left: 1rem;
  padding-left: 1rem;
}

.max-h\[60vh\] li {
  margin-bottom: 0.75rem;
  line-height: 1.6;
  color: #4a5568;
}

/* 弹窗按钮样式增强 */
.bg-primary:hover {
  background-color: #3b5bdb;
  box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
}
</style>