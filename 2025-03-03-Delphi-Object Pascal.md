---
layout: page
title: "Delphi/Object Pascal"
---

# <img src='https://www.tiobe.com/wp-content/themes/tiobe/tiobe-index/images/Delphi_Object_Pascal.png' width='80'> Delphi/Object Pascal
# Official website
 The official website for Delphi, which is developed and maintained by Embarcadero Technologies, is available here:  
[https://www.embarcadero.com/products/delphi](https://www.embarcadero.com/products/delphi)

This site provides details about the latest releases, features, and documentation for Delphi/Object Pascal.
# Static typing
 Yes, Delphi (Object Pascal) is a statically typed language. This means that the type of a variable is known at compile-time, which allows for early detection of type errors and can lead to optimizations in the generated code.

A few points that further clarify this:

- **Explicit Type Declarations:** In Object Pascal, when you declare a variable, you're typically required to specify its type. For example:

  ```pascal
  var
    Number: Integer;
    Greeting: string;
  ```

  Here, the types of `Number` and `Greeting` are explicitly declared as `Integer` and `string`, respectively.

- **Compile-Time Type Checking:** The compiler checks variable types during compilation. This means that if you try to assign a value of an incompatible type to a variable, the compiler will generate an error before the program is run.

- **Type Inference (Limited):** Although Delphi is fundamentally statically typed, newer versions support some forms of type inference (particularly with anonymous methods and generics). However, the underlying type system remains static, ensuring that all types are known at compile time.

In summary, Object Pascal is a statically typed language, which contributes to its robustness, helps catch errors early, and improves code performance through compile-time optimizations.
# Example code
 Below is an example of how you can implement a binary search tree (BST) search algorithm in Delphi/Object Pascal. In this example, we define a BST node record, a pointer type for nodes, and a function that recursively searches a value in the BST.

```delphi
program BSTSearchExample;

{$APPTYPE CONSOLE}

uses
  SysUtils;

type
  // Define the record type for a BST node
  PTreeNode = ^TTreeNode;
  TTreeNode = record
    Value: Integer;
    Left, Right: PTreeNode;
  end;

{ 
  Function: SearchBST
  Description:
    Recursively searches for a specified value in a binary search tree.
  Parameters:
    Root  - pointer to the root node of the BST.
    Key   - the integer value to search for.
  Returns:
    A pointer to the node containing the Key, or nil if the value is not found.
}
function SearchBST(Root: PTreeNode; Key: Integer): PTreeNode;
begin
  if Root = nil then
    Exit(nil); // Tree is empty or reached end of branch

  if Root^.Value = Key then
  begin
    Exit(Root); // Found the key
  end
  else if Key < Root^.Value then
  begin
    // Search in the left subtree
    Exit(SearchBST(Root^.Left, Key));
  end
  else
  begin
    // Search in the right subtree
    Exit(SearchBST(Root^.Right, Key));
  end;
end;

{ 
  Procedure: InsertNode
  Description:
    Inserts a new integer value into the BST. The tree is modified in place.
  Parameters:
    var Root  - pointer to the root node of the BST.
    Value     - the integer value to insert.
}
procedure InsertNode(var Root: PTreeNode; Value: Integer);
begin
  if Root = nil then
  begin
    New(Root);
    Root^.Value := Value;
    Root^.Left := nil;
    Root^.Right := nil;
  end
  else if Value < Root^.Value then
  begin
    InsertNode(Root^.Left, Value);
  end
  else
  begin
    InsertNode(Root^.Right, Value);
  end;
end;

{ 
  Procedure: FreeTree
  Description:
    Recursively free all nodes of the BST.
  Parameters:
    Root - pointer to the root node of the BST.
}
procedure FreeTree(Root: PTreeNode);
begin
  if Root <> nil then
  begin
    FreeTree(Root^.Left);
    FreeTree(Root^.Right);
    Dispose(Root);
  end;
end;

var
  Root, FoundNode: PTreeNode;
  searchKey: Integer;
begin
  Root := nil;

  // Insert some sample values into the BST
  InsertNode(Root, 50);
  InsertNode(Root, 30);
  InsertNode(Root, 70);
  InsertNode(Root, 20);
  InsertNode(Root, 40);
  InsertNode(Root, 60);
  InsertNode(Root, 80);

  Write('Enter a value to search: ');
  ReadLn(searchKey);

  FoundNode := SearchBST(Root, searchKey);
  if FoundNode <> nil then
    Writeln('Value ', searchKey, ' found in the BST.')
  else
    Writeln('Value ', searchKey, ' was not found in the BST.');

  // Free the allocated nodes
  FreeTree(Root);
  
  ReadLn;
end.
```

### Explanation

1. **Data Types and Node Structure:**
   - `TTreeNode` is a record representing a node in the BST. It contains an integer `Value` and two pointers (`Left`, `Right`) to its child nodes.
   - `PTreeNode` is a pointer to `TTreeNode`.

2. **SearchBST Function:**
   - This function takes a pointer to the root of the tree and the desired search key.
   - It recursively navigates the tree: if the node is `nil`, it returns `nil`; if the node’s value matches the key, it returns the node; otherwise, it continues searching in the left or right subtree, depending on whether the key is less than or greater than the current node’s `Value`.

3. **InsertNode Procedure:**
   - This procedure inserts a new node into the BST in the correct location to maintain BST properties.
  
4. **FreeTree Procedure:**
   - Recursively deallocates all nodes in the BST to avoid memory leaks.

5. **Main Program:**
   - Inserts sample nodes into the BST.
   - Asks the user for a value to search and calls `SearchBST` to retrieve information about the node.
   - Outputs whether the value was found or not.
   - Frees the tree memory before ending.

This complete code is ready to compile and run in a Delphi environment.
