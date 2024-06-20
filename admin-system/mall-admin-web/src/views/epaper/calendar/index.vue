<template>
  <div class="con-main">

    <div class="con-list">
      <!-- 日历 -->
      <el-calendar v-model="value">
        <!-- 插槽 -->
        <template slot="dateCell" slot-scope="{date, data}">
          <!--  date   单元格代表的日期  data { type, isSelected, day}，type 表示该日期的所属月份，可选值有 prev-month，current-month，next-month；isSelected 标明该日期是否被选中；day 是格式化的日期，格式为 yyyy-MM-dd-->
          <div>
            <div>{{ data.day.split('-').slice(2).join('-') }}</div>
            <!-- 这里加了周六周天的判断 -->
            <!-- 数组循环 -->
            <div class="cell" v-for="(item,index) in userPicList">
              <!-- 加数据 -->
              <div v-if="data.day == item.date">
                ✔️
              </div>
            </div>
          </div>
        </template>
      </el-calendar>
    </div>
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogCreateVisible"
      width="650px;"
      center>
      <div style="display: flex;margin: auto;margin-top: 5%;">
        <el-image
          style="width: 600px; height: 580px;margin: auto;"
          :src="dialogUrl"
          fit="contain"></el-image>
      </div>
      <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="dialogCreateVisible = false">确 定</el-button>
  </span>
    </el-dialog>
  </div>

</template>
<script>


import {getPicList} from "../../../api/epaper";
import user from "../../../store/modules/user";

export default {
  data() {
    return {
      value: new Date(),
      now_month: null,
      dialogTitle: "查看推送",
      dialogCreateVisible: false,
      dialogUrl: null, // 推送的图片
      userPicList: [], // 用户能够看到的壁纸
    }
  },
  created() {
    this.value = new Date();

  },
  mounted() {
  },
  methods: {
    /**
     * 获取月份的推送
     * @param new_date
     */
    getCalendarList(new_date) {
      // 每次获得一个月的数据吧
      let getData = {
        "date": new_date
      };
      let that = this;
      getPicList(getData).then((response => {
        let picList = response.data;
        for (let i = 0; i < picList.length; i++) {
          let temp_date = new Date(picList[i].date);
          let year = temp_date.getFullYear();
          let month = temp_date.getMonth() + 1;
          let date = temp_date.getDate()
          if (date >= 1 && date <= 9) {//日如果小于10就补个0
            date = "0" + date;
          }
          if (month >= 1 && month <= 9) {//月如果小于10就补个0
            month = "0" + month;
          }
          picList[i]["date"] = year + '-' + month + '-' + date;
        }
        that.userPicList = picList;
        that.showPic(new_date);
      }))
    },
    showPic(date) {
      for (let i = 0; i < this.userPicList.length; i++) {
        // 显示这天的内容
        if (date == this.userPicList[i].date) {
          this.dialogCreateVisible = true;
          let file = this.userPicList[i]["file"];
          if (this.userPicList[i].userId != 0) {
            file = this.userPicList[i].userId + "_" + file;
          }
          this.dialogUrl = "http://127.0.0.1:8080/epaper/epaperOriginal/pic/user/" + file;
        }
      }
    }
  },
  watch: {
    value: function () {
      var year = this.value.getFullYear();
      var month = this.value.getMonth() + 1;
      var date = this.value.getDate()
      if (date >= 1 && date <= 9) {//日如果小于10就补个0
        date = "0" + date;
      }
      if (month >= 1 && month <= 9) {//月如果小于10就补个0
        month = "0" + month;
      }
      console.log(year + '-' + month + '-' + date) // 打印出日历选中了哪年哪月'=
      let new_date = year + '-' + month + '-' + date;
      if (year + '-' + month == this.now_month) {
        this.showPic(new_date);
        return;
      }
      this.now_month = year + '-' + month;
      this.getCalendarList(new_date);
    }
  },
}
</script>

<style lang="scss" scoped>
div ::v-deep th.gutter {
  display: initial;
}

div ::v-deep .el-calendar-day {
  min-height: 110px;
  height: inherit !important;
  position: relative;
  z-index: inherit;
}

.bgcolor {
  padding: 2px;
  text-align: center;
  background-color: rgba(173, 221, 225, 0.63);
  color: #5a9cf8;
}
</style>
