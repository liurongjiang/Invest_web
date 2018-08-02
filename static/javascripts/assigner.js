$(document).ready(function() {
    invest();
});

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

function assign_industry(objButton){
    var table = $('#invest').DataTable()
    selected = table.rows('.selected').data()
    if (selected){
      select_index = table.row('.selected').index() + 1
      row = selected[0]
      data = {'event_id': row['id'], 'industry_id':objButton.innerHTML }
      data = JSON.stringify(data, null, '\t'),
      console.log(data)
      $.ajax({
        url: assign_industry_url,
        dataType: "json",
        contentType: 'application/json;charset=UTF-8',
        method: "POST",
        data: data,
        success: function(response) {
            console.log(response)
            localStorage['select_index'] = String(select_index)
            location.reload()
         },
         error: function(error) {
             alert('Error occured')
             console.log(response)
         }
      })
    }
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
        "url": "/assigner/invest_json",
        "dataSrc": function(data){
            return data.data;
        },
      },
      // 列控制
        "columns": [
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
            { "data": "introduction",
                "orderable":      false,
                "render": function (data, type, row) {
                    return '<div class="text-left">' + data + '</div>';
                }
            },
            { "data": "industry_tags",
                "orderable":      false,
                "render": function (data, type, row) {
                  return '<div class="center">' + data + '</div>';
                }
            },
            { "data": "industry",
                "orderable":      false,
                "render": function (data, type, row) {
                  return '<div class="center">' + data + '</div>';
                }
            },
      ]

    });

    $('.dataTables_scrollBody').attr('class', 'dataTables_scrollBody auto_crawler');
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
        table.ajax.url( '/assigner/invest_json?' + param).load();
    });

    $.fn.dataTable.ext.errMode = 'throw';

    $("#keyWords").change(function(){
        $('input[name="investDate"]').val('');
        var _id = $(this).attr("id");
        var param = "industry=" + $(".industry.filter_font").attr("id");
        param += "&round=" + $(".round.filter_font").attr("id");
        param += "&country=" + $(".country.filter_font").attr("id");
        param += '&keyWords=' + $("#keyWords").val();
        param += "&investDate=";
        param += "&keywords=";
        console.log(param);
        table.ajax.url( '/assigner/invest_json?' + param).load();
    });

    $("#investDate").on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD') + '/' + picker.endDate.format('YYYY-MM-DD'));
        var _id = $(this).attr("id");
        var param = "industry=" + $(".industry.filter_font").attr("id");
        param += "&round=" + $(".round.filter_font").attr("id");
        param += "&country=" + $(".country.filter_font").attr("id");
        param += '&investDate=' + $("#investDate").val();
        param += "&keywords=";
        console.log(param);
        table.ajax.url( '/assigner/invest_json?' + param).load();
    });


    $('#invest tbody').on( 'click', 'tr', function () {
        $('tr').removeClass('selected');
        $(this).addClass('selected');
    });

    $('#invest tbody').on( 'click', 'tr', function () {
        $('tr').removeClass('selected');
        $(this).addClass('selected');
    });
    $(window).load(function () {
      var select_index = localStorage['select_index'] || '0';
      select_index = parseInt(select_index)
      table.row(select_index).nodes().to$().addClass('selected');
    });
}
