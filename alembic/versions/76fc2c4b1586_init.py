"""init

Revision ID: 76fc2c4b1586
Revises: 
Create Date: 2023-10-23 04:11:31.701463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '76fc2c4b1586'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genres',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('ident', sa.String(length=30), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('genres_pkey'))
    )
    op.create_index(op.f('genres_id_idx'), 'genres', ['id'], unique=False)
    op.create_table('images',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('path', sa.String(length=256), nullable=False),
    sa.Column('extension', sa.String(length=8), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('images_pkey'))
    )
    op.create_index(op.f('images_id_idx'), 'images', ['id'], unique=False)
    op.create_table('locations',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('x', sa.Float(), nullable=False),
    sa.Column('y', sa.Float(), nullable=False),
    sa.Column('address_name', sa.String(length=150), nullable=False),
    sa.Column('place_name', sa.String(length=150), nullable=False),
    sa.Column('kakao_place_name', sa.String(length=150), nullable=False),
    sa.Column('kakao_place_url', sa.String(length=150), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('locations_pkey'))
    )
    op.create_index(op.f('locations_id_idx'), 'locations', ['id'], unique=False)
    op.create_table('performances',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('running_time', sa.String(length=30), nullable=False),
    sa.Column('grade', sa.String(length=30), nullable=False),
    sa.Column('begin', sa.Date(), nullable=False),
    sa.Column('end', sa.Date(), nullable=False),
    sa.Column('pre_booking_enabled', sa.Boolean(), nullable=False),
    sa.Column('pre_booking_closed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('poster_image_id', sa.Uuid(), nullable=True),
    sa.Column('snowflake_id', sa.BigInteger(), nullable=False),
    sa.Column('genre_idents', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['poster_image_id'], ['images.id'], name=op.f('performances_poster_image_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('performances_pkey'))
    )
    op.create_index(op.f('performances_id_idx'), 'performances', ['id'], unique=False)
    op.create_index(op.f('performances_snowflake_id_idx'), 'performances', ['snowflake_id'], unique=False)
    op.create_table('performers',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('profile_image_id', sa.Uuid(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['profile_image_id'], ['images.id'], name=op.f('performers_profile_image_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('performers_pkey'))
    )
    op.create_index(op.f('performers_id_idx'), 'performers', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('username', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('kakao_id', sa.String(length=256), nullable=True),
    sa.Column('avatar_image_id', sa.Uuid(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['avatar_image_id'], ['images.id'], name=op.f('users_avatar_image_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('users_pkey'))
    )
    op.create_index(op.f('users_email_idx'), 'users', ['email'], unique=True)
    op.create_index(op.f('users_id_idx'), 'users', ['id'], unique=False)
    op.create_index(op.f('users_kakao_id_idx'), 'users', ['kakao_id'], unique=True)
    op.create_index(op.f('users_username_idx'), 'users', ['username'], unique=True)
    op.create_table('areas',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('performance_id', sa.Uuid(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('snowflake_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['performance_id'], ['performances.id'], name=op.f('areas_performance_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('areas_pkey'))
    )
    op.create_index(op.f('areas_id_idx'), 'areas', ['id'], unique=False)
    op.create_index(op.f('areas_snowflake_id_idx'), 'areas', ['snowflake_id'], unique=False)
    op.create_table('discounts',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('performance_id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('discount_rate', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['performance_id'], ['performances.id'], name=op.f('discounts_performance_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('discounts_pkey'))
    )
    op.create_index(op.f('discounts_id_idx'), 'discounts', ['id'], unique=False)
    op.create_table('hot_performances',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('performance_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['performance_id'], ['performances.id'], name=op.f('hot_performances_performance_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('hot_performances_pkey'))
    )
    op.create_index(op.f('hot_performances_id_idx'), 'hot_performances', ['id'], unique=False)
    op.create_table('performance_contents',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('performance_id', sa.Uuid(), nullable=False),
    sa.Column('notice', sa.Text(), nullable=True),
    sa.Column('introduction', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['performance_id'], ['performances.id'], name=op.f('performance_contents_performance_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('performance_contents_pkey'))
    )
    op.create_index(op.f('performance_contents_id_idx'), 'performance_contents', ['id'], unique=False)
    op.create_table('roles',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('performance_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['performance_id'], ['performances.id'], name=op.f('roles_performance_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('roles_pkey'))
    )
    op.create_index(op.f('roles_id_idx'), 'roles', ['id'], unique=False)
    op.create_table('schedules',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('performance_id', sa.Uuid(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['performance_id'], ['performances.id'], name=op.f('schedules_performance_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('schedules_pkey'))
    )
    op.create_index(op.f('schedules_id_idx'), 'schedules', ['id'], unique=False)
    op.create_table('seat_grades',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('performance_id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('snowflake_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['performance_id'], ['performances.id'], name=op.f('seat_grades_performance_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('seat_grades_pkey'))
    )
    op.create_index(op.f('seat_grades_id_idx'), 'seat_grades', ['id'], unique=False)
    op.create_index(op.f('seat_grades_snowflake_id_idx'), 'seat_grades', ['snowflake_id'], unique=False)
    op.create_table('user_genre_likes',
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('genre_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], name=op.f('user_genre_likes_genre_id_fkey')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('user_genre_likes_user_id_fkey')),
    sa.PrimaryKeyConstraint('user_id', 'genre_id', name=op.f('user_genre_likes_pkey'))
    )
    op.create_table('user_performance_likes',
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('performance_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['performance_id'], ['performances.id'], name=op.f('user_performance_likes_performance_id_fkey')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('user_performance_likes_user_id_fkey')),
    sa.PrimaryKeyConstraint('user_id', 'performance_id', name=op.f('user_performance_likes_pkey'))
    )
    op.create_table('user_performer_likes',
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('performer_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['performer_id'], ['performers.id'], name=op.f('user_performer_likes_performer_id_fkey')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('user_performer_likes_user_id_fkey')),
    sa.PrimaryKeyConstraint('user_id', 'performer_id', name=op.f('user_performer_likes_pkey'))
    )
    op.create_table('castings',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('performance_id', sa.Uuid(), nullable=False),
    sa.Column('performer_id', sa.Uuid(), nullable=False),
    sa.Column('role_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['performance_id'], ['performances.id'], name=op.f('castings_performance_id_fkey')),
    sa.ForeignKeyConstraint(['performer_id'], ['performers.id'], name=op.f('castings_performer_id_fkey')),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('castings_role_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('castings_pkey'))
    )
    op.create_index(op.f('castings_id_idx'), 'castings', ['id'], unique=False)
    op.create_table('seats',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('area_id', sa.Uuid(), nullable=False),
    sa.Column('seat_grade_id', sa.Uuid(), nullable=False),
    sa.Column('x', sa.Float(), nullable=False),
    sa.Column('y', sa.Float(), nullable=False),
    sa.Column('row', sa.Integer(), nullable=False),
    sa.Column('col', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('row_col_cursor', sa.Integer(), sa.Computed('(row * 10000) + col', ), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['area_id'], ['areas.id'], name=op.f('seats_area_id_fkey')),
    sa.ForeignKeyConstraint(['seat_grade_id'], ['seat_grades.id'], name=op.f('seats_seat_grade_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('seats_pkey'))
    )
    op.create_index(op.f('seats_id_idx'), 'seats', ['id'], unique=False)
    op.create_index(op.f('seats_row_col_cursor_idx'), 'seats', ['row_col_cursor'], unique=False)
    op.create_table('schedule_casts',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('schedule_id', sa.Uuid(), nullable=False),
    sa.Column('casting_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['casting_id'], ['castings.id'], name=op.f('schedule_casts_casting_id_fkey')),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedules.id'], name=op.f('schedule_casts_schedule_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('schedule_casts_pkey'))
    )
    op.create_index(op.f('schedule_casts_id_idx'), 'schedule_casts', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('schedule_casts_id_idx'), table_name='schedule_casts')
    op.drop_table('schedule_casts')
    op.drop_index(op.f('seats_row_col_cursor_idx'), table_name='seats')
    op.drop_index(op.f('seats_id_idx'), table_name='seats')
    op.drop_table('seats')
    op.drop_index(op.f('castings_id_idx'), table_name='castings')
    op.drop_table('castings')
    op.drop_table('user_performer_likes')
    op.drop_table('user_performance_likes')
    op.drop_table('user_genre_likes')
    op.drop_index(op.f('seat_grades_snowflake_id_idx'), table_name='seat_grades')
    op.drop_index(op.f('seat_grades_id_idx'), table_name='seat_grades')
    op.drop_table('seat_grades')
    op.drop_index(op.f('schedules_id_idx'), table_name='schedules')
    op.drop_table('schedules')
    op.drop_index(op.f('roles_id_idx'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('performance_contents_id_idx'), table_name='performance_contents')
    op.drop_table('performance_contents')
    op.drop_index(op.f('hot_performances_id_idx'), table_name='hot_performances')
    op.drop_table('hot_performances')
    op.drop_index(op.f('discounts_id_idx'), table_name='discounts')
    op.drop_table('discounts')
    op.drop_index(op.f('areas_snowflake_id_idx'), table_name='areas')
    op.drop_index(op.f('areas_id_idx'), table_name='areas')
    op.drop_table('areas')
    op.drop_index(op.f('users_username_idx'), table_name='users')
    op.drop_index(op.f('users_kakao_id_idx'), table_name='users')
    op.drop_index(op.f('users_id_idx'), table_name='users')
    op.drop_index(op.f('users_email_idx'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('performers_id_idx'), table_name='performers')
    op.drop_table('performers')
    op.drop_index(op.f('performances_snowflake_id_idx'), table_name='performances')
    op.drop_index(op.f('performances_id_idx'), table_name='performances')
    op.drop_table('performances')
    op.drop_index(op.f('locations_id_idx'), table_name='locations')
    op.drop_table('locations')
    op.drop_index(op.f('images_id_idx'), table_name='images')
    op.drop_table('images')
    op.drop_index(op.f('genres_id_idx'), table_name='genres')
    op.drop_table('genres')
    # ### end Alembic commands ###
