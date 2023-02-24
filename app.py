from flask import Flask, render_template
import logging

app = Flask(__name__)

logger = logging.getLogger(__name__)  # create a logger
logger.setLevel(logging.INFO)  # show messages above info level
fh = logging.FileHandler('travelAgent.log')  # log file handler
ch = logging.StreamHandler()  # input stream handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # set a formatter

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)



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


if __name__ == '__main__':
    logger.info('The Website Starts Running!')
    app.run(debug=True, port=5000)
