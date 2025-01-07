import os
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv

# Load the .env file variables
load_dotenv()

def connect():
    """Establishes a connection to the PostgreSQL database."""
    # Retrieve connection parameters from environment variables
    connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    print("Starting the connection...")
    engine = create_engine(connection_string, future=True)
    return engine

# Create the engine
engine = connect()

# Create tables with IF NOT EXISTS
create_tables_sql = """
CREATE TABLE IF NOT EXISTS publishers(
    publisher_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY(publisher_id)
);

CREATE TABLE IF NOT EXISTS authors(
    author_id INT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(50) NULL,
    last_name VARCHAR(100) NULL,
    PRIMARY KEY(author_id)
);

CREATE TABLE IF NOT EXISTS books(
    book_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    total_pages INT NULL,
    rating DECIMAL(4, 2) NULL,
    isbn VARCHAR(13) NULL,
    published_date DATE,
    publisher_id INT NULL,
    PRIMARY KEY(book_id),
    CONSTRAINT fk_publisher FOREIGN KEY(publisher_id) REFERENCES publishers(publisher_id)
);

CREATE TABLE IF NOT EXISTS book_authors (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY(book_id, author_id),
    CONSTRAINT fk_book FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    CONSTRAINT fk_author FOREIGN KEY(author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);
"""

# Execute table creation
with engine.connect() as conn:
    conn.execute(text(create_tables_sql))
    print("Tables created successfully.")

# Fetch data into a DataFrame
query = "SELECT * FROM books;"
with engine.connect() as conn:
    dataframe = pd.read_sql(query, con=conn.connection)
    print(dataframe.head())

