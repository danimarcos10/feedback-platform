"""
Seed script for demo data.
Creates admin user, demo user, categories, tags, and sample feedback.
"""
import logging
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.category import Category
from app.models.tag import Tag
from app.models.feedback import Feedback, FeedbackStatus
from app.services.feedback_service import FeedbackService

logger = logging.getLogger(__name__)

# Sample feedback data with varying sentiments
SAMPLE_FEEDBACK = [
    # Negative feedback
    {"title": "Terrible UI experience", "content": "The interface is confusing and clunky. I can't find basic features and the navigation is awful.", "sentiment": "negative"},
    {"title": "Login keeps failing", "content": "I've tried multiple times but the login is broken. Getting error messages constantly.", "sentiment": "negative"},
    {"title": "App is unusable on mobile", "content": "The mobile experience is terrible. Buttons are too small and the layout is completely broken on my phone.", "sentiment": "negative"},
    {"title": "Slow performance issues", "content": "Everything takes forever to load. The app is painfully slow and frustrating to use.", "sentiment": "negative"},
    {"title": "Buggy checkout process", "content": "Lost my cart twice due to bugs. The checkout is broken and unreliable.", "sentiment": "negative"},
    {"title": "Awful error handling", "content": "When something goes wrong, I just see a blank screen. No helpful error messages at all.", "sentiment": "negative"},
    {"title": "Hate the new update", "content": "The recent update made everything worse. Please revert to the old version.", "sentiment": "negative"},
    
    # Neutral feedback
    {"title": "Feature request: dark mode", "content": "It would be nice to have a dark mode option for nighttime use.", "sentiment": "neutral"},
    {"title": "Question about export", "content": "Is there a way to export data to CSV? I couldn't find this option anywhere.", "sentiment": "neutral"},
    {"title": "Suggestion for dashboard", "content": "Maybe consider adding more customization options to the dashboard layout.", "sentiment": "neutral"},
    {"title": "Mobile app availability", "content": "Are there plans for a dedicated mobile app in the future?", "sentiment": "neutral"},
    {"title": "Documentation feedback", "content": "The help docs could use some more examples for common use cases.", "sentiment": "neutral"},
    {"title": "Keyboard shortcuts", "content": "Would be helpful to have keyboard shortcuts for common actions.", "sentiment": "neutral"},
    {"title": "Integration question", "content": "Does this integrate with Slack or Microsoft Teams?", "sentiment": "neutral"},
    {"title": "Account settings", "content": "Could you add an option to change username in settings?", "sentiment": "neutral"},
    
    # Positive feedback
    {"title": "Amazing new feature!", "content": "Love the new analytics dashboard! It's intuitive and really helpful for tracking progress.", "sentiment": "positive"},
    {"title": "Great customer support", "content": "The support team was amazing and resolved my issue quickly. Thank you!", "sentiment": "positive"},
    {"title": "Smooth onboarding", "content": "Just signed up and the onboarding process was clean and easy to follow.", "sentiment": "positive"},
    {"title": "Perfect for our team", "content": "This tool is exactly what we needed. Great job on making it so intuitive!", "sentiment": "positive"},
    {"title": "Love the simplicity", "content": "Finally a product that doesn't overcomplicate things. The UI is clean and beautiful.", "sentiment": "positive"},
    {"title": "Excellent performance", "content": "The app is super fast and responsive. Really impressed with the performance.", "sentiment": "positive"},
    {"title": "Best in class", "content": "Tried many similar tools but this is by far the best. Intuitive and powerful.", "sentiment": "positive"},
    {"title": "Fantastic update", "content": "The latest update is amazing! All the new features work perfectly.", "sentiment": "positive"},
    {"title": "Recommend to everyone", "content": "Already recommended this to all my colleagues. Such a great product!", "sentiment": "positive"},
    {"title": "Worth every penny", "content": "The value you get is incredible. Smooth experience and great features.", "sentiment": "positive"},
]

CATEGORIES = ["UI/UX", "Bugs", "Feature Request", "Performance"]
TAGS = ["ui", "login", "slow", "mobile", "layout", "dashboard", "analytics", "support"]


