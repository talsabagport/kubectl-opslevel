# Scorecard Remediation Guide

## Quick Reference: Fix notification-service Owner Issue

### Problem
Entity `notification-service` fails the `ServiceOwnership_has-owner` scorecard rule.

### Quick Fix Options

#### Option 1: Via Port MCP (When Available)
```bash
# Run the automated script
./remediation/fix-notification-service-owner.sh <team-identifier>

# Example:
./remediation/fix-notification-service-owner.sh platform
```

#### Option 2: Via Port API
```bash
# Set your credentials
export PORT_CLIENT_ID="your-client-id"
export PORT_CLIENT_SECRET="your-client-secret"

# Update the entity
curl -X PATCH "https://api.getport.io/v1/blueprints/service/entities/notification-service" \
  -H "Authorization: Bearer $PORT_CLIENT_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "owner": "platform"
    }
  }'
```

#### Option 3: Via Kubernetes (If Synced from K8s)
```bash
# Add owner annotation to the deployment
kubectl annotate deployment notification-service \
  opslevel.com/owner="platform" \
  --overwrite

# Trigger sync to OpsLevel
OPSLEVEL_API_TOKEN=$TOKEN kubectl opslevel service import
```

### Required Information

1. **Team Identifier**: Which team should own notification-service?
   - Common examples: `platform`, `backend-team`, `notifications-team`
   - Must match an existing team in your system

2. **Source System**: Where is the service defined?
   - Port (internal catalog)
   - Kubernetes (synced via kubectl-opslevel)
   - OpsLevel (direct)

### Validation

After applying the fix:

```bash
# Check the entity in Port
curl -X GET "https://api.getport.io/v1/blueprints/service/entities/notification-service" \
  -H "Authorization: Bearer $PORT_CLIENT_SECRET"

# Verify owner field is set
# Check scorecard status shows "Passed" for ServiceOwnership_has-owner
```

### Files in This Remediation

- **ServiceOwnership_has-owner_notification-service.md**: Detailed investigation and remediation plan
- **fix-notification-service-owner.sh**: Automated remediation script
- **README.md**: This file

### Port MCP Server Status

**Current Status**: ❌ Error - Connection unavailable

The Port MCP server must be authenticated and connected to use automated tools. To fix:

1. Open Cursor Settings
2. Navigate to MCP Servers
3. Configure Port server with credentials
4. Test connection

### Support

- OpsLevel Documentation: https://docs.opslevel.com/
- Port Documentation: https://docs.getport.io/
- Repository: kubectl-opslevel

---

**Task ID**: ServiceOwnership_has-owner_notification-service-remediation  
**Created**: 2026-06-07  
**Status**: Pending - Awaiting Port MCP connection or manual execution
