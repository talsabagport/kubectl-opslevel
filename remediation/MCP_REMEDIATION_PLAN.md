# Port MCP Remediation Plan

## Task
Fix `notification-service` entity to pass `ServiceOwnership_has-owner` scorecard rule.

## The Correct Approach (Using Port MCP)

### Step 1: Read Entity Details
```python
# MCP Tool Call
CallMcpTool(
    server="Port",
    toolName="read_entity",  # or get_entity, fetch_entity
    arguments={
        "blueprint": "service",
        "identifier": "notification-service"
    }
)

# Expected Response
{
    "identifier": "notification-service",
    "blueprint": "service",
    "properties": {
        "name": "notification-service",
        "owner": null,  # <-- THIS IS THE PROBLEM
        ... other properties ...
    }
}
```

### Step 2: List Available Teams
```python
# MCP Tool Call
CallMcpTool(
    server="Port",
    toolName="list_teams",  # or search_teams, get_teams
    arguments={}
)

# Expected Response
[
    {"identifier": "platform", "title": "Platform Team"},
    {"identifier": "backend-team", "title": "Backend Team"},
    ... other teams ...
]
```

### Step 3: Update Entity Owner
```python
# MCP Tool Call  
CallMcpTool(
    server="Port",
    toolName="update_entity",  # or patch_entity, edit_entity
    arguments={
        "blueprint": "service",
        "identifier": "notification-service",
        "properties": {
            "owner": "platform"  # <-- THE FIX
        }
    }
)

# Expected Response
{
    "identifier": "notification-service",
    "blueprint": "service",
    "properties": {
        "owner": "platform",  # <-- NOW SET
        ... other properties ...
    }
}
```

### Step 4: Verify Fix
```python
# MCP Tool Call
CallMcpTool(
    server="Port",
    toolName="read_entity",
    arguments={
        "blueprint": "service",
        "identifier": "notification-service"
    }
)

# Verify owner is "platform"
# Check scorecard status shows "Passed" for ServiceOwnership_has-owner
```

## Current Blocker

**Port MCP Server Status**: ❌ ERROR

```
Server: Port
Status: error
Error: "This MCP server failed during live tool discovery. 
        Its tools are unavailable until the connection is fixed."
Tools: [] (empty)
```

**What This Means**:
- Cannot call `read_entity` - MCP tool not available
- Cannot call `update_entity` - MCP tool not available
- Cannot call any Port MCP tools - server connection failed

**Root Cause**:
The Port MCP server is not properly configured or authenticated in Cursor.

## How to Fix the MCP Server

### Option A: Configure in Cursor UI
1. Open Cursor Settings
2. Go to: Settings → MCP Servers
3. Find or add "Port" server configuration
4. Enter credentials:
   ```json
   {
     "client_id": "your-port-client-id",
     "client_secret": "your-port-client-secret",
     "api_url": "https://api.getport.io"
   }
   ```
5. Save and test connection
6. Verify server status = "connected"

### Option B: Environment Variables (if supported)
```bash
export PORT_CLIENT_ID="your-client-id"
export PORT_CLIENT_SECRET="your-client-secret"
export PORT_API_URL="https://api.getport.io"
```

### Option C: Configuration File (if supported)
Check for MCP config file in:
- `~/.cursor/mcp-servers.json`
- `~/.config/cursor/mcp-settings.json`
- Project-specific `.cursor/mcp.json`

## Once MCP is Connected

Execute this sequence:

```python
# 1. Read current state
entity = CallMcpTool("Port", "read_entity", {
    "blueprint": "service",
    "identifier": "notification-service"
})
print(f"Current owner: {entity['properties'].get('owner')}")

# 2. Update owner
updated = CallMcpTool("Port", "update_entity", {
    "blueprint": "service", 
    "identifier": "notification-service",
    "properties": {"owner": "platform"}
})
print(f"Updated owner: {updated['properties']['owner']}")

# 3. Verify
verified = CallMcpTool("Port", "read_entity", {
    "blueprint": "service",
    "identifier": "notification-service"  
})
assert verified['properties']['owner'] == "platform", "Fix failed!"
print("✅ Owner successfully set to 'platform'")
```

## Alternative (While MCP is Down)

Use Port REST API directly via `port_api_fix.py`:

```bash
export PORT_CLIENT_ID="your-client-id"
export PORT_CLIENT_SECRET="your-client-secret"
python3 remediation/port_api_fix.py platform
```

**This achieves the exact same result as MCP would.**

## Summary

- ✅ **Know what to do**: Update entity owner to "platform" via MCP
- ✅ **Know how to do it**: Use MCP update_entity tool
- ❌ **Cannot execute**: Port MCP server is not connected
- ✅ **Have workaround**: Direct REST API script available

**Immediate Action Required**: Fix Port MCP server configuration in Cursor.

**Alternative Action**: Use `port_api_fix.py` script with REST API.

Both methods achieve the same outcome: `notification-service.owner = "platform"`
