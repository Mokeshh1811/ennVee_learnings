from fastapi import FastAPI,Depends,HTTPException
import services,db,schema
from db import get_db,engine
from sqlalchemy.orm import Session

app=FastAPI()

@app.get("/books/",response_model=list[schema.Book])
def get_all_books(db:Session = Depends(get_db)):
    return services.get_books(db)

@app.post("/books/",response_model=schema.Book)
def create_new_book(book:schema.BookCreate,db: Session=Depends(get_db)):
    return services.create_book(db,book)

@app.get("/books/{id}",response_model=schema.Book)
def get_book_by_id(id:int,db:Session = Depends(get_db)):
    book_queryset=services.get_book(db,id)
    if book_queryset:
        return book_queryset
    raise HTTPException(status_code=404, detail="Invalid Book ID")

@app.put("/books/{id}",response_model=schema.Book)
def update_book(book:schema.BookCreate,id:int,db:Session = Depends(get_db)):
    db_update=services.update_book(db,book,id)
    if not db_update:
        raise HTTPException(status_code=404,detail="Book Not Found")
    return db_update

@app.delete("/books/{id}",response_model=schema.Book)
def delete_book(id:int,db:Session = Depends(get_db)):
    delete_entry=services.delete_book(db,id)
    if delete_entry:
        return delete_entry
    raise HTTPException(status_code=404,detail="Not Book to delete on given ID")