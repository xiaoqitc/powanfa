from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# 示例数据（如为空则提示用户先进行搜索）
chart_data = {
    'x': [],
    'y': []
}

@app.route('/')
def dashboard():
    return render_template_string('''
    <html>
    <head>
        <title>数据可视化大屏</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
        <style>
            body { background: linear-gradient(135deg, #181c1f 60%, #232a34 100%); color: #39ff14; font-family: 'Consolas', 'Microsoft YaHei', monospace; margin: 0; }
            .panel { background: rgba(34,34,34,0.98); border-radius: 18px; padding: 40px 50px 30px 50px; margin: 60px auto 0 auto; width: 80%; max-width: 900px; box-shadow: 0 8px 40px #39ff1444, 0 1.5px 8px #000a; }
            h1 { color: #39ff14; font-size: 2.6em; letter-spacing: 2px; text-align: center; margin-bottom: 30px; text-shadow: 0 2px 12px #39ff1444; }
            #main { width: 100%; height: 420px; border-radius: 12px; background: #222; box-shadow: 0 0 16px #39ff1422 inset; }
            .nodata { color: #888; font-size: 1.3em; text-align: center; padding-top: 160px; }
            @media (max-width: 600px) {
                .panel { padding: 18px 5px; width: 98%; }
                h1 { font-size: 1.5em; }
                #main { height: 260px; }
                .nodata { padding-top: 80px; font-size: 1em; }
            }
        </style>
    </head>
    <body>
        <div class="panel">
            <h1>数据可视化大屏</h1>
            <div id="main"></div>
        </div>
        <script>
        fetch('/chart-data').then(resp => resp.json()).then(data => {
            var chartDom = document.getElementById('main');
            if(!data.x || data.x.length === 0 || !data.y || data.y.length === 0) {
                chartDom.innerHTML = '<div class="nodata">请先进行搜索</div>';
                return;
            }
            var chart = echarts.init(chartDom);
            var option = {
                title: { text: '', left: 'center', textStyle: { color: '#39ff14' } },
                tooltip: {},
                xAxis: { data: data.x, axisLabel: { color: '#39ff14', fontWeight: 'bold' }, axisLine: { lineStyle: { color: '#39ff14' } } },
                yAxis: { axisLabel: { color: '#39ff14', fontWeight: 'bold' }, axisLine: { lineStyle: { color: '#39ff14' } }, splitLine: { lineStyle: { color: '#333' } } },
                series: [{
                    name: '数量',
                    type: 'bar',
                    data: data.y,
                    itemStyle: { color: '#39ff14', borderRadius: [6,6,0,0], shadowColor: '#39ff14', shadowBlur: 10 }
                }],
                backgroundColor: 'rgba(34,34,34,0.98)'
            };
            chart.setOption(option);
            window.addEventListener('resize', function(){ chart.resize(); });
        });
        </script>
    </body>
    </html>
    ''')

@app.route('/chart-data')
def chart_data_api():
    return jsonify(chart_data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False) 