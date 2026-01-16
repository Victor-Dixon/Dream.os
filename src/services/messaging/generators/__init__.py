#!/usr/bin/env python3
"""
Generators Package - Work Resume Generation Infrastructure
==========================================================

<!-- SSOT Domain: messaging -->

Package containing specialized components for generating comprehensive work resumes
from agent status, devlogs, and activity data.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

from .data_collector import WorkResumeDataCollector
from .section_generator import WorkResumeSectionGenerator
from .resume_builder import WorkResumeBuilder

__all__ = [
    'WorkResumeDataCollector',
    'WorkResumeSectionGenerator',
    'WorkResumeBuilder',
]