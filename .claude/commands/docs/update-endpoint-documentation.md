# Update API Endpoint Documentation

Enhance FastAPI endpoints with comprehensive Swagger/OpenAPI documentation by analyzing the complete request flow and adding detailed docstrings.

## Target Endpoint: $ARGUMENTS

## Documentation Process

1. **Identify Target Endpoints**
   - If endpoint specified: Focus on the provided endpoint path
   - If no argument: Check recent git changes for modified endpoints
   - Identify all related endpoints that share similar functionality

2. **Analyze Endpoint Implementation**
   - Trace the complete request flow from endpoint to response
   - Map all function calls and data transformations
   - Identify all dependencies and external services
   - Document database queries and data sources
   - Track business logic and validation rules

3. **Document Components**
   - **Request Models**: Document all fields, types, and constraints
   - **Response Models**: Document structure and field meanings
   - **Query Parameters**: Purpose, defaults, and valid ranges
   - **Path Parameters**: Format requirements and validation
   - **Headers**: Required/optional headers and their purpose
   - **Status Codes**: All possible responses and when they occur

4. **Create Comprehensive Docstring**
   ```python
   """
   Brief endpoint description.

   Detailed explanation of endpoint functionality, business logic,
   and data flow. Explain the complete process from request to response.

   **Data Sources:**
   - Database tables/collections accessed
   - External APIs called
   - Cache layers used

   **Business Logic:**
   - Validation rules applied
   - Calculations performed
   - Transformations applied

   **Request Body** (if applicable):
   - field_name: Description, valid values, business meaning

   **Query Parameters:**
   - param_name: Purpose, defaults, constraints

   **Response Interpretation:**
   - How to interpret response fields
   - Relationship between fields
   - Special cases or edge conditions

   **Examples:**
   ```json
   {
     "request": { ... },
     "response": { ... }
   }
   ```

   **Error Scenarios:**
   - 400: Invalid input (specify conditions)
   - 401: Authentication required
   - 403: Insufficient permissions
   - 404: Resource not found
   - 500: Server error conditions
   """
   ```

5. **Implementation Checklist**
   - [ ] Traced complete request flow
   - [ ] Documented all input parameters
   - [ ] Explained all response fields
   - [ ] Added practical examples
   - [ ] Listed all status codes
   - [ ] Documented data sources
   - [ ] Explained business logic
   - [ ] Added field constraints
   - [ ] Included error scenarios

6. **Validation**
   - Ensure docstring follows FastAPI/Swagger format
   - Verify all parameters are documented
   - Check examples are valid and complete
   - Confirm business logic is accurately described
   - Test that Swagger UI renders correctly

## Execution Notes

- Follow existing documentation patterns in the codebase
- Include real-world examples from test data
- Document edge cases and error conditions
- Ensure consistency across related endpoints