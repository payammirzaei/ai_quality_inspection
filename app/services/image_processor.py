from PIL import Image, ImageEnhance
import cv2
import numpy as np
from typing import Tuple, Optional
import io

class ImageProcessor:
    @staticmethod
    def validate_image(image: Image.Image) -> bool:
        """Validate if image is suitable for defect detection"""
        if image is None:
            return False
        
        # Check minimum size
        min_size = 100
        if image.width < min_size or image.height < min_size:
            return False
        
        # Check if image has content (not completely black or white)
        img_array = np.array(image)
        if img_array.size == 0:
            return False
        
        # Check for reasonable brightness
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        mean_brightness = np.mean(gray)
        if mean_brightness < 10 or mean_brightness > 245:
            return False
        
        return True
    
    @staticmethod
    def preprocess_for_detection(image: Image.Image) -> Image.Image:
        """Preprocess image for defect detection"""
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Enhance image quality
        image = ImageProcessor.enhance_image(image)
        
        return image
    
    @staticmethod
    def enhance_image(image: Image.Image) -> Image.Image:
        """Enhance image quality for better detection"""
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)
        
        return image
    
    @staticmethod
    def resize_image(image: Image.Image, target_size: Tuple[int, int] = (224, 224)) -> Image.Image:
        """Resize image while maintaining aspect ratio"""
        # Calculate aspect ratio
        aspect_ratio = image.width / image.height
        target_aspect_ratio = target_size[0] / target_size[1]
        
        if aspect_ratio > target_aspect_ratio:
            # Image is wider than target
            new_width = int(target_size[1] * aspect_ratio)
            new_height = target_size[1]
        else:
            # Image is taller than target
            new_width = target_size[0]
            new_height = int(target_size[0] / aspect_ratio)
        
        # Resize image
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create new image with target size and paste resized image
        result = Image.new('RGB', target_size, (128, 128, 128))  # Gray background
        paste_x = (target_size[0] - new_width) // 2
        paste_y = (target_size[1] - new_height) // 2
        result.paste(resized, (paste_x, paste_y))
        
        return result
    
    @staticmethod
    def get_image_info(image: Image.Image) -> dict:
        """Get basic information about the image"""
        return {
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "format": getattr(image, 'format', 'Unknown'),
            "size_mb": len(image.tobytes()) / (1024 * 1024)
        }
    
    @staticmethod
    def create_thumbnail(image: Image.Image, size: Tuple[int, int] = (150, 150)) -> Image.Image:
        """Create a thumbnail for display purposes"""
        return image.copy().thumbnail(size, Image.Resampling.LANCZOS) 