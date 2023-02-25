from flask import Flask, render_template
import logging

from flask_login import LoginManager

from travelAgent.models import User

app = Flask(__name__)  # create an app instance
app.secret_key = 'BxeE3wJcjYi6yA7y1bjBJ1IAs0'

# -------------------------------------create a logger------------------------------------------
logger = logging.getLogger(__name__)  # create a logger
logger.setLevel(logging.INFO)  # show messages above info level
fh = logging.FileHandler('../log')  # log file handler
ch = logging.StreamHandler()  # input stream handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # set a formatter

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

# -------------------------------------login/logout------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)



@app.route('/')
def index():  # put application's code here
    logger.info('Entered the HOME page')
    return render_template("index.html")

@app.route('/about')
def about():
    logger.info('Entered the ABOUT page')
    return render_template("about.html")

@app.route('/sign-in')
def customer_login():
    logger.info('Entered the CUSTOMER LOGIN page')
    return render_template("sign-in.html")


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


if __name__ == '__main__':
    logger.info('The Website Starts Running!')
    app.run(debug=True, port=5000)
