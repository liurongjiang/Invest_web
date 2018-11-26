$(document).ready(function() {
    var urlPram = window.location.search;
    var regx = /matrix_id=(.+)$/;
    var res = regx.exec(urlPram);
    // 项目信息
    $.ajax({
      type: "GET",                      //请求类型
      url: "/invest/project_json?matrix_id=" + res[1],
      dataType: "json",                 //返回的数据类型
      success: function(data){          //data就是返回的json类型的数据
          content = '<table>';
          if(data.length==0){
            return 
          }
          var obj = data[0];
          project_info='<table width="100%">';
          project_info += '<tr><td rowspan="3" width="15%"><img src="'+ obj.logo +'" style="width: 100px; height: 100px;"></td><td width="15%" ><h3>'+ obj.project_name +'</h3></td><td width="20%" >'+ obj.platform_desc +'</td><td width="15%">'+ obj.city +'</td><td width="15%"></td><td width="10%"></td></tr>';
          project_info += '<tr><td class="right">公司名称：</td><td>'+ obj.company_name +'</td><td class="right">成立日期：</td><td>'+ obj.establish_date +'</td><td></td></tr>';
          project_info += '<tr><td class="right">联系电话：</td><td></td><td class="right">邮箱：</td><td></td><td></td></tr>';
          project_info += '<tr><td class="center">项目简介：</td><td colspan="4"><br/>'+ obj.introduction +'</td><td></td></tr>';
          project_info += '</table>';
          //$('#project_info').append(project_info);

          var project_info = '<table width="100%">';
          project_info += '<tr><td class="pro_td1"><img src="'+ obj.logo +'" class="logo"></td><td class="pro_td2"></td><td class="pro_td3"><span>'+ obj.introduction +'</span></td><td class="pro_td4"></td></tr>';
          project_info += '<tr><td rowspan="3"><div class="project"><h3>'+ obj.project_name +'</h3></div></td><td></td><td><div class="plat"><b>'+ obj.platform_desc +'</b></div></td><td></td></tr>';
          project_info += '<tr><td colspan="3"><span style="margin-left: 25px;"></span>';
          var other_tags=obj.other_tags.split('|');
          var tags = '';
          for(var i=0; i < other_tags.length; i++){
            var tag=other_tags[i];
            if(tag.trim()!=''){
                tags += '<span class="span"><a>'+ other_tags[i] +'</a></span>&nbsp;';
            }
          }
          project_info += tags;
          project_info += '</td></tr>';
          project_info += '<tr><td colspan="3"><ul class="company-info" style="white-space:nowrap;"><li style="margin-left: 16px;" class="li">地区：'+ obj.city +'</li><li class="li">公司名称：'+ obj.company_name +'</li><li class="li">成立日期：'+ obj.establish_date +'</li><li class="li">联系电话：'+ obj.tell +'</li><li class="li">邮箱：'+ obj.mail +'</li></ul></td></tr>';
          project_info += '</table>';
          $('#project_info').append(project_info);
      }
    });

    // 团队信息
    $.ajax({
        type: "GET",                      //请求类型
        url: "/invest/team_list?matrix_id=" + res[1],
        dataType: "json",                 //返回的数据类型
        success: function(data){          //data就是返回的json类型的数据
            var team_info='';
            for(index in data){
                obj=data[index]
                team_info += '<tr class="data"><td class="td1"><img class="picture" src="'+ obj.photo +'"></td><td class="td2"><b>姓名</b>：'+ obj.name +'<br/><b>职位</b>：'+ obj.position +'</td><td class="td3"><b>简介</b>：'+ obj.desc +'</td><td class="td4"></td></tr><tr><td colspan="4"><hr class="tr_hr" /></td></tr>'
            }
            $('#team_info').append(team_info);
        }
      });

    // 融资历程
    var table = $('#invest').DataTable({
      "searching": false,
      "processing": true,
      "serverSide": true,
      "select": true,
      "scrollX": true,
      "scrollY": true,
      "info": false,
      "destroy": false,
      "paging": false,
      "autoWidth": true,
      "ajax": {
        "url": "/invest/event_list?matrix_id=" + res[1],
        "dataSrc": function(data){
            return data.data;
        },
      },
      // 列控制
        "columns": [
            { "data": "finance_date",
              "orderable":      false,
                "render": function (data, type, row) {
                    return '<div class="center">' + data + '</div>';
                    }
                },
            { "data": "finance_turn",
              "orderable":      false,
                "render": function (data, type, row) {
                    return '<div class="center">' + data + '</div>';
                }
            },
            {   "data": "finance_amount",
                "orderable":      false,
                "render": function (data, type, row) {
                    return '<div class="center">'+ data +' </div>';
                }
            },
            {   "data": "institution",
                "orderable": false,
                "className": 'institution',
                "render": function (data, type, row) {
                    var reg = new RegExp( /\|/ , "g" );
                    data=data.replace(reg, '、');
                    return '<div class="center">'+ data +' </div>';; 
                }
            }
        ]
    });

    $.ajax({
        url: '/invest/log/check_record/' + res[1],
    });

});