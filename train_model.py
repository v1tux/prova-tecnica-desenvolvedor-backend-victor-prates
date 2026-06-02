from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression


# Caminho onde o modelo treinado será salvo.
MODEL_DIR = Path("model")
MODEL_PATH = MODEL_DIR / "model.joblib"


def train_and_save_model() -> None:
    """
    Treina um modelo simples de regressão linear e salva em arquivo.

    Para esta prova técnica, foi usado um conjunto de dados simples e fictício.
    O objetivo é demonstrar o fluxo de treinamento, persistência do modelo
    com joblib e posterior uso pela API.
    """

    # Dados de entrada fictícios.
    # Cada linha representa uma amostra com três características numéricas.
    # Exemplo: [quantidade, tempo, distância]
    x_train = np.array(
        [
            [1, 10, 100],
            [2, 20, 200],
            [3, 30, 300],
            [4, 40, 400],
            [5, 50, 500],
            [6, 60, 600],
        ]
    )

    # Valores esperados para treinamento.
    # O modelo aprenderá uma relação simples entre as entradas e a saída.
    y_train = np.array([15, 30, 45, 60, 75, 90])

    model = LinearRegression()
    model.fit(x_train, y_train)

    # Garante que a pasta model exista antes de salvar o arquivo.
    MODEL_DIR.mkdir(exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print(f"Modelo treinado e salvo em: {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save_model()