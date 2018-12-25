import mysql.connector
from MAIN import SENTI

username = 'root'
password = '123qweasd'
host = '39.104.67.5'
port = '3306'
schema = 'spider'
table = 'rslist3'

try:
    db = mysql.connector.connect(user=username, password=password, port=port, host=host, database=schema)
    cur = db.cursor()
except Exception as e:
    print(e)
else:
    print('successfully connect to the databse')

# query_op = 'SELECT id, title, subline FROM {} WHERE negative=-1'.format(table)
query_op = 'SELECT id, title, subline FROM {}'.format(table)
cur.execute(query_op)
list_of_news = cur.fetchall()

for line in list_of_news:

    try:
        id, title, subline = line

        sentiValueTitle = SENTI(title)
        ReviewScoreTitle = sentiValueTitle.write2SentiValues()

        sentiValueSubline = SENTI(subline)
        ReviewScoreSubline = sentiValueSubline.write2SentiValues()

        finalScore = ReviewScoreSubline + ReviewScoreTitle

        if finalScore > 0:
            prediction = 1
        elif finalScore == 0:
            prediction = 0
        else:
            prediction = 2

        update_op = 'UPDATE rslist3 SET negative={} WHERE id={}'.format(prediction, id)
        cur.execute(update_op)
        db.commit()

    except Exception as e:
        print(e)
    else:
        print('successfully update {}'.format(id))

print('updated all')
