from os.path import join

from torch import nn, load
from torch.nn import functional
import torchvision.models as models

from config import config

resnet_model_path = os.path.join(
    config.MODEL_DIR, "resnet101", "resnet101_imagenet.pt")


class ImageFeatureExtractor(nn.Module):
    def __init__(self, model_config=None):
        super(ImageFeatureExtractor, self).__init__()
        self._config = model_config

        if self._config is None:
            self._config = {
                'outlayer': 'C5',
                "model_path": None,
            }

        self.resnet101 = models.resnet101()
        self.resnet101.load_state_dict(torch.load(resnet_model_path))
        if self._config['outlayer'] == 'C5':
            self.output_layer = nn.Sequential(*(
                list(self.resnet101.children())[:-1]))

        elif self._config['outlayer'] == 'C4':
            self.output_layer = nn.Sequential(*(
                list(self.resnet101.children())[:-3]))
            self.glbAvgPool = nn.AdaptiveAvgPool2d(1)

    def freeze_all_layer(self):
        for p in self.resnet101.parameters():
            p.requires_grad = False

    def freeze_nth_layer(self, n):
        for i, p in enumerate(self.resnet101.parameters()):
            if i < n:
                p.requires_grad = False

    def forward(self, image_variable):
        x = self.output_layer(image_variable)
        if self._config['outlayer'] == 'C4':
            x = self.glbAvgPool(x)

        x = functional.normalize(x, p=2, dim=1)
        x.squeeze_(3)
        x.squeeze_(2)
        return x
