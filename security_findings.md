# Security Findings

## CVE-2025-3000 — PyTorch Memory Corruption

- **Package:** torch 2.12.0
- **Link:** https://osv.dev/vulnerability/BIT-pytorch-2025-3000
- **Alleged trigger:** Manipulation of `torch.jit.script()` causes a memory buffer overflow (CWE-119). The vulnerability is triggered when untrusted Python code is compiled into a TorchScript graph via `torch.jit.script`.
