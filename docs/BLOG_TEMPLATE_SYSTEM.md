# Blog Post Template System

## Overview

A standardized template system for generating consistent trading strategy blog posts on tradingrobotplug.com.

## Files Created

### Template Files
- `tools/templates/strategy_blog_post_template.html` - Main blog post template
- `tools/templates/README.md` - Template documentation
- `tools/templates/TEMPLATE_PREVIEW.md` - Visual structure preview

### Code Files
- `tools/strategy_blog_automation.py` - Updated to use template system
- `tools/schedule_strategy_blog.py` - Scheduled automation script

## Template Features

### Structure
1. **Header** - Strategy name, date, symbol
2. **Overview** - Brief introduction
3. **Strategy Configuration** - Two-column layout (Indicators | Risk Parameters)
4. **Entry Logic** - Long and Short entry conditions
5. **Exit Strategy** - Profit targets, stops, trailing stops
6. **Risk Management** - Detailed risk explanation
7. **Key Features** - Strategy highlights
8. **Performance Considerations** - When strategy works best
9. **Call-to-Action** - Links to free/premium reports
10. **Disclaimer** - Hobbyist/educational notice

### WordPress Integration
- Uses Gutenberg block format comments
- Properly renders in WordPress editor
- Mobile-responsive through WordPress blocks
- SEO-friendly heading hierarchy

## Usage

### Generate a Blog Post
```bash
python tools/strategy_blog_automation.py --site tradingrobotplug.com --generate-post
```

### Generate Reports
```bash
# Free report
python tools/strategy_blog_automation.py --site tradingrobotplug.com --generate-report

# Premium report
python tools/strategy_blog_automation.py --site tradingrobotplug.com --generate-report --premium
```

### Schedule Automated Posts
```bash
python tools/schedule_strategy_blog.py --site tradingrobotplug.com --frequency weekly
```

## Template Variables

All variables are automatically filled from strategy analysis:

- `{strategy_name}` - Strategy name
- `{analysis_date}` - Analysis date
- `{symbol}` - Trading symbol
- `{strategy_type}` - Strategy type
- `{indicators_list}` - HTML list of indicators
- `{risk_parameters_list}` - HTML list of risk parameters
- `{long_entry_conditions}` - Long entry conditions
- `{short_entry_conditions}` - Short entry conditions
- `{exit_strategy_list}` - Exit strategy details
- `{risk_management_list}` - Risk management features
- `{key_features_list}` - Key features
- `{performance_notes_list}` - Performance notes
- `{report_slug}` - Free report URL slug
- `{premium_report_slug}` - Premium report URL slug

## Customization

To modify the template:
1. Edit `tools/templates/strategy_blog_post_template.html`
2. Ensure variables are filled in `generate_blog_post_content()`
3. Test with a new post generation

## Benefits

✅ **Consistency** - All posts follow the same structure  
✅ **Professional** - Clean, organized layout  
✅ **Maintainable** - Single template file  
✅ **Scalable** - Easy to add new strategies  
✅ **Conversion-Optimized** - Clear CTAs to reports  

## Next Steps

1. ✅ Template created and tested
2. ⏳ Add more strategy templates (if needed)
3. ⏳ Create template preview tool
4. ⏳ Add template validation

