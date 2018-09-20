$(document).ready(function() {
    var urlPram = window.location.search;
    var regx = /id.+$/;
    var res = regx.exec(urlPram);
    $.ajax({
      type: "GET",                      //请求类型
      url: "/invest/project_json?id=" + res[0],
      dataType: "json",                 //返回的数据类型
      success: function(data){          //data就是返回的json类型的数据
          content = '<table>';
          if(data.length==0){
            return 
          }
          var obj = data[0];
          project_info='<br/><table width="100%">';
          project_info += '<tr><td rowspan="3" width="15%">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="'+ obj.logo +'" style="width: 100px; height: 100px;"></td><td width="15%" ><h3>'+ obj.project_name +'</h3></td><td width="20%" >'+ obj.platform_desc +'</td><td width="15%">'+ obj.city +'</td><td width="15%"></td><td width="10%"></td></tr>';
          project_info += '<tr><td class="right">公司名称：</td><td>'+ obj.company_name +'</td><td class="right">成立日期：</td><td>'+ obj.establish_date +'</td><td></td></tr>';
          project_info += '<tr><td class="right">联系电话：</td><td></td><td class="right">邮箱：</td><td></td><td></td></tr>';
          project_info += '<tr><td class="center">项目简介：</td><td colspan="4"><br/>'+ obj.introduction +'</td><td></td></tr>';
          project_info += '</table>';
          $('#project_info').append(project_info);

          invest_info='<tr><td></td><td></td><td></td><td></td></tr><tr><td class="center">'+ obj.finance_date +'</td><td class="center">'+ obj.finance_turn +'</td><td class="center">'+ obj.finance_amount+ obj.currency +'</td><td class="center">'+ obj.institution.replace(/\|/ig, '、') +'</td></tr>';
          $('#invest_info').append(invest_info);
      },
      error: function(data){
        alert('err');
      }
    });

    $.ajax({
      type: "GET",                      //请求类型
      url: "/invest/team_json?id=" + res[0],
      dataType: "json",                 //返回的数据类型
      success: function(data){          //data就是返回的json类型的数据
          content = '<table>';
          if(data.length==0){
            return 
          }
          tean_list=data;
          team_info='<br/><table width="100%"><tr><td>';
          for(person in tean_list){
            team_info += '<table width="100%"><tr><td rowspan="2" width="10%" class="center"><img src="" style="height: 50px;"></td><td width="50%" colspan="2">'+ person.name +': '+ person.position +'</td><td width="40%"></td></tr>';
            team_info += '<tr><td colspan="2">'+ person.desc +'</td><td></td></tr></table></br>';
          }
          team_info='</br></td></tr></table>';
          $('#team_info').append(team_info);
      },
      error: function(data){
        alert('err');
      }
    });
});