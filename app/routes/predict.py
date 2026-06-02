from fastapi import APIRouter, Depends, HTTPException, status

from app.models import User
from app.schemas import PredictionRequest, PredictionResponse
from app.security import get_current_user
from app.services.prediction_service import prediction_service

router = APIRouter(
    prefix="/predict",
    tags=["Predição"],
)


@router.post("/", response_model=PredictionResponse)
def predict(
    data: PredictionRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Realiza uma predição com base em três características numéricas.

    A entrada é validada pelo schema PredictionRequest.
    Depois, os valores são enviados para o serviço de predição,
    que utiliza o modelo treinado salvo em model/model.joblib.
    """
    try:
        prediction = prediction_service.predict(
            feature_1=data.feature_1,
            feature_2=data.feature_2,
            feature_3=data.feature_3,
        )

        return PredictionResponse(prediction=prediction)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao realizar predição: {str(error)}",
        )