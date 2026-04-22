window.onresize = function () {

    myChart.resize();
}
$.ajaxSetup({async: false});
// 基于准备好的容器(这里的容器是id为myChart的div)，初始化echarts实例
var myChart = echarts.init(document.getElementById("guanxi"));
myChart.showLoading();

myChart.hideLoading();

option = {
    // backgroundColor: "white",        // 背景颜色
    title: {                            //图表标题
        // text: '知识图谱',                  // 标题文本
        textStyle: {                        // 标题样式
            // color: "white",                    // 标题字体颜色
            fontWeight: "lighter",                // 定义更细的字符
        }
    },
    animationDurationUpdate: false,              // 数据更新动画的时长。[ default: 300 ]
    animationEasingUpdate: false,      // 数据更新动画的缓动效果。[ default: cubicOut ] quinticInOut
    legend: {                              //图表控件
        x: "center",
        show: true, //默认显示
        data: ["一级概念", "二级概念", "三级概念", "四级概念", "五级概念", "六级概念"]
    },
    series: [
        {
            type: 'graph',                          // 关系图
            layout: 'force',                        // 布局
            legendHoverLink : true,                 //是否启用图例 hover(悬停) 时的联动高亮。
            symbolSize: 30,                         //节点大小
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 4],
            edgeLabel: {
                normal: {
                    show: true,
                    textStyle: {
                        fontSize: 10
                    },
                    formatter: "{c}"
                }
            },
            force: {
                repulsion: 800,        // [ default: 50 ]节点之间的斥力因子(关系对象之间的距离)。支持设置成数组表达斥力的范围，此时不同大小的值会线性映射到不同的斥力。值越大则斥力越大
                edgeLength: [10, 100],   // [ default: 30 ]边的两个节点之间的距离(关系对象连接线两端对象的距离,会根据关系对象值得大小来判断距离的大小)，
                layoutAnimation: true,  //因为力引导布局会在多次迭代后才会稳定，这个参数决定是否显示布局的迭代动画，在浏览器端节点数据较多（>100）的时候不建议关闭，布局过程会造成浏览器假死。
                // gravity:0.1
            },
            focusNodeAdjacency: true,   // 是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点。[ default: false ]
            draggable: true,
            roam: true,                 // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            categories: [{               // 节点分类的类目，可选
                name: '一级概念',               // 类目名称，用于和 legend 对应以及格式化 tooltip 的内容。
                // itemStyle: {
                //     normal: {
                //         color: "#009800",
                //     }
                // }
            }, {
                name: '二级概念',
            }, {
                name: '三级概念',
            }, {
                name: '四级概念',
            }, {
                name: '五级概念',
            }, {
                name: '六级概念',
            },
            ],
            label: {        // 关系对象上的标签
                normal: {
                    show: true,             // 显示标签
                    position: "right",     // 标签位置
                    textStyle: {              // 文本样式
                        fontSize: 20
                    },
                }
            },
            tooltip: {              // 提示框配置
                trigger:'item',
                formatter: function (node) { // 区分连线和节点，节点上额外显示其他数字
                    if (!node.value) {
                        return node.data.name;
                    } else {
                        return node.data.name + ":" + node.data.showNum;
                    }
                },
                extraCssText:'z-index: 0'
            },
            lineStyle: {
                normal: {
                    opacity: 0.9,
                    width: 1,
                    curveness: 0,  // 边的曲度
                    color:"target"
                }
            },
            // progressiveThreshold: 700,
            nodes: [
              {
                name: '教师表情',
                category: 0,//设置节点所属类别
              },
              {
                name: '学生表情',
                category: 0,//设置节点所属类别
              },
              {
                name: '教师行为',
                category: 0,//设置节点所属类别
              },
              {
                name: '提问同学',
                category: 1,//设置节点所属类别
              },
              {
                name: '双手比划',
                category: 1,//设置节点所属类别
              },
              {
                name: '写板书',
                category: 1,//设置节点所属类别
              },
              {
                name: '来回走动',
                category: 1,//设置节点所属类别
              },
              {
                name: '授课',
                category: 1,//设置节点所属类别
              },
              {
                name: '课件展示',
                category: 1,//设置节点所属类别
              },
              {
                name: '引导讨论',
                category: 1,//设置节点所属类别
              },
              {
                name: '巡视教室',
                category: 1,//设置节点所属类别
              },
              {
                name: '观察学生',
                category: 1,//设置节点所属类别
              },
              {
                name: '其他',
                category: 1,//设置节点所属类别
              },
              {
                name: '语言表达',
                category: 2,//设置节点所属类别
              },
              {
                name: '课堂互动',
                category: 2,//设置节点所属类别
              },
              {
                name: '课堂管理',
                category: 2,//设置节点所属类别
              },
              {
                name: '强调纪律',
                category: 2,//设置节点所属类别
              },
              {
                name: '教学设计',
                category: 3,//设置节点所属类别
              },
              {
                name: '课程内容',
                category: 3,//设置节点所属类别
              },
              {
                name: '学生行为',
                category: 0,//设置节点所属类别
              },
              {
                name: '挠头',
                category: 1,//设置节点所属类别
              },
              {
                name: '举手',
                category: 1,//设置节点所属类别
              },
              {
                name: '站立',
                category: 1,//设置节点所属类别
              },
              {
                name: '低头',
                category: 1,//设置节点所属类别
              },
              {
                name: '交头接耳',
                category: 1,//设置节点所属类别
              },
              {
                name: '趴桌子',
                category: 1,//设置节点所属类别
              },
              {
                name: '看手机',
                category: 1,//设置节点所属类别
              },
              {
                name: '认真听讲',
                category: 1,//设置节点所属类别
              },
              {
                name: '注视黑板',
                category: 1,//设置节点所属类别
              },
              {
                name: '语气态度',
                category: 2,//设置节点所属类别
              },
              {
                name: '上课姿态',
                category: 2,//设置节点所属类别
              },
              {
                name: '无法集中',
                category: 3,//设置节点所属类别
              },
              {
                name: '缺少兴趣',
                category: 3,//设置节点所属类别
              },
              {
                name: '积极回应',
                category: 3,//设置节点所属类别
              },
              {
                name: '生气',
                category: 4,//设置节点所属类别
              },
              {
                name: '厌恶',
                category: 4,//设置节点所属类别
              },
              {
                name: '恐惧',
                category: 4,//设置节点所属类别
              },
              {
                name: '高兴',
                category: 4,//设置节点所属类别
              },
              {
                name: '中性',
                category: 4,//设置节点所属类别
              },
              {
                name: '悲伤',
                category: 4,//设置节点所属类别
              },
              {
                name: '惊喜',
                category: 4,//设置节点所属类别
              },
            ],
            links: [
              {
                source: '教师行为',//源节点
                target: '学生行为',//目标节点
                value: '相关',//关系
              },
              {
                source: '教师行为',//源节点
                target: '教师表情',//目标节点
                value: '相关',//关系
              },
              {
                source: '学生行为',//源节点
                target: '学生表情',//目标节点
                value: '相关',//关系
              },
              {
                source: '教师行为',//源节点
                target: '提问同学',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '双手比划',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '写板书',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '来回走动',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '授课',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '课件展示',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '引导讨论',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '巡视教室',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '观察学生',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '语言表达',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '课堂管理',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '课堂互动',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '强调纪律',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '教学设计',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '课程内容',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师行为',//源节点
                target: '其他',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '挠头',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '举手',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '站立',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '低头',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '交头接耳',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '趴桌子',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '看手机',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '认真听讲',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '注视黑板',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '语气态度',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '上课姿态',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '无法集中',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '缺少兴趣',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生行为',//源节点
                target: '积极回应',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师表情',//源节点
                target: '生气',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师表情',//源节点
                target: '厌恶',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师表情',//源节点
                target: '恐惧',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师表情',//源节点
                target: '高兴',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师表情',//源节点
                target: '中性',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师表情',//源节点
                target: '悲伤',//目标节点
                value: '包括',//关系
              },
              {
                source: '教师表情',//源节点
                target: '惊喜',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生表情',//源节点
                target: '生气',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生表情',//源节点
                target: '厌恶',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生表情',//源节点
                target: '恐惧',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生表情',//源节点
                target: '高兴',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生表情',//源节点
                target: '中性',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生表情',//源节点
                target: '悲伤',//目标节点
                value: '包括',//关系
              },
              {
                source: '学生表情',//源节点
                target: '惊喜',//目标节点
                value: '包括',//关系
              },
            ],
        }
    ]
};
