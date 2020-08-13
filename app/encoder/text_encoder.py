import os
from torch import cuda, device

from transformers import BertTokenizer
from network.text_model import BertForFeatureExtraction

# configuring device
machine_device = 'cuda' if cuda.is_available() else 'cpu'

# loading the model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
feature_extractor = BertForFeatureExtraction()
feature_extractor.freeze_bert_encoder()
feature_extractor.to(device(machine_device))


def vectorise(batch_text):
    """ Vectorise Text
    Arguments:
       [list] -- [list of str]
    Returns:
        [list] -- [list of tensors]
    """

    input_ids = tokenizer.batch_encode_plus(
        batch_text_or_text_pairs=batch_text, add_special_tokens=True, pad_to_max_length=True, return_tensors="pt")['input_ids']

    input_ids.to(device(machine_device))
    result = feature_extractor(input_ids)

    return result
