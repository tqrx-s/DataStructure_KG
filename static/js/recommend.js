function recommend(userId) {
    $.getJSON('/recommend_Id', {
        userId: userId,
    }, function (ans) {
        $('#recommend_results').empty();
        console.log("333");
        // 遍历数组，将每个节点的内容添加到页面上
        ans.forEach(function (res) {
            // var $resultElement = $('<div>').text(ans); // 每个结果是一个字符串
            // $('#recommend_results').append('<tr><td>' + $resultElement + '<tr><td>');
            $('#recommend_results').append('<tr><td>' + res + '<tr><td>');
        });
    });
}