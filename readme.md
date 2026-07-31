> A lightweight, clean, case-insensitive, dynamically typed scripting language built in Python.

Nova Script is an interpreted programming language designed from scratch with an intuitive and forgiving syntax. Keywords, variable names, and function identifiers are completely **case-insensitive**, making script writing fast and user-friendly.

---

## ✨ Features

- **Case-Insensitive Syntax** – Write keywords, variables, and function names in any case combination (`LET`, `let`, `Let`, `MyVar`, `myvar`).
- **Dynamic Typing** – Native support for numbers, strings, booleans, and `nil`.
- **First-Class Functions & Closures** – Named functions, recursion, and lexical block scoping.
- **Built-in Standard Library** – Includes `input()`, `clock()`, and `len()`.
- **Single-Line Comments** – Supports `//` comments.
- **Interactive REPL** – Execute code interactively.
- **Script Execution** – Run `.nova` files directly.

---

# Installation

## Android (Termux)

### 1. Install Python

```bash
pkg update && pkg upgrade -y
pkg install python -y
```

### 2. Create `nova.py`

```bash
nano nova.py
```

Paste your `nova.py` source code, then:

- **Ctrl + O** → Save
- **Enter**
- **Ctrl + X** → Exit

### 3. Make Executable

```bash
chmod +x nova.py
ln -s "$(pwd)/nova.py" $PREFIX/bin/nova
```

### 4. Verify

```bash
nova
```

---

## Linux (Ubuntu / Debian / Arch / Fedora / macOS)

### 1. Verify Python

```bash
python3 --version
```

### 2. Make Executable

Ensure the first line of `nova.py` is:

```python
#!/usr/bin/env python3
```

Then run:

```bash
chmod +x nova.py
```

### 3. Create System Link

```bash
sudo ln -s "$(pwd)/nova.py" /usr/local/bin/nova
```

### 4. Verify

```bash
nova
```

---

## Windows

### 1. Create the Installation Folder

Create:

```text
C:\NovaLang
```

Place `nova.py` inside it.

### 2. Create `nova.bat`

```bat
@echo off
python "%~dp0nova.py" %*
```

### 3. Add to PATH

1. Press **Win + R**
2. Type `sysdm.cpl`
3. Open **Advanced**
4. Click **Environment Variables**
5. Edit **Path**
6. Add:

```text
C:\NovaLang
```

Restart your terminal.

### 4. Verify

```powershell
nova
```

---

# Running Nova

## Interactive REPL

Run:

```bash
nova
```

Example:

```text
Nova Script 1.0 Shell (Case-Insensitive)
Type 'exit' to quit.

nova > LET name = INPUT("Enter name: ");
Enter name: Alex
nova > PRINT "Hello " + NAME;
Hello Alex
nova > EXIT
```

---

## Run a Script

```bash
nova script.nova
```

---

# Language Reference

## Data Types

| Type | Example | Python Type | Description |
|------|---------|-------------|-------------|
| Number | `42`, `3.14`, `-10` | `float` | Double-precision floating-point number |
| String | `"Hello"` | `str` | Supports concatenation with `+` |
| Boolean | `true`, `false` | `bool` | Case-insensitive |
| Nil | `nil` | `None` | Represents no value |

---

## Keywords

| Keyword | Example | Description |
|----------|----------|-------------|
| `let` | `LET x = 10;` | Declare a variable |
| `print` | `PRINT "Hello";` | Print a value |
| `fn` | `FN add(a,b){}` | Declare a function |
| `return` | `RETURN value;` | Return from a function |
| `if` / `else` | `IF x {}` | Conditional execution |
| `while` | `WHILE x {}` | Loop |
| `//` | `// comment` | Single-line comment |

---

## Operator Precedence

Highest → Lowest

1. Function Call / Grouping `()`
2. Unary `!`, `-`
3. Multiplication & Division `*`, `/`
4. Addition & Subtraction `+`, `-`
5. Comparison `< <= > >=`
6. Equality `== !=`
7. Assignment `=`

> **Truthiness:** Only `false` and `nil` are falsy. Everything else—including `0` and `""`—is truthy.

---

# Standard Library

| Function | Example | Description |
|----------|---------|-------------|
| `input(prompt)` | `LET name = INPUT("Name: ");` | Read user input |
| `clock()` | `LET t = CLOCK();` | Current Unix timestamp |
| `len(string)` | `LET n = LEN("text");` | String length |

---

# Examples

## Greeting

```nova
// greeting.nova

LET name = INPUT("What is your name? ");
LET length = LEN(name);

PRINT "Hello " + name + "!";
PRINT "Your name contains " + length + " letters.";
```

---

## Recursive Fibonacci

```nova
// fibonacci.nova

FN Fibonacci(n) {
    IF n <= 1 {
        RETURN n;
    }

    RETURN Fibonacci(n - 1) + Fibonacci(n - 2);
}

LET start = CLOCK();
LET target = 7;

LET result = Fibonacci(target);
LET elapsed = CLOCK() - start;

PRINT "Fibonacci(" + target + ") = " + result;
PRINT "Calculated in " + elapsed + " seconds.";
```

---

## Scope Test

```nova
// scope_test.nova

LET Count = 3;

WHILE Count > 0 {
    IF Count == 2 {
        PRINT "Midway point reached!";
    } ELSE {
        PRINT "Current count: " + Count;
    }

    Count = Count - 1;
}
```

---
