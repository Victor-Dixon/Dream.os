"""
<!-- SSOT Domain: integration -->

Architectural Principles Data Definitions
==========================================

Individual principle definitions extracted for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

from .architectural_models import ArchitecturalGuidance, ArchitecturalPrinciple


def get_srp_guidance() -> ArchitecturalGuidance:
    """Get Single Responsibility Principle guidance."""
    return ArchitecturalGuidance(
        principle=ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
        display_name="Single Responsibility Principle (SRP)",
        description="A class should have only one reason to change",
        responsibilities=[
            "Ensure each class/module has single, well-defined purpose",
            "Identify and eliminate classes with multiple responsibilities",
            "Create focused, cohesive units of functionality",
            "Maintain clear separation of concerns",
        ],
        guidelines=[
            "Classes should have 1-3 public methods maximum",
            "Methods should perform one specific task",
            "Avoid 'God classes' that do everything",
            "Use composition over inheritance for complex behaviors",
        ],
        examples=[
            "Separate data access from business logic",
            "Extract validation logic into dedicated classes",
            "Create specific handlers for different message types",
            "Isolate configuration from application logic",
        ],
        validation_rules=[
            "No class should have more than 3 public methods",
            "Methods should be under 30 lines",
            "Classes should be under 200 lines",
            "Circular dependencies must be eliminated",
        ],
    )


def get_ocp_guidance() -> ArchitecturalGuidance:
    """Get Open-Closed Principle guidance."""
    return ArchitecturalGuidance(
        principle=ArchitecturalPrinciple.OPEN_CLOSED,
        display_name="Open-Closed Principle (OCP)",
        description="Software entities should be open for extension but closed for modification",
        responsibilities=[
            "Design extensible systems without modifying existing code",
            "Implement plugin architectures and extension points",
            "Use abstraction to enable future enhancements",
            "Create frameworks that support new features",
        ],
        guidelines=[
            "Use abstract base classes for extension points",
            "Implement strategy pattern for algorithm variations",
            "Create configuration-driven behavior",
            "Use dependency injection for flexibility",
        ],
        examples=[
            "Message handlers that can be extended without modification",
            "Plugin system for different delivery backends",
            "Configurable validation rules",
            "Extensible command pattern implementation",
        ],
        validation_rules=[
            "New features should not require code changes",
            "Extension points must be clearly defined",
            "Configuration should drive behavior, not code",
            "Abstract interfaces must be stable",
        ],
    )


def get_lsp_guidance() -> ArchitecturalGuidance:
    """Get Liskov Substitution Principle guidance."""
    return ArchitecturalGuidance(
        principle=ArchitecturalPrinciple.LISKOV_SUBSTITUTION,
        display_name="Liskov Substitution Principle (LSP)",
        description="Objects of a superclass should be replaceable with objects of its subclasses without breaking the application",
        responsibilities=[
            "Ensure derived classes maintain parent class contracts",
            "Prevent violations of behavioral subtyping",
            "Maintain substitutability in inheritance hierarchies",
            "Validate that overridden methods preserve invariants",
        ],
        guidelines=[
            "Subclasses must not weaken preconditions",
            "Subclasses must not strengthen postconditions",
            "Subclasses must preserve invariants of parent class",
            "Use composition when inheritance violates LSP",
        ],
        examples=[
            "Repository implementations that can be swapped",
            "Publisher interfaces with multiple platform implementations",
            "Handler classes that maintain consistent behavior",
            "Service interfaces with interchangeable implementations",
        ],
        validation_rules=[
            "All subclasses must pass parent class tests",
            "No subclass should throw exceptions parent doesn't",
            "Subclasses must honor all parent class contracts",
            "Inheritance hierarchies must maintain substitutability",
        ],
    )


def get_isp_guidance() -> ArchitecturalGuidance:
    """Get Interface Segregation Principle guidance."""
    return ArchitecturalGuidance(
        principle=ArchitecturalPrinciple.INTERFACE_SEGREGATION,
        display_name="Interface Segregation Principle (ISP)",
        description="Clients should not be forced to depend on interfaces they do not use",
        responsibilities=[
            "Create focused, client-specific interfaces",
            "Avoid fat interfaces with too many methods",
            "Split large interfaces into smaller, cohesive ones",
            "Prevent clients from depending on unused methods",
        ],
        guidelines=[
            "Interfaces should be small and focused",
            "Clients should only depend on methods they use",
            "Split interfaces by client needs, not by functionality",
            "Use composition to combine multiple interfaces",
        ],
        examples=[
            "Separate read/write interfaces for repositories",
            "Platform-specific publisher interfaces",
            "Handler interfaces split by message type",
            "Service interfaces segregated by use case",
        ],
        validation_rules=[
            "No class should implement unused interface methods",
            "Interfaces should have 3-5 methods maximum",
            "Clients should not depend on methods they don't call",
            "Large interfaces must be split into smaller ones",
        ],
    )


def get_dip_guidance() -> ArchitecturalGuidance:
    """Get Dependency Inversion Principle guidance."""
    return ArchitecturalGuidance(
        principle=ArchitecturalPrinciple.DEPENDENCY_INVERSION,
        display_name="Dependency Inversion Principle (DIP)",
        description="High-level modules should not depend on low-level modules. Both should depend on abstractions",
        responsibilities=[
            "Depend on abstractions, not concrete implementations",
            "Invert dependency direction from low to high level",
            "Use dependency injection for flexibility",
            "Create stable abstractions for volatile implementations",
        ],
        guidelines=[
            "High-level modules should not import low-level modules",
            "Both should depend on abstractions (interfaces)",
            "Use dependency injection containers",
            "Abstract interfaces should be in high-level modules",
        ],
        examples=[
            "Services depend on repository interfaces, not implementations",
            "Controllers depend on service interfaces",
            "Engines depend on abstract analyzers",
            "Publishers depend on abstract base classes",
        ],
        validation_rules=[
            "No high-level module should import low-level modules directly",
            "All dependencies should go through interfaces",
            "Concrete classes should implement abstractions",
            "Dependency injection must be used for all external dependencies",
        ],
    )


def get_ssot_guidance() -> ArchitecturalGuidance:
    """Get Single Source of Truth guidance."""
    return ArchitecturalGuidance(
        principle=ArchitecturalPrinciple.SINGLE_SOURCE_OF_TRUTH,
        display_name="Single Source of Truth (SSOT)",
        description="Every piece of data should have a single, authoritative source",
        responsibilities=[
            "Maintain one authoritative source for each data element",
            "Eliminate data duplication across systems",
            "Ensure consistency through centralized data management",
            "Prevent conflicting information sources",
        ],
        guidelines=[
            "Each configuration value should have one source",
            "Status information should come from one system",
            "Constants should be defined in one location",
            "Use repositories or services as SSOT for data",
        ],
        examples=[
            "Centralized configuration files",
            "Single status.json per agent",
            "Unified message repository",
            "Consolidated contract definitions",
        ],
        validation_rules=[
            "No duplicate constant definitions",
            "Configuration must come from single source",
            "Status updates must go through SSOT",
            "Data synchronization must maintain SSOT",
        ],
    )


def get_dry_guidance() -> ArchitecturalGuidance:
    """Get Don't Repeat Yourself guidance."""
    return ArchitecturalGuidance(
        principle=ArchitecturalPrinciple.DONT_REPEAT_YOURSELF,
        display_name="Don't Repeat Yourself (DRY)",
        description="Every piece of knowledge must have a single, unambiguous representation",
        responsibilities=[
            "Eliminate code duplication",
            "Extract common logic into reusable functions",
            "Create shared utilities for repeated patterns",
            "Maintain single definition for business rules",
        ],
        guidelines=[
            "Extract duplicated code into functions or classes",
            "Use inheritance or composition to share behavior",
            "Create utility modules for common operations",
            "Parameterize functions to handle variations",
        ],
        examples=[
            "Shared validation logic in utility functions",
            "Base classes for common publisher patterns",
            "Common error handling in base handlers",
            "Reusable message formatting utilities",
        ],
        validation_rules=[
            "No code block should be duplicated more than once",
            "Common logic must be extracted to functions",
            "Similar classes should use inheritance or composition",
            "Repeated patterns must be abstracted",
        ],
    )


