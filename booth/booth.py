from __future__ import print_function

from time import time
import logging
import matplotlib.pyplot as plt

import numpy as np

#from sklearn.cross_validation import train_test_split
from sklearn.datasets import fetch_lfw_people
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import RandomizedPCA
from sklearn.svm import SVC
import pickle as pkl

from sklearn.ensemble import RandomForestClassifier

import students

print(__doc__)

# Display progress logs on stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s') 0.01  0.01  0.    0.11  0.15  0.08  0.    0.03  0.55  0.06]

folder = "./faces/"
w, h = 30, 50
def get_trained_classifier(folder):

	## load data
	images, names = students.load_student_database( folder, w, h )
	X = [ image.flatten() for image in images ]
	y = students.get_labels_numbered(names)
	target_names=list(set(names))

	## classifier
	param_grid = {'n_estimators': [100], }
	clf = GridSearchCV(
		RandomForestClassifier(n_jobs = 4), 
		param_grid)

	## fit
	clf = clf.fit(X_train, y_train)

	with open("classifier.pkl", "wb") as keeptrace:
	    pickler = pkl.Pickler(keeptrace)
	    pickler.dump(clf)

def predict(ugly_face):
	with open("classifier.pkl", "rb") as keeptrace:
	    clf = pkl.load(keeptrace)
	y_pred = clf.predict(ugly_face)
	y_prob = clf.predict_proba(ugly_face)

	    
	    














images, names = students.load_student_database( folder, w, h )

# for machine learning we use the 2 data directly (as relative pixel
# positions info is ignored by this model)
X = [ image.flatten() for image in images ]

# the label to predict  0.01  0.01  0.    0.11  0.15  0.08  0.    0.03  0.55  0.06] 0.01  0.01  0.    0.11  0.15  0.08  0.    0.03  0.55  0.06]is the id of the person
y = students.get_labels_numbered(names)
target_names=list(set(names))

# introspect the images arrays to find the shapes (for plotting)
n_samples = np.shape(X)[0]
n_features = np.shape(X)[1]
n_classes = len(target_names)

print("Total dataset size:")
print("n_samples: %d" % n_samples)
print("n_features: %d" % n_features)
print("n_classes: %d" % n_classes)

#assert( n_samples == len(y), "ERROR: Wrong number of labels!")


##
## Split into a training set and a test set using a stratified k fold
##
#X_train, X_test, y_train, y_test = train_test_split(
#   X, y, test_size=0.1)
X_train, X_test, y_train, y_test = students.train_test_split(
   X, y, test_each=2)


##
## Train a SVM classification model
##

print("Fitting the classifier to the training set")
t0 = time()
param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
              'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
param_grid = {'n_estimators': [100], }

# Selecting the best set of parameters

# Instatiation of the GridSearch
#clf = GridSearchCV(SVC(kernel='rbf', class_weight='auto', probability=True), param_grid)
clf = GridSearchCV(
	RandomForestClassifier(n_jobs = 4), 
	param_grid)

# Fitting the Gridsearch
clf = clf.fit(X_train, y_train)
print("done in %0.3fs" % (time() - t0))
print("Best estimator found by grid search:")
print(clf.best_estimator_)


##
## Quantitative evaluation of the model quality on the test set
##
print("Predicting people's names on the test set")
t0 = time()
y_pred = clf.predict(X_test)
y_prob = clf.predict_proba(X_test)
print(y_prob.shape)
print("done in %0.3fs" % (time() - t0))

print(classification_report(y_test, y_pred, target_names=target_names))
print(confusion_matrix(y_test, y_pred, labels=range(n_classes)))


##
## Qualitative evaluation of the predictions using matplotlib
##
def plot_gallery(images, titles, h, w, n_row=2, n_col=2):
    """Helper function to plot a gallery of portraits"""
    plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(n_row * n_col):
        plt.subplot(n_row, n_col, i + 1)
        plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
        plt.title(titles[i], size=12)
        plt.xticks(())
        plt.yticks(())


# plot the result of the prediction on a portion of the test set

def title(y_pred, y_test, target_names, i):
    pred_name = target_names[y_pred[i]].rsplit(' ', 1)[-1]
    true_name = target_names[y_test[i]].rsplit(' ', 1)[-1]
    return 'predicted: %s\ntrue:      %s' % (pred_name, true_name)

prediction_titles = [title(y_pred, y_test, target_names, i)
                     for i in range(y_pred.shape[0])]

#plot_gallery(X_test, prediction_titles, h, w)
print(y_prob[:, :])
plt.show()
