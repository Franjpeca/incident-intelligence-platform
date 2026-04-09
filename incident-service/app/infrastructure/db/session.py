import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Obtenemos la direccion de la BD del env
DATABASE_URL = os.getenv("DATABASE_URL")
# Creamos el engine y sesion para poder conectarnos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Esta funcion se usara en los endpoints para obtener una sesion de la base de datos, 
# Se encargara de cerrarla al finalizar
# Necesaria para atender peticiones de forma escalable y evitar problemas de conexiones abiertas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()