# Nova Script (`.nova`)

> A lightweight, clean, dynamically typed scripting language built in Python.

Nova Script is an interpreted programming language built from scratch. It features a complete pipeline—including a hand-written **Lexer**, **Recursive Descent Parser**, **Abstract Syntax Tree (AST)** generator, and a **Tree-Walk Interpreter** with dynamic environment scoping.

---

## Features

- **Clean Syntax:** Simple keyword footprint (`let`, `fn`, `if`, `while`, `return`, `print`).
- **Dynamic Typing:** Support for numbers, strings, booleans, and `nil`.
- **First-Class Functions:** Define recursive functions and pass them around effortlessly.
- **Lexical Scoping:** Proper nested environment resolution for variables and function parameters.
- **Dual Execution Modes:** Run `.nova` script files directly or launch an interactive REPL shell.

---

## Quick Start (Linux / macOS)

### 1. Installation

Clone or download this repository, then make `nova.py` executable and link it to your system path:

```bash
# Make the Python file executable
chmod +x nova.py

# Create a system-wide command shortcut
sudo ln -s "$(pwd)/nova.py" /usr/local/bin/nova


## Language Specifications & Built-in Features

### 1. Data Types & Primitives

Nova Script supports four primary data types:

| Type | Syntax Example | Internal Type | Description |
| :--- | :--- | :--- | :--- |
| **Number** | `42`, `3.14`, `-10` | `float` | Double-precision floating-point. All numbers are floats internally. |
| **String** | `"hello"`, `'world'` | `str` | Double or single-quoted text. Supports concatenation with `+`. |
| **Boolean** | `true`, `false` | `bool` | Logical truth values. |
| **Nil** | `nil` | `None` | Represents null or an uninitialized variable state. |

---

### 2. Keywords & Syntax Reference

| Keyword / Symbol | Example Syntax | Description |
| :--- | :--- | :--- |
| **`let`** | `let x = 10;` | Declares a new variable in the current scope. |
| **`print`** | `print "Hello";` | Evaluates an expression and outputs the result to stdout. |
| **`fn`** | `fn add(a, b) { ... }` | Declares a named function with zero or more arguments. |
| **`return`** | `return a + b;` | Exits a function and returns a value. |
| **`if` / `else`** | `if x > 5 { ... } else { ... }` | Conditional branching based on truthiness. |
| **`while`** | `while i < 10 { ... }` | Loop construct that executes as long as condition evaluates to true. |
| **`true` / `false`** | `let flag = true;` | Boolean literals. |
| **`nil`** | `let empty = nil;` | Explicit null literal. |

---

### 3. Operator Precedence Hierarchy

Operators are evaluated in the following order (from highest to lowest precedence):

1. **Call & Grouping:** `()`
2. **Unary Operators:** `!` (Logical NOT), `-` (Numeric Negation)
3. **Multiplicative (Factor):** `*`, `/`
4. **Additive (Term):** `+` (Numeric addition or string concatenation), `-`
5. **Comparison:** `<`, `<=`, `>`, `>=`
6. **Equality:** `==`, `!=`
7. **Assignment:** `=`

> **Truthiness Rule:** Only `false` and `nil` are considered falsy. Numbers (`0`), empty strings (`""`), and all other values evaluate to `true`.

---

### 4. Scoping & Functions

- **Lexical Scoping:** Variables declared inside a block `{ ... }` or function are scoped locally and isolated from outer scopes.
- **First-Class Functions & Closures:** Functions can be stored in variables, passed to other functions, and maintain access to their parent scope context.
- **Recursion:** Functions can call themselves recursively.

---

### 5. Architectural Breakdown (`nova.py`)

The interpreter operates across four distinct phases:

1. **`Lexer` (Tokenizer):** Scans raw text character-by-character into typed `Token` objects, stripping whitespace and tracking line numbers for error messaging.
2. **`Parser` (Recursive Descent):** Processes tokens into an **Abstract Syntax Tree (AST)** according to language grammar rules and operator precedence hierarchy.
3. **`Environment` (Symbol Table):** Manages variable bindings and lexical scope chains through parent-enclosing scope links.
4. **`Interpreter` (Evaluator):** Walks AST nodes using the Visitor Pattern to execute statements and evaluate expressions dynamically at runtime.
