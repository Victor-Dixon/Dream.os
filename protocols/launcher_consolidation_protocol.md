# Launcher Consolidation Protocol

## Trigger Conditions
- Multiple launcher scripts serve identical purposes
- PID file mismatches between launchers and service manager
- Duplicate implementations cause resource conflicts

## Protocol Steps
1. Audit all launcher scripts for functional overlap
2. Choose most robust implementation as primary
3. Standardize PID file naming to match service manager expectations
4. Add deprecation warnings to alternative launchers
5. Implement redirection logic for backward compatibility
6. Update service manager configuration
7. Test consolidated launcher and service management
8. Remove deprecated launchers after 2 swarm cycles

## Success Criteria
- Single launcher script exists
- Service manager commands work correctly
- No PID file conflicts
- Backward compatibility maintained
- No duplicate processes possible