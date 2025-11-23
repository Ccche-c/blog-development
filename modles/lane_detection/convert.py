import json
import os
from tqdm import tqdm  # 进度条库, 如果没有请运行 pip install tqdm

# ================= 配置区域 =================

# 1. 输入文件夹路径 (包含多个 json 文件的文件夹)
INPUT_DIR = "E:\\bdd100k\\bdd100k\\data\\bdd100k_labels\\bdd100k\\labels\\100k\\val"

# 2. 输出文件夹 (生成的 txt 存放在这里)
OUTPUT_DIR = "E:\\bdd100k\\bdd100k\\data\\bdd100k_labels\\bdd100k\\labels\\100k\\val_yolo"

# 3. 图片分辨率 (BDD100K 数据集固定为 1280x720)
# 如果你的数据来源不同，请修改这里
IMG_WIDTH = 1280
IMG_HEIGHT = 720

# 4. 类别映射表 (必须根据你的实际需求修改 ID)
# 格式: "JSON中的category名字": YOLO的class_id
CLASS_MAP = {
    # --- 检测类 (Box) ---
    "traffic sign": 0,
    "traffic light": 1,
    "car": 2,
    "rider": 3,
    "motorcycle": 4,
    "person": 5,
    "bus": 6,
    "truck": 7,
    "bicycle": 8,
    "train": 9,

    # --- 分割类 (Poly) ---
    "area/drivable": 10,
    "area/alternative": 11,
    "lane/road curb": 12,
    "lane/single white": 13,
    "lane/double white": 14,
    "lane/single yellow": 15,
    "lane/double yellow": 16,
    "lane/crosswalk": 17
}


# ===========================================

def convert_box(box):
    """将 box2d (x1,y1,x2,y2) 转换为 YOLO (cx,cy,w,h) 并归一化"""
    x1, y1, x2, y2 = box['x1'], box['y1'], box['x2'], box['y2']

    # 计算中心点和宽高
    w = x2 - x1
    h = y2 - y1
    cx = x1 + w / 2.0
    cy = y1 + h / 2.0

    # 归一化
    return f"{cx / IMG_WIDTH:.6f} {cy / IMG_HEIGHT:.6f} {w / IMG_WIDTH:.6f} {h / IMG_HEIGHT:.6f}"


def convert_poly(poly):
    """将 poly2d ([[x,y,type]...]) 转换为 YOLO (x1 y1 x2 y2...) 并归一化"""
    points = []
    for p in poly:
        # BDD格式通常是 [x, y, "L"] 或 [x, y, "C"]，我们只取前两个
        x, y = p[0], p[1]
        points.append(f"{x / IMG_WIDTH:.6f} {y / IMG_HEIGHT:.6f}")
    return " ".join(points)


def process_single_entry(entry):
    """处理单个图片的数据块"""
    # 1. 获取文件名 (去掉后缀)
    file_name = entry.get('name', 'unknown')
    if file_name.endswith('.jpg'):
        file_name = file_name[:-4]

    yolo_lines = []

    # 2. 提取对象列表 (兼容 frames 结构和直接 objects 结构)
    objects = []
    if 'frames' in entry:
        for frame in entry['frames']:
            objects.extend(frame.get('objects', []))
    elif 'labels' in entry:  # 标准 BDD100K 格式
        objects = entry.get('labels', [])
    else:
        objects = entry.get('objects', [])

    # 3. 遍历对象转换
    for obj in objects:
        category = obj.get('category')

        if category in CLASS_MAP:
            class_id = CLASS_MAP[category]
            line = None

            # 优先处理多边形 (Segmentation)
            if 'poly2d' in obj:
                poly_str = convert_poly(obj['poly2d'])
                line = f"{class_id} {poly_str}"

            # 其次处理矩形框 (Detection)
            elif 'box2d' in obj:
                box_str = convert_box(obj['box2d'])
                line = f"{class_id} {box_str}"

            if line:
                yolo_lines.append(line)

    return file_name, yolo_lines


def process_single_json(json_path, output_dir):
    """处理单个JSON文件"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 统一将数据转为列表处理 (兼容单对象和列表)
        if isinstance(data, dict):
            data_list = [data]
        else:
            data_list = data

        file_count = 0
        for entry in data_list:
            file_name, lines = process_single_entry(entry)

            if lines:
                save_path = os.path.join(output_dir, f"{file_name}.txt")
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                file_count += 1

        return file_count, len(data_list)

    except Exception as e:
        print(f"❌ 处理文件 {os.path.basename(json_path)} 时出错: {e}")
        return 0, 0


def main():
    # 创建输出目录
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 获取输入文件夹中的所有JSON文件
    json_files = []
    for file_name in os.listdir(INPUT_DIR):
        if file_name.lower().endswith('.json'):
            json_files.append(os.path.join(INPUT_DIR, file_name))

    if not json_files:
        print(f"❌ 在文件夹 {INPUT_DIR} 中未找到任何JSON文件")
        return

    print(f"📁 在 {INPUT_DIR} 中找到 {len(json_files)} 个JSON文件")
    print("开始转换...")

    total_txt_count = 0
    total_img_count = 0

    # 处理每个JSON文件
    for json_path in tqdm(json_files, desc="处理JSON文件"):
        txt_count, img_count = process_single_json(json_path, OUTPUT_DIR)
        total_txt_count += txt_count
        total_img_count += img_count

    print(f"✅ 转换完成！")
    print(f"📊 统计信息:")
    print(f"   - 处理的JSON文件: {len(json_files)} 个")
    print(f"   - 处理的图片数据: {total_img_count} 个")
    print(f"   - 生成的TXT文件: {total_txt_count} 个")
    print(f"📁 文件保存在: {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    main()