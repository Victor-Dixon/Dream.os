#!/usr/bin/env python3
"""
Create About Us Page for TradingRobotPlug Credibility
"""

import json
import paramiko
from pathlib import Path

def create_about_page():
    """Create About Us page for TradingRobotPlug"""

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

    # About Us page content (simplified to avoid escaping issues)
    about_content = """<h1>About TradingRobotPlug</h1>

<p><strong>Our Mission:</strong> To democratize algorithmic trading by providing accessible, powerful, and reliable automated trading solutions that help traders of all levels achieve consistent results through data-driven strategies and AI-powered insights.</p>

<h2>Our Story</h2>

<p>TradingRobotPlug was founded with a simple belief: that advanced trading technology should be accessible to everyone, not just institutional traders with million-dollar budgets. We started as a small team of experienced traders and software engineers who saw the gap between what was possible with modern technology and what was available to individual traders.</p>

<p>After years of developing proprietary trading systems for hedge funds and family offices, we decided to bring that same level of sophistication and reliability to retail traders. TradingRobotPlug was born from the recognition that the future of trading lies in automation, data-driven decision making, and AI-powered insights.</p>

<h2>Our Values</h2>

<p><strong>Transparency:</strong> We believe in complete transparency about our strategies, performance, and risks. No hidden fees, no undisclosed limitations, no surprise drawdowns.</p>

<p><strong>Reliability:</strong> Our systems are built for 24/7 operation with enterprise-grade reliability. We prioritize stability over flashy features.</p>

<p><strong>Education:</strong> We educate traders about automated trading, risk management, and strategy development.</p>

<h2>Company Information</h2>

<p><strong>Legal Entity:</strong> TradingRobotPlug LLC</p>
<p><strong>Jurisdiction:</strong> Delaware, United States</p>
<p><strong>Contact:</strong> For business inquiries, please use our contact form or email us at legal@tradingrobotplug.com</p>

<h2>Risk Disclosure</h2>

<p><strong>Important:</strong> Trading cryptocurrencies and forex involves substantial risk of loss. TradingRobotPlug provides automated trading tools but cannot guarantee profits or prevent losses. All trading involves risk, and past performance does not guarantee future results. Please trade responsibly and only with money you can afford to lose.</p>

<p>For full risk disclosures, please review our <a href="/product-terms">Product Terms</a>.</p>"""

    print("🔄 Creating About Us page for TradingRobotPlug...")

    # Create About Us page
    command = f"cd {wp_path} && wp post create --post_type=page --post_title='About Us' --post_name='about' --post_content='{about_content}' --post_status=publish"
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()

    print("About Us page creation result:")
    print(output)
    if error:
        print("Error:", error)

    ssh.close()

    if "Success:" in output:
        print("✅ About Us page created successfully")
        return True
    else:
        print("❌ Failed to create About Us page")
        return False

if __name__ == "__main__":
    success = create_about_page()
    if success:
        print("\n🎯 About Us page complete!")
        print("Next: Create Team page or validate page loads correctly")
    else:
        print("\n❌ About Us page creation failed")