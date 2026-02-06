# Integrity Gates Reference

Non-negotiable checks enforced during implementation and verification.
Any gate failure = hard stop. No exceptions.

## Gate Definitions

### 1. NaN/Inf Gate

**When**: After any operation involving numerical computation (forward pass, loss, gradients).

**Check**:
```python
# After forward pass
assert torch.isfinite(output).all(), f"NaN/Inf in output: {torch.isnan(output).sum()} NaN, {torch.isinf(output).sum()} Inf"

# After loss computation
assert torch.isfinite(loss), f"NaN/Inf in loss: {loss.item()}"

# After backward pass
for name, p in model.named_parameters():
    if p.grad is not None:
        assert torch.isfinite(p.grad).all(), f"NaN/Inf gradient in {name}"
```

**On failure**: STOP immediately. Create diagnostic analyze script. Offer Retry/Debug/Abort.

**Common causes**:
- Division by zero (add eps)
- Unstable softmax (subtract max before exp)
- Learning rate too high
- Missing gradient clipping
- Log of zero or negative values

### 2. Shape Gate

**When**: After any modification to tensor operations, model architecture, or data pipeline.

**Check**:
```python
# Create minimal input with known shapes
x = torch.randn(2, 16, 512)  # (batch, seq_len, dim)
output = model(x)

# Verify against documented shapes
assert output.shape == (2, 16, 512), f"Expected (2, 16, 512), got {output.shape}"
```

**On failure**: STOP immediately. Shape errors cascade silently and cause hard-to-debug issues downstream.

**Common causes**:
- Transposed dimensions
- Missing/extra squeeze/unsqueeze
- Broadcasting gone wrong
- Off-by-one in slicing

### 3. Import Gate

**When**: After every code change.

**Check**:
```bash
python -c "import src.module_that_was_changed"
```

**On failure**: STOP. Usually a syntax error, missing import, or circular dependency.

### 4. Gradient Gate

**When**: After any change to model architecture or loss function.

**Check**:
```python
model = build_model(cfg)
x = torch.randn(2, 16, 512, requires_grad=False)
output = model(x)
loss = output.sum()  # Or actual loss function
loss.backward()

for name, p in model.named_parameters():
    assert p.grad is not None, f"No gradient for {name}"
    assert torch.isfinite(p.grad).all(), f"NaN/Inf gradient for {name}"
    # Optional: check gradient magnitude is reasonable
    grad_norm = p.grad.norm().item()
    assert grad_norm < 1e6, f"Exploding gradient for {name}: {grad_norm}"
```

**On failure**: STOP. Gradient issues mean the model cannot train.

### 5. Test Gate

**When**: After every code change.

**Check**:
```bash
pytest test/ -x --tb=short  # fail-fast
```

**On failure**: STOP if new failures introduced. Pre-existing failures should be noted but don't block.

## Severity Levels

| Gate | Severity | Can Skip? | Notes |
|------|----------|-----------|-------|
| NaN/Inf | CRITICAL | Never | Silent corruption if ignored |
| Shape | CRITICAL | Never | Cascading errors downstream |
| Import | HIGH | Never | Code doesn't run at all |
| Gradient | HIGH | Only if change is non-trainable | Model can't learn |
| Test | HIGH | Only with researcher approval | Regression risk |

## When to Apply Which Gates

| Change Type | NaN/Inf | Shape | Import | Gradient | Test |
|-------------|---------|-------|--------|----------|------|
| Model architecture | ✅ | ✅ | ✅ | ✅ | ✅ |
| Loss function | ✅ | ✅ | ✅ | ✅ | ✅ |
| Data pipeline | ✅ | ✅ | ✅ | — | ✅ |
| Training loop | ✅ | — | ✅ | ✅ | ✅ |
| Utility function | — | — | ✅ | — | ✅ |
| Config change | — | — | ✅ | — | ✅ |

## Standard Numerical Health Check

Reusable function for analyze scripts and verification:

```python
def check_numerical_health(tensor: torch.Tensor, name: str) -> bool:
    """Standard numerical health check. Returns True if healthy."""
    is_finite = torch.isfinite(tensor).all().item()
    nan_count = torch.isnan(tensor).sum().item()
    inf_count = torch.isinf(tensor).sum().item()

    print(f"--- {name} ---")
    print(f"  Shape: {tensor.shape}, dtype: {tensor.dtype}")
    print(f"  Finite: {is_finite}")
    print(f"  NaN: {nan_count}, Inf: {inf_count}")
    print(f"  Range: [{tensor.min().item():.6g}, {tensor.max().item():.6g}]")
    print(f"  Mean: {tensor.float().mean().item():.6g}, Std: {tensor.float().std().item():.6g}")

    return is_finite
```

## Observability During Training

When implementing training loops, REQUIRE these logs:

```python
# Per step (or every N steps):
logger.info(f"step={step}, loss={loss.item():.6f}")
logger.info(f"  grad_norm={grad_norm:.4f}")
logger.info(f"  param_norms: {param_norm_dict}")
logger.info(f"  lr={optimizer.param_groups[0]['lr']:.2e}")

# Per epoch:
logger.info(f"epoch={epoch}, train_loss={avg_train:.6f}, val_loss={avg_val:.6f}")

# Detect "looks like training but wrong":
# - Loss decreasing but val_loss increasing (overfitting)
# - Grad norm consistently near zero (dead gradients)
# - Param norms not changing (frozen by accident)
# - Loss stuck at constant value (mode collapse)
```
