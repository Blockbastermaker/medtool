# -*- coding: utf-8 -*-

import numpy as np

class probabilityMatrix(object) :

    def __init__(self, datset, cutoff=0.05, ground_level=0.0):
        self.dat = datset
        self.node_edges_ = None
        self.labels_ = self.nodeLabel()
        self.combinations_ = self.eventCombinations()
        self.dat_prob_ = self.datasetProb(self.dat)
        self.delta_ = self.valueChanges()
        self.events_ = self.geneEvents(cutoff)
        self.eventsCounts_ = self.eventCountDict(ground_level)
        self.eventsProbs_ = self.eventCountProb()
        self.label_id_mapper = self.idLabelMapper()

    def nodeLabel(self, labels=[]):
        if len(labels) :
            return labels
        else :
            return ['S0', 'U1', 'N1', 'D1', 'U2', 'N2', 'D2']

    def eventCombinations(self):
        return [['S0U1', 'S0N1', 'S0D1', ],
                ['U1U2', 'U1N2', 'U1D2', 'N1U2', 'N1N2',
                 'N1D2', 'D1U2', 'D1N2', 'D1D2'], ]

    def datasetProb(self, dat):
        if dat.shape[0] :
            d_o = dat.copy()
            dat_prob = dat
        else :
            d_o = self.dat.copy()
            dat_prob = self.dat

        dat_prob[:, 0] = d_o[:, 0] / d_o[:, 0]

        dat_prob[:, 1] = d_o[:, 1] / d_o[:, 0]
        dat_prob[:, 2] = d_o[:, 2] / d_o[:, 1]

        return dat_prob

    def valueChanges(self):

        return self.dat_prob_ - np.reshape(np.repeat(1.0, self.dat.shape[0] * self.dat.shape[1]), self.dat.shape)

    def geneEvents(self, cutoff=0.05):

        events_ = []
        if self.dat.shape[0] :
            for item in self.delta_ :
                seq = self.labels_[0]
                for i in range(2):
                    if item[i + 1] >= cutoff:
                        seq += self.labels_[1 + i*3]
                    elif item[i + 1] <= cutoff * (-1):
                        seq += self.labels_[3 + i*3]
                    else:
                        seq += self.labels_[2 + i*3]
                events_.append(seq)
        return events_

    def eventCountDict(self, ground_level=0.5):
        event_dict = []

        for i in range(2):

            combinations = self.combinations_[i]

            c_dict = {}
            for c in combinations :
                c_dict[c] = 0.5

            for e in self.events_ :
                c_dict[e[i*2: i*2 + 4]] += 1

            event_dict.append(c_dict)

        return event_dict

    def idLabelMapper(self):

        mapper = {}
        for l,i  in zip(self.labels_, range(len(self.labels_))) :
            mapper[l] = i

        return mapper

    def eventCountProb(self):

        prob_dict = []
        for event_dict in self.eventsCounts_ :
            new_dict = {}
            for c in event_dict.keys() :
                new_dict[c] = event_dict[c] / float(self.dat.shape[0])
            prob_dict.append(new_dict)
        return prob_dict

    def eventNodeEdges(self):
        node_edges = []
        for event_dict in self.eventsProbs_ :
            for k in event_dict.keys() :
                node_edges.append((self.label_id_mapper[k[:2]],
                                   self.label_id_mapper[k[2:4]],
                                   event_dict[k]))

        self.node_edges_ = node_edges