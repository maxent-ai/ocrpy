import io
from PIL import Image
from typing import List
from attrs import define, field
from ocrpy import DocumentReader
from transformers import AutoFeatureExtractor, AutoModelForImageClassification

__all__ = ["DocumentClassifier"]


@define
class DocumentClassifier:
    """
    DocumentClassifier utilises a fine tuned Document image classifier (DiT) model
    to predict the document type.
    The default model is a dit-base model trained on the rvlcdip dataset.

    You can also choose alternate models available on HuggingFace modelshub
    at https://huggingface.co/models.

    Attributes
    ----------
    model_name : str
        The name of the model to use.
        Should be a valid model name from HuggingFace modelshub.

        default: "microsoft/dit-base-finetuned-rvlcdip"

    Note
    ----
    - The model is trained on the rvlcdip dataset and can identify the following document types:

    letter, form, email, handwritten, advertisement, scientific report, scientific publication,
    specification, file folder, news article, budget, invoice, presentation, questionnaire, resume, memo

    - For more information on the model please refer this paper: https://arxiv.org/abs/2203.02378

    - For more information on the document types, see this link: https://www.cs.cmu.edu/~aharley/rvl-cdip/
    """

    model_name: str = field(default="microsoft/dit-base-finetuned-rvlcdip")
    feature_extractor: AutoFeatureExtractor = field(
        default=None, init=False, repr=False
    )
    classifier: AutoModelForImageClassification = field(
        default=None, init=False, repr=False
    )

    def __attrs_post_init__(self):
        self.feature_extractor = AutoFeatureExtractor.from_pretrained(self.model_name)
        self.classifier = AutoModelForImageClassification.from_pretrained(
            self.model_name
        )

    def _bytes_to_img(self, reader):
        data = reader.read()
        if isinstance(data, bytes):
            data = [data]
        docs = []
        for page in data:
            try:
                img = Image.open(io.BytesIO(page)).convert("RGB")
                docs.append(img)
            except Exception as ex:
                print(ex)
                continue
        return docs

    def _classifier(self, images):
        inputs = self.feature_extractor(images=images, return_tensors="pt")
        outputs = self.classifier(**inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).tolist()
        labels = [self.classifier.config.id2label[i] for i in predicted_class_idx]
        return labels

    def predict(self, reader: DocumentReader) -> List:
        """
        Predict the document type of the document in the reader.

        Parameters
        ----------
        reader : DocumentReader
            The reader containing the document to predict.

        Returns
        -------
        predicted_labels: List
            A list of predicted document types.

        Note
        ----

        document types can be one of the following:
        letter, form, email, handwritten, advertisement, scientific report, scientific publication,
        specification, file folder, news article, budget, invoice, presentation, questionnaire, resume, memo
        """
        images = self._bytes_to_img(reader)
        predicted_labels = self._classifier(images)
        return predicted_labels
