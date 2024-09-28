import torch
import torchvision
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def load_model():
    # モデルの読み込み（事前学習済みの重みを使用）
    model = fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()  # 評価モードに設定
    return model

def detect_objects(model, image_path, threshold=0.5):
    # 画像の読み込みと前処理
    image = Image.open(image_path).convert("RGB")
    image_tensor = F.to_tensor(image).unsqueeze(0)

    # 推論の実行
    with torch.no_grad():
        predictions = model(image_tensor)

    # 結果の処理
    boxes = predictions[0]['boxes'].cpu().numpy()
    labels = predictions[0]['labels'].cpu().numpy()
    scores = predictions[0]['scores'].cpu().numpy()

    # スコアがしきい値を超える検出結果のみを保持
    mask = scores > threshold
    boxes = boxes[mask]
    labels = labels[mask]
    scores = scores[mask]

    return image, boxes, labels, scores

def draw_boxes(image, boxes, labels, scores):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # COCOデータセットのクラス名（ラベルIDに対応）
    coco_names = [
        'background', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
        'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'street sign',
        'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
        'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'backpack',
        'umbrella', 'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
        'skateboard', 'surfboard', 'tennis racket', 'bottle', 'plate', 'wine glass',
        'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
        'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
        'couch', 'potted plant', 'bed', 'mirror', 'dining table', 'window', 'desk',
        'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book',
        'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ]

    for box, label, score in zip(boxes, labels, scores):
        x1, y1, x2, y2 = box
        draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=2)
        label_name = coco_names[label]
        label_text = f"{label_name}: {score:.2f}"
        draw.text((x1, y1 - 10), label_text, fill="red", font=font)

    return image

def main():
    model = load_model()
    image_path = "test_image.jpg"  # 検出したい画像のパスを指定
    image, boxes, labels, scores = detect_objects(model, image_path)
    result_image = draw_boxes(image, boxes, labels, scores)
    result_image.show()
    result_image.save("result_image.jpg")

if __name__ == "__main__":
    main()
