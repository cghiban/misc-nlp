from itertools import izip

import numpy as np
from features import syllabifications, all_splits


def training_instances(syls):
    for syl in syls:
        for left, right, label in all_splits(syl.strip()):
            yield unicode(left), unicode(right), label


def shaped_instances(gen):
    k = (((l, r), label, k)
         for (l, r, label, k)
         in gen)
    return map(list, izip(*k))


def all_or_nothing_score(y_true, y_pred, groups=None):
    y_true, y_pred = (np.asarray(y) for y in (y_true, y_pred))
    if groups is None:
        groups = np.ones_like(y_true)
    else:
        groups = np.asarray(groups)

    hits = [np.all(y_true[np.where(groups == this_group)] ==
                   y_pred[np.where(groups == this_group)])
            for this_group in np.unique(groups)]
    return np.mean(hits)


def all_or_nothing_contig(y_true, y_pred, groups):
    matches = 0
    n_groups = 0
    trans_mat = np.zeros((8, 8))
    is_good = False
    prev_y = None
    for k, (this_y_true, this_y_pred) in enumerate(zip(y_true, y_pred)):
        if groups[k] != groups[k - 1]:
            n_groups += 1
            matches += is_good
            is_good = True
            prev_y = None
        else:
            if prev_y is not None:
                trans_mat[int(prev_y), int(this_y_pred)] += 1
            if this_y_true != this_y_pred:
                is_good = False
            prev_y = this_y_pred
    return trans_mat
    #return matches * 1.0 / n_groups
