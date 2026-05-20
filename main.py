import sys
from qtpy.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QComboBox)
from qtpy.QtCore import QTimer, Qt

class AutoFlowPomodoro(QWidget):
    def __init__(self):
        super().__init__()
        
        self.presets = {
            "25m Work / 5m Break": (25 * 60, 5 * 60),
            "50m Work / 10m Break": (50 * 60, 10 * 60),
            "60m Work / 15m Break": (60 * 60, 15 * 60)
        }
        
        self.current_preset = "25m Work / 5m Break"
        self.work_time, self.break_time = self.presets[self.current_preset]
        self.time_left = self.work_time
        self.is_work_mode = True
        
        self.init_ui()
        self.apply_theme()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_tick)
        
        # Start immediately
        self.start_timer()

    def init_ui(self):
        self.setWindowTitle("Auto-Flow Pomodoro")
        self.resize(500, 450)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        
        self.combo = QComboBox()
        self.combo.addItems(self.presets.keys())
        self.combo.setStyleSheet("font-size: 16px; padding: 5px;")
        self.combo.currentTextChanged.connect(self.change_preset)
        layout.addWidget(QLabel("Select Mode:"))
        layout.addWidget(self.combo)
        
        self.mode_label = QLabel("WORK TIME")
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.mode_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(self.mode_label)
        
        self.time_label = QLabel(self.format_time(self.time_left))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 100px; font-weight: bold;")
        layout.addWidget(self.time_label)
        
        self.toggle_btn = QPushButton("PAUSE")
        self.toggle_btn.setStyleSheet("padding: 20px; font-size: 20px; font-weight: bold; border-radius: 12px; border: none;")
        self.toggle_btn.clicked.connect(self.toggle_timer)
        layout.addWidget(self.toggle_btn)
        
        self.setLayout(layout)

    def apply_theme(self):
        if self.is_work_mode:
            bg_color, btn_color = "#E2504C", "#D3433F"
            self.mode_label.setText("WORK TIME")
        else:
            bg_color, btn_color = "#4CA6A6", "#3D8E8E"
            self.mode_label.setText("BREAK TIME")
            
        self.setStyleSheet(f"""
            QWidget {{ background-color: {bg_color}; color: #FFFFFF; }}
            QPushButton {{ background-color: {btn_color}; color: #FFFFFF; }}
            QComboBox {{ background-color: white; color: black; }}
        """)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def update_timer_tick(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.setText(self.format_time(self.time_left))
        else:
            self.timer.stop()
            self.is_work_mode = not self.is_work_mode
            self.apply_theme()

            self.time_left = self.work_time if self.is_work_mode else self.break_time
            self.time_label.setText(self.format_time(self.time_left))
            
            self.start_timer()

    def toggle_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.toggle_btn.setText("RESUME")
        else:
            self.start_timer()

    def start_timer(self):
        self.timer.start(1000)
        self.toggle_btn.setText("PAUSE")

    def change_preset(self, text):
        self.current_preset = text
        self.work_time, self.break_time = self.presets[text]
        self.is_work_mode = True
        self.apply_theme()
        self.time_left = self.work_time
        self.time_label.setText(self.format_time(self.time_left))
        self.start_timer()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutoFlowPomodoro()
    window.show()
    sys.exit(app.exec_())