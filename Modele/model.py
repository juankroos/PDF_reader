from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import fitz  # PyMuPDF
import os

# Modèle Pydantic pour Pdf
class Pdf(BaseModel):
    path: str = Field(..., description="Chemin du fichier PDF")
    title: Optional[str] = Field(None, description="Titre du PDF")
    author: Optional[str] = Field(None, description="Auteur du PDF")
    date: Optional[datetime] = Field(None, description="Date de création du PDF")
    size: Optional[int] = Field(None, description="Taille du fichier en octets")
    creator: Optional[str] = Field(None, description="Créateur du PDF")
    page_count: Optional[int] = Field(None, description="Nombre total de pages")
    current_page: int = Field(0, description="Page actuelle (index 0 = page 1)")

    class Config:
        from_attributes = True

    def load_metadata(self):
        """Charge les métadonnées du PDF."""
        try:
            with fitz.open(self.path) as doc:
                info = doc.metadata
                self.title = info.get("title", "Inconnu")
                self.author = info.get("author", "Inconnu")
                self.date = info.get("creationDate", None)  # Conversion si nécessaire
                self.creator = info.get("creator", "Inconnu")
                self.page_count = len(doc)
                self.size = os.path.getsize(self.path)
        except Exception as e:
            print(f"Erreur lors du chargement des métadonnées : {e}")

    def load_pdf(self):
        """Ouvre le document PDF."""
        try:
            self.doc = fitz.open(self.path)
            return True
        except Exception as e:
            print(f"Erreur lors du chargement du PDF : {e}")
            return False

    def close_pdf(self):
        """Ferme le document PDF."""
        if hasattr(self, 'doc') and self.doc is not None:
            self.doc.close()
            self.doc = None

    def page_skip(self, page_number: int) -> Optional[bytes]:
        """Change la page actuelle et renvoie une image pour l'affichage."""
        if not self.load_pdf():
            return None
        if not (0 <= page_number < self.page_count):
            print(f"Page {page_number + 1} hors limites (1-{self.page_count})")
            return None
        try:
            self.current_page = page_number
            page = self.doc.load_page(page_number)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            return pix.tobytes()  # Retourne les bytes de l'image
        except Exception as e:
            print(f"Erreur lors du changement de page : {e}")
            return None

    def search_text(self, text: str) -> list:
        """Recherche un texte dans la page actuelle et renvoie les zones trouvées."""
        if not self.load_pdf() or self.current_page is None:
            print("Aucun document ou page chargée")
            return []
        try:
            page = self.doc.load_page(self.current_page)
            areas = page.search_for(text)
            return areas  # Liste de rectangles
        except Exception as e:
            print(f"Erreur lors de la recherche : {e}")
            return []

# Modèle Pydantic pour Word
class Word(BaseModel):
    path: str = Field(..., description="Chemin du fichier Word")
    title: Optional[str] = Field(None, description="Titre du document")
    author: Optional[str] = Field(None, description="Auteur du document")
    date: Optional[datetime] = Field(None, description="Date de création")
    size: Optional[int] = Field(None, description="Taille du fichier en octets")
    creator: Optional[str] = Field(None, description="Créateur du document")
    page_count: Optional[int] = Field(None, description="Nombre total de pages")
    current_page: int = Field(0, description="Page actuelle (index 0 = page 1)")

    class Config:
        from_attributes = True

    def load_metadata(self):
        """Charge les métadonnées du document Word (à implémenter)."""
        try:
            # Exemple : utiliser python-docx pour les métadonnées
            from docx import Document
            doc = Document(self.path)
            self.title = doc.core_properties.title or "Inconnu"
            self.author = doc.core_properties.author or "Inconnu"
            self.date = doc.core_properties.created
            self.creator = doc.core_properties.last_modified_by or "Inconnu"
            self.size = os.path.getsize(self.path)
            # Note : page_count nécessite une logique spécifique pour Word
        except Exception as e:
            print(f"Erreur lors du chargement des métadonnées : {e}")

    def load_document(self):
        """Charge le document Word (à implémenter)."""
        try:
            from docx import Document
            self.doc = Document(self.path)
            return True
        except Exception as e:
            print(f"Erreur lors du chargement du document : {e}")
            return False