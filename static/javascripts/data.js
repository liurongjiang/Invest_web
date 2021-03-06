var language = {
    "emptyTable": "没有数据",
    "loadingRecords": "加载中...",
    "processing": "查询中...",
    "search": "搜索:",
    "lengthMenu": "每页 _MENU_ 条记录",
    "zeroRecords": "没有数据",
    "paginate": {
        "previous": "上一页",
        "next": "下一页"
    },
     //"infoFiltered": "从 _MAX_ 条记录中筛选",
    "info": "",
    //"info": "第 _PAGE_ 页 / 共 _PAGES_ 页",
    "infoEmpty": "",
}

function format(d){
    $.ajax({
        url: './log/check_record/'+d.id,
    }).done(function () {
        console.log('logged!');
    });
    // `d` is the original data object for the row
    table = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;" width="100%"><tr width="100%s" style="background-color:rgb(215, 221, 219); ">';
    table += '<td style="text-align:left;vertical-align:top;" width="32%" ><p><span style="font-weight:bold;">项目简介: <br></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+ d['introduction'] +'</p></td>';
    table += '</tr></table>';

    return table;
}

$(document).ready(function() {
    $("#keyWords").val('');
    $("#investDate").val('');
    invest();
});

function hide_show(curr_ele){
    module_list.ids.forEach(function(element) {
        try{
            if (element.indexOf(curr_ele) == -1){
                $(element).hide()
            }else{
                $(element).show()
            }
        }catch(err){
            console.log(err)
        }
    }, this);
}

function func_feedback(matrix_id, receiptor, user_name){
    console.log(matrix_id, receiptor, user_name)
    if(matrix_id=='null' || matrix_id.trim()=='' || receiptor.trim()=='' || receiptor=='null'){
        return null;
    }
    $.ajax({
        type: "GET",                      //请求类型
        url: "./feedback?matrix_id=" + matrix_id,
        dataType: "json",                 //返回的数据类型
        success: function(data){          //data就是返回的json类型的数据
            //var value = htmlDecodeByRegExp(data.crawlLog);
            $( "#mydailog").html('<textarea style="white-space: pre-wrap;" id="feedback" rows="14%" cols="100%">领取人：'+ receiptor +' &#10; &#10; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;记录：'+data['data']['feedback_desc']+'</textarea>');
        },
        error: function(data){
            alert('error');
        }
    });
    if(receiptor.trim()==user_name.trim()){
        $("#mydailog").dialog(
            {
                buttons: [
                    {
                        text: "更新",
                        icon: "ui-icon-heart",
                        click: function() {
                            info=""
                            var desc = $('#feedback').val().trim();
                            var patt=new RegExp(/记录：([\s\S]+)/);
                            result = patt.exec(desc)
                            if(result.length > 0){
                                info=result[1];
                            }
                            $.ajax({
                                type: "POST",                      //请求类型
                                url: "./feedback?matrix_id=" + matrix_id + '&desc=' + info,
                                contentType: "application/json; charset=utf-8",
                                data: '{}',
                                dataType: "json",                 //返回的数据类型
                                success: function(data){          //data就是返回的json类型的数据
                                    alert('更新成功');
                                },
                                error: function(data){
                                    alert('更新失败')
                                }
                            });
                        }
                    },
                    {
                        text: "关闭",
                        icon: "ui-icon-heart",
                        click: function() {
                        $( this ).dialog( "close" );
                        }
                    }
                ],
                width: 800,
                height: 413,
            });
    }else{
        $("#mydailog").dialog({
            buttons: [
                {
                    text: "关闭",
                    icon: "ui-icon-heart",
                    click: function() {
                    $( this ).dialog( "close" );
                    }
                }
            ],
            width: 800,
            height: 413
        });
    };
}

function func_receiptor(matrix_id, username){
    $.ajax({
        type: "GET",                      //请求类型
        url: "./receiptor?username="+username+"&matrix_id="+matrix_id,
        dataType: "json",                 //返回的数据类型
        success: function(data){          //data就是返回的json类型的数据
            alert('领取成功')
            $('div[item="'+ matrix_id +'"]').html('已领取');
            $('#' + matrix_id).html( '<a href="#" onclick="func_feedback(\''+ matrix_id +'\', \'' + username + '\', \''+ username +'\')">查看记录</a>');
        },
        error: function(data){
            alert('领取失败');
        }
    });
}
function func_unreceiptor(matrix_id){
    a='';
}

