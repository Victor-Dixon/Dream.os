<?php
/*
Template Name: Strategy Marketplace
*/

get_header(); ?>

<section class="strategy-marketplace py-20 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4">
        <div class="text-center mb-16">
            <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                AI Trading Strategy Marketplace
            </h1>
            <p class="text-xl text-gray-600 max-w-3xl mx-auto">
                Our swarm has developed and tested multiple trading algorithms.
                Each strategy is optimized for different market conditions.
            </p>
        </div>

        <!-- Strategy Filter Bar -->
        <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
            <div class="flex flex-wrap gap-4 items-center justify-between">
                <div class="flex gap-4">
                    <select id="risk-filter" class="px-4 py-2 border border-gray-300 rounded-lg">
                        <option value="">All Risk Levels</option>
                        <option value="low">Low Risk</option>
                        <option value="medium">Medium Risk</option>
                        <option value="high">High Risk</option>
                    </select>
                    <select id="sort-by" class="px-4 py-2 border border-gray-300 rounded-lg">
                        <option value="return">Sort by Return</option>
                        <option value="winrate">Sort by Win Rate</option>
                        <option value="name">Sort by Name</option>
                    </select>
                </div>
                <div class="text-sm text-gray-600">
                    <span id="strategy-count">3</span> strategies available
                </div>
            </div>
        </div>

        <!-- Strategy Cards Grid -->
        <div id="strategy-grid" class="grid md:grid-cols-3 gap-8">
            <!-- Strategy cards loaded dynamically -->
        </div>

        <!-- Backtesting Interface Modal -->
        <div id="backtest-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50">
            <div class="flex items-center justify-center min-h-screen p-4">
                <div class="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
                    <div class="p-6 border-b border-gray-200">
                        <div class="flex justify-between items-center">
                            <h2 class="text-2xl font-bold text-gray-900">Strategy Backtesting</h2>
                            <button id="close-modal" class="text-gray-400 hover:text-gray-600">
                                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                    <div id="backtest-content" class="p-6">
                        <!-- Backtesting interface loaded here -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<script>
// Strategy data
const strategies = [
    {
        id: 'conservative',
        name: 'Conservative Growth',
        description: 'Stable, long-term focused strategy with proven risk management.',
        return: 24.7,
        winRate: 89.3,
        maxDrawdown: 12.4,
        sharpeRatio: 1.8,
        risk: 'Low',
        color: 'green'
    },
    {
        id: 'momentum',
        name: 'Momentum Trading',
        description: 'High-conviction trades based on market momentum and volume analysis.',
        return: 42.1,
        winRate: 76.8,
        maxDrawdown: 28.7,
        sharpeRatio: 2.1,
        risk: 'Medium',
        color: 'blue'
    },
    {
        id: 'mean-reversion',
        name: 'Mean Reversion',
        description: 'Statistical arbitrage based on price deviations from moving averages.',
        return: 31.5,
        winRate: 82.4,
        maxDrawdown: 18.9,
        sharpeRatio: 1.9,
        risk: 'Medium',
        color: 'purple'
    }
];

// Render strategy cards
function renderStrategies() {
    const grid = document.getElementById('strategy-grid');
    const riskFilter = document.getElementById('risk-filter').value;
    const sortBy = document.getElementById('sort-by').value;

    let filteredStrategies = strategies;

    // Apply risk filter
    if (riskFilter) {
        filteredStrategies = strategies.filter(s => s.risk.toLowerCase() === riskFilter.toLowerCase());
    }

    // Apply sorting
    filteredStrategies.sort((a, b) => {
        switch (sortBy) {
            case 'return':
                return b.return - a.return;
            case 'winrate':
                return b.winRate - a.winRate;
            case 'name':
                return a.name.localeCompare(b.name);
            default:
                return 0;
        }
    });

    // Update count
    document.getElementById('strategy-count').textContent = filteredStrategies.length;

    // Render cards
    grid.innerHTML = filteredStrategies.map(strategy => `
        <div class="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow duration-300">
            <div class="w-12 h-12 bg-${strategy.color}-100 rounded-lg flex items-center justify-center mb-6">
                <span class="text-${strategy.color}-600 text-2xl">
                    ${strategy.id === 'conservative' ? '📈' :
                      strategy.id === 'momentum' ? '🚀' : '🔄'}
                </span>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-2">${strategy.name}</h3>
            <p class="text-gray-600 mb-6">${strategy.description}</p>

            <div class="space-y-3 mb-6">
                <div class="flex justify-between">
                    <span class="text-gray-600">Total Return</span>
                    <span class="font-bold text-green-600">+${strategy.return}%</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-600">Win Rate</span>
                    <span class="font-bold text-green-600">${strategy.winRate}%</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-600">Max Drawdown</span>
                    <span class="font-bold text-red-600">-${strategy.maxDrawdown}%</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-600">Sharpe Ratio</span>
                    <span class="font-bold text-blue-600">${strategy.sharpeRatio}</span>
                </div>
            </div>

            <div class="flex gap-3">
                <button onclick="openBacktest('${strategy.id}')"
                        class="flex-1 bg-${strategy.color}-600 hover:bg-${strategy.color}-700 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-200">
                    Backtest Strategy
                </button>
                <button onclick="viewDetails('${strategy.id}')"
                        class="px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200">
                    Details
                </button>
            </div>
        </div>
    `).join('');
}

