import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from azure_translator import Services

class MultilingualPDFGenerator:
    def __init__(self, font_dir):
        """
        Initialize PDF generator with directory containing font files
        """
        self.font_dir = font_dir
        self.font_map = {
            'hi': "NotoSansDevanagari-Regular.ttf",
            'mr': "NotoSansDevanagari-Regular.ttf",
            'gu': "NotoSansGujarati-Regular.ttf",
            'bn': "NotoSansBengali-Regular.ttf",
            'te': "NotoSansTelugu-Regular.ttf",
            'ta': "NotoSansTamil-Regular.ttf",
            'ur': "NotoSansArabic-Regular.ttf",
            'kn': "NotoSansKannada-Regular.ttf",
            'ml': "NotoSansMalayalam-Regular.ttf",
            'pa': "NotoSansGurmukhi-Regular.ttf",
            'ja': "NotoSansJP-Regular.ttf",
            'zh-cn': "NotoSansSC-Regular.ttf",
            'ar': "NotoSansArabic-Regular.ttf",
            'es': "NotoSans-Regular.ttf",  # Spanish
            'fr': "NotoSans-Regular.ttf",  # French
            'de': "NotoSans-Regular.ttf",  # German
            'it': "NotoSans-Regular.ttf"   # Italian
        }

        self.register_fonts()
    def wrap_cjk_text(self, text, c, font_name, font_size, max_width):
        """
        Special text wrapping for CJK (Chinese, Japanese, Korean) text.
        Returns an array of lines that fit within max_width.
        """
        lines = []
        current_line = ""
        
        for char in text:
            test_line = current_line + char
            # Check if adding this character exceeds the line width
            if c.stringWidth(test_line, font_name, font_size) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = char
        
        # Add the last line if there's any text remaining
        if current_line:
            lines.append(current_line)
        
        return lines
    def register_fonts(self):
        """
        Register all fonts with reportlab
        """
        for lang, font_file in self.font_map.items():
            font_path = os.path.join(self.font_dir, font_file)
            try:
                # Create a font identifier without spaces
                font_name = f"Noto_{lang}"
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                print(f"Registered font for {lang}: {font_name}")
            except Exception as e:
                print(f"Error registering font for {lang}: {str(e)}")

    def create_pdfs(self, translations_dict, output_dir):
        """
        Creates language-specific PDFs with the translated text.

        Args:
            translations_dict (dict): A dictionary where keys are language codes and values are translations
            output_dir (str): Directory to save the output PDFs
        """
        os.makedirs(output_dir, exist_ok=True)

        def wrap_cjk_text(text, c, font_name, font_size, max_width):
            lines = []
            current_line = ""
            for char in text:
                test_line = current_line + char
                if c.stringWidth(test_line, font_name, font_size) <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = char
            if current_line:
                lines.append(current_line)
            return lines

        for lang, translation in translations_dict.items():
            output_filename = os.path.join(output_dir, f"translation_{lang}.pdf")
            
            try:
                # Create PDF
                c = canvas.Canvas(output_filename, pagesize=A4)
                width, height = A4

                # Set font
                if lang=='zh-Hans':
                    lang='zh-cn'
                font_name = f"Noto_{lang}"
                c.setFont(font_name if lang in self.font_map else "Helvetica", 12)

                # Text formatting parameters
                margin = 50
                y = height - margin
                x = margin
                line_height = 14
                max_width = width - (2 * margin)

                if lang in ['ja', 'zh-cn']:
                    # CJK text handling
                    lines = wrap_cjk_text(translation, c, font_name, 12, max_width)
                    for line in lines:
                        if y < margin + line_height:
                            c.showPage()
                            y = height - margin
                            c.setFont(font_name, 12)
                        c.drawString(x, y, line)
                        y -= line_height
                else:
                    # Regular text handling
                    words = translation.split()
                    current_line = []
                    
                    for word in words:
                        current_line.append(word)
                        line = " ".join(current_line)
                        
                        if c.stringWidth(line, font_name, 12) > max_width:
                            current_line.pop()
                            final_line = " ".join(current_line)
                            
                            if y < margin + line_height:
                                c.showPage()
                                y = height - margin
                                c.setFont(font_name, 12)
                            
                            c.drawString(x, y, final_line)
                            y -= line_height
                            current_line = [word]
                    
                    # Print the last line if any words remain
                    if current_line:
                        final_line = " ".join(current_line)
                        if y < margin + line_height:
                            c.showPage()
                            y = height - margin
                            c.setFont(font_name, 12)
                        c.drawString(x, y, final_line)

                c.save()
                print(f"Successfully created {output_filename}")
                
            except Exception as e:
                print(f"Error creating PDF for {lang}: {str(e)}")

def main():
    # Initialize the Azure translator service
    translator = Services()

    # Example text to translate
    text = """
In the mid-19th century, the Opium Wars with Britain and France forced China to pay compensation, open treaty ports, allow extraterritoriality for foreign nationals, and cede Hong Kong to the British under the 1842 Treaty of Nanking, the first of what have been termed as the "unequal treaties". The First Sino-Japanese War (1894–1895) resulted in Qing China's loss of influence in the Korean Peninsula, as well as the cession of Taiwan to Japan. The Qing dynasty also began experiencing internal unrest in which tens of millions of people died, especially in the White Lotus Rebellion, the failed Taiping Rebellion that ravaged southern China in the 1850s and 1860s and the Dungan Revolt (1862–1877) in the northwest. The initial success of the Self-Strengthening Movement of the 1860s was frustrated by a series of military defeats in the 1880s and 1890s.

In the 19th century, the great Chinese diaspora began. Losses due to emigration were added to by conflicts and catastrophes such as the Northern Chinese Famine of 1876–1879, in which between 9 and 13 million people died. The Guangxu Emperor drafted a reform plan in 1898 to establish a modern constitutional monarchy, but these plans were thwarted by the Empress Dowager Cixi. The ill-fated anti-foreign Boxer Rebellion of 1899–1901 further weakened the dynasty. Although Cixi sponsored a program of reforms known as the late Qing reforms, the Xinhai Revolution of 1911–1912 ended the Qing dynasty and established the Republic of China. Puyi, the last Emperor, abdicated in 1912.
"""

    
    # Get translations
    initial_translation = translator.translate_transcript(text)
    translations = translator.multilingual(initial_translation)
    
    # Set up paths
    font_dir = "/home/muhd/Ai-Board-YIC/3. ml features/2. Video To Transcript with Trl"  # Update this path
    output_dir = os.path.join(os.getcwd(), "output")
    
    # Create and generate PDFs
    pdf_generator = MultilingualPDFGenerator(font_dir)
    pdf_generator.create_pdfs(translations, output_dir)

if __name__ == "__main__":
    main()