function invest(){
    var sourceMap = {};
    sourceMap.xiniu = "烯牛";
    sourceMap.itjuzi = "it桔子";
    sourceMap.jz36k= "鲸准";
    username=$('.dropbtn').text().trim();
    var table = $('#invest').DataTable({
      "searching": false,
      "processing": true,
      "serverSide": true,
      "select": true,
      "scrollX": true,
      "scrollY": true,
      "destroy": false,
      "autoWidth": true,
      "language": language,
      "ajax": {
        "url": "./invest_json",
        "dataSrc": function(data){
            return data.data;
        },
      },
      // 列控制
        "columns": [
            {
                "data": "project_name",
                "orderable": false,
                //"className": 'details-control',
                "render": function (data, type, row) {
                    //return '<div class="center"><a href="#">' + data + '</a></div>';
                    return '<div class="center"><a href="./content?matrix_id='+ row.matrix_id +'" target="_Blank">'+ data + '</a></div>';
                }
            },
            {
                "data": "project_name",
                "orderable": false,
                "visible": false,
                //"className": 'details-control',
                "render": function (data, type, row) {
                    //return '<div class="center"><a href="#">' + data + '</a></div>';
                    return '<div class="center">'+ data + '</div>';
                }
            },
            {   "data":"company_name",
                "orderable": false,
                "visible": false,
                "render": function (data, type, row) {
                    return '<div class="center"><a href="./content?matrix_id='+ row.matrix_id +'" target="_Blank">'+ data + '</a></div>';
                }
            },
            {
                "data": "detect_date",
                "visible": false,
                "render": function (data, type, row) {
                    return '<div class="center">' + data + '</div>';
                }
            },

            { "data": "finance_date",
                "render": function (data, type, row) {
                    return '<div class="center">' + data + '</div>';
                }
            },
            { "data": "finance_turn",
                "render": function (data, type, row) {
                    return '<div class="center">' + data + '</div>';
                }
            },
            {   "data": "finance_amount",
                "orderable":      false,
                "render": function (data, type, row) {
                    var regx=RegExp('未');
                    if(regx.test(data)){
                        return '<div class="center">'+ data +' </div>';
                    }
                    return '<div class="center">'+ data +' </div>';
                }
            },
            { "data": "industry",
                "orderable":      false,
                "render": function (data, type, row) {
                    
                    if(row.industry!='' && row.industry!=undefined){
                        var industrys=row.industry.replace('|', '<br/>');
                        return '<div class="center">' + industrys + '</div>';
                    }
                    return '<div class="center">' + data + '</div>';
                }
            },
            {   "data": "institution",
                "orderable": false,
                "className": 'institution',
                "render": function (data, type, row) {
                    return collapse(data); 
                }
            },
            { "data": "receiptor",
                "render": function (data, type, row) {
                    if(data==''||data==undefined){
                        return '<div class="center" item="'+ row.matrix_id +'" ><a href="#" onclick="func_receiptor(\''+ row.matrix_id +'\', \''+ username +'\',)">点击领取</a></div>';
                    }else if(data==username){
                        return '<div class="center">已领取</div>';
                    }else if(data!=username){
                        return '<div class="center">已被领取</div>';
                    }
                }
            },
            {   "data": "receiptor",
                "render": function (data, type, row) {
                    if(data=='' || data == null || data=='undefined'){
                        return '<div class="center" id="'+ row.matrix_id +'">查看记录</div>';
                    }else{
                        return '<div class="center"><a href="#" onclick="func_feedback(\''+ row.matrix_id +'\', \'' + data + '\', \''+ username +'\')">查看记录</a></div>';
                    }
                }
            }
        ]
    });
    // $(".a.b") 且
    // $(".a, .b") 或
    // $("span[class!='filter_font'], [class='industry'], [class='country'], [class='round']") 混合
    $("span[class!='filter_font'], [class='industry'], [class='region'], [class='round'],[class='source']").click(function(){
        var _class = $(this).attr("class");
        if ($(this).attr("value")=='工商'){
            table.columns( [0, 4] ).visible( false, false );
            table.columns( [1, 2, 3] ).visible( true, true );

            today = moment();
            var daysFromLastFriday = today.day() + 2;
            var daysFromLastLastSat = daysFromLastFriday + 6;
            var LastLastSat = moment().subtract(daysFromLastLastSat, 'days');
            var lastFriday = moment().subtract(daysFromLastFriday, 'days');
            var start = LastLastSat.format('YYYY-MM-DD');
            var end = lastFriday.format('YYYY-MM-DD');
            var res = start + ' / ' + end;
            $("#investDate").val(res);

        } else if ( $(this).attr("value")=='消息源' ){
            table.columns( [0, 4] ).visible( true, true );
            table.columns( [1, 2, 3] ).visible( false, false );
        }
        att='.' + _class + '.filter_font';
        $(att).attr('class', _class);
        $(this).addClass('filter_font');
        passParams();
    });
    $.fn.dataTable.ext.errMode = 'throw';
    $('.dataTables_scrollBody').attr('class', 'dataTables_scrollBody auto_crawler');
    $('#invest').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();   
            // tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            // tr.addClass('shown');
        }
    });
    $('#invest').on('click', 'td.institution', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        var td = $(this).closest('td');
        var institution = row.data().institution;
        if ($(this).hasClass('expand')){
            $(this).html(collapse(institution));
        }else{
            $(this).html(expand(institution));
        }
        $(this).toggleClass('expand');
    });
    $("#keyWords").change(function(){
        //清空日期
        $("#investDate").val('');
        //清空行业分类
        $(".industry.filter_font").attr('class', 'industry');
        $("span[value='不限'][class='industry']").attr('class', 'industry filter_font');
        //清空轮次
        $(".round.filter_font").attr('class', 'round');
        $("span[value='不限'][class='round']").attr('class', 'round filter_font');
        //清空区域
        $(".region.filter_font").attr('class', 'region');
        $("span[value='不限'][class='region']").attr('class', 'region filter_font');
        passParams();
    });
    $('input[name="investDate"]').daterangepicker({
        autoUpdateInput: false,
        locale: {
            format: 'YYYY-MM-DD'
        }
    });
    $('input[name="investDate"]').on('cancel.daterangepicker', function (ev, picker) {
        $(this).val('');
        passParams();
    });
    $("#investDate").on('apply.daterangepicker', function (ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' / ' + picker.endDate.format('YYYY-MM-DD'));
        passParams();
    });
    $("#investDate").on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' / ' + picker.endDate.format('YYYY-MM-DD'));
        passParams();
    });
    $("#lastWeekBtn").click(function () {
        today = moment();
        var daysFromLastFriday = today.day() + 2;
        var daysFromLastLastSat = daysFromLastFriday + 6;
        var LastLastSat = moment().subtract(daysFromLastLastSat, 'days');
        var lastFriday = moment().subtract(daysFromLastFriday, 'days');
        var start = LastLastSat.format('YYYY-MM-DD');
        var end = lastFriday.format('YYYY-MM-DD');
        var res = start + ' / ' + end;
        $("#investDate").val(res);
        passParams();
    });
    $("#lastMonthBtn").click(function () {
            today = moment();
            var start = moment(today).subtract(1, 'months').startOf('month').format('YYYY-MM-DD');
            var end = moment(today).subtract(1, 'months').endOf('month').format('YYYY-MM-DD');
            var res = start + ' / ' + end;
            $("#investDate").val(res);
            passParams();
    });

    function collapse(data) {
        if (data.includes('|')) {
            var count = 2;
            while (count < 3) {
                count++;
                data = data.replace('|', '<br>');
            }
            if (count >= 3) {
                index = data.indexOf('|');
                if (index > 0) {
                    remainingString = data.substring(index, data.length);
                    if(data.substring(index+1, data.length).includes('|') ) { //check if more than 1 element left
                        data = data.replace(remainingString, '<br><a href="#">等等</a>');
                    }else{
                        data = data.replace('|', '<br>');
                    }
                }
            }
        }
        return '<div class="center">' + data + '</div>'; 
    }
    function expand(data) {
        data = data.replace(/['|']/g, '<br>');
        return '<div class="center">' + data + '</div>';
    }
    function passParams() {
        var industryId = $(".industry.filter_font").attr("value");
        var roundId = $(".round.filter_font").attr("value");
        var regionId = $(".region.filter_font").attr("value");
        var sourceId = $(".source.filter_font").attr("value");
        var investDate = $("#investDate").val();
        if(industryId=='不限' && roundId=='不限' && regionId=='不限' && investDate==''){
            var keyWords = $("#keyWords").val();
        }else{
            $("#keyWords").val('');
        }

        var param = "";
        if (industryId != '不限') {
            param += param ? '&' : '';
            param += "industry=" + industryId;
        }
        if (roundId != '不限') {
            param += param ? '&' : '';
            param += "round=" + roundId;
        }
        if (regionId != '不限') {
            param += param ? '&' : '';
            param += "region=" + regionId;
        }
        if (sourceId != '不限') {
            param += param ? '&' : '';
            param += "source=" + sourceId;
        }
        if (keyWords) {
            param += param ? '&' : '';
            param += "keyWords=" + keyWords;
        }
        if (investDate) {
            param += param ? '&' : '';
            param += "investDate=" + investDate;
        }
        table.ajax.url('./invest_json?' + param).load();
    }
}

