import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
import time

# --- 配置区域 ---
# 1. 视频路径 (如果是摄像头请填 0)
VIDEO_PATH = "../交通片段.mp4"
# 2. 模型选择 (yolo11n, yolo11s, yolo11m, yolo11l, yolo11x)
MODEL_NAME = "yolo11n.pt"


# --- 核心类：视图转换器 (将像素坐标转换为真实世界坐标) ---
class ViewTransformer:
    def __init__(self, source: np.ndarray, target: np.ndarray):
        source = source.astype(np.float32)
        target = target.astype(np.float32)
        # 计算透视变换矩阵
        self.m = cv2.getPerspectiveTransform(source, target)

    def transform_points(self, points: np.ndarray) -> np.ndarray:
        # 将点转换为形状 (N, 1, 2) 以便 cv2.perspectiveTransform 使用
        reshaped_points = points.reshape(-1, 1, 2).astype(np.float32)
        transformed_points = cv2.perspectiveTransform(reshaped_points, self.m)
        return transformed_points.reshape(-1, 2)


def main():
    # 加载 YOLOv11 模型
    model = YOLO(MODEL_NAME)

    # 打开视频
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # --- [关键步骤] 标定摄像头 ---
    # 你需要在视频画面上找4个点（形成一个梯形区域），这4个点在现实世界中应该是一个矩形
    # 这里只是示例坐标，你需要根据你的视频手动调整 source_points

    # 假设画面中路面上的一个梯形区域
    source_points = np.array([
        [width * 0.23, height * 0.6],  # 左上
        [width * 0.72, height * 0.6],  # 右上
        [width * 0.95, height * 0.95],  # 右下
        [width * 0.05, height * 0.95]  # 左下
    ])

    # 对应的现实世界距离（鸟瞰图）
    # 假设这个梯形区域对应的真实路段是：宽 3.5米 (车道宽)，长 20米 (纵向距离)
    target_width = 3.5
    target_length = 20

    target_points = np.array([
        [0, 0],
        [target_width, 0],
        [target_width, target_length],
        [0, target_length]
    ])

    # 初始化转换器
    view_transformer = ViewTransformer(source_points, target_points)

    # 存储车辆历史位置: track_id -> 列表 [(timestamp, x, y), ...]
    track_history = defaultdict(lambda: [])

    # 存储平滑后的速度
    speed_cache = {}

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # 1. 运行 YOLOv11 追踪 (persist=True 保持ID连续)
        # classes=[2, 3, 5, 7] 对应 COCO 数据集的 Car, Motorcycle, Bus, Truck
        results = model.track(frame, persist=True, classes=[2, 3, 5, 7], verbose=False)

        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().numpy()
            cls_indices = results[0].boxes.cls.int().cpu().numpy()
            names = results[0].names

            # 绘制标定区域（调试用，确保车辆经过这个区域）
            cv2.polylines(frame, [source_points.astype(np.int32)], True, (0, 255, 255), 2)

            for box, track_id, cls_idx in zip(boxes, track_ids, cls_indices):
                x1, y1, x2, y2 = box

                # 获取车辆底部中心点 (通常底部中心最贴近路面，测距最准)
                cx, cy = int((x1 + x2) / 2), int(y2)

                # 2. 坐标转换：像素 -> 真实世界(米)
                pixel_point = np.array([[cx, cy]])
                real_point = view_transformer.transform_points(pixel_point)[0]

                current_time = time.time()

                # 记录轨迹
                track = track_history[track_id]
                track.append((current_time, real_point[0], real_point[1]))

                # 限制历史记录长度，避免内存溢出
                if len(track) > 30:
                    track.pop(0)

                # 3. 计算速度
                # 至少需要两个点，且时间间隔要足够长以减少抖动 (例如 0.5秒)
                speed_kmh = 0
                if len(track) >= 2:
                    # 取当前点和几个过去点比较
                    prev_time, prev_x, prev_y = track[0]  # 对比最早记录的点
                    curr_time, curr_x, curr_y = track[-1]

                    time_diff = curr_time - prev_time

                    # 避免除以零或时间过短
                    if time_diff > 0.1:
                        # 计算欧几里得距离 (单位：米)
                        distance = np.sqrt((curr_x - prev_x) ** 2 + (curr_y - prev_y) ** 2)

                        # 速度 = 距离 / 时间
                        speed_ms = distance / time_diff
                        speed_kmh = speed_ms * 3.6

                        # 简单的平滑处理
                        if track_id in speed_cache:
                            # 0.1 是平滑系数，使数值跳动不那么剧烈
                            speed_kmh = 0.9 * speed_cache[track_id] + 0.1 * speed_kmh
                        speed_cache[track_id] = speed_kmh

                # 绘制 UI
                class_name = names[cls_idx]
                label = f"{class_name} ID:{track_id} {int(speed_kmh)} km/h"

                # 根据速度变色 (超速变红，假设限速 80)
                color = (0, 255, 0) if speed_kmh < 80 else (0, 0, 255)

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                # 绘制底部中心点
                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

        # 显示画面
        cv2.imshow("YOLOv11 Speed Estimation", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()