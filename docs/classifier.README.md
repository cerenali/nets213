## Classifier Training, Testing

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

    single_classifier.py <training_data>

    import single_classifier
    single_classifier.get_classifier(<training file>)


### multi_classifier.py


