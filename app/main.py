import os
from fastapi import FastAPI, Depends, Form, Cookie, Request, Response, UploadFile, File, HTTPException
from jose import jwt
from fastapi.responses import RedirectResponse
from starlette.staticfiles import StaticFiles


from fastapi.security import OAuth2PasswordBearer
from .flowers_repository import Flower, FlowersRepository
from .purchases_repository import Purchase, PurchasesRepository
from .users_repository import User, UsersRepository
import json


app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()


# ваше решение сюда
def encodeJWT(payload) -> str:

    token = jwt.encode(payload, "lluna", "HS256")
    return token

def decodeJWT(token:str) -> int:
    data = jwt.decode(token, "lluna", "HS256")
    return data["ID"]
def verificate_user(token: str = Depends(oauth2_schema)):
    user_id = decodeJWT(token)
    user = users_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user token")
    return user

@app.get("/flowers")
def get_flowers(request: Request):
    return flowers_repository.get_all()


@app.post("/flowers")
def create_flower(flower: Flower):
    flowers_repository.save(flower)
    return {"flower_id": flower.id}


@app.post("/cart/items")
def cart_items_post(flower_id: int = Form(...),count: int = Form(), token: str = Depends(oauth2_schema), cart: str = Cookie(default="[]")):
    cart_json = json.loads(cart)

    if flower_id and count <= flowers_repository.get_by_id(flower_id).count:
        flowers_repository.save_in_cart(flower_id, count)
        cart_json.append(flowers_repository.get_all_in_cart())
        new_cart = json.dumps(cart_json)
        response = Response('{"msg":"flower successfully added to the basket"}', status_code=200)
        response.set_cookie(key="flower_ids", value=new_cart)
        return response

    return {"msg": "The flower out of stock"}


@app.get("/cart/items")
def cart_items_get(request: Request):
    user_cart = request.cookies.get("flower_ids")

    if not user_cart:
        return {"message": "The cart is empty"}

    flower_ids = [int(item) for item in user_cart.strip('[]').split(",")]

    flowers = [flowers_repository.get_by_id(flower_id) for flower_id in flower_ids]
    response_flowers = [{'id': flower.id, 'name': flower.name, 'price': flower.cost} for flower in flowers]
    total_cost = sum(flower.cost for flower in flowers)

    return {"flowers_in_cart": response_flowers, "total_cost": total_cost}


@app.post("/signup")
async def signup(email: str = Form(), full_name: str = Form(), password: str = Form(), photo: UploadFile = File()):
    photo_directory = "static/photos"

    os.makedirs(photo_directory, exist_ok=True)

    photo_path = os.path.join(photo_directory, photo.filename)
    with open(photo_path, "wb") as f:
        f.write(await photo.read())

    photo_path = photo_path[7:]

    user = User(email=email, full_name=full_name, password=password, photo=photo_path)
    saved_user = users_repository.save(user)
    print(saved_user)
    return users_repository.get_attr(saved_user)



@app.post("/login")
def login(username: str = Form(), password: str = Form() ):
    user = users_repository.get_by_email(username)
    if user is None or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = encodeJWT(users_repository.get_attr(user))
    return {"access_token": access_token, "type": "bearer"}

@app.get("/profile")
def profile(current_user: User = Depends(verificate_user)):
    return users_repository.get_attr(current_user)

@app.post("/purchased")
def purchase(request: Request, response: Response, current_user: User = Depends(verificate_user)):
    cookie_list = request.cookies.get('flower_ids')
    flower_ids = cookie_list.strip('[]').split('\054') if cookie_list else []
    for flower_id in flower_ids:
        purchase_temp = Purchase(current_user.id, int(flower_id))
        purchases_repository.save(purchase_temp)
    return {"msg": "Successfully purchased"}

@app.get("/purchased")
def get_all_purchased(request: Request,current_user: User = Depends(verificate_user)):
    purchases = purchases_repository.get_all_purchases_by_user_id(current_user.id)
    flowers = []
    for purchase in purchases:
        flowers.append(flowers_repository.get_one(purchase.flower_id))
    return flowers





# конец решения