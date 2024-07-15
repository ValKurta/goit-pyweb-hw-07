from database import engine, Base
from models import Groups, Teachers, Subjects, Students, Grades

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)
print("All tables dropped.")

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("All tables created successfully.")