def get_kiss_guidance() -> ArchitecturalGuidance:
    """Get Keep It Simple, Stupid guidance."""
    return ArchitecturalGuidance(
        principle=ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID,
        display_name="Keep It Simple, Stupid (KISS)",
        description="Simplicity should be a key goal in design, and unnecessary complexity should be avoided",
        responsibilities=[
            "Prefer simple solutions over complex ones",
            "Avoid over-engineering",
            "Choose straightforward implementations",
            "Maintain code readability and clarity",
        ],
        guidelines=[
            "Use the simplest solution that works",
            "Avoid premature optimization",
            "Prefer explicit code over clever tricks",
            "Keep functions and classes focused and small",
        ],
        examples=[
            "Simple if-else over complex state machines",
            "Direct function calls over elaborate patterns",
            "Clear variable names over abbreviations",
            "Straightforward algorithms over optimized ones",
        ],
        validation_rules=[
            "Functions should be easy to understand",
            "No unnecessary abstractions",
            "Code should be readable without comments",
            "Complexity should be justified by requirements",
        ],
    )


def get_tdd_guidance() -> ArchitecturalGuidance:
    """Get Test-Driven Development guidance."""
    return ArchitecturalGuidance(
        principle=ArchitecturalPrinciple.TEST_DRIVEN_DEVELOPMENT,
        display_name="Test-Driven Development (TDD)",
        description="Write tests before writing implementation code",
        responsibilities=[
            "Write failing tests before implementation",
            "Write minimal code to pass tests",
            "Refactor while maintaining test coverage",
            "Maintain comprehensive test suites",
        ],
        guidelines=[
            "Red-Green-Refactor cycle: Write test, make it pass, refactor",
            "Tests should cover happy paths and edge cases",
            "Mock external dependencies in tests",
            "Maintain test coverage above 85%",
        ],
        examples=[
            "Unit tests for all service methods",
            "Integration tests for repository operations",
            "Mock external APIs in handler tests",
            "Test fixtures for common test data",
        ],
        validation_rules=[
            "All new features must have tests",
            "Test coverage must be above 85%",
            "Tests must run before commits",
            "Failing tests must be fixed before new features",
        ],
    )