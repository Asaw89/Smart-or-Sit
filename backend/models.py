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
    position = Column(String(5), nullable=False)
    jersey_number = Column(Integer, nullable=True)
    headshot_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    injury_status = Column(String(20), nullable=True)
    # relationship
    team = relationship("Team", back_populates="players")


class Analyst(Base):
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


class Recommendation(Base):
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
    projected_points = Column(Float, nullable=False)
    position_rank = Column(Integer, nullable=True)
    scoring_format = Column(String(10), nullable=False)  # PPR,Half,Standard
    confidence = Column(String(10), nullable=True)
    analysis_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

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
    home_team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)

    # attributes
    week = Column(Integer, nullable=False)
    season = Column(Integer, nullable=False)
    status = Column(String(20), default="Scheduled")  # Scheduled,Live,Final
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    time_remaining = Column(String(10), nullable=True)

    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])


class ActualPerformance(Base):
    """Actual fantasy points and stats scored by players"""

    __tablename__ = "actual_performances"

    # Primary Key
    performance_id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.game_id"), nullable=False)

    # Context
    week = Column(Integer, nullable=False)
    season = Column(Integer, nullable=False)
    opponent = Column(String(10), nullable=True)  # e.g., "@CLE", "vs BAL"
    game_result = Column(String(20), nullable=True)  # e.g., "W 24-17"

    # Fantasy Points
    points_ppr = Column(Float, default=0.0)
    points_half = Column(Float, default=0.0)
    points_standard = Column(Float, default=0.0)

    # Passing Stats
    pass_completions = Column(Integer, default=0)
    pass_attempts = Column(Integer, default=0)
    pass_yards = Column(Integer, default=0)
    pass_tds = Column(Integer, default=0)
    interceptions = Column(Integer, default=0)

    # Rushing Stats
    rush_carries = Column(Integer, default=0)
    rush_yards = Column(Integer, default=0)
    rush_tds = Column(Integer, default=0)

    # Receiving Stats
    receptions = Column(Integer, default=0)
    rec_yards = Column(Integer, default=0)
    rec_tds = Column(Integer, default=0)
    targets = Column(Integer, default=0)

    # Misc
    fumbles_lost = Column(Integer, default=0)

    # DST Stats
    dst_tackles = Column(Integer, default=0)
    dst_sacks = Column(Integer, default=0)
    dst_forced_fumbles = Column(Integer, default=0)
    dst_fumble_recoveries = Column(Integer, default=0)
    dst_interceptions = Column(Integer, default=0)
    dst_int_return_tds = Column(Integer, default=0)
    dst_fumble_return_tds = Column(Integer, default=0)
    dst_points_allowed = Column(Integer, default=0)

    # Kicking Stats
    kick_fg_made_0_39 = Column(Integer, default=0)
    kick_fg_att_0_39 = Column(Integer, default=0)
    kick_fg_made_40_49 = Column(Integer, default=0)
    kick_fg_att_40_49 = Column(Integer, default=0)
    kick_fg_made_50_plus = Column(Integer, default=0)
    kick_fg_att_50_plus = Column(Integer, default=0)
    kick_xp_made = Column(Integer, default=0)
    kick_xp_att = Column(Integer, default=0)

    # Metadata
    updated_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )

    # Relationships
    player = relationship("Player", back_populates="performances")
    game = relationship("Game", back_populates="performances")

    # Unique Constraint
    __table_args__ = (
        UniqueConstraint(
            "player_id",
            "game_id",
            name="_player_game_uc",
        ),
    )
