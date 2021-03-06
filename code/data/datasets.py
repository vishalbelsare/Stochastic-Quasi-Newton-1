import numpy as np
import sklearn.datasets
import csv
import re

# functions for reading from loooong file as stream


def getstuff(filename, rowlim):
    with open(filename, "rb") as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
        for row in datareader:
            if count < rowlim:
                yield row
                count += 1
            else:
                return


def getdata(filename, rowlim):
    for row in getstuff(filename, rowlim):
        yield row

#####


def normalize(X):
    mu = X.mean(axis=0)
    std = X.std(axis=0)
    for i in range(X.shape[0]):
        X[i, :] -= mu
    for j in range(X.shape[1]):
        X[i, j] /= std[j]
    return X


def load_data1():
    dataset = np.genfromtxt(open('../datasets/ex2data1.txt', 'r'),
                            delimiter=',', dtype='f8')
    X = dataset[:, :2]
    z = dataset[:, 2][:, np.newaxis]

    X = normalize(X)

    X = np.concatenate((np.ones((len(z), 1)), X), axis=1)
    X_new = []
    for i in range(len(z)):
        x = np.array(list(X[i, :].flatten()))
        X_new.append(x)
    return X_new, list(z)


def load_data2():
    dataset = np.genfromtxt(open('../datasets/ex2data2.txt', 'r'),
                            delimiter=',', dtype='f8')

    X = dataset[:, :2]
    z = dataset[:, 2][:, np.newaxis]

    X = normalize(X)

    X = np.concatenate((np.ones((len(z), 1)), X), axis=1)
    X_new = []
    for i in range(len(z)):
        x = np.array(list(X[i, :].flatten()))
        X_new.append(x)
    return X_new, list(z)


def load_iris():
    iris = sklearn.datasets.load_iris()
    X = iris.data
    y = iris.target
    
    """    
    X, y = [], []
    for i in range(len(iris.target)):
        if iris.target[i] != 2:
            X.append(np.array([1] + list(iris.data[i])))
            y.append(iris.target[i])
    """
    return X, y


def split_into_files(src, dest_folder):
    counter = 1
    csvfile = open(src, "rb")
    line = csvfile.readline()
    while line is not None:
        line = csvfile.readline()
        with open(dest_folder + "/" + str(counter), "w+") as feature:
            feature.write(line)
        counter += 1
        if counter > 1e6:
            break
    csvfile.close()


"""
    Before you can use MySQL as database, you first have to create a user
    'casestudies' using the admin/root account.

    Then you have to make sure that the database HIGGS is created and that
    the user has access to it.

    mysql -u root -p
    CREATE USER 'casestudies'@'localhost';
    CREATE DATABASE HIGGS;
    GRANT ALL PRIVILEGES ON HIGGS.* TO 'casestudies'@'localhost';
"""

try:
        import MySQLdb
except:
        import pymysql as MySQLdb
        print "SQL Functionality is not working!"


"""
LOADING DATASET
"""

def get_mysql():
    db = MySQLdb.connect(user="casestudies",
                         db="HIGGS")  # name of the data base
    cur = db.cursor()
    dimensions = 29
    return db, cur, dimensions

def create_higgs():
    
    table_name = "DATA"
    db, cur, dimensions = get_mysql()
    sql = "CREATE TABLE IF NOT EXISTS " + table_name + " (ID INTEGER PRIMARY KEY, "

    for i in range(dimensions):
        sql += "x_" + str(i) + " DOUBLE, "
    sql = sql[:-2]
    sql += ");"

    try:
        cur.execute(sql)
    except Warning as w:
        print(w)
    cur.close()
    db.close()

def load_higgs_into_mysql():

    create_higgs()
    db, cur, table_name, dimensions = get_mysql()

    generic = "INSERT INTO " + table_name + " VALUES ("

    file_name = '../../datasets/HIGGS.csv'
    csvfile = open(file_name, "r")

    for count, line in enumerate(iter(csvfile)):
        line = re.sub('\s', '', str(line))
        entries = re.split(", ", str(line))
        insert_statement = generic
        insert_statement += str(count) + ","
        for index, entry in enumerate(entries):
            if index >= dimensions:
                break
            insert_statement += str(entry) + ","

        insert_statement = insert_statement[:-1]
        insert_statement += ')'
        if count % 1000 == 0:
            print(count)
        if count > 1e6:
            break
        try:
            cur.execute(insert_statement)
        except:
            continue

    csvfile.close()

    db.commit()
    cur.close()
    db.close()


def get_higgs_mysql(ID_list, db = None, cur = None, dimensions = None):
    stay_inside = False
    if any([db is None, cur is None, dimensions is None]):
            stay_inside = True
            db, cur, dimensions = get_mysql()
    table_name = "DATA"
    query = "SELECT * FROM " + table_name + " WHERE ID IN ("
    for ID in ID_list:
            query += "'" + str(ID) + "'" + ","
    query = query[:-1]
    query += ");"
    # print query
    cur.execute(query)
    X, y = [], []
    for c in cur:
            X_tmp, y_tmp = [], None
            for index in range(len(c)):
                    if index == 0:
                            continue
                    elif index == 1:
                            y_tmp = c[index]
                            X_tmp.append(1.0)
                    else:
                            X_tmp.append(c[index])
            X.append(np.array(X_tmp))
            y.append(y_tmp)
    if stay_inside:
        cur.close()
        db.close()

    return X, y





def load_higgs(rowlim=1000):
    print("Loading data from csv (this may take a while)...")
    file_name = '../datasets/HIGGS.csv'
    X, y = [], []
    for row in getdata(file_name, rowlim):
        X.append(np.array([1.0] + [float(r) for r in row[1:]]))
        y.append(float(row[0]))

    # print type(X[0])
    # print X[0][0]

    print("done.")
    return X, y


def load_eeg():
    '''
    This function loads .npy files X and y which correspond to eeg recordings
    and labels

    For this you need to have the EEG data set
    (Named: eeg_data.npy, eeg_label.npy) in the /datasets/ folder.
    folder. The dataset was sent around by Stan by email.

    NB :
    - Pay attention to label file dimension
    - You may want to convert the label file into a vector
    '''
    print("Loading eeg data set...")
    data_name = '../datasets/eeg_data.npy'
    label_name = '../datasets/eeg_label.npy'

    X = [ np.array(d) for d in np.load(data_name) ]
    y = np.load(label_name).flat[:]

    return X, y


if __name__ == "__main__":
    X, y = load_eeg()
