import math
import collections
import sys
def main():
    transition_prob = {}
    emission_prob = {}
    tags = collections.OrderedDict()
    word_dictionary = {}
    with open(sys.argv[1],"r") as file:
        for line in file:
            list_of_words = line.split()
            i = 0
            prev_tag = "q0"
            lengthOfSentence = list_of_words.__len__()
            for i in range(0,lengthOfSentence):
                word = list_of_words[i]
                temp = word.rsplit('/',1)
                # length = temp.__len__()
                if temp[1].__len__() == 2:
                    tag = temp[1]
                    obs = temp[0].lower()
                    # to maintain correct count for calculating emission probabilities
                    if i == lengthOfSentence - 1:
                        if tag in tags.keys():
                            if "lastWordCount" in tags[tag].keys():
                                tags[tag]["lastWordCount"] += 1
                            else:
                                tags[tag]["lastWordCount"] = 1
                        else:
                            tags[tag]={}
                            tags[tag]["lastWordCount"] = 1
                    if prev_tag in tags.keys():
                        if tag in tags[prev_tag].keys():
                            tags[prev_tag][tag] += 1
                        else:
                            tags[prev_tag][tag] = 1
                    else:
                        tags[prev_tag] = {}
                        tags[prev_tag][tag] = 1


                if obs in word_dictionary.keys():
                    if tag in word_dictionary[obs].keys():
                        word_dictionary[obs][tag] += 1
                    else:
                        word_dictionary[obs][tag] = 1
                else:
                    # to calculate emission probabilites
                    word_dictionary[obs] = {tag:1}
                prev_tag = tag


    # Calculate transition probability and write to model parameter file
    noOfTags = tags.__len__() - 1
    for tag in tags.keys():
        transition_prob[tag] = {}
        total = 0
        for transitionTag in tags[tag].keys():
            if transitionTag != "lastWordCount":
                total += tags[tag][transitionTag]
        total += noOfTags
        for transitionTag in tags.keys():
            if transitionTag != 'q0':
                if transitionTag in tags[tag].keys():
                    # transition_prob[tag][transitionTag] = math.log((tags[tag][transitionTag] + 1) / total)
                    transition_prob[tag][transitionTag] = ((tags[tag][transitionTag] + 1) / total)
                else:
                    # transition_prob[tag][transitionTag] = math.log(1 / total)
                    transition_prob[tag][transitionTag] = (1 / total)


    # Calculate emission probability and write to model parameter file.
    for word in word_dictionary.keys():
        emission_prob[word] = {}
        current_word = word_dictionary[word]
        total = sum(current_word.values())
        for tag in current_word.keys():
            # emission_prob[word][tag] = math.log(current_word[tag]/total)
            emission_prob[word][tag] = current_word[tag] / total

    output = open("hmmmodel.txt", 'w')
    output.write("Transition Probabilities:\n")
    output.write(str(transition_prob))
    output.write("\nMODEL PARAMETER 2 Emission Probabilities:\n")
    output.write(str(emission_prob))



main()