import subprocess
from config import *
from get_data import *
import os
import shutil


def main():
    print('----------项目初始化ing----------')
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    else:
        shutil.rmtree(out_path)
        os.mkdir(out_path)
    check_json = json.loads(read_file(config_path, 'utf-8'))
    if check_json["--output"] != output_path:
        check_json["--output"] = output_path
        with open(config_path, 'w', encoding='utf8') as f:
            f.write(json.dumps(check_json, indent=4, ensure_ascii=False))
    try:
        print("----------开始matrix检查app----------")
        cmd = "java -jar {} --config {}".format(matrix_path, config_path)
        print(f'----------执行命令{cmd}----------')
        subprocess.call(cmd, shell=True)
        print("----------检查app完成!----------")
        print("----------收集数据ing----------")
        app_name = check_json['--formatConfig'][0]['group'][-1]['name']
        gd = GetData()
        base_info = gd.get_base()
        pkg_info = gd.get_pkg_info()
        apk_info = gd.make_entries()
        apk_detail = gd.get_html_table()
        context = {
            'package': pkg_info['package'],
            'app_name': app_name,
            'versionName': pkg_info['versionName'],
            'apk_size': base_info['apk_size'],
            'minSdkVersion': pkg_info['minSdkVersion'],
            'targetSdkVersion': pkg_info['targetSdkVersion'],
            'versionCode': pkg_info['versionCode'],
            'app_info': apk_info,
            'app_detail': apk_detail,
            'create_time': time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        print("----------收集数据完成----------")
        html = f"""
            <html>
            <meta charset="UTF-8">
            <link rel="icon" href="{{ url_for('static',filename='favicon.ico')}}">
            <script src="https://img.hcharts.cn/jquery/jquery-1.8.3.min.js"></script>
            <script src="https://img.hcharts.cn/highcharts/highcharts.js"></script>
            <script src="https://img.hcharts.cn/highcharts-plugins/highcharts-zh_CN.js"></script>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.4.1/dist/css/bootstrap.min.css">
            <style type="text/css" media="screen">

                body        {{ font-family: Microsoft YaHei;padding: 20px; font-size: 100%}}
                table       {{ font-size: 100%;
                }}
                .table tbody tr td{{
                            vertical-align: middle;
                        }}

                .heading .description, .attribute {{
                    clear: both;
                }}
            </style>
                <h2 align="center">{context['app_name']}包大小检查测试报告 {context['create_time']}</h2>
                <br/>
                <hr>
                <div class="panel">
                    <div class="panel_title">
                        <h4>应用信息</h4>
                    </div>
                    <div class="panel_main" id="appInfoDiv">
                        <table class="table table-bordered" border="1" cellspacing="0" bordercolor="#778899" width = "80%">
                            <colgroup>
                                <col style="width:92px;">
                            </colgroup>
                            <tbody>

                            <tr>
                                <th>应用名称</th>
                                <td align="left"><span class="cut">{context['package']}</span></td>
                                <th>应用版本</th>
                                <td align="left"><span class="cut">{context['versionName']}</span></td>
                                <th>versionCode</th>
                                <td align="left"><span class="cut">{context['versionCode']}</span></td>

                            </tr>
                            <tr>
                                <th>minSdkVersion</th>
                                <td align="left"><span class="cut">{context['minSdkVersion']}</span></td>
                                <th>targetSdkVersion</th>
                                <td align="left"><span class="cut">{context['targetSdkVersion']}</span></td>
                                <th>包体大小/M</th>
                                <td align="left"><span class="cut">{context['apk_size']}</span></td>
                            </tr>

                            </tbody>
                        </table>
                    </div>
                </div>

            <!--    <h5>资源分布占比统计</h5>-->
                <div id="apk_percent" style="min-width:500px;height:400px"></div>
                <h5>资源详细信息</h5>
                <div class="table-sm table-striped table-bordered table-hover">
                {context['app_detail']}
                </div>
                <script>
                    $(function () {{
                        $('#apk_percent').highcharts({{
                         chart: {{
            		plotBackgroundColor: null,
            		plotBorderWidth: null,
            		plotShadow: false,
            		type: 'pie'
            	}},
            	title: {{
            		text: '资源分布占比统计'
            	}},
            	tooltip: {{
            		pointFormat: '{{series.name}}: <b>{{point.percentage:.1f}}%</b>'
            	}},
            	plotOptions: {{
            		pie: {{
            			allowPointSelect: true,
            			cursor: 'pointer',
            			dataLabels: {{
            				enabled: true,
            				format: '<b>{{point.name}}</b>: {{point.percentage:.1f}} %',
            				style: {{
            					color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
            				}}
            			}}
            		}}
            	}},
            	series: [
            	    {{
            		name: 'Brands',
            		colorByPoint: true,
            		data: [
                        {context['app_info']}
            		]
            	}}]
            }});
                    }})
                </script>
                <style type="text/css">
                </style>
            </body>
            </html>
            """
        with open(report_path, 'w', encoding='utf8') as f:
            f.write(html)
        print("----------成功生成测试报告----------")
    except Exception as e:
        print("检查app异常!{}".format(e))

    
if __name__ == '__main__':
    main()
