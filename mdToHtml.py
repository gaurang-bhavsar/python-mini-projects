#!/usr/bin/env python3
"""
Markdown to HTML Converter - A simple utility to convert Markdown files to HTML
"""

import re
import sys
import argparse
from pathlib import Path


class MarkdownConverter:
    """
    A class to convert Markdown to HTML
    """
    
    def __init__(self):
        """Initialize the converter with regex patterns for Markdown elements"""
        # Regex patterns for Markdown elements
        self.patterns = {
            # Headers (h1 to h6)
            'headers': re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE),
            
            # Bold text
            'bold': re.compile(r'\*\*(.+?)\*\*'),
            
            # Italic text
            'italic': re.compile(r'\*(.+?)\*'),
            
            # Code blocks with language
            'code_block': re.compile(r'```(\w*)\n(.*?)\n```', re.DOTALL),
            
            # Inline code
            'inline_code': re.compile(r'`(.+?)`'),
            
            # Links
            'link': re.compile(r'\[(.+?)\]\((.+?)\)'),
            
            # Images
            'image': re.compile(r'!\[(.+?)\]\((.+?)\)'),
            
            # Unordered lists
            'unordered_list': re.compile(r'^[ \t]*[-*+]\s+(.+)$', re.MULTILINE),
            
            # Ordered lists
            'ordered_list': re.compile(r'^[ \t]*(\d+)\.\s+(.+)$', re.MULTILINE),
            
            # Horizontal rule
            'hr': re.compile(r'^([-*_])\1{2,}$', re.MULTILINE),
            
            # Blockquote
            'blockquote': re.compile(r'^>\s+(.+)$', re.MULTILINE),
            
            # Tables
            'table': re.compile(r'^\|(.+)\|$', re.MULTILINE),
            
            # Paragraphs (non-empty lines)
            'paragraph': re.compile(r'^(?!<h|<ul|<ol|<blockquote|<hr|<table|<pre)(.+)$', re.MULTILINE)
        }
    
    def _convert_headers(self, markdown):
        """Convert Markdown headers to HTML"""
        def replace_header(match):
            level = len(match.group(1))
            text = match.group(2)
            return f'<h{level}>{text}</h{level}>\n'
        
        return self.patterns['headers'].sub(replace_header, markdown)
    
    def _convert_bold(self, markdown):
        """Convert Markdown bold to HTML strong"""
        return self.patterns['bold'].sub(r'<strong>\1</strong>', markdown)
    
    def _convert_italic(self, markdown):
        """Convert Markdown italic to HTML em"""
        return self.patterns['italic'].sub(r'<em>\1</em>', markdown)
    
    def _convert_code_block(self, markdown):
        """Convert Markdown code blocks to HTML pre/code"""
        def replace_code_block(match):
            language = match.group(1)
            code = match.group(2)
            if language:
                return f'<pre><code class="language-{language}">{code}</code></pre>'
            return f'<pre><code>{code}</code></pre>'
        
        return self.patterns['code_block'].sub(replace_code_block, markdown)
    
    def _convert_inline_code(self, markdown):
        """Convert Markdown inline code to HTML code"""
        return self.patterns['inline_code'].sub(r'<code>\1</code>', markdown)
    
    def _convert_links(self, markdown):
        """Convert Markdown links to HTML a"""
        return self.patterns['link'].sub(r'<a href="\2">\1</a>', markdown)
    
    def _convert_images(self, markdown):
        """Convert Markdown images to HTML img"""
        return self.patterns['image'].sub(r'<img src="\2" alt="\1">', markdown)
    
    def _convert_unordered_lists(self, markdown):
        """Convert Markdown unordered lists to HTML ul/li"""
        # Find all list items
        list_items = self.patterns['unordered_list'].findall(markdown)
        
        if not list_items:
            return markdown
        
        # Replace with HTML list
        html_list = '<ul>\n'
        for item in list_items:
            html_list += f'  <li>{item}</li>\n'
        html_list += '</ul>\n'
        
        # Replace in the original markdown
        return self.patterns['unordered_list'].sub('', markdown) + html_list
    
    def _convert_ordered_lists(self, markdown):
        """Convert Markdown ordered lists to HTML ol/li"""
        # Find all list items
        list_items = self.patterns['ordered_list'].findall(markdown)
        
        if not list_items:
            return markdown
        
        # Replace with HTML list
        html_list = '<ol>\n'
        for _, item in list_items:
            html_list += f'  <li>{item}</li>\n'
        html_list += '</ol>\n'
        
        # Replace in the original markdown
        return self.patterns['ordered_list'].sub('', markdown) + html_list
    
    def _convert_horizontal_rule(self, markdown):
        """Convert Markdown horizontal rule to HTML hr"""
        return self.patterns['hr'].sub('<hr>', markdown)
    
    def _convert_blockquote(self, markdown):
        """Convert Markdown blockquote to HTML blockquote"""
        # Find all blockquote lines
        blockquote_lines = self.patterns['blockquote'].findall(markdown)
        
        if not blockquote_lines:
            return markdown
        
        # Replace with HTML blockquote
        html_blockquote = '<blockquote>\n'
        for line in blockquote_lines:
            html_blockquote += f'  <p>{line}</p>\n'
        html_blockquote += '</blockquote>\n'
        
        # Replace in the original markdown
        return self.patterns['blockquote'].sub('', markdown) + html_blockquote
    
    def _convert_tables(self, markdown):
        """Convert Markdown tables to HTML tables"""
        # This is a simplified implementation
        lines = markdown.split('\n')
        table_lines = []
        in_table = False
        
        for i, line in enumerate(lines):
            if line.startswith('|') and line.endswith('|'):
                if not in_table:
                    in_table = True
                    table_lines.append(i)
                table_lines.append(line)
            elif in_table:
                in_table = False
        
        if not table_lines:
            return markdown
        
        # Process table lines
        # This is a very basic implementation that would need to be expanded
        html_table = '<table>\n'
        html_table += '  <tr>\n'
        for cell in table_lines[0].strip('|').split('|'):
            html_table += f'    <th>{cell.strip()}</th>\n'
        html_table += '  </tr>\n'
        
        for line in table_lines[2:]:
            html_table += '  <tr>\n'
            for cell in line.strip('|').split('|'):
                html_table += f'    <td>{cell.strip()}</td>\n'
            html_table += '  </tr>\n'
        
        html_table += '</table>\n'
        
        # Replace in the original markdown
        # This is simplified and would need to be improved
        return markdown + html_table
    
    def _convert_paragraphs(self, markdown):
        """Convert plain text to HTML paragraphs"""
        lines = markdown.split('\n')
        html_lines = []
        current_paragraph = []
        
        for line in lines:
            if line.strip():
                current_paragraph.append(line)
            elif current_paragraph:
                html_lines.append(f'<p>{" ".join(current_paragraph)}</p>')
                current_paragraph = []
        
        if current_paragraph:
            html_lines.append(f'<p>{" ".join(current_paragraph)}</p>')
        
        return '\n'.join(html_lines)
    
    def convert(self, markdown):
        """
        Convert Markdown to HTML
        
        Args:
            markdown: Markdown text to convert
            
        Returns:
            HTML text
        """
        html = markdown
        
        # Apply conversions in order
        html = self._convert_headers(html)
        html = self._convert_bold(html)
        html = self._convert_italic(html)
        html = self._convert_code_block(html)
        html = self._convert_inline_code(html)
        html = self._convert_links(html)
        html = self._convert_images(html)
        html = self._convert_unordered_lists(html)
        html = self._convert_ordered_lists(html)
        html = self._convert_horizontal_rule(html)
        html = self._convert_blockquote(html)
        html = self._convert_tables(html)
        html = self._convert_paragraphs(html)
        
        return html
    
    def convert_file(self, input_file, output_file=None):
        """
        Convert a Markdown file to HTML
        
        Args:
            input_file: Path to the Markdown file
            output_file: Path to the output HTML file (optional)
            
        Returns:
            HTML text
        """
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown = f.read()
        
        html = self.convert(markdown)
        
        # Add HTML document structure
        html_document = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{input_path.stem}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }}
        code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        blockquote {{ border-left: 4px solid #ddd; padding-left: 10px; color: #666; }}
        img {{ max-width: 100%; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
        
        if output_file:
            output_path = Path(output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_document)
            print(f"HTML file created: {output_path}")
        
        return html_document


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Convert Markdown to HTML")
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("-o", "--output", help="Output HTML file (default: input file with .html extension)")
    
    args = parser.parse_args()
    
    try:
        converter = MarkdownConverter()
        
        input_path = Path(args.input)
        output_path = args.output if args.output else input_path.with_suffix('.html')
        
        converter.convert_file(input_path, output_path)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
