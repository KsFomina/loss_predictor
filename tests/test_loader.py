from app.loader import load_csv, validate_row
from app.models import ItemFeature


def test_validate_row_ok():
    ok, reason = validate_row({
        "item_id": "X", "historical_return_rate": "0.5", "avg_item_losses_30d": "10"
    })
    assert ok and reason is None

def test_validate_row_empty_id():
    ok, reason = validate_row({
        "item_id": "", "historical_return_rate": "0.5", "avg_item_losses_30d": "10"
    })
    assert not ok

def test_validate_row_rate_out_of_range():
    ok, reason = validate_row({
        "item_id": "", "historical_return_rate": "1.1", "avg_item_losses_30d": "10"
    })
    assert not ok

def test_validate_row_negative_losess():
    ok, reason = validate_row({
        "item_id": "", "historical_return_rate": "0.5", "avg_item_losses_30d": "-1"
    })
    assert not ok

def test_load_csv_skip_bad_rows(tmp_path, db_session, monkeypatch):
    class NonClosingSession:
        def __init__(self, real): self._real = real
        def __getattr__(self, name): return getattr(self._real, name)
        def close(self): pass  
    monkeypatch.setattr("app.loader.SessionLocal", lambda: NonClosingSession(db_session))

    csv_file = tmp_path / "features.csv"
    csv_file.write_text(
        "item_id,historical_return_rate,avg_item_losses_30d,updated_at\n"
        "GOOD-1,0.5,100.0,2026-02-28T13:00:00Z\n"
        ",0.5,100.0,2026-02-28T13:00:00Z\n"
        "GOOD-2,1.5,100.0,2026-02-28T13:00:00Z\n"
        "GOOD-3,0.5,-1,2026-02-28T13:00:00Z\n"
        "GOOD-1,0.9,500.0,2026-02-28T13:00:00Z\n"
    )
    
    load_csv(str(csv_file))

    items = {i.item_id: i for i in db_session.query(ItemFeature).all()}
    assert "GOOD-1" in items
    assert items["GOOD-1"].historical_return_rate == 0.9
    assert items["GOOD-1"].avg_item_losses_30d == 500.0
    assert "GOOD-2" not in items
    assert "GOOD-3" not in items
    

