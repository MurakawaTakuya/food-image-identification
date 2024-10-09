import os
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'GoogleCloudKey.json'

client = vision.ImageAnnotatorClient()

def detect_objects(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    print('Detected objects:')
    for obj in objects:
        print(f'{obj.name} (confidence: {obj.score:.2f})')

    categories = {
        'vegetables': ['vegetable', 'carrot', 'lettuce', 'tomato', 'spinach', 'broccoli', 'cucumber', 'pepper'],
        'meats': ['beef', 'chicken', 'pork', 'meat', 'lamb', 'turkey', 'bacon'],
        'rice_dishes': ['rice', 'sushi', 'risotto']
    }

    counts = {'vegetables': 0, 'meats': 0, 'rice_dishes': 0}

    for obj in objects:
        name = obj.name.lower()
        for category, keywords in categories.items():
            if any(keyword in name for keyword in keywords):
                counts[category] += 1

    total_detected = sum(counts.values())

    if total_detected > 0:
        print("\nEstimated food composition:")
        for category, count in counts.items():
            percentage = (count / total_detected) * 100
            print(f'{category}: {percentage:.2f}%')
    else:
        print("No food-related objects detected.")

detect_objects('food.jpg')
