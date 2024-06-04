from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from db.models.stadiums import Stadium, Seat
from schemas.stadium_schema import StadiumCreate, StadiumRead, StadiumForSeat
from exceptions import (
    StadiumNotFound,
    MaxStadiumSeats,
    StadiumAlreadyExists,
    StadiumNotCreated,
    SeatsNotCreated,
)


class StadiumOperation:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_stadium(self, stadium: StadiumCreate):
        stadium = Stadium(**stadium.model_dump())
        async with self.db as db:
            try:
                db.add(stadium)
                await db.commit()
                await db.refresh(stadium)
                await self.create_seats(stadium_instance=stadium)

                return StadiumRead(
                    id=stadium.id, name=stadium.name, seat_num=stadium.seat_num
                )
            except IntegrityError:
                raise StadiumAlreadyExists
            except SeatsNotCreated as e:
                raise e
            except Exception:
                raise Exception("Statium not created")

    async def create_seats(self, stadium_instance):
        async with self.db as db:
            async with db.begin():
                try:
                    seats = (
                        Seat(num=i + 1, stadium_id=stadium_instance.id)
                        for i in range(stadium_instance.seat_num)
                    )
                    db.add_all(seats)
                    await db.commit()
                    return seats
                except Exception as e:
                    await db.rollback()
                    raise SeatsNotCreated

    async def create_stadium_with_seats(self, stadium: StadiumCreate):
        attempt = 0
        while attempt < 5:  # Retry up to 5 times
            async with self.db as db:
                async with db.begin():
                    try:
                        stadium = Stadium(**stadium.model_dump())
                        db.add(stadium)
                        await db.flush()  # Ensure the stadium ID is generated

                        seats = [
                            Seat(num=i + 1, stadium_id=stadium.id)
                            for i in range(stadium.seat_num)
                        ]
                        db.add_all(seats)

                        await db.commit()
                        return stadium
                    except Exception as e:
                        await db.rollback()
                        print(f"Attempt {attempt+1} failed: {e}")
                        attempt += 1

        raise StadiumNotCreated

    async def get_stadium(self, name):
        async with self.db as db:
            stadium = await db.execute(select(Stadium).where(Stadium.name == name))
            stadium = stadium.scalar_one_or_none()
            if stadium is None:
                raise StadiumNotFound
            return StadiumRead(
                id=stadium.id,
                name=stadium.name,
                seat_num=stadium.seat_num,
                seats=Stadium.seats,
            )

    async def get_stadiums(self, skip: int, limit: int):
        async with self.db as db:
            result = await db.execute(select(Stadium).offset(skip).limit(limit))
            stadiums = result.scalars().all()
            return stadiums

    async def delete_stadium(self, name):
        async with self.db as db:
            result = await db.execute(select(Stadium).where(Stadium.name == name))
            db_stadium = result.scalar_one_or_none()
            if db_stadium is None:
                raise StadiumNotFound
            db.delete(db_stadium)
            await db.commit()
            return db_stadium
