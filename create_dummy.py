from datetime import datetime
from database.mysql import db
from database.model.pond import Pond, WaterQuality, FishData, FishPondMetrics

# Create dummy data
def create_dummy_data():
    # Create dummy ponds
    pond1 = Pond(pond_name="Pond A", location="Location A")
    pond2 = Pond(pond_name="Pond B", location="Location B")

    # Add ponds to the session
    db.session.add(pond1)
    db.session.add(pond2)
    db.session.commit()

    # Create dummy water quality data
    water_quality1 = WaterQuality(
        pond_id=pond1.pond_id,
        pH=7.2,
        turbidity=30.5,
        temperature=26.0,
        nitrate=10.0,
        date="2024-07-01 10:00:00"
    )
    water_quality2 = WaterQuality(
        pond_id=pond2.pond_id,
        pH=7.5,
        turbidity=40.0,
        temperature=27.0,
        nitrate=15.0,
        date="2024-07-02 11:00:00"
    )

    # Add water quality data to the session
    db.session.add(water_quality1)
    db.session.add(water_quality2)
    db.session.commit()

    # Create dummy fish data
    fish_data1 = FishData(
        pond_id=pond1.pond_id,
        fish_weight=200.0,
        fish_height=30.0,
        fish_population=100,
        date="2024-07-01 10:00:00"
    )
    fish_data2 = FishData(
        pond_id=pond2.pond_id,
        fish_weight=150.0,
        fish_height=25.0,
        fish_population=150,
        date="2024-07-02 11:00:00"
    )

    # Add fish data to the session
    db.session.add(fish_data1)
    db.session.add(fish_data2)
    db.session.commit()

    # Create dummy fish pond metrics
    fish_pond_metrics1 = FishPondMetrics(
        pond_id=pond1.pond_id,
        total_fish_weight=2000.0,
        average_fish_weight=20.0,
        average_fish_height=5.0,
        total_population=100,
        date="2024-07-01 10:00:00"
    )
    fish_pond_metrics2 = FishPondMetrics(
        pond_id=pond2.pond_id,
        total_fish_weight=2250.0,
        average_fish_weight=15.0,
        average_fish_height=4.0,
        total_population=150,
        date="2024-07-02 11:00:00"
    )

    # Add fish pond metrics to the session
    db.session.add(fish_pond_metrics1)
    db.session.add(fish_pond_metrics2)
    db.session.commit()

if __name__ == "__main__":
    db.create_all()  # Ensure all tables are created
    create_dummy_data()
    print("Dummy data inserted successfully.")
