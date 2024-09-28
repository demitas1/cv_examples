import torch
import torchvision
from torchvision import transforms
from torchvision.models.segmentation import deeplabv3_resnet101
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def load_model():
    # モデルの読み込み（事前学習済みの重みを使用）
    model = deeplabv3_resnet101(pretrained=True)
    model.eval()  # 評価モードに設定
    return model

def preprocess_image(image_path):
    # 画像の前処理
    input_image = Image.open(image_path)
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)  # バッチ次元を追加
    return input_batch, input_image

def segment_image(model, input_batch):
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    with torch.no_grad():
        output = model(input_batch)['out'][0]
    output_predictions = output.argmax(0).byte().cpu().numpy()
    return output_predictions

def create_color_map():
    # PASCAL VOC データセットの色マップ
    return np.array([
        [0, 0, 0],          # background
        [128, 0, 0],        # aeroplane
        [0, 128, 0],        # bicycle
        [128, 128, 0],      # bird
        [0, 0, 128],        # boat
        [128, 0, 128],      # bottle
        [0, 128, 128],      # bus
        [128, 128, 128],    # car
        [64, 0, 0],         # cat
        [192, 0, 0],        # chair
        [64, 128, 0],       # cow
        [192, 128, 0],      # diningtable
        [64, 0, 128],       # dog
        [192, 0, 128],      # horse
        [64, 128, 128],     # motorbike
        [192, 128, 128],    # person
        [0, 64, 0],         # pottedplant
        [128, 64, 0],       # sheep
        [0, 192, 0],        # sofa
        [128, 192, 0],      # train
        [0, 64, 128]        # tvmonitor
    ])

def visualize_segmentation(input_image, output_predictions):
    # セグメンテーション結果の可視化
    color_map = create_color_map()
    r = np.zeros_like(output_predictions).astype(np.uint8)
    g = np.zeros_like(output_predictions).astype(np.uint8)
    b = np.zeros_like(output_predictions).astype(np.uint8)

    for l in range(0, 21):
        idx = output_predictions == l
        r[idx] = color_map[l, 0]
        g[idx] = color_map[l, 1]
        b[idx] = color_map[l, 2]

    rgb = np.stack([r, g, b], axis=2)

    plt.figure(figsize=(15, 5))
    plt.subplot(131)
    plt.imshow(input_image)
    plt.title("Original Image")
    plt.axis('off')

    plt.subplot(132)
    plt.imshow(rgb)
    plt.title("Segmentation Result")
    plt.axis('off')

    plt.subplot(133)
    plt.imshow(input_image)
    plt.imshow(rgb, alpha=0.7)
    plt.title("Overlay")
    plt.axis('off')

    plt.tight_layout()
    plt.savefig("segmentation_result.png")
    plt.show()

def main():
    model = load_model()
    image_path = "test_image.jpg"
    input_batch, input_image = preprocess_image(image_path)
    output_predictions = segment_image(model, input_batch)
    visualize_segmentation(input_image, output_predictions)

if __name__ == "__main__":
    main()
