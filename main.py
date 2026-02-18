from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# ----------------------
# DATABASE SETUP
# ----------------------

DATABASE_URL = "sqlite:///./restaurant.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ----------------------
# DATABASE MODELS
# ----------------------

class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Integer)
    status = Column(String, default="available")


class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    party_size = Column(Integer)
    table_id = Column(Integer)
    status = Column(String)


class Waitlist(Base):
    __tablename__ = "waitlist"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    party_size = Column(Integer)
    priority_score = Column(Integer)


Base.metadata.create_all(bind=engine)

# ----------------------
# APP INIT
# ----------------------

app = FastAPI()

# ----------------------
# TABLE OPTIMIZATION
# ----------------------

def best_fit_table(party_size, tables):
    suitable = [
        t for t in tables
        if t.capacity >= party_size and t.status == "available"
    ]

    if not suitable:
        return None

    suitable.sort(key=lambda x: x.capacity - party_size)
    return suitable[0]

# ----------------------
# PRIORITY SCORING
# ----------------------

def calculate_priority(party_size):
    return 100 - party_size  # smaller parties get higher priority

# ----------------------
# INITIAL TABLE DATA
# ----------------------

@app.on_event("startup")
def load_tables():
    db = SessionLocal()
    if db.query(Table).count() == 0:
        capacities = [2, 2, 4, 4, 6, 8]
        for cap in capacities:
            db.add(Table(capacity=cap))
        db.commit()
    db.close()

# ----------------------
# BOOK RESERVATION
# ----------------------

@app.post("/book")
def book_table(name: str, phone: str, party_size: int):
    db = SessionLocal()

    tables = db.query(Table).all()
    table = best_fit_table(party_size, tables)

    if table:
        table.status = "reserved"

        reservation = Reservation(
            name=name,
            phone=phone,
            party_size=party_size,
            table_id=table.id,
            status="confirmed"
        )

        db.add(reservation)
        db.commit()

        table_id = table.id
        db.close()

        return {"message": f"Reservation confirmed at table {table_id}"}

    else:
        score = calculate_priority(party_size)

        wait_entry = Waitlist(
            name=name,
            phone=phone,
            party_size=party_size,
            priority_score=score
        )

        db.add(wait_entry)
        db.commit()
        db.close()

        return {"message": "No tables available. Added to waitlist."}

# ----------------------
# FREE TABLE + AUTO REALLOCATION
# ----------------------

@app.post("/free_table")
def free_table(table_id: int):
    db = SessionLocal()

    table = db.query(Table).filter(Table.id == table_id).first()

    if not table:
        db.close()
        return {"message": "Table not found"}

    table.status = "available"
    db.commit()

    reassign_from_waitlist(db, table)

    db.close()
    return {"message": "Table freed successfully."}

# ----------------------
# CANCEL RESERVATION
# ----------------------

@app.delete("/reservation/{reservation_id}")
def cancel_reservation(reservation_id: int):
    db = SessionLocal()

    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id,
        Reservation.status.like("confirmed%")
    ).first()

    if not reservation:
        db.close()
        return {"message": "Reservation not found"}

    table = db.query(Table).filter(Table.id == reservation.table_id).first()

    # Cancel reservation
    reservation.status = "cancelled"
    table.status = "available"
    db.commit()

    reassign_from_waitlist(db, table)

    db.close()
    return {"message": "Reservation cancelled successfully."}

# ----------------------
# WAITLIST REALLOCATION LOGIC
# ----------------------

def reassign_from_waitlist(db, table):
    waitlist = db.query(Waitlist)\
                 .order_by(Waitlist.priority_score.desc())\
                 .all()

    for guest in waitlist:
        if guest.party_size <= table.capacity:
            table.status = "reserved"

            new_reservation = Reservation(
                name=guest.name,
                phone=guest.phone,
                party_size=guest.party_size,
                table_id=table.id,
                status="confirmed_from_waitlist"
            )

            db.add(new_reservation)
            db.delete(guest)
            db.commit()
            return

# ----------------------
# VIEW TABLES
# ----------------------

@app.get("/tables")
def view_tables():
    db = SessionLocal()
    tables = db.query(Table).all()

    result = [
        {"id": t.id, "capacity": t.capacity, "status": t.status}
        for t in tables
    ]

    db.close()
    return result

# ----------------------
# VIEW WAITLIST
# ----------------------

@app.get("/waitlist")
def view_waitlist():
    db = SessionLocal()

    guests = db.query(Waitlist)\
               .order_by(Waitlist.priority_score.desc())\
               .all()

    result = [
        {
            "id": g.id,
            "name": g.name,
            "party_size": g.party_size,
            "priority": g.priority_score
        }
        for g in guests
    ]

    db.close()
    return result
# ----------------------
# VIEW RESERVATIONS
# ----------------------

@app.get("/reservations")
def view_reservations():
    db = SessionLocal()

    reservations = db.query(Reservation).all()

    result = [
        {
            "reservation_id": r.id,
            "name": r.name,
            "phone": r.phone,
            "party_size": r.party_size,
            "table_id": r.table_id,
            "status": r.status
        }
        for r in reservations
    ]

    db.close()
    return result

