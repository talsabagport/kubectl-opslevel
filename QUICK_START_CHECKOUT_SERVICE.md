# Quick Start: Fix checkout-service Ownership

## Problem
`checkout-service` has no owner → Scorecard fails

## Solution (2 minutes)
```bash
# 1. Set credentials
export PORT_CLIENT_ID="your-client-id"
export PORT_CLIENT_SECRET="your-client-secret"

# 2. Run fix
python3 remediation/fix_checkout_service.py platform

# 3. Done! Scorecard will show "Passed" ✅
```

## What it does
Sets `checkout-service.owner = "platform"`

## Full docs
See `remediation/CHECKOUT_SERVICE_EXECUTION.md`

## PR
Branch: `cursor/fix-notification-service-owner-a70b`  
URL: https://github.com/talsabagport/kubectl-opslevel/pull/[number]

---
Task: ServiceOwnership_has-owner_checkout-service-remediation
