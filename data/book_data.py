from models.book import BookModel
from models.review import ReviewModel

books_list=[
    BookModel(name="The maid",description="fantasy,fiction",user_id="1"),
    BookModel(name="Twilight",description="fantasy",user_id=2),
    BookModel(name="The Kite Runner",description="horror and thriller",user_id=3),
]

reviews_list =[
    ReviewModel(rating="2",description="This is an average book",book_id=1),
    ReviewModel(rating="1",description="This is an bad book",book_id=2),
    ReviewModel(rating="5",description="This is an great book",book_id=3),
    
]