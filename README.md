# Tiny Out-of-Order CPU

This project implements a **minimal Out-of-Order (OoO) CPU** designed under the strict area constraints of TinyTapeout (~2000 cells). The goal is to demonstrate key microarchitectural concepts such as instruction scheduling, register renaming, and out-of-order execution in a compact design.

## Overview

The CPU supports a simple instruction set including:
- ADD, SUB, AND, OR, XOR (ALU operations)
- LD (memory operation)

Despite its small size, the processor includes essential OoO components:
- Instruction Queue (IQ)
- Register Alias Table (RAT)
- Reservation Stations (ALU + Memory)
- Reorder Buffer (ROB)
- Register File (RF)

## Key Features

- **Out-of-Order Execution**
  - Instructions execute as soon as operands are ready
- **In-order Commit**
  - Ensures correct program semantics using ROB
- **Register Renaming**
  - Eliminates WAR and WAW hazards using ROB index
- **Data Dependency Handling**
  - Supports RAW, WAR, and WAW scenarios

## Execution Flow

1. Instructions are fetched into the Instruction Queue
2. Instructions are decoded and issued if ROB and RS have space
3. Operands are checked:
   - Ready → execute immediately
   - Not ready → wait in RS
4. Execution:
   - ALU: 2 cycles
   - Memory: 4–5 cycles
5. Results written to ROB
6. Commit in program order → update register file

## Example Result

For a test program of 7 instructions:
- Total execution time: **28 cycles**
- Demonstrates true OoO execution due to different latencies

## Why this project?

This design shows how core CPU architecture concepts can be implemented even under extreme hardware constraints. It is intended as an educational demonstration of OoO execution mechanisms.

## Repository Structure

- `src/` → Verilog implementation
- `docs/info.md` → Detailed project description
- `test/` → Testbench and validation
