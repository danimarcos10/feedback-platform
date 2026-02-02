"""Add sentiment_label column to feedback table

Revision ID: 002
Revises: 001
Create Date: 2026-02-03

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Add sentiment_label column to feedback table
    op.add_column('feedback', sa.Column('sentiment_label', sa.String(20), nullable=True))
    
    # Create index for sentiment_label for faster filtering
    op.create_index('ix_feedback_sentiment_label', 'feedback', ['sentiment_label'])
    
    # Update existing rows to have a sentiment_label based on their score
    # This is a simple migration that sets labels based on existing scores
    op.execute("""
        UPDATE feedback 
        SET sentiment_label = CASE 
            WHEN sentiment_score <= -0.20 THEN 'negative'
            WHEN sentiment_score >= 0.20 THEN 'positive'
            ELSE 'neutral'
        END
        WHERE sentiment_score IS NOT NULL
    """)


def downgrade():
    op.drop_index('ix_feedback_sentiment_label', table_name='feedback')
    op.drop_column('feedback', 'sentiment_label')
