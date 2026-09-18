

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker


from app.config import MODEL_METADATA_PATH, MODEL_PATH
from app.database import Base, get_db
from app.ml import ModelWrapper
from app.models import ItemFeature
from app.routes import router


@pytest.fixture
def real_client():
    engine = create_engine(
         "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(ItemFeature(
        item_id="ITEM-001",
        historical_return_rate=0.773956,
        avg_item_losses_30d=623.1971,
    ))
    session.commit()
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = override_get_db
    app.state.model = ModelWrapper(MODEL_PATH, MODEL_METADATA_PATH)

    yield TestClient(app)
    session.close()

def test_full_scenario_real_model(real_client):
    payload = {
        "request_id": "full-1",
        "item_id": "ITEM-001",
        "item_price": 2500.0,
        "delivery_days": 4,
        "client_is_app": True,
        "type_prepayment": "card",
    }
    resp = real_client.post("/predictions", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert abs(body["prediction"] - 501.34) < 0.01     
    assert body["model_version"] == "1.0.0"