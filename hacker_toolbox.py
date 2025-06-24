import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QStackedWidget, QMessageBox, QFrame, QScrollArea, QLineEdit, QDialog, QSizePolicy, QFileDialog, QComboBox, QProgressBar, QCheckBox)
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl
from core_decoder import auto_analyze
from PyQt5.QtWebEngineWidgets import QWebEngineView
import requests
import os

# 多语言字典
LANGS = ['中文', 'English', '日本語']
LANG_DICT = {
    'title': ['破万法 - 黑客工具箱', 'PoWanFa - Hacker Toolbox', '破万法 - ハッカーツールボックス'],
    'login': ['登录', 'Login', 'ログイン'],
    'username': ['账号:', 'Username:', 'ユーザー名:'],
    'password': ['密码:', 'Password:', 'パスワード:'],
    'login_btn': ['登录', 'Login', 'ログイン'],
    'author': ['作者：小白  微信：ccyuwu8888  QQ：154418587', 'Author: Xiaobai  WeChat: ccyuwu8888  QQ: 154418587', '作者：小白  WeChat：ccyuwu8888  QQ：154418587'],
    'decode': ['加密解码分析', 'Decode & Analyze', '暗号解読分析'],
    'dashboard': ['可视化大屏', 'Web Dashboard', '可視化ダッシュボード'],
    'brute': ['爆破工具', 'Brute Force', 'ブルートフォース'],
    'input_content': ['请输入待分析内容：', 'Please input content to analyze:', '解析する内容を入力してください：'],
    'analyze': ['自动暴力解密', 'Auto Brute Decode', '自動ブルート解読'],
    'result': ['所有尝试结果：', 'All Results:', 'すべての試行結果：'],
    'cipher': ['密文:', 'Ciphertext:', '暗号文:'],
    'key': ['密钥（可手动输入或上传字典）:', 'Key (manual or upload dict):', 'キー（手動入力または辞書アップロード）:'],
    'upload_dict': ['上传字典', 'Upload Dict', '辞書アップロード'],
    'api': ['启用在线API爆破', 'Enable Online API', 'オンラインAPI有効化'],
    'api_addr': ['API地址（如有）', 'API URL (if any)', 'APIアドレス（任意）'],
    'start_brute': ['开始爆破', 'Start Brute', 'ブルート開始'],
    'progress': ['爆破进度:', 'Brute Progress:', 'ブルート進捗:'],
    'brute_result': ['爆破结果:', 'Brute Result:', 'ブルート結果:'],
    'help': ['帮助', 'Help', 'ヘルプ'],
    'lang': ['语言', 'Language', '言語'],
}

