import requests
from PIL import Image
from io import BytesIO
from torch import cat

import torchvision.transforms as transforms
from network.image_model import ImageFeatureExtractor


# initiating model
model = ImageFeatureExtractor()
model.freeze_all_layer()
model.eval()


def preprocess_images(urls):

    preprocessed_imgs = []

    for url in urls:

        response = requests.get(url)
        image_ = Image.open(BytesIO(response.content))

        resize = transforms.Resize((300, 300))

        loader = transforms.Compose([resize, transforms.ToTensor()])
        img = loader(image_).float().unsqueeze(0)

        preprocessed_imgs.append(img)

    return cat(preprocessed_imgs, dim=0)


def vectorise(urls):

    image_inputs = preprocess_images(urls)

    vectors = model(image_inputs).cpu().detach().numpy().flatten().tolist()

    return vectors
