from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ItemFeature, Prediction
from app.schemas import PredictionRequest, PredictionResponse

router = APIRouter(tags=["predictions"])


@router.post("/predictions", response_model=PredictionResponse)
def create_prediction(
    payload: PredictionRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    existing=(
        db.query(Prediction)
        .filter(Prediction.request_id == payload.request_id)
        .first()
    )
    if existing is not None:
        return PredictionResponse(
            request_id=existing.request_id,
            prediction=existing.prediction,
            model_version=existing.model_version
        )
    
    item=(
        db.query(ItemFeature)
        .filter(ItemFeature.item_id == payload.item_id)
        .first()
    )
    print(item)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"'Элемент с id {payload.item_id}' не найден"
        )
    
    features ={
        "item_price": payload.item_price,
        "delivery_days": payload.delivery_days,
        "client_is_app": payload.client_is_app,
        "type_prepayment": payload.type_prepayment,
        "historical_return_rate": item.historical_return_rate,
        "avg_item_losses_30d": item.avg_item_losses_30d
    }

    model=request.app.state.model
    prediction_value=round(model.predict(features),2)

    record = Prediction(
        request_id = payload.request_id,
        prediction=prediction_value,
        model_version=model.version
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return PredictionResponse(request_id = payload.request_id,
        prediction=prediction_value,
        model_version=model.version)
        

@router.get("/predictions/{request_id}", response_model=PredictionResponse)
def get_prediction(request_id: str, db:Session=Depends(get_db)):
    record=(
        db.query(Prediction)
        .filter(Prediction.request_id == request_id)
        .first()
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Предикт с id '{request_id}' не найден"
        )
    
        
    return PredictionResponse(
        request_id = record.request_id,
        prediction=record.prediction,
        model_version=record.model_version
        )