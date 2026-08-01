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


def generate_quality_comment(
    missing,
    duplicates,
):
    """
    データ品質コメントを生成する
    """

    if missing == 0 and duplicates == 0:
        return (
            "データ品質は良好です。"
            "欠損値・重複データは確認されませんでした。"
        )

    if missing > 0 and duplicates == 0:
        return (
            "欠損データが見つかりました。"
            "分析前に補完または削除を推奨します。"
        )

    if missing == 0 and duplicates > 0:
        return (
            "重複データが見つかりました。"
            "集計結果へ影響する可能性があります。"
        )

    return (
        "欠損データと重複データが確認されました。"
        "分析前にデータクリーニングを推奨します。"
    )


def generate_quality_score(
    missing,
    duplicates,
):
    """
    データ品質スコア生成
    """

    if missing == 0 and duplicates == 0:
        return (
            "★★★★★",
            "非常に良好"
        )

    if missing == 0 and duplicates <= 10:
        return (
            "★★★★☆",
            "概ね良好"
        )

    if missing <= 10 and duplicates <= 10:
        return (
            "★★★☆☆",
            "軽微な修正が必要"
        )

    if missing > 10 or duplicates > 10:
        return (
            "★★☆☆☆",
            "データ確認を推奨"
        )

    return (
        "★☆☆☆☆",
        "品質改善が必要"
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

    quality_comment = generate_quality_comment(
        missing,
        duplicates,
    )

    score, score_text = generate_quality_score(
        missing,
        duplicates,
    )


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
    "Segoe UI",
    "Meiryo",
    sans-serif;

    margin:40px;

    color:#333;

    background:#fafafa;

}}


h1 {{

    color:#1f2937;

    border-bottom:
    3px solid #2563eb;

    padding-bottom:
    10px;

}}


h2 {{

    margin-top:
    35px;

    color:#374151;

    border-left:
    6px solid #2563eb;

    padding-left:
    10px;

}}


table {{

    border-collapse:
    collapse;

    width:
    100%;

    background:white;

    margin-top:
    10px;

}}


th {{

    background:#e5e7eb;

    font-weight:bold;

}}


th, td {{

    border:
    1px solid #d1d5db;

    padding:
    10px;

    text-align:left;

}}


tr:nth-child(even){{

    background:#f9fafb;

}}
.score-card {{

    background:white;

    border-radius:
    8px;

    padding:
    20px;

    margin-top:
    10px;

    border:
    1px solid #ddd;

    font-size:
    18px;

}}


.score {{

    font-size:
    32px;

    font-weight:
    bold;

    color:#2563eb;

}}


.comment-card {{

    background:#eff6ff;

    border-left:
    6px solid #2563eb;

    padding:
    15px;

    margin-top:
    10px;

}}


.comment {{

    margin:
    0;

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
総合評価
</h2>


<div class="score-card">

<div class="score">

{score}

</div>


<p>

{score_text}

</p>


</div>



<h2>
品質コメント
</h2>


<div class="comment-card">

<p class="comment">

{quality_comment}

</p>

</div>



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