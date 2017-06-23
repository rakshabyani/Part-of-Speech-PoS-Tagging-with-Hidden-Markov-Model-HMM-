import sys
import ast
import collections
stateMatrix = collections.OrderedDict()
backpointerMatrix = {}

def main():
    with open("hmmmodel.txt","r") as file:
        file.readline()
        modelParams = file.read().split("MODEL PARAMETER 2 Emission Probabilities:\n")
        transitionProbModel = ast.literal_eval(modelParams[0])
        emissionProbModel = ast.literal_eval(modelParams[1])

    output = open("hmmoutput.txt","w")
    with open(sys.argv[1],"r") as file:
        for line in file:
            originalWords = line.split()
            words = [word.lower() for word in originalWords]
            backtrace = viterbiAlgorithm(transitionProbModel,emissionProbModel, words)
            i = backtrace.__len__() - 2
            for word in originalWords:
                output.write(word + "/" + backtrace[i] + " ")
                i -= 1
            output.write("\n")


    # print(stateMatrix)
    # print(backpointerMatrix)

def viterbiAlgorithm(transitionProbModel,emissionProbModel, words):
    stateMatrix = collections.OrderedDict()
    backpointerMatrix = {}
    noOfObs = words.__len__()
    for state in transitionProbModel.keys():
        if state != "q0":
            stateMatrix[state] = []

    # Smoothen emission probability
    for state in stateMatrix.keys():
        if words[0] in emissionProbModel.keys():
            if state in emissionProbModel[words[0]].keys():
                stateMatrix[state].append(transitionProbModel["q0"][state] * emissionProbModel[words[0]][state])
            else:
                m = min(emissionProbModel[words[0]].values())/10000
                stateMatrix[state].append(transitionProbModel["q0"][state] * m)
            backpointerMatrix[state] = ["q0"]
        else:
            stateMatrix[state].append(transitionProbModel["q0"][state] * 1)
            backpointerMatrix[state] = ["q0"]
        #calculate probability sequence By viterbi algorithm
    for i in range(1,noOfObs):
        for q_end in stateMatrix.keys():
            temp = {}
            for q_beg in stateMatrix.keys():
                if words[i] in emissionProbModel.keys():
                    if q_end in emissionProbModel[words[i]].keys():
                        temp[q_beg] = (stateMatrix[q_beg][i-1] * transitionProbModel[q_beg][q_end] * emissionProbModel[words[i]][q_end])
                    else:
                        m = min(emissionProbModel[words[i]].values())/10000
                        temp[q_beg] = (stateMatrix[q_beg][i-1] * transitionProbModel[q_beg][q_end] * m)
                else:
                    temp[q_beg] = (stateMatrix[q_beg][i - 1] * transitionProbModel[q_beg][q_end] * 1)
            maxProb = max(temp.values())
            stateMatrix[q_end].append(maxProb)

            for k, v in temp.items():
                if maxProb == v:
                    index = k
                    break
            backpointerMatrix[q_end].append(index)

    temp = {}
    for q in stateMatrix.keys():
        temp[q] = stateMatrix[q][noOfObs-1]
    maxProb = max(temp.values())
    for k,v in temp.items():
        if maxProb == v:
            index = k
            break

    state = index
    backtrace = [state]
    timeInstance = noOfObs - 1
    # Return the Best Path
    while state != 'q0' and timeInstance >=0 :
        state = backpointerMatrix[state][timeInstance]
        backtrace.append(state)
        timeInstance -= 1
    return backtrace
main()