from tailorder import create_app, db
from tailorder.helpers import create_order_series

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_order_series(db)
        print("Finished...")

