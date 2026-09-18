from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.database import Base, get_db
from app.models import ItemFeature
from app.routes import router


@pytest.fixture
def db_session():
    engine=create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)
    TestingSession=sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session=TestingSession()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    app=FastAPI()
    app.include_router(router)

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    class FakeModel:
        version ="test-1.0.0"
        def predict(self, features):
            return 501.34
        
    app.state.model = FakeModel()
    return TestClient(app)

@pytest.fixture
def item_in_db(db_session):
    item=ItemFeature(
        item_id="ITEM-001",
        historical_return_rate=0.773956,
        avg_item_losses_30d=623.1971,
    )

    db_session.add(item)
    db_session.commit()
    return item

    

    