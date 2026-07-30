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