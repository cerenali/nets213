## Classifier Training, Testing
This documents all the files in `src/classifier`

### prep_data.py

This module, found at `src/classifier`, handles training and testing a classifier that assigns labels
corresponding to social spheres for arbitrary lengths of text.

    cat <quality_control_output>.csv | python2 prep_data.py
    
Writes to `./training/` the following files:
* `family.train`
* `friends.train`
* `coworkers.train`
* `general.train`
* `specific.train`
Each file is of format:

        <0/1: is this the tweet's majority label>\t<tweet text>

Each file is used as training data for a binary classifier for the corresponding label.

### single_classifier.py

Constructs a binary unigram classifier for a label using training data in `data/training/'

    python2 single_classifier.py <training_data>
    

    import single_classifier
    single_classifier.get_classifier(<training file>)


### multi_classifier.py
This is the only part of the project not yet done. We've yet to combine the classifiers into a multi-label classifier.
One this is done, however, it will create 5 `single_classifier`s and combine them in a `OneVsRestClassifier`. 
The training files for the `single_classifiers` will be hard-coded into the file, so the only input is the test set.

    cat <test_tweets.tsv> | python2 multi_classifier.py > <test_results.txt>
    
The `test_tweets.tsv` file will be of format:

        <majority_label>\t<tweet text>



