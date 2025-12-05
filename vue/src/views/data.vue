<template>
  <div style="width:calc(200vh - 286px);">
    <el-card style="display: flex;">
        <el-date-picker v-model="data.date" type="date" placeholder="请选择要查询的日期" value-format="YYYY/MM/DD"/>
        <el-button style="margin-left: 30px" type="warning" @click="load">查询</el-button>
        <el-button style="margin-left: 30px" type="primary" @click="AiAnalysis">AI分析</el-button>
        <el-button style="margin-left: 30px" type="success" @click="reset">重置</el-button>
    </el-card>
    <div>
      <el-card style="display: flex;">
        <el-table :data="data.tableData" style="width:calc(200vh - 286px)" stripe>
          <el-table-column label="数据编号" prop="dataID" />
          <el-table-column label="用户编号" prop="userID" />
          <el-table-column label="年" prop="year" />
          <el-table-column label="月" prop="month"/>
          <el-table-column label="日" prop="day" />
          <el-table-column label="雷达检测心率" prop="bpm_rader"/>
          <el-table-column label="血氧检测心率" prop="bpm_finger"/>
        </el-table>
        <div style="margin-top: 10px;">
          <el-pagination
              @size-change="load"
              @current-change="load"
              v-model:current-page="data.pageNum"
              v-model:page-size="data.pageSize"
              :page-sizes="[5, 10, 15, 20]"
              background
              layout="total, sizes, prev, pager, next, jumper"
              :total=data.total
          />
        </div>
      </el-card>
      <el-card style="display: flex;">
        <span v-html="renderMarkdown(data.AiData)"></span>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import {reactive, ref} from "vue";
import request from "@/utils/request.js"
import { marked } from 'marked'
const data = reactive({
  date:'',
  pageNum:1,
  pageSize:10,
  total:0,
  tableData:[],
  AiData:''
})

const load = () => {
  request.get('/heartdata/selectPage',{
    params:{
      pageNum:data.pageNum,
      pageSize:data.pageSize,
      date: data.date
    }
  }).then(res => {
    data.tableData = res.data.list;
    data.total = res.data.total;
  })
}

const AiAnalysis = () => {
  const dateParam = data.date;
  const url = `http://localhost:8081/ai/chat?date=${encodeURIComponent(dateParam)}`;
  data.AiData='';
  const eventSource = new EventSource(url)

  eventSource.onmessage =  (event) =>{
    console.log(event.data);
    data.AiData += event.data;
  }

  eventSource.onerror = (error) => {
    eventSource.close();
  };


}

const renderMarkdown = (content) => {
  return marked(content);
}

const reset = () =>{
  data.date = '';
  data.AiData='';
  data.tableData=null;
}

</script>

<style scoped>

</style>