#!/usr/bin/env python

import os
import sys
import json
import yaml
import click
from datetime import datetime

# Import core modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from seo_agent.core.keyword_engine import KeywordEngine
from seo_agent.core.content_optimizer import ContentOptimizer
from seo_agent.core.backlink_analyzer import BacklinkAnalyzer
from seo_agent.core.site_auditor import SiteAuditor

# Load configuration
def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# Approval system
def require_approval(operation, details, config):
    if config.get('defaults', {}).get('approval_required', True):
        click.echo(f"\n📋 {operation}")
        click.echo(f"Details: {details}")
        response = click.prompt("Proceed? (y/n/details)", type=str, default='y')
        
        if response.lower() == 'details':
            click.echo("Detailed preview not implemented yet.")
            return require_approval(operation, details, config)
        
        return response.lower() == 'y'
    return True

# CLI commands
@click.group()
def cli():
    """SEO Agent - AI-powered SEO automation tool"""
    pass

@cli.command('keyword-research')
@click.option('--seed', required=True, help='Seed keyword to expand from')
@click.option('--industry', help='Industry for context')
@click.option('--output', default=None, help='Output file path')
def keyword_research(seed, industry, output):
    """Generate keyword research based on seed keywords"""
    config = load_config()
    
    click.echo(f"🔍 Performing keyword research for: {seed}")
    
    # Initialize engine
    engine = KeywordEngine(config)
    
    # Generate keywords
    results = engine.generate_keywords(seed, industry)
    
    # Generate default output filename if not provided
    if not output:
        timestamp = datetime.now().strftime("%Y_%m_%d")
        output = f"keywords_report_{timestamp}.json"
        output_path = os.path.join(config['output']['reports_folder'], output)
    else:
        output_path = output
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save results
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    click.echo(f"✅ Keyword research complete. Results saved to: {output_path}")
    
    # Approval for export to CSV
    if require_approval("Export to CSV for use in other tools", f"{len(results['keywords'])} keywords", config):
        csv_path = output_path.replace('.json', '.csv')
        # Export functionality would go here
        click.echo(f"📤 Exported to: {csv_path}")

@cli.command('optimize-content')
@click.option('--file', required=True, help='Content file to optimize')
@click.option('--keywords', help='Keywords JSON file to use for optimization')
def optimize_content(file, keywords):
    """Optimize content for SEO"""
    config = load_config()
    
    click.echo(f"✍️ Optimizing content: {file}")
    click.echo("Not implemented yet. Coming soon!")

@cli.command('audit-site')
@click.option('--domain', required=True, help='Domain to audit')
@click.option('--depth', default=50, help='Maximum pages to crawl')
def audit_site(domain, depth):
    """Perform a technical SEO audit on a website"""
    config = load_config()
    
    click.echo(f"🔧 Auditing site: {domain} (max {depth} pages)")
    click.echo("Not implemented yet. Coming soon!")

@cli.command('backlink-research')
@click.option('--domain', required=True, help='Domain to research')
@click.option('--competitors', help='Comma-separated list of competitor domains')
def backlink_research(domain, competitors):
    """Research backlink opportunities"""
    config = load_config()
    
    comp_list = competitors.split(',') if competitors else []
    click.echo(f"🔗 Researching backlink opportunities for: {domain}")
    if comp_list:
        click.echo(f"Comparing against competitors: {', '.join(comp_list)}")
    
    click.echo("Not implemented yet. Coming soon!")

if __name__ == '__main__':
    cli()