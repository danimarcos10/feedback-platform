from fastapi import APIRouter, HTTPException, status

from app.api.deps import DBSession, CurrentAdmin, CurrentUser
from app.schemas.tag import TagCreate, TagUpdate, TagResponse
from app.models.tag import Tag

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("/", response_model=list[TagResponse])
def list_tags(
    db: DBSession,
    current_user: CurrentUser
):
    """List all tags."""
    tags = db.query(Tag).order_by(Tag.name).all()
    return [TagResponse.model_validate(t) for t in tags]


@router.post("/", response_model=TagResponse)
def create_tag(
    request: TagCreate,
    db: DBSession,
    admin: CurrentAdmin
):
    """Create a new tag (admin only)."""
    # Check if exists
    existing = db.query(Tag).filter(Tag.name == request.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag already exists"
        )
    
    tag = Tag(name=request.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    
    return TagResponse.model_validate(tag)


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: int,
    request: TagUpdate,
    db: DBSession,
    admin: CurrentAdmin
):
    """Update a tag (admin only)."""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    if request.name:
        # Check for duplicate
        existing = db.query(Tag).filter(
            Tag.name == request.name,
            Tag.id != tag_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag name already exists"
            )
        tag.name = request.name
    
    db.commit()
    db.refresh(tag)
    
    return TagResponse.model_validate(tag)


@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    db: DBSession,
    admin: CurrentAdmin
):
    """Delete a tag (admin only)."""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    db.delete(tag)
    db.commit()
    
    return {"message": "Tag deleted successfully"}
