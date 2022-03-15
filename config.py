import os
import time


project_path = os.path.abspath(os.path.dirname(__file__))
out_path = project_path + "/out"
output_path = out_path + "/apk-checker-result"
config_path = project_path + "/check.json"
matrix_path = project_path + "/matrix-apk-canary-2.0.5.jar"
out_json_path = out_path + "/apk-checker-result.json"
out_html_path = out_path + "/apk-checker-result.html"
report_path = project_path + f"/report/{time.strftime('%Y%m%d%H%M%S')}.html"
template_path = "report.html"


taskDescription = "Unzip the apk file to dest path."
zn_taskDescription = u"解压文件"

taskDescription1 = "Read package info from the AndroidManifest.xml."
zn_taskDescription1 = u"读取AndroidManifest.xml文件"

taskDescription2 = "Find out the non-alpha png-format files whose size exceed limit size in desc order."
zn_taskDescription2 = u"找出大小超过限制大小的非alpha png格式文件(建议:对于不含alpha通道的png文件,可以转成jpg格式来减少文件的大小)"

taskDescription3 = "Show uncompressed file types."
zn_taskDescription3 = u"显示未压缩的文件类型(建议:某个文件类型的所有文件都没有经过压缩,可以考虑是否需要压缩)"

taskDescription4 = "Find out the duplicated files."
zn_taskDescription4 = u"找出重复文件(建议:对于两个内容完全相同的文件,应该去冗余)"

taskDescription5 = "Find out the unused assets."
zn_taskDescription5 = u"找出apk中包含的无用assets文件(建议:apk中未经使用的assets文件,应该予以删除)"

taskDescription6 = "Show files whose size exceed limit size in order."
zn_taskDescription6 = u"按顺序显示大小超过限制大小的文件"

taskDescription7 = "Count methods in dex file, output results group by class name or package name."
zn_taskDescription7 = "计算dex文件中的方法,按类名或包名输出结果"

taskDescription8 = "Check if there are more than one library dir in the 'lib'."
zn_taskDescription8 = u"检查是否包含多个ABI版本的动态库(建议:so文件的大小可能会在apk文件大小中占很大的比例,可以考虑在apk中只包含一个ABI版本的动态库)"

taskDescription9 = "Count the R class."
zn_taskDescription9 = u"统计apk中包含的R类以及R类中的field count(建议:编译之后,代码中对资源的引用都会优化成int常量,除了R.styleable之外,其他的R类其实都可以删除)"

taskDescription10 = "Check if the apk handled by resguard."
zn_taskDescription10 = u"检查是否经过了资源混淆(建议:推荐使用资源混淆来进一步减小apk的大小)"
