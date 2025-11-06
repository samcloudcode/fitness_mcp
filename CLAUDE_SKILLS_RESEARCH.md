# Claude Skills - Deep Dive Research
*Prioritizing Official Anthropic Documentation*

**Research Date:** November 2025
**Sources:** Anthropic official documentation, engineering blog, GitHub repository

---

## Table of Contents
1. [What Are Claude Skills?](#what-are-claude-skills)
2. [Core Design Pattern & Architecture](#core-design-pattern--architecture)
3. [Skill Structure & Requirements](#skill-structure--requirements)
4. [Best Practices](#best-practices)
5. [Creation Workflow](#creation-workflow)
6. [Availability & Platforms](#availability--platforms)
7. [Example Skills](#example-skills)
8. [Troubleshooting](#troubleshooting)
9. [Official Resources](#official-resources)

---

## What Are Claude Skills?

Claude Skills are **modular capabilities that package expertise into discoverable capabilities** through organized folders containing instructions, scripts, and resources that Claude can dynamically load when performing specialized tasks.

### Key Characteristics

- **Model-Invoked**: Claude autonomously decides when to use skills based on your request and the skill's description—unlike slash commands that require explicit user activation
- **Progressive Disclosure**: Load minimal information on-demand to optimize context window usage
- **Composable**: Multiple skills work together automatically
- **Portable**: Function consistently across Claude apps, Claude Code, and APIs
- **Powerful**: Include executable code for reliable task execution

### Official Definition
> "Skills are folders containing instructions, scripts, and resources that Claude dynamically loads to enhance performance on specialized tasks." — Anthropic Skills Repository

---

## Core Design Pattern & Architecture

### Progressive Disclosure Architecture

**Progressive disclosure is the core design principle** that makes Agent Skills flexible and scalable. The system uses three disclosure levels:

1. **Metadata Level**: Skill name and description pre-loaded into system prompt
2. **Full Content Level**: Complete SKILL.md file loaded when relevant
3. **Granular Level**: Additional bundled files loaded dynamically as needed

**Context Window Optimization:**
The system avoids loading entire skill definitions upfront. Instead, agents invoke bash tools to read `SKILL.md` content only when triggered by user intent, keeping token usage minimal.

> "Progressive disclosure is the core design principle that makes Agent Skills flexible and scalable. Like a well-organized manual, skills let Claude load information only as needed." — Anthropic Engineering Blog

### Architecture Components

**File Structure:**
- Root: `SKILL.md` with YAML frontmatter (required `name` and `description` fields)
- Supporting files: Referenced from SKILL.md, loaded on-demand
- Code scripts: Executable tools or documentation resources

**Context Window as Public Good:**
> "The context window is a public good. Your Skill shares the context window with everything else Claude needs to know." — Anthropic Best Practices

This principle drives all design decisions around Skills:
- Keep SKILL.md body under 500 lines
- Assume Claude has broad knowledge; only add necessary context
- Use progressive disclosure by splitting content into separate files
- Remember that only metadata pre-loads; detailed files load on-demand

---

## Skill Structure & Requirements

### Required: SKILL.md File

Every skill must have a `SKILL.md` file with:

#### YAML Frontmatter (Mandatory)

```yaml
---
name: skill-name
description: Brief explanation of functionality and usage triggers
---
```

**Field Requirements:**
- **`name`**:
  - Max 64 characters
  - Lowercase letters, numbers, hyphens only
  - Use gerund form (verb + "-ing") like "processing-pdfs" or "analyzing-spreadsheets"

- **`description`**:
  - Max 1024 characters
  - Non-empty, no XML tags
  - **Critical for skill discovery**: Claude uses this to decide whether to trigger the skill
  - Write in third person to avoid discovery problems
  - Include both capabilities and usage triggers

**Description Examples:**

✅ **Good**: "Extract text and tables from PDFs. Use when user requests PDF analysis or data extraction from documents."

❌ **Bad**: "Helps with documents" (too vague)

#### Markdown Content

After the frontmatter, include markdown instructions that Claude will follow when the skill activates. This should:
- Provide clear, concise guidance
- Reference supporting files when needed
- Include examples and workflows
- Stay under 500 lines total

### Optional: Supporting Files

Skills can include additional files:
- Reference guides (FORMS.md, REFERENCE.md, EXAMPLES.md)
- Templates for output generation
- Scripts (Python, JavaScript, etc.) for deterministic execution
- Example files showing desired outputs

**Progressive Disclosure Pattern**: Structure Skills like tables of contents—SKILL.md provides overview and navigation; detailed files load only when needed.

**One-Level-Deep References**: Keep all references one level from SKILL.md to ensure Claude reads complete files. Avoid nested references that might cause partial reads.

### Storage Locations

1. **Personal Skills** (`~/.claude/skills/`):
   - Available across all projects
   - Ideal for individual workflows and experimental features
   - Private to your account

2. **Project Skills** (`.claude/skills/`):
   - Shared with teams via git
   - Suited for team conventions and project-specific expertise
   - Committed to version control

3. **Plugin Skills**:
   - Bundled with installed plugins
   - Function identically to personal and project skills
   - Distributed via anthropics/skills marketplace

---

## Best Practices

### 1. Core Design Principles

#### Conciseness
- Keep SKILL.md body under 500 lines
- Assume Claude has broad knowledge; only add necessary context
- Use progressive disclosure by splitting content into separate files

#### Appropriate Freedom Levels
Match specificity to task fragility:
- **High Freedom** (text instructions): For flexible tasks
- **Medium Freedom** (pseudocode): For patterns with acceptable variation
- **Low Freedom** (specific scripts): For error-prone operations requiring strict sequences

#### Multi-Model Testing
Evaluate Skills across:
- **Claude Haiku**: Faster, needs more guidance
- **Sonnet**: Balanced
- **Opus**: Powerful reasoning

> "Skills act as additions to models, so effectiveness depends on the underlying model, and you should test your Skill with all the models you plan to use it with." — Anthropic Best Practices

### 2. Information Architecture

#### Progressive Disclosure Pattern
Structure Skills like tables of contents—SKILL.md provides overview and navigation; detailed files (FORMS.md, REFERENCE.md, EXAMPLES.md) load only when needed.

#### One-Level-Deep References
Keep all references one level from SKILL.md to ensure Claude reads complete files. Avoid nested references that might cause partial reads.

#### Long Reference Organization
Include table of contents for files exceeding 100 lines, enabling Claude to preview scope and navigate efficiently.

#### Domain-Based Organization
For multi-domain Skills, organize reference files by domain (finance.md, sales.md, product.md) so Claude loads only relevant context.

### 3. Workflow and Feedback Design

#### Complex Task Workflows
Break operations into clear sequential steps with copyable checklists that Claude can track progress against.

#### Validation Loops
Implement feedback patterns where Claude:
1. Runs validator
2. Receives errors
3. Fixes issues
4. Repeats

This significantly improves output quality.

#### Template Patterns
- **Strict templates**: For output requiring consistency (APIs, data formats)
- **Flexible templates**: For context-dependent tasks

#### Examples as Specification
Use concrete input/output pairs to demonstrate desired style and detail levels more effectively than descriptions alone.

### 4. Code and Script Best Practices

#### Error Handling
Scripts should solve problems rather than defer to Claude. Handle:
- Missing files
- Permission errors
- Invalid inputs

#### Justified Constants
Document why parameter values exist:
```python
REQUEST_TIMEOUT = 30  # HTTP requests typically complete within 30 seconds
```
This prevents "voodoo constants."

#### Utility Scripts Preferred
Pre-made scripts are:
- More reliable than generated code
- Token-saving
- Consistent across uses

**Execute scripts rather than loading their code into context.**

#### Visual Analysis
Convert PDFs to images; Claude's vision capabilities help understand layouts and identify fields.

#### Verifiable Intermediates
For complex operations, have Claude create structured plan files (like JSON) that validation scripts verify before execution proceeds.

#### Dependency Declaration
List required packages and verify availability in the code execution environment documentation.

### 5. Content and Terminology

#### Time-Sensitive Information
❌ Avoid: "If this is before August 2025, use X."
✅ Instead: Document current methods and deprecated patterns in collapsible sections.

#### Consistent Terminology
Choose single terms and maintain them throughout:
- Always "API endpoint," not mixing "URL," "route," "path"

#### Avoid Excessive Choices
Provide defaults with escape hatches rather than listing many valid approaches, reducing cognitive load.

### 6. Testing and Iteration

#### Evaluation-Driven Development
Create test scenarios before extensive documentation:
1. Identify gaps from Claude failures
2. Build three test scenarios
3. Measure baseline performance
4. Write minimal instructions
5. Iterate based on results

> "Start with Evaluation: Identify specific gaps in your agents' capabilities by running them on representative tasks and observing where they struggle." — Anthropic Engineering Blog

#### Collaborative Development
Use one Claude instance ("Claude A") to create Skills while testing with another instance ("Claude B"):
- Claude A designs and refines instructions
- Claude B tests on real tasks and reveals gaps
- Use observations to iteratively improve the Skill

> "Iterate with Claude: Collaborate with the model to capture successful patterns into reusable context and code." — Anthropic Engineering Blog

#### Usage Observation
Monitor how Claude navigates Skills for unexpected exploration paths, missed connections, ignored content—then iterate based on actual behavior rather than assumptions.

> "Think from Claude's Perspective: Monitor real-world usage patterns; prioritize skill `name` and `description` quality for proper triggering." — Anthropic Engineering Blog

### 7. Security and Technical Considerations

#### Security Best Practices
> "We recommend installing skills only from trusted sources. When installing a skill from a less-trusted source, thoroughly audit it before use." — Anthropic Engineering Blog

Pay particular attention to:
- Code dependencies
- External network connections
- File system access

#### Path Format
Always use forward slashes (scripts/helper.py, not scripts\helper.py) for cross-platform compatibility.

#### MCP Tool References
Use fully qualified names like "ServerName:tool_name" to avoid "tool not found" errors with multiple MCP servers.

#### No Assumptions About Tools
Explicitly show installation steps rather than assuming packages are available.

#### Avoid Windows-Style Paths
Unix-style paths work across all platforms; Windows-style paths fail on Unix systems.

### 8. Pre-Launch Checklist

Before deploying a skill, verify:

- [ ] Description is specific with usage triggers
- [ ] SKILL.md under 500 lines
- [ ] Progressive disclosure properly implemented
- [ ] Examples are concrete
- [ ] References one level deep
- [ ] No time-sensitive information
- [ ] Terminology consistent throughout
- [ ] Scripts have explicit error handling
- [ ] All required packages documented
- [ ] Tested with Haiku, Sonnet, and Opus
- [ ] Real-world usage scenarios verified
- [ ] No Windows-style file paths
- [ ] Security audit completed (if from external sources)

---

## Creation Workflow

### Option 1: Using the skill-creator Skill (Claude.ai)

The built-in "skill-creator" skill provides interactive guidance:
1. Claude asks about your workflow
2. Generates the folder structure
3. Formats the SKILL.md file
4. Bundles the resources you need

### Option 2: Manual Creation

1. **Create Directory Structure**:
   ```bash
   mkdir -p ~/.claude/skills/my-skill-name
   # or
   mkdir -p .claude/skills/my-skill-name  # for project-specific
   ```

2. **Create SKILL.md**:
   ```markdown
   ---
   name: my-skill-name
   description: Detailed description with usage triggers
   ---

   # Skill Instructions

   Your markdown content here...
   ```

3. **Add Supporting Files** (optional):
   ```
   my-skill-name/
   ├── SKILL.md
   ├── EXAMPLES.md
   ├── REFERENCE.md
   └── scripts/
       └── helper.py
   ```

4. **Test the Skill**:
   - Ask questions matching your description
   - Verify Skills activate for matching requests
   - Test with multiple models (Haiku, Sonnet, Opus)

5. **Share** (optional):
   - Via plugins (recommended)
   - Via project repositories (`.claude/skills/`)
   - Package as ZIP for manual upload (Claude.ai)

### Testing Strategy

> "Pay attention to how Claude actually uses skills in practice and iterate based on observations rather than assumptions." — Anthropic Best Practices

**Recommended approach:**
1. Start with simple test cases
2. Observe Claude's skill selection behavior
3. Monitor token usage and loading patterns
4. Iterate on description for better triggering
5. Test edge cases and failure modes

---

## Availability & Platforms

### Claude.ai

**Available to:** Pro, Max, Team, and Enterprise users

**Features:**
- Automatic skill invocation based on task relevance
- Built-in skills for Office documents (Excel, Word, PowerPoint, PDF)
- Upload custom skills as ZIP files
- Toggle skills on/off individually

**Setup:**
1. Navigate to Settings > Capabilities
2. Ensure "Code execution and file creation" is enabled
3. Toggle individual skills on/off
4. Click "Upload skill" to add custom skills as ZIP files

> "Claude will automatically use these tools when relevant. You don't need to explicitly invoke them." — Anthropic Support

### Claude Code

**Available to:** All Claude Code users

**Installation:**
- Via anthropics/skills marketplace
- Manually through `~/.claude/skills` (personal)
- Project-specific via `.claude/skills` (shared)

Skills load automatically when Claude Code starts and updates take effect after restart.

### Claude Developer Platform

**API Access:** The `/v1/skills` endpoint enables programmatic management

**Requirements:**
- Skills require the Code Execution Tool beta
- Developers get programmatic control over custom skill versioning and management

**Features:**
- Add Agent Skills to Messages API requests
- Version control for skills
- Programmatic deployment

---

## Example Skills

From the [anthropics/skills repository](https://github.com/anthropics/skills) (15.6k stars):

### Open Source Skills (Apache 2.0)

**Creative & Design:**
- **Algorithmic art**: Generation using p5.js
- **Canvas design**: Visual design (.png and .pdf)
- **Animated GIFs**: Optimized for Slack

**Development & Technical:**
- **HTML artifacts**: Complex builds with React and Tailwind CSS
- **MCP server creation**: Guidance for building MCP servers
- **Web testing**: Via Playwright automation

**Enterprise & Communication:**
- **Brand guidelines**: Application tools for consistency
- **Internal communications**: Templates and best practices
- **Professional themes**: Styling system

**Meta Skills:**
- **Creating skills**: Guidance for building new skills
- **Template starter**: Base project structure

### Source-Available Document Skills

Advanced capabilities for:
- **Word**: Tracked changes, templates, styling
- **PDF**: Form handling, extraction, generation
- **PowerPoint**: Slide creation, themes, layouts
- **Excel**: Formulas, data visualization, complex spreadsheets

---

## Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Skills not activating** | • Verify description specificity<br>• Check YAML syntax validity<br>• Ensure code execution enabled<br>• Try explicit requests matching description |
| **Skills section invisible** | Enable code execution in Settings > Capabilities |
| **File path errors** | • Confirm correct location<br>• Use forward slashes in paths<br>• Avoid Windows-style paths |
| **Upload fails** | • Check ZIP size<br>• Verify folder naming<br>• Ensure SKILL.md file present |
| **Skills greyed out** | Code execution may be disabled at organization level (Enterprise) |
| **Conflicting Skills** | Use distinct trigger terms in descriptions to help Claude differentiate |
| **Claude won't use skill** | • Check if toggled on<br>• Verify description clarity<br>• Test with explicit requests |

### Debugging Tips

1. **Check YAML Validity**: Ensure frontmatter is properly formatted
2. **Test Description**: Ask Claude directly if a task matches your skill description
3. **Monitor Context**: Use verbose mode to see which skills are being loaded
4. **Verify Permissions**: Ensure code execution and file access are enabled
5. **Review Logs**: Check for error messages during skill loading

---

## Official Resources

### Primary Documentation
- **Claude Code Skills Docs**: https://code.claude.com/docs/en/skills
- **Engineering Deep Dive**: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Best Practices**: https://anthropic.mintlify.app/en/docs/agents-and-tools/agent-skills/best-practices
- **Skills Announcement**: https://claude.com/blog/skills

### Support & Help
- **Using Skills in Claude**: https://support.claude.com/en/articles/12512180-using-skills-in-claude
- **What are Skills?**: https://support.claude.com/en/articles/12512176-what-are-skills
- **Claude Code Best Practices**: https://www.anthropic.com/engineering/claude-code-best-practices

### Community & Examples
- **Official Skills Repository**: https://github.com/anthropics/skills (15.6k stars)
- **Community Collections**: https://github.com/travisvn/awesome-claude-skills

### API & Developer Platform
- **Skills API Endpoint**: `/v1/skills`
- **Code Execution Tool**: Required beta feature for API skills
- **Messages API**: Skills can be added to requests

---

## Key Takeaways

### Design Philosophy

1. **Progressive Disclosure First**: Load only what's needed when needed
2. **Context Window as Shared Resource**: Keep skills concise and focused
3. **Evaluation-Driven Development**: Test before building extensive documentation
4. **Multi-Model Compatibility**: Test across Haiku, Sonnet, and Opus

### Success Factors

1. **Clear, Specific Descriptions**: Critical for Claude's skill discovery
2. **Focused Scope**: One skill = one capability
3. **Concrete Examples**: Better than lengthy explanations
4. **Executable Scripts**: More reliable than generated code
5. **Iterative Refinement**: Monitor usage and adapt

### Common Mistakes to Avoid

1. ❌ Vague descriptions that don't specify usage triggers
2. ❌ Monolithic skills trying to do everything
3. ❌ Loading entire skill content upfront instead of progressive disclosure
4. ❌ Assuming tool availability without documentation
5. ❌ Skipping multi-model testing
6. ❌ Installing skills from untrusted sources

### Future Development

According to Anthropic's announcement, future development targets:
- Simplified skill creation workflows
- Enterprise-wide deployment capabilities
- Enhanced team-wide skill distribution

---

## Integration with Claude Code Workflows

### Recommended Workflows (per Anthropic)

**1. Explore, Plan, Code, Commit**
- Research before implementation
- Use extended thinking modes ("think", "ultrathink")
- Confirm plan before coding
- Skills provide context during exploration

**2. Test-Driven Development**
- Write tests first
- Skills provide testing patterns and utilities
- Iterate implementation to pass tests

**3. Visual Iteration**
- Provide screenshots/mocks
- Skills guide design implementation
- Multiple rounds for refinement

### Skills in the Workflow

Skills complement these workflows by:
- Providing domain-specific expertise during exploration
- Offering testing utilities for TDD
- Supplying design system guidelines for visual work
- Loading relevant context only when needed

---

## Conclusion

Claude Skills represent a powerful paradigm for extending AI capabilities through **progressive disclosure** and **composable expertise**. By following Anthropic's best practices—particularly around clear descriptions, focused scope, and evaluation-driven development—you can create skills that significantly enhance Claude's effectiveness at specialized tasks while maintaining efficient context window usage.

The key insight is treating the context window as a shared resource and loading information progressively as needed, rather than front-loading all possible context. This architectural approach enables skills to scale effectively across diverse use cases while maintaining performance.

---

*This document synthesizes official Anthropic documentation, engineering blog posts, support articles, and the public skills repository. All direct quotes are attributed to their sources.*

*Last Updated: November 2025*
