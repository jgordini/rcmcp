# MCP Server Evaluation Suite

This evaluation suite tests the UAB Research Computing Documentation MCP server's ability to answer complex, realistic questions about UAB's research computing resources.

## Overview

The evaluation consists of 10 questions that:
- Require multiple tool calls to answer
- Test deep exploration of documentation
- Cover diverse topics (SLURM, storage, software, access, GPU computing)
- Have single, verifiable answers
- Are independent (don't depend on previous questions)
- Use only read-only operations

## Questions Coverage

1. **SLURM Job Limits**: Express partition time limits
2. **Job Monitoring**: SLURM queue commands
3. **Python Environments**: Package management best practices
4. **Storage Quotas**: Default individual allocations
5. **Data Transfer**: Large dataset transfer tools
6. **Authentication**: Portal access requirements
7. **Compute Rules**: Proper job submission practices
8. **GPU Computing**: Ampere GPU partition names
9. **Account Management**: Leaving UAB procedures
10. **Portal Access**: Open OnDemand URL

## Running Evaluations

To run the evaluation suite, you'll need an MCP evaluation harness that:

1. Connects to the MCP server (stdio or HTTP)
2. Iterates through each question in `evaluations.xml`
3. Invokes the server's tools to find answers
4. Compares responses to expected answers
5. Reports success/failure for each question

### Expected Performance

**Target Metrics:**
- Success Rate: >80% (8+ out of 10 correct)
- Average Tool Calls: 2-4 per question
- Average Response Time: <5 seconds per question
- Error Rate: <10%

## Evaluation Process

For each question, a good AI agent should:

1. **Understand the Question**: Parse what information is needed
2. **Search**: Use `search_documentation` to find relevant pages
3. **Retrieve**: Use `get_documentation_page` to get full content
4. **Extract**: Parse the retrieved content for the answer
5. **Verify**: Ensure the answer matches the expected format

## Answer Format

Answers are designed to be:
- **Short**: Single words or phrases
- **Specific**: Exact values, names, or terms
- **Stable**: Won't change over time
- **Verifiable**: Can be checked via string matching

## Updating Evaluations

When updating the evaluation suite:

1. Ensure questions remain:
   - Independent
   - Read-only
   - Verifiable
   - Stable over time

2. Test each question manually first
3. Verify answers are correct and complete
4. Update this README with any changes

## Integration with CI/CD

To integrate into continuous integration:

```bash
# Example workflow
1. Deploy MCP server
2. Run evaluation harness
3. Check success rate >= 80%
4. Report results
```

## Troubleshooting

If evaluation success rate drops:

1. **Check Documentation**: Has UAB RC docs structure changed?
2. **Test Tools**: Are all tools functioning correctly?
3. **Verify Answers**: Are answers still accurate?
4. **Review Logs**: Check for API rate limits or errors

## Contributing

To add new evaluation questions:

1. Follow the MCP guide Phase 4 process
2. Test with actual server
3. Verify answer is obtainable
4. Submit PR with updated `evaluations.xml`