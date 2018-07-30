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
    console.log(d)
    // `d` is the original data object for the row
    table = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;" width="100%"><tr width="100%s" style="background-color:rgb(215, 221, 219); ">';
    table += '<td width="7%" ></td>';
    table += '<td width="8%" ><p><span style="color:red;">城市: &nbsp;&nbsp;</span>'+ d['city'] +'</p></td>';
    table += '<td width="52%" ><p><span style="color:red;">项目简介: &nbsp;&nbsp;</span>'+ d['introduction'] +'</p></td>';
    table += '<td width="20%" ><p><span style="color:red;">投资方: &nbsp;&nbsp;</span>'+ d['institution'] +'</p></td>';
    table += '<td width="13%" ></td>';
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
            { "data": "company_name",
                "orderable":      false,
                "render": function (data, type, row) {
                    return '<div class="center">' + data + '</div>';
                }
            },
            { "data": "industry",
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
    $("span[class!='filter_font'], [class='industry'], [class='country'], [class='round']").click(function(){
        var _class = $(this).attr("class");
        console.log(_class);
        att='.' + _class + '.filter_font'
        $(att).attr('class', _class);
        $("#keyWords").val("");
        $("#investDate").val("");
        $(this).addClass('filter_font');
        
        var industryId=$(".industry.filter_font").attr("id");
        var roundId=$(".round.filter_font").attr("id");
        var countryId=$(".country.filter_font").attr("id");
        var param = "industry=" + industryId;
        param += "&round=" + roundId;
        param += "&country=" + countryId;

        param += "&keywords=";
        param += "&investDate=";
        console.log(param);
        table.ajax.url( '/invest/invest_json?' + param).load();
    });
 
    $.fn.dataTable.ext.errMode = 'throw';

    $("#keyWords,#investDate").change(function(){
        var _id = $(this).attr("id");
        var param = "industry=" + $(".industry.filter_font").attr("id");
        param += "&round=" + $(".round.filter_font").attr("id");
        param += "&country=" + $(".country.filter_font").attr("id");
        if(_id=='keyWords'){
            param += '&keyWords=' + $("#keyWords").val();
            param += "&investDate=";
        }else{
            param += '&investDate=' + $("#investDate").val();
            param += "&keywords=";
        }
        console.log(param);
        table.ajax.url( '/invest/invest_json?' + param).load();
    });
}
