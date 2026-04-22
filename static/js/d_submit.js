function search(name) {
        // 深拷贝
        temp_option = JSON.parse(JSON.stringify(option));
        temp_node_name=[];
        temp_node_name = option.series[0].links.map(link=>{
            if(link.source==name)
                return link.target;
        });
        temp_node_name.push(name);
        temp_node=[];
        temp_node=option.series[0].nodes.map(nodeA=>{
            match = temp_node_name.find(nodeB => nodeB == nodeA.name);
            return match ? nodeA : null;
        });
        fileter_node = [];
        for(key in temp_node)
        {
            if(temp_node[key]!=null)
                fileter_node.push(temp_node[key]);
        }
        temp_option.series[0].nodes = fileter_node;
        console.log(temp_option.series[0].nodes);
        console.log(option.series[0].nodes);
        // temp_option.series[0].nodes.pop(null);
        myChart.setOption(temp_option, true);
}