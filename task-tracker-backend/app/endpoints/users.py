import uuid

from fastapi import FastAPI, HTTPException

from app.database.db_connection import create_session
from app.model.User import UserTable

app = FastAPI()

@app.post('/register')
def post_new_registered_user(email: str, password_hash: str):
    session = create_session()
    try:
        existing_user = session.query(UserTable).filter_by(email=email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail='user already exists')
        new_user = UserTable(
            uuid=uuid.uuid4(),
            email=email,
            password_hash=password_hash
        )
        session.add(new_user)
        session.commit()
        return {'message': f'user created sucessfully {new_user.uuid}'}
    except:
        session.rollback()
        raise HTTPException(status_code=500, detail='database error')
    finally:
        session.close()