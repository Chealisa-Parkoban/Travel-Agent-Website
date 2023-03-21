import datetime
import random

class Random_str:
    # Create random numbers based on time
    def create_uuid(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");
        randomNum = random.randint(0,100);
        if randomNum <= 10:
            randomNum = str(0)+str(randomNum);

        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum;