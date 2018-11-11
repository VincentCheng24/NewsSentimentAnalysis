from MAIN import SENTI
import csv

date = 1111
sentiment_examples_path = '/Users/vincent/Desktop/Mini_Job/Semantics/sentiment_examples.csv'
res_path = '/Users/vincent/Desktop/Mini_Job/Semantics/res_{}.csv'.format(date)


with open(res_path, 'w', newline='') as dmp:
    fieldnames = ['id', 'title', 'ReviewScoreTitle', 'subline', 'ReviewScoreSubline', 'finalScore', 'negative', 'prediction']
    writer = csv.DictWriter(dmp, fieldnames=fieldnames)
    writer.writeheader()

    with open(sentiment_examples_path, 'r', newline='') as df:
        reader = csv.reader(df)

        headers = next(reader)
        for row in reader:
            id = row[0]
            title = row[3]
            subline = row[12]
            negative = row[6]

            sentiValueTitle = SENTI(title)
            ReviewScoreTitle = sentiValueTitle.write2SentiValues()

            sentiValueSubline = SENTI(subline)
            ReviewScoreSubline = sentiValueSubline.write2SentiValues()

            finalScore = ReviewScoreSubline + ReviewScoreTitle
            prediction = 1 if finalScore > 0 else 2

            writer.writerow({'id': id, 'title': title, 'ReviewScoreTitle': ReviewScoreTitle,
                             'subline': subline, 'ReviewScoreSubline': ReviewScoreSubline, 'finalScore': finalScore,
                             'negative': negative, 'prediction': prediction})

        print('well done')



