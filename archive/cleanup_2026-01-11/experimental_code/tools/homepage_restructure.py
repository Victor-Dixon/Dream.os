#!/usr/bin/env python3
"""
TradingRobotPlug Homepage Restructure Script
Replaces placeholder content with Services + Products sections for credibility overhaul
"""

import json
import paramiko
from pathlib import Path

def create_services_products_homepage():
    """Create new homepage content with Services and Products sections"""

    homepage_content = """<!-- wp:heading {"level":1,"className":"hero-title"} -->
<h1 class="hero-title">Advanced Trading Automation Platform</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"className":"hero-subtitle"} -->
<p class="hero-subtitle">Transform your trading with AI-powered automation, real-time sentiment analysis, and proven backtesting strategies. Join thousands of traders who have automated their success.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons {"className":"hero-cta"} -->
<div class="wp-block-buttons hero-cta"><!-- wp:button {"className":"is-style-primary"} -->
<div class="wp-block-button is-style-primary"><a class="wp-block-button__link" href="/waitlist">Start Free Trial</a></div>
<!-- /wp:button -->

<!-- wp:button {"className":"is-style-secondary"} -->
<div class="wp-block-button is-style-secondary"><a class="wp-block-button__link" href="/features">View Features</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->

<!-- wp:separator {"className":"section-divider"} -->
<hr class="wp-block-separator section-divider"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":2,"className":"section-title"} -->
<h2 class="section-title">Our Services</h2>
<!-- /wp:heading -->

<!-- wp:columns {"className":"services-grid"} -->
<div class="wp-block-columns services-grid"><!-- wp:column {"className":"service-card"} -->
<div class="wp-block-column service-card"><!-- wp:heading {"level":3} -->
<h3>Automated Trading Bots</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Deploy sophisticated trading algorithms that execute 24/7 across multiple markets. Our AI-driven bots analyze market conditions, sentiment data, and technical indicators to make intelligent trading decisions.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>Multi-market support (Forex, Crypto, Stocks)</li><li>Real-time sentiment analysis</li><li>Risk management integration</li><li>Performance tracking dashboard</li></ul>
<!-- /wp:list --></div>
<!-- /wp:column -->

<!-- wp:column {"className":"service-card"} -->
<div class="wp-block-column service-card"><!-- wp:heading {"level":3} -->
<h3>Backtesting & Strategy Development</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Validate your trading strategies with historical data spanning decades. Our advanced backtesting engine provides detailed performance metrics, drawdown analysis, and optimization tools.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>20+ years of historical data</li><li>Multiple timeframe analysis</li><li>Walk-forward optimization</li><li>Detailed performance reports</li></ul>
<!-- /wp:list --></div>
<!-- /wp:column -->

<!-- wp:column {"className":"service-card"} -->
<div class="wp-block-column service-card"><!-- wp:heading {"level":3} -->
<h3>Market Intelligence Platform</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Gain competitive advantage with real-time market intelligence. Our platform aggregates news, social sentiment, economic indicators, and technical analysis into actionable insights.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>Real-time news aggregation</li><li>Social media sentiment analysis</li><li>Economic calendar integration</li><li>Custom alert system</li></ul>
<!-- /wp:list --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:separator {"className":"section-divider"} -->
<hr class="wp-block-separator section-divider"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":2,"className":"section-title"} -->
<h2 class="section-title">Our Products</h2>
<!-- /wp:heading -->

<!-- wp:columns {"className":"products-grid"} -->
<div class="wp-block-columns products-grid"><!-- wp:column {"className":"product-card"} -->
<div class="wp-block-column product-card"><!-- wp:heading {"level":3} -->
<h3>TradingRobotPlug Pro</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>$99/month</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Full-featured trading automation platform with unlimited bots, advanced analytics, and priority support.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>Unlimited trading bots</li><li>Advanced backtesting suite</li><li>Real-time market data</li><li>Priority customer support</li><li>API access</li></ul>
<!-- /wp:list -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button {"className":"is-style-primary"} -->
<div class="wp-block-button is-style-primary"><a class="wp-block-button__link" href="/pricing">Learn More</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div>
<!-- /wp:column -->

<!-- wp:column {"className":"product-card"} -->
<div class="wp-block-column product-card"><!-- wp:heading {"level":3} -->
<h3>TradingRobotPlug Standard</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>$49/month</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Essential trading automation tools for individual traders. Perfect for getting started with algorithmic trading.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>Up to 5 trading bots</li><li>Basic backtesting tools</li><li>Market sentiment analysis</li><li>Email support</li><li>Mobile app access</li></ul>
<!-- /wp:list -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button {"className":"is-style-primary"} -->
<div class="wp-block-button is-style-primary"><a class="wp-block-button__link" href="/pricing">Learn More</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div>
<!-- /wp:column -->

<!-- wp:column {"className":"product-card"} -->
<div class="wp-block-column product-card"><!-- wp:heading {"level":3} -->
<h3>Market Intelligence Add-on</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>$29/month</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Enhance your trading with advanced market intelligence tools and real-time sentiment analysis.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>Real-time news feeds</li><li>Social sentiment tracking</li><li>Economic indicator alerts</li><li>Custom dashboard widgets</li><li>Data export capabilities</li></ul>
<!-- /wp:list -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button {"className":"is-style-primary"} -->
<div class="wp-block-button is-style-primary"><a class="wp-block-button__link" href="/features">Learn More</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:separator {"className":"section-divider"} -->
<hr class="wp-block-separator section-divider"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":2,"className":"section-title"} -->
<h2 class="section-title">Risk Disclosure</h2>
<!-- /wp:heading -->

<!-- wp:paragraph {"className":"risk-disclosure"} -->
<p class="risk-disclosure"><strong>Trading cryptocurrencies and forex involves substantial risk of loss and is not suitable for every investor.</strong> Past performance does not guarantee future results. All trading involves risk, and there is a possibility of losing money beyond your initial investment. Only trade with money you can afford to lose.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>For full risk disclosures and terms, please review our <a href="/product-terms">Product Terms</a>, <a href="/terms-of-service">Terms of Service</a>, and <a href="/privacy">Privacy Policy</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons {"className":"footer-cta"} -->
<div class="wp-block-buttons footer-cta"><!-- wp:button {"className":"is-style-secondary"} -->
<div class="wp-block-button is-style-secondary"><a class="wp-block-button__link" href="/waitlist">Start Your Free Trial</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->"""

    return homepage_content

