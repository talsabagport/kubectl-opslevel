# Port MCP Server Issue - Blocking Remediation

## Current Problem

The Port MCP server is in an **error state** and its tools are unavailable. This prevents using the MCP to:
- Read the `notification-service` entity details
- Query available teams
- Update the entity owner field

## Error Details

```
Server: Port
Status: error
Error: "This MCP server failed during live tool discovery. Its tools are unavailable until the connection is fixed."
Tools Available: [] (empty)
```

## Required Action

The Port MCP server needs to be authenticated and connected in Cursor before the remediation can proceed.

### Steps to Fix MCP Connection

1. **Open Cursor Settings**
   - Go to Settings → MCP Servers

2. **Configure Port MCP Server**
   - Ensure Port server credentials are set correctly
   - Required credentials typically include:
     - Port Client ID
     - Port Client Secret
     - Port API URL (if custom)

3. **Test Connection**
   - Save the configuration
   - Verify the server shows as "connected" or "ready"
   - Check that tools are discoverable

4. **Verify Tools Available**
   Once connected, the Port MCP server should provide tools like:
   - `read_entity` - Read entity details
   - `update_entity` - Update entity properties
   - `list_entities` - List entities in a blueprint
   - `search_entities` - Search for entities
   - Similar tools for teams, blueprints, etc.

## What I Can Do After MCP is Fixed

Once the Port MCP server is connected, I can:

1. **Read entity details**:
   ```
   Use Port MCP tool to get notification-service entity
   Check current owner value (likely null/empty)
   ```

2. **Query available teams**:
   ```
   Use Port MCP tool to list teams
   Confirm 'platform' team exists
   Get team identifier
   ```

3. **Update the owner**:
   ```
   Use Port MCP tool to update entity
   Set owner property to 'platform' (or appropriate team)
   ```

4. **Verify the fix**:
   ```
   Re-read entity to confirm owner is set
   Check scorecard status
   ```

## Temporary Workarounds

While the MCP server is being fixed, you can:

### Option 1: Use Port REST API Directly
```bash
export PORT_CLIENT_ID="your-client-id"
export PORT_CLIENT_SECRET="your-client-secret"

python3 remediation/port_api_fix.py platform
```

### Option 2: Use Port UI
1. Navigate to https://app.getport.io (or your Port instance)
2. Search for `notification-service`
3. Edit the entity
4. Set the `owner` field to `platform`
5. Save changes

### Option 3: Use curl
```bash
curl -X PATCH "https://api.getport.io/v1/blueprints/service/entities/notification-service" \
  -H "Authorization: Bearer $PORT_CLIENT_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"owner": "platform"}}'
```

## Recommended Immediate Action

**Priority**: Fix Port MCP server connection in Cursor settings

**Then**: I can use the MCP tools to:
1. Read the entity
2. Update the owner
3. Verify the fix
4. Close the remediation task

---

**Status**: Blocked by MCP server connection  
**Blocker Owner**: User/Admin (MCP configuration)  
**Next Step**: Configure Port MCP server in Cursor settings
