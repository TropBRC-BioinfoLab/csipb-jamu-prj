# classifier_util.py
import os
import numpy as np
from scoop import futures as fu
from scoop import shared as sh
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold

def divideSamples(x,y,maxSamplesPerBatch):
   nSplits = ( len(x)/maxSamplesPerBatch ) + 1
   if nSplits==1:# take all
      idxesList = [ range(len(x)) ]
   else:# abusely use StratifiedKFold, taking only the testIdx
      if y is None:
         cv = KFold(n_splits=nSplits)
         idxesList = [testIdx for  _, testIdx in cv.split(x) ]
      else:
         cv = StratifiedKFold(n_splits=nSplits,shuffle=True)
         idxesList = [testIdx for  _, testIdx in cv.split(x,y) ]

   ##
   xyList = []
   for idxes in idxesList:
      xList = [x[i] for i in idxes]
      if y is None: yList = None
      else: yList = [y[i] for i in idxes]
      xyList.append( (xList,yList) )

   return xyList

def loadFeature(x,comFeaDir,proFeaDir):
   sh.setConst(comFeaDir=comFeaDir)
   sh.setConst(proFeaDir=proFeaDir)
   xf = list(fu.map(_loadFeature,x))
   return xf

def _loadFeature(x):
   com,pro = x
   comFeaDir = sh.getConst('comFeaDir')
   proFeaDir = sh.getConst('proFeaDir')
   comFea = loadKlekotaroth(com,comFeaDir).tolist()
   proFea = loadAAC(pro,proFeaDir).tolist()
   return mergeComProFea(comFea,proFea)

def mergeComProFea(comFea,proFea):
   return comFea+proFea

def loadKlekotaroth(keggComID,dpath):
   fea = np.loadtxt(os.path.join(dpath,keggComID+'.fpkr'), delimiter=",")
   return fea

def loadAAC(keggProID,dpath):
   fea = np.loadtxt(os.path.join(dpath,keggProID+'.aac'), delimiter=",")
   return fea

def makeKernel(x1,x2,simDict):
   mat = np.zeros( (len(x1),len(x2)) )
   for i,ii in enumerate(x1):
      for j,jj in enumerate(x2):
         comSim = simDict['com'][ (ii[0],jj[0]) ]
         proSim = simDict['pro'][ (ii[1],jj[1]) ]
         mat[i][j] = mergeComProKernel( comSim,proSim )
   return mat

def mergeComProKernel(comSim,proSim,alpha = 0.5):
   sim = alpha*comSim + (1.0-alpha)*proSim
   return sim
