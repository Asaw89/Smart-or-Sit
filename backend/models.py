from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Float,
    DateTime,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from .database import Base
import datetime


class Team(Base):
    __tablename__ = "teams"

    # Columns defined in the spec sheet
    team_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    abbreviation = Column(String(5), unique=True, nullable=False)
    bye_week = Column(Integer, nullable=True)
    logo_url = Column(String(255), nullable=True)

    players = relationship("Player", back_populates="team")


class Player(Base):
    __tablename__ = "players"
    # primary key
    player_id = Column(Integer, primary_key=True, index=True)
    # foreign key
    team_id = Column(Integer, ForeignKey("teams.team_id"))
    # player details
    name = Column(String(100), nullable=False, index=True)
    position = Column(String(5), Nullable=False)
    jersey_number = Column(Integer, nullable=True)
    headshot_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    injury_status = Column(String(20), nullable=True)
    # relationship
    team = relationship("Team", back_populates="players")


class Analysts(Base):
    __tablename__ = "analysts"
    # primary key
    analyst_id = Column(Integer, primary_key=True, index=True)
    # analyst details
    name = Column(String(100), nullable=False, index=True)
    platform = Column(String(50), nullable=False)
    profile_url = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    # Accuracy Stats
    accuracy_score = Column(Float, default=0.0)
    total_predictions = Column(Integer, default=0)
    correct_predictions = Column(Integer, default=0)
    # Relationships
    recommendations = relationship("Recommendation", back_populates="analyst")


class Recommendations(Base):
    __tablename__ = "recommendations"
    # primary key
    recommendation_id = Column(Integer, primary_key=True, index=True)
    # foreign key
    analyst_id = Column(Integer, ForeignKey("analysts.analyst_id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    # rankings
    week = Column(Integer, nullable=False)
    season = Column(Integer, nullable=False)
    designation = Column(String(10), nullable=False)  # Start,Sit,Flex
    project_points = Column(Float, nullable=False)
    position_rank = Column(Integer, nullable=True)
    scoring_format = Column(String(10), nullable=False)  # PPR,Half,Standard
    confidence = Column(String(10), nullable=True)
    analysis_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, Default=datetime.datetime.now)

    # Relationships
    analyst = relationship("Analyst", back_populates="recommendations")
    player = relationship(
        "Player"
    )  # We didn't add back_populates on Player, so this is a one-way link for now, which is fine.

    # Unique Constraint
    # This ensures an analyst can't have duplicate records for the same player/week/format
    __table_args__ = (
        UniqueConstraint(
            "analyst_id",
            "player_id",
            "week",
            "season",
            "scoring_format",
            name="_analyst_player_week_uc",
        ),
    )


class Game(Base):
    __tablename__ = "games"
    # Primary Key
    game_id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    home_team_id = Column(Integer, ForeignKey("analysts.analyst_id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey(""), nullable=False)