class LoginDialog(QDialog):
    def __init__(self, lang_idx=0):
        super().__init__()
        self.lang_idx = lang_idx
        self.setWindowTitle(LANG_DICT['title'][self.lang_idx] + ' - ' + LANG_DICT['login'][self.lang_idx])
        self.setFixedSize(500, 340)
        self.setStyleSheet('background:#181c1f;')
        layout = QVBoxLayout()
        title = QLabel(LANG_DICT['title'][self.lang_idx])
        title.setFont(QFont('Consolas', 28, QFont.Bold))
        title.setStyleSheet('color:#39ff14; margin-bottom:20px;')
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        user_label = QLabel(LANG_DICT['username'][self.lang_idx])
        user_label.setStyleSheet('color:#39ff14; font-size:18px;')
        self.user_input = QLineEdit()
        self.user_input.setText('admin')
        self.user_input.setStyleSheet('background:#222; color:#39ff14; font-size:20px;')
        pass_label = QLabel(LANG_DICT['password'][self.lang_idx])
        pass_label.setStyleSheet('color:#39ff14; font-size:18px;')
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setText('admin')
        self.pass_input.setStyleSheet('background:#222; color:#39ff14; font-size:20px;')
        self.login_btn = QPushButton(LANG_DICT['login_btn'][self.lang_idx])
        self.login_btn.setStyleSheet('background:#39ff14; color:#111; font-weight:bold; font-size:20px;')
        self.login_btn.setFixedHeight(40)
        self.login_btn.clicked.connect(self.check_login)
        layout.addWidget(user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(pass_label)
        layout.addWidget(self.pass_input)
        layout.addSpacing(20)
        layout.addWidget(self.login_btn)
        author = QLabel(LANG_DICT['author'][self.lang_idx])
        author.setStyleSheet('color:#39ff14; font-size:16px; margin-top:30px;')
        layout.addStretch(1)
        layout.addWidget(author, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        self.accepted = False
    def check_login(self):
        if self.user_input.text() == 'admin' and self.pass_input.text() == 'admin':
            self.accepted = True
            self.accept()
        else:
            QMessageBox.warning(self, LANG_DICT['login'][self.lang_idx], '账号或密码错误！')

class DecodeWidget(QWidget):
    update_dashboard = pyqtSignal(list, list)
    def __init__(self, lang_idx=0):
        super().__init__()
        self.lang_idx = lang_idx
        layout = QVBoxLayout()
        label = QLabel(LANG_DICT['input_content'][self.lang_idx])
        label.setStyleSheet('color:#39ff14; font-size:20px;')
        self.text_input = QTextEdit()
        self.text_input.setFont(QFont('Consolas', 16))
        self.text_input.setStyleSheet('background:#222; color:#39ff14; border-radius:8px;')
        self.text_input.setFixedHeight(180)
        self.btn = QPushButton(LANG_DICT['analyze'][self.lang_idx])
        self.btn.setStyleSheet('background:#39ff14; color:#111; font-weight:bold; font-size:18px; border-radius:8px;')
        self.btn.setFixedHeight(40)
        self.btn.clicked.connect(self.analyze)
        self.result_area = QScrollArea()
        self.result_area.setWidgetResizable(True)
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout()
        self.result_widget.setLayout(self.result_layout)
        self.result_area.setWidget(self.result_widget)
        layout.addWidget(label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.btn)
        layout.addWidget(QLabel(LANG_DICT['result'][self.lang_idx]))
        layout.addWidget(self.result_area)
        author = QLabel(LANG_DICT['author'][self.lang_idx])
        author.setStyleSheet('color:#39ff14; font-size:16px; margin-top:10px;')
        layout.addWidget(author, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def analyze(self):
        import requests
        content = self.text_input.toPlainText()
        while self.result_layout.count():
            item = self.result_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
        if not content.strip():
            QMessageBox.warning(self, '提示', '请输入内容！')
            return
        all_results = auto_analyze(content)
        if not all_results:
            self.result_layout.addWidget(QLabel('<font color="#ff5555">未识别到可解码内容。</font>'))
            self.update_dashboard.emit([], [])
            return
        # 统计各解码方式成功次数
        method_count = {}
        for item in all_results:
            for res in item['decode_results']:
                if res['success']:
                    method_count[res['method']] = method_count.get(res['method'], 0) + 1
        x = list(method_count.keys())
        y = list(method_count.values())
        self.update_dashboard.emit(x, y)
        # 本地字典路径
        dict_path = os.path.join(os.path.dirname(__file__), 'passwords_top1000.txt')
        dict_keys = []
        if os.path.exists(dict_path):
            with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
                dict_keys = [line.strip() for line in f if line.strip()]
        # 内置弱口令
        weak_passwords = ['', '123456', 'password', 'admin', 'qwerty', 'letmein', '111111', 'abc123', '123123', '12345678', '123456789', 'root', 'user', 'test', 'pass', '000000', '654321', '666666', '888888', 'iloveyou', '1234', '1q2w3e4r', '123', '12345']
        for item in all_results:
            orig = item['original']
            group = QFrame()
            group.setStyleSheet('background:#232a34; border:1.5px solid #39ff14; border-radius:12px; margin-bottom:18px; box-shadow:0 4px 24px #39ff1440;')
            vbox = QVBoxLayout()
            vbox.addWidget(QLabel(f'<b style="color:#39ff14; font-size:18px;">原文：</b><span style="color:#fff; font-size:16px;">{orig}</span>'))
            sorted_results = sorted(item['decode_results'], key=lambda x: not x['success'])
            for res in sorted_results:
                color = '#39ff14' if res['success'] else '#888'
                out = res['output'] if res['output'] else '无法解码'
                path = ' → '.join(res['path']) if res['path'] else res['method']
                # 多重爆破：弱口令+本地字典+API
                if res['method'] == 'MD5识别' and '疑似MD5' in out:
                    found = False
                    import hashlib
                    # 1. 弱口令爆破
                    for weak in weak_passwords:
                        if hashlib.md5(weak.encode()).hexdigest() == orig:
                            out = f'弱口令爆破成功：{weak if weak else "<空密码>"}'
                            color = '#00e676'
                            found = True
                            break
                    # 2. 本地字典爆破
                    if not found:
                        for key in dict_keys:
                            if hashlib.md5(key.encode()).hexdigest() == orig:
                                out = f'本地字典爆破成功：{key}'
                                color = '#00e676'
                                found = True
                                break
                    # 3. API爆破
                    if not found:
                        try:
                            api_url = f'http://www.nmd5.com/api/md5.asp?md5={orig}'
                            r = requests.get(api_url, timeout=5)
                            if r.status_code == 200 and r.text.strip():
                                out = f'API爆破成功：{r.text.strip()}'
                                color = '#ffb300'
                                found = True
                        except Exception:
                            out = 'API爆破失败'
                            color = '#ff5555'
                    if not found:
                        out = '未爆破成功'
                        color = '#ff5555'
                out_edit = QTextEdit(out)
                out_edit.setReadOnly(True)
                out_edit.setFont(QFont('Consolas', 13))
                out_edit.setStyleSheet(f'background:#181c1f; color:{color}; border-radius:8px; border:1px solid #333;')
                out_edit.setFixedHeight(60)
                out_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                copy_btn = QPushButton('复制')
                copy_btn.setStyleSheet(f'background:{color}; color:#111; font-size:14px; border-radius:6px;')
                copy_btn.setFixedWidth(60)
                copy_btn.clicked.connect(lambda _, text=out: QApplication.clipboard().setText(text))
                hbox = QHBoxLayout()
                hbox.addWidget(QLabel(f'<b style="color:{color}; font-size:16px;">{res["method"]}</b> <span style="color:#aaa; font-size:14px;">[{path}]</span>'))
                hbox.addStretch(1)
                hbox.addWidget(copy_btn)
                vbox.addLayout(hbox)
                vbox.addWidget(out_edit)
            group.setLayout(vbox)
            self.result_layout.addWidget(group)
        self.result_layout.addStretch(1)

class WebDashboardWidget(QWidget):
    def __init__(self, lang_idx=0):
        super().__init__()
        self.lang_idx = lang_idx
        layout = QVBoxLayout()
        label = QLabel(LANG_DICT['dashboard'][self.lang_idx])
        label.setStyleSheet('color:#39ff14; font-size:22px;')
        layout.addWidget(label)
        self.webview = QWebEngineView()
        self.html_template = '''
        <html>
        <head>
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
            function renderChart(x, y) {
                var chartDom = document.getElementById('main');
                if(!x || x.length === 0 || !y || y.length === 0) {
                    chartDom.innerHTML = '<div class="nodata">请先进行搜索</div>';
                    return;
                }
                var chart = echarts.init(chartDom);
                var option = {
                    title: { text: '', left: 'center', textStyle: { color: '#39ff14' } },
                    tooltip: {},
                    xAxis: { data: x, axisLabel: { color: '#39ff14', fontWeight: 'bold' }, axisLine: { lineStyle: { color: '#39ff14' } } },
                    yAxis: { axisLabel: { color: '#39ff14', fontWeight: 'bold' }, axisLine: { lineStyle: { color: '#39ff14' } }, splitLine: { lineStyle: { color: '#333' } } },
                    series: [{
                        name: '成功次数',
                        type: 'bar',
                        data: y,
                        itemStyle: { color: '#39ff14', borderRadius: [6,6,0,0], shadowColor: '#39ff14', shadowBlur: 10 }
                    }],
                    backgroundColor: 'rgba(34,34,34,0.98)'
                };
                chart.setOption(option);
                window.addEventListener('resize', function(){ chart.resize(); });
            }
            window.renderChart = renderChart;
            renderChart([], []);
            </script>
        </body>
        </html>
        '''
        self.webview.setHtml(self.html_template)
        layout.addWidget(self.webview, stretch=1)
        self.setLayout(layout)

    def update_chart(self, x, y):
        js = f'renderChart({x}, {y});'
        self.webview.page().runJavaScript(js)

class BruteForceThread(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(str, str)
    finished = pyqtSignal()
    def __init__(self, algorithm, ciphertext, key_list, api_url=None):
        super().__init__()
        self.algorithm = algorithm
        self.ciphertext = ciphertext
        self.key_list = key_list
        self.api_url = api_url
        self._is_running = True
    def run(self):
        total = len(self.key_list)
        for idx, key in enumerate(self.key_list):
            if not self._is_running:
                break
            # 本地爆破（仅示例，AES/DES/RC4等可扩展）
            if self.algorithm == 'MD5':
                import hashlib
                if hashlib.md5(key.encode()).hexdigest() == self.ciphertext:
                    self.result.emit(key, f'爆破成功：{key}')
                    break
            # 可扩展AES/DES/RC4等
            # 在线API爆破
            if self.api_url:
                try:
                    resp = requests.get(self.api_url, params={'hash': self.ciphertext, 'key': key}, timeout=5)
                    if resp.status_code == 200 and 'success' in resp.text:
                        self.result.emit(key, f'API爆破成功：{key}')
                        break
                except Exception:
                    pass
            self.progress.emit(int((idx+1)/total*100))
        self.finished.emit()
    def stop(self):
        self._is_running = False

class BruteForceWidget(QWidget):
    def __init__(self, lang_idx=0):
        super().__init__()
        self.lang_idx = lang_idx
        layout = QVBoxLayout()
        title = QLabel(LANG_DICT['brute'][self.lang_idx])
        title.setStyleSheet('color:#39ff14; font-size:22px;')
        layout.addWidget(title)
        # 算法选择
        h_alg = QHBoxLayout()
        h_alg.addWidget(QLabel('算法:'))
        self.alg_combo = QComboBox()
        self.alg_combo.addItems(['MD5', 'AES', 'DES', 'RC4'])
        h_alg.addWidget(self.alg_combo)
        h_alg.addStretch(1)
        layout.addLayout(h_alg)
        # 密文输入
        layout.addWidget(QLabel(LANG_DICT['cipher'][self.lang_idx]))
        self.cipher_input = QLineEdit()
        self.cipher_input.setStyleSheet('background:#222; color:#39ff14; font-size:16px;')
        layout.addWidget(self.cipher_input)
        # 密钥输入/字典上传
        layout.addWidget(QLabel(LANG_DICT['key'][self.lang_idx]))
        h_key = QHBoxLayout()
        self.key_input = QLineEdit()
        self.key_input.setStyleSheet('background:#222; color:#39ff14; font-size:16px;')
        h_key.addWidget(self.key_input)
        self.upload_btn = QPushButton(LANG_DICT['upload_dict'][self.lang_idx])
        self.upload_btn.setStyleSheet('background:#39ff14; color:#111;')
        self.upload_btn.clicked.connect(self.upload_dict)
        h_key.addWidget(self.upload_btn)
        layout.addLayout(h_key)
        # 在线API爆破
        self.api_checkbox = QCheckBox(LANG_DICT['api'][self.lang_idx])
        self.api_checkbox.setStyleSheet('color:#39ff14;')
        layout.addWidget(self.api_checkbox)
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText(LANG_DICT['api_addr'][self.lang_idx])
        self.api_input.setStyleSheet('background:#222; color:#39ff14; font-size:16px;')
        layout.addWidget(self.api_input)
        # 爆破按钮与进度
        self.start_btn = QPushButton(LANG_DICT['start_brute'][self.lang_idx])
        self.start_btn.setStyleSheet('background:#39ff14; color:#111; font-size:18px;')
        self.start_btn.clicked.connect(self.start_brute)
        layout.addWidget(self.start_btn)
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        # 结果展示
        layout.addWidget(QLabel(LANG_DICT['brute_result'][self.lang_idx]))
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setStyleSheet('background:#222; color:#39ff14; font-size:16px;')
        layout.addWidget(self.result_box)
        self.setLayout(layout)
        self.dict_keys = []
        self.thread = None
    def upload_dict(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择字典文件', '', 'Text Files (*.txt)')
        if fname:
            with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
                self.dict_keys = [line.strip() for line in f if line.strip()]
            QMessageBox.information(self, '字典导入', f'已导入{len(self.dict_keys)}个密钥')
    def start_brute(self):
        alg = self.alg_combo.currentText()
        cipher = self.cipher_input.text().strip()
        key = self.key_input.text().strip()
        api_url = self.api_input.text().strip() if self.api_checkbox.isChecked() else None
        if not cipher:
            QMessageBox.warning(self, '提示', '请输入密文！')
            return
        key_list = []
        if key:
            key_list.append(key)
        if self.dict_keys:
            key_list.extend(self.dict_keys)
        if not key_list:
            # 默认内置Top1000精简字典
            dict_path = os.path.join(os.path.dirname(__file__), 'passwords_top1000.txt')
            if os.path.exists(dict_path):
                with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
                    key_list.extend([line.strip() for line in f if line.strip()])
        if not key_list:
            QMessageBox.warning(self, '提示', '请手动输入密钥或上传字典！')
            return
        self.result_box.clear()
        self.progress_bar.setValue(0)
        self.thread = BruteForceThread(alg, cipher, key_list, api_url)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.result.connect(self.show_result)
        self.thread.finished.connect(lambda: self.result_box.append('爆破结束'))
        self.thread.start()
    def show_result(self, key, msg):
        self.result_box.append(msg)

class HackerToolbox(QWidget):
    def __init__(self):
        super().__init__()
        self.lang_idx = 0
        self.setWindowTitle(LANG_DICT['title'][self.lang_idx])
        self.setGeometry(200, 60, 1300, 900)
        self.setWindowIcon(QIcon())
        self.init_ui()

    def init_ui(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(20, 20, 20))
        palette.setColor(QPalette.WindowText, QColor(57, 255, 20))
        self.setPalette(palette)
        # 语言切换
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(LANGS)
        self.lang_combo.setCurrentIndex(self.lang_idx)
        self.lang_combo.setStyleSheet('background:#222; color:#39ff14; font-size:16px;')
        self.lang_combo.currentIndexChanged.connect(self.change_lang)
        # 左侧菜单
        self.menu = QListWidget()
        self.menu.setStyleSheet('background:#111; color:#39ff14; font-size:22px;')
        self.menu.setFixedWidth(220)
        self.menu.addItem(QListWidgetItem(LANG_DICT['decode'][self.lang_idx]))
        self.menu.addItem(QListWidgetItem(LANG_DICT['dashboard'][self.lang_idx]))
        self.menu.addItem(QListWidgetItem(LANG_DICT['brute'][self.lang_idx]))
        # 可扩展更多功能
        self.stack = QStackedWidget()
        self.decode_widget = DecodeWidget(self.lang_idx)
        self.web_dashboard_widget = WebDashboardWidget(self.lang_idx)
        self.brute_widget = BruteForceWidget(self.lang_idx)
        self.stack.addWidget(self.decode_widget)
        self.stack.addWidget(self.web_dashboard_widget)
        self.stack.addWidget(self.brute_widget)
        # 布局
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.lang_combo, alignment=Qt.AlignmentFlag.AlignRight)
        vbox.addWidget(self.menu)
        hbox.addLayout(vbox)
        hbox.addWidget(self.stack, 1)
        self.setLayout(hbox)
        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.menu.setCurrentRow(0)
        # 连接信号
        self.decode_widget.update_dashboard.connect(self.web_dashboard_widget.update_chart)

    def change_lang(self, idx):
        self.lang_idx = idx
        self.setWindowTitle(LANG_DICT['title'][self.lang_idx])
        self.menu.item(0).setText(LANG_DICT['decode'][self.lang_idx])
        self.menu.item(1).setText(LANG_DICT['dashboard'][self.lang_idx])
        self.menu.item(2).setText(LANG_DICT['brute'][self.lang_idx])
        # TODO: 刷新所有子界面文本

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted and login.accepted:
        win = HackerToolbox()
        win.show()
        sys.exit(app.exec_()) 