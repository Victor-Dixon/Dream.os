# Swarm Protocol: Dumb Messages → Real Work

## Coordination Doctrine Update

When receiving coordination requests, the protocol is now:

1. **Immediate Action**: Transform message receipt into executable work
2. **Parallel Execution**: Leverage swarm force multiplication
3. **Public Visibility**: Make work discoverable through commits and documentation
4. **Forward Momentum**: Push directives rather than acknowledge loops

## Infrastructure Standards

### WordPress Site Optimization Protocol
All WordPress sites must implement:
- Asset deferral for non-critical CSS
- Security header cleanup
- Database query optimization
- Resource preconnection hints
- Automated deployment verification

### Discord Bot Reliability Standards
- Direct imports for command modules (no conditional loading)
- Proper inheritance chains at import time
- Configuration file validation at startup
- Error isolation between command modules

## Deployment Automation Requirements

### Cross-Site Optimization Script
```bash
python scripts/deploy/apply_performance_optimizations.py
```

**Capabilities:**
- Automatic WordPress site discovery
- Standardized optimization application
- Error handling and rollback
- Deployment reporting and verification

### Verification Protocols
- Git status check before destructive operations
- Path-scoped commits to avoid workspace conflicts
- Documentation generation for knowledge persistence
- Public build signals for transparency

## Swarm Force Multiplication

### Bilateral Coordination Pattern
Agent pairs working in parallel provide:
- Strategic oversight + technical execution
- Quality assurance through dual review
- Knowledge transfer and skill development
- Risk mitigation through parallel paths

### Session Closure Standards
Every session must produce:
- Factual devlog (no narration)
- Commit with proper agent attribution
- Public build signal
- Cold-start handoff support
- Duplication audit verification

## Quality Assurance Protocols

### Import Strategy Governance
- Direct imports for critical dependencies
- No conditional loading of core functionality
- Import-time validation of inheritance chains
- Fast failure on dependency unavailability

### Performance Optimization Standards
- Measurable improvements (15-30% targets)
- Non-breaking changes (backwards compatibility)
- Automated verification
- Documentation of tradeoffs

This doctrine ensures swarm operations scale beyond individual capacity while maintaining quality and reliability standards.

## Thea Integration Protocol: Discord Command Standards

### Discord Command Integration Requirements
All Discord commands must implement:
- Admin-only access controls via @RoleDecorators.admin_only()
- Comprehensive error handling with user-friendly embeds
- Response timeout management (30-second default)
- Proper embed formatting with color coding
- Command logging for operational visibility

### Thea Service Integration Standards
- Direct TheaBrowserService usage for immediate functionality
- Graceful degradation on authentication failures
- Response content validation and truncation
- User attribution in all service calls
- Error isolation between commands

### API Compatibility Validation Protocol
```python
# REQUIRED: Validate service API before command registration
def validate_service_compatibility():
    try:
        service = get_thea_service()
        # Test basic functionality
        return service.is_initialized()
    except Exception:
        return False
```

### Swarm Coordination Force Multiplication
Bilateral agent coordination provides:
- **Architecture Agent**: System design and integration patterns
- **Infrastructure Agent**: Service implementation and deployment
- **Quality Agent**: Testing and validation
- **Documentation Agent**: Knowledge persistence and handoffs

### Command Lifecycle Governance
Discord commands follow strict lifecycle:
1. **Registration**: Commands added to bot lifecycle at startup
2. **Validation**: API compatibility verified before loading
3. **Execution**: Error boundaries with user feedback
4. **Logging**: All interactions recorded for analysis
5. **Cleanup**: Proper resource management on shutdown

This establishes Discord commands as first-class swarm interfaces, ensuring every agent interaction advances system capabilities.