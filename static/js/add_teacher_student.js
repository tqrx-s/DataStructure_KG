const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

const cors = require("cors");

// 中间件
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public')); // 用于服务静态文件
app.use(cors());

// 处理 POST 请求
app.post('/add', (req, res) => {
    console.log('进入add函数！');
    const { character, action, relation, level } = req.body;
    
    // 生成要写入的文本内容
    const content = `Character: ${character}, Action: ${action}, Relation: ${relation}, Level: ${level}\n`;

    // 写入 TXT 文件
    console.log('路径为：',__dirname);
    fs.appendFile(path.join(__dirname, 'data.txt'), content, (err) => {
        if (err) {
            console.error('写入文件时出错:', err);
            return res.status(500).send('服务器错误');
        }
        console.log('成功处理要求！');
        res.send('数据已提交');
    });
});

// 启动服务器
app.listen(PORT, () => {
    console.log(`服务器正在运行，端口 ${PORT}`);
});
