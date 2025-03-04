---
layout: page
title: "Assembly language"
---

# <img src='https://www.tiobe.com/wp-content/themes/tiobe/tiobe-index/images/Assembly_language.png' width='80'> Assembly language
# Official website
 "Assembly language" refers to a category of low-level programming languages rather than a single language with one governing, official website. Each assembly language is generally specific to a processor architecture or developed by a particular vendor. For example:

- **x86 Assembly:**
  - There isn’t one "official" website for x86 assembly as a whole. However, you might want to check out resources from Intel or AMD.  
    • Intel’s manuals: [Intel® 64 and IA-32 Architectures Software Developer Manuals](https://software.intel.com/en-us/articles/intel-sdm)  
    • AMD’s manuals: [AMD Developer Guides and Manuals](https://www.amd.com/en/support)

- **MASM (Microsoft Macro Assembler):**
  - You can find official Microsoft documentation on MASM as part of their development tools: [Microsoft MASM documentation](https://docs.microsoft.com/en-us/cpp/assembler/masm/)

- **NASM (Netwide Assembler):**
  - NASM is an open-source assembler, and you can visit its official website: [NASM Official Website](https://www.nasm.us/)

If you were referring to a general resource or a specific assembly language version, please let me know so I can point you toward the most relevant official website or documentation.
# Static typing
 Assembly language is generally considered to be untyped rather than statically typed. Here's why:

1. **Lack of Type System:**  
   Assembly language operates very close to the hardware level. Instructions in assembly work on registers and memory addresses without enforcing a type system like those found in high-level languages (e.g., C, Java, or Haskell). There's no built-in mechanism to restrict operations to certain “types” of data.

2. **Interpretation of Data:**  
   In assembly, data is essentially just bits. How those bits are interpreted (as integers, floating-point numbers, characters, etc.) is determined by the instructions or by the programmer’s intent rather than by a type-checking system.

3. **No Compile-Time Type Checking:**  
   Static typing in high-level languages means the compiler enforces type rules at compile time. Assembly language assemblers do not perform such type checking, so they do not enforce data types before the program runs.

4. **Responsibility on the Programmer:**  
   Since assembly does not check types, it is up to the programmer to ensure that they are using data and instructions correctly. Misinterpreting data (for example, treating an address as data or vice versa) can lead to incorrect behavior, but the assembler won't flag this as a type error.

In summary, assembly language is not statically typed; it simply lacks a type system altogether, leaving all type management and interpretation up to the programmer.
# Example code
 Below is an example of an x86 Assembly algorithm written in NASM syntax that searches for a value in a binary search tree. In this example, each node of the tree is assumed to have the following structure (in C notation):

  struct Node {
    int value;      ; 4 bytes at offset 0
    struct Node *left;  ; 4 bytes at offset 4
    struct Node *right; ; 4 bytes at offset 8
  };

The function bst_find takes two arguments:
 • A pointer to the root node (first argument)
 • The target value to be found (second argument)

It returns in EAX a pointer to the node that contains the specified value, or 0 if the value is not found.

Below is the complete assembly code:

```nasm
;----------------------------------------------------------------------------
; binary_search_tree.asm
;----------------------------------------------------------------------------
; This routine implements a binary search in a binary search tree.
; Each node is assumed to have the following structure:
;
;   struct Node {
;       int value;         ; offset 0
;       struct Node *left;  ; offset 4
;       struct Node *right; ; offset 8
;   };
;
; The function bst_find receives:
;   - [ESP + 4] : Pointer to the root node
;   - [ESP + 8] : Target value to search for
;
; It returns:
;   - EAX : Pointer to the found node, or 0 if not found.
;----------------------------------------------------------------------------

SECTION .text
global bst_find

bst_find:
    push ebp
    mov  ebp, esp

    ; Load arguments:
    ; First argument: pointer to root node
    mov  esi, [ebp+8]
    ; Second argument: target value we are looking for
    mov  ebx, [ebp+12]

search_loop:
    ; If the current node pointer in ESI is NULL, value not found.
    cmp  esi, 0
    je   not_found

    ; Load the current node's value (stored at offset 0) into EAX.
    mov  eax, [esi]      
    
    ; Compare the target value (in EBX) to the node's value.
    cmp  ebx, eax
    je   found         ; The values are equal, node found.

    ; If target is less than current node's value, go to the left sub-tree.
    jl   go_left

    ; Otherwise, go to the right sub-tree.
    mov  esi, [esi+8]  ; Pointer to right child (offset 8)
    jmp  search_loop

go_left:
    mov  esi, [esi+4]  ; Pointer to left child (offset 4)
    jmp  search_loop

found:
    ; Node found. Return pointer in EAX.
    mov  eax, esi
    jmp  finish

not_found:
    ; Not found. Return 0.
    mov  eax, 0

finish:
    mov  esp, ebp
    pop  ebp
    ret
```

### Explanation

1. **Function Setup and Argument Retrieval:**
   - The function sets up the stack frame by pushing EBP and moving ESP into EBP.
   - It then loads the pointer to the root node into ESI and the target value into EBX.

2. **Search Loop:**
   - The loop starts by checking if the current node pointer (`ESI`) is NULL. If it is, the search terminates because the value isn’t in the tree.
   - It retrieves the node's value (from offset 0) and compares it with the target.
   - If the values are equal, it jumps to the `found` label.
   - If the target is less, the function moves to the left child (stored at offset 4). Otherwise, it moves to the right child (stored at offset 8).

3. **Return:**
   - If the node is found, the pointer to that node is returned in `EAX`.
   - If not found, `EAX` is set to 0.
   - The function then restores the previous stack frame and returns.

This example should be assembled with NASM and linked appropriately depending on your system and calling conventions.
