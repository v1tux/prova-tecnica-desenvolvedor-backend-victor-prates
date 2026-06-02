from pathlib import Path

import joblib
import numpy as np


MODEL_PATH = Path("model") / "model.joblib"


class PredictionService:
    """
    Serviço responsável por carregar o modelo treinado e realizar predições.

    O modelo é carregado uma vez na criação do serviço, evitando abrir o arquivo
    a cada chamada da rota /predict.
    """

    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Modelo não encontrado em {MODEL_PATH}. "
                "Execute 'python train_model.py' antes de iniciar a API."
            )

        self.model = joblib.load(MODEL_PATH)

    def predict(self, feature_1: float, feature_2: float, feature_3: float) -> float:
        """
        Executa uma predição com base em três valores numéricos.

        O modelo foi treinado esperando três características de entrada.
        Por isso, os valores são convertidos para um array 2D no formato:
        [[feature_1, feature_2, feature_3]]
        """

        input_data = np.array([[feature_1, feature_2, feature_3]])

        prediction = self.model.predict(input_data)

        return float(prediction[0])


prediction_service = PredictionService()