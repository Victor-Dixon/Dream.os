#!/usr/bin/env python3
import json

with open('final_project_readiness_validation.json', 'r') as f:
    data = json.load(f)

print('=== FINAL PROJECT READINESS VALIDATION SUMMARY ===')
print('Timestamp:', data['timestamp'])
ssot = data['validation_domains']['ssot']['details']
total = ssot['files_validated']
valid = ssot['files_valid']
invalid = ssot['files_invalid']
print('Total files validated:', total)
print('Valid files:', valid)
print('Invalid files:', invalid)
print('Success rate: {:.1f}%'.format(valid/total*100))

print('\n=== DOMAIN BREAKDOWN (showing domains with issues) ===')
for domain, stats in ssot['domain_stats'].items():
    if stats['invalid'] > 0:
        print('{}: {}/{} valid ({} invalid)'.format(domain, stats['valid'], stats['total'], stats['invalid']))