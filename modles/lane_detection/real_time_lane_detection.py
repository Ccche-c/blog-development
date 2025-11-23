import cv2
from ultralytics import YOLO
import numpy as np


class RealTimeLaneDetector:
    def __init__(self, model_path, conf_threshold=0.3):
        """初始化车道线检测器"""
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.colors = [
            (255, 0, 0),  # 红色 - road curb
            (255, 255, 0),  # 青色 - single white
            (255, 255, 255),  # 白色 - double white
            (0, 255, 255),  # 黄色 - single yellow
            (255, 255, 0),  # 黄色 - double yellow
            (0, 0, 255)  # 蓝色 - crosswalk
        ]

    def process_frame(self, frame):
        """处理单帧图像"""
        # 运行推理
        results = self.model(frame, conf=self.conf_threshold, imgsz=640)

        # 绘制结果
        annotated_frame = results[0].plot()

        return annotated_frame, results[0]

    def run_webcam(self):
        """运行摄像头实时检测"""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("无法打开摄像头")
            return

        print("按 'q' 退出实时检测")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 处理帧
            processed_frame, results = self.process_frame(frame)

            # 显示结果
            cv2.imshow('Real-time Lane Detection', processed_frame)

            # 按q退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


def main():
    # 初始化检测器
    detector = RealTimeLaneDetector(
        model_path='runs/segment/yolo11n_lane_detection/weights/best.pt',
        conf_threshold=0.3
    )

    # 运行实时检测
    detector.run_webcam()


if __name__ == "__main__":
    main()