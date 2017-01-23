Analysis of Delays Using K nearest Neighbors Classifier
============================
##Files (All in Python 3)
test_learn: Basic implementation of machine learning using scikit-learn. Classifier can be interchanged easily.
average_tester: Averages the accuracy of a classifier over multiple iterations. Creates and fits a new clasifier with a different part of the given data. Classifier can be interchanged, features and labels can be changed as well as many other settings.
k_neigh_auto: Automatically tests many neighbor values for a KNeighbors classifier. Each number of neighbors runs multiple tests to find the average. Writes to a text file with results when done. Features, labels, and many other settings can be changed.
feature_finder: Automatically creates combinations of features and tests each set of features over multiple iterations using the KNeighbors classifier to find the average. Fully threaded using multiprocessing. Writes to a csv file with results. Length of combinations, number of threads, and many other settings can be changed.

##Design Choices
Number of Iterations (10): Chosen after using a high number of iterations to find convergance of accuracy, then lowering number of iterations until average accuracy was consistent with itself and more iteration tests. Used average_tester.
Number of Neighbors (16 or 14): Chosen after testing the effects of number of neighbors on features Month, Day of Week, and CRS Departure Time with label Departure Delay. Tested large range of neighbors over multiple iterations, and found point where accuracy was consistent with more neighbors (no noticibly increasing accuracy anymore). Used k_neigh_auto.
