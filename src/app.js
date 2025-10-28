// Test application for MCP workflow-gated PR
console.log('🚀 Testing Git Workflow MCP Server!');

function calculateSum(numbers) {
    return numbers.reduce((sum, num) => sum + num, 0);
}

function formatMessage(name, count) {
    return `Hello ${name}! You have ${count} items.`;
}

// Test the functions
const testNumbers = [1, 2, 3, 4, 5];
const sum = calculateSum(testNumbers);
console.log(`Sum of [${testNumbers.join(', ')}] = ${sum}`);

const message = formatMessage('Developer', 42);
console.log(message);

module.exports = {
    calculateSum,
    formatMessage
};