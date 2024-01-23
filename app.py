from database import *
from config import *
from routes import *
from werkzeug.debug import DebuggedApplication  
app.debug = True
if __name__ == "__main__":
    app.run(debug=True)
    #app.run(port=5000, host="0.0.0.0")
    #application = DebuggedApplication(app, True)
    