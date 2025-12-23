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
