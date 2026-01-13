#!/usr/bin/env python3
"""
Agent Coordinate Calibration Tool
================================

Calibrates and validates agent screen coordinates for PyAutoGUI operations.

Author: Agent-2 (Architecture & Design)
Date: 2025-12-28
V2 Compliant: Yes (<300 lines)

<!-- SSOT Domain: tools -->
"""

import json
import time
import sys
from pathlib import Path
from typing import Dict, Tuple, List, Any
import logging

# Try to import PyAutoGUI
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
except ImportError:
    PYAUTOGUI_AVAILABLE = False

# Agent coordinate mappings
AGENT_COORDINATES = {
    "Agent-1": (-1269, 481),   # Integration & Core Systems
    "Agent-2": (-308, 480),    # Architecture & Design
    "Agent-3": (-1269, 1001),  # Infrastructure & DevOps
    "Agent-4": (-308, 1000),   # Captain (ALWAYS LAST)
    "Agent-5": (652, 421),     # Business Intelligence
    "Agent-6": (1612, 419),    # Coordination & Communication
    "Agent-7": (653, 940),     # Web Development
    "Agent-8": (1611, 941),    # SSOT & System Integration
}

class CoordinateCalibrator:
    """Calibrates agent screen coordinates."""

    def __init__(self):
        self.coordinates = AGENT_COORDINATES.copy()
        self.calibration_results = {}
        self.logger = logging.getLogger(__name__)

        if not PYAUTOGUI_AVAILABLE:
            self.logger.error("PyAutoGUI not available - coordinate calibration disabled")

    def calibrate_all_agents(self) -> Dict[str, Dict]:
        """Calibrate coordinates for all agents."""
        if not PYAUTOGUI_AVAILABLE:
            return {"error": "PyAutoGUI not available"}

        results = {}

        for agent_id, expected_coords in self.coordinates.items():
            self.logger.info(f"Calibrating {agent_id} at {expected_coords}")
            result = self._calibrate_agent(agent_id, expected_coords)
            results[agent_id] = result

            # Small delay between calibrations
            time.sleep(0.5)

        self.calibration_results = results
        return results

    def _calibrate_agent(self, agent_id: str, expected_coords: Tuple[int, int]) -> Dict:
        """Calibrate coordinates for a specific agent."""
        try:
            # Move mouse to expected position
            pyautogui.moveTo(expected_coords[0], expected_coords[1], duration=0.5)

            # Wait for movement to complete
            time.sleep(0.5)

            # Get actual position
            actual_pos = pyautogui.position()
            actual_coords = (actual_pos.x, actual_pos.y)

            # Calculate deviation
            deviation_x = abs(expected_coords[0] - actual_coords[0])
            deviation_y = abs(expected_coords[1] - actual_coords[1])
            total_deviation = (deviation_x ** 2 + deviation_y ** 2) ** 0.5

            # Determine status
            if total_deviation < 10:  # Within 10 pixels
                status = "excellent"
            elif total_deviation < 50:
                status = "good"
            elif total_deviation < 100:
                status = "acceptable"
            else:
                status = "poor"

            result = {
                "expected": expected_coords,
                "actual": actual_coords,
                "deviation": {
                    "x": deviation_x,
                    "y": deviation_y,
                    "total": round(total_deviation, 1)
                },
                "status": status,
                "needs_adjustment": total_deviation > 50
            }

            if result["needs_adjustment"]:
                result["recommendation"] = f"Consider adjusting coordinates by ({expected_coords[0] - actual_coords[0]}, {expected_coords[1] - actual_coords[1]})"

            return result

        except Exception as e:
            return {
                "expected": expected_coords,
                "error": str(e),
                "status": "error"
            }

    def validate_screen_bounds(self) -> Dict[str, Any]:
        """Validate that all coordinates are within screen bounds."""
        if not PYAUTOGUI_AVAILABLE:
            return {"error": "PyAutoGUI not available"}

        try:
            screen_size = pyautogui.size()
            screen_width, screen_height = screen_size.width, screen_size.height

            validation_results = {}

            for agent_id, coords in self.coordinates.items():
                x, y = coords

                within_bounds = (0 <= x < screen_width) and (0 <= y < screen_height)

                validation_results[agent_id] = {
                    "coordinates": coords,
                    "screen_size": (screen_width, screen_height),
                    "within_bounds": within_bounds,
                    "issues": [] if within_bounds else [f"Coordinates ({x}, {y}) outside screen bounds ({screen_width}x{screen_height})"]
                }

            return {
                "screen_size": (screen_width, screen_height),
                "validation_results": validation_results,
                "all_valid": all(r["within_bounds"] for r in validation_results.values())
            }

        except Exception as e:
            return {"error": str(e)}

    def generate_coordinate_report(self) -> str:
        """Generate a comprehensive coordinate calibration report."""
        report_lines = [
            "# Agent Coordinate Calibration Report",
            "",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Screen Bounds Validation",
        ]

        bounds_check = self.validate_screen_bounds()
        if "error" not in bounds_check:
            screen_size = bounds_check["screen_size"]
            report_lines.append(f"- Screen Size: {screen_size[0]}x{screen_size[1]}")
            report_lines.append(f"- All coordinates valid: {'✅' if bounds_check['all_valid'] else '❌'}")

            if not bounds_check["all_valid"]:
                report_lines.append("\n### Out of Bounds Agents:")
                for agent_id, result in bounds_check["validation_results"].items():
                    if not result["within_bounds"]:
                        report_lines.append(f"- **{agent_id}**: {', '.join(result['issues'])}")

        report_lines.append("\n## Calibration Results")

        if self.calibration_results:
            for agent_id, result in self.calibration_results.items():
                report_lines.append(f"\n### {agent_id}")

                if "error" in result:
                    report_lines.append(f"- **Error**: {result['error']}")
                    continue

                expected = result["expected"]
                actual = result["actual"]
                deviation = result["deviation"]
                status = result["status"]

                status_emoji = {
                    "excellent": "✅",
                    "good": "✅",
                    "acceptable": "⚠️",
                    "poor": "❌",
                    "error": "❌"
                }.get(status, "❓")

                report_lines.extend([
                    f"- **Expected**: {expected}",
                    f"- **Actual**: {actual}",
                    f"- **Deviation**: {deviation['total']}px ({deviation['x']}x, {deviation['y']}y)",
                    f"- **Status**: {status_emoji} {status.title()}"
                ])

                if result.get("needs_adjustment"):
                    report_lines.append(f"- **Recommendation**: {result['recommendation']}")
        else:
            report_lines.append("- No calibration results available. Run calibration first.")

        report_lines.extend([
            "",
            "## Recommendations",
            "",
            "1. **Screen Layout**: Ensure agents are positioned correctly on screen",
            "2. **Resolution**: Verify consistent screen resolution across restarts",
            "3. **Window Focus**: Ensure agent windows maintain consistent positioning",
            "4. **Calibration**: Run calibration after screen resolution changes",
            "",
            "## Usage",
            "",
            "```bash",
            "python tools/calibrate_agent_coordinates.py --calibrate",
            "python tools/calibrate_agent_coordinates.py --validate-bounds",
            "```"
        ])

        return "\n".join(report_lines)

    def save_report(self, filename: str = "coordinate_calibration_report.md"):
        """Save calibration report to file."""
        report = self.generate_coordinate_report()

        with open(filename, 'w') as f:
            f.write(report)

        self.logger.info(f"Calibration report saved to {filename}")


