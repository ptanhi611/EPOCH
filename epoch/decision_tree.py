import numpy as np
import matplotlib.pyplot as plt 




#Defining the class "Node"
class Node:
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, value=None):
        self.feature_index= feature_index
        self.threshold= threshold
        self.left = left
        self.right = right
        self.value = value






#Defining a helper function which will return the majority label in a list
def most_common_label(y):
    labels = {}
    for label in y:
        if label not in labels:
            labels[label] = 0
        labels[label] += 1

    max_count = -1
    majority_label = None
    for label in labels:
        if labels[label] > max_count:
            max_count = labels[label]
            majority_label = label

    return majority_label






#Calculating Gini Impurity 
def calculate_gini_impurity(labels):
    count_for_each = np.bincount(labels)
    probablities = count_for_each/len(labels)
    return 1-np.sum(probablities**2)







#Implementing the decision Making 
def splitter(X,Y):
    n_values, n_features = X.shape
    best_gini = 1
    best_threshold = None
    best_feature = None

    for feature in range(n_features):
        sorted_indexs = X[:,feature].argsort()
        X_sorted = X[sorted_indexs]
        Y_sorted = Y[sorted_indexs]

        for i in range(n_values-1):
            if (X_sorted[i][feature]==X_sorted[i+1][feature]):
                continue
            else:
                threshold = (X_sorted[i][feature]+X_sorted[i+1][feature]  )/2
                y_left = Y_sorted[:i]
                y_right = Y_sorted[i:]

                gini_y = calculate_gini_impurity(y_left)
                gini_r = calculate_gini_impurity(y_right)
                mean_gini = (len(y_left)*gini_y + len(y_right)*gini_r)/n_values

                if (mean_gini < best_gini):
                    best_gini = mean_gini
                    best_feature = feature
                    best_threshold = threshold

    return best_feature,best_threshold






#Function to Built tree using decision making 
def Built_tree(X,Y,depth=0,max_depth=None,min_sample=1):

    if (
        (max_depth is not None and depth >= max_depth) or
        (len(Y) < min_sample) or
        (np.all(Y == Y[0])) 
    ):
        return Node(value=most_common_label(Y))

    feature, threshold = splitter(X, Y)

    if(feature is None):
        return Node(value=most_common_label(Y))
    
    
    left_index = X[:,feature]<=threshold
    right_index = X[:,feature]>threshold

    left_Node = Built_tree(X[left_index],Y[left_index],depth+1,max_depth,min_sample)
    right_Node = Built_tree(X[right_index],Y[right_index],depth+1,max_depth,min_sample)

    return Node(feature,threshold,left_Node,right_Node)







#Importing the training and testing Data
data = [
    [12.0, 1.5, 1, 'Wine'],
    [5.0, 2.0, 0, 'Beer'],
    [40.0, 0.0, 1, 'Whiskey'],
    [13.5, 1.2, 1, 'Wine'],
    [4.5, 1.8, 0, 'Beer'],
    [38.0, 0.1, 1, 'Whiskey'],
    [11.5, 1.7, 1, 'Wine'],
    [5.5, 2.3, 0, 'Beer']
]
test_data = np.array([
    [6.0, 2.1, 0],   # Expected: Beer
    [39.0, 0.05, 1], # Expected: Whiskey
    [13.0, 1.3, 1]   # Expected: Wine
])

labels = {"Wine":0,"Beer":1,"Whiskey":2}

#Coverting the labels and data into numpy arrays
X = np.array([row[:3] for row in data])
Y = np.array([labels.get(row[3]) for row in data])








#Defining the predict_single and predict Functions.
def predict_single(input, tree):
    if tree.value is not None:
        return tree.value
    
    if input[tree.feature_index] <= tree.threshold:
        return predict_single(input, tree.left)
    else:
        return predict_single(input, tree.right)

def predict(X_test, tree):
    return np.array([predict_single(row, tree) for row in X_test])








# Build the decision tree
tree = Built_tree(X, Y, max_depth=5)

# Make predictions on the test data
predicted = predict(test_data, tree)

# Reverse map labels for display
inv_labels = {v: k for k, v in labels.items()}
predicted_names = [inv_labels[val] for val in predicted]

# Print results
for i, sample in enumerate(test_data):
    print(f"Input: {sample} --> Predicted: {predicted_names[i]}")


#Function to display the decision tree(this i have copied the whole from chat gpt, not other fucntions though)
def plot_tree(node, x=0.5, y=1.0, dx=0.2, dy=0.1, ax=None, level=0):
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_axis_off()

    # Plot the current node
    if node.value is not None:
        label = inv_labels[node.value]
        color = 'lightgreen'
    else:
        label = f"X[{node.feature_index}] <= {round(node.threshold, 2)}"
        color = 'lightblue'

    ax.text(x, y, label, ha='center', va='center', 
            bbox=dict(boxstyle='round4', facecolor=color, edgecolor='black', linewidth=2))

    # Recurse for children
    if node.left is not None:
        x_left = x - dx / (2 ** level)
        y_child = y - dy
        ax.plot([x, x_left], [y, y_child], 'k-', lw=2)
        ax.text((x + x_left) / 2, (y + y_child) / 2, 'No', ha='center', va='center', fontsize=12, color='red')
        plot_tree(node.left, x_left, y_child, dx, dy, ax, level + 1)

    if node.right is not None:
        x_right = x + dx / (2 ** level)
        y_child = y - dy
        ax.plot([x, x_right], [y, y_child], 'k-', lw=2)
        ax.text((x + x_right) / 2, (y + y_child) / 2, 'Yes', ha='center', va='center', fontsize=12, color='green')
        plot_tree(node.right, x_right, y_child, dx, dy, ax, level + 1)

    if ax is None:
        plt.show()



#Printing the Decision Tree
print()
print()
print("****************************************************")
print()
print("The decision tree structure is :")
print()
plot_tree(tree)
plt.show()