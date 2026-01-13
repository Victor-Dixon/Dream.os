<!-- SSOT Domain: documentation -->

# dream.os Standards

## 🎯 **Purpose**

This document serves as the **Single Source of Truth (SSOT)** for code quality standards, process rules, and reporting protocols across the dream.os Agent Cellphone V2 repository.

---

## 📏 **File Size Guidelines**

### **Guidelines (Clean Code Principles Take Precedence)**
- **Python Files**: ~400 lines (guideline - clean code principles take precedence)
- **Classes**: ~200 lines (guideline - prioritize single responsibility and cohesion)
- **Functions**: ~30 lines (guideline - prioritize clarity and maintainability)

**Note:** These are **guidelines**, not hard limits. Quality, clarity, and maintainability are more important than arbitrary line counts. Files exceeding these guidelines should be evaluated for:
- Single Responsibility Principle
- Code cohesion and maintainability
- Clear organization and documentation
- Whether splitting would improve or degrade code quality

### **Quality Evaluation (Not Enforcement)**
- **Pre-commit hooks**: Inform on files >400 lines (not blocking)
- **CI/CD pipeline**: Suggest review for files >600 lines
- **Code review**: Evaluate code quality, not just line counts

### **Guideline Reference Tiers**
- **≤400 lines**: ✅ Within guideline
- **401-500 lines**: ⚠️ Above guideline - evaluate code quality
- **501-600 lines**: 🔍 Review recommended - assess if splitting improves code
- **>600 lines**: 💡 Consider refactoring - evaluate if code quality benefits from modularization

**Remember:** Clean, well-organized, maintainable code is the goal. Line counts are just one indicator, not a hard rule.

---

## 🏗️ **Architecture Standards**

### **Design Principles**
1. **SOLID Compliance**: All modules must follow Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion principles
2. **Repository Pattern**: Use for all data access operations
3. **Service Layer**: Business logic isolated in service classes
4. **Dependency Injection**: Shared utilities via DI pattern
5. **No Circular Dependencies**: Maintain clear module boundaries

### **Code Organization**
- **Modular Design**: Each file has single, focused responsibility
- **Clear Boundaries**: Explicit separation between layers
- **Type Safety**: Type hints required for all functions/methods
- **Error Handling**: Comprehensive exception handling with logging

---

## 📝 **Code Style Standards**

### **Python Standards**
- **Style Guide**: PEP 8 compliance mandatory
- **Line Length**: ≤ 100 characters
- **Naming Conventions**:
  - `snake_case` for variables, functions, database columns
  - `PascalCase` for classes
  - `UPPER_CASE` for constants
- **Type Hints**: Required for all public functions/methods
- **Docstrings**: Required for all public classes and functions

### **Formatting Tools**
- **Black**: Auto-formatting (line length 100)
- **isort**: Import sorting
- **flake8**: Linting and style checking
- **mypy**: Type checking

---

## 🧪 **Testing Standards**

### **Coverage Requirements**
- **Minimum Coverage**: 85% for all new code
- **Critical Paths**: 100% coverage required
- **Test Framework**: pytest exclusively
- **Mocking**: Required for external APIs and database calls

### **Test Organization**
- **Unit Tests**: One test file per source file (`test_*.py`)
- **Integration Tests**: Separate `tests/integration/` directory
- **Fixtures**: Shared fixtures in `tests/conftest.py`
- **Test Naming**: Descriptive names following `test_<scenario>_<expected_result>` pattern

---

## 📊 **Reporting Standards**

### **Mission Summary Format**
**Single-line summary only**:
```
Agent-X: [Action Verb] [Target] - [Brief Result] ([Metric if applicable])
```

**Examples**:
- Agent-1: Fixed syntax errors in discord_commander_utils.py (15 errors resolved)
- Agent-2: Refactored messaging_service.py from 650→380 lines
- Agent-3: Applied Black formatting to 23 files across src/

### **Cycle Report Templates**

#### **Compact Cycle Report** (Default)
Use for regular check-ins and routine updates:
```markdown
## Agent-X Cycle Report

**Task**: [Brief task description]
**Status**: [Complete/In Progress/Blocked]
**Key Results**:
- [Result 1]
- [Result 2]
**Next**: [Next action]
```

#### **Full Cycle Report** (Milestones Only)
Use only for major milestones, project completions, or strategic updates:
```markdown
## Agent-X Full Cycle Report

**Mission**: [Detailed mission description]
**Duration**: [Time period]
**Objectives**: [What was planned]
**Execution**: [How it was done]
**Results**: [Detailed outcomes]
**Metrics**: [Quantified achievements]
**Learnings**: [Key insights]
**Next Phase**: [Strategic next steps]
```

