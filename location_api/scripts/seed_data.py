from app.db.session import SessionLocal
from app.db import models

def main():
    db = SessionLocal()
    try:
        if db.query(models.Country).count() > 0:
            print("Data already seeded.")
            return

        india = models.Country(code="IN", name="India", translations={"hi": {"name": "भारत"}})
        usa = models.Country(code="US", name="United States", translations={"es": {"name": "Estados Unidos"}})
        db.add_all([india, usa])
        db.flush()

        tn = models.State(country_id=india.id, code="TN", name="Tamil Nadu")
        ka = models.State(country_id=india.id, code="KA", name="Karnataka")
        ca = models.State(country_id=usa.id, code="CA", name="California")
        db.add_all([tn, ka, ca])
        db.flush()

        chennai = models.City(state_id=tn.id, name="Chennai", code="CHE", latitude=13.0827, longitude=80.2707)
        coimbatore = models.City(state_id=tn.id, name="Coimbatore", code="CBE", latitude=11.0168, longitude=76.9558)
        sf = models.City(state_id=ca.id, name="San Francisco", code="SFO", latitude=37.7749, longitude=-122.4194)
        db.add_all([chennai, coimbatore, sf])
        db.flush()

        towns = [
            models.Town(city_id=chennai.id, name="T. Nagar"),
            models.Town(city_id=chennai.id, name="Velachery"),
            models.Town(city_id=coimbatore.id, name="Gandhipuram"),
            models.Town(city_id=sf.id, name="Sunset District"),
        ]
        db.add_all(towns)
        db.commit()
        print("Seed complete.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
