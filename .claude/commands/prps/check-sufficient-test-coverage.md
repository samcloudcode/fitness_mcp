# Check Sufficient Test Coverage

Analyze test coverage for critical functionality and implementation correctness.

## Feature/Code to Review: $ARGUMENTS

## Analysis Process

1. **Identify What Matters**
   - Find core business logic and algorithms
   - Locate complex state transformations
   - Identify critical user workflows
   - Note data validation and error paths

2. **Assess Current Tests**
   - Find existing test files
   - Run coverage report
   - Focus on critical paths, not percentages
   - Check test quality, not just quantity

3. **Run Coverage Analysis**
   ```bash
   # Python: uv run pytest --cov=module --cov-report=term-missing
   ```

4. **Identify Gaps**
   - List untested business logic
   - Note missing error handling tests
   - Find uncovered edge cases that matter

5. **Prioritize Test Additions**
   - Must Have: Tests that prevent production issues
   - Should Have: Tests for common failures
   - Nice to Have: Tests for rare edge cases

6. **Report Assessment**
   - State if coverage is sufficient for deployment
   - List critical tests that must be added
   - Provide confidence score

## Philosophy

**Test what matters**:
- Core business logic
- Complex algorithms
- Data transformations
- Critical failure paths

**Skip tests for**:
- Getters/setters
- Framework boilerplate
- Trivial configuration
- One-line functions

## Target Coverage

- Critical paths: 80-90%
- Business logic: 70-80%
- Utilities: 50-60%
- UI/presentation: 30-40%

Note: Focus on testing behavior, not implementation. Follow the testing pyramid - many unit tests, fewer integration tests, minimal E2E tests.