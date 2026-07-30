from datetime import datetime
import os



def create_report_path(
    csv_path
):

    report_dir = os.path.join(
        os.path.dirname(csv_path),
        "reports"
    )


    os.makedirs(
        report_dir,
        exist_ok=True
    )


    base_name = os.path.splitext(
        os.path.basename(csv_path)
    )[0]


    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


    report_name = (
        f"{base_name}_report_{timestamp}.html"
    )


    return os.path.join(
        report_dir,
        report_name
    )





def generate_html_report(
    df,
    file_name,
    columns,
    missing,
    duplicates,
    statistics,
    output_path,
):

    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>
KaizenKit CSV Report
</title>


<style>

body {{

    font-family:
    Arial,
    sans-serif;

    margin:40px;

}}


h1 {{

    color:#333;

}}


table {{

    border-collapse:
    collapse;

    width:
    100%;

}}


th, td {{

    border:
    1px solid #999;

    padding:
    8px;

}}


th {{

    background:
    #eee;

}}

</style>


</head>


<body>


<h1>
KaizenKit CSV Quality Report
</h1>


<p>
作成日時：
{datetime.now()}
</p>



<h2>
ファイル情報
</h2>


<table>

<tr>
<th>項目</th>
<th>内容</th>
</tr>


<tr>
<td>ファイル名</td>
<td>{file_name}</td>
</tr>


<tr>
<td>行数</td>
<td>{len(df)}</td>
</tr>


<tr>
<td>列数</td>
<td>{len(df.columns)}</td>
</tr>


</table>




<h2>
データ品質
</h2>


<table>

<tr>
<th>項目</th>
<th>値</th>
</tr>


<tr>
<td>欠損セル数</td>
<td>{missing}</td>
</tr>


<tr>
<td>重複行数</td>
<td>{duplicates}</td>
</tr>


</table>





<h2>
列分析
</h2>


<table>


<tr>

<th>No</th>

<th>列名</th>

<th>型</th>

<th>欠損</th>

<th>ユニーク数</th>


</tr>

"""



    for item in columns:

        html += f"""

<tr>

<td>{item["no"]}</td>

<td>{item["column"]}</td>

<td>{item["dtype"]}</td>

<td>{item["missing"]}</td>

<td>{item["unique"]}</td>


</tr>

"""



    html += """

</table>



<h2>
数値統計
</h2>


<table>


<tr>

<th>列名</th>

<th>最小</th>

<th>最大</th>

<th>平均</th>

<th>中央値</th>


</tr>

"""



    for column, value in statistics.items():

        html += f"""

<tr>

<td>{column}</td>

<td>{value["min"]}</td>

<td>{value["max"]}</td>

<td>{value["mean"]}</td>

<td>{value["median"]}</td>


</tr>

"""



    html += """

</table>


</body>

</html>

"""



    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)