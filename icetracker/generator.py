import random


def generate_index(content: str):
    """
    生成主页html
    :param content: 内容
    :return:
    """
    text = """<div id="index" class="col s12"><div class="container">"""
    text += content
    text += "</div></div>"
    return text


def generate_procs(content: str):
    """
    生成进程页html
    :param content:
    :return:
    """
    text = """<div id="process" class="col s12"><div class="container">"""
    text += content
    text += "</div></div>"
    return text


def generate_card(title: str, content: str):
    """
    生成一个卡片html
    :param title:
    :param content:
    :return:
    """
    text = """
<div class="card"><div class="card-content">
    <span class="card-title">%s</span>
    <p>%s</p>
</div></div>
        """ % (title, content)
    return text


def generate_table(header: list, data: list):
    """
    生成一个表格html
    :param header:
    :param data:
    :return:
    """
    text = '<table class="striped responsive-table">'
    try:
        data[0]
    except IndexError:
        return ""
    if len(header) != len(data[0]):
        raise Exception("表格未对齐")

    # generate header
    text += "<tr>"
    for item in header:
        text += """<th>%s</th>""" % item
    text += "</tr>"

    # generate lines
    for line in data:
        text += "<tr>"
        for item in line:
            text += """<td>%s</td>""" % item
        text += "</tr>"

    text += "</table>"
    return text


def generate_stack(data: list):
    text = """<ul class="collapsible" data-collapsible="expandable">"""
    for item in data:
        text += "<li>"
        text += """<div class="collapsible-header"><i class="material-icons">filter_drama</i>%s</div>""" % item[0]
        text += """<div class="collapsible-body"><p>%s</p></div>""" % item[1]
        text += "</li>"
    text += "</ul>"
    return text


def generate_full(index: str, procs: str) -> str:
    text = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <title>iceTracker</title>
    <meta charset="utf-8">
    <meta HTTP-EQUIV="pragma" CONTENT="no-cache">
    <meta HTTP-EQUIV="Cache-Control" CONTENT="no-store, must-revalidate">
    <meta HTTP-EQUIV="expires" CONTENT="Wed, 26 Feb 1997 08:21:57 GMT">
    <meta HTTP-EQUIV="expires" CONTENT="0">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.3/css/materialize.min.css">
    <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.3/js/materialize.min.js"></script>
</head>
<body>
<div class="navbar-fixed">
    <nav><div class="nav-wrapper"><a class="brand-logo">iceTracker</a>
        <ul class="right">
            <li><a href="#top" target="_self">回到顶部</a></li>
        </ul>
    </div></nav>
</div>
<div class="row">
    <div class="col s12">
        <ul class="tabs">
            <li class="tab col s3"><a class="active" href="#index">基本信息</a></li>
            <li class="tab col s3"><a href="#process">进程信息</a></li>
        </ul>
    </div>

<!--  Index 页 开始  -->

###REPLACE_TAG_Index###

<!--  Index 页 结束  -->

<!--  Process 页 开始  -->

###REPLACE_TAG_Procs###

<!--  Process 页 结束  -->
</div>

</body>
</html>
    """
    full = text.replace("###REPLACE_TAG_Index###", index)
    full = full.replace("###REPLACE_TAG_Procs###", procs)
    return full
