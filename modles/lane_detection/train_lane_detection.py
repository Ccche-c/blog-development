from ultralytics import YOLO
import os
import torch

# 训练模型
def train_lane_detection():
    """训练车道线检测模型"""

    # 检查GPU可用性
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"使用设备: {device}")

    # 加载预训练模型（使用分割模型）
    model = YOLO('yolo11n-seg.pt')  # 分割模型

    # 训练参数配置
    training_params = {
        'data': 'bdd100k_lane.yaml',  # 数据集配置
        'epochs': 100,  # 训练轮数
        'patience': 20,  # 早停耐心值
        'batch': 16,  # 批次大小
        'imgsz': 640,  # 输入图像尺寸
        'device': device,  # 训练设备
        'workers': 4,  # 数据加载线程数
        'lr0': 0.01,  # 初始学习率
        'lrf': 0.01,  # 最终学习率
        'momentum': 0.937,  # 动量
        'weight_decay': 0.0005,  # 权重衰减
        'warmup_epochs': 3.0,  # 热身轮数
        'warmup_momentum': 0.8,  # 热身动量
        'box': 7.5,  # 框损失权重
        'cls': 0.5,  # 分类损失权重
        'dfl': 1.5,  # DFL损失权重
        'close_mosaic': 10,  # 关闭mosaic的轮数
        'save': True,  # 保存检查点
        'save_period': 10,  # 保存周期
        'cache': False,  # 数据缓存
        'name': 'yolo11n_lane_detection',  # 实验名称
        'exist_ok': True,  # 允许覆盖现有实验
        'pretrained': True,  # 使用预训练权重
        'optimizer': 'auto',  # 优化器
        'verbose': True,  # 详细输出
        'seed': 42,  # 随机种子
        'deterministic': True,  # 确定性训练
        'single_cls': False,  # 单类别模式
        'rect': False,  # 矩形训练
        'cos_lr': False,  # 余弦学习率调度
        'overlap_mask': True,  # 重叠掩码
        'mask_ratio': 4,  # 掩码下采样比率
    }

    print("开始训练车道线检测模型...")

    # 开始训练
    results = model.train(**training_params)

    print("✅ 训练完成！")
    return results


if __name__ == "__main__":
    train_lane_detection()