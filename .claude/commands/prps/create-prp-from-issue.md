# Create PRP from GitHub Issue

## GitHub Issue: $ARGUMENTS

Generate a complete PRP for feature implementation based on a GitHub issue with thorough research. Ensure context is passed to the AI agent to enable self-validation and iterative refinement. Fetch and analyze the GitHub issue first to understand requirements, acceptance criteria, and any linked context.

The AI agent only gets the context you are appending to the PRP and training data. Assume the AI agent has access to the codebase and the same knowledge cutoff as you, so its important that your research findings are included or referenced in the PRP. The Agent has Websearch capabilities, so pass urls to documentation and examples.

## Issue Analysis Process

1. **Fetch GitHub Issue**
   - Use `gh issue view <issue-number>` to get issue details
   - Extract title, description, and labels
   - Check comments for additional context/clarifications
   - Identify linked PRs or related issues
   - Note any acceptance criteria or definition of done

2. **Extract Requirements**
   - Core functionality needed
   - User stories or use cases
   - Performance requirements
   - Security considerations
   - Breaking changes to consider

## Research Process

1. **Codebase Analysis**
   - Search for similar features/patterns in the codebase
   - Identify files to reference in PRP
   - Note existing conventions to follow
   - Check test patterns for validation approach
   - Review any code mentioned in the issue

2. **External Research**
   - Search for similar features/patterns online
   - Library documentation (include specific URLs)
   - Implementation examples (GitHub/StackOverflow/blogs)
   - Best practices and common pitfalls
   - Check issue comments for referenced solutions

3. **User Clarification** (if needed)
   - Ambiguous requirements from issue?
   - Missing acceptance criteria?
   - Integration requirements unclear?

## PRP Generation

Using PRPs/templates/prp_base.md as template:

### Issue Context Section (New)
- **Issue Number**: #<number>
- **Issue Title**: <title>
- **Priority/Labels**: <labels>
- **Reporter**: <username>
- **Key Requirements**: Bullet list from issue
- **Acceptance Criteria**: From issue or inferred

### Critical Context to Include and pass to the AI agent as part of the PRP
- **Documentation**: URLs with specific sections
- **Code Examples**: Real snippets from codebase
- **Gotchas**: Library quirks, version issues
- **Patterns**: Existing approaches to follow
- **Issue Context**: Link to issue and key discussion points

### Implementation Blueprint
- Start with pseudocode showing approach
- Reference real files for patterns
- Include error handling strategy
- List tasks to be completed to fulfill the PRP in the order they should be completed
- Map tasks to acceptance criteria from issue

### Validation Gates (Must be Executable) eg for python
```bash
# Syntax/Style
ruff check --fix && mypy .

# Unit Tests
uv run pytest tests/ -v

# Issue-specific validation
# Add specific tests for acceptance criteria
```

### Issue Closure Checklist
- [ ] All acceptance criteria met
- [ ] Tests added for new functionality
- [ ] Documentation updated if needed
- [ ] Breaking changes documented
- [ ] Ready for PR review

*** CRITICAL AFTER YOU ARE DONE RESEARCHING AND EXPLORING THE CODEBASE BEFORE YOU START WRITING THE PRP ***

*** ULTRATHINK ABOUT THE PRP AND PLAN YOUR APPROACH THEN START WRITING THE PRP ***

## Output
Save as: `PRPs/issue-{issue-number}-{feature-name}.md`

## Quality Checklist
- [ ] Issue requirements fully captured
- [ ] All necessary context included
- [ ] Validation gates are executable by AI
- [ ] References existing patterns
- [ ] Clear implementation path
- [ ] Error handling documented
- [ ] Acceptance criteria mappable to tests

Score the PRP on a scale of 1-10 (confidence level to succeed in one-pass implementation using claude codes)

Remember: The goal is one-pass implementation success through comprehensive context extracted from the GitHub issue and research.