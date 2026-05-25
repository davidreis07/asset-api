# app/routers/assets.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Asset
from app.schemas import AssetCreate, AssetOut

router = APIRouter()

@router.post("/", response_model=AssetOut)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    asset = Asset(
        filename=payload.filename,
        file_type=payload.file_type,
        category=payload.category,
        path=payload.path,
        owner_id=1
    )

    db.add(asset)
    db.commit()
    db.refresh(asset)

    return asset


@router.get("/", response_model=list[AssetOut])
def list_assets(
    file_type: str | None = Query(default=None),
    category: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Asset)

    if file_type:
        query = query.filter(Asset.file_type == file_type)

    if category:
        query = query.filter(Asset.category == category)

    if search:
        query = query.filter(Asset.filename.ilike(f"%{search}%"))

    return query.order_by(Asset.created_at.desc()).all()


@router.get("/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    return asset


@router.put("/{asset_id}", response_model=AssetOut)
def update_asset(asset_id: int, payload: AssetCreate, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    asset.filename = payload.filename
    asset.file_type = payload.file_type
    asset.category = payload.category
    asset.path = payload.path

    db.commit()
    db.refresh(asset)

    return asset


@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    db.delete(asset)
    db.commit()

    return {"message": "Arquivo removido com sucesso"}


@router.get("/dashboard/metrics")
def dashboard_metrics(db: Session = Depends(get_db)):
    total = db.query(Asset).count()
    images = db.query(Asset).filter(Asset.file_type == "image").count()
    documents = db.query(Asset).filter(Asset.file_type == "document").count()
    videos = db.query(Asset).filter(Asset.file_type == "video").count()

    return {
        "total_assets": total,
        "images": images,
        "documents": documents,
        "videos": videos
    }