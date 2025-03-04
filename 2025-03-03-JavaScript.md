---
layout: page
title: "JavaScript"
---

# <img src='https://www.tiobe.com/wp-content/themes/tiobe/tiobe-index/images/JavaScript.png' width='80'> JavaScript
# Official website
 JavaScript itself doesn't have a single “official website” in the way that some languages (or projects) do. Instead, JavaScript is standardized as ECMAScript, and its specifications are maintained by [Ecma International](https://www.ecma-international.org/).

Here are a couple of important resources:

1. **ECMAScript Specifications**:  
   The official ECMAScript website by Ecma International contains the standards and technical details about the language.  
   Link: [https://www.ecma-international.org/](https://www.ecma-international.org/)

2. **MDN Web Docs**:  
   For comprehensive documentation, tutorials, and guides on JavaScript (along with web technologies), the MDN Web Docs provided by Mozilla is widely regarded as one of the best resources.  
   Link: [https://developer.mozilla.org/en-US/docs/Web/JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

Depending on what you’re looking for—a formal specification or documentation and learning resources—you might choose one of these links.
# Static typing
 No, JavaScript is not statically typed—it is dynamically typed. This means that in JavaScript, data types are determined at runtime, and you can assign a value of any type to a variable without specifying the type in advance. For instance:

```javascript
let example = 42;   // example is initially a number
example = "hello";  // now example holds a string
```

In contrast, statically typed languages (such as Java, C#, or even TypeScript, which is a superset of JavaScript) require variables to have a declared type at compile time, allowing the compiler to catch type-related errors before the program runs.

If you're interested in adding static typing to JavaScript code, you might explore TypeScript or Flow, which offer optional type annotations that can help catch type errors early in the development process.
# Example code
 Below is one way to implement a function to search for a value in a binary search tree using JavaScript. In this example, we'll define a simple Node class to represent tree nodes and then implement a recursive search function. The function returns the node containing the value if it’s found, or null otherwise.

```javascript
// Define a Node class for a binary search tree.
class Node {
  constructor(value) {
    this.value = value;
    this.left = null;
    this.right = null;
  }
}

// Recursive function to search for a value in a binary search tree.
function searchBST(root, target) {
  // Base case: Empty tree or node is found.
  if (root === null) {
    return null;
  }
  if (root.value === target) {
    return root;
  }
  
  // If target is less than the current node's value, search left
  if (target < root.value) {
    return searchBST(root.left, target);
  } else {
    // Otherwise, search right
    return searchBST(root.right, target);
  }
}

// To test the algorithm, let's build a sample binary search tree:
function insertNode(root, value) {
  if (root === null) {
    return new Node(value);
  }
  if (value < root.value) {
    root.left = insertNode(root.left, value);
  } else if (value > root.value) {
    root.right = insertNode(root.right, value);
  }
  // For duplicate values, do nothing or handle as needed
  return root;
}

// Create a binary search tree.
let root = null;
const values = [50, 30, 70, 20, 40, 60, 80];
values.forEach(value => {
  root = insertNode(root, value);
});

// Test the searchBST function.
const target = 60;
const result = searchBST(root, target);

if (result !== null) {
  console.log(`Found node with value: ${result.value}`);
} else {
  console.log(`Value ${target} not found in the BST.`);
}
```

### Explanation

1. **Node class**:  
   Each node stores a value and pointers to its left and right children.

2. **searchBST function**:  
   - If the current node is `null`, return `null` (target not found).  
   - If the current node's value is equal to the target, return the node.  
   - If the target is less than the current node’s value, recursively search the left subtree; if greater, search the right subtree.

3. **insertNode function**:  
   This helper function inserts a new value into the tree, maintaining the binary search tree property. This is used to build the tree for testing.

4. **Testing**:  
   The code builds a BST with the specified values and then searches for the value 60, printing the result.

This implementation is a straightforward example of how to search within a binary search tree in JavaScript.
