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
    console.log(d);
    $.ajax({
        url: '/invest/log/check_record/'+d.id,
    }).done(function () {
        console.log('logged!');
    });
    // `d` is the original data object for the row
    table = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;" width="100%"><tr width="100%s" style="background-color:rgb(215, 221, 219); ">';
    table += '<td width="8%" ></td>';
    table += '<td style="text-align:left;vertical-align:top;" width="12%"><span style="color:red;">企业名称: <br></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+ d['company_name'] +'</td>';
    table += '<td style="text-align:left;vertical-align:top;" width="32%" ><p><span style="color:red;">项目简介: <br></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+ d['introduction'] +'</p></td>';
    table += '<td style="text-align:left;vertical-align:top;" width="20%" ><p><span style="color:red;">投资方: <br></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+ d['institution'] +'</p></td>';
    table += '<td width="8%" ></td>';
    table += '</tr></table>';

    return table;
}


$(document).ready(function() {
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

function invest(){
    var sourceMap = {};
    sourceMap.xiniu = "稀牛";
    sourceMap.itjuzi = "IT桔子";
    sourceMap.jz36k= "鲸准";

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
        "url": "/invest/invest_json",
        "dataSrc": function(data){
            return data.data;
        },
      },
      // 列控制
        "columns": [
            {   "data": "logo",
                "orderable":      false,
                "render": function (data, type, row) {
                    return '<div class="center"><img src="'+ data +'" style="max-width: 38px;max-height: 38px;"></img><div>';
                }
            },
            {   "data":           null,
                "orderable":      false,
                "className":      'details-control',
                "defaultContent": ''
            },
            { "data": "project_name",
                "orderable":      false,
                "render": function (data, type, row) {
                    return '<div class="center"><a href="'+ row.source_url +'" target="_blank">' + data + '</a></div>';
                }
            },
            {
                "data": "source",
                "orderable": false,
                "render": function (data, type, row) {
                    return '<div class="center">' + sourceMap[data] + '</div>';    
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
            { "data": "finance_amount",
                "orderable":      false,
                "render": function (data, type, row) {
                    return '<div class="center">'+ data +' </div>';
                }
            },
            { "data": "currency",
                "orderable":      false,
                "render": function (data, type, row) {
                    return '<div class="center">' + data + '</div>';
                }
            },
            { "data": "city",
                "orderable":      false,
                "render": function (data, type, row) {
                    return '<div class="center">' + data + '</div>';
                }
            },
            { "data": "industry_tags",
                "orderable":      false,
                "render": function (data, type, row) {
                    /*
                    resp=''
                    resls=data.split('|')
                    for(i in resls){
                        resp += resls[i] + '</br>'
                    }*/
                    return '<div class="center">' + data + '</div>';
                }
            }
      ]
    });
    $('.dataTables_scrollBody').attr('class', 'dataTables_scrollBody auto_crawler');
    $('#invest').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });

    // $(".a.b") 且
    // $(".a, .b") 或
    // $("span[class!='filter_font'], [class='industry'], [class='country'], [class='round']") 混合
    $("span[class!='filter_font'], [class='industry'], [class='region'], [class='round'],[class='source']").click(function(){
        var _class = $(this).attr("class");
        console.log(_class);
        att='.' + _class + '.filter_font';
        $(att).attr('class', _class);
        $(this).addClass('filter_font');
        passParams();
    });

    $.fn.dataTable.ext.errMode = 'throw';

    $("#keyWords").change(function(){
        passParams();
    });
    $("#regionAll").click(function () {
        document.getElementById("cityDiv").style.display = 'none';
    });
    $("#regionOverseas").click(function () {
        document.getElementById("cityDiv").style.display = 'none';
    });
    $("#regionChina").click(function () {
        document.getElementById("cityDiv").style.display = 'block';
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
    
    function passParams() {
        var industryId = $(".industry.filter_font").attr("value");
        var roundId = $(".round.filter_font").attr("value");
        var regionId = $(".region.filter_font").attr("value");
        var sourceId = $(".source.filter_font").attr("value");
        var keyWords = $("#keyWords").val();
        var investDate = $("#investDate").val();

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
        console.log(param);
        table.ajax.url('/invest/invest_json?' + param).load();
    }
}
