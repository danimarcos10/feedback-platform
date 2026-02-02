#!/usr/bin/env python3
"""
Quick diagnostic script to test the application components.
Run with: python test_quick.py
"""

import sys

def print_header(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)

def print_ok(msg):
    print(f"  [OK] {msg}")

def print_fail(msg, error=None):
    print(f"  [FAIL] {msg}")
    if error:
        print(f"         Error: {error}")

def test_imports():
    """Test that all modules can be imported."""
    print_header("Testing Imports")
    
    modules = [
        ("FastAPI", "fastapi"),
        ("SQLAlchemy", "sqlalchemy"),
        ("Pydantic", "pydantic"),
        ("Passlib", "passlib.context"),
        ("PyJWT (jose)", "jose"),
        ("VADER Sentiment", "vaderSentiment.vaderSentiment"),
        ("Scikit-learn", "sklearn"),
    ]
    
    all_ok = True
    for name, module in modules:
        try:
            __import__(module)
            print_ok(name)
        except ImportError as e:
            print_fail(name, str(e))
            all_ok = False
    
    return all_ok

def test_app_modules():
    """Test that app modules can be imported."""
    print_header("Testing App Modules")
    
    modules = [
        ("Config", "app.core.config"),
        ("Security", "app.core.security"),
        ("Database Session", "app.db.session"),
        ("User Model", "app.models.user"),
        ("Feedback Model", "app.models.feedback"),
        ("Auth Schemas", "app.schemas.auth"),
        ("Auth Service", "app.services.auth_service"),
        ("Main App", "app.main"),
    ]
    
    all_ok = True
    for name, module in modules:
        try:
            __import__(module)
            print_ok(name)
        except Exception as e:
            print_fail(name, str(e))
            all_ok = False
    
    return all_ok

def test_password_hashing():
    """Test password hashing works."""
    print_header("Testing Password Hashing")
    
    try:
        # Check bcrypt version first
        import bcrypt
        bcrypt_version = getattr(bcrypt, '__version__', 'unknown')
        print_ok(f"bcrypt version: {bcrypt_version}")
        
        from app.core.security import get_password_hash, verify_password
        
        password = "testpassword123"
        hashed = get_password_hash(password)
        print_ok(f"Password hashed: {hashed[:20]}...")
        
        if verify_password(password, hashed):
            print_ok("Password verification works")
        else:
            print_fail("Password verification failed")
            return False
        
        return True
    except Exception as e:
        print_fail("Password hashing", str(e))
        import traceback
        traceback.print_exc()
        return False

def test_jwt_tokens():
    """Test JWT token creation and decoding."""
    print_header("Testing JWT Tokens")
    
    try:
        from app.core.security import create_access_token, decode_access_token
        
        token = create_access_token({"sub": "123"})
        print_ok(f"Token created: {token[:30]}...")
        
        payload = decode_access_token(token)
        if payload and payload.get("sub") == "123":
            print_ok("Token decoding works")
        else:
            print_fail("Token decoding returned wrong data")
            return False
        
        return True
    except Exception as e:
        print_fail("JWT tokens", str(e))
        return False

def test_database_connection():
    """Test database connection."""
    print_header("Testing Database Connection")
    
    try:
        from sqlalchemy import text
        from app.db.session import engine
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print_ok("Database connection works")
            
            # Check tables
            result = conn.execute(text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            ))
            tables = [row[0] for row in result.fetchall()]
            print_ok(f"Tables found: {', '.join(tables)}")
        
        return True
    except Exception as e:
        print_fail("Database connection", str(e))
        return False

def test_user_registration():
    """Test user registration flow (without database)."""
    print_header("Testing User Registration Logic")
    
    try:
        from app.schemas.auth import RegisterRequest
        from app.core.security import get_password_hash
        from app.models.user import User, UserRole
        
        # Test schema validation
        request = RegisterRequest(email="test@example.com", password="testpass123")
        print_ok(f"Schema validation works: {request.email}")
        
        # Test user model creation
        user = User(
            email=request.email,
            hashed_password=get_password_hash(request.password),
            role=UserRole.USER
        )
        print_ok(f"User model creation works: {user.email}, role={user.role}")
        
        return True
    except Exception as e:
        print_fail("User registration logic", str(e))
        import traceback
        traceback.print_exc()
        return False

def test_sentiment_analysis():
    """Test sentiment analysis."""
    print_header("Testing Sentiment Analysis")
    
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        
        analyzer = SentimentIntensityAnalyzer()
        
        texts = [
            ("I love this product!", "positive"),
            ("This is terrible and broken", "negative"),
            ("The meeting is at 3pm", "neutral"),
        ]
        
        for text, expected in texts:
            scores = analyzer.polarity_scores(text)
            compound = scores['compound']
            print_ok(f"'{text[:30]}...' -> {compound:.2f} ({expected})")
        
        return True
    except Exception as e:
        print_fail("Sentiment analysis", str(e))
        return False

def test_full_registration():
    """Test full registration with database."""
    print_header("Testing Full Registration (with DB)")
    
    try:
        from app.db.session import SessionLocal
        from app.services.auth_service import AuthService
        from app.schemas.auth import RegisterRequest
        from app.models.user import User
        import uuid
        
        db = SessionLocal()
        
        # Use unique email to avoid conflicts
        test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        
        try:
            auth_service = AuthService(db)
            request = RegisterRequest(email=test_email, password="testpass123")
            
            user = auth_service.register(request)
            print_ok(f"User registered: {user.email} (ID: {user.id})")
            
            # Clean up - delete test user
            db_user = db.query(User).filter(User.id == user.id).first()
            if db_user:
                db.delete(db_user)
                db.commit()
                print_ok("Test user cleaned up")
            
            return True
        finally:
            db.close()
            
    except Exception as e:
        print_fail("Full registration", str(e))
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*50)
    print("  FEEDBACK PLATFORM - DIAGNOSTIC TEST")
    print("="*50)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("App Modules", test_app_modules()))
    results.append(("Password Hashing", test_password_hashing()))
    results.append(("JWT Tokens", test_jwt_tokens()))
    results.append(("Database Connection", test_database_connection()))
    results.append(("User Registration Logic", test_user_registration()))
    results.append(("Sentiment Analysis", test_sentiment_analysis()))
    results.append(("Full Registration", test_full_registration()))
    
    # Summary
    print_header("SUMMARY")
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    for name, ok in results:
        status = "[OK]" if ok else "[FAIL]"
        print(f"  {status} {name}")
    
    print(f"\n  Results: {passed}/{total} passed")
    
    if passed == total:
        print("\n  All tests passed! The application should work correctly.")
        return 0
    else:
        print("\n  Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
