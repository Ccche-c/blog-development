from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2
import numpy as np


def validate_model():
    """验证训练好的车道线检测模型"""

    # 加载最佳模型
    model = YOLO('runs/segment/yolo11n_lane_detection/weights/best.pt')

    # 在验证集上评估
    print("开始在验证集上评估模型...")
    metrics = model.val(
        data='bdd100k_lane.yaml',
        batch=16,
        imgsz=640,
        conf=0.25,  # 置信度阈值
        iou=0.6,  # IoU阈值
        device='cuda' if torch.cuda.is_available() else 'cpu',
        save_json=True,  # 保存JSON结果
        save_hybrid=True,  # 保存混合标签
        plots=True  # 生成评估图表
    )

    print(f"📊 评估结果:")
    print(f"    mAP50: {metrics.box.map50:.4f}")
    print(f"    mAP50-95: {metrics.box.map:.4f}")
    print(f"    Precision: {metrics.box.mp:.4f}")
    print(f"    Recall: {metrics.box.mr:.4f}")

    return metrics


def predict_on_images():
    """在示例图像上进行预测"""

    model = YOLO('runs/segment/yolo11n_lane_detection/weights/best.pt')

    # 预测单张图像
    results = model.predict(
        source='path/to/test/image.jpg',  # 替换为测试图像路径
        conf=0.3,
        save=True,
        imgsz=640,
        show_labels=True,
        show_conf=True
    )

    # 显示结果
    for r in results:
        im_array = r.plot()  # 绘制预测结果
        plt.figure(figsize=(12, 8))
        plt.imshow(im_array)
        plt.axis('off')
        plt.title('Lane Detection Results')
        plt.show()


if __name__ == "__main__":
    import torch

    validate_model()
    # predict_on_images()