def seed():
    """Main seed function - creates demo data if not exists."""
    db = SessionLocal()
    try:
        logger.info("=" * 50)
        logger.info("Starting seed process...")
        
        # Create admin user
        admin = create_admin_user(db)
        
        # Create demo user
        demo_user = create_demo_user(db)
        
        # Create categories
        categories = create_categories(db)
        
        # Create tags
        tags = create_tags(db)
        
        # Create sample feedback
        create_sample_feedback(db, demo_user, admin, categories, tags)
        
        logger.info("Seed process completed successfully!")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"Seed process failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_admin_user(db: Session) -> User:
    """Create admin user if not exists."""
    admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    
    if not admin:
        admin = User(
            email=settings.ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        logger.info(f"Created admin user: {settings.ADMIN_EMAIL}")
    else:
        logger.info(f"Admin user already exists: {settings.ADMIN_EMAIL}")
    
    return admin


def create_demo_user(db: Session) -> User:
    """Create demo user if not exists."""
    demo_user = db.query(User).filter(User.email == settings.DEMO_USER_EMAIL).first()
    
    if not demo_user:
        demo_user = User(
            email=settings.DEMO_USER_EMAIL,
            hashed_password=get_password_hash(settings.DEMO_USER_PASSWORD),
            role=UserRole.USER
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        logger.info(f"Created demo user: {settings.DEMO_USER_EMAIL}")
    else:
        logger.info(f"Demo user already exists: {settings.DEMO_USER_EMAIL}")
    
    return demo_user


def create_categories(db: Session) -> list[Category]:
    """Create default categories if not exist."""
    categories = []
    
    for cat_name in CATEGORIES:
        category = db.query(Category).filter(Category.name == cat_name).first()
        if not category:
            category = Category(name=cat_name)
            db.add(category)
            db.commit()
            db.refresh(category)
            logger.info(f"Created category: {cat_name}")
        categories.append(category)
    
    return categories


def create_tags(db: Session) -> list[Tag]:
    """Create default tags if not exist."""
    tags = []
    
    for tag_name in TAGS:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
            logger.info(f"Created tag: {tag_name}")
        tags.append(tag)
    
    return tags


def create_sample_feedback(
    db: Session,
    demo_user: User,
    admin: User,
    categories: list[Category],
    tags: list[Tag]
) -> None:
    """Create sample feedback items if demo data doesn't exist."""
    # Check if demo feedback already exists by looking for a specific title
    demo_marker = db.query(Feedback).filter(
        Feedback.title == "Terrible UI experience"
    ).first()
    
    if demo_marker:
        logger.info("Demo feedback already exists, skipping seed")
        return
    
    logger.info("Creating sample feedback items...")
    
    # Use the FeedbackService to properly calculate sentiment
    feedback_service = FeedbackService(db)
    
    statuses = [
        FeedbackStatus.NEW,
        FeedbackStatus.NEW,
        FeedbackStatus.TRIAGED,
        FeedbackStatus.TRIAGED,
        FeedbackStatus.IN_PROGRESS,
        FeedbackStatus.IN_PROGRESS,
        FeedbackStatus.RESOLVED,
        FeedbackStatus.REJECTED,
    ]
    
    for i, feedback_data in enumerate(SAMPLE_FEEDBACK):
        # Spread feedback across the last 14 days
        days_ago = random.randint(0, 13)
        hours_ago = random.randint(0, 23)
        created_at = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago)
        
        # Calculate sentiment score using the service
        combined_text = f"{feedback_data['title']} {feedback_data['content']}"
        sentiment_score = feedback_service._calculate_sentiment(combined_text)
        sentiment_label = get_sentiment_label(sentiment_score, combined_text)
        
        # Assign random category and tags
        category = random.choice(categories)
        feedback_tags = random.sample(tags, k=random.randint(1, 3))
        
        # Assign status (more variety)
        status = random.choice(statuses)
        
        feedback = Feedback(
            user_id=demo_user.id,
            title=feedback_data["title"],
            content=feedback_data["content"],
            category_id=category.id,
            status=status,
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            created_at=created_at,
            updated_at=created_at,
            resolved_at=created_at if status == FeedbackStatus.RESOLVED else None
        )
        feedback.tags = feedback_tags
        
        db.add(feedback)
    
    db.commit()
    logger.info(f"Created {len(SAMPLE_FEEDBACK)} sample feedback items")


def get_sentiment_label(score: float, text: str) -> str:
    """
    Get sentiment label from score with keyword override.
    Uses improved thresholds and proper word matching.
    """
    import re
    
    # Extract individual words (not substrings) for accurate matching
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
    words = set(cleaned.split())
    
    # Strong keyword overrides - exact word matches only
    strong_negative = {"terrible", "awful", "unusable", "hate", "broken", "worst", "horrible"}
    strong_positive = {"amazing", "love", "perfect", "excellent", "fantastic", "great", "best"}
    
    if words & strong_negative:  # Set intersection
        return "negative"
    if words & strong_positive:  # Set intersection
        return "positive"
    
    # Use improved thresholds
    if score <= -0.20:
        return "negative"
    elif score >= 0.20:
        return "positive"
    else:
        return "neutral"


if __name__ == "__main__":
    # Allow running directly for testing
    logging.basicConfig(level=logging.INFO)
    seed()
