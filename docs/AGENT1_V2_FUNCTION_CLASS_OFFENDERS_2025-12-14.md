# V2 Function/Class Limit Offenders Report

**Date**: 2025-12-14  
**Tool**: `tools/verify_v2_function_class_limits.py`  
**Scope**: Refactored messaging modules

## Verification Tool Created

✅ Created `tools/verify_v2_function_class_limits.py`:
- Checks function limit: 30 lines
- Checks class limit: 200 lines
- Generates offender list with file, line, and excess count

## Offender List (12 Function Violations Found)

### Critical Offenders (>100 lines excess):
1. **discord_message_handler.py:32** - `send_discord_message_to_agent()` - 205 lines (excess: 175)
2. **agent_message_handler.py:37** - `send_to_agent()` - 140 lines (excess: 110)
3. **cli_parser.py:37** - `create_messaging_parser()` - 157 lines (excess: 127)

### High Priority Offenders (50-100 lines excess):
4. **broadcast_handler.py:33** - `broadcast_to_all()` - 104 lines (excess: 74)
5. **message_formatters.py:81** - `_apply_template()` - 104 lines (excess: 74)

### Medium Priority Offenders (20-50 lines excess):
6. **multi_agent_request_handler.py:31** - `send_multi_agent_request()` - 77 lines (excess: 47)
7. **cli_handlers.py:35** - `handle_cycle_v2_message()` - 72 lines (excess: 42)
8. **message_formatters.py:308** - `_format_normal_message_with_instructions()` - 56 lines (excess: 26)
9. **cli_handlers.py:126** - `handle_message()` - 52 lines (excess: 22)
10. **service_adapters.py:56** - `send_message()` - 50 lines (excess: 20)

### Low Priority Offenders (<20 lines excess):
11. **service_adapters.py:110** - `broadcast_message()` - 40 lines (excess: 10)
12. **message_formatters.py:206** - `_format_multi_agent_request_message()` - 37 lines (excess: 7)

### Class Violations:
✅ No class limit violations found

## Next Steps

1. Run tool on all refactored modules
2. Identify specific offenders
3. Create refactoring plan for each offender
4. Prioritize by excess line count

