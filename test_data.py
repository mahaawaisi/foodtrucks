from sqlalchemy import create_engine, MetaData, Table, select

# Set up SQLite database engine
db_name = "foodtrucktest"
engine = create_engine(f"sqlite:///{db_name}.db")

# Reflect the existing database schema
metadata = MetaData()
metadata.reflect(bind=engine)

print(metadata.tables.keys())
# Get the 'data' table from the reflected metadata

data_table = Table('data', metadata, autoload=True)

# Establish a connection to the database
with engine.connect() as conn:
    try:
        # Select all rows from the 'data' table
        result = conn.execute(data_table.select())

        # Fetch all rows
        rows = result.fetchall()

        # Print the rows
        for row in rows:
            print(row)

    except Exception as e:
        print("Error executing query:", e)