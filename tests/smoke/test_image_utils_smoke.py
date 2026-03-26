"""Smoke tests for image embedding utilities."""

from pathlib import Path

from modern_graphics.image_utils import (
    file_to_dataurl,
    image_path_to_img_tag,
    image_path_to_svg_image,
)
import pytest


def _create_tiny_png(path: Path) -> Path:
    """Create a minimal 1x1 red PNG file."""
    # Minimal PNG: 8-byte signature + IHDR + IDAT + IEND
    import struct, zlib
    sig = b'\x89PNG\r\n\x1a\n'
    # IHDR: 1x1, 8-bit RGB
    ihdr_data = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
    # IDAT: single red pixel (filter byte 0 + RGB)
    raw = zlib.compress(b'\x00\xff\x00\x00')
    idat_crc = zlib.crc32(b'IDAT' + raw) & 0xffffffff
    idat = struct.pack('>I', len(raw)) + b'IDAT' + raw + struct.pack('>I', idat_crc)
    # IEND
    iend_crc = zlib.crc32(b'IEND') & 0xffffffff
    iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
    path.write_bytes(sig + ihdr + idat + iend)
    return path


def test_file_to_dataurl_png(tmp_path):
    png = _create_tiny_png(tmp_path / "test.png")
    result = file_to_dataurl(str(png))
    assert result.startswith("data:image/png;base64,")


def test_file_to_dataurl_not_found():
    with pytest.raises(FileNotFoundError):
        file_to_dataurl("/nonexistent/image.png")


def test_file_to_dataurl_too_large(tmp_path):
    big = tmp_path / "big.png"
    big.write_bytes(b"\x00" * 100)
    with pytest.raises(ValueError, match="too large"):
        file_to_dataurl(str(big), max_size_mb=0.00001)


def test_image_path_to_img_tag(tmp_path):
    png = _create_tiny_png(tmp_path / "test.png")
    result = image_path_to_img_tag(str(png))
    assert "<img" in result
    assert "data:image/png;base64," in result


def test_image_path_to_svg_image(tmp_path):
    png = _create_tiny_png(tmp_path / "test.png")
    result = image_path_to_svg_image(str(png), width=100, height=100)
    assert "<svg" in result
    assert "<image" in result
    assert 'href="data:image/png;base64,' in result
