"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.Enum('user', 'admin', name='userrole'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_categories_id', 'categories', ['id'])
    op.create_index('ix_categories_name', 'categories', ['name'], unique=True)

    # Create tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tags_id', 'tags', ['id'])
    op.create_index('ix_tags_name', 'tags', ['name'], unique=True)

    # Create feedback table
    op.create_table(
        'feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum('new', 'triaged', 'in_progress', 'resolved', 'rejected', name='feedbackstatus'), nullable=False),
        sa.Column('sentiment_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_feedback_id', 'feedback', ['id'])
    op.create_index('ix_feedback_user_id', 'feedback', ['user_id'])
    op.create_index('ix_feedback_category_id', 'feedback', ['category_id'])
    op.create_index('ix_feedback_status', 'feedback', ['status'])

    # Create feedback_tags table (many-to-many)
    op.create_table(
        'feedback_tags',
        sa.Column('feedback_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['feedback_id'], ['feedback.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('feedback_id', 'tag_id')
    )

    # Create status_events table (audit trail)
    op.create_table(
        'status_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('feedback_id', sa.Integer(), nullable=False),
        sa.Column('old_status', sa.String(50), nullable=True),
        sa.Column('new_status', sa.String(50), nullable=False),
        sa.Column('changed_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['feedback_id'], ['feedback.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['changed_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_status_events_id', 'status_events', ['id'])
    op.create_index('ix_status_events_feedback_id', 'status_events', ['feedback_id'])
    op.create_index('ix_status_events_changed_by', 'status_events', ['changed_by'])

    # Create admin_responses table
    op.create_table(
        'admin_responses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('feedback_id', sa.Integer(), nullable=False),
        sa.Column('admin_id', sa.Integer(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['feedback_id'], ['feedback.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['admin_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_admin_responses_id', 'admin_responses', ['id'])
    op.create_index('ix_admin_responses_feedback_id', 'admin_responses', ['feedback_id'])
    op.create_index('ix_admin_responses_admin_id', 'admin_responses', ['admin_id'])


def downgrade() -> None:
    op.drop_table('admin_responses')
    op.drop_table('status_events')
    op.drop_table('feedback_tags')
    op.drop_table('feedback')
    op.drop_table('tags')
    op.drop_table('categories')
    op.drop_table('users')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS feedbackstatus')
    op.execute('DROP TYPE IF EXISTS userrole')
