import argparse
import mysql.connector
from MAIN import SENTI


def updateAssessment(args):

    try:
        db = mysql.connector.connect(user=args.username, password=args.password, port=args.port, host=args.host, database=args.schema)
        cur = db.cursor()
    except Exception as e:
        print(e)
    else:
        print('successfully connect to the databse')

    # query_op = 'SELECT id, title, subline FROM {} WHERE negative=-1'.format(table)
    query_op = 'SELECT id, title, subline FROM {}'.format(args.table)
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

    print('successfully updated all')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set the parameters to connect to the database and update the assessment')
    parser.add_argument('--username', type=str, help='username to access the database')
    parser.add_argument('--password', type=str, help='password to access the database')
    parser.add_argument('--host', type=str, default='39.104.67.5', help='host to access the database')
    parser.add_argument('--port', type=str, default='3306', help='port to access the database')
    parser.add_argument('--schema', type=str, default='spider', help='schema to access the database')
    parser.add_argument('--table', type=str, default='rslist3', help='table to be updated')

    args = parser.parse_args()

    updateAssessment(args)
    print('successfully updated all')