def update_homepage_content():
    """Update the homepage with new Services and Products content"""

    # Load credentials
    repo_root = Path(__file__).resolve().parents[1]
    creds_file = repo_root / ".deploy_credentials" / "sites.json"
    with open(creds_file, 'r') as f:
        creds_data = json.load(f)
    config = creds_data["tradingrobotplug.com"]

    # Connect via SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=config["host"],
        username=config["username"],
        password=config["password"],
        port=config["port"]
    )

    wp_path = config["remote_path"]

    # Get new homepage content
    new_content = create_services_products_homepage()

    print("🔄 Updating homepage with Services + Products sections...")

    # Update the homepage post content via WP-CLI
    # Escape single quotes for shell command
    escaped_content = new_content.replace("'", "\\'")

    command = f"cd {wp_path} && wp post update 1 --post_content='{escaped_content}' --post_title='TradingRobotPlug - Advanced Trading Automation'"
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()

    print("Homepage update result:")
    print(output)
    if error:
        print("Error:", error)

    # Also update the post status to publish and set it as front page
    command = f"cd {wp_path} && wp post update 1 --post_status=publish"
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()

    if error:
        print("Error setting post status:", error)

    ssh.close()

    if "Success:" in output:
        print("✅ Homepage successfully updated with Services and Products sections")
        return True
    else:
        print("❌ Failed to update homepage")
        return False

if __name__ == "__main__":
    success = update_homepage_content()
    if success:
        print("\n🎯 Homepage restructure complete!")
        print("Next: Validate homepage loads correctly with new content")
    else:
        print("\n❌ Homepage restructure failed")