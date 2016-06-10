import util
import numpy
from collections import defaultdict
from operator import itemgetter

import config as cfg


def testKendal(toolbox, pop, data):
    valid = False

    # Calcullate similarity betwreen REM and REF
    for individual in pop:
        simFunc = toolbox.compile(expr=individual)

        for classIdx, classData in data.iteritems():
            # Get refIdx for this class
            nSample = len(classData)
            nRef = int( cfg.nRefPerClassInPercentage/100.0 * nSample )
            refIdxList = numpy.random.randint(0,nSample, size=nRef)

            for refIdx in refIdxList:
                refString = value[refIdx]
                simScoreList = [] # each element contains 3-tuple of (simScore, refClassLabel, remClassLabel)

                # remaining from this class
                for remIdx in [idx for idx in range(nSample) if idx not in refIdxList]:
                    remString = classData[remIdx]
                    a = util.getFeatureA(refString, remString)
                    b = util.getFeatureB(refString, remString)
                    c = util.getFeatureC(refString, remString)
                    simScore = simFunc(a,b,c)
                    simScoreList.append( (simScore,classIdx,classIdx) )

                # remaining from other class
                for notThisClassIdx in [i for i in data.keys() if i not classIdx]:
                    for remString in data[notThisClassIdx]:
                        a = util.getFeatureA(refString, remString)
                        b = util.getFeatureB(refString, remString)
                        c = util.getFeatureC(refString, remString)
                        simScore = simFunc(a,b,c)
                        simScoreList.append( (simScore,classIdx,notThisClassIdx) )

                # Sort simScoreList based descending order of SimScore
                sortedIdx = sorted(range(len(simScoreList)), key=lambda k: s[k][0])
                nTop = cfg.nTopPercentace/100.0 * len(sortedIdx)
                sortedIdx = sortedIdx[0:nTop]

                # Get the number of recall/tp
                nRecall = 0
                for i in sortedIdx:
                    refClass = simScoreList[sortedIdx][1]
                    remClass = simScoreList[sortedIdx][2]
                    if refClass == remClass:
                        nRecall = nRecall +1

    recallMatrix = defaultdict(list)
    for individual in pop:
        func = toolbox.compile(expr=individual)

        similarity_pairwise = defaultdict(list)
        list_median = defaultdict(list)
        for ref in refList:
            for rem in remList:
                print "ref", ref, len(ref)
                print "rem", rem, len(rem)
                assert False
                a = util.getFeatureA(ref, rem)
                b = util.getFeatureB(ref, rem)
                c = util.getFeatureC(ref, rem)

                flg = 1 if (ref[0] == rem[0]) else 0

                '''
                Similarity_pairwise : An defaultDict with 3 column.
                    1-st column indicate label.
                    2-nd column indicate pairwise in same group or not (1 = same class; 0 otherwise).
                    3-th column indicate similarity values.
                '''
                similarity_pairwise[str(ref[0])].append([rem[0], flg, func(a, b, c)])

            # Sorting similarity_pairwise with descending order based on similarities values.
            similarity_pairwise = numpy.matrix(sorted(similarity_pairwise, key=itemgetter(2), reverse=True))

            true_positive = 0
            # Count True Positive (TP)
            for k in range(0, int(len(similarity_pairwise) * 0.1)):
                true_positive += 1 if (similarity_pairwise[k, 0] == 1) else 0

            '''
            list_median : A dictionary which contains true positive value.
            '''
            list_median[str(ref[0])].append(true_positive)

    # Get Recall Matrix
        recallMatrix[str(individual)].append(list_median)

    # Get Ranking Matrix

    # Test significance

    # Infer
    significant = True
    if (significant):
        valid = True
    return valid