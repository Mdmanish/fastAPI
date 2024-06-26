from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from blog import schemas, database, models, token
from sqlalchemy.orm import Session
from blog.hashing import Hash

router = APIRouter(
    prefix='/login',
    tags=['auth']
)

@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')

    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect password')
    
    access_token = token.create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
