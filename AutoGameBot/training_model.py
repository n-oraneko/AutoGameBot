"""学習モデルの作成

Todo:
    このpythonファイルを起動することにより、学習モデルを作成または追加学習する。

"""

import global_val as glb
from model_setting import *


class training_model():
    def __init__(self):
        pass

    def training_init(self):
        self.classes = []
        for button in glb.model_classes_list:
            self.classes.append(button)
        
    def add_training(self):
        self.model = CustomModel(num_classes=len(self.classes))
        self.model.load_state_dict(torch.load('model/custom_model.pth', map_location=torch.device('cpu')))


    def create_training(self):
        # モデルのインスタンス化
        self.model = CustomModel(num_classes=len(self.classes))

    def traing(self):
        # ハイパーパラメータの設定
        batch_size = 32
        num_epochs = 10
        learning_rate = 0.001

        # 画像の前処理の定義
        transform = transforms.Compose([
            transforms.Resize((800, 600)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

        # データセットのインスタンス化
        image_folder = 'dataset/images'  # 画像フォルダのパス
        label_folder = 'dataset/labels'  # ラベルフォルダのパス
        dataset = CustomDataset(image_folder, label_folder, transform=transform)

        # データローダーの定義
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)


        # 損失関数と最適化アルゴリズムの定義
        criterion = nn.CrossEntropyLoss()
        optimizer = optim
        # 最適化アルゴリズムの定義
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

        # 学習のループ
        for epoch in range(num_epochs):
            for i, (images, labels) in enumerate(dataloader):
                # 入力データの取得
                images = images.to('cpu')
                labels = labels.to('cpu')

                # モデルの推論
                outputs = self.model(images)

                # 損失の計算
                loss = criterion(outputs, labels)

                # 勾配の初期化とバックワード
                optimizer.zero_grad()
                loss.backward()

                # パラメータの更新
                optimizer.step()

            # ログの出力
            if (epoch + 1) % 1 == 0:
                print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(dataloader)}], Loss: {loss.item():.4f}')

        # 学習モデルの保存
        torch.save(self.model.to('cpu').state_dict(), 'model/custom_model.pth')

if __name__ == '__main__':
    print('[training]training start')
    _training = training_model()
    print('[training]init start')
    _training.training_init()
    print('[training]init done')

    #_training.create_training()
    _training.add_training()

    _training.traing()
    print('[training]training done')