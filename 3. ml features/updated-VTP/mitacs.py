import fitz
import os
from azure_translator import Services



class X:

    def __init__(self, font_dir):
        """
        Initialize font manager with directory containing font files
        """
        self.font_dir = font_dir
        self.loaded_fonts = {}
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
            'ar': "NotoSansArabic-Regular.ttf"
        }
        
    def load_fonts(self):
        """
        Load all fonts from the font directory and register them with PyMuPDF
        """
        for lang, font_file in self.font_map.items():
            font_path = os.path.join(self.font_dir, font_file)
            try:
                # Register font with PyMuPDF
                font = fitz.Font(fontfile=font_path)
                # Store the actual font name (from the font file) for this language
                self.loaded_fonts[lang] = font.name.replace(" ", "_")
                print(f"Loaded font for {lang}: {font}")
            except Exception as e:
                print(f"Error loading font for {lang}: {str(e)}")
    
    def get_font_name(self, lang):
        """
        Get the loaded font name for a language
        """
        return self.loaded_fonts.get(lang)  # fallback to helvetica if not found
    def make_pdfs(self,translations_dict, original_pdf_name):
        """
        Creates language-specific PDFs by overwriting each page of the original PDF
        with the translated text for each language.

        Args:
            translations_dict (dict): A dictionary where keys are language codes and values are translations.
            original_pdf_name (str): The path to the original PDF file.

        Returns:
            None
        """
        for lang, translation in translations_dict.items():
            # Create output filename
            pdf_base_name = os.path.splitext(original_pdf_name)[0]
            output_filename = f"{lang}_{pdf_base_name}.pdf"

            # Open the original PDF document
            doc = fitz.open(original_pdf_name)
            font_name = self.get_font_name(lang)
            print(font_name)


            # Process each page in the document
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Clear the page and insert the translation text
                page.clean_contents()  # Clears existing content
                page.insert_textbox(
                    fitz.Rect(50, 50, page.rect.width - 50, page.rect.height - 50),  # Leave margins
                    translation,
                    fontsize=12,
                    fontname=font_name,
                    color=(0, 0, 0),
                    align=fitz.TEXT_ALIGN_LEFT
                )
            
            try:
                # Save the translated PDF
                doc.save(output_filename)
                print(f"Successfully created {output_filename}")
            except Exception as e:
                print(f"Error saving {output_filename}: {str(e)}")
            finally:
                doc.close()





if __name__ == "__main__":
    A=Services()

    text="I would really like to drive your car around the block a few times!"
    B=A.translate_transcript(text)
    C=A.multilingual(B)
    print(C)
    output_dir = os.path.join(os.getcwd(), "output")
    base_filename = "translated"
    translation_file = os.path.join(output_dir, f"{base_filename}.pdf")
    x=X("/home/muhd/Ai-Board-YIC/3. ml features/2. Video To Transcript with Trl")    
    x.load_fonts()
    x.make_pdfs(C,f"{base_filename}.pdf")