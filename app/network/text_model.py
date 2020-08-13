""" Feature Extraction Bert"""

from os.path import join

from torch import nn
from transformers import BertModel
from torch.nn import functional


class BertForFeatureExtraction(nn.Module):
    """ Extract Features
    Arguments:
        nn {[token.tensor,token.tensor]} -- [token ids , attention mask]
    Returns:
        [token.tensor] -- [last hidden layer (normalized) output]
    """

    def __init__(self, model_config=None):
        super(BertForFeatureExtraction, self).__init__()
        self._config = model_config
        if self._config is None:
            self._config = {
                "embedding_transform": "",
                "embedding_transform_layers": 4
            }
        self.bert = BertModel.from_pretrained(
            "bert-base-uncased", output_hidden_states=True)
        self.gavg_pool = nn.AdaptiveAvgPool2d((1, 768))

    def forward(self, input_ids, attention_mask=None):

        output, _, hidden_states = self.bert(input_ids, attention_mask)
        embedding_output = hidden_states[0]

        transformed_embedding = output

        embedding_output = self.gavg_pool(transformed_embedding)
        normalized_output = functional.normalize(
            embedding_output, p=2, dim=2)

        # remove the 1 dims for batch and average sentence length
        normalized_output = normalized_output.squeeze()
        return normalized_output

    def freeze_bert_encoder(self):
        for param in self.bert.parameters():
            param.requires_grad = False

    def unfreeze_bert_encoder(self):
        for param in self.bert.parameters():
            param.requires_grad = True
