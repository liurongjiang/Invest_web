import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
#import MySQLdb
import dash_table
import pymysql
from event import app as server

matrix_con=pymysql.connect(host="192.168.1.180", user="rongjiang", password="password4321",
								  db="integrated", charset="utf8")
'''
matrix_con = MySQLdb.connect(host="192.168.1.180", user="rongjiang", password="password4321",
								  db="integrated", charset="utf8")
'''

one_year_begin = datetime.strftime(datetime.now() - relativedelta(years=1), "%Y-%m-%d")
sql_str = """ SELECT a.project_name, a.company_name, a.cleaned_company_name, a.introduction, 
          a.other_tags, b.institution, b.finance_turn, b.finance_amount, b.finance_date, a.industry, 
          a.detect_date from matrix_invest_project as a RIGHT JOIN matrix_invest_event as b 
          ON a.matrix_id = b.matrix_id WHERE b.finance_date > \"{0}\" ORDER BY b.finance_date DESC""".format(one_year_begin)
one_year_df = pd.read_sql(sql_str, matrix_con)

sql_str = """SELECT * FROM holding_detect_company WHERE detect_date > \"{0}\" ORDER BY detect_date DESC""".format(one_year_begin)
holding_year_df =pd.read_sql(sql_str, matrix_con)
source_column_list = ["project_name", "company_name", "cleaned_company_name", "introduction", "other_tags",
					  "finance_turn", "finance_amount", "institution", "industry", "finance_date"]
holding_column_list = ["project_name", "company_name", "cleaned_company_name", "introduction", "other_tags",
					   "finance_turn", "finance_amount", "institution", "industry", "detect_date"]
one_year_df = one_year_df[source_column_list]
holding_year_df = holding_year_df[holding_column_list]

holding_year_df = holding_year_df.rename(columns={"detect_date": "finance_date"})
holding_year_df = holding_year_df.drop_duplicates(subset=['cleaned_company_name', 'finance_turn'], keep='first')
one_year_df = one_year_df.append(holding_year_df[~holding_year_df["cleaned_company_name"].
								 isin(list(one_year_df["cleaned_company_name"]))])

display_column_list = ["project_name", "company_name", "other_tags", "industry", "finance_turn", "finance_amount",
	"institution", "finance_date"]
chinese_column_list = ["项目", "公司", "行业", "轮次", "金额", "日期", "机构"]
finance_turn_list = ["种子轮", "天使轮", "A轮", "B轮", "C轮", "D轮及以后", "战略投资"]

display_df = one_year_df[display_column_list]

def generate_table(dataframe, institution, startDate, endDate, industry, max_rows=1000):
    first_df = display_df[display_df["institution"].str.contains(institution)]
    second_df = first_df[first_df["finance_date"] >= startDate]
    if industry != "ALL":
        second_df = second_df[second_df["industry"].str.contains(industry)]
    institution_df = second_df[second_df["finance_date"] <= endDate]
    return html.Div([
		html.Label("{0}".format(institution), style={'color': 'blue', 'fontSize': 30}),
		html.Table(
        # Header
        [html.Tr([html.Th(col) for col in institution_df.columns])] +

        # Body
        [html.Tr([
            html.Td(institution_df.iloc[i][col]) for col in institution_df.columns
        ]) for i in range(min(len(institution_df), max_rows))]
    	)
	])


def dataframe_filter(year_df, start_date, end_date, inst_list, industry="ALL"):
	'''
	## year_df, 最近一年期的投资所有事件
	## start_date, 开始统计时间 format"XXXX_XX_XX"
	## end_date, 统计结束时间
	## inst_list 选择的机构列表
	## industry 选择的行业
	'''
	# filter with time
	after_starttime_df = year_df[year_df['finance_date'] >= start_date]
	date_filtered_df = after_starttime_df[after_starttime_df['finance_date'] <= end_date]

	# filter with institution
	if len(inst_list) == 0:
		return False
	row_select_series = date_filtered_df["institution"].str.contains(inst_list[0])
	for institution_item in inst_list[1:]:
		row_select_series = row_select_series | date_filtered_df["institution"].str.contains(institution_item)
	institution_filtered_df = date_filtered_df[row_select_series]

	# filter with industry
	if industry == "ALL":
		return institution_filtered_df
	else:
		industry_filtered_df = institution_filtered_df[institution_filtered_df["industry"].str.contains(industry)]
		return industry_filtered_df

