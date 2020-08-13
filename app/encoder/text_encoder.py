import os
import logging
from torch import cuda, device

from transformers import BertTokenizer
from network.text_model import BertForFeatureExtraction

logger = logging.getLogger('root')


class TextEncoder():

    def __init__(self):

        # configuring device
        self.machine_device = 'cuda' if cuda.is_available() else 'cpu'

        # loading the model and tokenizer
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.feature_extractor = BertForFeatureExtraction()
        self.feature_extractor.freeze_bert_encoder()
        self.feature_extractor.to(device(self.machine_device))

        logger.info("Initialised Text Encoder")
        logger.info("Device Used: {}".format(self.machine_device))

    def vectorise(self, batch_text):
        """ Vectorise Text
        Arguments:
        [list] -- [list of str]
        Returns:
            [list] -- [list of tensors]
        """

        input_ids = self.tokenizer.batch_encode_plus(
            batch_text_or_text_pairs=batch_text, add_special_tokens=True, pad_to_max_length=True, return_tensors="pt")['input_ids']

        input_ids.to(device(self.machine_device))
        result = self.feature_extractor(input_ids).cpu().tolist()
        logger.info("Vectorised Text")

        return result
