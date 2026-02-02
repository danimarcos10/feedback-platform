from fastapi import APIRouter, HTTPException, status

from app.api.deps import DBSession, CurrentAdmin, CurrentUser
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.models.category import Category

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryResponse])
def list_categories(
    db: DBSession,
    current_user: CurrentUser
):
    """List all categories."""
    categories = db.query(Category).order_by(Category.name).all()
    return [CategoryResponse.model_validate(c) for c in categories]


@router.post("/", response_model=CategoryResponse)
def create_category(
    request: CategoryCreate,
    db: DBSession,
    admin: CurrentAdmin
):
    """Create a new category (admin only)."""
    # Check if exists
    existing = db.query(Category).filter(Category.name == request.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"
        )
    
    category = Category(name=request.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return CategoryResponse.model_validate(category)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    request: CategoryUpdate,
    db: DBSession,
    admin: CurrentAdmin
):
    """Update a category (admin only)."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    if request.name:
        # Check for duplicate
        existing = db.query(Category).filter(
            Category.name == request.name,
            Category.id != category_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists"
            )
        category.name = request.name
    
    db.commit()
    db.refresh(category)
    
    return CategoryResponse.model_validate(category)


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: DBSession,
    admin: CurrentAdmin
):
    """Delete a category (admin only)."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": "Category deleted successfully"}
