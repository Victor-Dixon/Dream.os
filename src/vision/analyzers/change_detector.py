"""
<!-- SSOT Domain: vision -->

Change Detector
===============

Analyzes visual changes between images using image differencing and
provides change metrics and detection.

V2 Compliance: ≤200 lines, single responsibility, comprehensive error handling.

Author: Agent-2 - Architecture & Integration Specialist
License: MIT
"""

import logging

import numpy as np


class ChangeDetector:
    """
    Analyzes visual changes between images.

    Capabilities:
    - Image differencing
    - Change percentage calculation
    - Change region detection
    - Threshold-based change detection
    """

    def __init__(self, config: dict = None):
        """
        Initialize change detector.

        Args:
            config: Configuration dictionary with detection settings
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Change detection thresholds
        self.change_threshold = self.config.get("change_threshold", 10)
        self.min_change_area = self.config.get("min_change_area", 100)

    def detect_changes(self, image1: np.ndarray, image2: np.ndarray) -> dict:
        """
        Detect visual changes between two images.

        Args:
            image1: First image array
            image2: Second image array

        Returns:
            Dictionary with change detection results:
            - change_percentage: Percentage of image that changed
            - change_mask: Binary mask of changed regions
            - change_regions: List of change region bounding boxes
            - has_significant_change: Whether change exceeds threshold
        """
        try:
            # Ensure images are the same size
            if image1.shape != image2.shape:
                self.logger.warning("Images have different sizes, resizing image2 to match image1")
                # Simple resize - in production might want more sophisticated approach
                image2 = self._resize_image(image2, image1.shape[:2])

            # Calculate absolute difference
            diff = np.abs(image1.astype(np.float32) - image2.astype(np.float32))

            # Convert to grayscale if needed
            if len(diff.shape) == 3:
                # Convert to grayscale by averaging channels
                diff_gray = np.mean(diff, axis=2)
            else:
                diff_gray = diff

            # Create binary change mask
            change_mask = (diff_gray > self.change_threshold).astype(np.uint8)

            # Calculate change percentage
            total_pixels = change_mask.size
            changed_pixels = np.sum(change_mask)
            change_percentage = (changed_pixels / total_pixels) * 100

            # Find change regions
            change_regions = self._find_change_regions(change_mask)

            # Determine if change is significant
            has_significant_change = (
                change_percentage > self.config.get("significant_change_threshold", 1.0) and
                len(change_regions) > 0
            )

            return {
                "change_percentage": float(change_percentage),
                "change_mask": change_mask,
                "change_regions": change_regions,
                "has_significant_change": has_significant_change,
                "total_pixels": total_pixels,
                "changed_pixels": int(changed_pixels)
            }

        except Exception as e:
            self.logger.error(f"Change detection failed: {e}")
            return {
                "change_percentage": 0.0,
                "change_mask": np.array([]),
                "change_regions": [],
                "has_significant_change": False,
                "error": str(e)
            }

    def _resize_image(self, image: np.ndarray, target_size: tuple) -> np.ndarray:
        """Simple image resizing."""
        # Basic nearest neighbor resize - production version might use cv2.resize
        try:
            import cv2
            return cv2.resize(image, (target_size[1], target_size[0]))
        except ImportError:
            # Fallback to basic numpy resize
            self.logger.warning("OpenCV not available, using basic resize")
            # Very basic resize - just crop or pad
            h, w = target_size
            resized = np.zeros((h, w, image.shape[2]) if len(image.shape) == 3 else (h, w),
                              dtype=image.dtype)

            min_h = min(h, image.shape[0])
            min_w = min(w, image.shape[1])

            resized[:min_h, :min_w] = image[:min_h, :min_w]
            return resized

    def _find_change_regions(self, change_mask: np.ndarray) -> list:
        """
        Find bounding boxes of change regions.

        Args:
            change_mask: Binary mask of changed pixels

        Returns:
            List of (x, y, w, h) bounding boxes
        """
        try:
            import cv2

            # Find contours
            contours, _ = cv2.findContours(change_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            regions = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area >= self.min_change_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    regions.append((int(x), int(y), int(w), int(h)))

            return regions

        except ImportError:
            # Fallback without OpenCV - find basic bounding box
            self.logger.warning("OpenCV not available, using simplified region detection")
            if np.any(change_mask):
                rows, cols = np.where(change_mask > 0)
                if len(rows) > 0 and len(cols) > 0:
                    y_min, y_max = np.min(rows), np.max(rows)
                    x_min, x_max = np.min(cols), np.max(cols)
                    return [(x_min, y_min, x_max - x_min + 1, y_max - y_min + 1)]
            return []

    def compare_with_baseline(self, current_image: np.ndarray, baseline_image: np.ndarray) -> dict:
        """
        Compare current image with baseline and return change analysis.

        Args:
            current_image: Current image
            baseline_image: Baseline image to compare against

        Returns:
            Change analysis results
        """
        return self.detect_changes(baseline_image, current_image)