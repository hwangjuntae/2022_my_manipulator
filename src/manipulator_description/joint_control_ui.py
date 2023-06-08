#!/usr/bin/env python

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import rospy
from std_msgs.msg import Float64

class JointControlUI(QMainWindow):
    def __init__(self, joint_name):
        super().__init__()
        self.joint_name = joint_name
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.slider_value_changed)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Joint {joint_name} Control"))
        layout.addWidget(self.slider)
        
        widget = QWidgeWt()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        rospy.init_node('joint_control_ui')
        self.publisher = rospy.Publisher(f'{self.joint_name}_position_controller/command', Float64, queue_size=10)

    def slider_value_changed(self, value):
        min_joint_limit = -1.57
        max_joint_limit = 1.57
        joint_position = value / 100.0 * (max_joint_limit - min_joint_limit) + min_joint_limit
        self.publisher.publish(joint_position)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Define the joint names
    joint_names = ['Revolute 48', 'Revolute 50', 'Revolute 52', 'Revolute 54', 'Revolute 56', 'Revolute 59']
    
    # Create a UI window for each joint
    ui_windows = []
    for joint_name in joint_names:
        ui_window = JointControlUI(joint_name)
        ui_window.show()
        ui_windows.append(ui_window)
    
    sys.exit(app.exec_())
