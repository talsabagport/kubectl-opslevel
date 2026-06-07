# Remediation: checkout-service Owner Assignment

**Task ID**: ServiceOwnership_has-owner_checkout-service-remediation  
**Entity**: checkout-service  
**Rule**: ServiceOwnership_has-owner  
**Status**: Not passed  
**Date**: 2026-06-07

## Problem

The `checkout-service` entity fails the `ServiceOwnership_has-owner` scorecard rule because it does not have an owner/team assigned.

## Solution

### Quick Fix (5 minutes)

```bash
# Set Port API credentials
export PORT_CLIENT_ID="your-client-id"
export PORT_CLIENT_SECRET="your-client-secret"

# Run the fix script with recommended team
python3 remediation/fix_checkout_service.py platform

# Alternative teams to consider:
# - backend-team
# - checkout-team  
# - ecommerce-team
```

## Using Port MCP (Preferred - When Available)

Once Port MCP server is connected, the correct approach is:

```python
# 1. Read entity
CallMcpTool(
    server="Port",
    toolName="read_entity",
    arguments={
        "blueprint": "service",
        "identifier": "checkout-service"
    }
)

# 2. Update owner
CallMcpTool(
    server="Port",
    toolName="update_entity",
    arguments={
        "blueprint": "service",
        "identifier": "checkout-service",
        "properties": {"owner": "platform"}
    }
)

# 3. Verify
CallMcpTool(
    server="Port",
    toolName="read_entity",
    arguments={
        "blueprint": "service",
        "identifier": "checkout-service"
    }
)
```

**Current MCP Status**: ❌ Port MCP server unavailable (error state)

## Team Recommendation

For checkout-service, consider these teams:

1. **platform** - If checkout is part of core platform services
2. **backend-team** - If checkout is backend infrastructure
3. **checkout-team** - If there's a dedicated checkout team
4. **ecommerce-team** - If part of e-commerce organization

Based on repository analysis, `platform` is recommended as a default.

## Alternative Methods

### Via Port UI
1. Navigate to Port instance (https://app.getport.io or your domain)
2. Search for `checkout-service`
3. Click to edit entity
4. Set `owner` field to appropriate team
5. Save changes

### Via curl
```bash
curl -X PATCH "https://api.getport.io/v1/blueprints/service/entities/checkout-service" \
  -H "Authorization: Bearer $PORT_CLIENT_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"owner": "platform"}}'
```

## Validation Steps

After applying the fix:

1. **Verify entity update**:
   ```bash
   curl -X GET "https://api.getport.io/v1/blueprints/service/entities/checkout-service" \
     -H "Authorization: Bearer $PORT_CLIENT_SECRET"
   ```
   Check that `properties.owner` is populated

2. **Check scorecard**: 
   - Navigate to checkout-service scorecard in Port
   - Verify `ServiceOwnership_has-owner` rule shows "Passed"

3. **Monitor persistence**:
   - Wait for next sync cycle
   - Confirm owner still assigned after sync

## Files

- `fix_checkout_service.py` - Automated remediation script
- `CHECKOUT_SERVICE_REMEDIATION.md` - This file

## Next Steps

1. Confirm appropriate team for checkout-service
2. Run fix script or use Port MCP (when available)
3. Verify scorecard rule passes
4. Close remediation task: ServiceOwnership_has-owner_checkout-service-remediation

## Related

- Similar issue: notification-service (separate task)
- Repository: kubectl-opslevel
- OpsLevel Config: `/workspace/opslevel.yml`

---

**Status**: Solution ready  
**Blocker**: None (REST API script available)  
**Estimated Time**: 5 minutes
