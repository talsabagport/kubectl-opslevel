# Remediation Checklist: notification-service Owner Assignment

**Task**: ServiceOwnership_has-owner_notification-service-remediation  
**Date**: 2026-06-07  
**Assignee**: _____________  

## Pre-Requisites

- [ ] Port MCP server connection verified (or alternative access method identified)
- [ ] Appropriate permissions to modify service entities
- [ ] Team identifier/alias determined

## Investigation Phase

- [ ] **Query current entity state**
  - Entity identifier: `notification-service`
  - Blueprint: `service` (confirm)
  - Current owner value: _____________
  - Current scorecard status: Not passed

- [ ] **Identify correct owner team**
  - Team name: _____________
  - Team identifier/alias: _____________
  - Team confirmed in system: ☐ Yes ☐ No

- [ ] **Determine source of truth**
  - ☐ Port (internal catalog)
  - ☐ Kubernetes (synced)
  - ☐ OpsLevel (direct)
  - ☐ Other: _____________

## Remediation Phase

### Method Selected: ☐ Port MCP ☐ Port API ☐ Kubernetes ☐ OpsLevel UI

### Execution Steps

- [ ] **Backup current configuration** (if applicable)
  ```bash
  # Save current entity state
  # Document before making changes
  ```

- [ ] **Apply the fix**
  - Timestamp: _____________
  - Method used: _____________
  - Team assigned: _____________

- [ ] **Verify update applied**
  - Owner field populated: ☐ Yes ☐ No
  - Owner value correct: ☐ Yes ☐ No

## Validation Phase

- [ ] **Re-query entity**
  - Owner field value: _____________
  - Matches expected value: ☐ Yes ☐ No

- [ ] **Check scorecard status**
  - ServiceOwnership_has-owner rule: ☐ Passed ☐ Failed
  - Scorecard re-evaluated: ☐ Yes ☐ No
  - Overall score improved: ☐ Yes ☐ No

- [ ] **Monitor for persistence**
  - Wait for next sync cycle: _____________
  - Owner still assigned after sync: ☐ Yes ☐ No

## Documentation Phase

- [ ] **Document the fix**
  - Method used recorded
  - Team assignment justified
  - Source system updated (if needed)

- [ ] **Update runbooks/procedures**
  - Process documented for future
  - Team reference guide updated
  - Templates updated with owner requirement

## Post-Remediation

- [ ] **Close the task**
  - Task ID: ServiceOwnership_has-owner_notification-service-remediation
  - Closed date: _____________
  - Resolution notes: _____________

- [ ] **Review prevention measures**
  - Required field validation: ☐ Implemented ☐ Planned ☐ N/A
  - Default templates updated: ☐ Yes ☐ No ☐ N/A
  - CI/CD checks added: ☐ Yes ☐ No ☐ N/A

## Rollback Plan (If Needed)

If the fix causes issues:

- [ ] Revert to previous owner value: _____________
- [ ] Check for dependencies on owner assignment
- [ ] Document rollback reason
- [ ] Escalate to: _____________

## Notes

_Add any additional notes, observations, or issues encountered:_

```



```

## Sign-Off

- **Remediated by**: _____________ Date: _____________
- **Verified by**: _____________ Date: _____________
- **Approved by**: _____________ Date: _____________

---

**Status**: ☐ Not Started ☐ In Progress ☐ Completed ☐ Blocked

**Blocker** (if applicable): _____________________________________________
