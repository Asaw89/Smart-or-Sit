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
