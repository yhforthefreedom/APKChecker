import subprocess
from config import *
from get_data import *
import os
import shutil
from jinja2 import Environment, FileSystemLoader


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
        report_context = {
            "context": context
        }
        print("----------生成测试报告ing----------")
        template_environment = Environment(
            autoescape=False,
            loader=FileSystemLoader(project_path),
            trim_blocks=False)
        with open(report_path, 'w', encoding='utf8') as f:
            html = template_environment.get_template(template_path).render(report_context)
            f.write(html)
    except Exception as e:
        print("检查app异常!{}".format(e))

    
if __name__ == '__main__':
    main()