def main():
    """CLI interface for coordinate calibration."""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Coordinate Calibration")
    parser.add_argument("--calibrate", action="store_true", help="Run coordinate calibration")
    parser.add_argument("--validate-bounds", action="store_true", help="Validate screen bounds")
    parser.add_argument("--report", action="store_true", help="Generate calibration report")
    parser.add_argument("--save-report", type=str, help="Save report to file")

    args = parser.parse_args()

    calibrator = CoordinateCalibrator()

    if args.calibrate:
        print("🔧 Starting coordinate calibration...")
        results = calibrator.calibrate_all_agents()
        print("✅ Calibration complete")

        # Print summary
        for agent_id, result in results.items():
            if "error" in result:
                print(f"❌ {agent_id}: {result['error']}")
            else:
                status = result["status"]
                deviation = result["deviation"]["total"]
                print(f"{'✅' if status in ['excellent', 'good'] else '⚠️'} {agent_id}: {status.title()} ({deviation}px deviation)")

    if args.validate_bounds:
        print("\n📐 Validating screen bounds...")
        bounds_result = calibrator.validate_screen_bounds()

        if "error" in bounds_result:
            print(f"❌ Bounds validation error: {bounds_result['error']}")
        else:
            screen_size = bounds_result["screen_size"]
            all_valid = bounds_result["all_valid"]
            print(f"📐 Screen Size: {screen_size[0]}x{screen_size[1]}")
            print(f"📐 All coordinates valid: {'✅' if all_valid else '❌'}")

            if not all_valid:
                print("\nOut of bounds agents:")
                for agent_id, result in bounds_result["validation_results"].items():
                    if not result["within_bounds"]:
                        print(f"❌ {agent_id}: {', '.join(result['issues'])}")

    if args.report or args.save_report:
        report = calibrator.generate_coordinate_report()

        if args.save_report:
            calibrator.save_report(args.save_report)
            print(f"📄 Report saved to {args.save_report}")
        else:
            print("\n" + "="*60)
            print(report)
            print("="*60)


if __name__ == "__main__":
    main()


