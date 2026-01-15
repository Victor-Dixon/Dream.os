#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Discord Approval Commands
=========================

Commands for reviewing and approving Phase 1 consolidation plan.

Author: Agent-4 (Captain)
Date: 2025-01-27
"""

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class ApprovalCommands(commands.Cog):
    """Commands for reviewing consolidation approval plans."""

    def __init__(self, bot):
        """Initialize approval commands."""
        self.bot = bot
        self.project_root = Path(__file__).parent.parent.parent

    @commands.command(name="approval_plan", description="View Phase 1 consolidation approval plan")
    async def approval_plan(self, ctx: commands.Context):
        """Display Phase 1 consolidation approval plan summary."""
        try:
            plan_path = self.project_root / "docs/organization/PHASE1_DETAILED_APPROVAL_EXPLANATION.md"
            
            if not plan_path.exists():
                await ctx.send("❌ Approval plan document not found!")
                return

            # Read the plan
            with open(plan_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Create embed with summary
            embed = discord.Embed(
                title="📋 Phase 1 Consolidation - Approval Plan",
                description="**What You're Signing Off On**",
                color=discord.Color.blue(),
            )

            # Add key information
            embed.add_field(
                name="📊 The Numbers",
                value="**Current**: 75 repos\n**After Phase 1**: 49 repos\n**Reduction**: 26 repos (35% reduction)\n\n⚠️ **Note**: fastapi (external library) will be skipped - keep both as dependencies",
                inline=False
            )

            embed.add_field(
                name="🎯 What Will Happen",
                value="1. **Case Variations** (12 repos) - ⭐ ZERO RISK\n2. **Vision Attempts** (4 repos) - ⭐⭐ LOW RISK\n3. **Dream Projects** (2 repos) - ⭐⭐ MEDIUM RISK\n4. **Trading Repos** (3 repos) - ⭐⭐ MEDIUM RISK\n5. **Agent Systems** (2 repos) - ⭐⭐ MEDIUM RISK\n6. **Streaming Tools** (1 repo) - ⭐ LOW RISK\n7. **DaDudekC Projects** (1 repo) - ⭐ LOW RISK\n8. **ML Models** (1 repo) - ⭐ LOW RISK\n9. **Resume/Templates** (1 repo) - ⭐ LOW RISK",
                inline=False
            )

            embed.add_field(
                name="🚨 Critical Protections",
                value="✅ AutoDream_Os (repo 7) - **PROTECTED** (your current project)\n✅ prompt-library (repo 11) - **PROTECTED** (messaging protocol)\n✅ prompts (repo 65) - **PROTECTED** (messaging protocol)\n✅ All merged repos will be **ARCHIVED** (not deleted)",
                inline=False
            )

            embed.add_field(
                name="🛡️ Safety Measures",
                value="✅ Backups before every merge\n✅ Dry-run mode testing\n✅ Rollback capability\n✅ Batch execution (start with safest)",
                inline=False
            )

            embed.add_field(
                name="📝 Full Details",
                value=f"See: `docs/organization/PHASE1_DETAILED_APPROVAL_EXPLANATION.md`\n\n**File Location**: `{plan_path}`",
                inline=False
            )

            embed.set_footer(text="Review the detailed document before approving")

            await ctx.send(embed=embed)

            # Also send a file attachment if possible
            try:
                await ctx.send(
                    file=discord.File(plan_path),
                    content="📄 **Full Detailed Approval Explanation** - Review this document carefully!"
                )
            except Exception as e:
                logger.warning(f"Could not send file attachment: {e}")
                await ctx.send(
                    f"📄 **Full document available at**: `{plan_path}`\n"
                    f"Read it to understand exactly what you're approving!"
                )

        except Exception as e:
            logger.error(f"Error displaying approval plan: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="approval_summary", description="Quick summary of Phase 1 consolidation")
    async def approval_summary(self, ctx: commands.Context):
        """Display quick summary of what's being approved."""
        embed = discord.Embed(
            title="📋 Phase 1 Consolidation - Quick Summary",
            description="**What You're Approving**",
            color=discord.Color.green(),
        )

        embed.add_field(
            name="📊 Bottom Line",
            value="**75 repos → 49 repos** (26 repos reduction, 35% fewer repos)\n\n⚠️ **Note**: fastapi (external library) skipped - keep both as dependencies",
            inline=False
        )

        embed.add_field(
            name="✅ Safe Operations",
            value="**12 repos** - Case variations (ZERO RISK)\n**4 repos** - Vision attempts (extract then archive)\n**11 repos** - Functional groups (MEDIUM RISK)",
            inline=False
        )

        embed.add_field(
            name="🚨 What's Protected",
            value="✅ AutoDream_Os (your current project)\n✅ prompt-library & prompts (messaging protocol)\n✅ All repos archived (not deleted)",
            inline=False
        )

        embed.add_field(
            name="🛡️ Safety",
            value="✅ Backups before every merge\n✅ Dry-run testing first\n✅ Rollback capability\n✅ Execute in safe batches",
            inline=False
        )

        embed.add_field(
            name="📝 Full Details",
            value="Use `!approval_plan` to see complete detailed explanation",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="approval_checklist", description="Approval checklist for Phase 1")
    async def approval_checklist(self, ctx: commands.Context):
        """Display approval checklist."""
        embed = discord.Embed(
            title="✅ Phase 1 Approval Checklist",
            description="**Review Before Approving**",
            color=discord.Color.orange(),
        )

        checklist = """
**Before Approving, Confirm:**
- [ ] I understand 27 repos will be merged/archived
- [ ] I understand AutoDream_Os (repo 7) is PROTECTED
- [ ] I understand messaging protocol repos are PROTECTED
- [ ] I understand all repos will be ARCHIVED (not deleted)
- [ ] I understand backups will be created
- [ ] I understand dry-run testing will happen first
- [ ] I understand execution starts with safest batch (case variations)
- [ ] I have reviewed the detailed approval document

**To Approve:**
Use `!approve_phase1` command (when ready)
        """

        embed.add_field(name="Checklist", value=checklist, inline=False)
        embed.set_footer(text="Review carefully before approving!")

        await ctx.send(embed=embed)

    @commands.command(name="approve_phase1", description="Approve Phase 1 consolidation execution")
    async def approve_phase1(self, ctx: commands.Context):
        """Approve Phase 1 consolidation execution."""
        embed = discord.Embed(
            title="⚠️ Phase 1 Approval",
            description="**Are you sure you want to approve?**",
            color=discord.Color.red(),
        )

        embed.add_field(
            name="What This Approves",
            value="✅ Merge 22 repos into target repos (fastapi skipped)\n✅ Archive 4 vision attempt repos\n✅ Total: 26 repos reduction (75 → 49)\n⚠️ fastapi: Skip merge (keep both as external library dependencies)",
            inline=False
        )

        embed.add_field(
            name="Next Steps After Approval",
            value="1. Dry-run testing on all batches\n2. Review dry-run results\n3. Execute Batch 1 (case variations - safest)\n4. Monitor progress\n5. Execute remaining batches",
            inline=False
        )

        embed.add_field(
            name="⚠️ Confirmation Required",
            value="Reply with `!confirm_approve_phase1` to finalize approval",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="confirm_approve_phase1", description="Final confirmation for Phase 1 approval")
    async def confirm_approve_phase1(self, ctx: commands.Context):
        """Final confirmation for Phase 1 approval."""
        # Write approval to file
        approval_path = self.project_root / "docs/organization/PHASE1_APPROVAL_RECEIVED.md"
        
        approval_content = f"""# Phase 1 Consolidation - Approval Received

**Date**: 2025-01-27
**Approved By**: {ctx.author.display_name} (Discord User ID: {ctx.author.id})
**Approved Via**: Discord command `!confirm_approve_phase1`
**Status**: ✅ **APPROVED**

---

## Approval Details

**What Was Approved**:
- Phase 1 consolidation execution (27 repos reduction)
- Vision attempts extraction and archiving (4 repos)
- Execution timeline (3 weeks)
- Safety measures (backups, dry-run, rollback)

**Next Steps**:
1. Dry-run testing on all batches
2. Review dry-run results
3. Execute Batch 1 (case variations - safest)
4. Monitor progress
5. Execute remaining batches

---

**Approval timestamp**: {ctx.message.created_at.isoformat()}

**🐝 WE. ARE. SWARM. ⚡🔥**
"""

        try:
            approval_path.parent.mkdir(parents=True, exist_ok=True)
            with open(approval_path, 'w', encoding='utf-8') as f:
                f.write(approval_content)

            embed = discord.Embed(
                title="✅ Phase 1 Approval Confirmed!",
                description="**Approval received and recorded**",
                color=discord.Color.green(),
            )

            embed.add_field(
                name="Approval Recorded",
                value=f"Approval saved to: `{approval_path}`",
                inline=False
            )

            embed.add_field(
                name="Next Steps",
                value="1. Agent-1 will run dry-run tests\n2. Review dry-run results\n3. Execute Batch 1 (case variations)\n4. Monitor progress",
                inline=False
            )

            await ctx.send(embed=embed)

            # Notify agents
            logger.info(f"✅ Phase 1 approval received from {ctx.author.display_name}")

        except Exception as e:
            logger.error(f"Error recording approval: {e}", exc_info=True)
            await ctx.send(f"❌ Error recording approval: {e}")


def setup(bot):
    """Add approval commands to bot."""
    bot.add_cog(ApprovalCommands(bot))
    logger.info("✅ Approval commands loaded")

