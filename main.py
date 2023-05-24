from app import *

app = creat_app()

# db_drop_and_create_all(app)

app.run(host='0.0.0.0', port=80, debug=True)
