from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    event,
    func,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from db.engine import Base, get_db
from exceptions import MaxStadiumSeats, StadiumNotFound


class Stadium(Base):
    __tablename__ = "stadiums"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    seat_num = Column(Integer, nullable=False)
    seats = relationship("Seat", back_populates="stadium", cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.name} with {self.seat_num} number seats."

    @hybrid_property
    def seat_count(self):
        return self.seats.with_entities(func.count("*")).scalar()


class Seat(Base):
    __tablename__ = "seats"
    id = Column(Integer, primary_key=True)
    num = Column(Integer, nullable=False)
    stadium_id = Column(Integer, ForeignKey("stadiums.id"))
    stadium = relationship("Stadium", back_populates="seats")

    __table_args__ = (UniqueConstraint("num", "stadium_id", name="num_stadium_uq"),)

    def __str__(self):
        return f"seat num {self.num} from this stadium{self.stadium}"


async def check_seat_limit(mapper, connection, target):
    async with get_db() as session:
        stadium = await session.get(Stadium, target.stadium_id)
        if not stadium:
            raise StadiumNotFound
        if stadium.seat_count >= stadium.seat_num:
            raise MaxStadiumSeats(stadium.name)


# Attach the event listener to the Seat class before insert event
event.listen(Seat, "before_insert", check_seat_limit)
