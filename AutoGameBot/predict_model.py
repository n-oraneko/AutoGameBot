
import global_val as glb
from model_setting import *
from PIL import Image
import torch
import torchvision.transforms as transforms


class prediction_model():
    def __init__(self):
        pass

    def training_init(self):
        self.classes = []
        for button in glb.model_classes_list:
            self.classes.append(button)


        # モデルの読み込み
        self.model = CustomModel(num_classes=len(self.classes))
        self.model.load_state_dict(torch.load('model/custom_model.pth', map_location=torch.device('cpu')))
        self.model.eval()

        # 画像の前処理
        self.transform = transforms.Compose([
            transforms.Resize((600, 800)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ])

    def predict(self,image):
        # 画像の読み込みと前処理
        image = self.transform(image)
        image = image.unsqueeze(0)  # バッチ次元を追加

        # 推論の実行
        with torch.no_grad():
            outputs = self.model(image)
            probabilities = torch.sigmoid(outputs)  # ラベルの確率をシグモイド関数を適用して取得

        # ラベルごとの確率の表示
        label_probabilities = probabilities.squeeze().tolist()  # Tensorをリストに変換
        ret = {}
        for label, probability in zip(self.classes, label_probabilities):
            ret[label] = probability
            #print(f'{label}: {probability:.4f}')
        return ret