import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image, ImageFilter
import pathlib
import json

class model_setting():
    def __init__(self):
        pass

# データセットの定義
class CustomDataset(Dataset):
    def __init__(self, image_folder, label_folder, transform=None):
        self.image_folder = image_folder
        self.label_folder = label_folder
        self.transform = transform
        self.image_set = [pathlib.Path(i).stem for i in pathlib.Path(image_folder).glob('*.jpg')]
        # ラベル情報の読み込み
        self.label_set = []
        for idx in range(len(self.image_set)):
            with open(label_folder+'/'+str(self.image_set[idx])+'.json') as f:
                #j = json.load(f).values()
                self.label_set.append(list(json.load(f).values()))


    def __len__(self):
        return len(self.label_set)

    def __getitem__(self, index):
        # 画像の読み込み
        image_path = self.image_folder +'/'+self.image_set[index]+'.jpg'  # 画像ファイル名の例
        image = Image.open(image_path).convert('RGB')

        # 画像の前処理
        if self.transform is not None:
            image = self.transform(image)

        # ラベルの読み込み
        label = torch.Tensor(self.label_set[index])

        return image, label


# モデルの定義
class CustomModel(nn.Module):
    def __init__(self, num_classes):
        super(CustomModel, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc = nn.Linear(128 * 200 * 150, num_classes)  # 800x600の画像サイズに合わせて計算

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x