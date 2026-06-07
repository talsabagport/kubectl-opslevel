#!/bin/bash
#
# Remediation Script: Fix notification-service ownership
# Task: ServiceOwnership_has-owner_notification-service-remediation
# Rule: ServiceOwnership_has-owner
# Entity: notification-service
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Notification Service Ownership Remediation"
echo "=========================================="
echo ""

# Configuration
ENTITY_IDENTIFIER="notification-service"
BLUEPRINT="service"  # Update if different

# Function to check Port MCP availability
check_port_mcp() {
    echo "Checking Port MCP server availability..."
    # This would require MCP CLI or API check
    echo "${YELLOW}⚠ Port MCP server check required${NC}"
    echo "Please verify Port MCP server is connected and authenticated"
    echo ""
}

# Function to get available teams
get_available_teams() {
    echo "Available teams that can be assigned as owners:"
    echo "${YELLOW}⚠ Requires Port MCP API call to list teams${NC}"
    echo ""
    echo "Example teams (update based on your organization):"
    echo "  - platform"
    echo "  - backend-team"
    echo "  - notifications-team"
    echo "  - infrastructure"
    echo ""
}

# Function to get current entity details
get_entity_details() {
    echo "Current entity details for: ${ENTITY_IDENTIFIER}"
    echo "${YELLOW}⚠ Requires Port MCP API call${NC}"
    echo ""
    echo "Expected query:"
    echo '  curl -X GET "https://api.getport.io/v1/blueprints/'${BLUEPRINT}'/entities/'${ENTITY_IDENTIFIER}'"'
    echo "       -H 'Authorization: Bearer \$PORT_CLIENT_SECRET'"
    echo ""
}

# Function to update entity with owner
update_entity_owner() {
    local team_identifier=$1
    
    if [ -z "$team_identifier" ]; then
        echo "${RED}✗ Error: Team identifier is required${NC}"
        echo "Usage: $0 <team-identifier>"
        exit 1
    fi
    
    echo "Updating entity '${ENTITY_IDENTIFIER}' with owner: ${team_identifier}"
    echo "${YELLOW}⚠ Requires Port MCP API call${NC}"
    echo ""
    echo "Expected payload:"
    cat <<EOF
{
  "identifier": "${ENTITY_IDENTIFIER}",
  "properties": {
    "owner": "${team_identifier}"
  }
}
EOF
    echo ""
    echo "API call:"
    echo "  curl -X PATCH 'https://api.getport.io/v1/blueprints/${BLUEPRINT}/entities/${ENTITY_IDENTIFIER}'"
    echo "       -H 'Authorization: Bearer \$PORT_CLIENT_SECRET'"
    echo "       -H 'Content-Type: application/json'"
    echo "       -d '<payload>'"
    echo ""
}

# Function to validate fix
validate_fix() {
    echo "Validating the fix..."
    echo "${YELLOW}⚠ Requires Port MCP API call to check scorecard${NC}"
    echo ""
    echo "Steps:"
    echo "1. Re-fetch entity details"
    echo "2. Verify 'owner' field is populated"
    echo "3. Check scorecard evaluation"
    echo "4. Confirm ServiceOwnership_has-owner rule passes"
    echo ""
}

# Main execution
main() {
    echo "Step 1: Checking Port MCP Server"
    echo "-----------------------------------"
    check_port_mcp
    
    echo "Step 2: Getting Available Teams"
    echo "-----------------------------------"
    get_available_teams
    
    echo "Step 3: Current Entity Details"
    echo "-----------------------------------"
    get_entity_details
    
    echo "Step 4: Update Entity"
    echo "-----------------------------------"
    
    if [ -z "$1" ]; then
        echo "${YELLOW}⚠ No team identifier provided${NC}"
        echo ""
        echo "To apply the fix, run:"
        echo "  $0 <team-identifier>"
        echo ""
        echo "Example:"
        echo "  $0 platform"
        echo ""
        exit 0
    fi
    
    update_entity_owner "$1"
    
    echo "Step 5: Validate Fix"
    echo "-----------------------------------"
    validate_fix
    
    echo "${GREEN}✓ Remediation script complete${NC}"
    echo ""
    echo "Note: This script provides guidance for manual execution."
    echo "Once Port MCP server is available, these operations can be automated."
}

# Alternative: Kubernetes-based fix
show_kubernetes_alternative() {
    echo ""
    echo "=========================================="
    echo "Alternative: Fix via Kubernetes"
    echo "=========================================="
    echo ""
    echo "If notification-service is synced from Kubernetes:"
    echo ""
    echo "1. Find the deployment:"
    echo "   kubectl get deployment notification-service --all-namespaces"
    echo ""
    echo "2. Add owner annotation:"
    echo "   kubectl annotate deployment notification-service \\"
    echo "     opslevel.com/owner=\"<team-alias>\" \\"
    echo "     --overwrite"
    echo ""
    echo "3. Trigger sync:"
    echo "   OPSLEVEL_API_TOKEN=\$TOKEN kubectl opslevel service import"
    echo ""
}

# Check if user wants to see alternatives
if [ "$1" == "--k8s" ] || [ "$1" == "--kubernetes" ]; then
    show_kubernetes_alternative
    exit 0
fi

# Run main script
main "$@"
