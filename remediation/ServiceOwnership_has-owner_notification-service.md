# Scorecard Remediation: ServiceOwnership_has-owner for notification-service

## Task Details
- **Task ID**: ServiceOwnership_has-owner_notification-service-remediation
- **Rule**: ServiceOwnership_has-owner
- **Entity**: notification-service
- **Status**: Not passed
- **Date**: 2026-06-07

## Problem Statement

The `notification-service` entity is failing the `ServiceOwnership_has-owner` scorecard rule. This indicates that the service does not have an owner/team assigned, which is a critical requirement for service governance and accountability.

## Root Cause

The service is missing an owner assignment. This can occur due to:

1. **Missing owner field**: The entity was created without an owner property
2. **Null/empty owner value**: The owner field exists but contains no value
3. **Invalid owner reference**: The owner field references a team that doesn't exist
4. **Sync issue**: The owner was set in source system (e.g., Kubernetes) but didn't sync properly

## Investigation Steps

### Step 1: Verify Port MCP Server Connection

```bash
# Check if Port MCP server is available
# The server needs to be configured and authenticated in Cursor
```

**Status**: Port MCP server is currently in error state and unavailable.

### Step 2: Query Entity Details (When Port MCP Available)

Once Port MCP server is restored, use these queries:

```javascript
// Get notification-service entity details
{
  "identifier": "notification-service",
  "blueprint": "service" // or appropriate blueprint name
}
```

### Step 3: Check Available Teams

Query available teams that can be assigned as owners:

```bash
# List all teams in the system
# This will help identify valid team identifiers
```

## Solution Options

### Option A: Direct Fix via Port API (Recommended)

**Prerequisites**:
- Port MCP server connection restored
- Valid team identifier identified
- Appropriate permissions to update entities

**Implementation**:

1. Identify the correct team/owner that should be assigned
2. Update the entity with the owner property
3. Verify the scorecard rule passes

**Example Update Payload**:
```json
{
  "identifier": "notification-service",
  "properties": {
    "owner": "<team-identifier>"
  }
}
```

### Option B: Fix via Source System (Kubernetes + OpsLevel)

If `notification-service` is synced from Kubernetes:

1. **Locate the Kubernetes resource**:
   ```bash
   kubectl get deployment notification-service -o yaml
   # or
   kubectl get deployment notification-service --all-namespaces -o yaml
   ```

2. **Add OpsLevel owner annotation**:
   ```bash
   kubectl annotate deployment notification-service \
     opslevel.com/owner="<team-alias>" \
     --overwrite
   ```

3. **Trigger sync**:
   ```bash
   OPSLEVEL_API_TOKEN=<token> kubectl opslevel service import
   ```

### Option C: Fix via OpsLevel UI

1. Navigate to: https://app.opslevel.com
2. Search for `notification-service`
3. Click on the service
4. Edit service properties
5. Set the "Owner" field to the appropriate team
6. Save changes

## Required Information

To complete the remediation, gather:

- [ ] Valid team identifier/alias for the owner
- [ ] Confirmation of which system is the source of truth (Port, OpsLevel, Kubernetes)
- [ ] Current entity properties (via Port API when available)
- [ ] Team list to verify valid owner options

## Validation Steps

After applying the fix:

1. **Verify entity update**:
   - Check that the owner field is populated
   - Confirm the owner value is valid

2. **Re-run scorecard evaluation**:
   - Trigger scorecard re-evaluation if not automatic
   - Verify `ServiceOwnership_has-owner` rule passes

3. **Monitor for drift**:
   - Ensure the fix persists after next sync cycle
   - Document the owner in source system if applicable

## Prevention Measures

To prevent this issue in the future:

1. **Enforce owner requirement**: Make owner a required field during service creation
2. **Validation rules**: Add pre-sync validation to check for owner annotation
3. **Default templates**: Create service templates with owner pre-populated
4. **Automated checks**: Set up CI/CD validation for required annotations
5. **Documentation**: Maintain a team alias reference guide

## Next Steps

**Immediate Actions Required**:

1. ✅ Created remediation documentation
2. ⏳ Restore Port MCP server connection
3. ⏳ Query entity details from Port
4. ⏳ Identify correct team owner
5. ⏳ Apply fix using appropriate method
6. ⏳ Validate scorecard rule passes

## References

- Repository: kubectl-opslevel
- OpsLevel Configuration: `/workspace/opslevel.yml`
- Sample Config: See README.md lines 91-132
- Owner mapping: `.metadata.annotations."opslevel.com/owner"`

## Notes

- Port MCP server must be authenticated and connected to execute automated fixes
- The repository contains tools for Kubernetes-to-OpsLevel sync, not Port integration
- Manual intervention via Port UI or API may be required
- Consider documenting the chosen remediation approach for future reference
