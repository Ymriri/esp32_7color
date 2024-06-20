<template>
  <div style="margin: auto">
    <div style="margin-top:5%; "></div>
    <el-descriptions class="margin-top" style="margin-left:5%;margin-right: 5%; " title="设置日历基本信息" :column="3"
                     border :model="userInfo">
      <template slot="extra">
        <el-button type="primary" @click="changeUserInfo" size="small">修改</el-button>

      </template>
      <el-descriptions-item>
        <template slot="label">
          <i class="el-icon-user"></i>
          用户名称
        </template>
        <el-input v-model="userInfo.umsUserId" :disabled="true"></el-input>
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label">
          <i class="el-icon-mobile-phone"></i>
          WIFI-名称（SSID）
        </template>
        <el-input v-model="userInfo.wifiSsid" :disabled="changeFlag"></el-input>
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label">
          <i class="el-icon-mobile-phone"></i>
          WIFI-密码
        </template>
        <el-input v-model="userInfo.wifiPassword" :disabled="changeFlag"></el-input>
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label">
          <i class="el-icon-location-outline"></i>
          所在地
        </template>
        <el-input v-model="userInfo.urban" :disabled="changeFlag"></el-input>
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label">
          <i class="el-icon-tickets"></i>
          上次更新时间
        </template>
        <el-input v-model="userInfo.updateTime" :disabled="changeFlag"></el-input>
      </el-descriptions-item>
    </el-descriptions>
    <div style="margin: auto;margin-left: 45%;margin-top: 5%;">
      <el-button type="primary" v-if="!changeFlag" @click="showDia" size="medium">确定</el-button>
    </div>
    <el-dialog
      title="确定提示"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <span>确定修改信息？ 从第二天开始按照新配置更新 ！</span>
      <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="saveUserInfo">确 定</el-button>
  </span>
    </el-dialog>

  </div>
</template>

<script>
// 添加
import {getEpaperSetting, updateEpaperUserSettting} from "../../../api/epaper";


export default {
  name: 'epaperSettting',
  data() {
    return {
      size: '',
      userInfo: {
        "epaperUid": 0,
        "umsUserId": 0,
        "updateTime": "2024-04-06T10:10:30.000+00:00",
        "urban": "101280101",
        "wifiPassword": "***",
        "wifiSsid": "408408"
      },
      changeFlag: true,
      dialogVisible: false
    };
  },
  created() {
    this.getEpaperSetting();
  },
  methods: {

    getEpaperSetting() {
      let that = this;
      getEpaperSetting().then(response => {
        let epaperSetting = response.data;
        that.userInfo = epaperSetting;
      });
    },
    changeUserInfo() {
      this.changeFlag = false;
    },
    showDia() {
      this.dialogVisible = true;
    },
    saveUserInfo() {
      let that = this;
      this.dialogVisible = false;
      updateEpaperUserSettting(this.userInfo).then(response=>{
        if(response.code==200){
          that.$message({
            message: '更新成功！',
            type: 'success'
          })
        }
      })
      // 提交结果
      this.changeFlag = true;
    },
    handleClose(done) {
      let that = this;
      this.$confirm('确认关闭？')
        .then(_ => {
          done();

        })
        .catch(_ => {
        });
    }
  }

}
</script>

<style scoped>

</style>
