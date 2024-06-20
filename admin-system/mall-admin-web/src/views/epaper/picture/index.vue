<template>
  <div style="margin: auto;margin-top: 3%;margin-left: 5%;margin-right: 5%;">

    <el-table
      :data="list"
      v-loading="listLoading"
      border>
      <el-table-column
        fixed
        prop="fileId"
        label="ID"
      >
      </el-table-column>
      <el-table-column
        prop="title"
        label="标题"
      >
      </el-table-column>
      <el-table-column
        prop="description"
        label="内容"
      >
      </el-table-column>

      <el-table-column
        prop="updateTime"
        label="更新时间"
      >
      </el-table-column>

      <el-table-column
        prop="keyword"
        label="关键字"
      >
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
      >
        <template slot-scope="scope">
          <el-button @click="handleClick(scope.row)" type="text" size="small">查看原图</el-button>
          <el-button type="text" size="small" @click="handleCreateClick(scope.row)">预览</el-button>
          <el-button type="text" size="small" @click="handlePush(scope.row)">设置推送</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="display:flex;margin: auto;margin-top:2%;margin-left: 30%;margin-bottom: 3%; ">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        :page-count="totalPage"
        @prev-click="handlePrev"
        @next-click="handleNext"
        @current-change="handleCurrent"
      >
      </el-pagination>
    </div>
    <!--    显示原图-->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="650px;"
      center>
      <span style="margin: auto;margin-left: 2%;">{{ dialogDesc }}</span>
      <div style="display: flex;margin: auto;">
        <el-image
          style="width: 600px; height: 580px;margin: auto;"
          :src="dialogUrl"
          fit="contain"></el-image>
      </div>
      <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
  </span>
    </el-dialog>
    <!--    预览-->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogCreateVisible"
      width="650px;"
      center>
      <span style="margin: auto;margin-left: 2%;">{{ dialogDesc }}</span>
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
    <!--    设置推送-->
    <el-dialog
      title="设置推送"
      :visible.sync="dialogPushVisible"

      center>

      <div style="display: flex;margin: auto;margin-top: 5%;">
        <el-image
          style="width: 600px; height: 580px;margin: auto;"
          :src="dialogUrl"
          fit="contain"></el-image>
      </div>
      <el-divider></el-divider>
      <div style="display: flex;">
        <div style="margin: auto;">
          <span>接收者：</span>
          <el-select v-model="pushUserSetting" placeholder="请选择">
            <el-option
              v-for="item in pushUser"
              :key="item.id"
              :label="item.username"
              :value="item.id">
            </el-option>
          </el-select>
          <span>推送时间：</span>
          <el-date-picker
            v-model="pushDate"
            type="date"
            placeholder="选择日期">
          </el-date-picker>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
    <el-button plain type="primary" @click="dialogPushVisible = false">取 消</el-button>
    <el-button plain type="primary" @click="openPushUser">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>

<script>
import {getOriginalList, getOriginalPush, postOriginalPush} from "../../../api/epaper";

const defaultListQuery = {
  pageNum: 1,
  pageSize: 10,
  keyword: null
};

export default {
  name: "originalPic",
  data() {
    return {
      listQuery: Object.assign({}, defaultListQuery),
      tableData: [{
        "fileId": 26,
        "title": "我遇见你，我记得你",
        "description": "我想我会一直很爱你 ",
        "picPath": "我遇见你，我记得你___我想我会一直很爱你 .jpg",
        "updateTime": "2024-04-05T16:14:45.000+00:00",
        "keyword": null
      },],
      list: null,
      total: 1000,
      totalPage: 10, // 总页面
      pageSize: null,
      pageNum: null, //当前页
      listLoading: false,
      dialogVisible: false, // 是否显示图片
      dialogTitle: "",  // 图片的标题
      dialogDesc: "",
      dialogUrl: "",
      dialogCreateVisible: false, // 预览
      dialogPushVisible: false,   // 设置推送
      pushUser: [{
        "label": "Ymri",
        "value": 16,
      }, {
        "label": "Ymri",
        "value": 17,
      }],
      pushUserSetting: null, // 设置好的推送
      pushDate: null,
      nowRawData: null, // 推送需要使用
    }
  },
  created() {

    this.getList();
  },
  methods: {
    /**
     * 显示图片
     * @param row
     */
    handleClick(row) {
      this.dialogTitle = row.title;
      this.dialogVisible = true;
      this.dialogUrl = "http://127.0.0.1:8080/epaper/epaperOriginal/pic/" + row.fileId;
      this.dialogDesc = row.description;
    },
    /**
     * 预览
     * @param row
     */
    handleCreateClick(row) {
      this.dialogTitle = row.title;
      this.dialogCreateVisible = true;
      this.dialogUrl = "http://127.0.0.1:8080/epaper/epaperOriginal/pic/out/" + row.fileId;
      this.dialogDesc = row.description;
    },
    /**
     * 推送 设置
     * @param row
     */
    handlePush(row) {
      // console.log(row);
      this.dialogPushVisible = true;
      this.nowRawData = row;
      // 下面和预览一样的就行
      this.dialogTitle = row.title;
      this.dialogUrl = "http://127.0.0.1:8080/epaper/epaperOriginal/pic/out/" + row.fileId;
      this.dialogDesc = row.description;
      let that = this;
      getOriginalPush().then((response) => {
        let data = response.data;
        that.pushUser = data;
      })
    },
    handleResetSearch() {
      this.listQuery = Object.assign({}, defaultListQuery);
    },
    /**
     * 是否推送
     */
    openPushUser() {
      if (this.pushUserSetting == null || this.pushDate == null) {
        this.$notify.error({
          title: '错误',
          message: '请检查推送对象和推送日期！'
        });
        return;
      }
      let that = this;
      this.$confirm('此操作将覆盖原来的推送, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {

        that.postPushUser();
      }).catch((e) => {
        console.log(e);
        this.$message({
          type: 'info',
          message: '已取消更改推送!'
        });
      });

    },

    /**
     * 设置推送用户
     */
    postPushUser() {
      let postData = {
        "userId": this.pushUserSetting,
        "picId": this.nowRawData.fileId,
        "bindTime": this.pushDate
      }
      let that = this;
      postOriginalPush(postData).then((response) => {
        if (response.code == 200) {
        }
        that.$message({
          type: 'success',
          message: '更改推送成功！'
        });
        that.dialogPushVisible = false;
      }).catch((e) => {
        console.log(e);
        that.$message({
          type: 'error',
          message: '修改推送失败!'
        });
      });

    },
    /**
     * 上一页
     */
    handlePrev() {
      if (this.pageNum > 1) {
        this.listQuery.pageNum = this.pageNum - 1;
        this.getList();
      }

    },
    /**
     * 下一页
     */
    handleNext() {
      if (this.pageNum < this.totalPage) {
        this.listQuery.pageNum = this.pageNum + 1;
        this.getList();
      }

    },
    handleCurrent(page) {
      this.listQuery.pageNum = page;
      this.getList();
    },
    /**
     * 获取列表
     */
    getList() {
      this.listLoading = true;
      this.pageNum = true;
      let data = this.listQuery;
      let that = this;
      getOriginalList(data).then(response => {
        let retList = response.data;
        that.total = retList.total;
        that.pageNum = retList.pageNum;
        that.totalPage = retList.totalPage;
        that.list = retList.list;
        that.listLoading = false;
      });
    },


  },


}
</script>
<style>

</style>
