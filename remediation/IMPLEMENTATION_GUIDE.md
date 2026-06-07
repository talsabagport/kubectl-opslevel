# Implementation Guide: Notification Service Owner Remediation

**Generated**: 2026-06-07  
**Task**: ServiceOwnership_has-owner_notification-service-remediation  
**Priority**: High (Scorecard compliance)

## Executive Summary

The `notification-service` entity fails the `ServiceOwnership_has-owner` scorecard rule. This PR provides automated tooling and documentation to assign an owner team to the service.

## Recommended Team Assignment

Based on analysis of the repository configuration (`opslevel.yml`), the suggested team owner is:

**Team**: `platform`

**Rationale**:
- This repository's service (kubectl-opslevel) is owned by `platform` team
- Notification services typically fall under platform/infrastructure domains
- Consistent with organizational patterns

**Alternative teams to consider**:
- `backend-team` - If notification-service is part of backend infrastructure
- `notifications-team` - If there's a dedicated team for notifications
- `infrastructure` - If managed by infrastructure team

## Quick Start

### Prerequisites
```bash
# Ensure you have Port API credentials
export PORT_CLIENT_ID="your-client-id"
export PORT_CLIENT_SECRET="your-client-secret"
```

### Execute Fix (Recommended)
```bash
# Option 1: Using Python script (interactive)
python3 remediation/port_api_fix.py platform

# Option 2: Using curl (direct)
curl -X PATCH "https://api.getport.io/v1/blueprints/service/entities/notification-service" \
  -H "Authorization: Bearer $PORT_CLIENT_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"owner": "platform"}}'
```

## Implementation Steps

### Phase 1: Preparation (5 minutes)
1. ✅ Review remediation documentation (completed)
2. ⏳ Confirm team identifier: `platform` or alternative
3. ⏳ Verify Port API credentials are available
4. ⏳ Review current entity state in Port

### Phase 2: Execution (5 minutes)
1. ⏳ Run automated script: `python3 remediation/port_api_fix.py platform`
2. ⏳ Confirm the update when prompted
3. ⏳ Verify the script reports success

### Phase 3: Validation (5 minutes)
1. ⏳ Check entity in Port UI - verify owner field is set
2. ⏳ Re-run scorecard evaluation (may be automatic)
3. ⏳ Confirm `ServiceOwnership_has-owner` rule passes
4. ⏳ Close the remediation task

**Total estimated time**: 15 minutes

## Troubleshooting

### Issue: Port MCP Server Unavailable
**Solution**: Use the Python script (`port_api_fix.py`) which uses REST API directly

### Issue: Authentication Failed
**Solution**: Verify credentials are set correctly:
```bash
echo $PORT_CLIENT_ID
echo $PORT_CLIENT_SECRET
```

### Issue: Team Not Found
**Solution**: List available teams and select a valid one:
```bash
curl -X GET "https://api.getport.io/v1/blueprints/team/entities" \
  -H "Authorization: Bearer $PORT_CLIENT_SECRET"
```

### Issue: Entity Not Found
**Solution**: Verify entity identifier and blueprint:
```bash
curl -X GET "https://api.getport.io/v1/blueprints/service/entities/notification-service" \
  -H "Authorization: Bearer $PORT_CLIENT_SECRET"
```

## Files Reference

| File | Purpose | Usage |
|------|---------|-------|
| `port_api_fix.py` | Automated fix script | `python3 port_api_fix.py <team>` |
| `fix-notification-service-owner.sh` | Manual guidance | `./fix-notification-service-owner.sh` |
| `ServiceOwnership_has-owner_notification-service.md` | Detailed analysis | Read for background |
| `CHECKLIST.md` | Progress tracker | Fill in as you progress |
| `README.md` | Quick reference | Fast command lookup |

## Success Criteria

- [x] Remediation tooling created
- [x] Documentation completed
- [x] Multiple fix options provided
- [ ] Team identifier confirmed
- [ ] Fix executed
- [ ] Entity owner field populated
- [ ] Scorecard rule passes
- [ ] Task closed

## Next Actions

**Immediate** (Required before closing):
1. Confirm team identifier (`platform` recommended)
2. Execute fix using one of the provided methods
3. Validate scorecard rule passes

**Follow-up** (Recommended):
1. Document owner assignment policy
2. Add validation to service creation process
3. Update service templates with required fields
4. Schedule audit of other services

## Support Contacts

- **Port API Issues**: Port support team
- **Scorecard Questions**: Governance team
- **Team Assignment**: Service/platform team leads
- **Technical Issues**: Platform engineering

## Rollback

If the fix needs to be reverted:
```bash
python3 remediation/port_api_fix.py <original-team>
# or
curl -X PATCH "https://api.getport.io/v1/blueprints/service/entities/notification-service" \
  -H "Authorization: Bearer $PORT_CLIENT_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"owner": "<original-team>"}}'
```

## Questions?

Refer to:
- `remediation/README.md` - Quick reference
- `remediation/ServiceOwnership_has-owner_notification-service.md` - Detailed analysis
- Port Documentation: https://docs.getport.io/
- OpsLevel Documentation: https://docs.opslevel.com/

---

**Status**: Ready for execution  
**Blocker**: Port API credentials required  
**Next Step**: Execute `python3 remediation/port_api_fix.py platform`
