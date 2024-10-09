import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

# ResNet50 モデルのロード (ImageNetで事前学習済み)
model = ResNet50(weights='imagenet')

def predict_dish(image_path):
    # 画像を読み込んでサイズを調整
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # 画像をモデルに合わせて前処理
    img_array = preprocess_input(img_array)
    
    # 予測を行う
    predictions = model.predict(img_array)
    
    # 結果をデコードして、上位3つの予測を表示
    predicted_classes = decode_predictions(predictions, top=3)[0]
    
    for pred_class, name, score in predicted_classes:
        print(f"{name}: {score:.2%}")

# 使用する画像パスを指定して予測
predict_dish('food2.jpg')
