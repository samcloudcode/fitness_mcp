# Add Observability with Logfire

Add or enhance Logfire observability to Python codebases for comprehensive monitoring and debugging.

## Execution Mode: $ARGUMENTS

Choose execution mode:
- `initial` - Add Logfire to a project that doesn't have it
- `feature` - Add observability to new/recent features
- `review` - Audit and enhance existing Logfire implementation

## Execution Process

1. **Assess Current State**
   - Check if Logfire is already configured
   - Identify existing observability patterns
   - Review package dependencies (pyproject.toml, requirements.txt)
   - Understand the application architecture (FastAPI, SQLAlchemy, LLM integrations)
   - Locate main entry points and configuration files

2. **ULTRATHINK**
   - Analyze the codebase structure and patterns
   - Identify critical workflows needing observability
   - Plan instrumentation strategy based on execution mode
   - Use TodoWrite to break down implementation into manageable steps

3. **Execute Based on Mode**

   ### Mode: Initial Setup
   - Install Logfire dependency (only if required): `uv add logfire` or `uv add 'logfire[fastapi]'`
   - Create configuration at application entrypoint
   - Set up base instrumentation for frameworks (FastAPI, SQLAlchemy)
   - Add spans to critical workflows
   - Implement structured logging with Pydantic models
   - Configure auto-tracing for key modules

   ### Mode: Feature Observability
   - Review recent changes (git diff, new files)
   - Identify new endpoints, services, or workflows
   - Add spans for end-to-end operations
   - Implement request/response logging
   - Add error handling with exception recording
   - Ensure consistent naming patterns

   ### Mode: Review & Enhancement
   - Audit configuration parameters
   - Check span naming for low cardinality
   - Verify structured logging usage
   - Review exception handling patterns
   - Validate framework integrations
   - Optimize auto-tracing settings

4. **Implementation Guidelines**

   ### Configuration Setup

   Check the codebase and git for relevant parameters:

   Example:

   ```python
   import logfire
   from logfire import ConsoleOptions, CodeSource
   
   logfire.configure(
       environment='production',  # or 'development', 'staging'
       console=ConsoleOptions(min_log_level='info'),
       min_level='info',
       distributed_tracing=False,
       code_source=CodeSource(
           repository='github.com/org/repo',
           revision='main',
           root_path='.'
       ),
   )
   ```

   ### Span Patterns
   ```python
   # End-to-end workflow with nested spans
   with logfire.span('process order {order_id}', order_id=order.id):
       with logfire.span('validate items'):
           # validation logic
       with logfire.span('charge payment'):
           # payment logic
       logfire.info('order processed', order=OrderModel(...))
   ```

   ### FastAPI Integration
   ```python
   # Basic setup (do once at app initialization)
   import logfire
   from fastapi import FastAPI
   
   app = FastAPI()
   logfire.configure()
   logfire.instrument_fastapi(app)  # Automatic instrumentation
   
   # Optional: Enable extra spans for detailed tracking
   # logfire.instrument_fastapi(app, extra_spans=True)
   
   # Manual span for additional context (if needed)
   @router.post('/items', response_model=ItemOut)
   async def create_item(payload: ItemIn) -> ItemOut:
       # FastAPI instrumentation automatically logs request/response
       # Add manual logging only for business logic
       result = await service.create_item(payload)
       logfire.info('item created', item=result, user_id=current_user.id)
       return result
   ```

   ### Exception Handling
   ```python
   try:
       result = await risky_operation()
   except Exception as err:
       logfire.exception('operation failed')
       # or within a span: span.record_exception(err)
       raise
   ```

   ### Auto-Tracing
   ```python
   # Call BEFORE importing modules to trace
   logfire.install_auto_tracing(
       modules=['app.services', 'app.repositories'],
       min_duration=0.01
   )
   ```

5. **Validate**
   - Test application startup with Logfire configured
   - Verify logs appear in console/dashboard
   - Check span hierarchy and naming
   - Validate structured data capture
   - Test error scenarios for exception recording
   - Review performance impact

6. **Complete**
   - All critical paths have observability
   - Configuration follows best practices
   - Consistent span naming patterns
   - Structured logging for key data
   - Framework integrations working
   - Documentation updated if needed

## Key Principles

### Span Naming
- Use low-cardinality templates: `'process {entity_type}'` not `'process order-12345'`
- Pass specifics as attributes: `order_id=12345`
- Consistent verb patterns: `fetch`, `create`, `update`, `delete`, `process`

### Structured Logging
- Log Pydantic models directly: `logfire.info('created', user=UserModel(...))`
- Exclude sensitive fields: Use Pydantic field exclusion for PII/secrets
- Log at decision points and state changes

### Performance Considerations
- Set appropriate `min_duration` for auto-tracing
- Use `@logfire.no_auto_trace` for trivial helpers
- Avoid logging large payloads without filtering
- Consider sampling for high-volume endpoints

### Error Handling
- Always record exceptions in spans
- Include context in error messages
- Use appropriate log levels (error, warning, info)
- Preserve original stack traces

## Validation Commands

Based on project type, run:
- `uv run pytest` - Ensure tests pass with Logfire
- `uv run python -m app.main` - Verify startup and configuration
- `curl localhost:8000/health` - Check instrumented endpoints
- Review Logfire dashboard for proper span hierarchy

## Common Patterns to Fix

- Missing spans around database transactions
- Unstructured string logging instead of models
- High-cardinality span names with IDs
- Missing exception recording
- Duplicate configuration calls
- Auto-tracing imported before configuration
- Missing framework integrations (FastAPI, SQLAlchemy)
- Logging sensitive data without filtering
- Manual request/response logging when FastAPI instrumentation handles it automatically
- Not using `instrument_fastapi()` and manually wrapping every endpoint
- Mutating request attributes in `request_attributes_mapper` function

## Best Practices Summary

### FastAPI-Specific
- Use `logfire.instrument_fastapi(app)` for automatic request/response logging
- Enable `extra_spans=True` for detailed timing analysis during development
- Let instrumentation handle request/response; add manual logs only for business logic
- Use `request_attributes_mapper` to customize logged attributes without mutation

### Pydantic Integration
- Enable `pydantic_plugin` with `record="all"` for validation tracking
- Pass Pydantic models directly to logging functions for structured data
- Exclude sensitive fields using Pydantic's field configuration

### Performance
- Install with extras: `uv add 'logfire[fastapi]'` for optimized dependencies
- Set appropriate `min_duration` for auto-tracing (0.01s is a good default)
- Use SQL queries on Logfire dashboard for real-time metrics

Note: Always review existing patterns before adding new instrumentation to maintain consistency.