// Backtesting functions
function openBacktest(strategyId) {
    const modal = document.getElementById('backtest-modal');
    const content = document.getElementById('backtest-content');

    const strategy = strategies.find(s => s.id === strategyId);
    if (!strategy) return;

    content.innerHTML = `
        <div class="mb-6">
            <h3 class="text-xl font-bold text-gray-900 mb-2">Backtesting: ${strategy.name}</h3>
            <p class="text-gray-600">${strategy.description}</p>
        </div>

        <div class="grid md:grid-cols-2 gap-6 mb-6">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
                <input type="date" id="backtest-start" class="w-full px-3 py-2 border border-gray-300 rounded-md" value="2023-01-01">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">End Date</label>
                <input type="date" id="backtest-end" class="w-full px-3 py-2 border border-gray-300 rounded-md" value="2024-01-01">
            </div>
        </div>

        <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">Initial Capital ($)</label>
            <input type="number" id="initial-capital" class="w-full px-3 py-2 border border-gray-300 rounded-md" value="10000">
        </div>

        <div class="flex gap-4">
            <button onclick="runBacktest('${strategyId}')"
                    class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-200">
                Run Backtest
            </button>
            <button onclick="closeModal()"
                    class="bg-gray-600 hover:bg-gray-700 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-200">
                Close
            </button>
        </div>

        <div id="backtest-results" class="mt-6 hidden">
            <h4 class="text-lg font-bold text-gray-900 mb-4">Backtest Results</h4>
            <div id="results-content"></div>
        </div>
    `;

    modal.classList.remove('hidden');
}

function closeModal() {
    document.getElementById('backtest-modal').classList.add('hidden');
}

function runBacktest(strategyId) {
    const resultsDiv = document.getElementById('backtest-results');
    const contentDiv = document.getElementById('results-content');

    // Simulate backtest results (in real implementation, this would call your API)
    contentDiv.innerHTML = `
        <div class="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
            <div class="flex items-center">
                <svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span class="text-green-800 font-medium">Backtest completed successfully!</span>
            </div>
        </div>

        <div class="grid md:grid-cols-2 gap-6">
            <div class="bg-white border border-gray-200 rounded-lg p-4">
                <h5 class="font-bold text-gray-900 mb-2">Performance Summary</h5>
                <div class="space-y-2">
                    <div class="flex justify-between">
                        <span class="text-gray-600">Total Return</span>
                        <span class="font-bold text-green-600">+24.7%</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Total Trades</span>
                        <span class="font-bold">234</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Win Rate</span>
                        <span class="font-bold text-green-600">89.3%</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Max Drawdown</span>
                        <span class="font-bold text-red-600">-12.4%</span>
                    </div>
                </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-lg p-4">
                <h5 class="font-bold text-gray-900 mb-2">Risk Metrics</h5>
                <div class="space-y-2">
                    <div class="flex justify-between">
                        <span class="text-gray-600">Sharpe Ratio</span>
                        <span class="font-bold">1.8</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Sortino Ratio</span>
                        <span class="font-bold">2.1</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Calmar Ratio</span>
                        <span class="font-bold">1.9</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Volatility</span>
                        <span class="font-bold">18.5%</span>
                    </div>
                </div>
            </div>
        </div>
    `;

    resultsDiv.classList.remove('hidden');
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    renderStrategies();

    // Add filter event listeners
    document.getElementById('risk-filter').addEventListener('change', renderStrategies);
    document.getElementById('sort-by').addEventListener('change', renderStrategies);

    // Modal close handlers
    document.getElementById('close-modal').addEventListener('click', closeModal);
    document.getElementById('backtest-modal').addEventListener('click', function(e) {
        if (e.target === this) closeModal();
    });
});
</script>

<?php get_footer(); ?>