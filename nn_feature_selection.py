import math

def normalize(instances, instance, num_features):
    mean = []
    std = []
    normalized_instances = list(instances)
    for i in range(1, num_features + 1): 
        mean.append((sum(row[i] for row in instances)) / instance)
        
    for i in range(1, num_features + 1):
        std.append(math.sqrt((sum(pow((row[i] - mean[i-1]), 2) for row in instances)) / instance))    
    
    for i in range(0, instance):
        for j in range(1, num_features + 1):
            normalized_instances[i][j] = ((instances[i][j] - mean[j-1]) / std[j-1])
    return normalized_instances

def nearestNeighbor(instances, total_instances, out_data, features):
    nearest_neighbor = -1
    nearest_neighbor_distance = float('inf')
    featureLength = len(features)
    for i in range(0, total_instances):
        if (i == out_data):
            pass
        else:
            sum = 0
            for j in range(0, featureLength):
                sum = sum + pow((instances[i][features[j]] - instances[out_data][features[j]]), 2)
            distance = math.sqrt(sum)
            if distance < nearest_neighbor_distance:
                nearest_neighbor_distance = distance
                nearest_neighbor = i
    return nearest_neighbor

def classification(instances, nearest_neighbor, out_data):
    if (instances[nearest_neighbor][0] != instances[out_data][0]):
        return False
    return True

def leave_one_out_crossvalidation(instances, total_instances, current_features, testFeature):
    
    if testFeature > 0:
        list_features = list(current_features)
        list_features.append(testFeature)
    elif testFeature < 0:
        testFeature = testFeature * -1
        current_features.remove(testFeature)
        list_features = list(current_features)
        current_features.add(testFeature)
    elif testFeature == 0:
        list_features = list(current_features)

    correct = 0
    for i in range(0, total_instances):
        one_out = i
        nearest_neighbor = nearestNeighbor(instances, total_instances, one_out, list_features)
        correct_classification = classification(instances, nearest_neighbor, one_out)
        if (correct_classification):
            correct += 1
    accuracy = correct / total_instances
    print("Using feature(s): ", list_features, " accuracy is %f" % accuracy)
    return accuracy


def load(instance):
    try:
        f = open(r'C:\Users\Shreya Singh\Desktop\CS205_small_testdata__5.txt', 'r')
    except:
        raise FileNotFoundError()
    instances = [[] for i in range(instance)]
    for i in range(instance):
        instances[i] = [float(j) for j in f.readline().split()]
    return instances

def forward_feature_selection(data, total_instances, total_features):
    print("\n\n")
    current_set_of_features = set()
    best_so_far_accuracy = 0
    print("\n")
    for i in range(total_features):
        print("Search tree level %d" % (i+ 1),\
            "the set is", current_set_of_features)
        add_feature = -1
        for j in range(1, total_features + 1):
            if (j not in current_set_of_features):
                accuracy = leave_one_out_crossvalidation(data, total_instances,\
                    current_set_of_features, j)
                if accuracy > best_so_far_accuracy:
                    best_so_far_accuracy = accuracy
                    add_feature = j
        if (add_feature > 0):
            current_set_of_features.add(add_feature)
            print("At level %d," % ((i+1)),\
                " feature %d has the best accuracy: %f" \
                % (add_feature, best_so_far_accuracy))
            print("\n\n")
        else:
            print("End")
            break
    print("\n")
    print("Best feature set is", current_set_of_features,\
        "having accuracy", best_so_far_accuracy)

def backward_feature_elimination(data, total_instances, total_features):
    print("\n\n")
    current_set_of_features = set(i+1 for i in range(0, total_features))
    best_so_far_accuracy = 0
    print("\n")
    for i in range(total_features):
        print("Search tree level %d" % (i+1),\
            "the set is", current_set_of_features)
        remove_feature = -1
        for j in range(1, total_features + 1):
            if (j in current_set_of_features):
                accuracy = leave_one_out_crossvalidation(data, total_instances,\
                    current_set_of_features, (-1 *j))
                if accuracy > best_so_far_accuracy:
                    best_so_far_accuracy = accuracy
                    remove_feature = j
        if (remove_feature > 0):
            current_set_of_features.remove(remove_feature)
            print("At level %d," % (i+1),\
                "removing feature %d the accuracy is %f" \
                % (remove_feature, best_so_far_accuracy))
            print("\n\n")
        else:
            print("End")
            break
    print("\n")
    print("Best feature set is:", current_set_of_features,\
        "having accuracy", best_so_far_accuracy)

def main():
    instance = int(input("Choose the number of instances to run: for small dataset max instances are 300 and for large dataset there are 900 "))
    instances = load(instance)

    choice = ""
    while (choice != 1 and choice != 2):
        choice = int(input("""Select algorithm you want to run, enter:
                       1 for Forward Selection
                       2 for Backward Elimination
                       \r"""))
    num_features = len(instances[0]) - 1
    print("\t--------Data is being normalized-------- ")
    normalized = normalize(instances, instance,\
        num_features)
    print("There are %d features with %d instances." % (num_features, instance))
    if (choice == 1):
        forward_feature_selection(normalized, instance, num_features)
    elif (choice == 2):
        backward_feature_elimination(normalized, instance, num_features)
   
if __name__ == '__main__':
    main()



