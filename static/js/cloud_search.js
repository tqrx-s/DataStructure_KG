function search(name) {
    // 深拷贝
    temp_option = JSON.parse(JSON.stringify(option));
    temp_node_name=[];
    temp_node_name = option.series[0].links.map(link=>{
        if(link.source==name)
            return link.target;
        else if(link.target==name)
            return link.source;
    });
    temp_node_name.push(name);
    temp_node=[];
    temp_node=option.series[0].nodes.map(nodeA=>{
        match = temp_node_name.find(nodeB => nodeB == nodeA.name);
        return match ? nodeA : null;
    });
    // 过滤null
    fileter_node = [];
    for(const key in temp_node)
    {
        if(temp_node[key]!=null)
            fileter_node.push(temp_node[key]);
    }
    console.log(fileter_node);
    temp_option.series[0].nodes = fileter_node;
    myChart.setOption(temp_option, true);
}

function search_path(nameA, nameB) {
    // 深拷贝
    temp_option = JSON.parse(JSON.stringify(option));
    temp_node_name=[];
    temp_node_name.push('教师行为');
    temp_node_name.push('学生行为');
    temp_node_name.push(nameA);
    temp_node_name.push(nameB);
    temp_node=[];
    temp_node=option.series[0].nodes.map(nodeA=>{
        match = temp_node_name.find(nodeB => nodeB == nodeA.name);
        return match ? nodeA : null;
    });
    // 过滤null
    fileter_node = [];
    for(const key in temp_node)
    {
        if(temp_node[key]!=null)
            fileter_node.push(temp_node[key]);
    }
    temp_option.series[0].nodes = fileter_node;
    myChart.setOption(temp_option, true);
}