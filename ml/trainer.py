from ml.model import create_model


def train_model(data, labels):
    model = create_model()
    model.fit(data, labels)
    return model