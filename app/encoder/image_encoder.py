import requests
import logging
from io import BytesIO
from torch import cat, cuda, device
from PIL import Image, UnidentifiedImageError


import torchvision.transforms as transforms
from app.network.image_model import ImageFeatureExtractor

logger = logging.getLogger('root')


class ImageEncoder():

    def __init__(self):

        # configuring device
        self.machine_device = 'cuda' if cuda.is_available() else 'cpu'

        # initialising image model
        self.model = ImageFeatureExtractor()
        self.model.freeze_all_layer()
        self.model.eval()

        self.model.to(device(self.machine_device))
        logger.info("Initialised Image Encoder")

        logger.info("Device Used: {}".format(self.machine_device))

    def preprocess_images(self, urls):
        """ Preprocess Images
            Arguments:
                [list] -- [list of urls]
            Returns:
                [tensor] -- [tensor of tensors]
        """

        preprocessed_imgs = []
        for url in urls:
            if url:
                response = requests.get(url)
                image_ = Image.open(BytesIO(response.content))
            else:
                image_ = Image.new('RGB', (300, 300), (0, 0, 0))
            resize = transforms.Resize((300, 300))
            loader = transforms.Compose([resize, transforms.ToTensor()])
            img = loader(image_).float().unsqueeze(0)
            preprocessed_imgs.append(img)
        logger.info("Preprocessed Image Batch")

        return cat(preprocessed_imgs, dim=0)

    def vectorise(self, urls):
        """ Vectorise Images
        Arguments:
            [list] -- [list of urls]
        Returns:
            [list] -- [list of tensors]
        """

        image_inputs = self.preprocess_images(urls)
        image_inputs.to(device(self.machine_device))
        vectors = self.model(image_inputs).cpu().detach().numpy().tolist()
        logger.info("Vectorised Images")
        return vectors