### **Onboarding Templates**

#### **Minimal Onboarding** (Default)
```markdown
# Agent-X Onboarding

**Role**: [Agent role]
**Primary Task**: [Current assignment]
**Key Commands**:
- Check inbox: `ls agent_workspaces/Agent-X/inbox/`
- Update status: `echo {...} > status.json`
- Get task: `python -m src.services.messaging_cli --get-next-task`

**Start Working**: [Immediate action required]
```

#### **Full Onboarding** (New Agents Only)
Comprehensive onboarding with all protocols, tools, and context.

---

## 🔄 **Process Standards**

### **Commit Message Convention**
```
<type>: <short description>

[optional body]
[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
- `feat: add compact cycle report template`
- `fix: resolve circular import in messaging service`
- `docs: update STANDARDS.md with file size policy`

### **Pull Request Requirements**
1. **Code Review**: Required before merge
2. **CI Checks**: All tests must pass
3. **Linting**: No linter errors permitted
4. **Coverage**: Must maintain or improve coverage
5. **Documentation**: Update relevant docs

### **Workflow Standards**
1. **Branch Naming**: `<type>/<brief-description>` (e.g., `feat/lean-templates`)
2. **Small PRs**: Keep changes focused and reviewable
3. **Incremental Delivery**: Split large features into smaller PRs
4. **No Force Push**: To main/master branches
5. **Hook Compliance**: Never skip pre-commit hooks

---

## 📚 **Documentation Standards**

### **Required Documentation**
- **Docstrings**: All public functions, classes, methods
- **README Updates**: For new features or significant changes
- **CHANGELOG**: Record all notable changes
- **Usage Examples**: For new utilities or complex features

### **Documentation Style**
- **Clear and Concise**: Avoid verbosity
- **Code Examples**: Provide practical usage examples
- **Updated**: Keep docs synchronized with code changes
- **Accessible**: Write for developers at all skill levels

---

## 🎯 **V2 Compliance Standards**

### **Core Principles**
1. **Clean Code**: Readable, maintainable, self-documenting
2. **Tested Code**: Comprehensive unit and integration tests
3. **Reusable Code**: DRY principles, modular design
4. **Scalable Code**: Performance-optimized, efficient patterns

### **Quality Gates**
- **File Size**: Within defined limits
- **Test Coverage**: ≥ 85%
- **Linting**: Zero errors, minimal warnings
- **Type Safety**: Full type hint coverage
- **Documentation**: Complete and accurate

---

## 🚨 **Exception Policies**

### **Monitoring Component Exemption**
- **Path**: `src/core/health/monitoring/`
- **Exemption**: May use alternative technologies beyond Python if required for functionality
- **Rationale**: Monitoring tools may require specialized tech stacks

### **Legacy Code**
- **Gradual Migration**: Refactor legacy code incrementally
- **No New Violations**: Legacy exemptions don't apply to new code
- **Documentation**: Document all legacy exemptions with tickets

---

## 📈 **Continuous Improvement**

### **Regular Reviews**
- **Monthly**: Review and update standards as needed
- **Post-Milestone**: Assess effectiveness after major deliveries
- **Team Feedback**: Incorporate agent learnings and suggestions

### **Metrics Tracking**
- **File Size Distribution**: Monitor compliance trends
- **Test Coverage**: Track coverage improvements
- **Code Quality**: Measure linting violations, complexity
- **Velocity**: Assess impact on development speed

---

## 🔗 **Related Documentation**

- **AGENTS.md**: Agent development guidelines and swarm protocols
- **CYCLE_TIMELINE.md**: Cycle reporting procedures and templates
- **README.md**: Repository overview and quick start
- **CHANGELOG.md**: Version history and notable changes

---

## ✅ **Compliance Checklist**

Before committing code, verify:
- [ ] File size within limits (≤500 lines preferred, ≤600 max)
- [ ] PEP 8 compliant (Black formatted)
- [ ] Type hints on all public functions
- [ ] Docstrings on public classes/functions
- [ ] Unit tests written (≥85% coverage)
- [ ] Linter errors resolved
- [ ] Commit message follows convention
- [ ] Documentation updated
- [ ] Pre-commit hooks passed

---

**Version**: 1.0  
**Last Updated**: 2025-10-14  
**Maintained By**: Agent-4 (Captain & Strategic Oversight)

**This document is the authoritative source for all quality and process standards. When in doubt, consult STANDARDS.md.**

