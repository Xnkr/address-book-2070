## Address Book 2070

#### Requirements

1. Python 3.6+
2. NodeJS 12+ and npm 6.13+

#### To build (or) run the application

#####1. Start the server
- *(Optional)* Create a python virtual environment
- Install required python dependencies by running the command in the same directory as that of the application

    `pip install -r requirements.txt`
- *(Optional)* Remove any purge all data from the database by running

    `python db_manager.py`
- *(Optional)* Load the given CSV file (`data/contacts-from-req.csv`) by running
       
    `python db_builder.py`
- Start the server by
    
    `python app.py`

- Server will start in the default PORT 5000

#####2. Start the UI
- Install required npm dependencies by running the command in the `frontend/address-book-2070` directory

    `npm install`

- Start the npm server by

    `npm start`

- Address book can now be opened in the [browser](http://localhost:3000)