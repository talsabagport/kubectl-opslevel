#!/usr/bin/env python3
"""
Port API Remediation Script for checkout-service
Fixes ServiceOwnership_has-owner scorecard rule failure
"""

import os
import sys
import json
import requests
from typing import Optional, Dict, Any

# Configuration
PORT_API_BASE_URL = "https://api.getport.io/v1"
ENTITY_IDENTIFIER = "checkout-service"
BLUEPRINT = "service"

class PortAPIClient:
    """Port API client for entity operations"""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = PORT_API_BASE_URL
        self.access_token = None
    
    def authenticate(self) -> bool:
        """Authenticate with Port API"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/access_token",
                headers={"Content-Type": "application/json"},
                json={
                    "clientId": self.client_id,
                    "clientSecret": self.client_secret
                }
            )
            response.raise_for_status()
            self.access_token = response.json().get("accessToken")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def get_entity(self, blueprint: str, identifier: str) -> Optional[Dict[str, Any]]:
        """Get entity details"""
        try:
            response = requests.get(
                f"{self.base_url}/blueprints/{blueprint}/entities/{identifier}",
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get entity: {e}")
            return None
    
    def update_entity(self, blueprint: str, identifier: str, properties: Dict[str, Any]) -> bool:
        """Update entity properties"""
        try:
            response = requests.patch(
                f"{self.base_url}/blueprints/{blueprint}/entities/{identifier}",
                headers=self._get_headers(),
                json={"properties": properties}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to update entity: {e}")
            return False
    
    def list_teams(self) -> Optional[list]:
        """List available teams"""
        try:
            response = requests.get(
                f"{self.base_url}/blueprints/team/entities",
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json().get("entities", [])
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Could not list teams: {e}")
            return None

def print_banner():
    """Print script banner"""
    print("=" * 60)
    print("Port API - Checkout Service Owner Remediation")
    print("=" * 60)
    print()

def get_credentials() -> tuple:
    """Get Port API credentials from environment"""
    client_id = os.getenv("PORT_CLIENT_ID")
    client_secret = os.getenv("PORT_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Error: Port API credentials not found")
        print()
        print("Please set environment variables:")
        print("  export PORT_CLIENT_ID='your-client-id'")
        print("  export PORT_CLIENT_SECRET='your-client-secret'")
        print()
        sys.exit(1)
    
    return client_id, client_secret

def main():
    """Main execution"""
    print_banner()
    
    # Check for team identifier argument
    if len(sys.argv) < 2:
        print("Usage: python3 fix_checkout_service.py <team-identifier>")
        print()
        print("Example:")
        print("  python3 fix_checkout_service.py platform")
        print()
        print("Common team identifiers:")
        print("  - platform")
        print("  - backend-team")
        print("  - checkout-team")
        print("  - ecommerce-team")
        print()
        sys.exit(1)
    
    team_identifier = sys.argv[1]
    
    # Get credentials
    print("🔑 Loading Port API credentials...")
    client_id, client_secret = get_credentials()
    
    # Initialize client
    client = PortAPIClient(client_id, client_secret)
    
    # Authenticate
    print("🔐 Authenticating with Port API...")
    if not client.authenticate():
        sys.exit(1)
    print("✅ Authentication successful")
    print()
    
    # Get current entity state
    print(f"📋 Fetching current state of '{ENTITY_IDENTIFIER}'...")
    entity = client.get_entity(BLUEPRINT, ENTITY_IDENTIFIER)
    
    if entity:
        print("✅ Entity found")
        print()
        print("Current entity properties:")
        print(json.dumps(entity.get("properties", {}), indent=2))
        print()
        
        current_owner = entity.get("properties", {}).get("owner")
        if current_owner:
            print(f"⚠️  Current owner: {current_owner}")
            print(f"   Will update to: {team_identifier}")
        else:
            print(f"❌ No owner currently set")
            print(f"   Will set to: {team_identifier}")
        print()
    else:
        print(f"⚠️  Entity not found or error occurred")
        print()
    
    # List available teams
    print("📋 Checking available teams...")
    teams = client.list_teams()
    if teams:
        print(f"✅ Found {len(teams)} teams")
        team_identifiers = [t.get("identifier") for t in teams]
        
        if team_identifier in team_identifiers:
            print(f"✅ Team '{team_identifier}' exists")
        else:
            print(f"⚠️  Warning: Team '{team_identifier}' not found in teams list")
            print("   Available teams:", ", ".join(team_identifiers[:10]))
            
        print()
    
    # Confirm update
    response = input(f"Update '{ENTITY_IDENTIFIER}' with owner '{team_identifier}'? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("❌ Update cancelled")
        sys.exit(0)
    
    # Update entity
    print()
    print(f"🔄 Updating entity with owner: {team_identifier}...")
    
    success = client.update_entity(
        BLUEPRINT,
        ENTITY_IDENTIFIER,
        {"owner": team_identifier}
    )
    
    if success:
        print("✅ Entity updated successfully")
        print()
        
        # Verify update
        print("🔍 Verifying update...")
        updated_entity = client.get_entity(BLUEPRINT, ENTITY_IDENTIFIER)
        
        if updated_entity:
            new_owner = updated_entity.get("properties", {}).get("owner")
            if new_owner == team_identifier:
                print(f"✅ Verification successful: owner = {new_owner}")
                print()
                print("=" * 60)
                print("✅ REMEDIATION COMPLETE")
                print("=" * 60)
                print()
                print("Task: ServiceOwnership_has-owner_checkout-service-remediation")
                print("Entity: checkout-service")
                print(f"Owner: {new_owner}")
                print("Status: Fixed ✅")
                print()
                print("Next steps:")
                print("1. Verify scorecard shows rule passes")
                print("2. Monitor for persistence after sync cycles")
                print("3. Close the remediation task")
            else:
                print(f"⚠️  Warning: owner = {new_owner} (expected: {team_identifier})")
        else:
            print("⚠️  Could not verify update")
    else:
        print("❌ Update failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
