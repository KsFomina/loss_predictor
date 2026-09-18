import csv
from datetime import datetime
import sys
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from app.database import SessionLocal
from app.models import ItemFeature

def parse_updated_at(value:str)-> datetime|None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except:
        return None
    

def validate_row(row:dict) -> tuple[bool, str|None]:
    # сразу подготовила сообщения о неккоректных строках, если в дальнейшем решим логировать процесс обработки
    item_id=(row.get("item_id") or "").strip()
    if not item_id:
        return False, "пустой item_id"
    try:
        hrr= float(row["historical_return_rate"])
    except:
        return False, "historical_return_rate не число"
    if not( 0<=hrr<=1):
        return False, "historical_return_rate вне [0,1]"
    
    try:
        losses= float(row["avg_item_losses_30d"])
    except:
        return False, "avg_item_losses_30d не число"
    
    if losses < 0:
        return False, "avg_item_losses_30d < 0"
    
    return True, None

def load_csv(path:str)-> dict:
    session =SessionLocal()
    try:
        with open(path, newline="") as f:
            reader=csv.DictReader(f)
            for row in reader:
                ok,reason = validate_row(row)
                if not ok:
                    print(reason)
                    continue
                value={
                    "item_id": row["item_id"].strip(),
                    "historical_return_rate": float(row["historical_return_rate"].strip()),
                    "avg_item_losses_30d": float(row["avg_item_losses_30d"].strip()),
                    "updated_at": parse_updated_at(row.get("updated_at", "")),
                }

                stmt =sqlite_insert(ItemFeature).values(**value)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["item_id"],
                    set_={
                        "historical_return_rate": value["historical_return_rate"],
                        "avg_item_losses_30d": value["avg_item_losses_30d"],
                        "updated_at": value["updated_at"],
                    },
                )
                session.execute(stmt)

        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m app.loader <path_to_csv>")
        sys.exit(1)

    load_csv(sys.argv[1])