def turn_adjust(t_dic):
    new_turn_dic = {k:0 for k in finance_turn_list}
    for k, v in t_dic.items():
        if k in new_turn_dic.keys():
            new_turn_dic[k] = v
    for k, v in t_dic.items():
        if k not in new_turn_dic.keys():
            if "A" in k:
                new_turn_dic['A轮'] += v
            elif "B" in k:
                new_turn_dic['B轮'] += v
            elif "C" in k:
                new_turn_dic['C轮'] += v
            else:
                new_turn_dic['D轮及以后'] += v
    return new_turn_dic


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


#server = flask.Flask(__name__)
app = dash.Dash(__name__, url_base_pathname='/insitution/', server=server, external_stylesheets=external_stylesheets)

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
	[
		html.Div([

			html.Span("机构投资比较", className='app-title'),

			html.Div(
				html.Img(src='https://www.matrixpartners.com.cn/images/sample/logo.png', height="100%")
				, style={"float": "right", "height": "100%"})
		],
			className="row header"
		),

		# Tab content
		html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),
		html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css", rel="stylesheet"),
		html.Link(
			href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/"
				 "stylesheet-oil-and-gas.css",
			rel="stylesheet"),
		html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
		html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
		html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
		html.Link(
			href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/"
				 "cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css",
			rel="stylesheet"),

		html.Div(
		[
			html.Label('机构（多选）'),
			dcc.Checklist(
				options=[
					{'label': '经纬中国', 'value': '经纬中国'},
					{'label': '红杉资本', 'value': '红杉资本'},
					{'label': 'IDG资本', 'value': 'IDG资本'},
					{'label': '真格基金', 'value': '真格基金'},
					{'label': '险峰长青', 'value': '险峰长青'},
					{'label': '源码资本', 'value': '源码资本'},
					{'label': '顺为资本', 'value': '顺为资本'},
					{'label': '洪泰基金', 'value': '洪泰基金'},
					{'label': '梅花天使创投', 'value': '梅花天使创投'},
					{'label': '九合创投', 'value': '九合创投'},
					{'label': '高瓴资本', 'value': '高瓴资本'},
					{'label': 'GGV纪源资本', 'value': 'GGV纪源资本'},
				],
				id="institution_list",
				values=['经纬中国', '红杉资本', 'IDG资本'],
				style={'width': '25%', 'marginBottom': 20, 'marginTop': 20, "display": "inline-block"},
				labelStyle={'display': 'inline-block'},
			),

			html.Label('时间范围选择'),
			dcc.DatePickerRange(
				id='date-picker-range',
				start_date_placeholder_text="Start Period",
				end_date_placeholder_text="End Period",
				min_date_allowed=datetime(2008, 1, 1),
				max_date_allowed=datetime.now(),
				initial_visible_month=datetime.now(),
				end_date=datetime.now(),
				start_date=datetime.now() - relativedelta(years=1),
				# calendar_orientation='vertical',
			),

			html.Label('行业小组'),
			html.Span(
				dcc.Dropdown(
					id="industry_dropdown",
					options=[
						{"label": "所有行业", "value": "ALL"},
						{"label": "B2B交易平台", "value": "B2B交易平台"},
						{"label": "消费", "value": "消费"},
						{"label": "企业服务", "value": "企业服务"},
						{"label": "文娱+移动2C", "value": r"文娱\+移动2C"},
						{"label": "医疗", "value": "医疗"},
						{"label": "互联网金融", "value": "互联网金融"},
						{"label": "新技术(智能)", "value": r"新技术\(智能\)"},
						{"label": "教育", "value": "教育"},
						{"label": "大出行", "value": "大出行"},
					],
					value="ALL",
					# style={"display": "none"},
					# 'width': '20%', 'marginBottom': 20, 'marginTop': 20, 'float': 'left'
				),
			),

			html.Button('OK', id='button'),
		]),

		html.Div([
			dcc.Graph(
				id='invest_number'
			),
			dcc.Graph(
				id='turn_compare',
			),
			dcc.Graph(
				id="turn_percent"
			)
		], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20', 'marginBottom': 50, 'marginTop': 50}),

		html.Div(id='input_container'),
])



