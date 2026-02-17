#!/usr/bin/env python3
"""
LiptonWeb - Браузер на Python
Простой и функциональный браузер с встроенными инструментами для разработчика
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, 
                             QLineEdit, QPushButton, QStatusBar, QTabWidget, QHBoxLayout,
                             QSplitter, QTextEdit, QLabel, QComboBox, QCheckBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt, QPoint, QTimer
from PyQt5.QtGui import QIcon, QFont

class DevToolsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Toolbar для DevTools
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout()
        toolbar.setLayout(toolbar_layout)
        
        # Выбор типа инструментов
        self.tool_selector = QComboBox()
        self.tool_selector.addItems(["Консоль", "Сеть", "Элементы", "LocalStorage", "Cookies"])
        self.tool_selector.currentTextChanged.connect(self.switch_tool)
        toolbar_layout.addWidget(QLabel("Инструменты:"))
        toolbar_layout.addWidget(self.tool_selector)
        
        # Кнопка очистки
        clear_btn = QPushButton("Очистить")
        clear_btn.clicked.connect(self.clear_output)
        toolbar_layout.addWidget(clear_btn)
        
        toolbar_layout.addStretch()
        layout.addWidget(toolbar)
        
        # Область вывода
        self.output_area = QTextEdit()
        self.output_area.setFont(QFont("Courier", 10))
        self.output_area.setPlaceholderText("Результаты инструментов разработчика...")
        layout.addWidget(self.output_area)
        
        # Область ввода для консоли
        input_widget = QWidget()
        input_layout = QHBoxLayout()
        input_widget.setLayout(input_layout)
        
        input_layout.addWidget(QLabel(">>"))
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите JavaScript код...")
        self.input_field.returnPressed.connect(self.execute_js)
        input_layout.addWidget(self.input_field)
        
        execute_btn = QPushButton("Выполнить")
        execute_btn.clicked.connect(self.execute_js)
        input_layout.addWidget(execute_btn)
        
        layout.addWidget(input_widget)
        
        # Текущая вкладка для работы
        self.current_tab = None
        
    def set_current_tab(self, tab):
        self.current_tab = tab
        
    def switch_tool(self, tool_name):
        if not self.current_tab:
            return
            
        self.output_area.clear()
        
        if tool_name == "Консоль":
            self.output_area.append("=== JavaScript Консоль ===")
            self.output_area.append("Введите код в поле ниже для выполнения")
            
        elif tool_name == "Сеть":
            self.show_network_info()
            
        elif tool_name == "Элементы":
            self.show_page_elements()
            
        elif tool_name == "LocalStorage":
            self.show_localstorage()
            
        elif tool_name == "Cookies":
            self.show_cookies()
            
    def execute_js(self):
        if not self.current_tab:
            self.output_area.append("Ошибка: Нет активной вкладки")
            return
            
        code = self.input_field.text()
        if not code:
            return
            
        self.output_area.append(f">>> {code}")
        
        try:
            # Выполняем JavaScript с callback
            self.current_tab.web_view.page().runJavaScript(
                f"return {code}", 
                lambda result: self.display_js_result(result, code)
            )
        except Exception as e:
            self.output_area.append(f"Ошибка: {str(e)}")
            
        self.input_field.clear()
        
    def display_js_result(self, result, original_code):
        if result is not None:
            if isinstance(result, (dict, list)):
                import json
                self.output_area.append(f"Результат: {json.dumps(result, indent=2, ensure_ascii=False)}")
            else:
                self.output_area.append(f"Результат: {result}")
        else:
            self.output_area.append("Результат: undefined")
        
    def show_network_info(self):
        self.output_area.append("=== Сетевая активность ===")
        self.output_area.append("URL: " + self.current_tab.web_view.url().toString())
        self.output_area.append("Заголовок: " + self.current_tab.web_view.title())
        
    def show_page_elements(self):
        js_code = """
        var elements = [];
        var all = document.querySelectorAll('*');
        for(var i = 0; i < Math.min(all.length, 50); i++) {
            var el = all[i];
            elements.push(el.tagName.toLowerCase() + 
                        (el.id ? '#' + el.id : '') + 
                        (el.className ? '.' + el.className.split(' ').join('.') : ''));
        }
        return elements.slice(0, 20).join('\\n');
        """
        
        self.current_tab.web_view.page().runJavaScript(js_code, self.display_elements)
        
    def display_elements(self, elements):
        self.output_area.append("=== Элементы страницы ===")
        self.output_area.append(elements or "Элементы не найдены")
        
    def show_localstorage(self):
        js_code = "return JSON.stringify(localStorage, null, 2);"
        self.current_tab.web_view.page().runJavaScript(js_code, self.display_localstorage)
        
    def display_localstorage(self, data):
        self.output_area.append("=== Local Storage ===")
        try:
            import json
            parsed = json.loads(data)
            if parsed:
                for key, value in parsed.items():
                    self.output_area.append(f"{key}: {value}")
            else:
                self.output_area.append("Local Storage пуст")
        except:
            self.output_area.append(data or "Local Storage пуст")
            
    def show_cookies(self):
        js_code = """
        var cookies = document.cookie.split(';');
        return cookies.filter(c => c.trim()).join('\\n');
        """
        self.current_tab.web_view.page().runJavaScript(js_code, self.display_cookies)
        
    def display_cookies(self, cookies):
        self.output_area.append("=== Cookies ===")
        if cookies:
            for cookie in cookies.split('\n'):
                if cookie.strip():
                    self.output_area.append(cookie.strip())
        else:
            self.output_area.append("Cookies не найдены")
            
    def clear_output(self):
        self.output_area.clear()

class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Web view
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # Connect signals
        self.web_view.urlChanged.connect(self.url_changed)
        self.web_view.loadFinished.connect(self.load_finished)
        self.web_view.titleChanged.connect(self.title_changed)
        
    def load_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        self.web_view.setUrl(QUrl(url))
        
    def url_changed(self, url):
        # Передаем сигнал родителю
        if hasattr(self.parent(), 'tab_url_changed'):
            self.parent().tab_url_changed(self, url)
            
    def load_finished(self, success):
        # Передаем сигнал родителю
        if hasattr(self.parent(), 'tab_load_finished'):
            self.parent().tab_load_finished(self, success)
            
    def title_changed(self, title):
        # Передаем сигнал родителю
        if hasattr(self.parent(), 'tab_title_changed'):
            self.parent().tab_title_changed(self, title)

class LiptonWebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LiptonWeb Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Navigation buttons
        back_btn = QPushButton("←")
        back_btn.clicked.connect(self.go_back)
        toolbar.addWidget(back_btn)
        
        forward_btn = QPushButton("→")
        forward_btn.clicked.connect(self.go_forward)
        toolbar.addWidget(forward_btn)
        
        reload_btn = QPushButton("⟳")
        reload_btn.clicked.connect(self.reload_page)
        toolbar.addWidget(reload_btn)
        
        # Tab controls
        new_tab_btn = QPushButton("+")
        new_tab_btn.clicked.connect(self.add_new_tab)
        toolbar.addWidget(new_tab_btn)
        
        close_tab_btn = QPushButton("×")
        close_tab_btn.clicked.connect(self.close_current_tab)
        toolbar.addWidget(close_tab_btn)
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setPlaceholderText("Введите URL...")
        toolbar.addWidget(self.url_bar)
        
        # Dev tools button
        dev_btn = QPushButton("🔧 DevTools")
        dev_btn.setCheckable(True)
        dev_btn.clicked.connect(self.toggle_devtools)
        toolbar.addWidget(dev_btn)
        
        # Main splitter
        self.main_splitter = QSplitter(Qt.Vertical)
        layout.addWidget(self.main_splitter)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)
        self.main_splitter.addWidget(self.tab_widget)
        
        # DevTools widget (изначально скрыт)
        self.dev_tools = DevToolsWidget()
        self.main_splitter.addWidget(self.dev_tools)
        self.dev_tools.hide()
        
        # Устанавливаем начальные размеры сплиттера
        self.main_splitter.setSizes([600, 0])
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Create first tab
        self.add_new_tab()
        
    def add_new_tab(self, url="https://duckduckgo.com"):
        tab = BrowserTab(self)
        tab_index = self.tab_widget.addTab(tab, "Новая вкладка")
        self.tab_widget.setCurrentIndex(tab_index)
        tab.load_url(url)
        
    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
        else:
            # Нельзя закрыть последнюю вкладку
            pass
            
    def close_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        self.close_tab(current_index)
        
    def tab_changed(self, index):
        if index >= 0:
            current_tab = self.tab_widget.currentWidget()
            if current_tab and current_tab.web_view.url():
                self.url_bar.setText(current_tab.web_view.url().toString())
            # Обновляем DevTools для новой вкладки
            self.dev_tools.set_current_tab(current_tab)
            # Если DevTools открыты, обновляем содержимое
            if hasattr(self, 'dev_btn') and self.dev_btn.isChecked():
                self.dev_tools.switch_tool(self.dev_tools.tool_selector.currentText())
                
    def get_current_tab(self):
        return self.tab_widget.currentWidget()
        
    def navigate_to_url(self):
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.load_url(self.url_bar.text())
        
    def go_back(self):
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.web_view.back()
        
    def go_forward(self):
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.web_view.forward()
        
    def reload_page(self):
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.web_view.reload()
        
    def tab_url_changed(self, tab, url):
        if tab == self.get_current_tab():
            self.url_bar.setText(url.toString())
            
    def tab_load_finished(self, tab, success):
        if tab == self.get_current_tab():
            if success:
                self.status_bar.showMessage("Страница загружена")
            else:
                self.status_bar.showMessage("Ошибка загрузки")
                
    def tab_title_changed(self, tab, title):
        tab_index = self.tab_widget.indexOf(tab)
        if tab_index >= 0:
            # Обрезаем длинные заголовки
            display_title = title[:30] + "..." if len(title) > 30 else title
            self.tab_widget.setTabText(tab_index, display_title)
            
    def toggle_devtools(self):
        # Находим кнопку DevTools
        for action in self.findChildren(QPushButton):
            if "🔧 DevTools" in action.text():
                self.dev_btn = action
                break
                
        if self.dev_btn.isChecked():
            # Показываем DevTools
            self.dev_tools.show()
            self.main_splitter.setSizes([400, 300])
            # Устанавливаем текущую вкладку
            current_tab = self.get_current_tab()
            if current_tab:
                self.dev_tools.set_current_tab(current_tab)
                self.dev_tools.switch_tool(self.dev_tools.tool_selector.currentText())
        else:
            # Скрываем DevTools
            self.dev_tools.hide()
            self.main_splitter.setSizes([600, 0])

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("LiptonWeb Browser")
    
    browser = LiptonWebBrowser()
    browser.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
