import pyodbc
import random

# Azure SQL Database Connection Details
server = 'sqldbpoc1.database.windows.net'  # Replace with your Azure SQL Server
database = 'aismetadata'  # Your database name
username = 'saadmin'  # Your Azure username
password = 'Photon~1~'  # Your password

#Roles to assign randomly
roles = [
    "Engineer", "Researcher", "Scientist", "Developer", "Professor",
    "Educator", "Linguist", "Data Scientist", "Analyst", "Philosopher",
    "Musician", "Cloud Engineer", "IT Specialist", "Software Developer",
    "DevOps Engineer", "Contributor", "Manager", "Editor", "Supply Chain Manager",
    "Marketing Manager", "Customer Support", "Chef", "Data Analyst", "HR Manager",
    "Operations", "Quality Control", "Kitchen Manager", "Digital Strategist",
    "Operations Manager", "Restaurant Staff", "Sustainability Manager", "Executive Chef",
    "E-commerce Manager", "IT Developer", "Security Officer", "IT Security Analyst",
    "Finance", "Management", "Marketing", "Product Dev", "Sales", "HR", "Admin",
    "Expansion", "R&D", "Technology", "Community Outreach"
]
 
try:
    # Establish connection to Azure SQL
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
        f'Timeout=300;'  # Increase timeout to 5 minutes
    )
    cursor = conn.cursor()
    print("✅ Connected to Azure SQL Database")
 
    # Fetch Data
    cursor.execute("SELECT id, search_type, search_tag FROM search_data")
    rows = cursor.fetchall()
    print(f"📊 Fetched {len(rows)} records from search_data.")
 
    for row in rows:
        record_id, search_type, search_tag = row[0], row[1], row[2]
        # Assign a random role
        assigned_role = random.choice(roles)
        print(f"🔹 ID {record_id}: '{search_tag}' → {assigned_role}")
        # Update role in database
        cursor.execute(
            "UPDATE search_data SET role = ? WHERE id = ?",
            (assigned_role, record_id)
        )
        conn.commit()
        print(f"✅ Updated ID {record_id}: '{search_tag}' → {assigned_role}")
 
except pyodbc.Error as db_err:
    print(f"\n❌ Database connection failed: {db_err}")
 
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    print("\n🔌 Connection closed")