@app.callback(
	Output('input_container', 'children'),
	[Input('button', 'n_clicks')],
	[State('institution_list', 'values'),
	 State('date-picker-range', 'start_date'),
	 State('date-picker-range', 'end_date'),
	 State('industry_dropdown', 'value')])
def make_sliders(n_clicks, institution_selected_list, start_date, end_date, industry):
	print(institution_selected_list)
	return [generate_table(display_df, institution, start_date, end_date, industry) for institution in institution_selected_list]

@app.callback(
	Output('invest_number', 'figure'),
	[Input('button', 'n_clicks')],
	[State('institution_list', 'values'),
	 State('date-picker-range', 'start_date'),
	 State('date-picker-range', 'end_date'),
	 State('industry_dropdown', 'value')]
	)
def invest_number_vis(n_clicks, institution_selected_list,start_date, end_date, industry):
	institution_interval_df = dataframe_filter(one_year_df, start_date, end_date, institution_selected_list, industry)
	invest_num_dic = {}
	for item in institution_selected_list:
		invest_num_dic[item] = institution_interval_df["institution"].str.contains(item).sum()
	return {
		"data": [go.Bar(
			x=institution_selected_list,
			y=[invest_num_dic[item] for item in institution_selected_list],
		)],
		"layout": go.Layout(title="机构投资数量")
	}

@app.callback(
	Output('turn_compare', 'figure'),
	[Input('button', 'n_clicks')],
	[State('institution_list', 'values'),
	 State('date-picker-range', 'start_date'),
	 State('date-picker-range', 'end_date'),
	 State('industry_dropdown', 'value')]
	)
def turn_num_vis(n_clicks, institution_selected_list,start_date, end_date, industry):
	institution_interval_df = dataframe_filter(one_year_df, start_date, end_date, institution_selected_list, industry)
	institution_invest_df_dic = {}
	for item in institution_selected_list:
		institution_invest_df_dic[item] = institution_interval_df[
			institution_interval_df["institution"].str.contains(item)]
	total_turn_dic = {}
	for key, value_df in institution_invest_df_dic.items():
		turn_dic = {k: list(value_df['finance_turn']).count(k) for k in list(value_df['finance_turn'])}
		turn_dic = turn_adjust(turn_dic)
		total_turn_dic[key] = turn_dic
	turn_df = pd.DataFrame(total_turn_dic).T
	turn_df = turn_df[finance_turn_list]
	trace_list = []
	for item in institution_selected_list:
		trace_list.append(go.Bar(
			x=finance_turn_list,
			y=list(turn_df.T[item]),
			name=item,
		))
	return {
		"data": trace_list,
		"layout": go.Layout(barmode='group', title="机构不同轮次投资数量")
	}

@app.callback(
	Output('turn_percent', 'figure'),
	[Input('button', 'n_clicks')],
	[State('institution_list', 'values'),
	 State('date-picker-range', 'start_date'),
	 State('date-picker-range', 'end_date'),
	 State('industry_dropdown', 'value')]
	)
def turn_percent_vis(n_clicks, institution_selected_list,start_date, end_date, industry):
	institution_interval_df = dataframe_filter(one_year_df, start_date, end_date, institution_selected_list, industry)
	institution_invest_df_dic = {}
	for item in institution_selected_list:
		institution_invest_df_dic[item] = institution_interval_df[
			institution_interval_df["institution"].str.contains(item)]
	total_turn_dic = {}
	for key, value_df in institution_invest_df_dic.items():
		turn_dic = {k: list(value_df['finance_turn']).count(k) for k in list(value_df['finance_turn'])}
		turn_dic = turn_adjust(turn_dic)
		total_turn_dic[key] = turn_dic
	turn_df = pd.DataFrame(total_turn_dic).T
	turn_df = turn_df[finance_turn_list]
	turn_percent_df = (turn_df.T / turn_df.T.sum()).T
	turn_percent_df = turn_percent_df[finance_turn_list]
	trace_list = []
	for item in institution_selected_list:
		trace_list.append(go.Bar(
			x=finance_turn_list,
			y=list(turn_percent_df.T[item]),
			name=item,
		))
	return {
		"data": trace_list,
		"layout": go.Layout(barmode='group', title="机构不同轮次投资数量百分比")
	}

if __name__ == '__main__':
		app.run_server(host='127.0.0.1', port=80, threaded=True)
