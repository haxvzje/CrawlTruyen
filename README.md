# CrawlTruyen

A Python web scraper that converts Vietnamese web novels (truyen) into EPUB format. This tool crawls story content from websites like **truyenfull.vn**, **truyentv.tv**, and **truyensextv.com**, and generates professionally formatted e-books.

## Features

- 🌐 **Multi-site Support**: Scrapes novels from various Vietnamese story websites
- 📚 **EPUB Generation**: Creates properly formatted e-books compatible with e-readers
- 🔄 **Series Support**: Handles multi-volume series with automatic organization
- 📖 **Metadata Management**: Preserves book information including title, author, and publication date
- 🎨 **Custom Styling**: Includes CSS styling for consistent EPUB formatting
- 💾 **Efficient Output**: Generates clean, organized output files in the `output/` directory

## Requirements

- Python 3.7+
- Dependencies (see `requirements.txt`):
  - `requests` - For HTTP requests
  - `beautifulsoup4` - For HTML parsing
  - `EbookLib` - For EPUB generation
  - `argparse` - For command-line argument parsing

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/CrawlTruyen.git
   cd CrawlTruyen
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with a novel URL using the `-l` or `--link` parameter:

```bash
python main.py -l https://truyenfull.vn/your-novel-name/
```

### Example

```bash
python main.py --link https://truyenfull.vn/nhan-cai-day-lan/
```

### Command-line Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--link` | `-l` | URL of the novel to crawl | Yes |

### Input Requirements

- Must provide a valid HTTPS or HTTP URL
- URL format: `https://domain.com/novel-name/`
- Supports multiple volumes automatically detected from the website

### Output

- Generated EPUB files are saved to: `output/{novel-name}/`
- Each volume creates a separate EPUB file
- Directory structure is automatically created if it doesn't exist

## How It Works

1. **URL Parsing**: Extracts domain and novel identifier from the provided URL
2. **Book Discovery**: Fetches the novel page and detects all available volumes
3. **Metadata Extraction**: Gathers title, author, and other book information
4. **Content Crawling**: Iterates through all chapters and extracts content
5. **EPUB Creation**: Compiles all chapters into properly formatted EPUB files
6. **Cleanup**: Removes temporary files after successful completion

## Project Structure

```
CrawlTruyen/
├── main.py              # Main crawler script
├── requirements.txt     # Python dependencies
├── epub.css            # CSS styling for EPUB files
├── LICENSE             # Project license
├── README.md           # This file
├── output/             # Generated EPUB files (created at runtime)
├── lib/                # Library files
└── bin/                # Binary/executable files
```

## Error Handling

The script includes comprehensive error handling:

- **Invalid URL**: Validates that the URL contains `http://` or `https://`
- **Network Errors**: Implements retry logic for failed requests
- **Parsing Errors**: Gracefully handles missing or malformed HTML
- **Temporary File Cleanup**: Automatically removes temporary files on error or interruption

### Common Error Messages

| Error | Solution |
|-------|----------|
| `URL KHONG HOP LE` | Ensure the URL starts with `http://` or `https://` |
| `Không tìm thấy thông tin chapter.` | Website structure may have changed; verify the URL works in browser |
| `Không tìm thấy thông tin book.` | Novel series structure not detected; check the website |

## Features in Detail

### Multi-Volume Support
The tool automatically:
- Detects all volumes in a series
- Creates separate EPUB files for each volume
- Maintains proper metadata for each volume

### Content Processing
- Removes advertisement tags and unnecessary markup
- Preserves formatting and text content
- Adds introduction chapters with book metadata
- Includes a signature crediting the crawler

### EPUB Standards Compliance
- Follows EPUB 3.0 standards
- Generates proper navigation files (NCX and NAV)
- Includes table of contents
- Supports Vietnamese language encoding

## Troubleshooting

**Script hangs or is slow**:
- Some websites may have rate limiting
- Check your internet connection
- Verify the website is accessible in your browser

**Generated EPUB won't open**:
- Try opening with a different e-reader application
- Verify the website structure hasn't changed
- Check console output for parsing errors

**Missing chapters**:
- The website structure may have changed
- Run the crawler again to retry
- Verify the source website has the chapters

## Keyboard Interrupt

Press `Ctrl+C` to cancel the operation. The script will:
- Clean up temporary files
- Display a cancellation message
- Exit gracefully

## Legal Notice

This tool is intended for personal use only. Ensure you have the right to download and convert the content. Always respect copyright laws and the terms of service of the source websites.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests to help improve this project.

## License

This project is provided under the MIT License. See the LICENSE file for details.

## Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for ensuring their use complies with applicable laws and the terms of service of the websites being accessed. The author assumes no liability for misuse or legal issues arising from the use of this tool.

## Author

**github@haxvzje**

## Support

If you encounter issues or have suggestions, please open an issue on GitHub or contact the repository maintainer.

---

**Note**: This tool may require updates if website structures change. Regular maintenance ensures compatibility with target websites.
