# 🚀 RV32I Simulator in Python

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![RISC-V](https://img.shields.io/badge/RISC--V-RV32I-red?style=for-the-badge)
![Simulator](https://img.shields.io/badge/Simulator-32Bit-success?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Computer-Architecture-orange?style=for-the-badge)

### ⚡ Python-based RV32I Simulator  
Execute 32-bit RISC-V machine code with support for registers, memory operations, branching, instruction tracing, and runtime error handling.

</div>

---

# 📌 Overview

This project implements a **RISC-V RV32I Simulator** in Python capable of executing 32-bit binary machine code instructions.

The simulator models core architectural components such as registers, memory, branching, stack management, and program counter updates while providing detailed execution tracing and runtime validation.

Designed for educational use, architecture simulations, and understanding low-level instruction execution.

---

# ✨ Features

✅ Executes 32-bit RV32I machine code  
✅ Supports R, I, S, B, U, and J instruction types  
✅ Simulates registers and memory operations  
✅ Handles branching and PC updates  
✅ Supports stack and data memory management  
✅ Generates register trace after every instruction  
✅ Provides memory dump generation  
✅ Detects infinite loops and invalid execution states  
✅ Includes alignment and runtime error checking  

---

# 🧠 Supported Instruction Types

| Type | Supported Instructions |
|------|-------------------------|
| 🔹 **R-Type** | `add`, `sub`, `sll`, `slt`, `sltu`, `xor`, `srl`, `or`, `and` |
| 🔹 **I-Type** | `lw`, `addi`, `sltiu`, `jalr` |
| 🔹 **S-Type** | `sw` |
| 🔹 **B-Type** | `beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu` |
| 🔹 **U-Type** | `lui`, `auipc` |
| 🔹 **J-Type** | `jal` |

---

# 📂 Project Structure

```bash
📦 RV32I-Simulator
 ┣ 📜 simulator.py
 ┣ 📜 input.txt
 ┣ 📜 output.txt
 ┗ 📜 README.md
```

---

# ⚙️ How to Run

## ▶️ Command

```bash
python simulator.py input.txt output.txt
```

---

# 📝 Input Format

The simulator accepts **32-bit binary machine code instructions** as input.

## 📥 Example (`input.txt`)

```text
00000000101000000000000010010011
00000001010000000000000100010011
00000000001000001000000110110011
00000000000000000000000001100011
```

---

# 📤 Output

The simulator generates:

- 🧾 Register trace after every instruction
- 💾 Memory dump
- ⚠️ Runtime error reports (if any)

---

# 🛡️ Runtime Error Handling

The simulator detects and reports:

| ❌ Error Type | 📌 Description |
|---|---|
| Invalid Opcode | Unsupported machine instruction |
| Misaligned Memory Access | Non-word-aligned memory address |
| Invalid Memory Address | Access outside allowed memory |
| Misaligned PC | PC not aligned to 4 bytes |
| PC Out of Range | PC exceeds instruction memory |
| Stack Pointer Error | Invalid stack pointer update |
| Infinite Loop Detection | Possible endless execution |
| Invalid Input | Non-binary instruction input |
| Missing Virtual Halt | Halt instruction not found |

---

# 🏗️ Architecture Components

| Component | Description |
|---|---|
| 🧠 Registers | 32 General Purpose Registers |
| 💾 Data Memory | Simulated data memory region |
| 📚 Stack Memory | Simulated stack region |
| 📍 Program Counter | Instruction execution tracking |
| 🔄 Branch Logic | Conditional and unconditional jumps |

---

# 🏗️ Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Core implementation |
| 📂 File Handling | Input/output processing |
| ⚙️ Bit Manipulation | Instruction decoding & execution |

---

# 🎯 Applications

- 📘 Computer Architecture coursework
- 🖥️ RISC-V ISA learning
- ⚙️ Machine code execution simulation
- 🧪 Architecture testing and debugging
- 📚 Educational and academic projects

---

# 🚧 Future Improvements

- 🔸 Pipeline simulation
- 🔸 Cache memory simulation
- 🔸 GUI-based execution visualizer
- 🔸 Step-by-step debugging mode
- 🔸 Performance statistics tracking

---

# 🤝 Team Project

This project was collaboratively developed by a team of four students as part of a Computer Architecture project.

## | Prabhav Agrawal | Simulator Development |


🎓 B.Tech Students  
📚 Computer Science and Applied Mathematics  

---

# 📄 Description

Python-based RV32I simulator that executes 32-bit RISC-V machine code with support for registers, memory operations, branching, instruction tracing, memory dumps, alignment checks, infinite loop detection, and runtime error handling.

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a star!

</div>
